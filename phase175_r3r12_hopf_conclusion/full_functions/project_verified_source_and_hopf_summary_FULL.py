def project_verified_source_and_hopf_summary(lines: list[str], model) -> list[str]:
    """Single post-render presentation hook; all other searches pass unchanged."""
    scope = _completed_scope(model)
    if scope is None:
        return list(lines)
    from phase175_r3r12_hopf_conclusion.projection import (
        project_verified_hopf_lift_conclusion,
    )
    with_sources = _reference_body_lines(lines, model, scope)
    normalized = _normalized_zero_image(with_sources, model, scope)
    summary = _verified_hopf_chain_lines(normalized, model, scope)
    return project_verified_hopf_lift_conclusion(summary, model)
