# Phase 163 R4-R11 — 変更コード全文

既存のクラス・関数・import は変更しません。R11 は新規モジュールとテストの追加だけです。

## 変更対象と追加位置

- `phase163_r4_r11_prop56_remaining.py`：新規モジュール（プロジェクト直下）
- `tests/test_phase163_r4_r11_prop56_remaining.py`：新規軽量テスト（tests/ 内）
- `audit.py`：ZIP 内専用監査（パッケージ内）
- `run.ps1`：ZIP 内 Windows 実行スクリプト

## 検証対象

- `Proposition 5.6` の `pi6_3_group_relation`、`pi7_4_group_relation`、`pi8_5_group_relation`、`higher_nu_group_relation`。
- 生成元と直和を保持。高次の範囲 `n >= 6` は既存 `GIVEN` 範囲と registry scope の双方を照合。
- 文献原本との独立照合は実施しておらず、構造化接続の意味を越える有効性は主張しない。
- full pytest は実施しない。

## 完了条件

- focused pytest 8件 PASS
- R7 の実引用検証が4件すべて成功
- 四成分の内容監査がすべて成功
- report.md および summary.json 作成

## 次 Phase との境界

他 Proposition の一括登録と backward search 接続は対象外。

## `phase163_r4_r11_prop56_remaining.py`

```python
"""R4-R11: typed integrity checks for remaining Proposition 5.6 components.

This reads structured registry snapshots. It does not infer a citation,
change a renderer, or silently substitute group generators or range facts.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import GeneratorSymbol, HomotopyElement, ScalarProduct, ScalarSum, ScalarSymbol, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from proof import Relation, RelationType
from scalar_rules import ScalarGreaterEqualStatement


LOCATOR = "Proposition 5.6"
COMPONENT_KEYS = (
    "pi6_3_group_relation",
    "pi7_4_group_relation",
    "pi8_5_group_relation",
    "higher_nu_group_relation",
)


@dataclass(frozen=True)
class ComponentIntegrity:
    component_key: str
    generator: object
    order: object
    scope: str | None
    status: str


def _nu(element: object, *, index: int | None = None, prime: bool = False) -> bool:
    if not isinstance(element, HomotopyElement):
        return False
    symbol = element.generator
    if not isinstance(symbol, GeneratorSymbol) or symbol.family != "ν":
        return False
    if prime:
        return symbol.decoration == "′"
    return symbol.index == index and symbol.decoration is None


def _relation(snapshot: RegistryBridgeResult, key: str) -> Relation:
    if not isinstance(snapshot, RegistryBridgeResult):
        raise TypeError("snapshot must be RegistryBridgeResult")
    if key not in COMPONENT_KEYS:
        raise ValueError("Unsupported Proposition 5.6 component")
    assertion_id = f"boundary:{LOCATOR}:{key}"
    records = [record for record in snapshot.records if record.assertion_id == assertion_id]
    if len(records) != 1 or records[0].status is not MigrationStatus.STRUCTURED:
        raise ValueError(f"{key} must be uniquely STRUCTURED")
    conclusion = snapshot.registry.assertion(assertion_id).content
    if not isinstance(conclusion, Relation) or conclusion.relation_type is not RelationType.EQUALITY:
        raise ValueError("Expected typed equality Relation")
    return conclusion


def verify_prop56_remaining_component(
    snapshot: RegistryBridgeResult,
    component_key: str,
    *,
    higher_range: object | None = None,
) -> ComponentIntegrity:
    """Require exact structural generator data, not only abstract group order."""
    statement = _relation(snapshot, component_key)
    left, right = statement.lhs, statement.rhs
    if not isinstance(left, TodaPrimaryGroup):
        raise ValueError("Expected TodaPrimaryGroup")

    if component_key == "pi6_3_group_relation":
        if (left.group_dimension, left.sphere_dimension) != (6, 3):
            raise ValueError("Wrong pi6_3 group")
        if not isinstance(right, FiniteCyclicGroup) or right.order != 4 or not _nu(right.generator, prime=True):
            raise ValueError("pi6_3 order or nu-prime generator mismatch")
        return ComponentIntegrity(component_key, right.generator, 4, None, "GENERATOR_PRESERVED")

    if component_key == "pi7_4_group_relation":
        if (left.group_dimension, left.sphere_dimension) != (7, 4):
            raise ValueError("Wrong pi7_4 group")
        if not isinstance(right, DirectSumGroup) or len(right.summands) != 2:
            raise ValueError("pi7_4 must retain both direct summands")
        free, torsion = right.summands
        if not isinstance(free, FreeCyclicGroup) or not _nu(free.generator, index=4):
            raise ValueError("pi7_4 free generator mismatch")
        if (not isinstance(torsion, FiniteCyclicGroup) or torsion.order != 4
                or not isinstance(torsion.generator, Suspension)
                or not _nu(torsion.generator.expression, prime=True)):
            raise ValueError("pi7_4 torsion generator mismatch")
        return ComponentIntegrity(component_key, (free.generator, torsion.generator), (0, 4), None, "GENERATORS_PRESERVED")

    if component_key == "pi8_5_group_relation":
        if (left.group_dimension, left.sphere_dimension) != (8, 5):
            raise ValueError("Wrong pi8_5 group")
        if not isinstance(right, FiniteCyclicGroup) or right.order != 8 or not _nu(right.generator, index=5):
            raise ValueError("pi8_5 order or nu5 generator mismatch")
        return ComponentIntegrity(component_key, right.generator, 8, "n = 5", "GENERATOR_PRESERVED")

    if (not isinstance(left.sphere_dimension, ScalarSymbol)
            or left.sphere_dimension.name != "n"):
        raise ValueError("Higher group must retain symbolic n")
    n = left.sphere_dimension
    if left.group_dimension != ScalarSum(n, 3):
        raise ValueError("Higher group dimension must be n+3")
    if not isinstance(right, FiniteCyclicGroup) or right.order != 8:
        raise ValueError("Higher cyclic group must have order 8")
    if not _nu(right.generator, index=n):
        raise ValueError("Higher group must retain nu_n generator")
    if not isinstance(higher_range, ScalarGreaterEqualStatement) or higher_range.left != n or higher_range.right != 6:
        raise ValueError("Higher-group scope n >= 6 must be supplied and checked")
    assertion = snapshot.registry.assertion(f"boundary:{LOCATOR}:{component_key}")
    if assertion.scope != "n >= 6":
        raise ValueError("Higher-group registry scope must be n >= 6")
    return ComponentIntegrity(component_key, right.generator, 8, "n >= 6", "GENERATOR_AND_SCOPE_PRESERVED")
```

## `tests/test_phase163_r4_r11_prop56_remaining.py`

```python
from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, ScalarSum, ScalarSymbol, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_r11_prop56_remaining import (
    COMPONENT_KEYS,
    verify_prop56_remaining_component,
)
from phase163_r4_r7_representative_bindings import WitnessCandidate, bind_representative_witnesses
from phase163_r4_registry_bridge import build_registry_bridge
from proof import FoundationalReferenceIdentity, InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation, RelationType
from scalar_rules import ScalarGreaterEqualStatement


def _nu(index=None, prime=False):
    return HomotopyElement(
        name="ν′" if prime else f"ν{index}",
        dimension=3,
        generator=GeneratorSymbol(family="ν", decoration="′" if prime else None, index=index),
    )


def _citation(witness, locator, component, expected):
    identity = FoundationalReferenceIdentity(
        key=f"literature:{locator}:{component}", label=locator
    )
    leaf = ProofStep(expected, (), ProofRule.GIVEN, foundational_reference=identity)
    return ProofStep(
        expected, (leaf,), ProofRule.INFERENCE,
        foundational_reference=identity,
        inference_rule=InferenceRule(
            name="phase162_verified_literature_citation",
            literature_reference=LiteratureReference(label="Toda " + locator, locator=locator),
        ),
    )


def _relation(dimension, sphere, group):
    return Relation(TodaPrimaryGroup(dimension, sphere), group, RelationType.EQUALITY)


def _sample():
    n = ScalarSymbol("n")
    contents = {
        "pi6_3_group_relation": _relation(6, 3, FiniteCyclicGroup(4, _nu(prime=True))),
        "pi7_4_group_relation": _relation(7, 4, DirectSumGroup((FreeCyclicGroup(_nu(4)), FiniteCyclicGroup(4, Suspension(_nu(prime=True)))))),
        "pi8_5_group_relation": _relation(8, 5, FiniteCyclicGroup(8, _nu(5))),
        "higher_nu_group_relation": _relation(ScalarSum(n, 3), n, FiniteCyclicGroup(8, _nu(n))),
    }
    return contents


def _snapshot(contents):
    premise = ProofStep("source", (), ProofRule.GIVEN)
    candidates = tuple(
        WitnessCandidate(
            "Proposition 5.6", key,
            ProofStep(contents[key], (premise,), ProofRule.INFERENCE),
            contents[key], "focused test",
        )
        for key in COMPONENT_KEYS
    )
    snapshot, attempts = bind_representative_witnesses(
        build_registry_bridge(), candidates, citation_builder=_citation
    )
    assert all(attempt.status == "STRUCTURED" for attempt in attempts)
    return snapshot


def test_r4_r11_registers_four_typed_generators_and_scope():
    contents = _sample()
    snapshot = _snapshot(contents)
    n = ScalarSymbol("n")
    range_fact = ScalarGreaterEqualStatement(n, 6)
    for key in COMPONENT_KEYS:
        result = verify_prop56_remaining_component(
            snapshot, key,
            higher_range=range_fact if key == "higher_nu_group_relation" else None,
        )
        assert result.generator is not None
        assert result.status.startswith("GENERATOR")
        assert snapshot.registry.assertion(f"boundary:Proposition 5.6:{key}").content == contents[key]
    assert verify_prop56_remaining_component(snapshot, COMPONENT_KEYS[-1], higher_range=range_fact).scope == "n >= 6"


def test_r4_r11_pi6_3_rejects_wrong_generator():
    contents = _sample()
    contents["pi6_3_group_relation"] = _relation(6, 3, FiniteCyclicGroup(4, _nu(3)))
    with pytest.raises(ValueError, match="generator"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[0])


def test_r4_r11_pi7_4_rejects_lost_direct_sum():
    contents = _sample()
    contents["pi7_4_group_relation"] = _relation(7, 4, FiniteCyclicGroup(4, Suspension(_nu(prime=True))))
    with pytest.raises(ValueError, match="direct summands"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[1])


def test_r4_r11_pi7_4_rejects_wrong_free_generator():
    contents = _sample()
    contents["pi7_4_group_relation"] = _relation(7, 4, DirectSumGroup((FreeCyclicGroup(_nu(5)), FiniteCyclicGroup(4, Suspension(_nu(prime=True))))))
    with pytest.raises(ValueError, match="free generator"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[1])


def test_r4_r11_pi8_5_rejects_wrong_order():
    contents = _sample()
    contents["pi8_5_group_relation"] = _relation(8, 5, FiniteCyclicGroup(4, _nu(5)))
    with pytest.raises(ValueError, match="order"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[2])


def test_r4_r11_higher_requires_range_fact():
    with pytest.raises(ValueError, match="scope"):
        verify_prop56_remaining_component(_snapshot(_sample()), COMPONENT_KEYS[3])


def test_r4_r11_higher_rejects_wrong_generator():
    contents = _sample()
    n = ScalarSymbol("n")
    contents["higher_nu_group_relation"] = _relation(ScalarSum(n, 3), n, FiniteCyclicGroup(8, _nu(5)))
    with pytest.raises(ValueError, match="generator"):
        verify_prop56_remaining_component(_snapshot(contents), COMPONENT_KEYS[3], higher_range=ScalarGreaterEqualStatement(n, 6))


def test_r4_r11_unstructured_snapshot_is_rejected():
    with pytest.raises(ValueError, match="STRUCTURED"):
        verify_prop56_remaining_component(build_registry_bridge(), COMPONENT_KEYS[0])
```

## `audit.py`

```python
"""Use existing Phase 65 ProofSteps and R7 citation checks; never forge witnesses."""
from __future__ import annotations

import json
from pathlib import Path

from phase163_r4_r11_prop56_remaining import COMPONENT_KEYS, verify_prop56_remaining_component
from phase163_r4_r7_representative_bindings import WitnessCandidate, bind_representative_witnesses
from phase163_r4_registry_bridge import build_registry_bridge
from probes.probe_phase65_capabilities import build_phase65_representative_result
from proof import ProofRule


def run_audit(output_dir: Path) -> dict[str, object]:
    sample = build_phase65_representative_result()
    values = (
        ("pi6_3_group_relation", "pi6_3_step"),
        ("pi7_4_group_relation", "pi7_4_step"),
        ("pi8_5_group_relation", "pi8_5_step"),
        ("higher_nu_group_relation", "higher_step"),
    )
    candidates = tuple(
        WitnessCandidate(
            "Proposition 5.6", key, sample[name], sample[name].conclusion,
            f"Existing Phase65 {name}",
        )
        for key, name in values
    )
    if sample["higher_range_step"].rule is not ProofRule.GIVEN:
        raise ValueError("Unexpected high-range premise classification")
    base = build_registry_bridge()
    snapshot, attempts = bind_representative_witnesses(base, candidates)
    failures = tuple(attempt for attempt in attempts if attempt.status != "STRUCTURED")
    results = []
    if not failures:
        results = [
            verify_prop56_remaining_component(
                snapshot, key,
                higher_range=sample["higher_range_step"].conclusion if key == "higher_nu_group_relation" else None,
            )
            for key in COMPONENT_KEYS
        ]
    payload = {
        "phase": "163 R4-R11",
        "attempts": [{"component": a.component_key, "status": a.status, "detail": a.detail} for a in attempts],
        "integrity": [{"component": r.component_key, "status": r.status, "scope": r.scope,
                       "order": r.order if isinstance(r.order, int) else list(r.order)} for r in results],
        "source_independently_verified": False,
        "full_pytest_run": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R11 — Proposition 5.6 残り4成分", "", "| component | 接続 | 内容監査 | 範囲 |", "|---|---|---|---|"]
    outcome = {r.component_key: r for r in results}
    for attempt in attempts:
        result = outcome.get(attempt.component_key)
        lines.append(f"| `{attempt.component_key}` | {attempt.status} | {result.status if result else 'NOT_VERIFIED'} | {result.scope or '' if result else ''} |")
    lines += ["", "- 生成元・群構造は型付き Statement のまま保持", "- 文献原本との独立照合は未実施", "- 全体 pytest は未実施", ""]
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    if failures:
        raise RuntimeError(f"Citation verification failed: {failures}")
    return payload


if __name__ == "__main__":
    result = run_audit(Path("phase163_r4_r11_output"))
    print("Phase 163 R4-R11", {r["component"]: r["status"] for r in result["integrity"]})
    print("Saved phase163_r4_r11_output/report.md")
    print("Full pytest not run.")
```

## `run.ps1`

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'proof.py',
  'expression.py',
  'homotopy_groups.py',
  'toda_literature_statement_boundary.py',
  'phase162_reference_boundary.py',
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r6_structured_binding.py',
  'phase163_r4_r7_representative_bindings.py',
  'unified_statement_registry.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing required project file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r11_prop56_remaining.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_prop56_remaining.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r11_prop56_remaining.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r11_prop56_remaining.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r11_prop56_remaining.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 focused tests failed; audit skipped.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 actual registry audit failed.' }
Write-Host 'Phase 163 R4-R11 focused tests and representative audit finished. Full suite not run.'
```
