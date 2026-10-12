"""Phase 163 R4-R59: isolated immutable-ID / mutable-position trial.

Synthetic inserted entries are *test fixtures*, not Toda claims or IDs to promote.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)

EXPECTED = (("(2.9)", 40, r"\Delta"),
            ("(2.10)", 41, r"\Delta^{-1}"),
            ("(4.3)", 65, r"\pi_i^n"))


@dataclass(frozen=True)
class OrderSnapshot:
    reference: LiteratureEntry
    assertion: AssertionEntry


def read_readiness(path: Path) -> dict:
    result = json.loads(path.read_text(encoding="utf-8"))
    if result.get("phase") != "163 R4-R58" or result.get("definition_count") != 3:
        raise ValueError("unexpected R4-R58 input")
    records = result.get("records")
    if not isinstance(records, list) or len(records) != 3:
        raise ValueError("expected exactly three records")
    actual = [(r["locator"], r["publication_position"], r["defined_symbol"])
              for r in records]
    if actual != list(EXPECTED):
        raise ValueError("unexpected locators, order, or symbols")
    source_ids = [r["source_unit_id"] for r in records]
    trial_refs = [r["trial_reference_id"] for r in records]
    trial_assertions = [r["trial_assertion_id"] for r in records]
    if (len(set(source_ids)) != 3 or len(set(trial_refs)) != 3 or
            len(set(trial_assertions)) != 3):
        raise ValueError("duplicate source or trial ID")
    for r in records:
        if not (r["trial_reference_id"].startswith("trial:r55:") and
                r["trial_assertion_id"] == r["trial_reference_id"] + ":definition" and
                r["metadata_complete"] is True and
                r["source_grounded_content_present"] is True and
                r["explicit_scope_evidence_present"] is True and
                r["archival_staging_status"] == "READY_WITH_UNVERIFIED_SEMANTICS" and
                r["semantic_registration_status"] == "BLOCKED_BY_UNVERIFIED_SEMANTICS" and
                r["proof_eligibility"] == "NOT_ELIGIBLE" and
                r["production_registration_applied"] is False and
                r["original_edition_verified"] is False):
            raise ValueError("unsafe or inconsistent readiness record")
    if (result.get("production_ids_allocated") is not False or
            result.get("production_registry_modified") is not False or
            result.get("proof_search_connected") is not False):
        raise ValueError("production mutation claimed by input")
    return result


def build_trial_registry(records: list[dict], positions: dict[str, int] | None = None) -> tuple[UnifiedStatementRegistry, tuple[OrderSnapshot, ...]]:
    registry = UnifiedStatementRegistry()
    snapshots = []
    for r in records:
        ref = LiteratureEntry(
            reference_id=r["trial_reference_id"],
            kind=ReferenceKind.EQUATION,
            locator=r["locator"],
            source_id="Toda:TeX:unverified_original",
            publication_position=(positions or {}).get(r["trial_reference_id"], r["publication_position"]),
        )
        assertion = AssertionEntry(
            assertion_id=r["trial_assertion_id"],
            reference_id=ref.reference_id,
            kind=AssertionKind.DEFINITION,
            content=("SOURCE_TEX_DIGEST", r["tex_sha256"]),
            defined_symbol=r["defined_symbol"],
            component_position=1,
            scope={"source_line": r["source_line"], "semantic_verification": False},
        )
        registry.add_reference(ref)
        registry.add_assertion(assertion)
        snapshots.append(OrderSnapshot(ref, assertion))
    return registry, tuple(snapshots)


def simulate_insertion(records: list[dict]) -> dict:
    original, before = build_trial_registry(records)
    initial_ids = [(r.reference.reference_id, r.assertion.assertion_id) for r in before]

    # The new order is a synthetic demonstration: existing positions may shift.
    shifted = {records[0]["trial_reference_id"]: 40,
               records[1]["trial_reference_id"]: 42,
               records[2]["trial_reference_id"]: 66}
    modified, after = build_trial_registry(records, shifted)
    synthetic_ref_id = "simulation:r59:inserted:reference"
    synthetic_assertion_id = "simulation:r59:inserted:assertion"
    modified.add_reference(LiteratureEntry(
        synthetic_ref_id, ReferenceKind.REMARK,
        "SYNTHETIC INSERTION (not Toda)", publication_position=41,
    ))
    modified.add_assertion(AssertionEntry(
        synthetic_assertion_id, synthetic_ref_id, AssertionKind.STATEMENT,
        "SYNTHETIC ONLY", component_position=1,
    ))
    resulting_ids = [(r.reference.reference_id, r.assertion.assertion_id) for r in after]
    if resulting_ids != initial_ids:
        raise AssertionError("existing IDs must survive an insertion")
    if any(modified.assertion(aid).reference_id != rid for rid, aid in initial_ids):
        raise AssertionError("existing reference links must survive an insertion")

    # A separate synthetic insertion into an existing reference tests component order.
    original_ref = before[0].reference
    existing_assertion = before[0].assertion
    component_registry = UnifiedStatementRegistry()
    component_registry.add_reference(original_ref)
    component_registry.add_assertion(existing_assertion)
    second_id = "simulation:r59:existing:second"
    middle_id = "simulation:r59:inserted:component"
    component_registry.add_assertion(AssertionEntry(
        second_id, original_ref.reference_id, AssertionKind.STATEMENT,
        "SYNTHETIC SECOND", component_position=3,
    ))
    component_registry.add_assertion(AssertionEntry(
        middle_id, original_ref.reference_id, AssertionKind.STATEMENT,
        "SYNTHETIC MIDDLE", component_position=2,
    ))
    component_order = [(a.assertion_id, a.component_position)
                       for a in sorted(component_registry.assertions_for(original_ref.reference_id),
                                       key=lambda a: a.component_position)]
    if component_registry.assertion(existing_assertion.assertion_id).component_position != 1:
        raise AssertionError("existing component ID or position changed")

    return {
        "phase": "163 R4-R59",
        "mode": "ISOLATED_ID_ORDER_INSERTION_TRIAL",
        "reference_count_before": len(before),
        "reference_count_after_synthetic_insertion": len(before) + 1,
        "stable_reference_id_count": len(before),
        "stable_assertion_id_count": len(before),
        "synthetic_reference_insertion_position": 41,
        "synthetic_component_insertion_position": 2,
        "component_positions_independent": True,
        "positions_mutated_only_in_new_trial_snapshot": True,
        "ids_preserved": True,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "mathematical_semantics_verified": False,
        "proof_search_connected": False,
        "original_edition_verified": False,
        "untouched_definition_candidate_count": 16,
        "pending_other_candidates_count": 237,
        "records": [{
            "locator": r["locator"],
            "source_unit_id": r["source_unit_id"],
            "reference_id": r["trial_reference_id"],
            "assertion_id": r["trial_assertion_id"],
            "position_before": r["publication_position"],
            "position_after": shifted[r["trial_reference_id"]],
            "component_position_before": original.assertion(r["trial_assertion_id"]).component_position,
            "component_position_after": modified.assertion(r["trial_assertion_id"]).component_position,
            "id_preserved": True,
            "id_is_trial_only": True,
        } for r in records],
        "synthetic_component_order": component_order,
        "synthetic_ids_are_not_toda_statements": True,
    }


def write_outputs(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "id_order_trial.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (out_dir / "id_order_trial.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result["records"][0]))
        writer.writeheader()
        writer.writerows(result["records"])
    lines = ["# Phase 163 R4-R59 識別子と掲載順の分離試行", "",
             "- 対象：R4-R58 の仮定義3件（本番 ID ではない）",
             "- 掲載順 40 と 41 の間への架空挿入：既存の参照・主張 ID は3件とも不変",
             "- 一つの参照内への架空挿入：component_position は掲載順と独立",
             "- 架空項目は Toda の命題を表さない",
             "- 新しいスナップショットでのみ位置を付け直し、元の Registry を変更しない",
             "- 仮 ID を本番 ID に昇格せず、数学的意味・引用可能性・証明利用を認定しない",
             "- 本番 Registry・TeX・証明探索は変更しない。全体 pytest は実施しない", ""]
    (out_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readiness", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    validated = read_readiness(args.readiness)
    result = simulate_insertion(validated["records"])
    result["input_sha256"] = hashlib.sha256(args.readiness.read_bytes()).hexdigest()
    write_outputs(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k not in ("records", "synthetic_component_order")}, ensure_ascii=False, indent=2))
    print("R4-R59 isolated ID/order trial complete. Full pytest not run.")


if __name__ == "__main__":
    main()
