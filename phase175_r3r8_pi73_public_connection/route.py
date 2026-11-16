"""Attach the R3R7 source-backed general rules to ordinary Group query search.

Only the already registered (3,4) group selects this route. The inference
rules themselves are reusable, and all six premises remain independent
backward goals. No target conclusion or saved ProofStep is imported.
"""
from __future__ import annotations

from pathlib import Path

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    TodaLemma54TypedSource,
)
from phase174_r3_r6_r2_prop44_lemma54.source import attach_earlier_verified_lemma54
from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
    expand_hopf_injective_from_zero_image,
    hopf_injectivity_from_zero_image_inputs,
)
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
from phase175_r3r6_lemma57_general.rule import (
    expand_cited_lemma57_zero_generator,
    lemma57_criterion_inputs,
)
from phase175_r3r6_lemma57_general.source import (
    GENERAL_ASSERTION_ID,
    TodaLemma57GeneralCriterion,
    build_isolated_lemma57_source,
    merge_isolated_cited_source,
)
from phase175_r3r7_lemma54_membership.rule import (
    cited_lemma54_double_relation,
    expand_cited_lemma54_double,
    expand_even_factor_membership,
)
from phase175_r3r7_lemma54_membership.source import verify_lemma54_before_lemma57
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def public_cited_ehp_extensions(available: tuple[object, ...]):
    """Return reusable proposals using only the screened source conclusions.

    This closure does not carry a completed proof. Existing R3R7 algebraic
    inference rules are called unmodified. A lower group is only a candidate
    goal; the canonical resolver independently establishes its provenance.
    """
    if (available.count(TodaLemma54TypedSource()) != 1
            or available.count(TodaLemma57GeneralCriterion()) != 1):
        raise ValueError("R3R8 requires exactly one screened Lemma 5.4 and 5.7")
    equation = cited_lemma54_double_relation()

    def expand(statement: object):
        options = []
        options.extend(expand_cited_lemma54_double(statement, available))
        options.extend(expand_even_factor_membership(statement, (equation,)))
        options.extend(expand_cited_lemma57_zero_generator(statement, available))
        if isinstance(statement, ImageZeroStatement):
            suspension = statement.map
            if isinstance(suspension, TodaSuspensionMap):
                domain, codomain = suspension.source_group, suspension.target_group
                if (isinstance(domain, TodaPrimaryGroup)
                        and isinstance(codomain, TodaPrimaryGroup)
                        and type(domain.group_dimension) is int
                        and type(domain.sphere_dimension) is int
                        and codomain == TodaPrimaryGroup(
                            domain.group_dimension + 1,
                            domain.sphere_dimension + 1,
                        )):
                    n = domain.sphere_dimension
                    k = domain.group_dimension - n
                    prior = exact_prior_database_result(n, k)
                    if isinstance(prior, Relation) and prior.relation_type is RelationType.EQUALITY:
                        options.extend(expand_zero_image_from_cyclic_generator(
                            statement, prior,
                        ))
        options.extend(expand_hopf_injective_from_zero_image(statement))
        options.extend(expand_cited_hopf_lift(statement, available))
        return tuple(options)

    return expand


def prepare_pi73_public_connection(*, bridge, goal, citing_assertion_id,
                                   prior_conclusions: tuple):
    """Return (augmented bridge, real target citation ID, public provider).

    This mirrors the existing pi_7^4 public connection: the target alone
    chooses the *routing*, never the mathematical facts. Returning None is a
    safe refusal; the existing ordinary search is left untouched.
    """
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be tuple")
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or goal.lhs != TodaPrimaryGroup(7, 3)):
        return None
    candidates = registered_group_goal_candidates(bridge, n=3, k=4)
    if len(candidates) != 1 or candidates[0] != goal:
        return None
    exact_id = resolve_specialized_goal_citing_id(bridge, goal)
    if not isinstance(exact_id, str) or not exact_id:
        return None
    if citing_assertion_id is not None and citing_assertion_id != exact_id:
        return None
    if (ADOPTED_ASSERTION_ID in bridge.registry._assertions
            or GENERAL_ASSERTION_ID in bridge.registry._assertions):
        return None
    root = Path(__file__).resolve().parents[1]
    verify_lemma54_before_lemma57(root)
    earlier = attach_earlier_verified_lemma54(bridge, exact_id)
    extra = build_isolated_lemma57_source(root)
    augmented = merge_isolated_cited_source(earlier, extra)
    for assertion_id in (ADOPTED_ASSERTION_ID, GENERAL_ASSERTION_ID):
        if assertion_id not in augmented.registry._assertions:
            return None
        if not precedes_citing_assertion(augmented, assertion_id, exact_id):
            return None
    screened = prefer_universal_prop42_derivation(
        screen_shared_proof_context(
            augmented, goal=goal, citing_assertion_id=exact_id,
            explicit_publication_target=True,
        )
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    if (available.count(TodaLemma54TypedSource()) != 1
            or available.count(TodaLemma57GeneralCriterion()) != 1
            or goal in available):
        return None

    # Check the same independent, typed chain as R3R7 before making it public.
    prior = exact_prior_database_result(2, 4)
    if (not isinstance(prior, Relation)
            or prior.lhs != TodaPrimaryGroup(6, 2)):
        return None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    generator_image = GeneratorImage(e, prior.rhs.generator, Zero())
    inputs = lemma57_criterion_inputs(generator_image)
    if inputs is None:
        return None
    structure = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    lifts = expand_cited_hopf_lift(structure, available)
    if len(lifts) != 1 or lifts[0].subgoals[0] is None:
        return None
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(lifts[0].subgoals[0])
    if hopf_inputs is None or hopf_inputs[0] != ImageZeroStatement(e):
        return None
    if len(expand_zero_image_from_cyclic_generator(hopf_inputs[0], prior)) != 1:
        return None

    from phase165_r52_r9_shared_math import shared_expansion_provider

    ordinary = shared_expansion_provider(
        screened, proof_target=goal, prior_conclusions=prior_conclusions,
    )
    extensions = public_cited_ehp_extensions(available)

    def provider(statement: object):
        # Keep R3R7's first-successful proposal ordering. No step is injected.
        return extensions(statement) + ordinary(statement)

    return augmented, exact_id, provider
