from dataclasses import dataclass
import pytest
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep
from phase165_r6_2_r2_verified_inverse import reverse_rules_from_witnesses

@dataclass(frozen=True)
class Fact:
    value: int


def rule():
    return InferenceRule(
        name="generic addition from two typed premises",
        premise_patterns=(PremisePattern(statement_type=Fact), PremisePattern(statement_type=Fact)),
        conclusion_builder=lambda p: Fact(p[0].conclusion.value + p[1].conclusion.value),
    )


def test_unpatterned_conclusion_inverted_by_verified_witnesses():
    steps=(ProofStep(Fact(2),(),ProofRule.GIVEN),ProofStep(Fact(3),(),ProofRule.GIVEN))
    result=reverse_rules_from_witnesses(Fact(5),(rule(),),steps)
    assert result
    assert all(item.subgoals in ((Fact(2),Fact(3)),(Fact(3),Fact(2))) for item in result)


def test_unknown_goal_does_not_invent_premises():
    steps=(ProofStep(Fact(2),(),ProofRule.GIVEN),)
    assert reverse_rules_from_witnesses(Fact(5),(rule(),),steps)==()


def test_budget_fail_closed():
    steps=tuple(ProofStep(Fact(i),(),ProofRule.GIVEN) for i in range(8))
    with pytest.raises(ValueError,match="budget"):
        reverse_rules_from_witnesses(Fact(99),(rule(),),steps,max_combinations=32)


def test_invalid_input_fails_closed():
    with pytest.raises(TypeError):
        reverse_rules_from_witnesses(Fact(5),(object(),),())
    with pytest.raises(ValueError):
        reverse_rules_from_witnesses(Fact(5),(rule(),),(),max_combinations=0)
