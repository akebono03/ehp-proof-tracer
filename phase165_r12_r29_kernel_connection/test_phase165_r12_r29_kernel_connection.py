from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r29_kernel_connection import expand_kernel_multiple_from_suspension
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def _goal():
    source = TodaPrimaryGroup(3, 2)
    target = TodaPrimaryGroup(4, 3)
    eta = HomotopyElement("η₂", 2, 3, 2, GeneratorSymbol("η", 2))
    mapping = TodaSuspensionMap(source, target)
    return KernelMultipleStatement(mapping, source, eta, 2)


def test_r29_existing_kernel_rule_reconstructs_exact_goal():
    goal = _goal()
    options = expand_kernel_multiple_from_suspension(goal)
    assert len(options) == 1
    parent = options[0].subgoals[0]
    assert parent == SuspensionKernelFreeCyclicStatement(
        goal.map, FreeCyclicGroup(Multiple(2, goal.source_generator))
    )
    premise = ProofStep(parent, (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(options[0].rule, (premise,))
    assert len(matches) == 1
    proof = apply_inference_match(matches[0])
    assert proof.conclusion == goal
    assert proof.premises == (premise,)
    assert proof.rule is ProofRule.INFERENCE


def test_r29_bad_map_rejected():
    goal = _goal()
    wrong = KernelMultipleStatement(object(), goal.domain, goal.source_generator, 2)
    assert expand_kernel_multiple_from_suspension(wrong) == ()
    wrong_domain = KernelMultipleStatement(goal.map, TodaPrimaryGroup(5, 3), goal.source_generator, 2)
    assert expand_kernel_multiple_from_suspension(wrong_domain) == ()


def test_r29_not_reinterpreting_arbitrary_goal():
    assert expand_kernel_multiple_from_suspension(object()) == ()
    assert expand_kernel_multiple_from_suspension("kernel") == ()
