"""Status-independent presentation contract for all group proof narratives.

This is a structural presentation pass. It adds no ProofStep, inference,
literature reference, group conclusion, or proof status. The existing Markdown
API remains unchanged. One Web section hierarchy is produced for every status.
"""
from __future__ import annotations


def _public_search_diagnostic_line(line: str) -> str:
    """Present a recorded diagnostic without exposing a Python object repr.

    This only changes the public display. The original diagnostic remains in
    ProofNarrativeModel and PartialProofResult for inspection and auditing.
    """
    if not line.startswith("- "):
        return line
    message = line[2:].strip()
    prefix = "expected a verified registered derivation for "
    if message.startswith(prefix):
        before, separator, count = message.rpartition(", found ")
        if separator and before.startswith(prefix) and count.isdecimal():
            return (
                "- 登録済みの前提から証明目標を導く検証済みの推論が見つかりませんでした"
                f"（導出候補 {count} 件）。"
            )
    if any(token in message for token in (
        "Relation(", "TodaPrimaryGroup(", "HomotopyElement(",
        "GeneratorSymbol(",
    )):
        return "- 型付き証明目標の内部診断があります。詳細は監査ログを参照してください。"
    return line


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
    in_search_diagnostics = False
    for index, line in enumerate(normalized):
        if line.startswith(("## ", "### ")):
            in_search_diagnostics = line.strip() == "## 探索診断"
        elif in_search_diagnostics and line.startswith("- "):
            normalized[index] = _public_search_diagnostic_line(line)
    normalized = _normalize_narrative_punctuation(normalized)
    result = "\n".join(normalized)
    return result.rstrip("\n") + ("\n" if markdown.endswith("\n") else "")

def _normalize_narrative_punctuation(lines: list[str]) -> list[str]:
    """Apply uniform prose punctuation to the common Web narrative layout.

    Math and inline-code spans remain untouched. Numbered source locators,
    decimal points, headings, and display math remain intact. Sentence-final
    periods create physical line breaks, not new proof steps.
    """
    result: list[str] = []
    in_display_math = False
    in_code_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            result.append(line)
            continue
        if stripped == r"\[":
            in_display_math = True
            result.append(line)
            continue
        if stripped == r"\]":
            in_display_math = False
            result.append(line)
            continue
        if (in_code_fence or in_display_math
                or stripped.startswith(("# ", "## ", "### "))):
            result.append(line)
            continue

        chunks: list[str] = []
        current: list[str] = []
        in_inline_math = False
        in_inline_code = False
        for index, raw in enumerate(line):
            if raw == "$" and not in_inline_code and (index == 0 or line[index - 1] != "\\"):
                in_inline_math = not in_inline_math
            elif raw == "`" and not in_inline_math and (index == 0 or line[index - 1] != "\\"):
                in_inline_code = not in_inline_code

            protected = in_inline_math or in_inline_code or raw in ("$", "`")
            character = raw
            if not protected and raw in ("、", "，"):
                character = "," if (index + 1 < len(line) and line[index + 1].isspace()) else ", "
            elif not protected and raw == "。":
                character = "."
            current.append(character)

            if protected or character != ".":
                continue
            remaining = line[index + 1:]
            next_word = remaining.lstrip()
            if not next_word:
                continue
            # The dot in 4.4, 0.5, or an enumerated item is not a full stop.
            if raw == "." and remaining[0].isdigit():
                continue
            if raw == "." and "".join(current[:-1]).strip().isdigit():
                continue
            next_char = next_word[0]
            is_japanese = (
                "\u3040" <= next_char <= "\u30ff"
                or "\u3400" <= next_char <= "\u9fff"
            )
            sentence_boundary = raw == "。" or is_japanese or (
                remaining[0].isspace()
                and (next_char.isupper() or next_char in "（[「")
            )
            if sentence_boundary:
                chunks.append("".join(current).rstrip())
                current = []
        final = "".join(current).strip()
        if final:
            chunks.append(final)
        if chunks:
            result.extend(chunks)
        else:
            result.append("")
    return result
