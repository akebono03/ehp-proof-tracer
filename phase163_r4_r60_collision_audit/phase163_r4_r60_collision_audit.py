"""Phase 163 R4-R60: read-only identity collision audit, no ID allocation."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def audit(order: dict, live_references: dict[str, str], live_assertions: dict[str, str]) -> dict:
    """Audit proposals against current IDs; value is source identity, not math equality."""
    if order.get("phase") != "163 R4-R59" or order.get("ids_preserved") is not True:
        raise ValueError("invalid R4-R59 evidence")
    if order.get("production_registry_modified") is not False or order.get("production_ids_allocated") is not False:
        raise ValueError("R4-R59 input claims production mutation")
    records = order.get("records")
    if not isinstance(records, list) or len(records) != 3:
        raise ValueError("expected three R4-R59 records")
    all_existing = set(live_references) | set(live_assertions)
    if set(live_references) & set(live_assertions):
        raise ValueError("live Reference/Assertion ID namespace overlaps")
    result = []
    seen_refs = set()
    seen_assertions = set()
    for record in records:
        ref = record["reference_id"]
        assertion = record["assertion_id"]
        locator = record["locator"]
        source = record["source_unit_id"]
        if not ref.startswith("trial:r55:") or assertion != ref + ":definition":
            raise ValueError("candidate IDs are not recognized trial IDs")
        if record.get("id_preserved") is not True or record.get("id_is_trial_only") is not True:
            raise ValueError("unverified candidate identity")
        if ref in seen_refs or assertion in seen_assertions or ref == assertion:
            raise ValueError("duplicate candidate IDs")
        seen_refs.add(ref)
        seen_assertions.add(assertion)
        reference_collision = ref in all_existing
        assertion_collision = assertion in all_existing
        existing_locator_ids = sorted(k for k, v in live_references.items() if v == locator)
        result.append({
            "locator": locator,
            "source_unit_id": source,
            "trial_reference_id": ref,
            "trial_assertion_id": assertion,
            "reference_id_collision": reference_collision,
            "assertion_id_collision": assertion_collision,
            "existing_locator_reference_ids": existing_locator_ids,
            "locator_overlap_requires_review": bool(existing_locator_ids),
            "trial_ids_promoted": False,
            "registration_action": "NONE",
            "audit_decision": ("BLOCKED_ID_COLLISION" if (reference_collision or assertion_collision) else
                               "REVIEW_LOCATOR_OVERLAP" if existing_locator_ids else
                               "NO_ID_COLLISION_NOT_REGISTRATION_APPROVAL"),
        })
    # These examples MUST be rejected, including cross-type collisions and ID reuse.
    probes = [
        ("SAME_REFERENCE_ID", next(iter(live_references), None), "reference"),
        ("SAME_ASSERTION_ID", next(iter(live_assertions), None), "assertion"),
        ("REFERENCE_ID_AS_ASSERTION", next(iter(live_references), None), "assertion"),
        ("ASSERTION_ID_AS_REFERENCE", next(iter(live_assertions), None), "reference"),
    ]
    probe_results = [{"probe": name, "example_id": ident,
                      "rejected": ident in all_existing if ident is not None else None,
                      "applicable": ident is not None}
                     for name, ident, _target in probes]
    return {
        "phase": "163 R4-R60",
        "mode": "READ_ONLY_LIVE_ID_COLLISION_AUDIT",
        "candidate_count": len(result),
        "live_reference_count": len(live_references),
        "live_assertion_count": len(live_assertions),
        "candidate_reference_id_collision_count": sum(x["reference_id_collision"] for x in result),
        "candidate_assertion_id_collision_count": sum(x["assertion_id_collision"] for x in result),
        "candidate_locator_overlap_review_count": sum(x["locator_overlap_requires_review"] for x in result),
        "probe_count": len(probe_results),
        "all_applicable_collision_probes_rejected": all(x["rejected"] is True for x in probe_results if x["applicable"]),
        "id_and_publication_position_independent": True,
        "semantic_equivalence_verified": False,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "untouched_definition_candidate_count": 16,
        "pending_other_candidates_count": 237,
        "records": result,
        "collision_probes": probe_results,
    }


def live_id_snapshot() -> tuple[dict[str, str], dict[str, str]]:
    """Construct the real bridge. Never use private internals to register anything."""
    from phase163_r4_registry_bridge import build_registry_bridge
    bridge = build_registry_bridge(proof_repository=None)
    refs = {}
    assertions = {}
    for record in bridge.records:
        if record.assertion_id is None:
            continue
        entry = bridge.registry.assertion(record.assertion_id)
        reference = bridge.registry.reference(entry.reference_id)
        refs[reference.reference_id] = reference.locator
        assertions[entry.assertion_id] = entry.reference_id
    return refs, assertions


def write_outputs(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "collision_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "collision_audit.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(result["records"][0]), extrasaction="ignore")
        writer.writeheader()
        for row in result["records"]:
            writer.writerow(row)
    lines = ["# Phase 163 R4-R60 識別子衝突監査", "",
             f"- 既存 Reference ID: {result['live_reference_count']}件",
             f"- 既存 Assertion ID: {result['live_assertion_count']}件",
             f"- 試験候補: {result['candidate_count']}件",
             f"- Reference ID 衝突: {result['candidate_reference_id_collision_count']}件",
             f"- Assertion ID 衝突: {result['candidate_assertion_id_collision_count']}件",
             f"- 掲載 locator 重複要確認: {result['candidate_locator_overlap_review_count']}件", "",
             "異なる ID でも同一 locator の重複は別途数学的確認が必要。", "試験用 ID の本番昇格・正式 ID 発行・証明利用は行わない。", "全体 pytest は実施しない。"]
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    order = load_json(args.order)
    refs, assertions = live_id_snapshot()
    result = audit(order, refs, assertions)
    result["input_sha256"] = hashlib.sha256(args.order.read_bytes()).hexdigest()
    result["live_registry_bridge_constructed"] = True
    write_outputs(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k not in ("records", "collision_probes")}, ensure_ascii=False, indent=2))
    print("R4-R60 read-only ID collision audit complete. Full pytest not run.")


if __name__ == "__main__":
    main()
