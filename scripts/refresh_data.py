from __future__ import annotations

import os
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

TARGET_PATH = Path(__file__).resolve().parents[1] / "docs" / "data" / "sat_practice_scores.csv"
ENV_VAR = "SAT_DATA_SOURCE_URL"


def fetch_csv(url: str) -> str:
    with urlopen(url) as response:  # nosec B310 - trusted URL provided by maintainer
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)


def main() -> None:
    source_url = os.environ.get(ENV_VAR)
    if not source_url:
        print(f"{ENV_VAR} is unset; exiting without refreshing data.")
        return

    try:
        csv_text = fetch_csv(source_url).strip()
    except URLError as error:
        raise SystemExit(f"Failed to fetch CSV from {source_url}: {error}")

    if not csv_text:
        raise SystemExit("Fetched CSV is empty; aborting.")

    existing = TARGET_PATH.read_text(encoding="utf-8").strip() if TARGET_PATH.exists() else ""
    if existing == csv_text:
        print("Dataset is already up to date.")
        return

    TARGET_PATH.write_text(csv_text + "\n", encoding="utf-8")
    print("Updated docs/data/sat_practice_scores.csv with refreshed content.")


if __name__ == "__main__":
    main()
