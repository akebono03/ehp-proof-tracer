def index_typed_components(registry: UnifiedStatementRegistry) -> tuple[TypedComponentMatch, ...]:
    """Create a lossless read-only index of fixed typed assertions and their fields."""
    if not isinstance(registry, UnifiedStatementRegistry):
        raise TypeError("registry must be UnifiedStatementRegistry")
    matches = []
    for assertion in registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        value = assertion.content
        component_fields = (
            tuple(field.name for field in fields(value))
            if is_dataclass(value) and not isinstance(value, type) else ()
        )
        legacy_prop51_fields = (
            "pi3_2_group_relation",
            "eta2_hopf_relation",
            "delta_iota5_relation",
            "higher_eta_group_relation",
        )
        explicitly_declared = (
            isinstance(assertion.scope, tuple)
            and len(assertion.scope) == 2
            and assertion.scope[0] == "typed_composite_fields"
            and assertion.scope[1] == component_fields
        )
        if component_fields and (
            explicitly_declared or component_fields == legacy_prop51_fields
        ):
            components = tuple((field.name, getattr(value, field.name)) for field in fields(value))
        else:
            components = (("__self__", value),)
        for name, content in components:
            if content is None:
                continue
            matches.append(TypedComponentMatch(
                assertion_id=assertion.assertion_id,
                reference_id=assertion.reference_id,
                component_name=name,
                content=content,
                origin=assertion.origin,
            ))
    return tuple(matches)


