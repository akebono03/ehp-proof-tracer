"""Register explicitly reviewed Definition occurrences, never inferred from CSV alone.

Review attestations are data, not generator-specific inference rules.  Each
attestation pins an adopted transcription, a paragraph, a unique formula, and
a relative publication order.  It makes no claim of original-print checking.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
)
from phase169_r10eo_r2_definition_index.definition_index import (
    ROOT,
    DefinitionOccurrence,
    occurrences_for_family,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"


@dataclass(frozen=True)
class ReviewedDefinitionAttestation:
    """Human-reviewed location/typing constraints; never a proof by itself."""

    family_id: int
    stem: int
    minimum_n: int
    latex: str
    source_id: str
    source_path: str
    source_sha256: str
    line: int
    paragraph_start: str
    section_end: str
    locator: str


# Each item below requires an actual source review. Never populate this from
# HyoujiGen.csv or from unreviewed DefinitionOccurrence results automatically.
REVIEWED_ATTESTATIONS = (
    ReviewedDefinitionAttestation(
        family_id=16,
        stem=11,
        minimum_n=5,
        latex=r"\zeta",
        source_id="chapter_vi",
        source_path="sources/toda/Toda_06_2.tex",
        source_sha256=(
            "e38a2119381cc9fb65b38ccb078b81933242c345cdec7d5db52af3e76281d0f1"
        ),
        line=2138,
        paragraph_start=r"\paragraph{v). The elements \(\zeta_{n}\).}",
        section_end=r"\end{paracol}",
        locator="Chapter VI, v) Definition of indexed elements",
    ),
)


def reviewed_definition_ids() -> frozenset[int]:
    """Names of independently attested entries, NOT automatic CSV admissions."""
    ids = [entry.family_id for entry in REVIEWED_ATTESTATIONS]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate reviewed Definition ID")
    return frozenset(ids)


def _chapter_vi_base(manifest_path: Path) -> int:
    """Use the existing fixed Chapter V source-order boundary, not guessed rank."""
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))
    if (manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or manifest.get("publication_order_scope")
            != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise ValueError("unreviewed publication-order manifest")
    positions = [row.get("publication_position")
                 for row in manifest.get("assertions", ())
                 if row.get("chapter") == 5
                 and type(row.get("publication_position")) is int]
    if not positions or max(positions) != 10800:
        raise ValueError("Chapter V source-order boundary changed")
    return max(positions)


def verified_reviewed_definitions(
    *, root: Path = ROOT, manifest_path: Path = MANIFEST,
    attestations: tuple[ReviewedDefinitionAttestation, ...] = REVIEWED_ATTESTATIONS,
) -> tuple[tuple[ReviewedDefinitionAttestation, DefinitionOccurrence, int], ...]:
    """Fail closed unless every reviewed occurrence matches its pinned source."""
    family_rows = {row.family_id: row for row in read_registered_stable_families(
        root / "data" / "HyoujiGen.csv")}
    chapter_vi_base = _chapter_vi_base(manifest_path)
    seen_ids: set[int] = set()
    seen_positions: set[int] = set()
    checked = []
    for attestation in attestations:
        if attestation.family_id in seen_ids:
            raise ValueError("duplicate reviewed Definition ID")
        seen_ids.add(attestation.family_id)
        row = family_rows.get(attestation.family_id)
        if (row is None or row.stem != attestation.stem
                or row.minimum_n != attestation.minimum_n
                or row.latex != attestation.latex):
            raise ValueError("reviewed Definition metadata disagrees with CSV")
        if (attestation.source_id != "chapter_vi"
                or attestation.source_path != "sources/toda/Toda_06_2.tex"):
            raise ValueError("unsupported reviewed Definition source/order")
        text = (root / attestation.source_path).read_text(encoding="utf-8-sig")
        found = occurrences_for_family(
            row, text,
            source_id=attestation.source_id,
            source_path=attestation.source_path,
        )
        if len(found) != 1:
            raise ValueError("Definition occurrence is absent or ambiguous")
        occurrence = found[0]
        if (occurrence.source_sha256 != attestation.source_sha256
                or occurrence.line != attestation.line
                or occurrence.preceding_paragraph != attestation.paragraph_start):
            raise ValueError("reviewed source fingerprint, line or paragraph changed")
        if text.count(attestation.paragraph_start) != 1:
            raise ValueError("reviewed source paragraph not unique")
        paragraph_position = text.index(attestation.paragraph_start)
        section_end = text.find(attestation.section_end, paragraph_position)
        if not (paragraph_position < occurrence.start_offset
                < occurrence.end_offset < section_end):
            raise ValueError("reviewed Definition outside source paragraph")
        position = chapter_vi_base + occurrence.line
        if position in seen_positions:
            raise ValueError("duplicate reviewed Definition source position")
        seen_positions.add(position)
        checked.append((attestation, occurrence, position))
    return tuple(checked)


def build_cited_reviewed_definitions() -> RegistryBridgeResult:
    """Create only reviewed fixed source leaves; image proofs use existing rules."""
    checked = verified_reviewed_definitions()
    registry = UnifiedStatementRegistry()
    links = []
    for record, occurrence, position in checked:
        source = CitedStableFamilyDefinition(
            record.family_id, record.minimum_n, record.stem,
        )
        reference_id = f"adopted:reference:toda6:reviewed_definition:{record.family_id}"
        assertion_id = f"adopted:assertion:toda6:reviewed_definition:{record.family_id}"
        registry.add_reference(LiteratureEntry(
            reference_id=reference_id,
            kind=ReferenceKind.DEFINITION,
            locator=record.locator,
            source_id=(record.source_path
                       + " (adopted transcription, original edition unverified)"),
            publication_position=position,
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=reference_id,
            kind=AssertionKind.DEFINITION,
            content=source,
            origin=AssertionOrigin.FIXED_STATEMENT,
            defined_symbol=f"stable_family_{record.family_id}",
            scope=f"n>={record.minimum_n}",
        ))
        step = ProofStep(
            source, (), ProofRule.GIVEN,
            inference_rule=InferenceRule(
                name="Cited reviewed Definition",
                literature_reference=LiteratureReference(
                    label="Toda Definition", locator=record.locator,
                ),
            ),
        )
        links.append(ProofStepLink(assertion_id, step=step))
    return RegistryBridgeResult(registry, (), tuple(links))
