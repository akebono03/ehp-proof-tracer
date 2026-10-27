def _eta_pair(goal: GeneratorSuspension):
    """Match only recognized typed eta spellings to cited family instances.

    The DB uses Unicode subscript names and Toda's existing eta path may use
    underscore names.  The already existing alias checker verifies family,
    index, source, target, dimension and one of the two accepted spellings.
    No new proof source, suspension axiom, or equality is introduced.
    """
    if not isinstance(goal, GeneratorSuspension) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    n = getattr(getattr(goal.target_generator, "generator", None), "index", None)
    if type(n) is not int or n < 3:
        return None
    older = toda_eta_family_definition_statement(n - 1)
    newer = toda_eta_family_definition_statement(n)
    from phase165_r12_r28_presentation_connection import _matching_eta_name
    if (goal.map != TodaSuspensionMap(TodaPrimaryGroup(n, n - 1), TodaPrimaryGroup(n + 1, n))
            or not _matching_eta_name(goal.source_generator, older.element)
            or not _matching_eta_name(goal.target_generator, newer.element)):
        return None
    return older, newer
