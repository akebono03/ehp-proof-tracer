from dataclasses import dataclass
import pytest

from phase165_r6_2_r4_seeded_goals import generate_seeded_backward_goals
from proof import InferenceRule, PatternVariable, PremisePattern, ProofRule, ProofStep


@dataclass(frozen=True)
class Term:
    symbol: object


def test_cited_anchor_binds_new_goal_without_certifying_it():
    x = PatternVariable("x")
    rule = InferenceRule(
        name="test generic two premises",
        conclusion_pattern=Term("target"),
        premise_patterns=(
            PremisePattern(statement_pattern=Term(x)),
            PremisePattern(statement_pattern=Term("unproved")),
        ),
    )
    anchor = ProofStep(conclusion=Term("known"), premises=(), rule=ProofRule.GIVEN)
    output = generate_seeded_backward_goals(Term("target"), (rule,), (anchor,))
    assert len(output) == 1
    assert output[0].subgoals == (Term("known"), Term("unproved"))


def test_missing_anchor_cannot_invent_variable():
    x = PatternVariable("x")
    rule = InferenceRule(
        name="unbound",
        conclusion_pattern=Term("target"),
        premise_patterns=(PremisePattern(statement_pattern=Term(x)),),
    )
    assert generate_seeded_backward_goals(Term("target"), (rule,), ()) == ()


def test_rejects_derived_step_as_cited_anchor():
    step = ProofStep(conclusion=Term("derived"), premises=(), rule=ProofRule.INFERENCE)
    with pytest.raises(TypeError):
        generate_seeded_backward_goals(Term("target"), (), (step,))


def test_budget_guard():
    x = PatternVariable("x")
    rule = InferenceRule(
        name="bounded", conclusion_pattern=Term("target"),
        premise_patterns=(PremisePattern(statement_pattern=Term(x)),),
    )
    anchors = tuple(
        ProofStep(conclusion=Term(i), premises=(), rule=ProofRule.GIVEN)
        for i in range(3)
    )
    with pytest.raises(ValueError, match="budget exceeded"):
        generate_seeded_backward_goals(Term("target"), (rule,), anchors, max_candidates=1)
