# Phase 163 R4-R10 — 変更コード全文

変更先はプロジェクト直下の `phase163_r4_r10_generator_integrity.py` と `tests/test_phase163_r4_r10_generator_integrity.py`。監査はパッケージ内の `audit.py` から実行。既存クラス・メソッド・import を変更しない。

追加する関数は `verify_prop56_pi5_2_generator()`、`_eta_index()`、監査用 `run_audit()`。クラス `GeneratorIntegrityResult` は新規。各ファイルの全文を示す。

## phase163_r4_r10_generator_integrity.py

```python
"""Phase 163 R4-R10: verify generator preservation in a typed fixed statement.

Read-only inspection of a registry snapshot; no renderer or proof changes.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from proof import Relation, RelationType


ASSERTION_ID = "boundary:Proposition 5.6:pi5_2_group_relation"
CANONICAL_LATEX = r"\pi_5^2=\mathbb{Z}/2\{\eta_2^3\}"


@dataclass(frozen=True)
class GeneratorIntegrityResult:
    assertion_id: str
    group_dimension: int
    sphere_dimension: int
    order: int
    generator: object
    canonical_latex: str
    status: str


def _eta_index(value: object, index: int) -> bool:
    return (
        isinstance(value, HomotopyElement)
        and isinstance(value.generator, GeneratorSymbol)
        and value.generator.family == "η"
        and value.generator.index == index
    )


def verify_prop56_pi5_2_generator(
    snapshot: RegistryBridgeResult,
) -> GeneratorIntegrityResult:
    """Fail closed unless the registered content includes the expected generator.

    The exact typed composite is checked: eta_2 o (eta_3 o eta_4).
    The mathematical notation eta_2^3 is a *display alias*, not a rewrite
    of the underlying Composition expression.
    """
    if not isinstance(snapshot, RegistryBridgeResult):
        raise TypeError("snapshot must be RegistryBridgeResult")
    records = tuple(r for r in snapshot.records if r.assertion_id == ASSERTION_ID)
    if len(records) != 1 or records[0].status is not MigrationStatus.STRUCTURED:
        raise ValueError("Proposition 5.6 pi5_2 must be uniquely STRUCTURED")
    statement = snapshot.registry.assertion(ASSERTION_ID).content
    if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
        raise ValueError("Registered content must be an equality Relation")
    group, cyclic = statement.lhs, statement.rhs
    if not isinstance(group, TodaPrimaryGroup) or (group.group_dimension, group.sphere_dimension) != (5, 2):
        raise ValueError("Unexpected source homotopy group")
    if not isinstance(cyclic, FiniteCyclicGroup) or cyclic.order != 2:
        raise ValueError("Expected a cyclic group of order two")
    generator = cyclic.generator
    if not (
        isinstance(generator, Composition)
        and _eta_index(generator.left, 2)
        and isinstance(generator.right, Composition)
        and _eta_index(generator.right.left, 3)
        and _eta_index(generator.right.right, 4)
    ):
        raise ValueError("Generator is missing or is not eta_2 o eta_3 o eta_4")
    return GeneratorIntegrityResult(
        assertion_id=ASSERTION_ID,
        group_dimension=5,
        sphere_dimension=2,
        order=2,
        generator=generator,
        canonical_latex=CANONICAL_LATEX,
        status="GENERATOR_PRESERVED",
    )

```

## tests/test_phase163_r4_r10_generator_integrity.py

```python
import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_r10_generator_integrity import (
    ASSERTION_ID,
    CANONICAL_LATEX,
    verify_prop56_pi5_2_generator,
)
from phase163_r4_r7_representative_bindings import (
    WitnessCandidate,
    bind_representative_witnesses,
)
from phase163_r4_registry_bridge import build_registry_bridge
from proof import (
    FoundationalReferenceIdentity,
    InferenceRule,
    LiteratureReference,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
)


def _citation(witness, locator, component, expected):
    identity = FoundationalReferenceIdentity(
        key=f"literature:{locator}:{component}", label=locator
    )
    leaf = ProofStep(
        conclusion=expected,
        premises=(),
        rule=ProofRule.GIVEN,
        foundational_reference=identity,
    )
    return ProofStep(
        conclusion=expected,
        premises=(leaf,),
        rule=ProofRule.INFERENCE,
        foundational_reference=identity,
        inference_rule=InferenceRule(
            name="phase162_verified_literature_citation",
            literature_reference=LiteratureReference(
                label="Toda " + locator, locator=locator
            ),
        ),
    )


def _element(index):
    return HomotopyElement(
        name=f"η{index}",
        dimension=index,
        generator=GeneratorSymbol(family="η", index=index),
    )


def _snapshot(generator, order=2):
    conclusion = Relation(
        lhs=TodaPrimaryGroup(group_dimension=5, sphere_dimension=2),
        rhs=FiniteCyclicGroup(order=order, generator=generator),
        relation_type=RelationType.EQUALITY,
    )
    given = ProofStep(conclusion="premise", premises=(), rule=ProofRule.GIVEN)
    witness = ProofStep(
        conclusion=conclusion, premises=(given,), rule=ProofRule.INFERENCE
    )
    candidate = WitnessCandidate(
        "Proposition 5.6", "pi5_2_group_relation",
        witness, conclusion, "focused test",
    )
    base = build_registry_bridge()
    snapshot, attempts = bind_representative_witnesses(
        base, (candidate,), citation_builder=_citation
    )
    assert attempts[0].status == "STRUCTURED"
    assert base.registry.assertion(ASSERTION_ID).content != conclusion
    return snapshot


def test_r4_r10_preserves_full_generator_and_standard_notation():
    generator = Composition(_element(2), Composition(_element(3), _element(4)))
    result = verify_prop56_pi5_2_generator(_snapshot(generator))
    assert result.generator == generator
    assert result.order == 2
    assert result.canonical_latex == CANONICAL_LATEX
    assert result.status == "GENERATOR_PRESERVED"


def test_r4_r10_rejects_missing_generator():
    with pytest.raises(ValueError, match="Generator"):
        verify_prop56_pi5_2_generator(_snapshot(None))


def test_r4_r10_rejects_wrong_generator():
    generator = Composition(_element(2), Composition(_element(3), _element(5)))
    with pytest.raises(ValueError, match="Generator"):
        verify_prop56_pi5_2_generator(_snapshot(generator))


def test_r4_r10_requires_structured_registration():
    with pytest.raises(ValueError, match="STRUCTURED"):
        verify_prop56_pi5_2_generator(build_registry_bridge())


def test_r4_r10_rejects_wrong_order():
    generator = Composition(_element(2), Composition(_element(3), _element(4)))
    with pytest.raises(ValueError, match="order two"):
        verify_prop56_pi5_2_generator(_snapshot(generator, order=4))


def test_r4_r10_rejects_wrong_argument_type():
    with pytest.raises(TypeError, match="RegistryBridgeResult"):
        verify_prop56_pi5_2_generator(None)

```

## audit.py

```python
"""Audit the actual Phase 65 representative through the Phase 163 R7 binding."""
from __future__ import annotations

import json
from pathlib import Path

from phase163_r4_r10_generator_integrity import (
    ASSERTION_ID,
    verify_prop56_pi5_2_generator,
)
from phase163_r4_r7_representative_bindings import (
    bind_representative_witnesses,
    representative_candidates,
)
from phase163_r4_registry_bridge import build_registry_bridge


def run_audit(output_dir: Path) -> dict[str, object]:
    base = build_registry_bridge()
    candidates = tuple(
        candidate for candidate in representative_candidates()
        if (candidate.reference_locator, candidate.component_key)
        == ("Proposition 5.6", "pi5_2_group_relation")
    )
    if len(candidates) != 1:
        raise ValueError("Expected exactly one real Phase 65 proposition witness")
    snapshot, attempts = bind_representative_witnesses(base, candidates)
    if len(attempts) != 1 or attempts[0].status != "STRUCTURED":
        raise ValueError(f"Actual witness failed verification: {attempts}")
    integrity = verify_prop56_pi5_2_generator(snapshot)
    payload = {
        "phase": "163 R4-R10",
        "assertion_id": ASSERTION_ID,
        "status": integrity.status,
        "registration": attempts[0].status,
        "order": integrity.order,
        "generator_structure": "Composition(eta_2, Composition(eta_3, eta_4))",
        "canonical_latex": integrity.canonical_latex,
        "note": "Existing registered mathematical content is preserved; no production renderer or registration rewrite.",
        "literature_source_independently_verified": False,
        "full_pytest_run": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "report.md").write_text(
        "# Phase 163 R4-R10 — Proposition 5.6 生成元保持監査\n\n"
        f"- Assertion: `{ASSERTION_ID}`\n"
        f"- 結果: `{integrity.status}`\n"
        f"- 登録状態: `{attempts[0].status}`\n"
        f"- 位数: {integrity.order}\n"
        f"- 生成元内部構造: `Composition(eta_2, Composition(eta_3, eta_4))`\n"
        f"- 標準表示: `${integrity.canonical_latex}$`\n"
        "- 既存の登録内容・Renderer は変更していません\n"
        "- 文献原本との独立照合は未完了\n"
        "- 全体 pytest は未実施\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    result = run_audit(Path("phase163_r4_r10_output"))
    print(f"Phase 163 R4-R10: {result['status']}")
    print("Saved phase163_r4_r10_output/report.md")
    print("Full pytest not run.")

```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'proof.py',
  'expression.py',
  'homotopy_groups.py',
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
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r10_generator_integrity.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r10_generator_integrity.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r10_generator_integrity.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r10_generator_integrity.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r10_generator_integrity.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R10 focused tests failed; audit skipped.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R10 actual generator audit failed.' }
Write-Host 'Phase 163 R4-R10 focused checks finished. Full suite not run.'

```

## 検証

`python -B -m pytest -q tests/test_phase163_r4_r10_generator_integrity.py`

監査成功条件: 実際の Proposition 5.6 の `ProofStep` が STRUCTURED となり、登録 Assertion の位数が2、生成元が eta2∘eta3∘eta4。

Phase 164 の backward search 接続は行わない。全体 pytest は Phase 163 最終段階のみ。
