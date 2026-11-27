"""Three typed specializations of the cited Toda (5.12), isolated only."""
from dataclasses import dataclass
from pathlib import Path

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import _load_manifest_reference_order
from phase175_r4r10_cited_58_prop25_public.source import CHAPTER_5_BLOB, vetted_source
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (AssertionEntry, AssertionKind, AssertionOrigin,
                                        LiteratureEntry, ProofStepLink, ReferenceKind,
                                        UnifiedStatementRegistry)
from .source_contract import REFERENCE_ID, verify_clause, verify_positions

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = 'sources/toda/Toda_05_2.tex'


@dataclass(frozen=True)
class CitedToda512:
    n: int
    statement: MapInjective
    locator: str = '(5.12)'


def canonical_512(n):
    if type(n) is not int or n not in (4, 5, 6):
        raise ValueError('N_OUTSIDE_CITED_RANGE')
    return CitedToda512(n, MapInjective(TodaDeltaMap(
        TodaPrimaryGroup(n + 7, 2*n + 1), TodaPrimaryGroup(n + 5, n))))


def build_cited_512_source(root=ROOT, manifest=DEFAULT_MANIFEST):
    chapter = vetted_source(Path(root) / CHAPTER, CHAPTER_5_BLOB)
    verify_clause(chapter)
    positions, _, _ = _load_manifest_reference_order(Path(manifest))
    position = verify_positions(positions)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID, kind=ReferenceKind.EQUATION,
        locator='(5.12)', publication_position=position,
        source_id=CHAPTER + ' (adopted Japanese TeX; original edition unverified)'))
    links = []
    for n in (4, 5, 6):
        claim = canonical_512(n)
        assertion_id = f'toda:178:r15:equation512:n{n}'
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id, reference_id=REFERENCE_ID,
            kind=AssertionKind.STATEMENT, content=claim,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope='Only cited Delta injectivity; no group structure'))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=claim, premises=(), rule=ProofRule.GIVEN,
            inference_rule=InferenceRule(name='Cited Toda (5.12)',
                literature_reference=LiteratureReference(label='Toda (5.12)', locator='(5.12)')))))
    return RegistryBridgeResult(registry, (), tuple(links))
