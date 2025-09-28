# SAT Problem Bank Specification

Each SAT practice problem lives in its own Markdown file with YAML front matter that encodes metadata used for indexing, tagging, and analytics. Use the template below when authoring new problems.

```yaml
---
id: sat-alg-001
topic: Algebra
subtopic: Quadratics
skill: Discriminant
difficulty: 2   # 1–5
tags: [dsat, functions]
answer: C
seed: 42
---
## Prompt
(problem text)

## Choices
A) ...
B) ...
C) ...
D) ...

<details><summary>Solution</summary>
(steps + final)
</details>
```

## Authoring Notes
- Place each file under `docs/sat/problem-bank/` and keep filenames aligned with the `id` (e.g., `sat-alg-001.md`).
- Keep prompts concise and reference only one primary skill.
- Use the collapsible solution pattern from the repository `README` for worked steps.

## Automation
- Run `python scripts/build_problem_index.py` after adding or editing problems to regenerate the index and tag pages.
- Execute `python scripts/validate_problem_bank.py` before committing changes to ensure required metadata is present.
