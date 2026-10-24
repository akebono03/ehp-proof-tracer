def project_narrative_order(
    model: ProofNarrativeModel,
    suppressed_exactness: frozenset[int] | set[int] = frozenset(),
) -> tuple[NarrativeOrderEntry, ...]:
    """Preserve proof order except for justified quotient placement.

    A quotient is moved only behind an already present later equality
    that explicitly describes its domain. Every recorded step index is
    from the input model; there are no invented steps or citations.
    """
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if any(type(i) is not int or not 0 <= i < len(model.steps)
           for i in suppressed_exactness):
        raise ValueError("invalid suppressed proof-step index")
    postponed: dict[int, list[int]] = {}
    for index, step in enumerate(model.steps):
        statement = step.conclusion
        if not isinstance(statement, QuotientIsomorphismStatement):
            continue
        for later in range(index + 1, len(model.steps)):
            if later in suppressed_exactness:
                continue
            candidate = model.steps[later].conclusion
            if (isinstance(candidate, Relation)
                    and candidate.relation_type is RelationType.EQUALITY
                    and candidate.lhs == statement.domain):
                postponed.setdefault(later, []).append(index)
                break
    # Delay an already-present generator image until its source group and
    # typed suspension isomorphism have been presented. No steps are added.
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from homotopy_groups import TodaSuspensionMap, TodaIteratedSuspensionMap
    from toda_rules import Toda45IsomorphismStatement
    for index, step in enumerate(model.steps):
        statement = step.conclusion
        if not isinstance(statement, (GeneratorImage, GeneratorSuspension)):
            continue
        if not isinstance(statement.map, TodaSuspensionMap):
            continue
        source_index = next((j for j in range(index + 1, len(model.steps))
                             if getattr(model.steps[j].conclusion, "lhs", None)
                             == statement.map.source_group), None)
        iso_index = next((j for j in range(index + 1, len(model.steps))
                          if isinstance(model.steps[j].conclusion, Toda45IsomorphismStatement)
                          and isinstance(getattr(model.steps[j].conclusion, "map", None), TodaIteratedSuspensionMap)
                          and model.steps[j].conclusion.map.exponent == 1
                          and model.steps[j].conclusion.map.source_group == statement.map.source_group
                          and model.steps[j].conclusion.map.target_group == statement.map.target_group), None)
        if source_index is not None and iso_index is not None:
            postponed.setdefault(max(source_index, iso_index), []).append(index)
    held = {i for group in postponed.values() for i in group}
    return tuple(
        NarrativeOrderEntry(index, tuple(postponed.get(index, ())))
        for index in range(len(model.steps))
        if index not in suppressed_exactness and index not in held
    )
