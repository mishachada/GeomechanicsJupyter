# Changelog

## Phase 0 - Scan & Prep
- Created initial project scaffolding directories for documentation, scripts, data, and automation.
- Added repository-wide agent guide outlining conventions and acceptance criteria.
- Introduced licensing structure separating code (MIT) and content (CC BY-NC-SA 4.0).
- Configured base .gitignore for common local artifacts.

## Phase 1 - Site Scaffold
- Added MkDocs configuration using the Material theme with math rendering support via KaTeX.
- Seeded initial pages for the landing, about, SAT guide, AP Physics unit, and placeholder sections.
- Documented math authoring guidance and collapsible solution snippets in the README.
- Created KaTeX initialization script within the docs assets.

## Phase 2 - Problem Bank Automation
- Defined the SAT problem front-matter specification and authoring workflow documentation.
- Added three sample SAT problems with metadata-rich front matter and solutions.
- Implemented automated index and tag generation via `scripts/build_problem_index.py`.
- Introduced `scripts/validate_problem_bank.py` for pre-commit metadata validation.
- Generated the initial problem index and tag pages.

## Phase 3 - Interactive Demos
- Built discriminant, CLT simulator, and projectile motion demos with accessible controls and clipboard prompts.
- Added inline ES module scripts for live visualization (SVG, Chart.js, and Canvas).
- Updated MkDocs navigation and demo landing page to surface new experiences.

## Phase 4 - Notebook Integration
- Added a Fourier series demo notebook with hidden code cells rendered via mkdocs-jupyter.
- Documented the notebook entry point on the notebooks landing page.

## Phase 5 - Data Dashboard
- Added a synthetic SAT practice scores CSV powering analytics views.
- Built a dashboard page with Chart.js visualizations (rolling averages and distributions) plus a section filter.
- Documented dataset usage within the data index.
- Hardened the dashboard script to handle missing data and fetch failures gracefully for
  better accessibility.

## Phase 6 - Nightly Refresh Pipeline
- Added a configurable refresh script that syncs the practice scores CSV when an environment URL is provided.
- Created a scheduled GitHub Actions workflow to run nightly, commit updates, and keep Pages content fresh.

## Phase 7 - GitHub Pages Deploy
- Added a Pages workflow to build the MkDocs site on pushes to main and manual triggers.
- Configured deployment to GitHub Pages via the official actions pipeline with strict builds.

## Phase 8 - Quality & Testing
- Added formatting configuration for Black, Ruff, and Prettier to standardize code style.
- Introduced unit tests for the problem bank parser and documented pytest settings.

## Phase 9 - Documentation & Handoff
- Expanded the README with quickstart commands, authoring guidance, automation notes, and deployment steps.
- Documented formatting/testing decisions and future tasks in `AGENTS.md`.

