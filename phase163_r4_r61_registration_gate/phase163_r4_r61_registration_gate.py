"""Phase 163 R4-R61: read-only registration gate, no production ID allocation."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def assess(readiness: dict, order: dict, collision: dict) -> dict:
    """Cross-check documentary identity; never infer semantic equivalence."""
    if (readiness.get("phase"), order.get("phase"), collision.get("phase")) != (
        "163 R4-R58", "163 R4-R59", "163 R4-R60"
    ):
        raise ValueError("unexpected input phase")
    for label, data in (("readiness", readiness), ("order", order), ("collision", collision)):
        if data.get("production_registry_modified") is not False or data.get("production_ids_allocated") is not False:
            raise ValueError(f"{label} reports production mutation")
    if order.get("ids_preserved") is not True or collision.get("id_and_publication_position_independent") is not True:
        raise ValueError("ID/order invariance has not been established")
    if collision.get("live_registry_bridge_constructed") is not True:
        raise ValueError("live bridge evidence required")
    if collision.get("all_applicable_collision_probes_rejected") is not True:
        raise ValueError("collision rejection probes failed")
    rrows, orows, crows = (source.get("records") for source in (readiness, order, collision))
    if any(not isinstance(rows, list) or len(rows) != 3 for rows in (rrows, orows, crows)):
        raise ValueError("expected three records in each input")
    def keyed(rows: list[dict]) -> dict[str, dict]:
        result = {}
        for row in rows:
            key = row["source_unit_id"]
            if key in result:
                raise ValueError("duplicate source unit within input")
            result[key] = row
        return result
    rmap, omap, cmap = keyed(rrows), keyed(orows), keyed(crows)
    if set(rmap) != set(omap) or set(rmap) != set(cmap):
        raise ValueError("mismatched source units")
    if readiness.get("archival_staging_ready_count") != 3:
        raise ValueError("archival stage not confirmed")
    if readiness.get("semantic_registration_ready_count") != 0 or readiness.get("proof_eligible_count") != 0:
        raise ValueError("unexpected semantic readiness")
    if collision.get("candidate_count") != 3:
        raise ValueError("unexpected collision candidate count")
    records = []
    seen_ref, seen_assertion, seen_locator = set(), set(), set()
    for key in sorted(rmap, key=lambda k: rmap[k]["publication_position"]):
        r, o, c = rmap[key], omap[key], cmap[key]
        locator = r["locator"]
        reference_id, assertion_id = r["trial_reference_id"], r["trial_assertion_id"]
        if (o["locator"], c["locator"]) != (locator, locator):
            raise ValueError("locator conflict")
        if (o["reference_id"], c["trial_reference_id"]) != (reference_id, reference_id):
            raise ValueError("reference identity conflict")
        if (o["assertion_id"], c["trial_assertion_id"]) != (assertion_id, assertion_id):
            raise ValueError("assertion identity conflict")
        if not reference_id.startswith("trial:r55:") or assertion_id != reference_id + ":definition":
            raise ValueError("unrecognized trial identity")
        if reference_id in seen_ref or assertion_id in seen_assertion or locator in seen_locator:
            raise ValueError("duplicate proposed identity or locator")
        seen_ref.add(reference_id)
        seen_assertion.add(assertion_id)
        seen_locator.add(locator)
        if r["publication_position"] != o["position_before"]:
            raise ValueError("original publication position conflict")
        if o.get("id_preserved") is not True or o.get("id_is_trial_only") is not True:
            raise ValueError("ID immutability evidence missing")
        if c.get("reference_id_collision") or c.get("assertion_id_collision"):
            raise ValueError("existing ID collision")
        if c.get("locator_overlap_requires_review") or c.get("existing_locator_reference_ids"):
            raise ValueError("existing literature locator overlap")
        if (r.get("archival_staging_status") != "READY_WITH_UNVERIFIED_SEMANTICS"
                or r.get("semantic_registration_status") != "BLOCKED_BY_UNVERIFIED_SEMANTICS"
                or r.get("proof_eligibility") != "NOT_ELIGIBLE"):
            raise ValueError("semantic boundary violated")
        if r.get("formal_mathematical_ast") is not False or r.get("mathematical_equivalence_verified") is not False:
            raise ValueError("unexpected formal mathematical assertion")
        if r.get("original_edition_verified") is not False or r.get("production_registration_applied") is not False:
            raise ValueError("source verification/registration status changed")
        issues = r.get("unresolved_semantics")
        if not isinstance(issues, list) or len(issues) != r.get("unresolved_semantics_count") or not issues:
            raise ValueError("unresolved mathematical conditions lost")
        records.append({
            "locator": locator,
            "source_unit_id": key,
            "original_publication_position": r["publication_position"],
            "simulated_publication_position": o["position_after"],
            "trial_reference_id": reference_id,
            "trial_assertion_id": assertion_id,
            "source_tex_sha256": r["tex_sha256"],
            "archive_staging_ready": True,
            "identity_consistent": True,
            "id_collision_found": False,
            "locator_overlap_found": False,
            "id_stable_under_insertion": True,
            "semantic_registration_allowed": False,
            "proof_eligible": False,
            "original_edition_verified": False,
            "unresolved_semantics": issues,
            "registration_gate": "BLOCKED_SEMANTIC_AND_SOURCE_VERIFICATION",
        })
    return {
        "phase": "163 R4-R61",
        "mode": "READ_ONLY_PRE_REGISTRATION_GATE",
        "candidate_count": len(records),
        "identity_consistent_count": len(records),
        "id_collision_count": 0,
        "locator_overlap_count": 0,
        "archive_staging_ready_count": len(records),
        "semantic_registration_allowed_count": 0,
        "proof_eligible_count": 0,
        "unresolved_semantics_count": sum(len(r["unresolved_semantics"]) for r in records),
        "gate_blocked_count": len(records),
        "trial_ids_promoted_count": 0,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "original_edition_verified": False,
        "untouched_definition_candidate_count": 16,
        "pending_other_candidates_count": 237,
        "records": records,
    }


def write_outputs(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "registration_gate.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (output / "registration_gate.csv").open("w", encoding="utf-8-sig", newline="") as file:
        fields = [key for key in result["records"][0] if key != "unresolved_semantics"]
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(result["records"])
    lines = [
        "# Phase 163 R4-R61 正式登録前の境界監査", "",
        f"- 照合候補：{result['candidate_count']}件",
        f"- 出典・ID 対応が整合：{result['identity_consistent_count']}件",
        f"- ID 衝突：{result['id_collision_count']}件",
        f"- 文献 locator 重複：{result['locator_overlap_count']}件",
        f"- 保管候補として準備済み：{result['archive_staging_ready_count']}件",
        f"- 数学的登録の許可：{result['semantic_registration_allowed_count']}件",
        f"- 正式登録を保留：{result['gate_blocked_count']}件",
        f"- 未解決の数学的事項：{result['unresolved_semantics_count']}件", "",
        "ID・文献 locator の整合性は数学的同値性を保証しない。",
        "原本照合・形式的数学的意味の検証が未完了のため、正式登録と証明利用は許可しない。",
        "本番 Registry・Statement ID・証明探索には変更を加えない。全体 pytest は実施しない。",
    ]
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readiness", required=True, type=Path)
    parser.add_argument("--order", required=True, type=Path)
    parser.add_argument("--collision", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = assess(load_json(args.readiness), load_json(args.order), load_json(args.collision))
    result["input_sha256"] = {
        key: hashlib.sha256(getattr(args, key).read_bytes()).hexdigest()
        for key in ("readiness", "order", "collision")
    }
    write_outputs(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, indent=2, ensure_ascii=False))
    print("R4-R61 read-only registration gate complete. Full pytest not run.")


if __name__ == "__main__":
    main()
