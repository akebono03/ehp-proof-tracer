"""Typed transcription of the signed Delta clause in Toda Lemma 5.7."""
from __future__ import annotations

from pathlib import Path

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase175_r3r5_pi73_lemma57_frontier.source import LEMMA_START, LEMMA_END, SOURCE_PATH
from phase175_r3r9_lemma57_explicit_public.source import (
    SOURCE_ID, SOURCE_POSITION, verify_explicit_lemma57_source,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ID = 'toda:176:r3r48:Lemma 5.7 signed Delta clause'
ASSERTION_ID = 'toda:176:r3r48:lemma57:signed_delta_image'
CLAUSE = r"\Delta(\nu_5)=\pm(\eta_2\circ\nu')"


def canonical_signed_delta():
    """Use the existing structured generator representation, not a DB map coefficient."""
    nu5 = HomotopyElement('ν₅', 5, 8, 5, GeneratorSymbol('ν', index=5))
    eta2 = HomotopyElement('η₂', 2, 3, 2, GeneratorSymbol('η', index=2))
    nu_prime = HomotopyElement("ν'", 3, 6, 3, GeneratorSymbol(r"\nu'"))
    return TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(8, 5), TodaPrimaryGroup(6, 2)),
        nu5, Composition(eta2, nu_prime),
    )


def build_cited_lemma57_delta_source(root: Path = ROOT) -> RegistryBridgeResult:
    """Verify the adopted source and add exactly one signed source leaf."""
    root = Path(root)
    verify_explicit_lemma57_source(root)
    chapter = (root / SOURCE_PATH).read_text(encoding='utf-8-sig')
    lemma = chapter.split(LEMMA_START, 1)[1].split(LEMMA_END, 1)[0]
    if lemma.count(CLAUSE) != 1:
        raise ValueError('R3R48_SIGNED_CLAUSE_NOT_UNIQUE_IN_LEMMA')
    claim = canonical_signed_delta()
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID, kind=ReferenceKind.LEMMA,
        locator='Lemma 5.7', source_id=SOURCE_ID,
        publication_position=SOURCE_POSITION,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID, reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT, content=claim,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=('signed clause only', 'adopted TeX; original edition unverified'),
    ))
    step = ProofStep(
        conclusion=claim, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name='Cited signed Delta image of Toda Lemma 5.7',
            literature_reference=LiteratureReference(label='Toda Lemma 5.7', locator='Lemma 5.7'),
        ),
    )
    record = MigrationRecord('phase176_r3r48', SOURCE_ID, ASSERTION_ID,
                             MigrationStatus.STRUCTURED, 'Signed image only; no kernel or group GIVEN')
    return RegistryBridgeResult(registry, (record,), (ProofStepLink(ASSERTION_ID, step=step),))
