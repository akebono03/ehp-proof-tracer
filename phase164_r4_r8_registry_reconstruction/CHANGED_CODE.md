# Phase 164 R4-R8 — 変更コード全文

## 変更対象

- 新規 `phase164_r4_r8_registry_reconstruction.py`
  - `RegistryBackedPi53Proof`（新規クラス）
  - `reconstruct_phase164_r4_r8_pi5_3`（新規関数）
  - `_known_trusted_roots`（既存テスト用の再現補助、新規関数）
  - `audit_current` / `write_report` / `main`（新規関数）
- 新規 `tests/test_phase164_r4_r8_registry_reconstruction.py`（10テスト）
- `run.ps1`（新規、局所テストのみ）

既存クラス・関数・import は変更しません。新規モジュールをルート直下に、新規テストを `tests/` に配置します。

## 実装コード（importを含む全文）

```python
"""Phase 164 R4-R8: reconstruct pi_5^3 using two registered fixed references.

This is an explicit fixed-literature citation path, separate from R2's
same-document publication-order checker. No order or verified ID is invented.
The cited propositions are supplied as user-confirmed sources, not re-proved.
Existing INFERENCE steps and trusted GIVEN roots retain their provenance.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    ValidatedBackwardReconstruction,
    reconstruct_phase161_r7_validated_goal,
    validate_phase161_r7_provenance,
)
from phase163_r3_registry_validation import audit_dependencies
from phase163_r4_registry_bridge import MigrationStatus
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from unified_statement_registry import AssertionOrigin


_EXPECTED_IDS = (
    "toda:typed:ch5:prop5.1:finite_dimensional_subset",
    "toda:typed:ch5:eq5.3:hopf",
)


@dataclass(frozen=True)
class RegistryBackedPi53Proof:
    validated: ValidatedBackwardReconstruction
    cited_assertion_ids: tuple[str, ...]
    used_source_ids: tuple[str, ...]
    exactness_leaf_count: int
    citation_mode: str = "confirmed_fixed_literature"


def reconstruct_phase164_r4_r8_pi5_3(
    crosswalk: dict,
    existing_leaves: tuple[ProofStep, ...],
    trusted_given_roots: tuple[ProofStep, ...],
    *,
    user_confirmed_original: bool,
) -> RegistryBackedPi53Proof:
    """Take *registered typed* premises through unchanged Phase 161 proof search.

    The fixed-literature path requires explicit source confirmation, exact
    registration and step identity, strict source coverage, and trusted proof
    ancestry. It does not claim a positive R2 same-document order decision.
    """
    if not isinstance(existing_leaves, tuple) or any(
        type(step) is not ProofStep for step in existing_leaves
    ):
        raise TypeError("existing_leaves must be a tuple of ProofStep")
    if not isinstance(trusted_given_roots, tuple) or any(
        type(step) is not ProofStep for step in trusted_given_roots
    ):
        raise TypeError("trusted_given_roots must be a tuple of ProofStep")
    if len(existing_leaves) != 6 or len({id(s) for s in existing_leaves}) != 6:
        raise ValueError("exactly six distinct existing proof leaves required")
    literature = tuple(
        step for step in existing_leaves
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    exactness = tuple(
        step for step in existing_leaves
        if step.rule is ProofRule.GIVEN
        and isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    if len(literature) != 2 or len(exactness) != 4:
        raise ValueError("two literature and four exactness witnesses required")
    if any(s.premises for s in exactness):
        raise ValueError("exactness witnesses must be premise-free")
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, literature, user_confirmed_original=user_confirmed_original,
    )
    if not registration.user_source_confirmation_recorded:
        raise ValueError("source confirmation was not recorded")
    if len(registration.bindings) != 2 or len(registration.bridge.proof_links) != 2:
        raise ValueError("two typed bindings and two proof links required")
    if not audit_dependencies(registration.bridge.registry).valid:
        raise ValueError("invalid registered dependencies")

    selected = []
    for index, expected_id in enumerate(_EXPECTED_IDS):
        binding = registration.bindings[index]
        link = registration.bridge.proof_links[index]
        record = registration.bridge.records[index]
        if (binding.assertion_id != expected_id
                or link.assertion_id != expected_id
                or record.assertion_id != expected_id
                or record.status is not MigrationStatus.STRUCTURED
                or binding.step is not literature[index]
                or link.step is not literature[index]):
            raise ValueError("unexpected or altered registered proof binding")
        assertion = registration.bridge.registry.assertion(expected_id)
        reference = registration.bridge.registry.reference(assertion.reference_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or assertion.content is not binding.step.conclusion
                or assertion.dependencies
                or reference.locator != binding.locator
                or reference.publication_position is not None
                or assertion.available_after_position is not None):
            raise ValueError("typed reference content or boundary changed")
        selected.append(link.step)

    # Existing R7 validates the very same concrete INFERENCE ancestry and
    # separately supplied GIVEN trust boundary, rather than inventing roots.
    validate_phase161_r7_provenance(tuple(selected) + exactness, trusted_given_roots)
    validated = reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), tuple(selected) + exactness,
        trusted_given_roots,
    )
    if len(validated.reconstruction.derived_steps) != 7:
        raise ValueError("expected seven production derivations")
    if validated.reconstruction.final_step.conclusion != phase161_r5_target_goal():
        raise ValueError("wrong reconstructed conclusion")
    if len(tuple(s for s in validated.reconstruction.leaf_steps
                 if isinstance(s.conclusion, TodaProp42ExactnessStatement))) != 4:
        raise ValueError("not all four exactness windows used")
    return RegistryBackedPi53Proof(
        validated=validated,
        cited_assertion_ids=tuple(_EXPECTED_IDS),
        used_source_ids=tuple(b.source_statement_id for b in registration.bindings),
        exactness_leaf_count=4,
    )


def _known_trusted_roots(steps: tuple[ProofStep, ...]) -> tuple[ProofStep, ...]:
    """Replay only: collect the established Phase 59 GIVEN objects for R7.

    Collecting a root does not independently certify its mathematical truth.
    Production callers must provide the reviewed roots explicitly.
    """
    found: dict[int, ProofStep] = {}
    seen: set[int] = set()

    def visit(step: ProofStep) -> None:
        identity = id(step)
        if identity in seen:
            return
        seen.add(identity)
        if step.rule is ProofRule.GIVEN:
            found[identity] = step
        for premise in step.premises:
            visit(premise)

    for step in steps:
        visit(step)
    return tuple(found.values())


def audit_current(manifest: Path) -> dict:
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data

    existing_leaves = build_phase59_3_data()["premise_steps"]
    crosswalk = audit_current_repository(manifest)
    validated = reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, existing_leaves, _known_trusted_roots(existing_leaves),
        user_confirmed_original=True,
    )
    from phase162_validated_proof_presentation import (
        build_validated_backward_proof_presentation,
        render_validated_backward_proof_markdown,
    )
    presentation = build_validated_backward_proof_presentation(validated.validated)
    narrative = render_validated_backward_proof_markdown(presentation)
    if not narrative or "## 証明" not in narrative or "□" not in narrative:
        raise ValueError("validated narrative missing proof or end marker")
    return {
        "phase": "164 R4-R8",
        "status": "REGISTERED_FIXED_LITERATURE_PI5_3_RECONSTRUCTED",
        "typed_assertion_ids": list(validated.cited_assertion_ids),
        "source_statement_ids": list(validated.used_source_ids),
        "registry_backed_reconstruction_success": True,
        "derived_step_count": len(validated.validated.reconstruction.derived_steps),
        "exactness_leaf_count": validated.exactness_leaf_count,
        "provenance_verified_inferences": validated.validated.provenance.verified_inferences,
        "narrative_rendered": True,
        "narrative": narrative,
        "citation_mode": validated.citation_mode,
        "r2_same_document_order_approval_claimed": False,
        "user_original_confirmation_recorded": True,
        "independent_edition_check_claimed": False,
        "source_archive_promoted": False,
        "production_modified": False,
        "full_pytest_run": False,
    }


def write_report(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    public = {key: value for key, value in report.items() if key != "narrative"}
    (output / "report.json").write_text(
        json.dumps(public, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (output / "proof.md").write_text(report["narrative"], encoding="utf-8")
    lines = [
        "# Phase 164 R4-R8 — 登録済み文献命題による証明再構築", "",
        "- 状態: " + report["status"],
        "- 登録済み Assertion: " + ", ".join(report["typed_assertion_ids"]),
        "- 既存の7推論・4つの完全性の証人から証明を再構築した。",
        "- Reference の出典確認はユーザー確認済みとして記録する。",
        "- R2 の同一文献内掲載順判定を通過したという主張はしない。",
        "- 原本転記117件の一括昇格・本番 Registry の変更はしない。",
        "- 原本版の機械照合、GIVEN の数学的真偽は独立認定しない。",
        "- 全体 pytest は Phase 終了時のみ。", "",
    ]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_current(args.manifest)
    write_report(report, args.output)
    print(json.dumps({k: v for k, v in report.items() if k != "narrative"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

## テストコード（importを含む全文）

```python
"""Phase 164 R4-R8: fixed literature references flow into actual reconstruction."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r8_registry_reconstruction import (
    _known_trusted_roots,
    reconstruct_phase164_r4_r8_pi5_3,
)
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement


@pytest.fixture(scope="module")
def inputs():
    crosswalk = audit_current_repository(Path("phase163_r4_r94_output/manifest.json"))
    leaves = build_phase59_3_data()["premise_steps"]
    roots = _known_trusted_roots(leaves)
    return crosswalk, leaves, roots


def test_actual_registered_two_statements_reconstruct_pi5_3(inputs):
    crosswalk, leaves, roots = inputs
    result = reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, leaves, roots, user_confirmed_original=True,
    )
    assert result.validated.reconstruction.final_step.conclusion == phase161_r5_target_goal()
    assert len(result.validated.reconstruction.derived_steps) == 7
    assert result.exactness_leaf_count == 4
    assert result.validated.provenance.verified_inferences >= 7


def test_registered_ids_are_real_and_limited(inputs):
    crosswalk, leaves, roots = inputs
    result = reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, leaves, roots, user_confirmed_original=True,
    )
    assert result.cited_assertion_ids == (
        "toda:typed:ch5:prop5.1:finite_dimensional_subset",
        "toda:typed:ch5:eq5.3:hopf",
    )
    assert result.used_source_ids == ("toda:tex:ch5:0002", "toda:tex:ch5:0005")
    assert result.citation_mode == "confirmed_fixed_literature"


def test_user_confirmation_cannot_be_omitted(inputs):
    crosswalk, leaves, roots = inputs
    with pytest.raises(ValueError, match="explicit user"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves, roots, user_confirmed_original=False,
        )


def test_missing_trusted_root_rejected(inputs):
    crosswalk, leaves, roots = inputs
    with pytest.raises(ValueError, match="Untrusted GIVEN"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves, roots[1:], user_confirmed_original=True,
        )


def test_mutated_prop51_claim_rejected(inputs):
    crosswalk, leaves, roots = inputs
    old = leaves[0].conclusion
    delta = old.delta_iota5_relation
    changed_delta = replace(
        delta, positive_value=replace(delta.positive_value, coefficient=3),
    )
    changed_step = replace(leaves[0], conclusion=replace(old, delta_iota5_relation=changed_delta))
    with pytest.raises(ValueError, match="typed mathematical clause mismatch"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, (changed_step,) + leaves[1:], roots,
            user_confirmed_original=True,
        )


def test_fake_source_statement_id_rejected(inputs):
    crosswalk, leaves, roots = inputs
    changed = dict(crosswalk)
    changed["leaves"] = [dict(row) for row in crosswalk["leaves"]]
    changed["leaves"][1]["source_statement_id"] = "toda:tex:ch5:fake"
    with pytest.raises(ValueError, match="pairing mismatch"):
        reconstruct_phase164_r4_r8_pi5_3(
            changed, leaves, roots, user_confirmed_original=True,
        )


def test_missing_exactness_witness_rejected(inputs):
    crosswalk, leaves, roots = inputs
    with pytest.raises(ValueError, match="six distinct"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves[:-1], roots, user_confirmed_original=True,
        )


def test_duplicate_leaf_identity_rejected(inputs):
    crosswalk, leaves, roots = inputs
    with pytest.raises(ValueError, match="six distinct"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves[:-1] + (leaves[0],), roots,
            user_confirmed_original=True,
        )


def test_trusted_root_clone_rejected(inputs):
    crosswalk, leaves, roots = inputs
    altered = (replace(roots[0]),) + roots[1:]
    with pytest.raises(ValueError, match="Untrusted GIVEN"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves, altered, user_confirmed_original=True,
        )


def test_original_leaf_rules_remain_unchanged(inputs):
    crosswalk, leaves, roots = inputs
    before = tuple(id(s) for s in leaves)
    reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, leaves, roots, user_confirmed_original=True,
    )
    assert tuple(id(s) for s in leaves) == before
    assert sum(s.rule is ProofRule.INFERENCE for s in leaves) == 2
    assert sum(s.rule is ProofRule.GIVEN and isinstance(s.conclusion, TodaProp42ExactnessStatement)
               for s in leaves) == 4
```

## PowerShell 実行コード全文

```powershell
$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project
$Required = @(
  'phase164_r4_r6_typed_binding.py',
  'phase164_r4_r3_independent_semantic_audit.py',
  'phase164_r4_r1_source_crosswalk.py',
  'phase161_r7_premise_provenance_validation.py',
  'phase162_validated_proof_presentation.py',
  'phase163_r4_r94_output\manifest.json',
  'tests\test_phase59_n3_ehp_chain.py'
)
foreach ($File in $Required) {
  if (-not (Test-Path (Join-Path $Project $File))) {
    throw "Missing prerequisite: $File"
  }
}
Copy-Item (Join-Path $PSScriptRoot 'phase164_r4_r8_registry_reconstruction.py') (Join-Path $Project 'phase164_r4_r8_registry_reconstruction.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r4_r8_registry_reconstruction.py') (Join-Path $Project 'tests\test_phase164_r4_r8_registry_reconstruction.py') -Force
python -B -m pytest -q `
  tests/test_phase164_r4_r8_registry_reconstruction.py `
  tests/test_phase164_r4_r6_typed_binding.py `
  tests/test_phase164_r4_r3_independent_semantic_audit.py `
  tests/test_phase161_r7_premise_provenance_validation.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R8 targeted tests failed' }
python -B -m phase164_r4_r8_registry_reconstruction `
  --manifest 'phase163_r4_r94_output/manifest.json' `
  --output 'phase164_r4_r8_output'
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R4-R8 reconstruction failed' }
Write-Output 'Phase 164 R4-R8 registry-backed pi5_3 reconstruction completed. Full pytest NOT run.'
```

## 完了条件と境界

- 登録した2件のAssertionを読み出し、元のProofStepオブジェクトとの一致を確認
- 7つの既存推論と4つの完全性の証人で `E: pi_4^2 -> pi_5^3` を再構築
- R7による推論祖先とユーザー指定のGIVEN信頼境界を検査
- 既存Rendererで `proof.md` を生成
- R2の同一文献内の掲載順判定を通過したとは主張しない
- 原著確認はユーザー確認として扱い、原本の独立機械照合とは区別
- Phase 163の未検証原文117件を一括許可しない
- 全体pytestはPhase 164終了時にのみ実行
