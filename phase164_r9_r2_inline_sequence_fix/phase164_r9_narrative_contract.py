"""Conservative, generic normalization of a rendered public proof.

A repeated EHP sequence subwindow may be omitted from prose. The mathematical
claims, inference order, provenance, and proof-tree nodes are not modified.
"""
from __future__ import annotations

import re

_MATH_SPAN = re.compile(r"(?<!\\)(\\\[[\s\S]*?\\\]|\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[\s\S]*?(?<!\$)\$(?!\$))")
_GROUP = re.compile(r"\\pi\s*_\s*(?:\{\s*([^{}]+?)\s*\}|([A-Za-z0-9]+))\s*\^\s*(?:\{\s*([^{}]+?)\s*\}|([A-Za-z0-9]+))")
_MAP = re.compile(r"(?:\\xrightarrow\s*\{([^{}]+)\}|\\(?:overset|stackrel)\s*\{([^{}]+)\}\s*\{\s*\\(?:to|rightarrow|longrightarrow)\s*\})")
_ARROW = re.compile(r"\\(?:to|rightarrow|longrightarrow)|\\xrightarrow|\\overset|\\stackrel")


def _sequence_signature(math_text: str):
    """Return ordered group and map tokens, or None for non-sequence math."""
    groups = list(_GROUP.finditer(math_text))
    if len(groups) < 3:
        return None
    terms = [(re.sub(r"\s+", "", m.group(1) or m.group(2)),
              re.sub(r"\s+", "", m.group(3) or m.group(4))) for m in groups]
    labels = []
    for current, following in zip(groups, groups[1:]):
        gap = math_text[current.end():following.start()]
        if not _ARROW.search(gap):
            return None
        match = _MAP.search(gap)
        label = re.sub(r"\s+", "", (match.group(1) or match.group(2))) if match else "UNLABELED"
        labels.append(label)
    return terms, labels


def _contained(candidate, earlier):
    if candidate is None or earlier is None:
        return False
    terms, labels = candidate
    big_terms, big_labels = earlier
    if len(terms) >= len(big_terms):
        return False
    for index in range(len(big_terms) - len(terms) + 1):
        if big_terms[index:index + len(terms)] == terms and big_labels[index:index + len(labels)] == labels:
            return True
    return False


def _remove_repeated_math_subwindows(body: str) -> str:
    seen = []
    removed = []
    for match in _MATH_SPAN.finditer(body):
        signature = _sequence_signature(match.group())
        if signature is None:
            continue
        if any(_contained(signature, earlier) for earlier in seen):
            # Omit only the repeated math, never an adjacent explanation.
            removed.append((match.start(), match.end()))
        else:
            seen.append(signature)
    if not removed:
        return body
    for start, end in reversed(removed):
        # Drop a standalone math paragraph including its newline, when possible.
        left = body.rfind("\n", 0, start) + 1
        right = body.find("\n", end)
        right = len(body) if right == -1 else right
        if body[left:start].strip() == "" and body[end:right].strip() in ("", ".", "。"):
            remove_right = right + (right < len(body))
            body = body[:left] + body[remove_right:]
        else:
            body = body[:start] + body[end:]
    return body


def _normalize_connectors(body: str) -> str:
    body = re.sub(r"完全性より\s*[,，]\s*これより\s*[,，]", "完全性より,", body)
    body = re.sub(r"完全性より\s*[,，]\s*完全性より\s*[,，]", "完全性より,", body)
    lines = body.splitlines(keepends=True)
    result = []
    for line in lines:
        if line.strip() == "完全性より,":
            preceding = next((s.strip() for s in reversed(result) if s.strip()), "")
            if preceding == "完全性より,":
                continue
        result.append(line)
    return "".join(result)


def normalize_public_narrative_contract(markdown: str) -> str:
    """Remove only already-displayed EHP subwindows and duplicated connectors."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a str")
    # Only proof body is normalized, never cited references or goal statements.
    boundary = re.search(r"(?m)^##\s*証明\s*$", markdown)
    if boundary:
        head, body = markdown[:boundary.end()], markdown[boundary.end():]
    else:
        head, body = "", markdown
    body = _remove_repeated_math_subwindows(body)
    body = _normalize_connectors(body)
    return head + body
