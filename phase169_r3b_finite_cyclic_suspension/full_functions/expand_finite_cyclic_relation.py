def expand_finite_cyclic_relation(goal: object) -> tuple[GoalExpansion, ...]:
    """Propose typed derivations; no source goal or map property is accepted as fact."""
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return ()
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        return ()
    if type(goal.rhs.order) is not int or goal.rhs.order < 1:
        return ()
    source = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    options = [GoalExpansion(finite_cyclic_structure_as_relation_inference_rule(), (source,))]

    # Phase 169: generate one structural 2-stem candidate from a separately
    # registered lower-dimensional Goal, not from a stored or assumed proof.
    if not isinstance(goal.lhs, TodaPrimaryGroup):
        return tuple(options)
    q = goal.lhs.group_dimension
    n = goal.lhs.sphere_dimension
    if (type(q) is not int or type(n) is not int
            or n < 3 or q != n + 2
            or not isinstance(goal.rhs.generator, Composition)):
        return tuple(options)

    from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
    candidates = database_structured_group_goal_candidates(n=n - 1, k=2)
    if len(candidates) != 1:
        return tuple(options)
    lower = candidates[0]
    if (not isinstance(lower, Relation)
            or lower.relation_type is not RelationType.EQUALITY
            or lower.lhs != TodaPrimaryGroup(q - 1, n - 1)
            or not isinstance(lower.rhs, FiniteCyclicGroup)
            or lower.rhs.order != goal.rhs.order
            or not isinstance(lower.rhs.generator, Composition)):
        return tuple(options)

    suspension = TodaSuspensionMap(source_group=lower.lhs, target_group=goal.lhs)
    options.append(GoalExpansion(
        finite_cyclic_suspension_transport_inference_rule(),
        (
            lower,
            TodaSuspensionIsomorphismStatement(map=suspension),
            GeneratorImage(
                map=suspension,
                source_generator=lower.rhs.generator,
                target_generator=goal.rhs.generator,
            ),
        ),
    ))
    return tuple(options)
