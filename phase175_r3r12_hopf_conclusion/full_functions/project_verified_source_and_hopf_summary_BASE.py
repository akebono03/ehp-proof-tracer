def project_verified_source_and_hopf_summary(lines: list[str], model) -> list[str]:
    """Single post-render presentation hook; all other searches pass unchanged."""
    scope = _completed_scope(model)
    if scope is None:
        return list(lines)
    with_sources = _reference_body_lines(lines, model, scope)
    normalized = _normalized_zero_image(with_sources, model, scope)
    return _verified_hopf_chain_lines(normalized, model, scope)
