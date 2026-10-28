"""Shape-neutral Toda (4.5) transport with independently proved generator images.

No DB row, candidate generator identity or stable-range test creates a GIVEN.
The citation gate remains authoritative; unavailable source citations fail closed.
"""
from __future__ import annotations

from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaIteratedSuspensionMap,
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
    TodaSuspensionMap,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from phase169_r7_general_stable_transport.rule import _intermediate_typed_generator
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from unified_statement_registry import AssertionOrigin


def _goal_group(goal: object) -> TodaPrimaryGroup | None:
    if isinstance(goal, TodaPrimaryGroupZeroStatement):
        return goal.group if isinstance(goal.group, TodaPrimaryGroup) else None
    if (isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)):
        return goal.lhs
    return None


def _components(goal: object) -> tuple[object, ...] | None:
    """Return an ordered cyclic presentation, or () for an explicitly zero group.

    Direct-sum correspondence is position-preserving.  We do not infer a
    permutation or a change of basis from a DB presentation.
    """
    if isinstance(goal, TodaPrimaryGroupZeroStatement):
        return ()
    if not isinstance(goal, Relation):
        return None
    structure = goal.rhs
    if isinstance(structure, (FiniteCyclicGroup, FreeCyclicGroup)):
        return (structure,)
    if isinstance(structure, DirectSumGroup):
        if not structure.summands:
            return None
        if not all(isinstance(item, (FiniteCyclicGroup, FreeCyclicGroup))
                   for item in structure.summands):
            return None
        return tuple(structure.summands)
    return None


def _transport_shape(source: object, goal: object) -> tuple[int, int, int] | None:
    """Return (source sphere n, stem k, suspension count r) in Toda stable range."""
    left, right = _goal_group(source), _goal_group(goal)
    if left is None or right is None:
        return None
    if type(source) is not type(goal):
        return None
    values = (left.group_dimension, left.sphere_dimension,
              right.group_dimension, right.sphere_dimension)
    if not all(type(value) is int for value in values):
        return None
    q, n, p, m = values
    k, r = q - n, m - n
    if (k < 0 or n < 2 or n < k + 2 or r < 1
            or p - q != r):
        return None
    return n, k, r


def generator_images_for_group_transport(
    source: object, goal: object,
) -> tuple[GeneratorImage, ...] | None:
    """Build typed image *obligations* for any supported group presentation.

    Zero groups have no generator obligations.  For an ordered direct sum,
    every component must independently preserve cyclic type and order.
    """
    dimensions = _transport_shape(source, goal)
    left_components = _components(source)
    right_components = _components(goal)
    if (dimensions is None or left_components is None or right_components is None
            or len(left_components) != len(right_components)):
        return None
    n, k, r = dimensions
    if not left_components:
        return ()
    images = []
    for left, right in zip(left_components, right_components):
        if type(left) is not type(right):
            return None
        if (isinstance(left, FiniteCyclicGroup)
                and (type(left.order) is not int or left.order < 2
                     or left.order != right.order)):
            return None
        candidates = tuple(
            _intermediate_typed_generator(left.generator, right.generator, i, r)
            for i in range(r + 1)
        )
        if any(value is None for value in candidates):
            return None
        for i in range(r):
            images.append(GeneratorImage(
                map=TodaSuspensionMap(
                    TodaPrimaryGroup(n + k + i, n + i),
                    TodaPrimaryGroup(n + k + i + 1, n + i + 1),
                ),
                source_generator=candidates[i],
                target_generator=candidates[i + 1],
            ))
    return tuple(images)


def general_group_transport_rule(goal: object, source: object) -> InferenceRule:
    """One typed group-structure rule: source, cited isomorphism, proved images."""
    shape = _transport_shape(source, goal)
    images = generator_images_for_group_transport(source, goal)
    if shape is None or images is None:
        raise ValueError("source/target stable structures cannot be transported")
    n, k, r = shape
    source_group = TodaPrimaryGroup(n + k, n)
    target_group = TodaPrimaryGroup(n + k + r, n + r)
    iso = Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
        exponent=r, source_group=source_group, target_group=target_group,
    ))
    expected = (source, iso) + images

    def guard(premises, bindings):
        return (len(premises) == len(expected)
                and tuple(item.conclusion for item in premises) == expected
                and all(item.rule is ProofRule.INFERENCE for item in premises[1:])
                and generator_images_for_group_transport(source, goal) == images)

    return InferenceRule(
        name="typed arbitrary-fold stable transport of group structure",
        description=(
            "Transfer a cited source presentation along a proved Toda (4.5) "
            "isomorphism, discharging each generator image independently. "
            "An empty tuple of images is valid only for a typed zero group."
        ),
        premise_patterns=(
            PremisePattern(statement_type=type(source), statement_pattern=source),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Toda45IsomorphismStatement,
                           statement_pattern=iso),
        ) + tuple(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=GeneratorImage,
                           statement_pattern=image)
            for image in images
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def _zero_citing_assertion_id(bridge: RegistryBridgeResult, goal: object) -> str | None:
    """Zero targets require one independently positioned, exactly typed source."""
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        return None
    matches = []
    for assertion in bridge.registry._assertions.values():
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and assertion.content == goal
                and assertion.component_position is not None
                and bridge.registry.reference(assertion.reference_id).publication_position is not None):
            matches.append(assertion.assertion_id)
    return matches[0] if len(matches) == 1 else None


def _prior_zero_goal(
    bridge: RegistryBridgeResult, *, source_n: int, stem: int, citing_id: str,
) -> TodaPrimaryGroupZeroStatement | None:
    """Find an *earlier cited* zero assertion, not merely a zero DB row."""
    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
    from phase166_r3c_publication_order import precedes_citing_assertion

    candidates = database_zero_group_goal_candidates(n=source_n, k=stem)
    if len(candidates) != 1:
        return None
    source = candidates[0]
    eligible = tuple(
        assertion for assertion in bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT
        and assertion.content == source
        and precedes_citing_assertion(bridge, assertion.assertion_id, citing_id)
    )
    if len(eligible) != 1:
        return None
    return source


def expand_prior_general_group_transport(
    goal: object,
    available: tuple[object, ...],
    bridge: RegistryBridgeResult,
    *,
    proof_target: object,
) -> tuple[GoalExpansion, ...]:
    """Transport a screened earlier result, with or without a cited root target.

    If the goal has its own positioned citing assertion, publication precedence
    is mandatory and the established R7 finite-cyclic behavior is preserved.
    A DB-only goal has no fictional publication position: only uniquely
    screened, independently positioned prior FIXED statements can serve as
    source premises. A same-group source is never accepted.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("typed source bridge required")
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if goal != proof_target or _goal_group(goal) is None:
        return ()
    group = _goal_group(goal)
    if not all(type(x) is int for x in (group.group_dimension, group.sphere_dimension)):
        return ()
    n = group.sphere_dimension
    k = group.group_dimension - n
    if k < 0 or n <= k + 2 or _components(goal) is None:
        return ()
    # R10EG: established eta-specific 1-stem derivations must not compete
    # with the newer arbitrary-fold general transport at the same root.
    # This is a proposal-selection restriction, not a mathematical fact.
    if (k == 1 and isinstance(goal, Relation)
            and isinstance(goal.rhs, FiniteCyclicGroup)
            and goal.rhs.order == 2):
        from phase165_r12_r28_presentation_connection import _matching_eta_name
        from toda_rules import toda_eta_family_definition_statement
        eta = toda_eta_family_definition_statement(n).element
        if _matching_eta_name(goal.rhs.generator, eta):
            return ()
    citing_id = (
        _zero_citing_assertion_id(bridge, goal)
        if isinstance(goal, TodaPrimaryGroupZeroStatement)
        else resolve_specialized_goal_citing_id(bridge, goal)
    )
    if isinstance(goal, Relation) and isinstance(goal.rhs, FiniteCyclicGroup):
        from phase169_r7_general_stable_transport.rule import (
            expand_prior_general_stable_transport,
        )
        legacy = expand_prior_general_stable_transport(
            goal, available, bridge, proof_target=proof_target,
        )
        if legacy:
            return legacy

    for source_n in range(k + 2, n):
        if citing_id is None:
            from phase169_r10e2_unpositioned_citation.source_first import (
                uniquely_screened_prior_sources,
            )
            found = uniquely_screened_prior_sources(
                bridge, goal=goal, source_n=source_n,
            )
            source = found[0] if len(found) == 1 else None
        elif isinstance(goal, TodaPrimaryGroupZeroStatement):
            source = _prior_zero_goal(
                bridge, source_n=source_n, stem=k, citing_id=citing_id,
            )
        else:
            prior = resolve_prior_group_result(
                bridge, source_n=source_n, source_k=k,
                citing_assertion_id=citing_id,
            )
            source = prior.relation if prior.eligible else None
        if source is None:
            # The root may cite no proposition. Adopt an explicitly
            # stored earlier DB structure, never a synthetic stable fallback.
            from phase169_r10e4_ordered_db_prior.db_prior import (
                exact_prior_database_result, precedes_db_goal,
            )
            if precedes_db_goal(source_n, k, n, k):
                source = exact_prior_database_result(source_n, k)
        if source is None:
            continue
        images = generator_images_for_group_transport(source, goal)
        shape = _transport_shape(source, goal)
        if images is None or shape is None:
            continue
        actual_n, stem, r = shape
        iso = Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
            exponent=r,
            source_group=TodaPrimaryGroup(actual_n + stem, actual_n),
            target_group=group,
        ))
        if not any(
            isinstance(schema, Toda45IsomorphismStatement)
            and (schema == iso or specialize_typed_statement(schema, iso) is not None)
            for schema in available
        ):
            continue
        return (GoalExpansion(
            general_group_transport_rule(goal, source),
            (source, iso) + images,
        ),)
    return ()
