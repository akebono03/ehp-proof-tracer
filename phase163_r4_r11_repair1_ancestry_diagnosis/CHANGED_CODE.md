# Phase 163 R4-R11 repair1 — 変更コード全文

既存のクラス・メソッド・import は変更しません。追加関数は `phase163_r4_r11_ancestry_diagnosis.py` に、監査の置換関数は `audit.py` に配置します。

**注意:** この修正は原因位置を特定する監査であり、4件の構造化登録を完了したことにはなりません。

## `phase163_r4_r11_ancestry_diagnosis.py`

```python
"""Read-only ancestry diagnostics for Proposition 5.6 R4-R11 witnesses.

Does not make any provenance decisions or turn missing data into a citation.
"""
from __future__ import annotations

from dataclasses import dataclass

from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class AncestryFinding:
    path: str
    issue: str
    conclusion_type: str
    rule_name: str | None


def diagnose_incomplete_ancestry(root: ProofStep) -> tuple[AncestryFinding, ...]:
    """Report all reachable structural provenance gaps, bounded by node identity."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    findings: list[AncestryFinding] = []
    seen: set[int] = set()
    active: set[int] = set()

    def visit(node: ProofStep, path: str) -> None:
        identity = id(node)
        if identity in active:
            findings.append(AncestryFinding(path, "CYCLIC_ANCESTRY", type(node.conclusion).__name__, None))
            return
        if identity in seen:
            return
        active.add(identity)
        try:
            inference_name = node.inference_rule.name if node.inference_rule is not None else None
            if node.rule is ProofRule.INFERENCE:
                if node.inference_rule is None:
                    findings.append(AncestryFinding(path, "INFERENCE_RULE_MISSING", type(node.conclusion).__name__, None))
                if not node.premises:
                    findings.append(AncestryFinding(path, "INFERENCE_PREMISES_MISSING", type(node.conclusion).__name__, inference_name))
            elif node.rule is ProofRule.GIVEN:
                if node.premises:
                    findings.append(AncestryFinding(path, "GIVEN_HAS_PREMISES", type(node.conclusion).__name__, inference_name))
            else:
                findings.append(AncestryFinding(path, "UNSUPPORTED_PROOF_RULE", type(node.conclusion).__name__, inference_name))
            for position, premise in enumerate(node.premises):
                child_path = f"{path}/premise[{position}]"
                if not isinstance(premise, ProofStep):
                    findings.append(AncestryFinding(child_path, "NON_PROOFSTEP_PREMISE", type(premise).__name__, None))
                else:
                    visit(premise, child_path)
        finally:
            active.remove(identity)
            seen.add(identity)

    visit(root, "root")
    return tuple(findings)

```

## `tests/test_phase163_r4_r11_ancestry_diagnosis.py`

```python
from proof import InferenceRule, ProofRule, ProofStep
from phase163_r4_r11_ancestry_diagnosis import diagnose_incomplete_ancestry


def test_r4_r11_diagnosis_records_missing_rule_in_ancestor():
    leaf = ProofStep("axiom", (), ProofRule.GIVEN)
    ancestor = ProofStep("middle", (leaf,), ProofRule.INFERENCE)
    root = ProofStep("goal", (ancestor,), ProofRule.INFERENCE, inference_rule=InferenceRule("goal_rule"))
    findings = diagnose_incomplete_ancestry(root)
    assert [(f.path, f.issue) for f in findings] == [
        ("root/premise[0]", "INFERENCE_RULE_MISSING")
    ]


def test_r4_r11_diagnosis_records_missing_premises_without_promoting():
    root = ProofStep("goal", (), ProofRule.INFERENCE, inference_rule=InferenceRule("rule"))
    findings = diagnose_incomplete_ancestry(root)
    assert len(findings) == 1
    assert findings[0].issue == "INFERENCE_PREMISES_MISSING"
    assert root.premises == ()


def test_r4_r11_diagnosis_accepts_structurally_complete_tree():
    leaf = ProofStep("axiom", (), ProofRule.GIVEN)
    root = ProofStep("goal", (leaf,), ProofRule.INFERENCE, inference_rule=InferenceRule("rule"))
    assert diagnose_incomplete_ancestry(root) == ()


def test_r4_r11_diagnosis_rejects_non_proofstep_root():
    try:
        diagnose_incomplete_ancestry("not-a-step")
    except TypeError as exc:
        assert "root" in str(exc)
    else:
        raise AssertionError("TypeError expected")

```

## `audit.py`

```python
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

```

## `run.ps1`

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @('proof.py', 'phase163_r4_registry_bridge.py', 'phase163_r4_r11_prop56_remaining.py', 'phase163_r4_r7_representative_bindings.py')
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) { throw "Missing required project file: $Filename" }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r11_ancestry_diagnosis.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_ancestry_diagnosis.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r11_ancestry_diagnosis.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r11_ancestry_diagnosis.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'audit.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_prop56_remaining\audit.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r11_prop56_remaining.py tests/test_phase163_r4_r11_ancestry_diagnosis.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 focused tests failed.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $ProjectRoot 'phase163_r4_r11_prop56_remaining\audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 diagnostic execution failed.' }
Write-Host 'R4-R11 provenance diagnosis executed. R4-R11 is not complete if audit reports BLOCKED_BY_PROVENANCE. Full suite not run.'

```
