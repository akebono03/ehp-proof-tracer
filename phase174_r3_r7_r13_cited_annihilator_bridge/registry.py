"""Isolated, source-checked Toda (5.9) bridge; not installed in production.

Only the general published n>=6 annihilator is a source GIVEN. The n=6
relation is a distinct INFERENCE goal, never a source assertion or direct GIVEN.
"""
from __future__ import annotations

import json
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator, TODA_CLAUSE, reviewed_toda59_annihilator_schema,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"
REF_ID = "isolated:toda:(5.9):nu_eta_general"
ASSERTION_ID = "isolated:toda:(5.9):nu_eta_general:statement"
SOURCE_REFERENCE_ID = "toda:(5.9)"


def reviewed_toda59_source_position(manifest_path: Path = MANIFEST) -> int:
    """Use the reviewed adopted source-order record, never guess a print rank."""
    document = json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))
    if (document.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or document.get("publication_order_scope")
            != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise RuntimeError("Unexpected source-order manifest metadata")
    rows = tuple(
        x for x in document.get("assertions", ())
        if x.get("reference_id") == SOURCE_REFERENCE_ID
    )
    if len(rows) != 1:
        raise RuntimeError("Toda (5.9) must have exactly one position record")
    record = rows[0]
    pos = record.get("publication_position")
    if (type(pos) is not int or pos <= 0
            or record.get("source_file") != "Toda_05_2.tex"
            or record.get("chapter") != 5
            or record.get("review_needed") is not False
            or TODA_CLAUSE not in record.get("source_text", "")):
        raise RuntimeError("Unreviewed or incorrect Toda (5.9) position")
    return pos


def build_isolated_toda59_annihilator_bridge(
    source_path: Path | None = None,
    manifest_path: Path = MANIFEST,
) -> RegistryBridgeResult:
    """Register exactly one typed general law, with its cited source identity."""
    from phase174_r3_r7_r12_toda59_annihilator_source.source import TODA_SOURCE

    path = TODA_SOURCE if source_path is None else Path(source_path)
    schema = reviewed_toda59_annihilator_schema(path)
    position = reviewed_toda59_source_position(manifest_path)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REF_ID,
        kind=ReferenceKind.EQUATION,
        locator="(5.9)",
        source_id="sources/toda/Toda_05_2.tex (adopted; printed edition unchecked)",
        publication_position=position,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REF_ID,
        kind=AssertionKind.STATEMENT,
        content=schema,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope="nu_n composed eta_(n+3) = 0, n>=6",
    ))
    step = ProofStep(
        conclusion=schema,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Cited general annihilator source (5.9)",
            literature_reference=LiteratureReference(
                label="Toda (5.9)", locator="(5.9)",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry=registry, records=(),
        proof_links=(ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )


def join_isolated_source_bridge(
    existing: RegistryBridgeResult,
    added: RegistryBridgeResult,
) -> RegistryBridgeResult:
    """Build a new in-memory registry; never mutate the public existing bridge."""
    if not isinstance(existing, RegistryBridgeResult) or not isinstance(added, RegistryBridgeResult):
        raise TypeError("Two typed bridges are required")
    if len(added.proof_links) != 1 or added.proof_links[0].assertion_id != ASSERTION_ID:
        raise ValueError("Only one Toda (5.9) source link can be attached")
    link = added.proof_links[0]
    fixed_schema = reviewed_toda59_annihilator_schema()
    try:
        assertion = added.registry.assertion(ASSERTION_ID)
        reference = added.registry.reference(REF_ID)
    except KeyError as exc:
        raise ValueError("Checked Toda (5.9) assertion/reference missing") from exc
    if (link.step is None or link.step.rule is not ProofRule.GIVEN
            or link.step.premises
            or link.step.conclusion != fixed_schema
            or assertion.content != fixed_schema
            or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or assertion.reference_id != REF_ID
            or reference.locator != "(5.9)"
            or reference.publication_position != reviewed_toda59_source_position()
            or link.step.inference_rule is None
            or link.step.inference_rule.literature_reference is None
            or link.step.inference_rule.literature_reference.locator != "(5.9)"):
        raise ValueError("Only the independently checked cited general source may be joined")
    registry = UnifiedStatementRegistry()
    for bridge in (existing, added):
        for entry in bridge.registry._references.values():
            registry.add_reference(entry)
        for entry in bridge.registry._assertions.values():
            registry.add_assertion(entry)
    return RegistryBridgeResult(
        registry=registry,
        records=existing.records + added.records,
        proof_links=existing.proof_links + added.proof_links,
    )
