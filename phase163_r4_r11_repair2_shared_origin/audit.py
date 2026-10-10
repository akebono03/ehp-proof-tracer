"""Phase 163 R4-R11 repair2: attribute shared missing-ancestry origins."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from phase163_r4_r11_shared_origin import find_missing_origins
from probes.probe_phase65_capabilities import build_phase65_representative_result
from phase163_r4_r7_representative_bindings import WitnessCandidate, bind_representative_witnesses
from phase163_r4_registry_bridge import build_registry_bridge


WITNESSES = (
    ("pi6_3_group_relation", "pi6_3_step"),
    ("pi7_4_group_relation", "pi7_4_step"),
    ("pi8_5_group_relation", "pi8_5_step"),
    ("higher_nu_group_relation", "higher_step"),
)


def run_audit(output_dir: Path) -> dict[str, object]:
    sample = build_phase65_representative_result()
    nodes = tuple((component, sample[step_key]) for component, step_key in WITNESSES)
    origins = find_missing_origins(nodes)
    candidates = tuple(
        WitnessCandidate("Proposition 5.6", component, step, step.conclusion, "Phase65 existing proof")
        for component, step in nodes
    )
    _snapshot, attempts = bind_representative_witnesses(build_registry_bridge(), candidates)
    statuses = {attempt.component_key: attempt.status for attempt in attempts}
    payload = {
        "phase": "163 R4-R11 repair2",
        "audit_status": "BLOCKED_BY_PROVENANCE" if any(status != "STRUCTURED" for status in statuses.values()) else "VERIFIED",
        "registration_status": statuses,
        "total_missing_occurrences": sum(len(origin.paths) for origin in origins),
        "distinct_missing_object_identities": len(origins),
        "origins": [asdict(origin) for origin in origins],
        "full_pytest_run": False,
        "caveat": "Runtime identity sharing proves shared objects, not the generating source file; equal content can be separate objects.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "shared_origin_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = ["# Phase 163 R4-R11 repair2 — 共通祖先の同一性診断", "",
             f"監査状態: **{payload['audit_status']}**", "",
             f"欠落ノードへの到達回数: **{payload['total_missing_occurrences']}**", "",
             f"異なる Python オブジェクトとしての欠落ノード数: **{len(origins)}**", "",
             "| ID | 関連成分 | Statement 型 | 推論規則名 | 前提数 | 不備 |", "|---|---|---|---|---:|---|"]
    for origin in origins:
        lines.append(f"| {origin.ordinal} | {', '.join(origin.components)} | `{origin.conclusion_type}` | `{origin.inference_rule_name}` | {origin.premise_count} | `{origin.issue}` |")
    for origin in origins:
        lines.extend(["", f"## 欠落ノード {origin.ordinal}", "",
                      f"- Statement: `{origin.conclusion_repr}`",
                      f"- note: `{origin.proof_note}`",
                      "- 到達経路:"])
        lines.extend(f"  - `{path}`" for path in origin.paths)
    lines.extend(["", "未検証の成分は metadata_only を保持し、証明木や引用検証器は変更していません。", ""])
    (output_dir / "shared_origin_report.md").write_text("\n".join(lines), encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = run_audit(Path("phase163_r4_r11_output"))
    print("R4-R11 repair2:", result["audit_status"])
    print("Missing ancestry occurrences:", result["total_missing_occurrences"])
    print("Distinct missing ProofStep identities:", result["distinct_missing_object_identities"])
    for origin in result["origins"]:
        print("origin", origin["ordinal"], origin["conclusion_type"], origin["inference_rule_name"], "components:", ",".join(origin["components"]))
    print("Saved phase163_r4_r11_output/shared_origin_report.md")
    print("Full pytest not run.")
