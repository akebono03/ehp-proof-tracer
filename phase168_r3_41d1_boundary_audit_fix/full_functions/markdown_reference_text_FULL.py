def markdown_reference_text(markdown: str) -> str:
    """Return precisely the Reference section in either common format."""
    reference, _ = split_narrative_sections(markdown)
    return reference
