from __future__ import annotations

from pathlib import Path

import pytest

from problem_bank import ProblemParseError, load_problems


def write_problem(tmp_path: Path, content: str) -> Path:
    docs_root = tmp_path / "docs"
    bank_dir = docs_root / "sat" / "problem-bank"
    bank_dir.mkdir(parents=True)
    problem_path = bank_dir / "sample.md"
    problem_path.write_text(content, encoding="utf-8")
    return docs_root


def test_load_problems_parses_valid_front_matter(tmp_path: Path) -> None:
    docs_root = write_problem(
        tmp_path,
        """---\nid: demo-001\ntopic: Algebra\nsubtopic: Linear\nskill: Intercepts\ndifficulty: 2\ntags: [demo, algebra]\nanswer: A\nseed: 10\n---\n<a id=\"demo-001\"></a>\n## Prompt\nExample.\n""",
    )
    problems = load_problems(docs_root)
    assert len(problems) == 1
    assert problems[0].id == "demo-001"
    assert problems[0].tags == ["demo", "algebra"]


def test_load_problems_rejects_missing_field(tmp_path: Path) -> None:
    docs_root = write_problem(
        tmp_path,
        """---\nid: demo-002\ntopic: Algebra\nsubtopic: Linear\nskill: Intercepts\ndifficulty: 2\nanswer: A\nseed: 12\n---\n<a id=\"demo-002\"></a>\n## Prompt\nExample.\n""",
    )
    with pytest.raises(ProblemParseError):
        load_problems(docs_root)
