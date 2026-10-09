"""Phase 162 R4-B2: eta-family generator normalization with explicit premises.

The concrete Toda (4.5) transport must already have been derived. This
module neither changes repository roots nor generates narrative prose.
"""

from dataclasses import dataclass

from expression import IteratedSuspension, ScalarProduct, ScalarSum
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    run_inference_until_stable_with_history,
)
from toda_rules import (
    TodaEtaFamilyDefinitionStatement,
    toda_eta_family_definition_statement,
)
from toda_stable_concrete_transport_proof import (
    TodaStableConcreteTransportProof,
)


@dataclass(frozen=True)
class TodaStableEtaNormalizedProof:
    transport_proof: TodaStableConcreteTransportProof
    base_definition_step: ProofStep
    target_definition_step: ProofStep
    normalized_step: ProofStep


def toda_eta_concrete_generator_normalization_inference_rule():
    """Normalize only a concrete 1-stem suspension supported by eta definitions."""

    def guard(premises, bindings):
        transported = premises[0].conclusion
        base_definition = premises[1].conclusion
        target_definition = premises[2].conclusion
        if not isinstance(transported, Relation):
            return False
        if transported.relation_type != RelationType.EQUALITY:
            return False
        if not isinstance(transported.lhs, TodaPrimaryGroup):
            return False
        if not isinstance(transported.rhs, FiniteCyclicGroup):
            return False
        n = transported.lhs.sphere_dimension
        if isinstance(n, bool) or not isinstance(n, int) or n <= 3:
            return False
        if transported.lhs.group_dimension != n + 1:
            return False
        if base_definition.index != 3 or target_definition.index != n:
            return False
        if not isinstance(transported.rhs.generator, IteratedSuspension):
            return False
        generator = transported.rhs.generator
        if generator.expression != base_definition.element:
            return False
        if generator.exponent != ScalarSum(
            left=n, right=ScalarProduct(left=-1, right=3)
        ):
            return False
        if base_definition != toda_eta_family_definition_statement(3):
            return False
        if target_definition != toda_eta_family_definition_statement(n):
            return False
        return True

    def conclusion(premises):
        transported = premises[0].conclusion
        target_definition = premises[2].conclusion
        return Relation(
            lhs=transported.lhs,
            rhs=FiniteCyclicGroup(
                order=transported.rhs.order,
                generator=target_definition.element,
            ),
            relation_type=RelationType.EQUALITY,
        )

    return InferenceRule(
        name="Toda eta-family concrete transported-generator normalization",
        description=(
            "Use canonical eta-family definitions for eta_3 and eta_n "
            "to identify E^(n-3) eta_3 with eta_n after a concrete "
            "finite-cyclic Toda (4.5) transport."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=TodaEtaFamilyDefinitionStatement),
            PremisePattern(statement_type=TodaEtaFamilyDefinitionStatement),
        ),
        match_guard=guard,
        conclusion_builder=conclusion,
    )


def build_toda_stable_eta_normalized_proof(
    transport_proof: TodaStableConcreteTransportProof,
) -> TodaStableEtaNormalizedProof:
    """Derive a named eta generator from a concrete 1-stem transport proof."""
    if not isinstance(transport_proof, TodaStableConcreteTransportProof):
        raise TypeError("transport_proof must be a TodaStableConcreteTransportProof")
    n = transport_proof.target.sphere_dimension
    if isinstance(n, bool) or not isinstance(n, int) or n <= 3:
        raise ValueError("only concrete transported eta-family targets are supported")
    if transport_proof.target.group_dimension != n + 1:
        raise ValueError("only the eta-family 1-stem is supported")
    base_definition = ProofStep(
        conclusion=toda_eta_family_definition_statement(3),
        premises=(),
        rule=ProofRule.GIVEN,
    )
    target_definition = ProofStep(
        conclusion=toda_eta_family_definition_statement(n),
        premises=(),
        rule=ProofRule.GIVEN,
    )
    rule = toda_eta_concrete_generator_normalization_inference_rule()
    result = run_inference_until_stable_with_history(
        rule,
        (transport_proof.transported_step, base_definition, target_definition),
    )
    matches = tuple(
        step for step in result.steps
        if step.inference_rule is rule
        and step.premises == (
            transport_proof.transported_step, base_definition, target_definition
        )
    )
    if len(matches) != 1:
        raise ValueError("eta normalization could not be derived from the supplied premises")
    return TodaStableEtaNormalizedProof(
        transport_proof=transport_proof,
        base_definition_step=base_definition,
        target_definition_step=target_definition,
        normalized_step=matches[0],
    )
