"""General, source-first Toda Proposition 4.4 inference proposals for n=4.

The domain is determined by typed input groups, proven predecessor order,
strict generator-image shapes, and the source theorem, not a list of stems.
Zero groups have no generator-image obligations. A missing or unknown image
fails closed. This module does NOT install a public search route or a renderer.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
    group_coordinates,
    verified_db_step,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase173_r4_r4_typed_generator_audit.audit import (
    _group_components,
    _map_components,
)
from phase173_r4_r6_alias_source_audit.audit import components_match_alias
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)


GENERAL_ROOT_NAME = "Toda Proposition 4.4 generic n=4 typed direct-sum transport"
HOPF_ROOT_NAME = "Toda Lemma 5.4 cited Hopf identity consequence"


def checked_general_inputs(goal: object) -> tuple[object, object] | None:
    """Read exactly two earlier registered DB priors and check target shape.

    This is a necessary *shape* check only, not a proof or a new GIVEN.
    It allows zero, finite cyclic, free cyclic, and direct-sum presentations.
    A family without a vetted symbolic image (e.g. epsilon) is rejected.
    """
    if group_coordinates(goal) is None:
        return None
    n, k = group_coordinates(goal)
    if n != 4 or type(k) is not int:
        return None
    dimension = n + k
    if dimension < 7:
        return None
    group = (
        goal.group if hasattr(goal, "group") else
        goal.lhs if isinstance(goal, Relation) and goal.relation_type is RelationType.EQUALITY
        else None
    )
    if group != TodaPrimaryGroup(dimension, 4):
        return None
    registered = exact_prior_database_result(4, k)
    if type(registered) is not type(goal) or registered != goal:
        return None
    first = exact_prior_database_result(3, k)
    second = exact_prior_database_result(7, dimension - 7)
    if first is None or second is None:
        return None
    if (admitted_db_step(first, proof_target=goal) is None
            or admitted_db_step(second, proof_target=goal) is None):
        return None
    mapped = _map_components(first, second)
    actual = _group_components(goal)
    if mapped is None or actual is None or not components_match_alias(mapped, actual):
        return None
    return first, second


def general_toda56_rule(
    goal: object, first: object, second: object, *, bridge: object = None,
) -> InferenceRule:
    """Create a typed root with separate literature, two DB, and Hopf premises.

    The source-screened proof engine must establish every leaf. A returned
    InferenceRule is not itself a completed proof.
    """
    if checked_general_inputs(goal) != (first, second):
        raise ValueError("The registered target and its two earlier typed priors must match")
    theorem = TodaProp44UniversalStatement()
    hopf = canonical_hopf_relation()
    expected = (theorem, first, second, hopf)

    def guard(premises, bindings):
        return (
            len(premises) == 4
            and tuple(step.conclusion for step in premises) == expected
            and premises[0].rule is ProofRule.GIVEN
            and verified_db_step(premises[1], proof_target=goal, bridge=bridge)
            and verified_db_step(premises[2], proof_target=goal, bridge=bridge)
            and premises[3].rule is ProofRule.INFERENCE
            and premises[3].inference_rule is not None
            and premises[3].inference_rule.name == HOPF_ROOT_NAME
            and len(premises[3].premises) == 1
            and premises[3].premises[0].rule is ProofRule.GIVEN
            and premises[3].premises[0].conclusion == TodaLemma54TypedSource()
            and checked_general_inputs(goal) == (first, second)
        )

    return InferenceRule(
        name=GENERAL_ROOT_NAME,
        description=(
            "Specialize Toda Proposition 4.4 using the independently derived "
            "Hopf identity H(nu_4)=iota_7 from Lemma 5.4. Transport the two "
            "separately admitted earlier DB groups along (alpha,beta) -> "
            "E(alpha) + nu_4 composed with beta. Require typed generator "
            "shapes and exact orders for all nonzero summands; the zero "
            "case has no generators. DB priors are adopted hypotheses, "
            "never independent literature proofs."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaProp44UniversalStatement,
                statement_pattern=theorem,
            ),
            PremisePattern(statement_type=type(first), statement_pattern=first),
            PremisePattern(statement_type=type(second), statement_pattern=second),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=hopf,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_general_toda56(
    statement: object, available: tuple[object, ...], *, proof_target: object,
    bridge: object = None,
) -> tuple[GoalExpansion, ...]:
    """Offer only an evidenced candidate root; never inject any GIVEN leaf.

    Source screening is the caller's job and must precede this call. Neither
    candidate roots nor these source tuples authorize a public Web completion.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a screened tuple of source conclusions")
    if statement != proof_target:
        return ()
    if sum(type(item) is TodaProp44UniversalStatement
           and item == TodaProp44UniversalStatement() for item in available) != 1:
        return ()
    if sum(type(item) is TodaLemma54TypedSource
           and item == TodaLemma54TypedSource() for item in available) != 1:
        return ()
    inputs = checked_general_inputs(statement)
    if inputs is None:
        return ()
    first, second = inputs
    return (GoalExpansion(
        general_toda56_rule(statement, first, second, bridge=bridge),
        (TodaProp44UniversalStatement(), first, second, canonical_hopf_relation()),
    ),)
