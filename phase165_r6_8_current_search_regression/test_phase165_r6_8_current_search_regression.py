"""R6-8: Current backward-search regression independent of retired Phase 50 probes."""
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from homotopy_groups import TodaPrimaryGroup
from proof import ProofRule, Relation, RelationType


def test_r6_8_current_pi4_3_uses_proven_conclusion():
    result = search_group_from_registered_goal(n=3, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert isinstance(result.conclusion, Relation)
    assert result.conclusion.relation_type is RelationType.EQUALITY
    assert result.conclusion.lhs == TodaPrimaryGroup(group_dimension=4, sphere_dimension=3)
    assert any(
        step.conclusion == result.conclusion and step.rule is ProofRule.INFERENCE
        for step in result.proven_steps
    )


def test_r6_8_current_pi3_2_uses_proven_conclusion():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert isinstance(result.conclusion, Relation)
    assert result.conclusion.relation_type is RelationType.EQUALITY
    assert result.conclusion.lhs == TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    assert any(
        step.conclusion == result.conclusion and step.rule is ProofRule.INFERENCE
        for step in result.proven_steps
    )
