from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


class ProblemParseError(Exception):
    """Raised when a problem file is missing required metadata."""


@dataclass(frozen=True)
class Problem:
    id: str
    topic: str
    subtopic: str
    skill: str
    difficulty: int
    tags: List[str]
    answer: str
    seed: int
    file_path: Path
    docs_root: Path

    @property
    def bank_root(self) -> Path:
        for parent in self.file_path.parents:
            if parent.name == "problem-bank":
                return parent
        raise ProblemParseError(f"Could not locate problem-bank directory for {self.file_path}")

    @property
    def relative_to_bank(self) -> Path:
        return self.file_path.relative_to(self.bank_root)


REQUIRED_FIELDS = {
    "id",
    "topic",
    "subtopic",
    "skill",
    "difficulty",
    "tags",
    "answer",
    "seed",
}


def parse_front_matter(content: str) -> tuple[dict[str, object], int]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ProblemParseError("File must start with front matter delimited by ---")

    data: dict[str, object] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return data, index + 1
        if not line.strip():
            continue
        key, _, raw_value = line.partition(":")
        if not _:
            raise ProblemParseError(f"Invalid front matter line: {line}")
        key = key.strip()
        value = raw_value.split("#", 1)[0].strip()
        if key == "tags":
            if not value.startswith("[") or not value.endswith("]"):
                raise ProblemParseError("tags must be a list formatted as [tag1, tag2]")
            tag_body = value[1:-1].strip()
            if tag_body:
                tags = [segment.strip().strip("\"'") for segment in tag_body.split(",")]
            else:
                tags = []
            data[key] = [tag for tag in tags if tag]
        elif key in {"difficulty", "seed"}:
            if not value:
                raise ProblemParseError(f"{key} must have a value")
            data[key] = int(value)
        else:
            data[key] = value
    raise ProblemParseError("Front matter not closed with ---")


def load_problems(docs_root: Path) -> list[Problem]:
    problems: list[Problem] = []
    search_pattern = "**/problem-bank/**/*.md"
    for file_path in docs_root.glob(search_pattern):
        if file_path.name in {"README.md", "index.md"}:
            continue
        text = file_path.read_text(encoding="utf-8")
        if not text.lstrip().startswith("---"):
            continue
        try:
            meta, _ = parse_front_matter(text)
        except ProblemParseError as error:
            raise ProblemParseError(f"{file_path}: {error}") from error
        missing = REQUIRED_FIELDS.difference(meta)
        if missing:
            raise ProblemParseError(f"{file_path} missing required fields: {', '.join(sorted(missing))}")
        problem = Problem(
            id=str(meta["id"]),
            topic=str(meta["topic"]),
            subtopic=str(meta["subtopic"]),
            skill=str(meta["skill"]),
            difficulty=int(meta["difficulty"]),
            tags=[str(tag) for tag in meta["tags"]],
            answer=str(meta["answer"]),
            seed=int(meta["seed"]),
            file_path=file_path,
            docs_root=docs_root,
        )
        problems.append(problem)
    return problems


def dedupe_ids(problems: Iterable[Problem]) -> None:
    seen: dict[str, Path] = {}
    for problem in problems:
        if problem.id in seen:
            raise ProblemParseError(
                f"Duplicate problem id '{problem.id}' found in {problem.file_path} and {seen[problem.id]}"
            )
        seen[problem.id] = problem.file_path


__all__ = ["Problem", "ProblemParseError", "load_problems", "dedupe_ids", "REQUIRED_FIELDS"]
