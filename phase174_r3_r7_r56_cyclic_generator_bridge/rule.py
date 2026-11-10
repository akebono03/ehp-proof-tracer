"""Shared cyclic-generator lifting and generator-image surjectivity in EHP.

The first rule separates the cyclic generator conclusion from the already
certified four-premise R37 Hopf argument. The second uses that conclusion and
an independently proved typed Hopf-Delta formula to establish surjectivity.
Neither rule creates a source leaf, trusts a database name as evidence, nor
special-cases a fixed group/stem. R37's original public rule is retained.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27TypedHopfDeltaStatement,
    typed_specialization,
)
from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
    upper_delta_surjectivity_inputs,
)
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


CYCLIC_RULE_NAME = "injective Hopf generated image lifts a free cyclic generator"
SURJECTIVE_RULE_NAME = "generator of Delta codomain is Delta image implies surjectivity"


def canonical_typed_delta_generator(
    witness: object,
) -> HomotopyElement | None:
    """Project a *typed* Delta(iota) witness to the existing DB goal notation.

    This is a canonical representation constructor, not a proof step. In
    particular, an arbitrary HomotopyElement whose printed name resembles
    Delta(iota) cannot supply the witness. The sourced R25 theorem and its
    independently verified prerequisites remain mandatory in the rules.
    """
    if type(witness) is not Prop27TypedHopfDeltaStatement:
        return None
    n = witness.n
    if type(n) is not int or n < 4 or n % 2 != 0:
        return None
    if witness != typed_specialization(n):
        return None
    delta = witness.delta
    target = delta.target_group
    if (type(delta) is not TodaDeltaMap
            or type(target) is not TodaPrimaryGroup
            or target.sphere_dimension != n
            or target.group_dimension != 2 * n - 1
            or witness.source_iota_dimension != 2 * n + 1):
        return None
    index = witness.source_iota_dimension
    return HomotopyElement(
        name=f"Δ(ι{index})",
        dimension=target.sphere_dimension,
        source=target.group_dimension,
        target=target.sphere_dimension,
        generator=GeneratorSymbol(family=rf"\Delta(\iota_{{{index}}})"),
    )


def cyclic_generator_inputs(goal: object) -> tuple[object, ...] | None:
    """Only the already checked R37 four-premise typed EHP geometry qualifies."""
    if (type(goal) is not Relation
            or goal.relation_type is not RelationType.EQUALITY
            or type(goal.lhs) is not TodaPrimaryGroup
            or type(goal.rhs) is not FreeCyclicGroup):
        return None
    target = goal.lhs
    n = target.sphere_dimension
    if type(n) is not int or n < 4 or n % 2:
        return None
    witness = typed_specialization(n)
    if (witness.delta.target_group != target
            or canonical_typed_delta_generator(witness) != goal.rhs.generator):
        return None
    required = upper_delta_surjectivity_inputs(MapSurjective(witness.delta))
    if (required is None or len(required) != 4 or required[3] != witness):
        return None
    return required


def cyclic_generator_rule(goal: Relation) -> InferenceRule:
    """H injective and im(H)=<H(g)> imply A=<g>, with four certified facts."""
    required = cyclic_generator_inputs(goal)
    if required is None:
        raise ValueError("not an exact typed cyclic-generator EHP goal")

    def guard(premises, bindings):
        return (
            len(premises) == 4
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and cyclic_generator_inputs(goal) == required
        )

    return InferenceRule(
        name=CYCLIC_RULE_NAME,
        description=(
            "For an injective H with im(H)=<2*iota> and an independently "
            "proved H(Delta(iota))=+/-2*iota, the typed Delta(iota) generates "
            "its source group. Every antecedent is an ordinary inferred "
            "ProofStep; a database generator label is never an axiom."
        ),
        premise_patterns=tuple(
            PremisePattern(
                statement_type=type(item),
                statement_pattern=item,
                proof_rule=ProofRule.INFERENCE,
            )
            for item in required
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_cyclic_generator_from_hopf(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Offer the proved-generator root for any matching even EHP dimension."""
    required = cyclic_generator_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(cyclic_generator_rule(goal), required),)


def delta_surjectivity_generator_inputs(
    goal: object,
) -> tuple[Relation, Prop27TypedHopfDeltaStatement] | None:
    """Separate cyclic target presentation from typed Delta(iota) provenance."""
    if type(goal) is not MapSurjective or type(goal.map) is not TodaDeltaMap:
        return None
    delta = goal.map
    if type(delta.target_group) is not TodaPrimaryGroup:
        return None
    n = delta.target_group.sphere_dimension
    if type(n) is not int or n < 4 or n % 2:
        return None
    witness = typed_specialization(n)
    generator = canonical_typed_delta_generator(witness)
    if generator is None or witness.delta != delta:
        return None
    return (
        Relation(delta.target_group, FreeCyclicGroup(generator), RelationType.EQUALITY),
        witness,
    )


def delta_surjectivity_from_generator_rule(goal: MapSurjective) -> InferenceRule:
    """A=<Delta(iota)> and sourced typed Delta(iota) imply Delta is onto.

    A prior DB result is allowed as a group premise only when the existing
    source-first search itself admits it; this function never admits a DB row.
    """
    required = delta_surjectivity_generator_inputs(goal)
    if required is None:
        raise ValueError("not an exact typed Delta cyclic surjectivity goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].rule is ProofRule.INFERENCE
            and tuple(step.conclusion for step in premises) == required
            and delta_surjectivity_generator_inputs(goal) == required
        )

    return InferenceRule(
        name=SURJECTIVE_RULE_NAME,
        description=(
            "An element written as the typed Delta of the canonical identity "
            "generates the target group; the proved typed Delta application "
            "witness therefore makes Delta surjective. An earlier admitted "
            "database presentation or an inferred cyclic group can be used."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[0],
            ),
            PremisePattern(
                statement_type=Prop27TypedHopfDeltaStatement,
                statement_pattern=required[1],
                proof_rule=ProofRule.INFERENCE,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_delta_surjectivity_from_generator(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Generic reverse candidate; no source, GIVEN or proof result is created."""
    required = delta_surjectivity_generator_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(delta_surjectivity_from_generator_rule(goal), required),)
