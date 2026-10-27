"""Register checked Chapter VI series definitions as cited leaves, not rules.

All family type values are read from HyoujiGen.csv. The generic inference
engine is phase169_r10d2_general_family_definition.family_citation.
"""
from __future__ import annotations

import json
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
)
from phase169_r10e8_hyoujigen_generic_suspension.source_records import (
    CHAPTER_VI_SOURCE_RECORDS,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parent.parent
CHAPTER_VI_SOURCE = ROOT / "sources" / "toda" / "Toda_06_2.tex"
CHAPTER_V_SOURCE_MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"


def verified_chapter_vi_source_positions(
    source_path: Path = CHAPTER_VI_SOURCE,
    manifest_path: Path = CHAPTER_V_SOURCE_MANIFEST,
) -> tuple[tuple[int, int], ...]:
    """Validate source clauses and assign relative order in the adopted text.

    Position numbers are relative to reviewed Chapter V positions; they do
    not assert that the original Toda printing has been independently audited.
    """
    source_text = Path(source_path).read_text(encoding="utf-8-sig")
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))
    if (manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or manifest.get("publication_order_scope")
            != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise ValueError("unreviewed Chapter V source-order manifest")
    chapter_v_positions = tuple(
        row.get("publication_position")
        for row in manifest.get("assertions", ())
        if row.get("chapter") == 5
        and type(row.get("publication_position")) is int
    )
    if not chapter_v_positions or max(chapter_v_positions) != 10800:
        raise ValueError("Chapter V source-order boundary changed")
    chapter_v_end = max(chapter_v_positions)
    family_rows = {row.family_id: row for row in read_registered_stable_families()}
    reviewed = []
    used_locations = set()
    for record in CHAPTER_VI_SOURCE_RECORDS:
        family = family_rows.get(record.family_id)
        if family is None:
            raise ValueError("Chapter VI family ID not found in HyoujiGen.csv")
        # Source n-base, source name and CSV-identified family must agree.
        if (f"n-{family.minimum_n}" not in record.defining_clause
                or not any(token in record.defining_clause for token in (
                    f"_{family.minimum_n}", f"_{{{family.minimum_n}}}",
                ))):
            raise ValueError("reviewed source formula and CSV minimum n disagree")
        symbol_in_toda = family.latex.replace(r"\bar{", r"\overline{")
        if symbol_in_toda not in record.defining_clause:
            raise ValueError("reviewed source formula and CSV family symbol disagree")
        if (source_text.count(record.defining_clause) != 1
                or source_text.count(record.paragraph_start) != 1
                or source_text.count(record.paragraph_end) != 1):
            raise ValueError("Chapter VI source clause or paragraph ambiguous")
        start = source_text.index(record.paragraph_start)
        statement = source_text.index(record.defining_clause)
        end = source_text.index(record.paragraph_end)
        if not (start < statement < end):
            raise ValueError("Chapter VI source definition moved between paragraphs")
        line_number = source_text.count("\n", 0, statement) + 1
        publication_position = chapter_v_end + line_number
        if publication_position in used_locations:
            raise ValueError("repeated Chapter VI source position")
        used_locations.add(publication_position)
        reviewed.append((record.family_id, publication_position))
    if tuple(position for _, position in reviewed) != tuple(sorted(used_locations)):
        raise ValueError("Chapter VI family definitions are not in source order")
    return tuple(reviewed)


def build_cited_chapter_vi_family_definitions(
    source_path: Path = CHAPTER_VI_SOURCE,
    manifest_path: Path = CHAPTER_V_SOURCE_MANIFEST,
) -> RegistryBridgeResult:
    """Add three independent fixed definitions to the existing source bridge.

    Neither the row, the registry nor this function establishes an E image.
    The existing inference-only R10D2 rule proves every concrete image.
    """
    positions = dict(verified_chapter_vi_source_positions(source_path, manifest_path))
    families = {row.family_id: row for row in read_registered_stable_families()}
    registry = UnifiedStatementRegistry()
    proof_links = []
    for record in CHAPTER_VI_SOURCE_RECORDS:
        family = families[record.family_id]
        claim = CitedStableFamilyDefinition(
            family_id=family.family_id,
            minimum_n=family.minimum_n,
            stem=family.stem,
        )
        reference_id = f"adopted:reference:toda6:stable_family:{family.family_id}"
        assertion_id = f"adopted:assertion:toda6:stable_family:{family.family_id}"
        registry.add_reference(LiteratureEntry(
            reference_id=reference_id,
            kind=ReferenceKind.DEFINITION,
            locator=record.locator,
            source_id=("sources/toda/Toda_06_2.tex "
                       "(adopted transcription, original edition unverified)"),
            publication_position=positions[family.family_id],
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=reference_id,
            kind=AssertionKind.DEFINITION,
            content=claim,
            origin=AssertionOrigin.FIXED_STATEMENT,
            defined_symbol=f"stable_family_{family.family_id}",
            scope=f"n>={family.minimum_n}",
        ))
        proof_links.append(ProofStepLink(
            assertion_id,
            step=ProofStep(
                claim, (), ProofRule.GIVEN,
                inference_rule=InferenceRule(
                    name="Cited stable-family definition",
                    literature_reference=LiteratureReference(
                        label="Toda stable-family definition",
                        locator=record.locator,
                    ),
                ),
            ),
        ))
    return RegistryBridgeResult(registry, (), tuple(proof_links))
