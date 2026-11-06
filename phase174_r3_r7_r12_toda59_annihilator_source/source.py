"""Source-first, unadmitted general annihilator schema from Toda (5.9).

Source text and family metadata are checked independently. Returning a
schema does not register a GIVEN, a ProofStep, or a production rule.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODA_SOURCE = ROOT / "sources" / "toda" / "Toda_05_2.tex"
TODA_CLAUSE = r"\nu_n\circ \eta_{n+3}=0\ (n\ge6)"
PROPOSITION_START = r"\begin{proposition}\label{prop:5.9}"
SOURCE_ANNIHILATOR_LOCATOR = "Toda (5.9), in the proof of Proposition 5.9"


@dataclass(frozen=True)
class CitedFamilyAnnihilator:
    """An unadmitted, citation-qualified family-composition relation schema."""

    left_family_id: int
    right_family_id: int
    minimum_left_index: int
    right_index_offset: int
    citation_locator: str


def verify_toda59_annihilator_text(path: Path = TODA_SOURCE) -> dict[str, object]:
    """Check the exact general law within its position in the adopted TeX."""
    text = Path(path).read_text(encoding="utf-8-sig")
    start = text.find(PROPOSITION_START)
    if start < 0 or text.count(PROPOSITION_START) != 1:
        raise RuntimeError("Proposition 5.9 source boundary missing or ambiguous")
    end = text.find(r"\qed", start)
    if end < 0:
        raise RuntimeError("Proposition 5.9 proof end missing")
    excerpt = text[start:end]
    marker = r"\textbf{(5.9).}"
    if excerpt.count(marker) != 1 or excerpt.count(TODA_CLAUSE) != 1:
        raise RuntimeError("Reviewed Toda (5.9) general annihilator missing or repeated")
    relation_pos = excerpt.index(TODA_CLAUSE)
    direct_pos = excerpt.find(r"E\pi_{10}^5=0")
    if not (excerpt.index(marker) < relation_pos < direct_pos):
        raise RuntimeError("Toda general source is not prior to the derived zero-image claim")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "locator": SOURCE_ANNIHILATOR_LOCATOR,
        "general_relation": TODA_CLAUSE,
        "relative_position": relation_pos,
        "direct_image_zero_position": direct_pos,
        "printed_edition_independently_verified": False,
        "source_not_registered_as_given": True,
    }


def reviewed_toda59_annihilator_schema(
    path: Path = TODA_SOURCE,
    family_csv: Path | None = None,
) -> CitedFamilyAnnihilator:
    """Return an unproved general schema only after source and family checks."""
    verify_toda59_annihilator_text(path)
    from phase169_r10b_registered_stable_family_binding.family_registry import (
        read_registered_stable_families,
    )

    families = read_registered_stable_families(family_csv)
    left = tuple(x for x in families if x.family_id == 4)
    right = tuple(x for x in families if x.family_id == 2)
    if (len(left) != 1 or len(right) != 1
            or left[0].symbol_family != "ν" or left[0].stem != 3
            or left[0].minimum_n > 6 or right[0].symbol_family != "η"
            or right[0].stem != 1 or right[0].minimum_n > 9):
        raise RuntimeError("Typed ν/η metadata differs from reviewed Toda (5.9)")
    return CitedFamilyAnnihilator(
        left_family_id=left[0].family_id,
        right_family_id=right[0].family_id,
        minimum_left_index=6,
        right_index_offset=3,
        citation_locator=SOURCE_ANNIHILATOR_LOCATOR,
    )
