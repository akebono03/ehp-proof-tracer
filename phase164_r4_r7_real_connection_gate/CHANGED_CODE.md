# Phase 164 R4-R7 — 変更コード全文

## 変更対象

- 新規: `phase164_r4_r7_real_connection_gate.py`（プロジェクト直下に追加）。`ConnectionGateResult`、`_make_distinct_proof_context`、`_trusted_roots`、`audit_phase164_r4_r7_connection`、`audit_current`、`write_report`、`main` を新設。
- 新規: `tests/test_phase164_r4_r7_real_connection_gate.py`（tests/ に追加）。全テスト関数を以下に収録。
- 実行専用: `run.ps1`（ZIP 内）。既存ファイルは変更しない。

## 実行 pytest

`tests/test_phase164_r4_r7_real_connection_gate.py`, `tests/test_phase164_r4_r6_typed_binding.py`, `tests/test_phase164_r3_registry_search_connection.py`, `tests/test_phase164_r2_citation_eligibility.py`, `tests/test_phase161_r7_premise_provenance_validation.py`。

## 完了条件

実登録2件に対する R2 非許可を R3 が確実に拒否し、従来の7推論・4完全性証人は変更なく再構築される。利用可能位置を捏造せず、Source Archive 117主張を昇格しない。

## 次の Phase 境界

別文献を引用する場合の R2 外部引用ポリシーと、独立の検証証拠の扱いは R4-R8 で仕様化。R4-R7 で勝手に ALLOWED にしない。

## 新規 Python モジュール（import・全クラス・全関数）

```python
"""Phase 164 R4-R7: real typed-binding connection gate, without invented order.

The R2 checker presently models same-document order. This module records what
happens when the two actual R4-R6 bindings are presented for a distinct EHP
Proof Tracer proof. It deliberately does not mint a fake Toda citing position,
add independently verified IDs, change an R2 decision, or use a blocked leaf.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import reconstruct_phase161_r7_validated_goal
from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from phase164_r3_registry_search_connection import (
    RegisteredLiteraturePremise,
    reconstruct_phase164_r3_pi5_3,
)
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


_PROOF_ASSERTION_ID = "ehp-proof-tracer:pi5_3:isomorphism:goal"
_PROOF_REFERENCE_ID = "ehp-proof-tracer:pi5_3:local-proof"


@dataclass(frozen=True)
class ConnectionGateResult:
    status: str
    cited_assertion_ids: tuple[str, ...]
    citation_reasons: tuple[str, ...]
    accepted_assertion_ids: tuple[str, ...]
    r3_rejected: bool
    legacy_derived_step_count: int
    exactness_leaf_count: int
    verified_inferences: int
    external_citation_order_supported: bool


def _make_distinct_proof_context(bridge: RegistryBridgeResult) -> RegistryBridgeResult:
    """Copy source references and create a separate, unordered local proof goal.

    This copy is not a publication in Toda and is never represented as one.
    """
    registry = UnifiedStatementRegistry()
    original = bridge.registry
    for binding_record in bridge.records:
        if binding_record.assertion_id is None:
            raise ValueError("R4-R6 binding record missing assertion ID")
        assertion = original.assertion(binding_record.assertion_id)
        source_ref = original.reference(assertion.reference_id)
        try:
            registry.reference(source_ref.reference_id)
        except KeyError:
            registry.add_reference(source_ref)
        registry.add_assertion(assertion)
    registry.add_reference(LiteratureEntry(
        reference_id=_PROOF_REFERENCE_ID,
        kind=ReferenceKind.REMARK,
        locator="EHP Proof Tracer pi_5^3 local proof",
        source_id="EHP Proof Tracer (not Toda)",
        publication_position=None,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=_PROOF_ASSERTION_ID,
        reference_id=_PROOF_REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=phase161_r5_target_goal(),
        origin=AssertionOrigin.PROOF_INTERNAL,
        available_after_position=None,
    ))
    return RegistryBridgeResult(registry, bridge.records, bridge.proof_links)


def _trusted_roots(leaves: tuple[ProofStep, ...]) -> tuple[ProofStep, ...]:
    roots: dict[int, ProofStep] = {}
    seen: set[int] = set()

    def visit(step: ProofStep) -> None:
        marker = id(step)
        if marker in seen:
            return
        seen.add(marker)
        if step.rule is ProofRule.GIVEN:
            roots[marker] = step
        for parent in step.premises:
            visit(parent)

    for leaf in leaves:
        visit(leaf)
    return tuple(roots.values())


def audit_phase164_r4_r7_connection(
    crosswalk: dict,
    original_leaves: tuple[ProofStep, ...],
    *,
    user_confirmed_original: bool,
) -> ConnectionGateResult:
    """Exercise the real binding and fail-closed search boundary.

    In particular, `verified_assertion_ids` stays empty: source confirmation
    and typed checks are not a recorded independent citation authorization.
    """
    if len(original_leaves) != 6:
        raise ValueError("expected exactly six existing leaves")
    literature = tuple(
        step for step in original_leaves
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    exactness = tuple(
        step for step in original_leaves
        if step.rule is ProofRule.GIVEN
        and isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    if len(literature) != 2 or len(exactness) != 4:
        raise ValueError("two literature and four exactness witnesses required")
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, literature,
        user_confirmed_original=user_confirmed_original,
    )
    if len(registration.bindings) != 2 or registration.citation_eligible:
        raise ValueError("unexpected typed-binding authorization state")
    bridge = _make_distinct_proof_context(registration.bridge)
    premises = tuple(
        RegisteredLiteraturePremise(binding.assertion_id, binding.step)
        for binding in registration.bindings
    )
    for premise, binding in zip(premises, registration.bindings):
        if premise.step is not binding.step:
            raise ValueError("ProofStep identity not preserved")
        if bridge.registry.assertion(premise.assertion_id).content is not premise.step.conclusion:
            raise ValueError("typed content identity not preserved")
    decisions = tuple(
        assess_phase164_r2_citation(
            bridge, binding.assertion_id, _PROOF_ASSERTION_ID,
            verified_assertion_ids=(),
        )
        for binding in registration.bindings
    )
    if any(decision.usable for decision in decisions):
        raise ValueError("unreviewed citation unexpectedly allowed")
    roots = _trusted_roots(original_leaves)
    rejected = False
    try:
        reconstruct_phase164_r3_pi5_3(
            bridge, _PROOF_ASSERTION_ID, premises, exactness, roots,
            verified_assertion_ids=(),
        )
    except ValueError as error:
        if "citation not eligible" not in str(error):
            raise
        rejected = True
    if not rejected:
        raise ValueError("R3 failed to reject non-eligible citations")
    # Independent baseline only; NOT a registry-authorized reconstruction.
    baseline = reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), original_leaves, roots,
    )
    if len(baseline.reconstruction.derived_steps) != 7:
        raise ValueError("legacy seven-step reconstruction changed")
    return ConnectionGateResult(
        status="REAL_BINDINGS_SCREENED_R3_BLOCKED_EXTERNAL_CITATION_POLICY_PENDING",
        cited_assertion_ids=tuple(binding.assertion_id for binding in registration.bindings),
        citation_reasons=tuple(decision.reason for decision in decisions),
        accepted_assertion_ids=(),
        r3_rejected=rejected,
        legacy_derived_step_count=len(baseline.reconstruction.derived_steps),
        exactness_leaf_count=len(exactness),
        verified_inferences=baseline.provenance.verified_inferences,
        external_citation_order_supported=False,
    )


def audit_current(manifest: Path) -> dict:
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data

    crosswalk = audit_current_repository(manifest)
    leaves = build_phase59_3_data()["premise_steps"]
    result = audit_phase164_r4_r7_connection(
        crosswalk, leaves, user_confirmed_original=True,
    )
    return {
        "phase": "164 R4-R7",
        "status": result.status,
        "source_statement_count": 2,
        "typed_assertion_ids": list(result.cited_assertion_ids),
        "citation_reasons": list(result.citation_reasons),
        "accepted_assertion_ids": list(result.accepted_assertion_ids),
        "r2_allowed_count": 0,
        "r3_rejected": result.r3_rejected,
        "legacy_reconstruction_success": True,
        "legacy_derived_step_count": result.legacy_derived_step_count,
        "exactness_leaf_count": result.exactness_leaf_count,
        "legacy_provenance_verified_inferences": result.verified_inferences,
        "external_citation_order_supported": result.external_citation_order_supported,
        "user_original_confirmation_recorded": True,
        "availability_position_fabricated": False,
        "citation_eligible": False,
        "proof_search_connected": False,
        "production_modified": False,
        "source_archive_promoted": False,
        "full_pytest_run": False,
    }


def write_report(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 164 R4-R7 — 実 Typed Binding の接続ゲート監査", "",
        "- 判定: " + report["status"],
        "- 対象: Proposition 5.1 の4成分と (5.3) の Hopf 等式。",
        "- R2 判定理由: " + ", ".join(report["citation_reasons"]),
        "- R3 は許可されない2件を拒否した。",
        "- 既存証明は別経路で7推論・4完全性証人を再構築した。",
        "- この別経路の成功は Registry 経由の証明が成功したことを意味しない。",
        "- 既存 R2 は同一文献内の順序判定モデルであり、外部文献引用の別建てルールは未実装。",
        "- ユーザー原本確認は記録済みだが、検証済み ID と架空の文献掲載位置は作らない。",
        "- Production・Renderer・Phase 163 原本転記は変更なし。",
        "- 全体 pytest は Phase 164 の最後だけ実施。", "",
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

## 新規 pytest（import・全テスト）

```python
"""Phase 164 R4-R7 focused real typed citation gate tests."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r7_real_connection_gate import (
    _make_distinct_proof_context,
    audit_phase164_r4_r7_connection,
)
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from phase164_r3_registry_search_connection import RegisteredLiteraturePremise, reconstruct_phase164_r3_pi5_3
from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement


@pytest.fixture(scope="module")
def prepared():
    crosswalk = audit_current_repository(Path("phase163_r4_r94_output/manifest.json"))
    leaves = build_phase59_3_data()["premise_steps"]
    return crosswalk, leaves


def test_real_bindings_are_screened_and_not_auto_approved(prepared):
    result = audit_phase164_r4_r7_connection(*prepared, user_confirmed_original=True)
    assert result.r3_rejected is True
    assert len(result.cited_assertion_ids) == 2
    assert result.accepted_assertion_ids == ()
    assert result.citation_reasons == (
        "independent_verification_not_recorded",
        "independent_verification_not_recorded",
    )


def test_baseline_proof_remains_seven_steps_four_exactness(prepared):
    result = audit_phase164_r4_r7_connection(*prepared, user_confirmed_original=True)
    assert result.legacy_derived_step_count == 7
    assert result.exactness_leaf_count == 4
    assert result.verified_inferences >= 7
    assert result.external_citation_order_supported is False


def test_distinct_proof_reference_does_not_invent_toda_order(prepared):
    crosswalk, leaves = prepared
    literature = tuple(step for step in leaves if step.rule is ProofRule.INFERENCE)
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, literature, user_confirmed_original=True,
    )
    bridge = _make_distinct_proof_context(registration.bridge)
    citing = bridge.registry.assertion("ehp-proof-tracer:pi5_3:isomorphism:goal")
    destination = bridge.registry.reference(citing.reference_id)
    assert destination.publication_position is None
    assert destination.source_id != bridge.registry.reference(
        bridge.registry.assertion(registration.bindings[0].assertion_id).reference_id
    ).source_id
    for binding in registration.bindings:
        assert bridge.registry.assertion(binding.assertion_id).available_after_position is None
        decision = assess_phase164_r2_citation(
            bridge, binding.assertion_id, citing.assertion_id,
            verified_assertion_ids=(),
        )
        assert decision.usable is False


def test_missing_user_confirmation_rejected(prepared):
    with pytest.raises(ValueError, match="explicit user"):
        audit_phase164_r4_r7_connection(*prepared, user_confirmed_original=False)


def test_exactness_missing_is_rejected(prepared):
    crosswalk, leaves = prepared
    with pytest.raises(ValueError, match="six existing leaves"):
        audit_phase164_r4_r7_connection(crosswalk, leaves[:-1], user_confirmed_original=True)


def test_registry_search_never_returns_success_with_unapproved_ids(prepared):
    crosswalk, leaves = prepared
    literature = tuple(step for step in leaves if step.rule is ProofRule.INFERENCE)
    exactness = tuple(step for step in leaves if isinstance(step.conclusion, TodaProp42ExactnessStatement))
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, literature, user_confirmed_original=True,
    )
    bridge = _make_distinct_proof_context(registration.bridge)
    mapped = tuple(RegisteredLiteraturePremise(binding.assertion_id, binding.step)
                   for binding in registration.bindings)
    roots = {}
    seen = set()
    def walk(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        if step.rule is ProofRule.GIVEN:
            roots[id(step)] = step
        for parent in step.premises:
            walk(parent)
    for step in leaves:
        walk(step)
    with pytest.raises(ValueError, match="citation not eligible"):
        reconstruct_phase164_r3_pi5_3(
            bridge, "ehp-proof-tracer:pi5_3:isomorphism:goal",
            mapped, exactness, tuple(roots.values()), verified_assertion_ids=(),
        )


def test_tampered_source_identity_is_rejected(prepared):
    crosswalk, leaves = prepared
    bad = dict(crosswalk)
    bad["leaves"] = [dict(row) for row in crosswalk["leaves"]]
    bad["leaves"][1]["source_statement_id"] = "toda:tex:invalid"
    with pytest.raises(ValueError):
        audit_phase164_r4_r7_connection(bad, leaves, user_confirmed_original=True)

```
