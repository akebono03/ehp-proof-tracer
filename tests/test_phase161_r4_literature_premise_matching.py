from homotopy_groups import TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from phase161_r3_backward_goal_schema import expand_phase161_r3_goal
from phase161_r4_literature_premise_matching import (
    expand_phase161_r4_literature_goal,
    match_phase161_r4_existing_premises,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaDeltaInjectiveStatement, TodaHopfInvariantSurjectiveStatement


def _terminal_goals():
    root = TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
            target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        )
    )
    expansion = expand_phase161_r3_goal(root)
    return tuple(
        expand_phase161_r3_goal(
            expand_phase161_r3_goal(branch).subgoals[0]
        ).subgoals[0]
        for branch in expansion.subgoals
    )


def test_r4_terminal_plans_follow_actual_production_contracts():
    goals = _terminal_goals()
    assert isinstance(goals[0], TodaHopfInvariantSurjectiveStatement)
    assert isinstance(goals[1], TodaDeltaInjectiveStatement)
    plans = tuple(expand_phase161_r4_literature_goal(goal) for goal in goals)
    assert all(plan is not None for plan in plans)
    assert tuple(len(p.requirements) for p in plans) == (2, 1)
    for plan in plans:
        assert tuple(r.statement_type for r in plan.requirements) == tuple(
            p.statement_type for p in plan.inference_rule.premise_patterns
        )
        assert all(r.proof_rule is ProofRule.INFERENCE for r in plan.requirements)


def test_r4_matches_preexisting_proof_steps_without_creating_proof_steps():
    data = build_phase59_3_data()
    existing = tuple(data["premise_steps"])
    for goal in _terminal_goals():
        plan = expand_phase161_r4_literature_goal(goal)
        matches = match_phase161_r4_existing_premises(plan, existing)
        assert matches, f"No existing proof witness for {goal!r}"
        for match in matches:
            assert all(any(premise is step for step in existing) for premise in match.premises)
            assert plan.inference_rule.match_guard(match.premises, ())
            assert plan.inference_rule.conclusion_builder(match.premises) == goal


def test_r4_rejects_incorrect_equality_and_given_provenance():
    data = build_phase59_3_data()
    existing = tuple(data["premise_steps"])
    goal = _terminal_goals()[0]
    plan = expand_phase161_r4_literature_goal(goal)
    assert match_phase161_r4_existing_premises(plan, ()) == ()
    prop = next(s for s in existing if s.conclusion.__class__.__name__ == "TodaProp51FiniteDimensionalStatement")
    given_prop = ProofStep(conclusion=prop.conclusion, premises=(), rule=ProofRule.GIVEN)
    assert match_phase161_r4_existing_premises(plan, (given_prop,)) == ()
    wrong = ProofStep(
        conclusion=Relation(lhs="invalid", rhs="relation", relation_type=RelationType.EQUALITY),
        premises=(given_prop,),
        rule=ProofRule.INFERENCE,
    )
    assert match_phase161_r4_existing_premises(plan, (wrong, prop)) == ()


def test_r4_unrelated_goal_has_no_literature_plan():
    assert expand_phase161_r4_literature_goal("Hopf is surjective") is None
    other = TodaHopfInvariantSurjectiveStatement(
        map=_terminal_goals()[0].map.__class__(
            source_group=TodaPrimaryGroup(group_dimension=7, sphere_dimension=4),
            target_group=TodaPrimaryGroup(group_dimension=7, sphere_dimension=7),
        )
    )
    assert expand_phase161_r4_literature_goal(other) is None
