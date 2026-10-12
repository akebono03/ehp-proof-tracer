"""Generic, conservative public proof narrative cleanup.

Only exact sequence subwindows already shown and duplicate exactness connectors
are removed. The proof tree and mathematical assertions are never altered.
"""
import re


def _math_tokens(text: str) -> tuple[str, ...]:
    compact = re.sub(r"\s+", "", text)
    # Preserve map labels: H and Delta must not be conflated.
    compact = re.sub(r"\\xrightarrow\{([^{}]*)\}", lambda m: "→" + m.group(1) + "→", compact)
    compact = re.sub(r"\\(?:to|rightarrow|longrightarrow)", "→→", compact)
    return tuple(re.split(r"(→[^→]*→)", compact))


def _is_sequence_math(block: str) -> bool:
    return ("\\pi" in block or "\\mathop" in block) and (
        "\\xrightarrow" in block or "\\overset" in block or
        block.count("\\to") >= 2 or block.count("\\rightarrow") >= 2
    )


def _is_subwindow(candidate: str, earlier: str) -> bool:
    if not _is_sequence_math(candidate) or not _is_sequence_math(earlier):
        return False
    small = _math_tokens(candidate)
    big = _math_tokens(earlier)
    if len(small) < 3 or len(big) < len(small):
        return False
    return any(big[i:i + len(small)] == small for i in range(len(big) - len(small) + 1))


def normalize_public_narrative_contract(markdown: str) -> str:
    """Normalize repeated connectors and duplicate EHP subwindows, conservatively."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a str")
    lines = markdown.splitlines(keepends=True)
    output: list[str] = []
    seen_sequences: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        # Only remove display math if its exact full token sequence is a subwindow.
        if line.strip() in (r"\[", "$$"):
            closer = r"\]" if line.strip() == r"\[" else "$$"
            finish = index + 1
            while finish < len(lines) and lines[finish].strip() != closer:
                finish += 1
            if finish < len(lines):
                block = "".join(lines[index + 1:finish])
                if _is_sequence_math(block):
                    if any(_is_subwindow(block, previous) for previous in seen_sequences):
                        index = finish + 1
                        while index < len(lines) and not lines[index].strip():
                            index += 1
                        continue
                    seen_sequences.append(block)
                output.extend(lines[index:finish + 1])
                index = finish + 1
                continue
        normalized = re.sub(r"完全性より\s*[,，]\s*これより\s*[,，]", "完全性より,", line)
        normalized = re.sub(r"完全性より\s*[,，]\s*完全性より\s*[,，]", "完全性より,", normalized)
        if normalized.strip() == "完全性より,":
            preceding = next((x.strip() for x in reversed(output) if x.strip()), None)
            if preceding == "完全性より,":
                index += 1
                continue
        output.append(normalized)
        index += 1
    result = "".join(output)
    # Preserve input's trailing-newline convention.
    return result
