# Phase 163 R4-R12 — 変更コード全文

既存のファイル・クラス・関数には変更なし。次の4ファイルを新規追加する。

## 変更対象と追加位置

- `phase163_r4_r12_literature_registration.py` — 新規：登録処理および8成分の型・位数・生成元・範囲検査
- `tests/test_phase163_r4_r12_literature_registration.py` — 新規：軽量テスト8件
- `audit.py` — 新規：読み取り専用監査
- `run.ps1` — 新規：展開後のインストール・軽量テスト・監査

登録コードはプロジェクト直下へ、テストは `tests/` へコピーされる。`audit.py` と `run.ps1` はパッケージディレクトリから実行。

## 完了条件と Phase 境界

- Proposition 5.1 と Proposition 5.3 の計8成分が型付きで取得できる。
- 位数・生成元・5.1 n>=3・5.3 n>=5 の構造条件を軽量テストで検査。
- `SOURCE_UNVERIFIED` と `PROOF_ANCESTRY_NOT_CHECKED` を明示。
- ProofStepLink、既存原本、Renderer、Backward Search は変更しない。
- Phase 164 の探索接続、文献原典の独立検証、Phase 163 最終全体テストは対象外。

## `phase163_r4_r12_literature_registration.py` — 全文

```python
"""Phase 163 R4-R12: typed source-unverified registrations for Toda 5.1/5.3.

Uses existing aggregate statement values, not their proof ancestry. A typed
registration is not evidence that the printed literature has been checked.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import sys

from expression import Composition, HomotopyElement, MapApplication, Multiple, ScalarSum, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from proof import Relation, RelationType
from scalar_rules import ScalarGreaterEqualStatement
from toda_rules import TodaDeltaImageUpToSignStatement, TodaProp51FiniteDimensionalStatement, TodaProp53FiniteDimensionalStatement
from unified_statement_registry import AssertionKind, UnifiedStatementRegistry

COMPONENTS = {
    "Proposition 5.1": (
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    ),
    "Proposition 5.3": (
        "pi4_2_group_relation", "pi5_3_group_relation",
        "pi6_4_group_relation", "higher_eta_squared_group_relation",
    ),
}
SCOPES = {"Proposition 5.1": 3, "Proposition 5.3": 5}


@dataclass(frozen=True)
class LiteratureComponentInput:
    locator: str
    component_key: str
    statement: object
    source_description: str
    scope_statement: object | None = None

    def __post_init__(self) -> None:
        if self.locator not in COMPONENTS or self.component_key not in COMPONENTS[self.locator]:
            raise ValueError("unrecognized literature component")
        if not isinstance(self.source_description, str) or not self.source_description.strip():
            raise ValueError("source_description is required")
        if self.statement is None:
            raise ValueError("statement is required")


@dataclass(frozen=True)
class LiteratureComponentEvidence:
    assertion_id: str
    source_description: str
    verification_status: str = "SOURCE_UNVERIFIED"
    proof_status: str = "PROOF_ANCESTRY_NOT_CHECKED"


@dataclass(frozen=True)
class LiteratureComponentRegistrationResult:
    snapshot: RegistryBridgeResult
    evidence: tuple[LiteratureComponentEvidence, ...]


def _eta(element: object, index: int | ScalarSymbol | ScalarSum) -> bool:
    return (
        isinstance(element, HomotopyElement)
        and element.generator is not None
        and element.generator.family == "η"
        and element.generator.index == index
    )


def _group_relation(value: object, k: int, n: int, order: int | None) -> None:
    if not isinstance(value, Relation) or value.relation_type is not RelationType.EQUALITY:
        raise ValueError("expected group equality Relation")
    if value.lhs != TodaPrimaryGroup(group_dimension=k, sphere_dimension=n):
        raise ValueError("wrong homotopy group")
    if order is None:
        if not isinstance(value.rhs, FreeCyclicGroup):
            raise ValueError("free cyclic group required")
    else:
        if not isinstance(value.rhs, FiniteCyclicGroup) or value.rhs.order != order:
            raise ValueError("wrong finite cyclic order")
    if value.rhs.generator is None:
        raise ValueError("generator is missing")


def _scope(value: object, minimum: int) -> ScalarSymbol:
    if not isinstance(value, ScalarGreaterEqualStatement):
        raise ValueError("typed higher-dimensional scope is required")
    if value.right != minimum or value.left != ScalarSymbol(name="n"):
        raise ValueError("higher-dimensional scope mismatch")
    return value.left


def _validate_component(item: LiteratureComponentInput) -> None:
    key = item.component_key
    statement = item.statement
    higher_key = COMPONENTS[item.locator][-1]
    if key == higher_key:
        n = _scope(item.scope_statement, SCOPES[item.locator])
        if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
            raise ValueError("higher group relation must be an equality")
        expected_offset = 1 if item.locator == "Proposition 5.1" else 2
        if statement.lhs != TodaPrimaryGroup(
            group_dimension=ScalarSum(left=n, right=expected_offset), sphere_dimension=n
        ):
            raise ValueError("higher group dimension mismatch")
        if not isinstance(statement.rhs, FiniteCyclicGroup) or statement.rhs.order != 2:
            raise ValueError("higher cyclic group must have order two")
        gen = statement.rhs.generator
        if item.locator == "Proposition 5.1":
            if not _eta(gen, n):
                raise ValueError("higher eta generator mismatch")
        else:
            if not isinstance(gen, Composition) or not _eta(gen.left, n):
                raise ValueError("higher eta-squared generator mismatch")
            if not _eta(gen.right, ScalarSum(left=n, right=1)):
                raise ValueError("higher eta-squared second factor mismatch")
        return
    if item.scope_statement is not None:
        raise ValueError("unexpected scope for concrete statement")
    if item.locator == "Proposition 5.1":
        if key == "pi3_2_group_relation":
            _group_relation(statement, 3, 2, None)
            if not _eta(statement.rhs.generator, 2):
                raise ValueError("pi3_2 generator must be eta2")
        elif key == "eta2_hopf_relation":
            if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
                raise ValueError("Hopf equality required")
            if not isinstance(statement.lhs, MapApplication) or statement.lhs.map != EHP_H_MAP:
                raise ValueError("Hopf map must be H")
            if not _eta(statement.lhs.expression, 2):
                raise ValueError("Hopf relation argument must be eta2")
            if statement.rhs is None:
                raise ValueError("Hopf value is missing")
        elif key == "delta_iota5_relation":
            if not isinstance(statement, TodaDeltaImageUpToSignStatement):
                raise ValueError("signed Delta-image statement required")
            if not isinstance(statement.positive_value, Multiple) or statement.positive_value.coefficient != 2:
                raise ValueError("Delta positive value must be twice a generator")
            if not _eta(statement.positive_value.expression, 2):
                raise ValueError("Delta image requires eta2")
    else:
        indices = {
            "pi4_2_group_relation": (4, 2),
            "pi5_3_group_relation": (5, 3),
            "pi6_4_group_relation": (6, 4),
        }
        k, n = indices[key]
        _group_relation(statement, k, n, 2)
        gen = statement.rhs.generator
        if not isinstance(gen, Composition) or not _eta(gen.left, n) or not _eta(gen.right, n + 1):
            raise ValueError("eta-square generator not preserved")


def register_prop51_prop53_literature_statements(
    base: RegistryBridgeResult,
    inputs: tuple[LiteratureComponentInput, ...],
) -> LiteratureComponentRegistrationResult:
    """Copy validated mathematical contents into a new metadata-bridge snapshot."""
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    if not isinstance(inputs, tuple) or any(not isinstance(i, LiteratureComponentInput) for i in inputs):
        raise TypeError("inputs must be typed tuple")
    expected = {(locator, key) for locator, keys in COMPONENTS.items() for key in keys}
    keys = [(i.locator, i.component_key) for i in inputs]
    if len(keys) != len(expected) or set(keys) != expected:
        raise ValueError("exactly eight distinct 5.1/5.3 components required")
    lookup = {r.assertion_id: r for r in base.records}
    for item in inputs:
        assertion_id = f"boundary:{item.locator}:{item.component_key}"
        record = lookup.get(assertion_id)
        if record is None or record.source != "boundary" or record.status is not MigrationStatus.METADATA_ONLY:
            raise ValueError("target boundary must be metadata_only")
        _validate_component(item)
    replacements = {
        f"boundary:{item.locator}:{item.component_key}": item.statement
        for item in inputs
    }
    registry = UnifiedStatementRegistry()
    seen_references: set[str] = set()
    for record in base.records:
        if record.assertion_id is None:
            continue
        assertion = base.registry.assertion(record.assertion_id)
        if assertion.reference_id not in seen_references:
            registry.add_reference(base.registry.reference(assertion.reference_id))
            seen_references.add(assertion.reference_id)
        if record.assertion_id in replacements:
            assertion = replace(assertion, kind=AssertionKind.STATEMENT, content=replacements[record.assertion_id])
        registry.add_assertion(assertion)
    records = tuple(
        replace(record, status=MigrationStatus.STRUCTURED,
                detail="Typed source-unverified candidate; no proof ancestry certification")
        if record.assertion_id in replacements else record
        for record in base.records
    )
    evidence = tuple(LiteratureComponentEvidence(
        assertion_id=f"boundary:{item.locator}:{item.component_key}",
        source_description=item.source_description,
    ) for item in inputs)
    return LiteratureComponentRegistrationResult(
        snapshot=RegistryBridgeResult(registry, records, base.proof_links),
        evidence=evidence,
    )


def existing_prop51_prop53_candidates() -> tuple[LiteratureComponentInput, ...]:
    """Use existing aggregate Statement objects, not their derivation ancestry."""
    tests_dir = Path(__file__).resolve().parent / "tests"
    if str(tests_dir) not in sys.path:
        sys.path.insert(0, str(tests_dir))
    from toda_prop56_zero_bootstrap import _build_prop51_step
    from test_phase59_prop53_integration import build_phase59_8_data

    prop51 = _build_prop51_step().conclusion
    prop53_fixture = build_phase59_8_data()
    prop53 = prop53_fixture["integration_step"].conclusion
    if not isinstance(prop51, TodaProp51FiniteDimensionalStatement):
        raise ValueError("unexpected Proposition 5.1 aggregate Statement")
    if not isinstance(prop53, TodaProp53FiniteDimensionalStatement):
        raise ValueError("unexpected Proposition 5.3 aggregate Statement")
    inputs: list[LiteratureComponentInput] = []
    for locator, aggregate in (("Proposition 5.1", prop51), ("Proposition 5.3", prop53)):
        for key in COMPONENTS[locator]:
            inputs.append(LiteratureComponentInput(
                locator=locator,
                component_key=key,
                statement=getattr(aggregate, key),
                source_description=f"Existing typed aggregate {type(aggregate).__name__}.{key}",
                scope_statement=(
                    prop53_fixture["higher_range_step"].conclusion
                    if locator == "Proposition 5.3"
                    else ScalarGreaterEqualStatement(left=ScalarSymbol(name="n"), right=3)
                ) if key == COMPONENTS[locator][-1] else None,
            ))
    return tuple(inputs)
```

## `tests/test_phase163_r4_r12_literature_registration.py` — 全文

```python
from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from phase163_r4_r12_literature_registration import (
    COMPONENTS, LiteratureComponentInput, _validate_component,
    register_prop51_prop53_literature_statements,
)
from proof import Relation, RelationType
from scalar_rules import ScalarGreaterEqualStatement


def _inputs():
    from phase163_r4_r12_literature_registration import existing_prop51_prop53_candidates
    return existing_prop51_prop53_candidates()


def test_registers_all_eight_and_preserves_source_metadata():
    base = build_registry_bridge()
    output = register_prop51_prop53_literature_statements(base, _inputs())
    assert len(output.evidence) == 8
    assert output.snapshot.proof_links == base.proof_links
    for record in output.snapshot.records:
        if record.assertion_id in {e.assertion_id for e in output.evidence}:
            assert record.status is MigrationStatus.STRUCTURED
            assert base.registry.assertion(record.assertion_id).content != output.snapshot.registry.assertion(record.assertion_id).content
            assert any(old.assertion_id == record.assertion_id and old.status is MigrationStatus.METADATA_ONLY for old in base.records)
    assert all(e.verification_status == "SOURCE_UNVERIFIED" for e in output.evidence)
    assert all(e.proof_status == "PROOF_ANCESTRY_NOT_CHECKED" for e in output.evidence)


def test_raises_on_missing_or_duplicate_component():
    base = build_registry_bridge()
    inputs = _inputs()
    with pytest.raises(ValueError):
        register_prop51_prop53_literature_statements(base, inputs[:-1])
    with pytest.raises(ValueError):
        register_prop51_prop53_literature_statements(base, inputs[:-1] + (inputs[0],))


def test_rejects_group_wrong_generator():
    item = next(i for i in _inputs() if i.component_key == "pi4_2_group_relation")
    wrong = replace(item.statement, rhs=FiniteCyclicGroup(
        order=2, generator=HomotopyElement(
            name="other", dimension=2, generator=GeneratorSymbol(family="η", index=7)
        )
    ))
    with pytest.raises(ValueError):
        _validate_component(replace(item, statement=wrong))


def test_rejects_wrong_higher_scope():
    item = next(i for i in _inputs() if i.component_key == "higher_eta_squared_group_relation")
    with pytest.raises(ValueError):
        _validate_component(replace(item, scope_statement=ScalarGreaterEqualStatement(
            left=ScalarSymbol(name="n"), right=4
        )))


def test_rejects_missing_scope_and_concrete_extra_scope():
    inputs = _inputs()
    higher = next(i for i in inputs if i.component_key == "higher_eta_group_relation")
    concrete = next(i for i in inputs if i.component_key == "pi5_3_group_relation")
    with pytest.raises(ValueError):
        _validate_component(replace(higher, scope_statement=None))
    with pytest.raises(ValueError):
        _validate_component(replace(concrete, scope_statement=ScalarGreaterEqualStatement(
            left=ScalarSymbol(name="n"), right=5
        )))


def test_registration_does_not_replace_unrelated_records():
    base = build_registry_bridge()
    output = register_prop51_prop53_literature_statements(base, _inputs())
    targets = {e.assertion_id for e in output.evidence}
    assert all(a == b for a, b in zip(
        (r for r in base.records if r.assertion_id not in targets),
        (r for r in output.snapshot.records if r.assertion_id not in targets),
    ))


def test_validation_rejects_incorrect_delta_relation():
    item = next(i for i in _inputs() if i.component_key == "delta_iota5_relation")
    with pytest.raises(ValueError):
        _validate_component(replace(item, statement=Relation(
            lhs="Delta", rhs=0, relation_type=RelationType.EQUALITY
        )))


def test_rejects_wrong_locator_or_unknown_component():
    with pytest.raises(ValueError):
        LiteratureComponentInput("Proposition 5.6", "pi3_2_group_relation", object(), "candidate")
    with pytest.raises(ValueError):
        LiteratureComponentInput("Proposition 5.1", "pi999_group_relation", object(), "candidate")
```

## `audit.py` — 全文

```python
"""Read-only literature statement registration audit for Proposition 5.1/5.3."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r12_literature_registration import (
    COMPONENTS, existing_prop51_prop53_candidates,
    register_prop51_prop53_literature_statements,
)


def run_audit(directory: Path) -> dict[str, object]:
    base = build_registry_bridge()
    result = register_prop51_prop53_literature_statements(
        base, existing_prop51_prop53_candidates()
    )
    targets = {e.assertion_id for e in result.evidence}
    unchanged_original = all(
        r.status.value == "metadata_only" for r in base.records if r.assertion_id in targets
    )
    output = {
        "phase": "163 R4-R12",
        "status": "TYPED_SOURCE_UNVERIFIED",
        "registered_count": len(result.evidence),
        "counts_by_reference": {
            locator: len(keys) for locator, keys in COMPONENTS.items()
        },
        "proof_status": "PROOF_ANCESTRY_NOT_CHECKED",
        "proof_links_unchanged": result.snapshot.proof_links == base.proof_links,
        "base_metadata_unchanged": unchanged_original,
        "evidence": [
            {
                "assertion_id": e.assertion_id,
                "source_description": e.source_description,
                "verification_status": e.verification_status,
                "proof_status": e.proof_status,
            }
            for e in result.evidence
        ],
    }
    if len(result.evidence) != 8 or not output["proof_links_unchanged"] or not unchanged_original:
        raise RuntimeError("Proposition 5.1/5.3 registration audit failed")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "summary.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R12 — Proposition 5.1 / 5.3 の型付き登録",
        "", "状態: TYPED_SOURCE_UNVERIFIED（原典照合は未実施）", "",
        "| 文献 | 成分 | 登録 | 出典検証 | 証明木検証 |",
        "|---|---|---|---|---|",
    ]
    for entry in result.evidence:
        locator, component = entry.assertion_id.removeprefix("boundary:").rsplit(":", 1)
        lines.append(
            f"| {locator} | `{component}` | STRUCTURED | {entry.verification_status} | {entry.proof_status} |"
        )
    lines.extend([
        "", "生成元・型付き範囲は R4-R12 の検証で確認。",
        "Proposition 5.1 の高次部分は境界 metadata の n >= 3 を型付き宣言として保持。",
        "Proposition 5.3 の高次部分は n >= 5 を型付き宣言として保持。",
        "出典の数学的正しさや証明成立を示すものではありません。",
        "全体 pytest は実施していません。", "",
    ])
    (directory / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    output = run_audit(Path("phase163_r4_r12_output"))
    print(f"Phase 163 R4-R12: {output['status']} {output['registered_count']}")
    print("Saved phase163_r4_r12_output/report.md")
    print("Full pytest not run.")
```

## `run.ps1` — 全文

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'proof.py',
  'toda_rules.py',
  'toda_prop56_zero_bootstrap.py',
  'unified_statement_registry.py',
  'phase163_r4_registry_bridge.py',
  'tests\test_phase59_prop53_integration.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing required project file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r12_literature_registration.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r12_literature_registration.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r12_literature_registration.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r12_literature_registration.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r12_literature_registration.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 focused tests failed; audit skipped.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 typed literature registration audit failed.' }
Write-Host 'R4-R12 typed registration audit finished. Full suite not run.'
```
