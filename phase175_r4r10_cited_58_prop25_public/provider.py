"""Citation-backed backward proposals for Toda (5.8) and Proposition 2.5.

No group result, source, or ProofStep is created here. The common recursive
search must independently obtain the two cited GIVEN parents and the inferred
signed Delta and identity-composition parents before completing any result.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase175_r4r7_prop25_typed_composition.rule import (
    prop25_inputs,
    prop25_signed_composition_rule,
)
from phase175_r4r10_cited_58_prop25_public.source import (
    CitedToda58SignedDelta,
    CitedTodaProp25,
    canonical_toda58,
)
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import AssertionOrigin


SOURCE58_RULE = "read cited Toda (5.8) signed Delta image"
ETA_IDENTITY_RULE = "identity composition and cited eta suspension definition"
CITED_PROP25_RULE = "cited Toda Proposition 2.5 conditional composition"


def screened_cited_facts(bridge: RegistryBridgeResult) -> tuple[object, ...]:
    """Read only exact fixed-statement GIVEN links of the screened bridge."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    selected = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or link.step.premises or assertion.content != link.step.conclusion):
            continue
        if link.step.conclusion not in selected:
            selected.append(link.step.conclusion)
    return tuple(selected)


def expand_cited_toda58(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """A signed typed reading of one already-cited source claim."""
    if not isinstance(goal, TodaDeltaImageUpToSignStatement):
        return ()
    sources = tuple(
        claim for claim in available
        if type(claim) is CitedToda58SignedDelta
        and claim.locator == "(5.8)"
        and claim.statement == canonical_toda58()
        and claim.statement == goal
    )
    if len(sources) != 1:
        return ()
    source = sources[0]

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and not premises[0].premises
            and premises[0].conclusion == source
            and goal == canonical_toda58()
        )

    return (GoalExpansion(InferenceRule(
        name=SOURCE58_RULE,
        description="Translate the precisely cited (5.8) into its typed signed image; do not choose ±.",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=CitedToda58SignedDelta,
            statement_pattern=source,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    ), (source,)),)


def eta_identity_indices(goal: object) -> int | None:
    """Recognize iota_(n+2) o E^2(eta_n) = eta_(n+2) for n >= 2."""
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, Composition)
            or not isinstance(goal.lhs.left, HomotopyElement)
            or not isinstance(goal.lhs.right, IteratedSuspension)
            or type(goal.lhs.right.exponent) is not int
            or goal.lhs.right.exponent != 2
            or not isinstance(goal.lhs.right.expression, HomotopyElement)
            or not isinstance(goal.rhs, HomotopyElement)):
        return None
    alpha, beta, gamma = goal.lhs.left, goal.lhs.right.expression, goal.rhs
    n = beta.target
    if type(n) is not int or n < 2:
        return None
    if (alpha.source != n + 2 or alpha.target != n + 2
            or alpha.dimension != n + 2
            or alpha.generator != GeneratorSymbol("ι", index=n + 2)
            or beta.dimension != n or beta.source != n + 1 or beta.target != n
            or beta.generator != GeneratorSymbol("η", index=n)
            or gamma.dimension != n + 2
            or gamma.source != n + 3 or gamma.target != n + 2
            or gamma.generator != GeneratorSymbol("η", index=n + 2)):
        return None
    return n


def expand_eta_identity(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Derive the definitional identity from the cited universal eta notation."""
    if (eta_identity_indices(goal) is None
            or available.count(TodaEtaFamilyGeneralDefinition()) != 1):
        return ()
    definition = TodaEtaFamilyGeneralDefinition()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == definition
            and not premises[0].premises
            and eta_identity_indices(goal) is not None
        )

    return (GoalExpansion(InferenceRule(
        name=ETA_IDENTITY_RULE,
        description="Use cited eta_n=E^(n-2) eta_2 and the identity map, not a new theorem.",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaEtaFamilyGeneralDefinition,
            statement_pattern=definition,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    ), (definition,)),)


def expand_cited_prop25(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Use the *general* R4R7 rule with an independent Prop 2.5 citation."""
    if (not isinstance(goal, TodaDeltaImageUpToSignStatement)
            or not isinstance(goal.positive_value, Composition)):
        return ()
    props = tuple(x for x in available if type(x) is CitedTodaProp25
                  and x.locator == "Proposition 2.5")
    signed_sources = tuple(x for x in available if type(x) is CitedToda58SignedDelta
                           and x.locator == "(5.8)"
                           and x.statement == canonical_toda58())
    if len(props) != 1 or len(signed_sources) != 1:
        return ()
    source = signed_sources[0].statement
    beta = goal.positive_value.right
    identity = Relation(
        lhs=Composition(source.element, IteratedSuspension(beta, 2)),
        rhs=goal.element,
        relation_type=RelationType.EQUALITY,
    )
    if (prop25_inputs(goal, source, identity) != (source, identity)
            or eta_identity_indices(identity) is None):
        return ()
    # Preserve the existing R4R7 condition/guard and require a source citation.
    base = prop25_signed_composition_rule(goal, source, identity)
    prop = props[0]

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule is ProofRule.GIVEN
            and not premises[0].premises
            and premises[0].conclusion == prop
            and base.match_guard(premises[1:], ())
        )

    return (GoalExpansion(InferenceRule(
        name=CITED_PROP25_RULE,
        description="Cited Proposition 2.5, with R4R7 exact arithmetic guard and both proved inputs.",
        literature_reference=LiteratureReference(
            label="Toda Proposition 2.5", locator="Proposition 2.5",
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.GIVEN,
                           statement_type=CitedTodaProp25, statement_pattern=prop),
        ) + base.premise_patterns,
        match_guard=guard,
        conclusion_pattern=goal,
    ), (prop, source, identity)),)


def build_cited_58_prop25_provider(bridge: RegistryBridgeResult):
    """Only expose candidate expansions; all premises use ordinary proof search."""
    available = screened_cited_facts(bridge)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        return (
            expand_cited_toda58(goal, available)
            + expand_eta_identity(goal, available)
            + expand_cited_prop25(goal, available)
        )

    return expand
