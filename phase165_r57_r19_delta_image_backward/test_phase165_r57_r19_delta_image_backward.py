"""Focused R57-R19 mathematical and search integration checks."""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r57_r19_delta_image_backward import expand_registered_delta_image_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step
from toda_rules import TodaDeltaImageFreeCyclicStatement, TodaDeltaImageUpToSignStatement


def _case():
    source = TodaPrimaryGroup(5, 5)
    target = TodaPrimaryGroup(3, 2)
    delta = TodaDeltaMap(source, target)
    iota = HomotopyElement(name="ι_5", dimension=5,
                           generator=GeneratorSymbol(family="ι", index=5))
    eta = HomotopyElement(name="η₂", dimension=2, source=3, target=2,
                          generator=GeneratorSymbol(family="η", index=2))
    multiple = Multiple(coefficient=2, expression=eta)
    witness = TodaDeltaImageUpToSignStatement(map=delta, element=iota, positive_value=multiple)
    goal = TodaDeltaImageFreeCyclicStatement(map=delta, image_group=FreeCyclicGroup(multiple))
    group = Relation(source, FreeCyclicGroup(iota), relation_type=RelationType.EQUALITY)
    return goal, witness, group


def test_r19_reverse_requires_exact_cited_signed_delta():
    goal, witness, source = _case()
    expansion = expand_registered_delta_image_goal(goal, (witness,))
    assert len(expansion) == 1
    assert expansion[0].subgoals == (source, witness)


def test_r19_forward_rule_derives_exact_target_from_proved_premises():
    goal, witness, source = _case()
    expansion = expand_registered_delta_image_goal(goal, (witness,))[0]
    premises = (ProofStep(conclusion=source, premises=(), rule=ProofRule.GIVEN),
                ProofStep(conclusion=witness, premises=(), rule=ProofRule.GIVEN))
    matches = find_inference_matches_for_rule(expansion.rule, premises)
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.conclusion == goal
    assert step.rule is ProofRule.INFERENCE


def test_r19_no_signed_reference_no_expansion():
    goal, witness, source = _case()
    assert expand_registered_delta_image_goal(goal, ()) == ()
    assert expand_registered_delta_image_goal(goal, (source,)) == ()


def test_r19_ambiguous_signed_references_fail_closed():
    goal, witness, _ = _case()
    assert expand_registered_delta_image_goal(goal, (witness, witness)) == ()


def test_r19_unrelated_image_is_not_derived():
    goal, witness, _ = _case()
    wrong = TodaDeltaImageFreeCyclicStatement(goal.map, FreeCyclicGroup(witness.element))
    assert expand_registered_delta_image_goal(wrong, (witness,)) == ()


def test_r19_shared_provider_uses_only_registered_delta_witness():
    bridge = build_shared_typed_bridge()
    goal, witness, source = _case()
    available = tuple(link.step.conclusion for link in bridge.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    options = shared_expansion_provider(bridge, proof_target=goal)(goal)
    matches = tuple(option for option in options if getattr(option.rule, "name", "") == "free cyclic generator Delta image")
    if witness in available:
        assert len(matches) == 1
        assert matches[0].subgoals == (source, witness)
    else:
        assert matches == ()
