"""Scope one Hopf codomain to its earlier cited general source.

Do not change the Hopf rule, accept an adopted DB leaf as a replacement for
its inferred group premise, or insert previously completed proof steps.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import (
    scoped_expansion_provider,
    walk_proof_ancestry,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def source_bound_hopf_provider(root: ProofStep, screened, citing: str,
                               hopf_goal: MapSurjective, fallback_provider):
    """Require cited *inference* for a Hopf codomain without altering other goals.

    `SourceBoundGoal` changes only the group's proof-search obligation.  The
    existing recursive engine then has to specialize the cited general theorem,
    instead of returning an independently eligible DB prior as a GIVEN.
    """
    if not (
        isinstance(hopf_goal, MapSurjective)
        and isinstance(hopf_goal.map, TodaHopfInvariantMap)
        and isinstance(citing, str)
        and citing
    ):
        raise ValueError("a typed Hopf surjectivity goal and citing ID are required")
    original = tuple(
        step for step in walk_proof_ancestry(root)
        if type(step.conclusion) is type(hopf_goal) and step.conclusion == hopf_goal
    )
    if len(original) != 1 or original[0].rule is not ProofRule.INFERENCE:
        raise ValueError("expected one inferred Hopf surjectivity ancestor")
    hopf = original[0]
    if len(hopf.premises) != 2 or hopf.inference_rule is None:
        raise ValueError("Hopf rule does not have two inferred antecedents")
    group_step, image_step = hopf.premises
    if not (
        group_step.rule is ProofRule.INFERENCE
        and image_step.rule is ProofRule.INFERENCE
        and len(group_step.premises) == 1
        and group_step.inference_rule is not None
        and isinstance(group_step.conclusion, Relation)
        and group_step.conclusion.relation_type is RelationType.EQUALITY
        and group_step.conclusion.lhs == hopf_goal.map.target_group
        and isinstance(group_step.conclusion.rhs, FiniteCyclicGroup)
        and group_step.premises[0].rule is ProofRule.GIVEN
        and not group_step.premises[0].premises
    ):
        raise ValueError("a cited, inferred cyclic codomain is required")
    source = group_step.premises[0].conclusion
    matching_links = []
    for link in screened.proof_links:
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and type(step.conclusion) is type(source)
            and step.conclusion == source
            and step.conclusion == assertion.content
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == "Proposition 5.3"
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            matching_links.append(link)
    if len(matching_links) != 1:
        raise ValueError("Hopf codomain lacks a unique preceding Proposition 5.3 source")

    bound = SourceBoundGoal(group_step.conclusion, source)
    ordinary_scoped = scoped_expansion_provider(root, fallback_provider)
    original_proposal = ordinary_scoped(hopf_goal)
    expected_subgoals = (group_step.conclusion, image_step.conclusion)
    if (
        len(original_proposal) != 1
        or original_proposal[0].rule is not hopf.inference_rule
        or original_proposal[0].subgoals != expected_subgoals
        or len(ordinary_scoped(group_step.conclusion)) != 1
        or ordinary_scoped(group_step.conclusion)[0].subgoals != (source,)
    ):
        raise ValueError("original R4-R8 Hopf derivation is not source-boundable")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if type(goal) is type(hopf_goal) and goal == hopf_goal:
            return (GoalExpansion(hopf.inference_rule, (bound, image_step.conclusion)),)
        return ordinary_scoped(goal)

    return expand, bound, matching_links[0].assertion_id
