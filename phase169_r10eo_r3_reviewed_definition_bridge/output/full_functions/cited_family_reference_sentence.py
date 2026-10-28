def cited_family_reference_sentence(statement: object) -> str | None:
    """General cited Definition in Reference; concrete result in proof body."""
    if not isinstance(statement, CitedStableFamilyDefinition):
        return None
    from phase169_r10eo_r3_reviewed_definition_bridge.reviewed_definitions import (
        reviewed_definition_ids,
    )
    authorized_ids = (
        {record.family_id for record in SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS}
        | reviewed_definition_ids()
    )
    if statement.family_id not in authorized_ids:
        return None
    family = _registered_family(statement.family_id)
    if family is None or _source_for(family) != statement:
        return None
    return (
        rf"$n\ge {family.minimum_n}$ に対し, "
        rf"${family.latex}_n=E^{{n-{family.minimum_n}}}"
        rf"{family.latex}_{{{family.minimum_n}}}$ と定義する."
    )
