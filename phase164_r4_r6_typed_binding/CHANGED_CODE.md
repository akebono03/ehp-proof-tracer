# Phase 164 R4-R6 変更コード全文

変更対象: 新規 `phase164_r4_r6_typed_binding.py`（クラス `ConfirmedSourceBinding`, `TypedBindingRegistration`、関数 `register_phase164_r4_r6_typed_bindings`, `audit_current`, `write_report`, `main`。冒頭 import も全文）、新規 `tests/test_phase164_r4_r6_typed_binding.py`（各テスト関数と必要な import）、新規 `run.ps1`。新規クラス・関数はモジュール先頭の import の直後に追加。既存 API・クラス・関数は変更なし。

## モジュール全文

```python
"""Phase 164 R4-R6: limited typed bindings for two user-confirmed Toda references.

An explicit user confirmation applies to source transcription, not automatic
mathematical certification or publication-order availability. The two existing
INFERENCE witnesses remain unchanged. Nothing is installed into the global
production registry or submitted to proof search by this module.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path

from phase163_r3_registry_validation import audit_dependencies
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r3_independent_semantic_audit import assess_typed_clauses
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class ConfirmedSourceBinding:
    """Source-confirmed binding; never an R2 citation approval token."""

    assertion_id: str
    source_statement_id: str
    locator: str
    step: ProofStep
    coverage: str
    verification_basis: str


@dataclass(frozen=True)
class TypedBindingRegistration:
    bridge: RegistryBridgeResult
    bindings: tuple[ConfirmedSourceBinding, ...]
    user_source_confirmation_recorded: bool
    citation_eligible: bool = False
    proof_search_connected: bool = False


_TARGETS = (
    ("prop51_finite_dimensional", "Proposition 5.1", "toda:tex:ch5:0002",
     "toda:typed:ch5:prop5.1:finite_dimensional_subset", ReferenceKind.PROPOSITION,
     "Four typed components only; excludes stable (G_1;2) clause."),
    ("nu_prime_hopf", "(5.3)", "toda:tex:ch5:0005",
     "toda:typed:ch5:eq5.3:hopf", ReferenceKind.EQUATION,
     "H(nu-prime)=eta_5 only; excludes membership and twice-nu relation."),
)


def register_phase164_r4_r6_typed_bindings(
    crosswalk: dict,
    literature_leaves: tuple[ProofStep, ...],
    *,
    user_confirmed_original: bool,
) -> TypedBindingRegistration:
    """Build an isolated typed bridge after validating R4-R1 and R4-R3 contracts.

    Original confirmation is recorded as user attestation. A source text hash,
    typed shape, and recorded attestation cannot establish when a proposition
    became available in the original work or a new proof's citation context.
    """
    if type(user_confirmed_original) is not bool or not user_confirmed_original:
        raise ValueError("explicit user original-source confirmation required")
    if not isinstance(crosswalk, dict) or not isinstance(literature_leaves, tuple):
        raise TypeError("crosswalk dict and literature_leaves tuple required")
    if (crosswalk.get("source_manifest_verified") is not True
            or crosswalk.get("source_archive_proof_eligible_count") != 0
            or len(literature_leaves) != 2
            or any(type(s) is not ProofStep or s.rule is not ProofRule.INFERENCE
                   for s in literature_leaves)):
        raise ValueError("source manifest or existing literature leaf contract invalid")
    typed = assess_typed_clauses(crosswalk, literature_leaves)
    if (typed.get("typed_checks_passed") != 5
            or typed.get("citation_eligible") is not False
            or typed.get("typed_registry_binding_written") is not False):
        raise ValueError("R4-R3 contract changed")
    rows = crosswalk.get("leaves")
    if not isinstance(rows, list) or len(rows) != 2:
        raise ValueError("R4-R1 source rows missing")
    registry = UnifiedStatementRegistry()
    records = []
    links = []
    bindings = []
    for index, (name, locator, source_id, assertion_id, kind, coverage) in enumerate(_TARGETS):
        source = rows[index]
        if (source.get("legacy_name") != name
                or source.get("source_locator") != locator
                or source.get("source_statement_id") != source_id
                or source.get("source_identity_match") is not True
                or source.get("source_publication_position_scope") != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
            raise ValueError("source-to-leaf pairing mismatch: " + name)
        step = literature_leaves[index]
        reference_id = "toda:" + locator
        registry.add_reference(LiteratureEntry(
            reference_id=reference_id,
            kind=kind,
            locator=locator,
            source_id="Toda:1962:user-checked",
            publication_position=None,
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=reference_id,
            kind=AssertionKind.STATEMENT,
            content=step.conclusion,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope=coverage,
            component_position=None,
            available_after_position=None,
            dependencies=(),
        ))
        records.append(MigrationRecord(
            source="phase164_r4_r6_user_confirmed_typed",
            source_key=source_id,
            assertion_id=assertion_id,
            status=MigrationStatus.STRUCTURED,
            detail="Existing INFERENCE witness bound; external verification and availability remain distinct",
        ))
        links.append(ProofStepLink(assertion_id=assertion_id, step=step))
        bindings.append(ConfirmedSourceBinding(
            assertion_id=assertion_id,
            source_statement_id=source_id,
            locator=locator,
            step=step,
            coverage=coverage,
            verification_basis="user_confirmed_original_correspondence",
        ))
    bridge = RegistryBridgeResult(registry, tuple(records), tuple(links))
    if not audit_dependencies(registry).valid:
        raise ValueError("typed binding dependencies are invalid")
    return TypedBindingRegistration(
        bridge=bridge, bindings=tuple(bindings),
        user_source_confirmation_recorded=True,
    )


def audit_current(manifest_path: Path) -> dict:
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
    crosswalk = audit_current_repository(manifest_path)
    leaves = tuple(
        step for step in build_phase59_3_data()["premise_steps"]
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, leaves, user_confirmed_original=True,
    )
    return {
        "phase": "164 R4-R6",
        "mode": "ISOLATED_TYPED_BINDING_USER_SOURCE_CONFIRMATION",
        "status": "TWO_TYPED_BINDINGS_REGISTERED_CITATION_AVAILABILITY_PENDING",
        "typed_binding_count": len(registration.bindings),
        "source_statement_ids": [b.source_statement_id for b in registration.bindings],
        "typed_assertion_ids": [b.assertion_id for b in registration.bindings],
        "coverage": [b.coverage for b in registration.bindings],
        "user_original_confirmation_recorded": registration.user_source_confirmation_recorded,
        "independent_edition_check_claimed": False,
        "availability_position_established": False,
        "citation_eligible": registration.citation_eligible,
        "proof_search_connected": registration.proof_search_connected,
        "source_archive_promoted": False,
        "production_registry_modified": False,
        "full_pytest_run": False,
    }


def write_report(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 164 R4-R6 — 2件の型付き対応付け", "",
        "- 状態: " + report["status"],
        "- 型付き Assertion: 2件。元の ProofStep の INFERENCE 祖先は維持。",
        "- 原著対応: ユーザー確認済みとして記録（独立機械照合とは区別）。",
        "- Proposition 5.1: 既存4成分だけを登録。安定群の節は未収録。",
        "- (5.3): Hopf 等式だけを登録。他の節は未収録。",
        "- 文献掲載順・引用可能位置: 未確定。R2 による許可はまだ行わない。",
        "- 既存の全域 Registry・Proof Search・Renderer・Source Archive は変更しない。",
        "- 全体 pytest は Phase 164 の最終段階のみ。", "",
    ]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_current(args.manifest)
    write_report(report, args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

## テスト全文

```python
"""Phase 164 R4-R6 focused typed-binding tests."""
from dataclasses import replace

import pytest

from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from phase163_r3_registry_validation import audit_dependencies
from phase163_r4_registry_bridge import MigrationStatus
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from unified_statement_registry import AssertionOrigin


@pytest.fixture(scope="module")
def inputs():
    from pathlib import Path
    crosswalk = audit_current_repository(Path("phase163_r4_r94_output/manifest.json"))
    leaves = tuple(
        step for step in build_phase59_3_data()["premise_steps"]
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    return crosswalk, leaves


def test_registers_exact_two_typed_assertions(inputs):
    crosswalk, leaves = inputs
    result = register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    assert len(result.bindings) == 2
    assert len(result.bridge.records) == 2
    assert all(row.status is MigrationStatus.STRUCTURED for row in result.bridge.records)
    assert all(result.bridge.registry.assertion(b.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT for b in result.bindings)


def test_uses_original_leaf_identity_and_conclusion(inputs):
    crosswalk, leaves = inputs
    result = register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    for binding, leaf, link in zip(result.bindings, leaves, result.bridge.proof_links):
        assert binding.step is leaf
        assert link.step is leaf
        assert result.bridge.registry.assertion(binding.assertion_id).content is leaf.conclusion
        assert leaf.rule is ProofRule.INFERENCE


def test_explicit_source_confirmation_required(inputs):
    crosswalk, leaves = inputs
    with pytest.raises(ValueError, match="explicit user"):
        register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=False)


def test_tampered_manifest_pairing_rejected(inputs):
    crosswalk, leaves = inputs
    changed = dict(crosswalk)
    changed["leaves"] = [dict(row) for row in crosswalk["leaves"]]
    changed["leaves"][0]["source_statement_id"] = "toda:tex:ch5:incorrect"
    with pytest.raises(ValueError):
        register_phase164_r4_r6_typed_bindings(changed, leaves, user_confirmed_original=True)


def test_corrupted_math_rejected(inputs):
    crosswalk, leaves = inputs
    original = leaves[0].conclusion
    changed_delta = replace(original.delta_iota5_relation, positive_value=replace(original.delta_iota5_relation.positive_value, coefficient=3))
    changed_step = replace(leaves[0], conclusion=replace(original, delta_iota5_relation=changed_delta))
    with pytest.raises(ValueError, match="typed mathematical clause mismatch"):
        register_phase164_r4_r6_typed_bindings(crosswalk, (changed_step, leaves[1]), user_confirmed_original=True)


def test_no_availability_or_proof_search_promotion(inputs):
    crosswalk, leaves = inputs
    result = register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    assert result.citation_eligible is False
    assert result.proof_search_connected is False
    for binding in result.bindings:
        entry = result.bridge.registry.assertion(binding.assertion_id)
        ref = result.bridge.registry.reference(entry.reference_id)
        assert entry.available_after_position is None
        assert ref.publication_position is None
    assert audit_dependencies(result.bridge.registry).valid


def test_partial_statement_coverage_preserved(inputs):
    crosswalk, leaves = inputs
    result = register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    assert "excludes stable" in result.bindings[0].coverage
    assert "excludes membership" in result.bindings[1].coverage


def test_no_global_registry_mutation(inputs):
    from phase163_r4_registry_bridge import build_registry_bridge
    before = build_registry_bridge()
    before_count = len(before.records)
    crosswalk, leaves = inputs
    register_phase164_r4_r6_typed_bindings(crosswalk, leaves, user_confirmed_original=True)
    after = build_registry_bridge()
    assert len(after.records) == before_count
```

## 実行スクリプト全文

```powershell
$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project
$Required = @(
  'phase164_r4_r1_source_crosswalk.py',
  'phase164_r4_r2_semantic_structure.py',
  'phase164_r4_r3_independent_semantic_audit.py',
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r94_output\manifest.json',
  'tests\test_phase59_n3_ehp_chain.py'
)
foreach ($File in $Required) {
  if (-not (Test-Path (Join-Path $Project $File))) {
    throw "Missing prerequisite: $File"
  }
}
Copy-Item (Join-Path $PSScriptRoot 'phase164_r4_r6_typed_binding.py') (Join-Path $Project 'phase164_r4_r6_typed_binding.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r4_r6_typed_binding.py') (Join-Path $Project 'tests\test_phase164_r4_r6_typed_binding.py') -Force
python -B -m pytest -q `
  tests/test_phase164_r4_r6_typed_binding.py `
  tests/test_phase164_r4_r3_independent_semantic_audit.py `
  tests/test_phase164_r4_r2_semantic_structure.py `
  tests/test_phase163_r4_registry_bridge.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R6 targeted tests failed' }
python -B -m phase164_r4_r6_typed_binding `
  --manifest 'phase163_r4_r94_output/manifest.json' `
  --output 'phase164_r4_r6_output'
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R6 binding audit failed' }
Write-Output 'Phase 164 R4-R6 targeted typed bindings complete. Full pytest NOT run.'
```

## 完了条件と次の境界

2件の型付き主張、ユーザー原本確認記録、既存 ProofStep 同一性、必要な局所テストが通ること。R2 引用許可・実探索への接続・未収録部分の登録・原本掲載順の確定は今回行わない。全体 pytest は Phase 164 の最終工程に限る。
