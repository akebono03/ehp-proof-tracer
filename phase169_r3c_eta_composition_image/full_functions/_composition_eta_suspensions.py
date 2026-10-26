def _composition_eta_suspensions(goal: object) -> tuple[GeneratorSuspension, GeneratorSuspension] | None:
    """Bind a suspended composition to its two separately provable eta steps.

    This checks typed source/target dimensions; it does not prove the steps.
    """
    if not isinstance(goal, GeneratorImage) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    source, target = goal.source_generator, goal.target_generator
    if not isinstance(source, Composition) or not isinstance(target, Composition):
        return None
    f, g = source.left, source.right
    ef, eg = target.left, target.right
    if not all(isinstance(item, HomotopyElement) for item in (f, g, ef, eg)):
        return None
    if (f.source != g.target or ef.source != eg.target
            or goal.map.source_group != TodaPrimaryGroup(g.source, f.target)
            or goal.map.target_group != TodaPrimaryGroup(eg.source, ef.target)):
        return None
    if not all(type(value) is int for value in (
        f.source, f.target, g.source, g.target, ef.source, ef.target, eg.source, eg.target,
    )):
        return None
    first = GeneratorSuspension(
        TodaSuspensionMap(TodaPrimaryGroup(f.source, f.target),
                          TodaPrimaryGroup(ef.source, ef.target)),
        f, ef,
    )
    second = GeneratorSuspension(
        TodaSuspensionMap(TodaPrimaryGroup(g.source, g.target),
                          TodaPrimaryGroup(eg.source, eg.target)),
        g, eg,
    )
    if _eta_pair(first) is None or _eta_pair(second) is None:
        return None
    return first, second

