def resolve_specialized_goal_citing_id(bridge, goal: Relation) -> str | None:
    """Resolve unique positioned citations, including checked higher-stem instances."""
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, TodaPrimaryGroup)
            or not isinstance(goal.rhs, _GROUP_STRUCTURES)):
        return None
    n = goal.lhs.sphere_dimension
    m = goal.lhs.group_dimension
    if type(n) is not int or type(m) is not int:
        return None

    from phase168_r2_8_4_generic_specialization.specialization import (
        specialize_registered_higher_stem,
    )

    concrete = []
    generic = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if ":component:" in assertion.assertion_id:
            continue
        if assertion.component_position is None:
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if reference.publication_position is None:
            continue
        statement = assertion.content
        if not isinstance(statement, Relation):
            continue
        if (statement.relation_type is RelationType.EQUALITY
                and isinstance(statement.lhs, TodaPrimaryGroup)
                and statement.lhs.group_dimension == m
                and statement.lhs.sphere_dimension == n
                and isinstance(statement.rhs, _GROUP_STRUCTURES)
                and _same_group_structure(goal, statement)):
            concrete.append(assertion.assertion_id)
            continue
        candidate = specialize_registered_higher_stem(statement, n)
        if candidate is not None and candidate.lhs == goal.lhs and _same_group_structure(goal, candidate):
            generic.append(assertion.assertion_id)
            continue
        if not _is_generic_eta_group_relation(statement):
            continue
        try:
            specialized = specialize_eta_group_relation(statement, n)
        except (ValueError, TypeError):
            continue
        if specialized == goal:
            generic.append(assertion.assertion_id)
    if concrete:
        return concrete[0] if len(concrete) == 1 else None
    return generic[0] if len(generic) == 1 else None
