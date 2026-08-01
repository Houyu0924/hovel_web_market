from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / "loop-engineering"

REQUIRED_FILES = [
    LOOP / "README.md",
    LOOP / "config" / "goals.yml",
    LOOP / "config" / "quality-gates.yml",
    LOOP / "config" / "stop-conditions.yml",
    LOOP / "data" / "content-metrics.csv",
    LOOP / "data" / "x-experiments.csv",
    LOOP / "data" / "product-reviews.csv",
    LOOP / "prompts" / "weekly-review.md",
    LOOP / "prompts" / "x-post-optimizer.md",
    LOOP / "prompts" / "product-review-evaluator.md",
    LOOP / "workflows" / "operating-procedure.md",
]

EXPECTED_HEADERS = {
    "content-metrics.csv": [
        "date", "platform", "title_or_id", "category", "content_type",
        "views", "likes", "comments", "clicks", "affiliate_clicks",
        "profile_visits", "followers_delta", "style_variant", "hypothesis",
        "result", "next_action", "notes",
    ],
    "x-experiments.csv": [
        "date", "post_id", "source_content", "style_variant", "hook",
        "has_link", "impressions", "likes", "replies", "reposts",
        "bookmarks", "profile_visits", "link_clicks", "followers_delta",
        "hypothesis", "result", "next_action", "notes",
    ],
    "product-reviews.csv": [
        "date", "product", "variant", "source", "purchase_price_jpy",
        "test_day", "use_case", "weather_or_environment", "amount_used",
        "scent_strength_1_5", "scent_duration_hours", "cleanliness_feel_1_5",
        "skin_or_scalp_reaction", "office_suitability_1_5",
        "repurchase_intent_1_5", "affiliate_clicks", "verdict",
        "evidence_status", "next_action", "notes",
    ],
}

ALLOWED_NEXT_ACTIONS = {"", "continue", "improve", "stop", "start_test"}
ALLOWED_VERDICTS = {
    "", "recommended", "conditionally_recommended", "not_recommended",
    "insufficient_evidence",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_required_files() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def validate_headers() -> None:
    for filename, expected in EXPECTED_HEADERS.items():
        path = LOOP / "data" / filename
        headers, _ = read_csv(path)
        if headers != expected:
            fail(f"Unexpected header in {filename}. Expected {expected}, got {headers}")


def validate_numeric(value: str, field: str, filename: str, row_number: int) -> None:
    if value == "":
        return
    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"{filename}:{row_number} {field} must be numeric") from exc
    if number < 0:
        raise ValueError(f"{filename}:{row_number} {field} must be non-negative")


def validate_rows() -> None:
    numeric_fields = {
        "content-metrics.csv": {
            "views", "likes", "comments", "clicks", "affiliate_clicks",
            "profile_visits", "followers_delta",
        },
        "x-experiments.csv": {
            "impressions", "likes", "replies", "reposts", "bookmarks",
            "profile_visits", "link_clicks", "followers_delta",
        },
        "product-reviews.csv": {
            "purchase_price_jpy", "scent_strength_1_5", "scent_duration_hours",
            "cleanliness_feel_1_5", "office_suitability_1_5",
            "repurchase_intent_1_5", "affiliate_clicks",
        },
    }

    for filename in EXPECTED_HEADERS:
        path = LOOP / "data" / filename
        _, rows = read_csv(path)
        for index, row in enumerate(rows, start=2):
            for field in numeric_fields[filename]:
                validate_numeric(row.get(field, ""), field, filename, index)

            action = row.get("next_action", "")
            if action not in ALLOWED_NEXT_ACTIONS:
                fail(f"{filename}:{index} invalid next_action: {action}")

            if filename == "product-reviews.csv":
                verdict = row.get("verdict", "")
                if verdict not in ALLOWED_VERDICTS:
                    fail(f"{filename}:{index} invalid verdict: {verdict}")


def main() -> None:
    validate_required_files()
    validate_headers()
    try:
        validate_rows()
    except ValueError as exc:
        fail(str(exc))
    print("HOVEL loop data validation passed.")


if __name__ == "__main__":
    main()
