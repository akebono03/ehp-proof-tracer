def web_reference_text(view: object) -> str:
    """Extract only the Web Reference section, excluding the target and proof."""
    lines = []
    started = False
    for line in view.rendered_lines:
        content = web_line_text(line)
        if not started:
            if content.strip() == "使用する結果":
                started = True
                lines.append(content)
            continue
        if content.strip() == "証明":
            return "\n".join(lines)
        lines.append(content)
    raise ValueError("Web Narrative lacks a Reference or proof boundary")
