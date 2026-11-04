"""Status-independent presentation contract for all group proof narratives.

This is a structural presentation pass. It adds no ProofStep, inference,
literature reference, group conclusion, or proof status. The existing Markdown
API remains unchanged. One Web section hierarchy is produced for every status.
"""
from __future__ import annotations


def canonicalize_proof_layout(markdown: str) -> str:
    """Use one Reference/Proof section layout, preserving proof body verbatim.

    Both historical Markdown spellings (plain and ## headings) represent the
    same semantic sections. Only the outer Web-owned target and Proof headers
    are suppressed when duplicates are present inside the narrative. This
    transformation never reads status, n, k, references, or mathematical data.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be str")
    lines = markdown.splitlines()
    reference_indices = [
        i for i, line in enumerate(lines)
        if line.strip() in ("使用する結果", "## 使用する結果")
    ]
    if len(reference_indices) != 1:
        return markdown
    reference_index = reference_indices[0]
    proof_indices = [
        i for i in range(reference_index + 1, len(lines))
        if lines[i].strip() in ("証明", "## 証明")
    ]
    if len(proof_indices) != 1:
        return markdown
    proof_index = proof_indices[0]

    prelude = list(lines[:reference_index])
    # WebGroupProofView already presents the group target above the narrative.
    # Remove the second copy only when the entire prelude consists of that
    # exact heading and one displayable math target. Leave unknown preludes
    # intact rather than silently discarding source content.
    meaningful = [line.strip() for line in prelude if line.strip()]
    if (len(meaningful) == 2 and meaningful[0] == "## 証明対象"
            and meaningful[1].startswith("$") and meaningful[1].endswith("$")):
        prelude = []

    reference_body = list(lines[reference_index + 1:proof_index])
    while reference_body and not reference_body[-1].strip():
        reference_body.pop()
    if reference_body and reference_body[-1].strip() == "---":
        reference_body.pop()
    while reference_body and not reference_body[-1].strip():
        reference_body.pop()
    while reference_body and not reference_body[0].strip():
        reference_body.pop(0)

    proof_body = list(lines[proof_index + 1:])
    while proof_body and not proof_body[0].strip():
        proof_body.pop(0)

    # The outer Web Proof heading owns the proof section title. All narratives
    # receive the same inner Reference heading and the same section separator.
    # Only headings and redundant duplicate-target presentation are modified.
    normalized = [*prelude, "## 使用する結果", "", *reference_body,
                  "", "---", "", *proof_body]
    result = "\n".join(normalized)
    return result.rstrip("\n") + ("\n" if markdown.endswith("\n") else "")
