from __future__ import annotations

from pathlib import Path

from problem_bank import REQUIRED_FIELDS, ProblemParseError, dedupe_ids, load_problems


def main() -> None:
    docs = Path(__file__).resolve().parents[1] / "docs"
    try:
        problems = load_problems(docs)
        if not problems:
            raise SystemExit("No problem files found.")
        dedupe_ids(problems)
        for problem in problems:
            if problem.difficulty < 1 or problem.difficulty > 5:
                raise ProblemParseError(
                    f"{problem.file_path} has difficulty {problem.difficulty}; expected value between 1 and 5."
                )
            if problem.answer.upper() not in {"A", "B", "C", "D", "E"}:
                raise ProblemParseError(
                    f"{problem.file_path} has answer '{problem.answer}'; expected one of A/B/C/D/E."
                )
            if not problem.tags:
                raise ProblemParseError(f"{problem.file_path} must include at least one tag.")
    except ProblemParseError as error:
        raise SystemExit(f"Problem validation failed: {error}") from error
    missing_fields = REQUIRED_FIELDS - {"tags"}
    print(f"Validated {len(problems)} problems. Required fields present: {', '.join(sorted(missing_fields))} + tags.")


if __name__ == "__main__":
    main()
