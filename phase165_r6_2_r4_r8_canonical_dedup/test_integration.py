from dataclasses import dataclass

from proof import InferenceRule, ProofRule, ProofStep
from phase165_r6_2_r4_r8_dedup import (
    append_unique_verified_derivation,
    same_cited_scalar_specialization,
)
from expression import ScalarSymbol


@dataclass(frozen=True)
class TypedClaim:
    value: object


def _steps(source=None):
    # Use a typed symbolic source that can be instantiated by scalar substitution.
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from expression import GeneratorSymbol, HomotopyElement, ScalarSum
    from proof import Relation
    n = ScalarSymbol("n")
    symbolic = Relation(
        TodaPrimaryGroup(ScalarSum(n, 1), n),
        FiniteCyclicGroup(2, HomotopyElement(name="η_n", dimension=n,
            source=ScalarSum(n, 1), target=n, generator=GeneratorSymbol("η", n))),
    )
    concrete = Relation(
        TodaPrimaryGroup(4, 3),
        FiniteCyclicGroup(2, HomotopyElement(name="η_3", dimension=3,
            source=4, target=3, generator=GeneratorSymbol("η", 3))),
    )
    cited = ProofStep(conclusion=symbolic, premises=(), rule=ProofRule.GIVEN)
    a = ProofStep(conclusion=concrete, premises=(cited,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="Toda Proposition 5.1 generic higher-eta specialization"))
    b = ProofStep(conclusion=concrete, premises=(cited,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="generic cited typed scalar specialization"))
    return a, b


def test_duplicate_scalar_routes():
    a, b = _steps()
    assert same_cited_scalar_specialization(a, b)
    options = [a]
    append_unique_verified_derivation(options, b)
    assert options == [a]


def test_reversed_order():
    a, b = _steps()
    assert same_cited_scalar_specialization(b, a)


def test_distinct_cited_step_preserved():
    a, b = _steps()
    distinct = ProofStep(conclusion=b.premises[0].conclusion, premises=(), rule=ProofRule.GIVEN)
    b = ProofStep(conclusion=b.conclusion, premises=(distinct,), rule=ProofRule.INFERENCE,
        inference_rule=b.inference_rule)
    assert not same_cited_scalar_specialization(a, b)


def test_other_rules_not_collapsed():
    a, b = _steps()
    other = ProofStep(conclusion=b.conclusion, premises=b.premises, rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="different mathematical rule"))
    assert not same_cited_scalar_specialization(a, other)


def test_different_conclusion_not_collapsed():
    a, b = _steps()
    other = ProofStep(conclusion="unrelated", premises=b.premises, rule=ProofRule.INFERENCE,
        inference_rule=b.inference_rule)
    assert not same_cited_scalar_specialization(a, other)
