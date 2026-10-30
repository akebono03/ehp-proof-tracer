"""Bind a second cited Hopf codomain to its earlier general source.

Only typed proof *obligations* are changed in this scoped adapter. Neither
previously proved steps nor new GIVEN leaves are supplied to search.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2j_r2_cyclic_hopf_surjective.source import _valid_surjective_pair
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import walk_proof_ancestry
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def bind_cited_hopf_codomain(
    root: ProofStep, screened, citing: str, provider,
    *, expected_locator: str,
) -> tuple[object, SourceBoundGoal, str, MapSurjective]:
    """Require an INFERENCE cyclic group from one cited preceding fixed source.

    Match the genuine two-premise Hopf ancestry whose second premise is a
    literature GIVEN.  Reconstruct only its cyclic codomain from the exact
    source.  The existing surjectivity InferenceRule and its guard stay intact.
    """
    if (
        not isinstance(root, ProofStep)
        or root.rule is not ProofRule.INFERENCE
        or not callable(provider)
        or not isinstance(citing, str)
        or not citing
        or not isinstance(expected_locator, str)
        or not expected_locator
    ):
        raise ValueError("valid inferred root, provider, citation and locator required")
    candidates = []
    for step in walk_proof_ancestry(root):
        if not (
            step.rule is ProofRule.INFERENCE
            and isinstance(step.conclusion, MapSurjective)
            and isinstance(step.conclusion.map, TodaHopfInvariantMap)
            and step.inference_rule is not None
            and len(step.premises) == 2
        ):
            continue
        group_step, image_step = step.premises
        if not (
            group_step.rule is ProofRule.INFERENCE
            and len(group_step.premises) == 1
            and group_step.inference_rule is not None
            and group_step.premises[0].rule is ProofRule.GIVEN
            and not group_step.premises[0].premises
            and image_step.rule is ProofRule.GIVEN
            and not image_step.premises
            and isinstance(group_step.conclusion, Relation)
            and group_step.conclusion.relation_type is RelationType.EQUALITY
            and isinstance(group_step.conclusion.rhs, FiniteCyclicGroup)
            and group_step.conclusion.lhs == step.conclusion.map.target_group
            and isinstance(image_step.conclusion, Relation)
            and _valid_surjective_pair(
                step.conclusion, group_step.conclusion, image_step.conclusion,
            )
        ):
            continue
        candidates.append(step)
    if len(candidates) != 1:
        raise ValueError("one inferred cyclic-codomain/cited-image Hopf ancestor required")
    hopf = candidates[0]
    group_step, image_step = hopf.premises
    source = group_step.premises[0].conclusion
    eligible = []
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
            and assertion.content == step.conclusion
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == expected_locator
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            eligible.append(link)
    if len(eligible) != 1:
        raise ValueError("unique screened preceding source of cited Hopf codomain required")
    group_route = provider(group_step.conclusion)
    hopf_route = provider(hopf.conclusion)
    if (
        len(group_route) != 1
        or group_route[0].rule is not group_step.inference_rule
        or group_route[0].subgoals != (source,)
        or len(hopf_route) != 1
        or hopf_route[0].rule is not hopf.inference_rule
        or hopf_route[0].subgoals != (
            group_step.conclusion, image_step.conclusion,
        )
    ):
        raise ValueError("original scoped inferred route is not source-bindable")
    bound = SourceBoundGoal(group_step.conclusion, source)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if type(goal) is type(hopf.conclusion) and goal == hopf.conclusion:
            return (GoalExpansion(
                hopf.inference_rule,
                (bound, image_step.conclusion),
            ),)
        return provider(goal)

    return expand, bound, eligible[0].assertion_id, hopf.conclusion
