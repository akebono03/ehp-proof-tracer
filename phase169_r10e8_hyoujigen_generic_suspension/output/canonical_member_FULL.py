def canonical_member(source: CitedStableFamilyDefinition, index: int
                     ) -> StableFamilyMemberDefinition | None:
    """Generate an instance from a cited type signature, without a GIVEN."""
    if not isinstance(source, CitedStableFamilyDefinition) or type(index) is not int:
        return None
    # Registration is explicit: a DB row alone never authorizes a definition.
    if source.family_id not in {record.family_id for record in SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS}:
        return None
    family = _registered_family(source.family_id)
    if (family is None or _source_for(family) != source
            or index < family.minimum_n):
        return None
    element = HomotopyElement(
        name=family.name_at(index), dimension=index,
        source=index + family.stem, target=index,
        generator=GeneratorSymbol(family=family.symbol_family, index=index),
    )
    if registered_family_of(element) != family:
        return None
    return StableFamilyMemberDefinition(source, index, element,
                                        index - family.minimum_n)

