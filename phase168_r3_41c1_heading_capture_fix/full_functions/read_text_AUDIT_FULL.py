def read_text(view):
    """Include both segmented lines and unsegmented heading prefixes."""
    return '\n'.join(
        ''.join(part.value for part in line.segments)
        if line.segments else line.prefix + (line.statement_latex or '') + line.suffix
        for line in view.rendered_lines
    )
