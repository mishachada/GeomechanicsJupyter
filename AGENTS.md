# Teaching Hub Agent Guide

## Coding Conventions
- Prefer Python 3.10+ features but remain compatible with 3.9.
- Use type hints in new Python scripts and keep functions pure where practical.
- For JavaScript in docs/demos, write accessible, semantic markup and inline ES modules without bundlers.
- Follow Markdown lint best practices: use ATX headings, wrap math in `$$` for block expressions, and keep line length under 100 characters when reasonable.
- When editing notebooks, keep execution counts sequential and clear all large outputs.

## Folder Intent
- `docs/` contains the MkDocs content for the public site. Subdirectories map to topical areas, demos, dashboards, and supporting assets.
- `scripts/` holds automation utilities such as problem index builders and data refresh tooling.
- `.github/workflows/` defines CI/CD automation, including site deployment and optional data refresh jobs.
- `docs/data/` stores small, non-sensitive CSVs consumed by dashboards or demos.
- `docs/demos/` houses fully client-side interactive examples that should not require a build process.

## Acceptance Criteria Snapshot
- MkDocs Material site builds locally via `mkdocs serve`.
- Problem bank pages include front matter and are indexed automatically by `scripts/build_problem_index.py`.
- Interactive demos must be keyboard accessible and announce dynamic updates via `aria-live` regions.
- The dashboard reads local CSV data and renders charts using CDN-hosted libraries only.
- Workflows should be safe to run without secret configuration; data refresh must no-op when no source URL is provided.
- Update `CHANGELOG.md` with each phase to document progress.

## Decisions & TODOs
- Formatting is standardized via Black, Ruff, and Prettier (`pyproject.toml`, `.prettierrc.json`). Run these tools before committing substantial changes.
- Scheduled data refresh reads from `SAT_DATA_SOURCE_URL`; set the secret in repository settings when connecting to a live data source.
- GitHub Pages deployment relies on the Material theme — if extra plugins are added, update `pages.yml` to install them.
- Future work: expand the problem bank, flesh out AP Physics lab content, and capture screenshots of demos/dashboard once Pages is live for PR updates.
