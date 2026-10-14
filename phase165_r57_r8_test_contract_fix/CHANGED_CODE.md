# 変更対象

- `phase165_r57_r8_general_specialization/test_phase165_r57_r8_general_specialization.py`（ファイル全体を置換、必要な import を全文含む）
- `phase165_r57_r8_test_contract_fix/install.py`（新規：`install()` 全体）
- `phase165_r57_r8_test_contract_fix/run.ps1`（新規）

本番コードは変更しない。以下は修正後のテストファイル全文。

```python
"""R57-R8 narrowly scoped mathematical typed specialization tests."""
from dataclasses import replace
from pathlib import Path

import pytest

from expression import GeneratorSymbol, HomotopyElement, ScalarSum, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r57_r8_eta_specialization import (
    _fixed_typed_relations,
    expand_registered_eta_specialization,
    specialize_eta_group_relation,
    specialized_eta_group_goal_candidates,
)
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import shared_expansion_provider
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _source():
    bridge = build_adopted_prop51_reference()
    sources = _fixed_typed_relations(bridge)
    assert len(sources) == 1
    return bridge, sources[0]


def test_specialization_is_generic_across_n3_n4_n5():
    _, source = _source()
    for n in (3, 4, 5):
        goal = specialize_eta_group_relation(source, n)
        assert goal.lhs == TodaPrimaryGroup(n+1,n)
        assert goal.rhs.order == 2
        assert goal.rhs.generator.generator == GeneratorSymbol(family="η",index=n)


def test_specialization_range_and_source_restrictions():
    _, source = _source()
    with pytest.raises(ValueError):
        specialize_eta_group_relation(source, 2)
    with pytest.raises(ValueError):
        specialize_eta_group_relation(source, True)
    with pytest.raises(ValueError):
        specialize_eta_group_relation(Relation(TodaPrimaryGroup(5,4),FiniteCyclicGroup(2,source.rhs.generator)),4)


def test_goal_selection_uses_only_fixed_typed_symbolic_claim():
    bridge, _ = _source()
    found = specialized_eta_group_goal_candidates(TodaPrimaryGroup(5,4),bridge)
    assert len(found) == 1
    assert found[0].lhs == TodaPrimaryGroup(5,4)
    assert specialized_eta_group_goal_candidates(TodaPrimaryGroup(6,3),bridge) == ()


def test_backward_expansion_creates_no_given_and_requires_cited_premise():
    _, source = _source()
    goal = specialize_eta_group_relation(source,4)
    assert expand_registered_eta_specialization(goal,()) == ()
    expansion, = expand_registered_eta_specialization(goal,(source,))
    assert expansion.subgoals == (source,)
    assert expansion.rule.name.startswith("Toda Proposition 5.1")
    assert not hasattr(expansion, "given_step")


def test_shared_provider_has_specialization_with_screened_reference():
    bridge, source = _source()
    goal = specialize_eta_group_relation(source,4)
    # Production build_shared_typed_bridge exposes only cited GIVEN components.
    # An unexpanded composite itself is not a Relation proof leaf.
    screened_components = expand_cited_given_components(bridge)
    expansions = shared_expansion_provider(screened_components)(goal)
    assert any(item.subgoals == (source,) for item in expansions)


def test_inference_rule_derives_only_from_typed_source_step():
    _, source = _source()
    goal = specialize_eta_group_relation(source, 4)
    expansion, = expand_registered_eta_specialization(goal, (source,))
    leaf = ProofStep(conclusion=source, premises=(), rule=ProofRule.GIVEN)
    matched = find_inference_matches_for_rule(expansion.rule, (leaf,))
    assert len(matched) == 1
    assert matched[0].premises == (leaf,)
    step = derive_inference_proof_step(matched[0])
    assert step.conclusion == goal
    assert step.premises == (leaf,)
    assert step.rule is ProofRule.INFERENCE

```
