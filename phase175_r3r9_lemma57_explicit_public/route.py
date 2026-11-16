"""Public Group query route citing Lemma 5.7's explicit nu-prime clause.

Only the already registered pi_7^3 goal selects this routing module. All
mathematical rules for zero image, EHP exactness and Hopf lift remain the
shared generic rules. No direct goal GIVEN or specialized narrative is added.
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
from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
    expand_hopf_injective_from_zero_image,
    hopf_injectivity_from_zero_image_inputs,
)
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
from phase175_r3r6_lemma57_general.source import merge_isolated_cited_source
from phase175_r3r8r1_verified_prior_public.rule import (
    expand_verified_prior_hopf_lift,
    expand_verified_prior_zero_image,
)
from phase175_r3r9_lemma57_explicit_public.rule import (
    exact_lemma57_zero_image_goal,
    expand_cited_lemma57_explicit_zero,
)
from phase175_r3r9_lemma57_explicit_public.source import (
    ASSERTION_ID,
    TodaLemma57ExplicitNuPrimeZero,
    build_explicit_lemma57_source,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def public_cited_ehp_extensions(
    available: tuple[object, ...], *, proof_target: object = None, bridge: object = None,
):
    """Place the citation extraction before generic EHP and Hopf proposals."""
    if available.count(TodaLemma57ExplicitNuPrimeZero()) != 1:
        raise ValueError("R3R9_REQUIRES_EXACTLY_ONE_CITED_LEMMA57_CLAUSE")

    def expand(statement: object):
        options = []
        options.extend(expand_cited_lemma57_explicit_zero(statement, available))
        if isinstance(statement, ImageZeroStatement):
            suspension = statement.map
            if isinstance(suspension, TodaSuspensionMap):
                domain, codomain = suspension.source_group, suspension.target_group
                if (
                    isinstance(domain, TodaPrimaryGroup)
                    and isinstance(codomain, TodaPrimaryGroup)
                    and type(domain.group_dimension) is int
                    and type(domain.sphere_dimension) is int
                    and codomain == TodaPrimaryGroup(
                        domain.group_dimension + 1, domain.sphere_dimension + 1,
                    )
                ):
                    n = domain.sphere_dimension
                    k = domain.group_dimension - n
                    prior = exact_prior_database_result(n, k)
                    if isinstance(prior, Relation) and prior.relation_type is RelationType.EQUALITY:
                        if proof_target is not None and bridge is not None:
                            options.extend(expand_verified_prior_zero_image(
                                statement, prior,
                                proof_target=proof_target, bridge=bridge,
                            ))
                        options.extend(expand_zero_image_from_cyclic_generator(
                            statement, prior,
                        ))
        options.extend(expand_hopf_injective_from_zero_image(statement))
        lifts = expand_cited_hopf_lift(statement, available)
        if proof_target is not None and bridge is not None:
            for lift in lifts:
                if len(lift.subgoals) != 3:
                    continue
                options.extend(expand_verified_prior_hopf_lift(
                    statement, lift.subgoals[1], lift.subgoals[2],
                    proof_target=proof_target, bridge=bridge,
                ))
        options.extend(lifts)
        return tuple(options)

    return expand


def prepare_pi73_public_connection(
    *, bridge, goal, citing_assertion_id, prior_conclusions: tuple,
):
    """Select the published clause; retain the ordinary typed proof resolver."""
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be tuple")
    if (
        not isinstance(goal, Relation)
        or goal.relation_type is not RelationType.EQUALITY
        or goal.lhs != TodaPrimaryGroup(7, 3)
    ):
        return None
    candidates = registered_group_goal_candidates(bridge, n=3, k=4)
    if len(candidates) != 1 or candidates[0] != goal:
        return None
    exact_id = resolve_specialized_goal_citing_id(bridge, goal)
    if not isinstance(exact_id, str) or not exact_id:
        return None
    if citing_assertion_id is not None and citing_assertion_id != exact_id:
        return None
    if ASSERTION_ID in bridge.registry._assertions:
        return None

    root = Path(__file__).resolve().parents[1]
    supplemental = build_explicit_lemma57_source(root)
    augmented = merge_isolated_cited_source(bridge, supplemental)
    if (
        ASSERTION_ID not in augmented.registry._assertions
        or not precedes_citing_assertion(augmented, ASSERTION_ID, exact_id)
    ):
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
    if (
        available.count(TodaLemma57ExplicitNuPrimeZero()) != 1
        or goal in available
    ):
        return None

    prior = exact_prior_database_result(2, 4)
    if (
        not isinstance(prior, Relation)
        or prior.lhs != TodaPrimaryGroup(6, 2)
    ):
        return None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    zero = GeneratorImage(e, prior.rhs.generator, Zero())
    if (
        not exact_lemma57_zero_image_goal(zero)
        or len(expand_cited_lemma57_explicit_zero(zero, available)) != 1
    ):
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
    if len(expand_verified_prior_zero_image(
        hopf_inputs[0], prior, proof_target=goal, bridge=screened,
    )) != 1:
        return None

    from phase165_r52_r9_shared_math import shared_expansion_provider

    ordinary = shared_expansion_provider(
        screened, proof_target=goal, prior_conclusions=prior_conclusions,
    )
    extensions = public_cited_ehp_extensions(
        available, proof_target=goal, bridge=screened,
    )

    def provider(statement: object):
        # First successful, cited proof wins. No proof step is imported.
        return extensions(statement) + ordinary(statement)

    return augmented, exact_id, provider
