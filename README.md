# Teaching Hub (WIP)

This repository powers a public-facing hub for SAT Math and AP Physics resources. Content is published with MkDocs Material on GitHub Pages and includes guides, problem banks, interactive demos, dashboards, and notebooks.

## Quickstart
1. Install Python tooling (MkDocs, notebook renderer, lint, and tests):
   ```bash
   pip install mkdocs-material mkdocs-jupyter black ruff pytest
   ```
2. Regenerate the problem index after editing problems:
   ```bash
   python scripts/build_problem_index.py
   ```
3. Serve the site locally:
   ```bash
   mkdocs serve
   ```
4. Run quality checks:
   ```bash
   ruff check scripts tests
   black --check scripts tests
   pytest
   ```

## Authoring Guide
### SAT Problem Specification
- Each problem lives under `docs/sat/problem-bank/` and follows the front-matter template documented in [`docs/sat/problem-bank/README.md`](docs/sat/problem-bank/README.md).
- Use the collapsible solution snippet for worked answers:

```
   <details><summary>Solution</summary>
   Your steps here.
   </details>
```

- Rebuild the index (`python scripts/build_problem_index.py`) and validate metadata (`python scripts/validate_problem_bank.py`) before committing.

### Adding Interactive Demos
- Place standalone HTML files in `docs/demos/` with inline ES modules and accessible controls (labels plus `aria-live` regions for updates).
- Link new demos from `docs/demos/index.md` and update the MkDocs navigation in `mkdocs.yml`.
- Include a "Copy problem to clipboard" helper so teachers can port the prompt into worksheets quickly.

### Adding Notebooks
- Drop notebooks into `docs/notebooks/` and tag computational cells with `hide-input` so mkdocs-jupyter collapses code by default.
- Preview locally with `mkdocs serve` to verify math rendering, then list the notebook on `docs/notebooks/index.md`.

## Data & Automation
- Synthetic dashboard data lives at `docs/data/sat_practice_scores.csv`. Replace it with anonymized aggregates that keep the same headers to update charts.
- `scripts/refresh_data.py` refreshes the CSV when the `SAT_DATA_SOURCE_URL` environment variable is set (for example, a published Google Sheet CSV URL). The script exits quietly when the variable is missing, making it safe for scheduled runs.
- A nightly GitHub Actions workflow (`.github/workflows/refresh_data.yml`) runs at 02:00 UTC, commits any new dataset changes, and triggers a site rebuild.

## Deployment & Domains
- `.github/workflows/pages.yml` builds the MkDocs site on pushes to `main` and deploys to GitHub Pages using the official actions pipeline.
- Configure the repository’s **Settings → Pages** panel to point at the `github-pages` environment (created automatically by the workflow).
- To enable a custom domain, add a `CNAME` file under `docs/` with the desired domain and configure DNS records per GitHub’s Pages documentation.
- The live site will publish to `https://<your-username>.github.io/teaching-hub/` once Pages is enabled.

## Repository Layout
- `docs/` — Markdown content, demos, notebooks, and small datasets served by MkDocs.
- `scripts/` — Automation utilities for indexing problems and refreshing datasets.
- `.github/workflows/` — Continuous integration, deployment, and nightly refresh pipelines.

## Math Typesetting
KaTeX is loaded via CDN in `mkdocs.yml` (`katex.min.css`, `katex.min.js`, and `auto-render.min.js`) with an initializer at `docs/js/katex-init.js`. Author math using `$...$` for inline expressions and `$$...$$` for display mode.

## Licensing & Privacy
- Code is released under the [MIT License](LICENSE_CODE).
- Written content (guides, problems, notes) is shared under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 License](LICENSE_CONTENT).
- Only upload synthetic or anonymized aggregates; never commit student personally identifiable information.
