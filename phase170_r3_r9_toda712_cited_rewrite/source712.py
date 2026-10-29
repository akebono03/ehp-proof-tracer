"""Source-checked adoption of exactly one Toda (7.12) generator equality.

Chapter VII, (7.12) is a cited GIVEN. A separate, replayable inference
uses it with the admitted prior DB group and Toda (5.2). This module neither
certifies a proof nor claims that the original printed edition was checked.
"""
from __future__ import annotations

from dataclasses import replace
from hashlib import sha1
import json
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase166_r3aj_structured_generator import structured_generator_from_ids
from proof import Relation, RelationType
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ReferenceKind, UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parent.parent
CHAPTER_VI = ROOT / "sources" / "toda" / "Toda_06_2.tex"
CHAPTER_VII = ROOT / "sources" / "toda" / "Toda_07_2.tex"
MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"
GENERATORS = ROOT / "data" / "HyoujiGen.csv"
CHAPTER_VI_BLOB = "76934583cff01c8ea83f768e26947eb9b556653b"
CHAPTER_VII_BLOB = "b5b366f2d2b72d7b419192fa74ab848eff098686"
CLAUSE = (
    r"\varepsilon_3\circ\nu_{11} = \nu'\circ\ov{\nu}_6,\qquad"
    "\n"
    r"\varepsilon'\circ\eta_{13} = \nu'\circ\varepsilon_6 ."
)
LOCATOR_MARKER = r"\textbf{(7.12).}"
REF_ID = "adopted:toda7:eq7.12:generator_equality"
ASSERT_ID = "adopted:toda7:eq7.12:epsilon3_nu11_equal_nuprime_barnu6"


def _verified_adopted_source(path: Path, required_blob: str) -> str:
    """Match the reviewed Git blob, accepting local CRLF checkout conversion."""
    raw = path.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n")
    def blob_digest(data: bytes) -> str:
        return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()
    if not any(blob_digest(value) == required_blob for value in (raw, normalized)):
        raise ValueError("unreviewed adopted Toda source: " + path.name)
    return normalized.decode("utf-8-sig")


def verified_toda712_generator_equality() -> tuple[Relation, int]:
    """Validate the unique printed (7.12) clause and typed registered IDs."""
    vi = _verified_adopted_source(CHAPTER_VI, CHAPTER_VI_BLOB)
    vii = _verified_adopted_source(CHAPTER_VII, CHAPTER_VII_BLOB)
    if vii.count(CLAUSE) != 1:
        raise ValueError("reviewed Toda (7.12) equality missing or ambiguous")
    clause_offset = vii.index(CLAUSE)
    marker_offset = vii.rfind(LOCATOR_MARKER, 0, clause_offset)
    if (marker_offset < 0 or clause_offset - marker_offset > 160
            or vii.count(LOCATOR_MARKER, marker_offset, clause_offset) != 1):
        raise ValueError("Toda (7.12) occurrence is outside its reviewed locator")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    if (manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or manifest.get("publication_order_scope")
            != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise ValueError("unreviewed adopted Chapter V reference order")
    positions = tuple(row.get("publication_position") for row in manifest.get("assertions", ())
                      if row.get("chapter") == 5
                      and type(row.get("publication_position")) is int)
    if not positions or max(positions) != 10800:
        raise ValueError("Chapter V source-order boundary changed")
    # Relative to the frozen adopted transcription; never a claim about
    # absolute positions in Toda's original printed edition.
    adopted_position = max(positions) + vi.count("\n") + 1 + vii.count("\n", 0, clause_offset) + 1
    left = structured_generator_from_ids(
        ids=(10, 4), start_dimension=3, generator_csv=GENERATORS,
    )
    right = structured_generator_from_ids(
        ids=(3, 11), start_dimension=3, generator_csv=GENERATORS,
    )
    if left is None or right is None or left == right:
        raise ValueError("HyoujiGen typed generator correspondence invalid")
    from phase168_r2_toda52_transport import _typed_source_and_target
    if (_typed_source_and_target(left) != (14, 3)
            or _typed_source_and_target(right) != (14, 3)):
        raise ValueError("Toda (7.12) source and target dimensions disagree")
    return Relation(lhs=left, rhs=right, relation_type=RelationType.EQUALITY), adopted_position


def register_cited_toda712_generator_equality(base: RegistryBridgeResult) -> RegistryBridgeResult:
    """Register an exact fixed equality; never add a fabricated proof link.

    The ordinary source-first screen constructs the authorized GIVEN from
    this independently positioned assertion. Trust verification checks it.
    """
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    equality, position = verified_toda712_generator_equality()
    registry = UnifiedStatementRegistry()
    for reference in base.registry._references.values():
        registry.add_reference(reference)
    registry.add_reference(LiteratureEntry(
        reference_id=REF_ID, kind=ReferenceKind.EQUATION,
        locator="(7.12)",
        source_id="sources/toda/Toda_07_2.tex (adopted transcription, original edition unverified)",
        publication_position=position,
    ))
    for assertion in base.registry._assertions.values():
        registry.add_assertion(assertion)
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERT_ID, reference_id=REF_ID,
        kind=AssertionKind.STATEMENT, content=equality,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("typed generator equality in pi_14^3",),
    ))
    return RegistryBridgeResult(registry, base.records, base.proof_links)
