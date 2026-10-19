"""Read-only classification of pytest collection errors from existing logs."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

ERR = re.compile(r"^E\s+(?P<type>ImportError|ModuleNotFoundError|SyntaxError|AttributeError|NameError):\s*(?P<detail>.+)$")
START = re.compile(r"^_+\s+ERROR collecting (?P<path>.+?)\s+_+\s*$")
END = re.compile(r"^={3,}\s+short test summary info")


def parse_collection_log(content: str) -> list[dict[str, str]]:
    """Bind each collection exception to its test path without running pytest."""
    records: list[dict[str, str]] = []
    current: str | None = None
    for line in content.splitlines():
        match_start = START.match(line)
        if match_start:
            current = match_start.group("path")
            continue
        if END.match(line):
            current = None
        match_error = ERR.match(line)
        if match_error and current is not None:
            records.append({"test_path": current, "exception_type": match_error.group("type"), "detail": match_error.group("detail")})
            current = None
    return records


def category(record: dict[str, str]) -> str:
    detail = record["detail"]
    if "toda_pi4_3_delta_image_free_cyclic_inference_rule" in detail:
        return "removed_group_specific_rule_import"
    if "tests.test_phase143_19_method_evidence" in detail:
        return "missing_test_fixture_dependency"
    if "repository_inference" in detail:
        return "missing_legacy_repository_module"
    if "test_phase144_6_r5_18_production_generic_proof_chain_foundation" in detail:
        return "missing_historical_test_module"
    if detail.startswith("No module named '"):
        return "other_missing_module"
    if record["exception_type"] == "ImportError":
        return "other_missing_export"
    return "other_collection_exception"


def build_report(content: str) -> dict[str, object]:
    records = parse_collection_log(content)
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in records:
        groups[category(record)].append(record)
    summaries = [{"category": key, "count": len(value), "distinct_details": len({r["detail"] for r in value}), "examples": value[:5]} for key, value in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))]
    return {"status": "CLASSIFIED_NOT_RESOLVED", "total_collection_errors": len(records), "unique_details": len({(r['exception_type'], r['detail']) for r in records}), "summary": summaries, "records": records, "policy": "No tests excluded or changed; no removed API restored; root cause requires independent source review."}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    log = Path(args.log)
    if not log.is_file():
        parser.error("collection log does not exist: " + str(log))
    report = build_report(log.read_text(encoding="utf-8", errors="replace"))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Collection errors:", report["total_collection_errors"])
    print("Unique exception messages:", report["unique_details"])
    for group in report["summary"]:
        print(f"{group['count']:4} {group['category']}")
    print("Report:", target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
