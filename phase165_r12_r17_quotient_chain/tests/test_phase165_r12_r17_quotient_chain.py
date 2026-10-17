"""Focused reusable quotient-inference checks; synthetic test inputs are not literature."""
from dataclasses import dataclass

from homotopy_groups import FiniteCyclicGroup
from map_property_rules import SurjectiveMapStatement
from phase165_r12_r2_quotient_rules import (
    CyclicStructureStatement,
    HomomorphismPresentationStatement,
    KernelMultipleStatement,
)
from phase165_r12_r17_quotient_chain import build_generic_quotient_chain
from proof import ProofRule, ProofStep, Relation, RelationType


@dataclass(frozen=True)
class Symbol:
    value: str


def _step(statement):
    return ProofStep(conclusion=statement, premises=(), rule=ProofRule.GIVEN)


def _premises():
    f, a, b, x, y = [Symbol(name) for name in ("f", "A", "B", "x", "y")]
    return (
        _step(HomomorphismPresentationStatement(f, a, b, x, y)),
        _step(KernelMultipleStatement(f, a, x, 2)),
        _step(SurjectiveMapStatement(f)),
        _step(CyclicStructureStatement(a, x, None)),
    )


def test_generic_chain_preserves_all_ancestor_proofs():
    inputs = _premises()
    result = build_generic_quotient_chain(*inputs)
    assert result.status == "DERIVED_NOT_PROVENANCE_CERTIFIED"
    assert result.proof.conclusion == Relation(
        inputs[0].conclusion.codomain,
        FiniteCyclicGroup(2, inputs[0].conclusion.target_generator),
        RelationType.EQUALITY,
    )
    assert all(step.rule is ProofRule.INFERENCE for step in result.intermediate_steps)
    assert result.intermediate_steps[0].premises == inputs[:3]
    assert result.intermediate_steps[1].premises == (result.intermediate_steps[0], inputs[3])
    assert result.proof.premises == (result.intermediate_steps[1],)


def test_mismatched_generator_fails_closed():
    items = list(_premises())
    k = items[1].conclusion
    items[1] = _step(KernelMultipleStatement(k.map, k.domain, Symbol("wrong"), 2))
    result = build_generic_quotient_chain(*items)
    assert result.status == "UNRESOLVED"
    assert result.proof is None


def test_finite_source_fails_closed():
    items = list(_premises())
    s = items[3].conclusion
    items[3] = _step(CyclicStructureStatement(s.group, s.generator, 4))
    result = build_generic_quotient_chain(*items)
    assert result.status == "UNRESOLVED"
    assert result.proof is None
