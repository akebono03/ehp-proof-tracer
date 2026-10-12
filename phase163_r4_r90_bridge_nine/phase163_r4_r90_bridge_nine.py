"""Phase 163 R4-R90: opt-in integration of R89 source-only assertions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
    build_registry_bridge,
)
from phase163_r4_r89_source_assertions.phase163_r4_r89_source_assertions import (
    build_source_only_registry,
    load_json,
)
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_R86 = ROOT / "phase163_r4_r86_output" / "claim_review_catalog.json"
DEFAULT_R88 = ROOT / "phase163_r4_r88_output" / "scope_conditions.json"


def build_registry_bridge_with_r89_nine(
    r86_path: Path = DEFAULT_R86,
    r88_path: Path = DEFAULT_R88,
    *,
    base: RegistryBridgeResult | None = None,
) -> tuple[RegistryBridgeResult, dict]:
    """Build a fresh/explicit bridge with nine archival assertions, never proof premises.

    This function deliberately DOES NOT call the R83/R85 eight-assertion path.
    R89 IDs are source archival IDs and not semantically certified permanent IDs.
    """
    archive, archive_report = build_source_only_registry(
        load_json(r86_path), load_json(r88_path)
    )
    if base is None:
        base = build_registry_bridge()
    registry = base.registry
    expected_ref_ids = (
        "toda:Proposition 1.6",
        "toda:Theorem 2.4",
        "toda:Proposition 2.5",
        "toda:Proposition 4.2",
    )
    if archive_report["assertion_count"] != 9 or archive_report["reference_count"] != 4:
        raise ValueError("invalid R89 cardinality")

    # Check all collisions before mutating the opt-in registry.
    add_reference = []
    reused_reference = []
    for ref_id in expected_ref_ids:
        candidate = archive.reference(ref_id)
        try:
            existing = registry.reference(ref_id)
        except KeyError:
            add_reference.append(candidate)
        else:
            if existing.kind != candidate.kind or existing.locator != candidate.locator:
                raise ValueError(f"reference conflict: {ref_id}")
            reused_reference.append(ref_id)

    additions = []
    existing_archived = set()
    for row in archive_report["records"]:
        item = archive.assertion(row["assertion_id"])
        if item.origin is not AssertionOrigin.SOURCE_ARCHIVE:
            raise ValueError("R89 entry must remain source archive")
        if item.available_after_position is not None:
            raise ValueError("archive availability may not be inferred")
        if any(item.content[k] is not False for k in (
            "proof_eligible", "mathematics_verified", "original_edition_verified"
        )):
            raise ValueError("R89 semantic flags illegally promoted")
        if row["registration_status"] != "SOURCE_ONLY":
            raise ValueError("R89 source-only status required")
        try:
            registry.assertion(item.assertion_id)
        except KeyError:
            additions.append(item)
        else:
            existing_archived.add(item.assertion_id)
    if existing_archived:
        raise ValueError(f"duplicate source assertion IDs: {sorted(existing_archived)}")
    if len(additions) != 9 or len({x.assertion_id for x in additions}) != 9:
        raise ValueError("unexpected R89 source assertion identities")
    if any(link.assertion_id in {x.assertion_id for x in additions}
           for link in base.proof_links):
        raise ValueError("archival ID already connected to proof")

    for reference in add_reference:
        registry.add_reference(reference)
    for item in additions:
        registry.add_assertion(item)
    added_records = tuple(MigrationRecord(
        source="r89_source_archive",
        source_key=item.assertion_id,
        assertion_id=item.assertion_id,
        status=MigrationStatus.METADATA_ONLY,
        detail="R89 translated TeX source claim; original/math not certified; not proof eligible",
    ) for item in additions)
    combined = RegistryBridgeResult(
        registry=registry,
        records=base.records + added_records,
        proof_links=base.proof_links,
    )
    report = {
        "phase": "163 R4-R90",
        "mode": "OPT_IN_R89_NINE_TO_UNIFIED_BRIDGE_SOURCE_ONLY",
        "reference_added_count": len(add_reference),
        "reference_reused_count": len(reused_reference),
        "assertion_added_count": len(additions),
        "metadata_only_record_count": len(added_records),
        "mathematical_semantics_verified_count": 0,
        "original_edition_verified": False,
        "proof_eligible_count": 0,
        "production_auto_connected": False,
        "production_registry_modified": False,
        "proof_search_connected": False,
        "full_suite_run": False,
        "assertion_ids": [entry.assertion_id for entry in additions],
        "reference_ids_added": [entry.reference_id for entry in add_reference],
        "reference_ids_reused": reused_reference,
    }
    return combined, report


def write_report(report: dict, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    text = [
        "# Phase 163 R4-R90：R89 9主張の統一台帳 Bridge への任意接続",
        "",
        "原文用 Assertion を9件追加。数学的認定は行わず、ProofStepLink は追加しない。",
        "R83/R85 の8件経路は同時に呼び出さない。既存本番処理は変更しない。",
        "",
        f"- 新規 Reference: {report['reference_added_count']}",
        f"- 再利用 Reference: {report['reference_reused_count']}",
        f"- 追加 Assertion: {report['assertion_added_count']}",
        "- 数学的認定: 0",
        "- 全体 pytest: 未実施",
    ]
    (directory / "report.md").write_text("\n".join(text) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r86", type=Path, default=DEFAULT_R86)
    parser.add_argument("--r88", type=Path, default=DEFAULT_R88)
    parser.add_argument("--output", type=Path, default=ROOT / "phase163_r4_r90_output")
    args = parser.parse_args()
    bridge, report = build_registry_bridge_with_r89_nine(args.r86, args.r88)
    assert len(bridge.records_for("r89_source_archive")) == 9
    write_report(report, args.output)
    print(json.dumps({k: v for k, v in report.items() if not isinstance(v, list)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
