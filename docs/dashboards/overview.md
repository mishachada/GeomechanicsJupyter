# SAT Practice Dashboard

Track practice trends across SAT sections using the lightweight charts below. Select a section to focus the analysis.

<div class="dashboard-controls">
  <label for="section-filter">Section</label>
  <select id="section-filter" aria-describedby="filter-hint"></select>
  <span id="filter-hint" class="hint">Charts update instantly when you change the section.</span>
</div>

<div class="dashboard-grid">
  <figure>
    <figcaption>Rolling Average (3-sample)</figcaption>
    <canvas id="rolling-chart" height="280" role="img" aria-label="Line chart of rolling average scores."></canvas>
  </figure>
  <figure>
    <figcaption>Score Distribution</figcaption>
    <canvas id="distribution-chart" height="280" role="img" aria-label="Bar chart showing score distribution."></canvas>
  </figure>
</div>

<p class="dashboard-summary" aria-live="polite" aria-atomic="true" id="dashboard-summary">Loading dashboard data…</p>

<style>
  .dashboard-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    align-items: center;
    background: #ffffff;
    border-radius: 0.75rem;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
    margin-bottom: 1.5rem;
  }
  .dashboard-controls label {
    font-weight: 600;
  }
  .dashboard-controls select {
    font: inherit;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    border: 1px solid #cbd5f5;
  }
  .hint {
    font-size: 0.9rem;
    color: #334155;
  }
  .dashboard-grid {
    display: grid;
    gap: 1.5rem;
  }
  @media (min-width: 768px) {
    .dashboard-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }
  figure {
    background: #ffffff;
    border-radius: 0.75rem;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
  }
  figcaption {
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  .dashboard-summary {
    margin-top: 1.5rem;
    font-size: 1rem;
    color: #0b7285;
  }
</style>

<script type="module">
  import { Chart, registerables } from "https://cdn.jsdelivr.net/npm/chart.js@4.4.6/dist/chart.esm.js";

  Chart.register(...registerables);

  const sectionFilter = document.getElementById("section-filter");
  const summary = document.getElementById("dashboard-summary");
  const rollingCanvas = document.getElementById("rolling-chart");
  const distributionCanvas = document.getElementById("distribution-chart");
  let rollingChart;
  let distributionChart;
  let records = [];

  async function loadData() {
    try {
      const response = await fetch("../data/sat_practice_scores.csv");
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }
      const text = await response.text();
      records = parseCsv(text);
      populateFilter();
      if (!sectionFilter.value) {
        summary.textContent = "No sections available in the dataset.";
        sectionFilter.disabled = true;
        return;
      }
      sectionFilter.disabled = false;
      updateCharts(sectionFilter.value);
    } catch (error) {
      console.error(error);
      summary.textContent = "Unable to load dashboard data right now.";
      sectionFilter.disabled = true;
    }
  }

  function parseCsv(text) {
    const lines = text.trim().split("\n");
    const headers = lines.shift().split(",");
    return lines.map((line) => {
      const values = line.split(",");
      const entry = {};
      headers.forEach((header, index) => {
        entry[header] = values[index];
      });
      entry.date = new Date(entry.date);
      entry.score = Number.parseInt(entry.score, 10);
      return entry;
    });
  }

  function populateFilter() {
    const sections = Array.from(new Set(records.map((record) => record.section))).sort();
    sectionFilter.innerHTML = sections
      .map((section) => `<option value="${section}">${section}</option>`)
      .join("");
    if (!sections.length) {
      sectionFilter.innerHTML = "";
    }
  }

  function computeRollingAverage(section, windowSize = 3) {
    const filtered = records
      .filter((record) => record.section === section)
      .sort((a, b) => a.date - b.date);
    const groupedByDate = new Map();
    filtered.forEach((record) => {
      const key = record.date.toISOString().slice(0, 10);
      if (!groupedByDate.has(key)) {
        groupedByDate.set(key, []);
      }
      groupedByDate.get(key).push(record.score);
    });
    const daily = Array.from(groupedByDate.entries()).map(([date, scores]) => ({
      date,
      average: scores.reduce((sum, value) => sum + value, 0) / scores.length,
    }));
    daily.sort((a, b) => new Date(a.date) - new Date(b.date));
    const rolling = daily.map((entry, index) => {
      const window = daily.slice(Math.max(0, index - windowSize + 1), index + 1);
      const mean = window.reduce((sum, item) => sum + item.average, 0) / window.length;
      return { date: entry.date, value: Number.parseFloat(mean.toFixed(1)) };
    });
    return rolling;
  }

  function buildDistribution(section) {
    const filtered = records.filter((record) => record.section === section);
    const buckets = new Map();
    filtered.forEach((record) => {
      const key = record.score;
      buckets.set(key, (buckets.get(key) || 0) + 1);
    });
    const sorted = Array.from(buckets.entries()).sort((a, b) => a[0] - b[0]);
    return {
      labels: sorted.map(([score]) => score.toString()),
      counts: sorted.map(([, count]) => count),
    };
  }

  function renderRolling(section) {
    const rolling = computeRollingAverage(section);
    const labels = rolling.map((entry) => entry.date);
    const data = rolling.map((entry) => entry.value);
    if (rollingChart) {
      rollingChart.destroy();
    }
    if (!labels.length) {
      return false;
    }
    rollingChart = new Chart(rollingCanvas, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: `${section} rolling average`,
            data,
            tension: 0.3,
            borderColor: "#2563eb",
            backgroundColor: "rgba(37, 99, 235, 0.15)",
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            suggestedMin: 500,
            suggestedMax: 650,
          },
        },
      },
    });
    return true;
  }

  function renderDistribution(section) {
    const distribution = buildDistribution(section);
    if (distributionChart) {
      distributionChart.destroy();
    }
    if (!distribution.labels.length) {
      return false;
    }
    distributionChart = new Chart(distributionCanvas, {
      type: "bar",
      data: {
        labels: distribution.labels,
        datasets: [
          {
            label: `${section} score counts`,
            data: distribution.counts,
            backgroundColor: "rgba(16, 185, 129, 0.6)",
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: { display: true, text: "Score" },
          },
          y: {
            beginAtZero: true,
            title: { display: true, text: "Students" },
          },
        },
        plugins: {
          legend: { display: false },
        },
      },
    });
    return true;
  }

  function updateSummary(section, { hasRolling, hasDistribution }) {
    const filtered = records.filter((record) => record.section === section);
    if (!filtered.length) {
      summary.textContent = `No data available for ${section}.`;
      return;
    }
    if (!hasRolling) {
      summary.textContent = `${section} does not have enough data for a rolling average.`;
      return;
    }
    if (!hasDistribution) {
      summary.textContent = `${section} does not have any recorded scores yet.`;
      return;
    }
    const average =
      filtered.reduce((sum, record) => sum + record.score, 0) / filtered.length;
    summary.textContent = `${section} section average score is ${average.toFixed(
      1
    )} across ${filtered.length} practice results.`;
  }

  function updateCharts(section) {
    const hasRolling = renderRolling(section);
    const hasDistribution = renderDistribution(section);
    updateSummary(section, { hasRolling, hasDistribution });
  }

  sectionFilter.addEventListener("change", (event) => {
    updateCharts(event.target.value);
  });

  loadData();
</script>

> **Tip:** Replace the CSV at `docs/data/sat_practice_scores.csv` with anonymized aggregated data to refresh the charts. Keep the headers identical for the scripts above to work without modification.
