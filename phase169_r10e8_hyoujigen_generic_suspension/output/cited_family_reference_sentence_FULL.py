def cited_family_reference_sentence(statement: object) -> str | None:
    """General definition only in Reference; concrete instances stay in proof."""
    if not isinstance(statement, CitedStableFamilyDefinition):
        return None
    if statement.family_id not in {record.family_id for record in SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS}:
        return None
    family = _registered_family(statement.family_id)
    if family is None or _source_for(family) != statement:
        return None
    return (
        rf"$n\ge {family.minimum_n}$ に対し, "
        rf"${family.latex}_n=E^{{n-{family.minimum_n}}}"
        rf"{family.latex}_{{{family.minimum_n}}}$ と定義する."
    )

