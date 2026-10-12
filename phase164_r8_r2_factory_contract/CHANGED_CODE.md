# Phase 164 R8-R2 変更コード全文

新規追加位置: リポジトリ直下 `phase164_r8_proofstep_factory.py`。既存ファイルへの import 変更はありません。

```python
"""Phase 164 R8-R2: restricted entry points for ProofStep construction.

This module does not confer trust on GIVEN evidence. It leaves calculation,
exactness, and other domain-specific constructors unchanged until reviewed.
"""
from proof import (
    InferenceMatch,
    ProofRule,
    ProofStep,
    Relation,
    apply_inference_match,
    relation_proof_step,
)


def create_relation_proof_step(relation: Relation) -> ProofStep:
    """Create a relation through the existing checked constructor."""
    if not isinstance(relation, Relation):
        raise TypeError("relation must be a Relation")
    result = relation_proof_step(relation)
    if (type(result) is not ProofStep or result.rule is not ProofRule.RELATION
            or result.conclusion is not relation or result.premises != ()):
        raise ValueError("relation constructor contract changed")
    return result


def derive_inference_proof_step(match: InferenceMatch) -> ProofStep:
    """Derive using the existing inference matcher; never bypass its rules."""
    if not isinstance(match, InferenceMatch):
        raise TypeError("match must be an InferenceMatch")
    result = apply_inference_match(match)
    if (type(result) is not ProofStep or result.rule is not ProofRule.INFERENCE
            or result.inference_rule is not match.inference_rule
            or result.premises != match.premises):
        raise ValueError("inference constructor contract changed")
    return result


def retain_existing_proof_step(step: ProofStep) -> ProofStep:
    """Preserve the exact existing object for repository lookup and replay."""
    if not isinstance(step, ProofStep):
        raise TypeError("step must be a ProofStep")
    return step
```

新規テスト追加位置: `tests/test_phase164_r8_r2_factory_contract.py`。

```python
"""Focused R8-R2 contract tests; no production callers migrated yet."""
import pytest

from phase164_r8_proofstep_factory import (
    create_relation_proof_step,
    derive_inference_proof_step,
    retain_existing_proof_step,
)
from proof import InferenceMatch, InferenceRule, ProofRule, ProofStep, Relation


def test_relation_uses_existing_checked_constructor():
    relation = Relation(lhs="a", rhs="b")
    step = create_relation_proof_step(relation)
    assert type(step) is ProofStep
    assert step.conclusion is relation
    assert step.rule is ProofRule.RELATION
    assert step.premises == ()


def test_relation_rejects_wrong_input():
    with pytest.raises(TypeError, match="relation"):
        create_relation_proof_step("a=b")


def test_inference_uses_existing_rule_with_same_premise_objects():
    premise = ProofStep(conclusion="input", premises=(), rule=ProofRule.GIVEN)
    rule = InferenceRule(
        name="phase164_r8_r2_fixture",
        conclusion_builder=lambda premises: ("derived", premises[0].conclusion),
    )
    match = InferenceMatch(inference_rule=rule, premises=(premise,))
    step = derive_inference_proof_step(match)
    assert step.rule is ProofRule.INFERENCE
    assert step.inference_rule is rule
    assert step.premises == (premise,)
    assert step.premises[0] is premise
    assert step.conclusion == ("derived", "input")


def test_inference_rejects_unchecked_argument():
    with pytest.raises(TypeError, match="match"):
        derive_inference_proof_step(object())


def test_replay_preserves_identity():
    step = ProofStep(conclusion="existing", premises=(), rule=ProofRule.GIVEN)
    assert retain_existing_proof_step(step) is step


def test_replay_rejects_non_proof_step():
    with pytest.raises(TypeError, match="ProofStep"):
        retain_existing_proof_step(object())
```

変更一覧: 上記2ファイルの追加のみ。既存 API・Replay・ProofStep のクラス・推論処理は変更しません。

実行する pytest: `python -m pytest -q tests/test_phase164_r8_r2_factory_contract.py tests/test_phase161_r5_backward_proof_reconstruction.py`。

完了条件: 限定 pytest PASS。次の R8-R3 で使用箇所を段階的に移行します。Phase 164 終了までは全体 pytest は実施しません。
