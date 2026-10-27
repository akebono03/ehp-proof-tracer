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

