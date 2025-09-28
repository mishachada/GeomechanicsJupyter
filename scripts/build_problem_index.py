from __future__ import annotations

import os
from collections import defaultdict
from pathlib import Path

from problem_bank import Problem, ProblemParseError, dedupe_ids, load_problems


def docs_root() -> Path:
    return Path(__file__).resolve().parents[1] / "docs"


def format_tags(tags: list[str]) -> str:
    return ", ".join(tags) if tags else "—"


def build_topic_tables(problems: list[Problem]) -> dict[str, dict[str, list[Problem]]]:
    grouped: dict[str, dict[str, list[Problem]]] = defaultdict(lambda: defaultdict(list))
    for problem in problems:
        grouped[problem.topic][problem.subtopic].append(problem)
    for topic in grouped:
        for subtopic in grouped[topic]:
            grouped[topic][subtopic].sort(key=lambda prob: prob.id)
    return dict(sorted(grouped.items(), key=lambda item: item[0].lower()))


def write_index(bank_root: Path, problems: list[Problem]) -> None:
    index_lines: list[str] = ["# SAT Problem Index", ""]
    grouped = build_topic_tables(problems)
    for topic, subtopics in grouped.items():
        index_lines.append(f"## {topic}")
        index_lines.append("")
        for subtopic, entries in sorted(subtopics.items(), key=lambda item: item[0].lower()):
            index_lines.append(f"### {subtopic}")
            index_lines.append("")
            index_lines.append("| ID | Skill | Difficulty | Tags | Answer |")
            index_lines.append("| --- | --- | --- | --- | --- |")
            for problem in entries:
                relative = problem.relative_to_bank.as_posix()
                link = f"[{problem.id}]({relative}#{problem.id})"
                index_lines.append(
                    f"| {link} | {problem.skill} | {problem.difficulty} | {format_tags(problem.tags)} | {problem.answer} |"
                )
            index_lines.append("")
    (bank_root / "index.md").write_text("\n".join(index_lines).strip() + "\n", encoding="utf-8")


def write_tag_pages(bank_root: Path, problems: list[Problem]) -> None:
    tag_dir = bank_root / "tags"
    tag_dir.mkdir(exist_ok=True)
    tags: dict[str, list[Problem]] = defaultdict(list)
    for problem in problems:
        for tag in problem.tags:
            tags[tag].append(problem)
    for tag_problems in tags.values():
        tag_problems.sort(key=lambda prob: prob.id)
    for tag in sorted(tags):
        tag_path = tag_dir / f"{tag}.md"
        lines = [f"# Tag: {tag}", "", "| Problem | Topic | Subtopic | Skill | Difficulty | Answer |", "| --- | --- | --- | --- | --- | --- |"]
        for problem in tags[tag]:
            relative = os.path.relpath(problem.file_path, start=tag_path.parent)
            link = f"[{problem.id}]({relative.replace(os.sep, '/')}#{problem.id})"
            lines.append(
                f"| {link} | {problem.topic} | {problem.subtopic} | {problem.skill} | {problem.difficulty} | {problem.answer} |"
            )
        lines.append("")
        tag_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def build_indexes() -> None:
    root = docs_root()
    problems = load_problems(root)
    if not problems:
        raise SystemExit("No problems found to index.")
    dedupe_ids(problems)
    banks: dict[Path, list[Problem]] = defaultdict(list)
    for problem in problems:
        banks[problem.bank_root].append(problem)
    for bank_root, bank_problems in banks.items():
        write_index(bank_root, bank_problems)
        write_tag_pages(bank_root, bank_problems)


if __name__ == "__main__":
    try:
        build_indexes()
    except ProblemParseError as error:
        raise SystemExit(f"Error: {error}")
