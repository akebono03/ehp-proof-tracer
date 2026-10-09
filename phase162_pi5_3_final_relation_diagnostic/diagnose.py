"""Read-only diagnostic of final Phase 162 inference conclusion."""
from dataclasses import fields, is_dataclass
from pprint import pformat

from phase161_r5_backward_proof_reconstruction import reconstruct_phase161_r5_goal
from phase162_pi5_3_backward_selection import (
    _canonical_goals,
    expand_phase162_pi5_3_group_goal,
)
from proof import apply_inference_match, find_inference_matches_for_rule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_pi5_3_eta3_squared import build_phase59_4_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data
from toda_rules import (
    toda_eta_family_definition_statement,
    toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
)
from proof import ProofRule, ProofStep


def diagnose():
    pi4_goal, goal, bridge_goal = _canonical_goals()
    expansion = expand_phase162_pi5_3_group_goal(goal)
    assert expansion is not None
    pi4_step = build_phase59_2_data()["result_steps"][0]
    leaves = build_phase59_3_data()["premise_steps"]
    suspension = reconstruct_phase161_r5_goal(expansion.subgoals[1], leaves).final_step
    definitions = tuple(
        ProofStep(
            conclusion=toda_eta_family_definition_statement(index),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for index in (3, 4)
    )
    bridge_matches = tuple(find_inference_matches_for_rule(
        toda_prop53_n3_eta_square_suspension_bridge_inference_rule(), definitions
    ))
    assert len(bridge_matches) == 1
    bridge = apply_inference_match(bridge_matches[0])
    premises = (pi4_step, suspension, bridge)
    matches = tuple(find_inference_matches_for_rule(expansion.inference_rule, premises))
    print("Transport matches:", len(matches))
    assert len(matches) == 1
    actual = apply_inference_match(matches[0]).conclusion
    print("Goal equals actual:", goal == actual)
    print("\nGOAL:\n", pformat(goal, width=110))
    print("\nACTUAL:\n", pformat(actual, width=110))
    if type(goal) is type(actual) and is_dataclass(goal):
        for fld in fields(goal):
            wanted = getattr(goal, fld.name)
            got = getattr(actual, fld.name)
            print(f"Field {fld.name}: equal={wanted == got}")
            if wanted != got:
                print("  goal:", pformat(wanted, width=110))
                print("  actual:", pformat(got, width=110))
    print("\nPremise comparison with Phase59 fixture:")
    historical = build_phase59_4_data()
    for label, current, old in zip(
        ("pi4", "suspension", "bridge"),
        premises,
        (historical["pi4_2_step"], historical["suspension_isomorphism_step"], historical["eta_square_step"]),
    ):
        print(f"  {label}: conclusion_equal={current.conclusion == old.conclusion}, rule_equal={current.rule == old.rule}")
    print("  Phase59 final equals goal:", historical["final_step"].conclusion == goal)
    return actual == goal


if __name__ == "__main__":
    diagnose()
