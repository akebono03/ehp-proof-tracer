def split_narrative_sections(markdown: str) -> tuple[str, str]:
    """Recognize both completed and incomplete common Narrative headings.

    The incomplete format has a preceding `## 証明対象` heading. Neither that
    target nor the proof body is part of the Reference section. Reject unknown
    formats instead of silently treating the whole document as references.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a str")
    lines = markdown.splitlines()
    reference_start = next(
        (index for index, line in enumerate(lines)
         if line.strip() in ("使用する結果", "## 使用する結果")), None)
    if reference_start is None:
        raise ValueError("common Narrative lacks the Reference boundary")
    proof_start = next(
        (index for index in range(reference_start + 1, len(lines))
         if lines[index].strip() in ("証明", "## 証明")), None)
    if proof_start is None:
        raise ValueError("common Narrative lacks the proof boundary")
    reference = "\n".join(lines[reference_start:proof_start]).strip()
    proof = "\n".join(lines[proof_start + 1:]).strip()
    return reference, proof
