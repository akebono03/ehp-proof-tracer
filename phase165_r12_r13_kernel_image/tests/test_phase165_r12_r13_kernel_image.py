"""Focused R12-R13 generic kernel inference, reference, and negative tests."""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import (
    FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r12_r13_kernel_image import (
    SuspensionKernelFreeCyclicStatement,
    build_concrete_kernel_provider,
    delta_image_and_exactness_imply_kernel_inference_rule,
    expand_concrete_suspension_kernel,
)
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
from phase165_r14_r26_prop42_typed import typed_delta_e_window
from phase165_r3_recursive_search import reconstruct_registered_goal, RegisteredGoalUnresolved
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaDeltaImageFreeCyclicStatement, TodaDeltaImageUpToSignStatement


def make_case():
    source = TodaPrimaryGroup(5, 5)
    middle = TodaPrimaryGroup(3, 2)
    target = TodaPrimaryGroup(4, 3)
    delta = TodaDeltaMap(source, middle)
    iota = HomotopyElement("ι_5", dimension=5, generator=GeneratorSymbol("ι", 5))
    eta = HomotopyElement("η₂", dimension=2, source=3, target=2, generator=GeneratorSymbol("η", 2))
    twice_eta = Multiple(coefficient=2, expression=eta)
    witness = TodaDeltaImageUpToSignStatement(map=delta, element=iota, positive_value=twice_eta)
    goal = SuspensionKernelFreeCyclicStatement(
        TodaSuspensionMap(middle, target), FreeCyclicGroup(twice_eta),
    )
    return goal, witness


def test_r13_generic_backward_binds_existing_signed_reference():
    goal, witness = make_case()
    expansion, = expand_concrete_suspension_kernel(goal, (witness,))
    image, exact = expansion.subgoals
    assert image == TodaDeltaImageFreeCyclicStatement(witness.map, goal.kernel_group)
    assert exact == EHPImageEqualsKernelStatement(typed_delta_e_window(2, 4).window)


def test_r13_forward_rule_creates_inference_not_given():
    goal, witness = make_case()
    expansion, = expand_concrete_suspension_kernel(goal, (witness,))
    premises = tuple(ProofStep(x, (), ProofRule.GIVEN) for x in expansion.subgoals)
    matches = find_inference_matches_for_rule(expansion.rule, premises)
    assert len(matches) == 1
    conclusion = derive_inference_proof_step(matches[0])
    assert conclusion.conclusion == goal
    assert conclusion.rule is ProofRule.INFERENCE
    assert len(conclusion.premises) == 2


def test_r13_missing_signed_reference_does_not_propose_kernel():
    goal, witness = make_case()
    assert expand_concrete_suspension_kernel(goal, ()) == ()
    assert expand_concrete_suspension_kernel(goal, (object(),)) == ()


def test_r13_wrong_generator_and_ambiguous_reference_are_rejected():
    goal, witness = make_case()
    wrong = SuspensionKernelFreeCyclicStatement(goal.map, FreeCyclicGroup(witness.element))
    assert expand_concrete_suspension_kernel(wrong, (witness,)) == ()
    assert expand_concrete_suspension_kernel(goal, (witness, witness)) == ()


def test_r13_wrong_suspension_degrees_are_rejected():
    goal, witness = make_case()
    bad = SuspensionKernelFreeCyclicStatement(
        TodaSuspensionMap(goal.map.source_group, TodaPrimaryGroup(4, 4)),
        goal.kernel_group,
    )
    assert expand_concrete_suspension_kernel(bad, (witness,)) == ()


def test_r13_screened_bridge_provider_never_invents_delta_witness():
    bridge = build_shared_typed_bridge()
    goal, witness = make_case()
    candidate = build_concrete_kernel_provider(bridge)(goal)
    relevant = [link.step.conclusion for link in bridge.proof_links
                if link.step is not None and link.step.rule is ProofRule.GIVEN]
    if witness in relevant:
        assert len(candidate) == 1
    else:
        assert candidate == ()


def test_r13_no_forged_proof_when_citation_screen_removes_delta():
    from phase163_r4_registry_bridge import RegistryBridgeResult
    bridge = build_shared_typed_bridge()
    empty = RegistryBridgeResult(bridge.registry, bridge.records, ())
    goal, witness = make_case()
    assert build_concrete_kernel_provider(empty)(goal) == ()
