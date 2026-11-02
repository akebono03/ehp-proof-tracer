"""Source-bound pi_7^4 decomposition: only a backward proposal, never a GIVEN.

The general Toda Proposition 4.4 source is a mandatory screened leaf.
The pi_6^3 prior must pass the published-prior source ordering rule.
The diagonal pi_7^7 relation and H(nu_4)=iota_7 must be independently
proved INFERENCE steps. A DB goal or candidate generator is not evidence.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, MapApplication
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r20_general_specialization import expand_cited_general_specialization
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import EHP_H_MAP


def _target_generators(goal: object) -> tuple[HomotopyElement, HomotopyElement] | None:
    """Match the exact current typed target; do not repair symbolic mismatches."""
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and goal.lhs == TodaPrimaryGroup(7, 4)
        and isinstance(goal.rhs, DirectSumGroup)
        and len(goal.rhs.summands) == 2
    ):
        return None
    free, torsion = goal.rhs.summands
    if not (
        isinstance(free, FreeCyclicGroup)
        and isinstance(torsion, FiniteCyclicGroup)
        and type(torsion.order) is int and torsion.order == 4
        and isinstance(free.generator, HomotopyElement)
        and isinstance(torsion.generator, IteratedSuspension)
        and type(torsion.generator.exponent) is int
        and torsion.generator.exponent == 1
        and isinstance(torsion.generator.expression, HomotopyElement)
    ):
        return None
    nu4 = free.generator
    prime = torsion.generator.expression
    if not (
        nu4.dimension == 4 and nu4.source == 7 and nu4.target == 4
        and isinstance(nu4.generator, GeneratorSymbol)
        and nu4.generator.family == "ν" and nu4.generator.index == 4
        and prime.dimension == 3 and prime.source == 6 and prime.target == 3
        and isinstance(prime.generator, GeneratorSymbol)
        and prime.generator.family in ("\\nu'", "ν")
        and (prime.generator.family == "\\nu'" or prime.generator.decoration == "′")
    ):
        return None
    return nu4, prime


def _diagonal_goal(bridge: object) -> Relation | None:
    """Require the independently registered pi_7^7 goal with its identity."""
    candidates = registered_group_goal_candidates(bridge, n=7, k=0)
    if len(candidates) != 1:
        return None
    relation = candidates[0]
    if not (
        isinstance(relation, Relation)
        and relation.relation_type is RelationType.EQUALITY
        and relation.lhs == TodaPrimaryGroup(7, 7)
        and isinstance(relation.rhs, FreeCyclicGroup)
        and isinstance(relation.rhs.generator, HomotopyElement)
    ):
        return None
    iota = relation.rhs.generator
    if not (
        isinstance(iota.generator, GeneratorSymbol)
        and iota.generator.family == "ι" and iota.generator.index == 7
        and iota.dimension == 7
    ):
        return None
    return relation


def source_bound_toda56_rule(
    goal: Relation, prior_relation: Relation, diagonal: Relation, hopf: Relation,
) -> InferenceRule:
    """Derive the exact presentation only after four proved typed premises."""
    generators = _target_generators(goal)
    if generators is None or not isinstance(prior_relation, Relation):
        raise ValueError("Exact pi_7^4 target and typed prior relation required")
    nu4, prime = generators
    expected_prior = Relation(
        TodaPrimaryGroup(6, 3), FiniteCyclicGroup(4, prime), RelationType.EQUALITY,
    )
    if prior_relation != expected_prior:
        raise ValueError("The pi_6^3 generator is not the target's suspended generator")
    if not (
        isinstance(diagonal, Relation)
        and diagonal.relation_type is RelationType.EQUALITY
        and diagonal.lhs == TodaPrimaryGroup(7, 7)
        and isinstance(diagonal.rhs, FreeCyclicGroup)
        and isinstance(diagonal.rhs.generator, HomotopyElement)
        and diagonal.rhs.generator.generator is not None
        and diagonal.rhs.generator.generator.family == "ι"
        and diagonal.rhs.generator.generator.index == 7
    ):
        raise ValueError("An independently typed diagonal generator is required")
    exact_hopf = Relation(
        MapApplication(map=EHP_H_MAP, expression=nu4),
        diagonal.rhs.generator,
        RelationType.EQUALITY,
    )
    if hopf != exact_hopf:
        raise ValueError("The independent n=4 Hopf-invariant premise differs")
    universal = TodaProp44UniversalStatement()
    expected = (universal, expected_prior, diagonal, exact_hopf)

    def guard(premises, bindings):
        return (
            len(premises) == 4
            and tuple(step.conclusion for step in premises) == expected
            and premises[0].rule is ProofRule.GIVEN
            and premises[2].rule is ProofRule.INFERENCE
            and premises[3].rule is ProofRule.INFERENCE
        )

    return InferenceRule(
        name="Toda (5.6) pi_7^4 source-bound direct-sum presentation",
        description=(
            "Specialize cited Toda Proposition 4.4 at n=4, i=7 using the "
            "independently proved Hopf invariant H(nu_4)=iota_7. Its map "
            "(alpha,beta) -> E(alpha)+nu_4 composed with beta sends "
            "nu-prime to E nu-prime and identity iota_7 to nu_4. "
            "Transport the independently proved pi_6^3 and pi_7^7 "
            "presentations along this isomorphism; no DB result is an axiom."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.GIVEN,
                           statement_type=TodaProp44UniversalStatement,
                           statement_pattern=universal),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=expected_prior),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=diagonal),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=exact_hopf),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_source_bound_toda56(
    goal: object, available: tuple[object, ...], bridge: object, *, proof_target: object,
) -> tuple[GoalExpansion, ...]:
    """Offer one sound root; proof search must discharge all four subgoals."""
    if not isinstance(available, tuple):
        raise TypeError("screened available claims must be a tuple")
    generators = _target_generators(goal)
    if generators is None or goal != proof_target:
        return ()
    if sum(type(x) is TodaProp44UniversalStatement and x == TodaProp44UniversalStatement()
           for x in available) != 1:
        return ()
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        return ()
    prior = resolve_prior_group_result(
        bridge, source_n=3, source_k=3, citing_assertion_id=citing_id,
    )
    if not prior.eligible or prior.relation is None:
        return ()
    diagonal = _diagonal_goal(bridge)
    if diagonal is None:
        return ()
    # A direct DB/adopted GIVEN for pi_7^7 does not satisfy this root's
    # independent INFERENCE premise. Bind the diagonal to the screened
    # universal Toda (5.1) scalar specialization instead.
    diagonal_routes = expand_cited_general_specialization(diagonal, available)
    if len(diagonal_routes) != 1 or len(diagonal_routes[0].subgoals) != 1:
        return ()
    diagonal_source = diagonal_routes[0].subgoals[0]
    source_links = tuple(
        link for link in bridge.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == diagonal_source
        and bridge.registry.reference(
            bridge.registry.assertion(link.assertion_id).reference_id
        ).locator == "(5.1)"
    )
    if len(source_links) != 1 or diagonal_source == diagonal:
        return ()
    nu4, _ = generators
    hopf = Relation(
        MapApplication(map=EHP_H_MAP, expression=nu4),
        diagonal.rhs.generator,
        RelationType.EQUALITY,
    )
    try:
        rule = source_bound_toda56_rule(goal, prior.relation, diagonal, hopf)
    except ValueError:
        return ()
    return (GoalExpansion(
        rule, (TodaProp44UniversalStatement(), prior.relation,
               SourceBoundGoal(diagonal, diagonal_source), hopf),
    ),)
