"""Source-first, bounded Toda Proposition 4.4 proof proposals for pi_i^4, i=8..10.

The target is never a GIVEN or a publication-position assumption. All proposed
premises must be discharged by the existing backward search. Earlier sphere.csv
rows remain explicitly adopted DB priors, not independently proven literature.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
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


TARGET_DIMENSIONS = (8, 9, 10)


def checked_inputs(goal: object) -> tuple[object, object] | None:
    """Recognize only a DB-registered typed target and its two earlier inputs.

    A compatible decomposition is a prerequisite, NOT a proof of generator maps.
    The (eta_7, eta-subscript-7) name pair is checked by the existing strict
    eta alias inspector, never by a free-form name replacement.
    """
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and isinstance(goal.lhs, TodaPrimaryGroup)
        and goal.lhs.sphere_dimension == 4
        and type(goal.lhs.group_dimension) is int
        and goal.lhs.group_dimension in TARGET_DIMENSIONS
    ):
        return None
    dimension = goal.lhs.group_dimension
    registered = exact_prior_database_result(4, dimension - 4)
    if registered is None or registered != goal:
        return None
    first = exact_prior_database_result(3, dimension - 4)
    second = exact_prior_database_result(7, dimension - 7)
    if first is None or second is None:
        return None
    if (admitted_db_step(first, proof_target=goal) is None
            or admitted_db_step(second, proof_target=goal) is None):
        return None
    calculated = _map_components(first, second)
    stored = _group_components(goal)
    if not components_match_alias(calculated, stored):
        return None
    return (first, second)


def source_first_toda56_rule(
    goal: Relation, first: object, second: object, *, bridge: object = None,
) -> InferenceRule:
    """Build a guarded inference, not a direct assertion about the target group."""
    if checked_inputs(goal) != (first, second):
        raise ValueError("The target and two independently registered prior groups must match")
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
            and premises[3].inference_rule.name
                == "Toda Lemma 5.4 cited Hopf identity consequence"
            and len(premises[3].premises) == 1
            and premises[3].premises[0].rule is ProofRule.GIVEN
            and premises[3].premises[0].conclusion == TodaLemma54TypedSource()
            and checked_inputs(goal) == (first, second)
        )

    return InferenceRule(
        name="Toda Proposition 4.4 source-first n=4 typed direct-sum transport",
        description=(
            "Specialize the independently cited Proposition 4.4 with "
            "H(nu_4)=iota_7, inferred from a source-verified Lemma 5.4. "
            "Apply (alpha,beta) -> E(alpha)+nu_4 o beta to the two separately "
            "admitted earlier DB groups. Require exact generator family/index/" 
            "dimension correspondence, permitting only the vetted eta-name "
            "alias. This is a conditional proof using explicitly adopted "
            "database priors; it does not claim independent proofs of them."
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


def expand_source_first_toda56(
    statement: object, available: tuple[object, ...], *, proof_target: object,
    bridge: object = None,
) -> tuple[GoalExpansion, ...]:
    """Offer only the bounded (8,9,10)-dimensional root after screened sources."""
    if not isinstance(available, tuple):
        raise TypeError("available must be screened source conclusions")
    if statement != proof_target or not isinstance(statement, Relation):
        return ()
    if sum(type(x) is TodaProp44UniversalStatement for x in available) != 1:
        return ()
    if sum(type(x) is TodaLemma54TypedSource for x in available) != 1:
        return ()
    inputs = checked_inputs(statement)
    if inputs is None:
        return ()
    first, second = inputs
    return (GoalExpansion(
        source_first_toda56_rule(statement, first, second, bridge=bridge),
        (TodaProp44UniversalStatement(), first, second, canonical_hopf_relation()),
    ),)
