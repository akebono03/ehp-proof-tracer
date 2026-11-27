"""Register only the three published intermediate Delta images of (5.13)."""
from pathlib import Path

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple, Zero
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import _load_manifest_reference_order
from phase175_r4r10_cited_58_prop25_public.source import CHAPTER_5_BLOB, vetted_source
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import (AssertionEntry, AssertionKind, AssertionOrigin,
                                        LiteratureEntry, ProofStepLink, ReferenceKind,
                                        UnifiedStatementRegistry)
from .source_contract import REFERENCE_ID, verify_clause, verify_positions

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = 'sources/toda/Toda_05_2.tex'


def _element(family, n, stem):
    digits = str(n).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))
    return HomotopyElement(family + digits, n, n + stem, n, GeneratorSymbol(family, index=n))


def canonical_513():
    """The sign is unresolved; zero images are attached to their typed maps."""
    nu9 = _element('ν', 9, 3)
    nu4_square = Composition(_element('ν', 4, 3), _element('ν', 7, 3))
    eta11_square = Composition(_element('η', 11, 1), _element('η', 12, 1))
    # Single generators use the existing simple DB adapter's indexed notation.
    # The structured composite generators above retain their Unicode names.
    eta13 = HomotopyElement('η_13', 13, 14, 13, GeneratorSymbol('η', index=13))
    return (
        TodaDeltaImageUpToSignStatement(
            TodaDeltaMap(TodaPrimaryGroup(12, 9), TodaPrimaryGroup(10, 4)),
            nu9, Multiple(2, nu4_square)),
        GeneratorImage(TodaDeltaMap(TodaPrimaryGroup(13, 11), TodaPrimaryGroup(11, 5)),
                       eta11_square, Zero()),
        GeneratorImage(TodaDeltaMap(TodaPrimaryGroup(14, 13), TodaPrimaryGroup(12, 6)),
                       eta13, Zero()),
    )


def build_cited_513_source(root=ROOT, manifest=DEFAULT_MANIFEST):
    chapter = vetted_source(Path(root) / CHAPTER, CHAPTER_5_BLOB)
    verify_clause(chapter)
    positions, _, _ = _load_manifest_reference_order(Path(manifest))
    position = verify_positions(positions)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID, kind=ReferenceKind.EQUATION,
        locator='(5.13)', publication_position=position,
        source_id=CHAPTER + ' (adopted Japanese TeX; original edition unverified)'))
    links = []
    for name, claim in zip(('nu9', 'eta11_square', 'eta13'), canonical_513()):
        assertion_id = 'toda:178:r16:equation513:' + name
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id, reference_id=REFERENCE_ID,
            kind=AssertionKind.STATEMENT, content=claim,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope='Published intermediate Delta image only; no group structure or zero-map claim'))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=claim, premises=(), rule=ProofRule.GIVEN,
            inference_rule=InferenceRule(name='Cited Toda (5.13)',
                literature_reference=LiteratureReference(label='Toda (5.13)', locator='(5.13)')))))
    return RegistryBridgeResult(registry, (), tuple(links))
