def _text(view):
    """Read both inline content and Web heading rows in the rendered view."""
    return "\n".join(
        "".join(part.value for part in line.segments)
        if line.segments else line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )
