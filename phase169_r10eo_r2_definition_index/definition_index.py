"""Read-only, generic index of literal suspension definitions in adopted Toda TeX.

The index is untrusted discovery data. Neither a CSV row nor an exact formula
match is an attestation, citation, GIVEN, or verified inference.
"""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path

from phase169_r10b_registered_stable_family_binding.family_registry import (
    RegisteredStableFamily,
    read_registered_stable_families,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = (
    ("chapter_v", Path("sources/toda/Toda_05_2.tex")),
    ("chapter_vi", Path("sources/toda/Toda_06_2.tex")),
)
_TEX_SPACING = (r"\qquad", r"\quad", r"\,", r"\;", r"\!")


@dataclass(frozen=True)
class DefinitionOccurrence:
    """One exact textual occurrence. This object carries NO proof authority."""

    family_id: int
    stem: int
    minimum_n: int
    latex: str
    source_id: str
    source_path: str
    source_sha256: str
    line: int
    start_offset: int
    end_offset: int
    normalized_formula: str
    preceding_paragraph: str | None
    classification: str = "TEXT_ONLY_NOT_CITED"


def mask_tex_comments(source: str) -> str:
    """Hide unescaped TeX comments without shifting original source offsets."""
    result: list[str] = []
    comment = False
    for index, char in enumerate(source):
        if char == "\n":
            comment = False
            result.append(char)
        elif comment:
            result.append(" ")
        elif char == "%" and (index == 0 or source[index - 1] != "\\"):
            comment = True
            result.append(" ")
        else:
            result.append(char)
    return "".join(result)


def normalized_tex_with_offsets(source: str) -> tuple[str, tuple[int, ...]]:
    """Normalize surface TeX for *literal* indexing; retain original offsets.

    This is deliberately not a general-purpose TeX semantic equivalence check.
    """
    result: list[str] = []
    offsets: list[int] = []
    i = 0
    while i < len(source):
        char = source[i]
        if char.isspace():
            i += 1
            continue
        spacing = next((token for token in _TEX_SPACING
                        if source.startswith(token, i)), None)
        if spacing is not None:
            i += len(spacing)
            continue
        if source.startswith(r"\overline{\nu}", i):
            replacement = r"\bar{\nu}"
            result.extend(replacement)
            offsets.extend((i,) * len(replacement))
            i += len(r"\overline{\nu}")
            continue
        if source.startswith(r"\overline\nu", i):
            replacement = r"\bar{\nu}"
            result.extend(replacement)
            offsets.extend((i,) * len(replacement))
            i += len(r"\overline\nu")
            continue
        if source.startswith(r"\bar\nu", i):
            replacement = r"\bar{\nu}"
            result.extend(replacement)
            offsets.extend((i,) * len(replacement))
            i += len(r"\bar\nu")
            continue
        if char == "_" and i + 2 < len(source) and source[i + 1] == "{":
            end = source.find("}", i + 2)
            inside = source[i + 2:end] if end != -1 else ""
            if inside == "n" or inside.isdecimal():
                piece = "_" + inside
                result.extend(piece)
                offsets.extend((i,) * len(piece))
                i = end + 1
                continue
        result.append(char)
        offsets.append(i)
        i += 1
    return "".join(result), tuple(offsets)


def normalized_tex(source: str) -> str:
    """Return the normalized candidate surface, without mathematical claims."""
    return normalized_tex_with_offsets(source)[0]


def expected_formula(family: RegisteredStableFamily) -> str:
    """Derive a literal lookup pattern from CSV type metadata only."""
    if family.family_id <= 0 or family.minimum_n < 1 or family.stem < 0:
        raise ValueError("invalid generator metadata for definition indexing")
    symbol = family.latex.strip()
    if not symbol:
        raise ValueError("empty generator TeX")
    return normalized_tex(
        rf"{symbol}_n:=E^{{n-{family.minimum_n}}}{symbol}_{{{family.minimum_n}}}"
    )


def occurrences_for_family(
    family: RegisteredStableFamily, text: str, *,
    source_id: str, source_path: str,
) -> tuple[DefinitionOccurrence, ...]:
    """Find exact formulas with stable offsets and no 130-char window overlap."""
    pattern = expected_formula(family)
    normalized, offsets = normalized_tex_with_offsets(mask_tex_comments(text))
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    found: list[DefinitionOccurrence] = []
    cursor = 0
    while True:
        start = normalized.find(pattern, cursor)
        if start < 0:
            break
        beginning = offsets[start]
        ending = offsets[start + len(pattern) - 1] + 1
        paragraph_start = text.rfind(r"\paragraph{", 0, beginning)
        paragraph = None
        if paragraph_start >= 0:
            paragraph_end = text.find("\n", paragraph_start)
            if paragraph_end == -1:
                paragraph_end = len(text)
            paragraph = text[paragraph_start:paragraph_end].strip()
        found.append(DefinitionOccurrence(
            family_id=family.family_id,
            stem=family.stem,
            minimum_n=family.minimum_n,
            latex=family.latex,
            source_id=source_id,
            source_path=source_path,
            source_sha256=digest,
            line=text.count("\n", 0, beginning) + 1,
            start_offset=beginning,
            end_offset=ending,
            normalized_formula=pattern,
            preceding_paragraph=paragraph,
        ))
        cursor = start + len(pattern)
    return tuple(found)


def index_definitions(root: Path = ROOT) -> dict:
    """Index EVERY registered kinds=0 row, without promoting text to GIVEN."""
    registered = read_registered_stable_families(root / "data" / "HyoujiGen.csv")
    sources = tuple((name, relative.as_posix(),
                     (root / relative).read_text(encoding="utf-8-sig"))
                    for name, relative in SOURCE_FILES)
    items: list[dict] = []
    for family in registered:
        matches = tuple(
            occurrence
            for source_id, source_path, content in sources
            for occurrence in occurrences_for_family(
                family, content, source_id=source_id, source_path=source_path,
            )
        )
        status = ("UNIQUE_TEXT_CANDIDATE_NOT_AUTHORIZED" if len(matches) == 1
                  else "NO_EXACT_TEXT_CANDIDATE" if not matches
                  else "AMBIGUOUS_TEXT_CANDIDATES_NOT_AUTHORIZED")
        items.append({
            "family_id": family.family_id,
            "display": family.display,
            "stem": family.stem,
            "minimum_n": family.minimum_n,
            "latex": family.latex,
            "pattern": expected_formula(family),
            "status": status,
            "occurrences": [asdict(match) for match in matches],
        })
    return {
        "mode": "AUDIT_ONLY",
        "source_kind": "ADOPTED_TRANSCRIPTION_NOT_INDEPENDENTLY_CHECKED_PRINT",
        "registered_series": len(registered),
        "unique_literal_candidates": sum(len(item["occurrences"]) == 1 for item in items),
        "ambiguous_literal_candidates": sum(len(item["occurrences"]) > 1 for item in items),
        "no_literal_candidates": sum(len(item["occurrences"]) == 0 for item in items),
        "fixed_statements_added": 0,
        "given_proof_steps_added": 0,
        "inference_rules_changed": False,
        "families": items,
    }


def check_existing_reviewed_records(index: dict) -> tuple[dict, ...]:
    """Cross-check existing human-reviewed records; never replace them."""
    from phase169_r10d2_general_family_definition.family_citation import SOURCE_RECORDS
    from phase169_r10e8_hyoujigen_generic_suspension.source_records import (
        CHAPTER_VI_SOURCE_RECORDS,
    )
    existing = {record.family_id: record for record in
                SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS}
    reports: list[dict] = []
    for item in index["families"]:
        record = existing.get(item["family_id"])
        if record is None:
            continue
        source_id = "chapter_v" if hasattr(record, "left_anchor") else "chapter_vi"
        selected = [match for match in item["occurrences"]
                    if match["source_id"] == source_id]
        if len(selected) != 1:
            raise ValueError("reviewed source formula has no unique literal match")
        if not normalized_tex(record.defining_clause).startswith(item["pattern"]):
            raise ValueError("reviewed source formula diverges from CSV-based pattern")
        reports.append({"family_id": item["family_id"], "source_id": source_id,
                        "existing_reviewed_record_agrees": True})
    if len(reports) != len(existing):
        raise ValueError("a reviewed source record has no indexed member")
    return tuple(reports)
