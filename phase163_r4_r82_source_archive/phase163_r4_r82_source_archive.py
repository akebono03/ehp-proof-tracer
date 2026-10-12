"""Phase 163 R4-R82: source-text archive registration, not mathematical proof eligibility."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from phase163_r4_registry_bridge import build_registry_bridge
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ReferenceKind, UnifiedStatementRegistry,
)


LOCATORS = {
    "prop:1-6": ("Proposition 1.6", ReferenceKind.PROPOSITION),
    "thm:2.4": ("Theorem 2.4", ReferenceKind.THEOREM),
    "prop:2.5": ("Proposition 2.5", ReferenceKind.PROPOSITION),
    "prop:4.2": ("Proposition 4.2", ReferenceKind.PROPOSITION),
}


def archive_source_assertions(registry: UnifiedStatementRegistry, preflight: dict,
                              duplicate_audit: dict) -> dict:
    """Add archival *source text* to registry; never grant theorem/proof eligibility.

    The caller owns registry lifetime; the function refuses repeated registration
    and conflicting/unknown upstream evidence. Entries are not formalized math.
    """
    if preflight.get("phase") != "163 R4-R80" or duplicate_audit.get("phase") != "163 R4-R81":
        raise ValueError("unexpected audit phase")
    for evidence in (preflight, duplicate_audit):
        if evidence.get("production_registry_modified") is not False or evidence.get("production_ids_allocated") is not False:
            raise ValueError("upstream evidence must be unmodified")
        if evidence.get("semantic_registration_allowed_count") != 0:
            raise ValueError("upstream semantic approval unexpectedly set")
    records = preflight.get("records")
    checks = duplicate_audit.get("records")
    if not isinstance(records, list) or len(records) != 8 or not isinstance(checks, list) or len(checks) != 4:
        raise ValueError("unexpected candidate count")
    by_owner = {r["owner"]: r for r in checks}
    if set(by_owner) != set(LOCATORS):
        raise ValueError("owner mismatch")
    grouped = {owner: [] for owner in LOCATORS}
    for row in records:
        owner = row["owner"]
        if owner not in grouped:
            raise ValueError("unknown owner")
        if row.get("registration_allowed") is not False or row.get("permanent_id_allocated") is not False:
            raise ValueError("unexpected source approval")
        if not row.get("shared_scope_note") or not row.get("claim_text"):
            raise ValueError("missing scope or source text")
        if hashlib.sha256(row["claim_text"].encode("utf-8")).hexdigest() != row["source_claim_sha256"]:
            raise ValueError("claim text checksum mismatch")
        grouped[owner].append(row)
    expected = {"prop:1-6": 3, "thm:2.4": 2, "prop:2.5": 2, "prop:4.2": 1}
    if {k: len(v) for k, v in grouped.items()} != expected:
        raise ValueError("component count mismatch")
    for owner, rows in grouped.items():
        positions = [row["component_position"] for row in rows]
        if positions != list(range(1, len(rows) + 1)):
            raise ValueError("invalid component order")
        check = by_owner[owner]
        locator, kind = LOCATORS[owner]
        if check["locator"] != locator or check["kind"] != kind.value:
            raise ValueError("locator identity mismatch")
        if check["proposed_assertion_count"] != len(rows):
            raise ValueError("audited component count mismatch")
        already = bool(check["live_bridge_reference_found"])
        try:
            original = registry.reference("toda:" + locator)
        except KeyError:
            original = None
        if already != (original is not None):
            raise ValueError("bridge reference status changed")
        if original is not None and (original.locator != locator or original.kind is not kind):
            raise ValueError("conflicting reference")
    added_refs = []
    added_ids = []
    for owner, rows in grouped.items():
        locator, kind = LOCATORS[owner]
        reference_id = "toda:" + locator
        try:
            registry.reference(reference_id)
        except KeyError:
            registry.add_reference(LiteratureEntry(reference_id, kind, locator, source_id="Toda TeX transcript (unverified against original)"))
            added_refs.append(reference_id)
        for row in rows:
            # `archive:` explicitly distinguishes an archival transcript from a formal theorem.
            assertion_id = "archive:" + row["proposed_assertion_key"].removeprefix("proposal:")
            # Store exact transcribed text and its metadata, without claiming typed mathematical truth.
            content = {
                "source_text": row["claim_text"],
                "source_file": row["source_file"],
                "source_lines": [row["start_line"], row["end_line"]],
                "source_sha256": row["source_claim_sha256"],
                "boundary_issues": tuple(row["boundary_issues"]),
                "mathematics_verified": False,
                "original_edition_verified": False,
                "proof_eligible": False,
            }
            registry.add_assertion(AssertionEntry(
                assertion_id, reference_id, AssertionKind.STATEMENT, content,
                origin=AssertionOrigin.FIXED_STATEMENT,
                component_position=row["component_position"],
                scope=row["shared_scope_note"],
            ))
            added_ids.append(assertion_id)
    return {
        "phase": "163 R4-R82", "mode": "SOURCE_ARCHIVE_REGISTRATION_NOT_PROOF_ELIGIBLE",
        "reference_reused_count": 1, "reference_added_count": len(added_refs),
        "source_text_assertion_added_count": len(added_ids),
        "added_reference_ids": added_refs, "added_source_text_ids": added_ids,
        "fixed_mathematical_assertion_verified_count": 0,
        "original_edition_verified": False,
        "production_catalog_auto_connected": False,
        "production_ids_allocated": False,
        "proof_search_connected": False, "full_suite_run": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--duplicates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    preflight = json.loads(args.preflight.read_text(encoding="utf-8"))
    duplicates = json.loads(args.duplicates.read_text(encoding="utf-8"))
    bridge = build_registry_bridge()
    summary = archive_source_assertions(bridge.registry, preflight, duplicates)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "source_archive.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R82：出典原文の保存登録", "",
             f"- 既存 Reference 再利用：{summary['reference_reused_count']}件",
             f"- Reference 追加：{summary['reference_added_count']}件",
             f"- 出典テキスト Assertion 追加：{summary['source_text_assertion_added_count']}件",
             "- これは実行時の Registry に対する登録であり、本番アプリの自動登録ではない。",
             "- 原本未照合。数学的な主張としての採用と証明利用は未許可。", "- 全体 pytest は未実施。"]
    (args.output / "report.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if not isinstance(v,list)}, ensure_ascii=False,indent=2))
    print("R82 archive validation complete. Full pytest not run.")


if __name__ == "__main__":
    main()
