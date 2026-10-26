def project_proven_map_property(step, latex: str) -> str | None:
    """Translate a known suffix without changing the map or its proof.

    The renderer uses the returned *whole sentence* only for derived ProofSteps.
    An unknown suffix, an unproved step, or a non-LaTeX field stays unchanged.
    """
    if step.rule is not ProofRule.INFERENCE or not isinstance(latex, str):
        return None
    match = _PROPERTY_PATTERN.search(latex)
    if match is None:
        return None
    words = match.group(1) or match.group(2)
    math = latex[:match.start()].rstrip()
    if not math:
        return None
    return f"${math}$ は{_PROPERTY_WORDS[words]}."
