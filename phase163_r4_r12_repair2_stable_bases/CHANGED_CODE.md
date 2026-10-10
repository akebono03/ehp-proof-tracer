# Phase 163 R4-R12 repair2 — 置換可能なコード全文

新規ファイルのみ。既存関数・クラスの置換はありません。


## audit.py

```python
"""Phase 163 R4-R12 repair2 focused stable-base audit."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) in sys.path:
    sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))

from phase163_r4_r12_stable_bases import (
    BASE_ID_1, BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2,
    existing_stable_minimal_registration,
)


def run_audit(destination: Path) -> dict[str, object]:
    result = existing_stable_minimal_registration()
    registry = result.snapshot.registry
    targets = (BASE_ID_1, BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2)
    statements = {key: registry.assertion(key) for key in targets}
    output = {
        "phase": "163 R4-R12 repair2",
        "status": "TYPED_SOURCE_UNVERIFIED",
        "new_independent_minimum": BASE_ID_1,
        "existing_independent_minimum": BASE_ID_2,
        "generic_1_scope": statements[GENERAL_ID_1].scope,
        "generic_2_scope": statements[GENERAL_ID_2].scope,
        "1_stem_relation": result.relation_1,
        "2_stem_relation": result.relation_2,
        "source_verification": result.source_status,
        "proof_ancestry": result.proof_status,
        "base_1_generator": repr(statements[BASE_ID_1].content.rhs.generator),
        "base_2_generator": repr(statements[BASE_ID_2].content.rhs.generator),
        "proof_links_count": len(result.snapshot.proof_links),
    }
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "summary.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R12 repair2 — stable 最低次元の独立登録",
        "", "状態: TYPED_SOURCE_UNVERIFIED", "",
        "| stem | 最低次元 Statement | 一般形の範囲 | 関係 |",
        "|---|---|---|---|",
        f"| 1-stem | `{BASE_ID_1}` | n >= 3 | n=3 は適用範囲内、個別の導出結果として記録 |",
        f"| 2-stem | `{BASE_ID_2}` | n >= 5 | n=4 は適用範囲外、既存の独立成分を保持 |",
        "", "pi_4^3 の出典候補は現行 Phase 50 の final_group_step.conclusion です。",
        "新しい文献固定成分と断定せず、PROOF_INTERNAL（導出結果）として区別しています。",
        "Proposition 5.1／5.3 の既存8成分や ProofStepLink は変更していません。",
        "原典の独立照合・証明木全祖先の検証・全体 pytest は未実施です。", "",
    ]
    (destination / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    result = run_audit(Path("phase163_r4_r12_repair2_output"))
    print("Phase 163 R4-R12 repair2:", result["status"])
    print("Minimum stem entries: 2 (new 1, reused 1)")
    print("Saved phase163_r4_r12_repair2_output/report.md")
    print("Full pytest not run.")

```


## phase163_r4_r12_stable_bases.py

```python
"""Phase 163 R4-R12 repair2: separate minimal stable-stem records.

The pi_4^3 record is an existing derived concrete statement associated with
Proposition 5.1, not a newly asserted literal component of that publication.
The pi_6^4 record already exists in the Proposition 5.3 fixed catalog.
Neither record certifies ancestry or independent literature verification.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import HomotopyElement, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase163_r4_r12_literature_registration import (
    LiteratureComponentRegistrationResult,
    existing_prop51_prop53_candidates,
    register_prop51_prop53_literature_statements,
)
from proof import Relation, RelationType
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, UnifiedStatementRegistry,
)

BASE_ID_1 = "stable-base:1-stem:pi4_3_group_relation"
BASE_ID_2 = "boundary:Proposition 5.3:pi6_4_group_relation"
GENERAL_ID_1 = "boundary:Proposition 5.1:higher_eta_group_relation"
GENERAL_ID_2 = "boundary:Proposition 5.3:higher_eta_squared_group_relation"


@dataclass(frozen=True)
class StableBaseRegistration:
    snapshot: RegistryBridgeResult
    base_1_id: str
    base_2_id: str
    relation_1: str
    relation_2: str
    source_status: str = "SOURCE_UNVERIFIED"
    proof_status: str = "PROOF_ANCESTRY_NOT_CHECKED"


def _check_pi4_3(value: object) -> None:
    if not isinstance(value, Relation) or value.relation_type is not RelationType.EQUALITY:
        raise ValueError("pi_4^3 must be an equality Relation")
    if value.lhs != TodaPrimaryGroup(group_dimension=4, sphere_dimension=3):
        raise ValueError("expected pi_4^3")
    if not isinstance(value.rhs, FiniteCyclicGroup) or value.rhs.order != 2:
        raise ValueError("pi_4^3 must be cyclic of order two")
    eta = value.rhs.generator
    if not isinstance(eta, HomotopyElement):
        raise ValueError("generator must be HomotopyElement")
    if (eta.generator is None or eta.generator.family != "η"
            or eta.generator.index != 3 or eta.dimension != 3
            or eta.source != 4 or eta.target != 3):
        raise ValueError("pi_4^3 must preserve eta_3")


def register_stable_minimal_dimensions(
    previous: LiteratureComponentRegistrationResult,
    pi4_3_statement: object,
) -> StableBaseRegistration:
    """Add a separate pi_4^3 record; preserve the existing pi_6^4 record.

    The 1-stem boundary is a specialization within n>=3.  The 2-stem
    minimum n=4 lies outside the 5.3 higher-formula scope n>=5.
    """
    if not isinstance(previous, LiteratureComponentRegistrationResult):
        raise TypeError("previous must be LiteratureComponentRegistrationResult")
    base = previous.snapshot
    _check_pi4_3(pi4_3_statement)
    existing_ids = {record.assertion_id for record in base.records}
    if BASE_ID_1 in existing_ids:
        raise ValueError("pi_4^3 minimal dimension already registered")
    if not {BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2}.issubset(existing_ids):
        raise ValueError("required Proposition 5.1/5.3 components missing")
    if not {e.assertion_id for e in previous.evidence}.issuperset({BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2}):
        raise ValueError("required components are not part of the typed registration")
    pi6 = base.registry.assertion(BASE_ID_2)
    if not isinstance(pi6.content, Relation) or pi6.content.lhs != TodaPrimaryGroup(
        group_dimension=6, sphere_dimension=4
    ):
        raise ValueError("pi_6^4 must be stored independently")
    if (not isinstance(pi6.content.rhs, FiniteCyclicGroup)
            or pi6.content.rhs.order != 2):
        raise ValueError("pi_6^4 order mismatch")
    generic_1 = base.registry.assertion(GENERAL_ID_1)
    generic_2 = base.registry.assertion(GENERAL_ID_2)
    if generic_1.scope != "n >= 3" or generic_2.scope != "n >= 5":
        raise ValueError("unexpected stable higher-formula scope")
    # Copy the existing registry without changing any existing assertion.
    registry = UnifiedStatementRegistry()
    seen: set[str] = set()
    for record in base.records:
        if record.assertion_id is None:
            continue
        assertion = base.registry.assertion(record.assertion_id)
        if assertion.reference_id not in seen:
            registry.add_reference(base.registry.reference(assertion.reference_id))
            seen.add(assertion.reference_id)
        registry.add_assertion(assertion)
    # A separate derived concrete fact, associated with the existing literature
    # reference but NOT represented as an additional fixed-literature component.
    registry.add_assertion(AssertionEntry(
        assertion_id=BASE_ID_1,
        reference_id=generic_1.reference_id,
        kind=AssertionKind.STATEMENT,
        content=pi4_3_statement,
        origin=AssertionOrigin.PROOF_INTERNAL,
        dependencies=(GENERAL_ID_1,),
    ))
    new_record = MigrationRecord(
        source="stable_base_specialization",
        source_key="1-stem/pi4_3",
        assertion_id=BASE_ID_1,
        status=MigrationStatus.STRUCTURED,
        detail=("Typed pi_4^3 result from existing Phase 50; specialization of "
                "5.1 n>=3; neither literature independently checked nor ancestry certified"),
    )
    return StableBaseRegistration(
        snapshot=RegistryBridgeResult(registry, base.records + (new_record,), base.proof_links),
        base_1_id=BASE_ID_1,
        base_2_id=BASE_ID_2,
        relation_1="WITHIN_GENERAL_SCOPE_N_EQUALS_3",
        relation_2="INDEPENDENT_MINIMUM_N_EQUALS_4_OUTSIDE_GENERAL_N_GE_5",
    )


def existing_stable_minimal_registration() -> StableBaseRegistration:
    """Construct candidate values from existing builders, without traversing ancestry."""
    from phase163_r4_registry_bridge import build_registry_bridge
    from toda_upstream_bootstrap import _build_phase50_result

    previous = register_prop51_prop53_literature_statements(
        build_registry_bridge(), existing_prop51_prop53_candidates()
    )
    pi4_3 = _build_phase50_result()["final_group_step"].conclusion
    return register_stable_minimal_dimensions(previous, pi4_3)

```


## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r12_literature_registration.py',
  'tests\test_phase163_r4_r12_literature_registration.py',
  'toda_upstream_bootstrap.py',
  'tests\test_phase59_prop53_integration.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing project file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r12_stable_bases.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r12_stable_bases.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r12_stable_bases.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r12_stable_bases.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r12_literature_registration.py tests/test_phase163_r4_r12_audit_import.py tests/test_phase163_r4_r12_stable_bases.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 repair2 focused tests failed.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 repair2 audit failed.' }
Write-Host 'R4-R12 repair2 stable base registration completed. Full pytest not run.'

```


## tests/test_phase163_r4_r12_stable_bases.py

```python
from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from phase163_r4_r12_literature_registration import (
    existing_prop51_prop53_candidates,
    register_prop51_prop53_literature_statements,
)
from phase163_r4_r12_stable_bases import (
    BASE_ID_1, BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2,
    _check_pi4_3, existing_stable_minimal_registration,
    register_stable_minimal_dimensions,
)
from unified_statement_registry import AssertionOrigin
from toda_upstream_bootstrap import _build_phase50_result


def _previous():
    return register_prop51_prop53_literature_statements(
        build_registry_bridge(), existing_prop51_prop53_candidates()
    )


def test_minimal_stems_are_distinct_typed_entries():
    result = existing_stable_minimal_registration()
    first = result.snapshot.registry.assertion(BASE_ID_1)
    second = result.snapshot.registry.assertion(BASE_ID_2)
    assert first.content.lhs == TodaPrimaryGroup(group_dimension=4, sphere_dimension=3)
    assert second.content.lhs == TodaPrimaryGroup(group_dimension=6, sphere_dimension=4)
    assert first.origin is AssertionOrigin.PROOF_INTERNAL
    assert second.origin is AssertionOrigin.FIXED_STATEMENT
    assert result.base_1_id != result.base_2_id


def test_correct_boundaries_do_not_specialize_n4_from_n_ge_5():
    result = existing_stable_minimal_registration()
    assert result.snapshot.registry.assertion(GENERAL_ID_1).scope == "n >= 3"
    assert result.snapshot.registry.assertion(GENERAL_ID_2).scope == "n >= 5"
    assert result.relation_1 == "WITHIN_GENERAL_SCOPE_N_EQUALS_3"
    assert result.relation_2 == "INDEPENDENT_MINIMUM_N_EQUALS_4_OUTSIDE_GENERAL_N_GE_5"


def test_pi4_3_generator_is_preserved():
    statement = existing_stable_minimal_registration().snapshot.registry.assertion(BASE_ID_1).content
    assert statement.rhs.order == 2
    assert statement.rhs.generator.generator == GeneratorSymbol(family="η", index=3)
    assert statement.rhs.generator.source == 4
    assert statement.rhs.generator.target == 3


def test_rejects_incorrect_pi4_3_generator():
    statement = _build_phase50_result()["final_group_step"].conclusion
    wrong = replace(statement, rhs=FiniteCyclicGroup(
        order=2,
        generator=HomotopyElement(name="η₅", dimension=5, source=6, target=5,
                                 generator=GeneratorSymbol(family="η", index=5)),
    ))
    with pytest.raises(ValueError):
        _check_pi4_3(wrong)


def test_rejects_incorrect_pi4_3_order():
    statement = _build_phase50_result()["final_group_step"].conclusion
    with pytest.raises(ValueError):
        _check_pi4_3(replace(statement, rhs=FiniteCyclicGroup(
            order=4, generator=statement.rhs.generator
        )))


def test_preserves_existing_eight_and_proof_links():
    previous = _previous()
    statement = _build_phase50_result()["final_group_step"].conclusion
    result = register_stable_minimal_dimensions(previous, statement)
    assert result.snapshot.proof_links == previous.snapshot.proof_links
    assert result.snapshot.records[:-1] == previous.snapshot.records
    for evidence in previous.evidence:
        assert (result.snapshot.registry.assertion(evidence.assertion_id)
                == previous.snapshot.registry.assertion(evidence.assertion_id))
    assert result.snapshot.records[-1].status is MigrationStatus.STRUCTURED


def test_no_unverified_proofstep_link_is_added():
    result = existing_stable_minimal_registration()
    assert all(link.assertion_id != BASE_ID_1 for link in result.snapshot.proof_links)
    assert result.source_status == "SOURCE_UNVERIFIED"
    assert result.proof_status == "PROOF_ANCESTRY_NOT_CHECKED"


def test_rejects_untyped_previous_result():
    with pytest.raises(TypeError):
        register_stable_minimal_dimensions(object(), object())

```
