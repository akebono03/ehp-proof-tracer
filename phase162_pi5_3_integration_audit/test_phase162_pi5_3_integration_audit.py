"""Focused integration audit, not a general goal-only backward search."""
from expression import Composition, GeneratorSymbol, HomotopyElement, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase161_r5_backward_proof_reconstruction import (
    phase161_r5_target_goal,
    reconstruct_phase161_r5_goal,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data
from toda_rules import (
    toda_eta_family_definition_statement,
    toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
    toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule,
)


def _apply_exact(rule, premises, expected):
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, premises)
        if tuple(match.premises) == tuple(premises)
    )
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == expected
    return step


def test_phase162_pi5_3_group_result_uses_reconstructed_isomorphism():
    """Bridge Phase 161 R5 to existing Phase 59 rules without finished E step."""
    n3 = build_phase59_3_data()
    reconstructed = reconstruct_phase161_r5_goal(
        phase161_r5_target_goal(), n3["premise_steps"]
    )
    assert reconstructed.final_step is reconstructed.derived_steps[-1]
    assert all(
        reconstructed.final_step is not step
        for step in n3["result"].steps
    )

    pi4_2_step = build_phase59_2_data()["result_steps"][0]
    eta3 = HomotopyElement(
        name="η₃", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3)
    )
    eta4 = HomotopyElement(
        name="η₄", dimension=4, source=5, target=4,
        generator=GeneratorSymbol(family="η", index=4)
    )
    definitions = tuple(
        ProofStep(
            conclusion=toda_eta_family_definition_statement(index),
            premises=(), rule=ProofRule.GIVEN
        )
        for index in (3, 4)
    )
    bridge_goal = Relation(
        lhs=Suspension(
            expression=Composition(
                left=HomotopyElement(
                    name="η₂", dimension=2, source=3, target=2,
                    generator=GeneratorSymbol(family="η", index=2)
                ),
                right=eta3,
            )
        ),
        rhs=Composition(left=eta3, right=eta4),
        relation_type=RelationType.EQUALITY,
    )
    bridge = _apply_exact(
        toda_prop53_n3_eta_square_suspension_bridge_inference_rule(),
        definitions, bridge_goal
    )
    goal = Relation(
        lhs=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        rhs=FiniteCyclicGroup(
            order=2, generator=Composition(left=eta3, right=eta4)
        ),
        relation_type=RelationType.EQUALITY,
    )
    final = _apply_exact(
        toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule(),
        (pi4_2_step, reconstructed.final_step, bridge), goal
    )
    assert final.premises[1] is reconstructed.final_step
    assert final.conclusion == goal
