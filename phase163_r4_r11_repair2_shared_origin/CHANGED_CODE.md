# Phase 163 R4-R11 repair2 — 変更コード全文

対象: 新規 `phase163_r4_r11_shared_origin.py`、新規 `tests/test_phase163_r4_r11_shared_origin.py`、新規 `audit.py`、新規 `run.ps1`。既存ファイルは変更しません。

## phase163_r4_r11_shared_origin.py

```python
"""Read-only shared-ancestry identity inventory for Phase 163 R4-R11."""
from __future__ import annotations

from dataclasses import dataclass

from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class MissingOrigin:
    ordinal: int
    paths: tuple[str, ...]
    components: tuple[str, ...]
    conclusion_type: str
    conclusion_repr: str
    inference_rule_name: str | None
    proof_note: str | None
    has_inference_rule: bool
    premise_count: int
    issue: str


def find_missing_origins(witnesses: tuple[tuple[str, ProofStep], ...]) -> tuple[MissingOrigin, ...]:
    """Group missing inference ancestry by Python object identity across witnesses.

    Report paths per witness even if a DAG has repeated references. No steps,
    premises, trust boundaries or registry records are modified.
    """
    observations: dict[int, dict[str, object]] = {}
    for component, root in witnesses:
        if not isinstance(root, ProofStep):
            raise TypeError("witness root must be a ProofStep")
        active: set[int] = set()

        def walk(node: ProofStep, path: str) -> None:
            identity = id(node)
            if identity in active:
                return
            active.add(identity)
            try:
                if node.rule is ProofRule.INFERENCE and (
                    not node.premises or node.inference_rule is None
                ):
                    record = observations.setdefault(identity, {"node": node, "paths": [], "components": []})
                    record["paths"].append(f"{component}:{path}")
                    if component not in record["components"]:
                        record["components"].append(component)
                for index, child in enumerate(node.premises):
                    if isinstance(child, ProofStep):
                        walk(child, f"{path}/premise[{index}]")
            finally:
                active.remove(identity)

        walk(root, "root")

    result: list[MissingOrigin] = []
    for position, record in enumerate(observations.values(), start=1):
        node = record["node"]
        assert isinstance(node, ProofStep)
        rule = node.inference_rule
        reasons = []
        if not node.premises:
            reasons.append("INFERENCE_PREMISES_MISSING")
        if rule is None:
            reasons.append("INFERENCE_RULE_MISSING")
        result.append(MissingOrigin(
            ordinal=position,
            paths=tuple(record["paths"]),
            components=tuple(record["components"]),
            conclusion_type=type(node.conclusion).__name__,
            conclusion_repr=repr(node.conclusion),
            inference_rule_name=rule.name if rule is not None else None,
            proof_note=node.note,
            has_inference_rule=rule is not None,
            premise_count=len(node.premises),
            issue=" + ".join(reasons),
        ))
    return tuple(result)

```

## tests/test_phase163_r4_r11_shared_origin.py

```python
from proof import InferenceRule, ProofRule, ProofStep
from phase163_r4_r11_shared_origin import find_missing_origins


def _missing(name: str) -> ProofStep:
    return ProofStep(
        conclusion=name,
        premises=(),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name=f"source_{name}"),
    )


def _parent(name: str, children: tuple[ProofStep, ...]) -> ProofStep:
    return ProofStep(
        conclusion=name,
        premises=children,
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name=f"parent_{name}"),
    )


def test_shared_identity_across_roots_is_one_origin():
    missing = _missing("same")
    left = _parent("left", (missing,))
    right = _parent("right", (missing,))
    entries = find_missing_origins((("a", left), ("b", right)))
    assert len(entries) == 1
    assert entries[0].components == ("a", "b")
    assert entries[0].paths == ("a:root/premise[0]", "b:root/premise[0]")


def test_equal_conclusions_but_distinct_nodes_remain_separate():
    first = _missing("same")
    second = _missing("same")
    assert len(find_missing_origins((("a", first), ("b", second)))) == 2


def test_shared_dag_multiple_paths_retained():
    missing = _missing("shared")
    root = _parent("root", (missing, missing))
    entries = find_missing_origins((("a", root),))
    assert len(entries) == 1
    assert entries[0].paths == ("a:root/premise[0]", "a:root/premise[1]")


def test_complete_inference_is_not_reported():
    leaf = ProofStep(conclusion="fact", premises=(), rule=ProofRule.GIVEN)
    root = _parent("goal", (leaf,))
    assert find_missing_origins((("a", root),)) == ()


def test_missing_rule_is_separately_reported():
    leaf = ProofStep(conclusion="leaf", premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(conclusion="goal", premises=(leaf,), rule=ProofRule.INFERENCE)
    entries = find_missing_origins((("a", root),))
    assert len(entries) == 1
    assert entries[0].issue == "INFERENCE_RULE_MISSING"
    assert entries[0].premise_count == 1


def test_reject_non_proofstep_root():
    import pytest
    with pytest.raises(TypeError):
        find_missing_origins((("a", "not a step"),))

```

## audit.py

```python
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

```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'proof.py',
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r7_representative_bindings.py',
  'phase163_r4_r11_prop56_remaining.py',
  'tests\test_phase65_prop56_integration.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing project prerequisite: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r11_shared_origin.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_shared_origin.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r11_shared_origin.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r11_shared_origin.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r11_shared_origin.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 repair2 focused tests failed.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 repair2 read-only audit failed.' }
Write-Host 'R4-R11 repair2 read-only shared ancestry audit finished. Full pytest not run.'

```

## pytest

`python -B -m pytest -q tests/test_phase163_r4_r11_shared_origin.py`

## 完了条件

同一オブジェクトの欠落祖先が複数群から共有されるかを可視化。登録成功ではありません。

## 次との境界

発生元の既存コード変更は、この診断結果と生成コードの確認後に別 repair として扱います。全体テストは Phase 最終段階のみ。
