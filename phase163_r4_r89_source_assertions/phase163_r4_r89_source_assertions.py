"""Phase 163 R4-R89: opt-in source-only registration of nine reviewed claims."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)

LOCATORS = {
    "Proposition 1.6": ("prop:1-6", ReferenceKind.PROPOSITION, 3),
    "Theorem 2.4": ("thm:2.4", ReferenceKind.THEOREM, 3),
    "Proposition 2.5": ("prop:2.5", ReferenceKind.PROPOSITION, 2),
    "Proposition 4.2": ("prop:4.2", ReferenceKind.PROPOSITION, 1),
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_source_only_registry(r86: dict, r88: dict) -> tuple[UnifiedStatementRegistry, dict]:
    if r86.get("phase") != "163 R4-R86" or r88.get("phase") != "163 R4-R88":
        raise ValueError("unexpected source review phase")
    if r86.get("review_unit_count") != 9 or r88.get("review_unit_count") != 9:
        raise ValueError("expected nine reviewed claims")
    if (r88.get("source_scope_token_verified_count") != 9
            or r88.get("mathematical_semantics_verified_count") != 0
            or r88.get("semantic_registration_allowed_count") != 0
            or r88.get("production_registry_modified") is not False):
        raise ValueError("unexpected R88 certification flags")
    sources = r86["records"]
    checked = r88["records"]
    if len(sources) != 9 or len(checked) != 9:
        raise ValueError("invalid record count")
    if len({x["review_unit_id"] for x in sources}) != 9:
        raise ValueError("duplicate review unit ID")
    if [x["review_unit_id"] for x in sources] != [x["review_unit_id"] for x in checked]:
        raise ValueError("R86/R88 order mismatch")
    registry = UnifiedStatementRegistry()
    report_rows = []
    grouped = {name: [] for name in LOCATORS}
    for original, verified in zip(sources, checked):
        if original["reference_locator"] != verified["reference_locator"]:
            raise ValueError("reference mismatch")
        for key in ("component_position", "subposition", "source_lines"):
            if original[key] != verified[key]:
                raise ValueError(f"source discrepancy: {key}")
        if (verified["source_scope_token_verified"] is not True
                or verified["mathematical_semantics_verified"] is not False
                or verified["original_edition_verified"] is not False
                or verified["semantic_registration_allowed"] is not False
                or verified["proof_eligible"] is not False):
            raise ValueError("source review must remain ineligible for proof search")
        raw = original["claim_text"]
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        if digest != original["claim_sha256"]:
            raise ValueError("claim digest mismatch")
        locator = original["reference_locator"]
        if locator not in grouped:
            raise ValueError("unknown source reference")
        grouped[locator].append((original, verified))
    for locator, (owner, kind, count) in LOCATORS.items():
        pairs = grouped[locator]
        if len(pairs) != count:
            raise ValueError("incorrect assertion count")
        reference_id = "toda:" + locator
        registry.add_reference(LiteratureEntry(
            reference_id=reference_id,
            kind=kind,
            locator=locator,
            source_id="Toda translated TeX; original edition unverified",
        ))
        for original, verified in pairs:
            review_id = original["review_unit_id"]
            assertion_id = "archive:" + review_id.removeprefix("review:r86:")
            content = {
                "source_text": original["claim_text"],
                "source_file": original["source_file"],
                "source_lines": original["source_lines"],
                "source_sha256": original["claim_sha256"],
                "required_scope_conditions_jp": verified["required_scope_conditions_jp"],
                "remaining_mathematical_review_jp": verified["remaining_mathematical_review_jp"],
                "subposition": original["subposition"],
                "original_edition_verified": False,
                "mathematics_verified": False,
                "proof_eligible": False,
            }
            registry.add_assertion(AssertionEntry(
                assertion_id=assertion_id,
                reference_id=reference_id,
                kind=AssertionKind.STATEMENT,
                origin=AssertionOrigin.SOURCE_ARCHIVE,
                component_position=original["component_position"],
                content=content,
                scope=original["shared_scope_note"],
            ))
            report_rows.append({
                "reference_id": reference_id,
                "assertion_id": assertion_id,
                "review_unit_id": review_id,
                "component_position": original["component_position"],
                "subposition": original["subposition"],
                "source_file": original["source_file"],
                "source_lines": original["source_lines"],
                "source_sha256": original["claim_sha256"],
                "registration_status": "SOURCE_ONLY",
                "mathematics_verified": False,
                "proof_eligible": False,
            })
    return registry, {
        "phase": "163 R4-R89",
        "mode": "OPT_IN_SOURCE_ONLY_NINE_ASSERTIONS",
        "reference_count": len(LOCATORS),
        "assertion_count": len(report_rows),
        "mathematical_semantics_verified_count": 0,
        "semantic_registration_allowed_count": 0,
        "production_registry_modified": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "records": report_rows,
    }


def write_report(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R89：9主張の原文登録",
        "",
        "4 Reference、9 Assertion を独立した SOURCE_ARCHIVE 台帳に登録した。",
        "原著照合・数学的認定・本番台帳への移行・証明探索への接続は実施していない。",
        "",
        "| Reference | Assertion ID | 位置 | 状態 |",
        "|---|---|---|---|",
    ]
    for row in report["records"]:
        lines.append(
            f"| {row['reference_id']} | `{row['assertion_id']}` | "
            f"{row['component_position']}.{row['subposition']} | SOURCE_ONLY |"
        )
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r86", required=True, type=Path)
    parser.add_argument("--r88", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    registry, report = build_source_only_registry(load_json(args.r86), load_json(args.r88))
    assert sum(len(registry.assertions_for("toda:" + key)) for key in LOCATORS) == 9
    write_report(report, args.output)
    print(json.dumps({k: v for k, v in report.items() if k != "records"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
