"""Diagnostic-only R4-R11 audit; blocked witnesses remain metadata-only."""
from __future__ import annotations

import json
from pathlib import Path

from phase163_r4_r11_ancestry_diagnosis import diagnose_incomplete_ancestry
from phase163_r4_r11_prop56_remaining import COMPONENT_KEYS, verify_prop56_remaining_component
from phase163_r4_r7_representative_bindings import WitnessCandidate, bind_representative_witnesses
from phase163_r4_registry_bridge import build_registry_bridge
from probes.probe_phase65_capabilities import build_phase65_representative_result
from proof import ProofRule


WITNESSES = (
    ("pi6_3_group_relation", "pi6_3_step"),
    ("pi7_4_group_relation", "pi7_4_step"),
    ("pi8_5_group_relation", "pi8_5_step"),
    ("higher_nu_group_relation", "higher_step"),
)


def run_audit(output_dir: Path) -> dict[str, object]:
    sample = build_phase65_representative_result()
    if sample["higher_range_step"].rule is not ProofRule.GIVEN:
        raise ValueError("Unexpected high-range premise classification")
    candidates = tuple(
        WitnessCandidate("Proposition 5.6", key, sample[name], sample[name].conclusion,
                         f"Existing Phase65 {name}")
        for key, name in WITNESSES
    )
    snapshot, attempts = bind_representative_witnesses(build_registry_bridge(), candidates)
    attempts_by_key = {a.component_key: a for a in attempts}
    results = []
    rows = []
    for key, name in WITNESSES:
        attempt = attempts_by_key[key]
        findings = diagnose_incomplete_ancestry(sample[name])
        integrity = "NOT_VERIFIED"
        scope = None
        if attempt.status == "STRUCTURED":
            verified = verify_prop56_remaining_component(
                snapshot, key,
                higher_range=sample["higher_range_step"].conclusion if key == "higher_nu_group_relation" else None,
            )
            integrity = verified.status
            scope = verified.scope
            results.append(verified)
        rows.append({
            "component": key,
            "binding_status": attempt.status,
            "binding_detail": attempt.detail,
            "integrity": integrity,
            "scope": scope,
            "ancestry_findings": [
                {"path": f.path, "issue": f.issue, "conclusion_type": f.conclusion_type,
                 "rule_name": f.rule_name}
                for f in findings
            ],
        })
    blocked = sum(row["binding_status"] != "STRUCTURED" for row in rows)
    payload = {
        "phase": "163 R4-R11 repair1",
        "audit_status": "BLOCKED_BY_PROVENANCE" if blocked else "VERIFIED_BY_EXISTING_VALIDATOR",
        "blocked_components": blocked,
        "components": rows,
        "source_independently_verified": False,
        "full_pytest_run": False,
        "note": "A structurally complete ancestry tree is necessary, not sufficient, for citation verification.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R11 — 祖先由来の診断", "",
             f"**監査状態: {payload['audit_status']}**", "",
             "| 成分 | 引用接続 | 内容検査 | 祖先の構造的不備 |",
             "|---|---|---|---|"]
    for row in rows:
        issues = ", ".join(f"`{f['path']}: {f['issue']}`" for f in row["ancestry_findings"])
        lines.append(f"| `{row['component']}` | {row['binding_status']} | {row['integrity']} | {issues or '検出なし'} |")
    lines.extend(["", "## 重要", "", "- 引用検証に失敗した Statement は metadata_only のまま維持します。",
                  "- 不備を検出しなかった場合も、既存の validator が不合格なら接続しません。",
                  "- 証明木に不足する推論規則や前提を捏造して補いません。",
                  "- 文献原本の独立照合、全体 pytest は未実施です。", ""])
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return payload


if __name__ == "__main__":
    report = run_audit(Path("phase163_r4_r11_output"))
    print("Phase 163 R4-R11 ancestry diagnosis:", report["audit_status"])
    for row in report["components"]:
        print(row["component"], row["binding_status"], row["binding_detail"],
              "gaps:", len(row["ancestry_findings"]))
    print("Saved phase163_r4_r11_output/report.md and summary.json")
    print("Full pytest not run.")
