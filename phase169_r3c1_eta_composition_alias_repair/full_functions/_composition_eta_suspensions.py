def _composition_eta_suspensions(goal: object) -> tuple[GeneratorSuspension, GeneratorSuspension] | None:
    """Bind a composite DB eta goal to independently provable canonical steps.

    Source database spelling may use Unicode subscripts, whereas the existing
    cited eta-family definitions use their own canonical element objects.
    Treat only previously recognized eta-name aliases as the same generator;
    index, family, dimension, source and target must all match exactly.
    The returned subgoals are canonical typed goals, not proof certificates.
    """
    if not isinstance(goal, GeneratorImage) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    source, target = goal.source_generator, goal.target_generator
    if not isinstance(source, Composition) or not isinstance(target, Composition):
        return None
    left, right = source.left, source.right
    suspended_left, suspended_right = target.left, target.right
    factors = (left, right, suspended_left, suspended_right)
    if not all(isinstance(factor, HomotopyElement) for factor in factors):
        return None
    if not all(type(value) is int for factor in factors
               for value in (factor.dimension, factor.source, factor.target)):
        return None
    n = left.target
    if n < 2 or left.source != right.target or suspended_left.source != suspended_right.target:
        return None
    if (goal.map.source_group != TodaPrimaryGroup(n + 2, n)
            or goal.map.target_group != TodaPrimaryGroup(n + 3, n + 1)):
        return None

    from phase165_r12_r28_presentation_connection import _matching_eta_name
    older = toda_eta_family_definition_statement(n).element
    middle = toda_eta_family_definition_statement(n + 1).element
    newer = toda_eta_family_definition_statement(n + 2).element
    if not all(_matching_eta_name(actual, canonical) for actual, canonical in (
        (left, older),
        (right, middle),
        (suspended_left, middle),
        (suspended_right, newer),
    )):
        return None

    first = GeneratorSuspension(
        TodaSuspensionMap(
            TodaPrimaryGroup(n + 1, n),
            TodaPrimaryGroup(n + 2, n + 1),
        ),
        older,
        middle,
    )
    second = GeneratorSuspension(
        TodaSuspensionMap(
            TodaPrimaryGroup(n + 2, n + 1),
            TodaPrimaryGroup(n + 3, n + 2),
        ),
        middle,
        newer,
    )
    if _eta_pair(first) is None or _eta_pair(second) is None:
        return None
    return first, second
