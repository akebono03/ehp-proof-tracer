"""Source-verified isolated registration of the universal part of Toda Lemma 5.7.

This module never registers the particular nu-prime conclusion as a GIVEN.
The original printed edition has not been independently checked; the source
is the project's adopted Chapter V transcription with a reviewed Git blob.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from phase175_r3r5_pi73_lemma57_frontier.source import verify_reviewed_toda_source

MANIFEST = Path("phase163_r4_r94_output/manifest.json")
GENERAL_ASSERTION_ID = "toda:175:r3r6:lemma57:general_conditional"
GENERAL_REFERENCE_ID = "toda:175:r3r6:Lemma 5.7"
SOURCE_ID = "toda:tex:ch5:0015"
SOURCE_SHA256 = "01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c"


@dataclass(frozen=True)
class TodaLemma57GeneralCriterion:
    """For alpha in pi_i^3, E^2 alpha in 2 iota_5 pi_(i+2)^5 implies E(eta_2 alpha)=0."""
    domain_sphere: int = 3
    target_sphere: int = 2
    twice_suspended_sphere: int = 5


def verify_lemma57_manifest(root: Path) -> dict[str, object]:
    """Pin the published source unit, adopted source checksum, and precedence."""
    source = verify_reviewed_toda_source(Path(root))
    manifest_path = Path(root) / MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST":
        raise ValueError("R3R6 unexpected publication-order manifest mode")
    rows = manifest.get("assertions")
    if not isinstance(rows, list):
        raise ValueError("R3R6 publication-order assertions are missing")
    lemma = [row for row in rows if row.get("reference_id") == "toda:Lemma 5.7"]
    proposition = [row for row in rows if row.get("reference_id") == "toda:Proposition 5.8"]
    if (len(lemma) != 1 or len(proposition) != 1
            or lemma[0].get("statement_id") != SOURCE_ID
            or lemma[0].get("source_sha256") != SOURCE_SHA256
            or lemma[0].get("publication_position") != 9100
            or proposition[0].get("publication_position") != 9200
            or lemma[0].get("review_needed") is not False
            or proposition[0].get("review_needed") is not False):
        raise ValueError("R3R6 Lemma 5.7 -> Proposition 5.8 source order changed")
    for term in (
        r"\alpha\in\pi_i(S^3)",
        r"E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5)",
        r"E(\eta_2\circ\alpha)=0",
    ):
        if term not in lemma[0].get("source_text", ""):
            raise ValueError("R3R6 general conditional not present in reviewed source unit")
    if r"\begin{proposition}\label{prop:5.8}" not in proposition[0].get("source_text", ""):
        raise ValueError("R3R6 citing proposition source changed")
    return {
        "source": source,
        "source_id": SOURCE_ID,
        "source_sha256": SOURCE_SHA256,
        "lemma_position": 9100,
        "proposition_position": 9200,
        "new_concrete_given": 0,
    }


def build_isolated_lemma57_source(root: Path):
    """Create one cited *general* GIVEN; no new concrete zero-image facts."""
    from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
    from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
        ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
    )

    verify_lemma57_manifest(root)
    statement = TodaLemma57GeneralCriterion()
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=GENERAL_REFERENCE_ID,
        kind=ReferenceKind.LEMMA,
        locator="Lemma 5.7",
        source_id="sources/toda/Toda_05_2.tex (adopted transcription; original edition unverified)",
        publication_position=9100,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=GENERAL_ASSERTION_ID,
        reference_id=GENERAL_REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=statement,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("universal conditional only", "no nu-prime conclusion as GIVEN"),
    ))
    step = ProofStep(
        conclusion=statement,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Cited universal Toda Lemma 5.7 conditional",
            literature_reference=LiteratureReference(
                label="Toda Lemma 5.7", locator="Lemma 5.7",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry=registry,
        records=(MigrationRecord(
            "phase175_r3r6", SOURCE_ID, GENERAL_ASSERTION_ID,
            MigrationStatus.STRUCTURED,
            "General source conditional only; membership and consequence remain unproved",
        ),),
        proof_links=(ProofStepLink(assertion_id=GENERAL_ASSERTION_ID, step=step),),
    )


def merge_isolated_cited_source(base, supplemental):
    """Copy the screened registry into an isolated context; never mutate production."""
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import UnifiedStatementRegistry

    if not isinstance(base, RegistryBridgeResult) or not isinstance(supplemental, RegistryBridgeResult):
        raise TypeError("R3R6 requires typed source bridges")
    registry = UnifiedStatementRegistry()
    for bridge in (base, supplemental):
        for reference in bridge.registry._references.values():
            registry.add_reference(reference)
        for assertion in bridge.registry._assertions.values():
            registry.add_assertion(assertion)
    return RegistryBridgeResult(
        registry=registry,
        records=base.records + supplemental.records,
        proof_links=base.proof_links + supplemental.proof_links,
    )
