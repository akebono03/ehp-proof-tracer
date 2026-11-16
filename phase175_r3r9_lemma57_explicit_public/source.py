"""Quote the independently explicit nu-prime clause of Toda Lemma 5.7.

The cited source is a FIXED_STATEMENT, but it is not the generator-image
ProofStep or a group-structure theorem. A separately guarded extraction
inference must convert the cited clause to an ordinary GeneratorImage.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from phase175_r3r6_lemma57_general.source import (
    MANIFEST,
    SOURCE_ID,
    SOURCE_SHA256,
    verify_lemma57_manifest,
)

REFERENCE_ID = "toda:175:r3r9:Lemma 5.7 explicit particular clause"
ASSERTION_ID = "toda:175:r3r9:lemma57:explicit_nu_prime_zero"
SOURCE_POSITION = 9100
PARTICULAR_CLAUSE = r"E(\eta_2\circ\nu')=0"


@dataclass(frozen=True)
class TodaLemma57ExplicitNuPrimeZero:
    """The source explicitly says 'in particular, E(eta_2 o nu') = 0'."""


def verify_explicit_lemma57_source(root: Path) -> dict[str, object]:
    """Check the reviewed source SHA, whole lemma and exact particular text.

    This verifies the project's adopted Japanese transcription, not an
    independently compared printed first edition of Toda's book.
    """
    root = Path(root)
    predecessor = verify_lemma57_manifest(root)
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8-sig"))
    rows = [
        row for row in manifest["assertions"]
        if row.get("reference_id") == "toda:Lemma 5.7"
    ]
    if len(rows) != 1:
        raise ValueError("R3R9_LEMMA57_SOURCE_NOT_UNIQUE")
    lemma = rows[0]
    source_text = lemma.get("source_text", "")
    if (
        lemma.get("statement_id") != SOURCE_ID
        or lemma.get("source_sha256") != SOURCE_SHA256
        or lemma.get("publication_position") != SOURCE_POSITION
        or lemma.get("review_needed") is not False
        or not isinstance(source_text, str)
        or "特に," not in source_text
        or source_text.count(PARTICULAR_CLAUSE) != 1
        or r"\Delta(\nu_5)=\pm(\eta_2\circ\nu')" not in source_text
    ):
        raise ValueError("R3R9_LEMMA57_PARTICULAR_CLAUSE_NOT_SOURCE_VERIFIED")
    return {
        "source": predecessor,
        "source_id": SOURCE_ID,
        "source_sha256": SOURCE_SHA256,
        "publication_position": SOURCE_POSITION,
        "particular_clause": PARTICULAR_CLAUSE,
        "new_group_given": 0,
        "particular_cited_source_count": 1,
    }


def build_explicit_lemma57_source(root: Path):
    """Create one verifiable source leaf, never a direct zero-image GIVEN."""
    from phase163_r4_registry_bridge import (
        MigrationRecord,
        MigrationStatus,
        RegistryBridgeResult,
    )
    from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
    from unified_statement_registry import (
        AssertionEntry,
        AssertionKind,
        AssertionOrigin,
        LiteratureEntry,
        ProofStepLink,
        ReferenceKind,
        UnifiedStatementRegistry,
    )

    verify_explicit_lemma57_source(root)
    claim = TodaLemma57ExplicitNuPrimeZero()
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.LEMMA,
        locator="Lemma 5.7",
        source_id=(
            "sources/toda/Toda_05_2.tex "
            "(adopted transcription; original printed edition not verified)"
        ),
        publication_position=SOURCE_POSITION,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=claim,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=(
            "explicit in-particular clause of Lemma 5.7 only",
            "no group-structure GIVEN, no direct GeneratorImage GIVEN",
        ),
    ))
    step = ProofStep(
        conclusion=claim,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Cited explicit nu-prime clause of Toda Lemma 5.7",
            literature_reference=LiteratureReference(
                label="Toda Lemma 5.7", locator="Lemma 5.7",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry=registry,
        records=(MigrationRecord(
            "phase175_r3r9", SOURCE_ID, ASSERTION_ID,
            MigrationStatus.STRUCTURED,
            "Source-verified explicit particular clause; image requires inference",
        ),),
        proof_links=(ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )
