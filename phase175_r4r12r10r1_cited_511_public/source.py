"""A single source-verified Toda equation (5.11), not the pi_9^5 group result."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_DELTA_MAP
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from phase175_r4r10_cited_58_prop25_public.source import vetted_source, CHAPTER_5_BLOB
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = "sources/toda/Toda_05_2.tex"
REFERENCE_ID = "toda:(5.11)"
ASSERTION_ID = "toda:175:r4r12r10r1:equation511"
LABEL = r"\begin{equation}\label{eq:5.11}"
FORMULA = r"\Delta(\eta_9)=E\nu'\circ\eta_7"


@dataclass(frozen=True)
class CitedToda511:
    statement: Relation
    locator: str = "(5.11)"


def canonical_511() -> Relation:
    eta9 = HomotopyElement("η₉", 9, 10, 9, GeneratorSymbol("η", index=9))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    nu_prime = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    return Relation(
        MapApplication(EHP_DELTA_MAP, eta9),
        Composition(Suspension(nu_prime), eta7),
        RelationType.EQUALITY,
    )


def verify_cited_511(root: Path = ROOT, manifest: Path = DEFAULT_MANIFEST) -> int:
    chapter = vetted_source(root / CHAPTER, CHAPTER_5_BLOB)
    if chapter.count(LABEL) != 1:
        raise RuntimeError("R10R1_SOURCE_LABEL_NOT_UNIQUE")
    section = chapter.split(LABEL, 1)[1].split(r"\end{equation}", 1)[0]
    if section.count(FORMULA) != 1:
        raise RuntimeError("R10R1_SOURCE_FORMULA_CHANGED")
    proof_start = chapter.index(r"\begin{proposition}\label{prop:5.8}")
    proof_end = chapter.index(r"\begin{proposition}\label{prop:5.9}")
    if not proof_start < chapter.index(LABEL) < proof_end:
        raise RuntimeError("R10R1_SOURCE_ORDER_CHANGED")
    positions, _, _ = _load_manifest_reference_order(manifest)
    position = positions.get(REFERENCE_ID)
    if type(position) is not int or position <= 0:
        raise RuntimeError("R10R1_REFERENCE_NOT_IN_MANIFEST")
    return position


def build_cited_511_source(root: Path = ROOT, manifest: Path = DEFAULT_MANIFEST) -> RegistryBridgeResult:
    position = verify_cited_511(root, manifest)
    citation = CitedToda511(canonical_511())
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.EQUATION,
        locator="(5.11)",
        source_id=CHAPTER + " (adopted Japanese TeX; original edition unverified)",
        publication_position=position,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=citation,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope="only the published Delta(eta_9) image; not the pi_9^5 group result",
    ))
    step = ProofStep(
        conclusion=citation,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Cited Toda (5.11)",
            literature_reference=LiteratureReference(label="Toda (5.11)", locator="(5.11)"),
        ),
    )
    return RegistryBridgeResult(registry, (), (ProofStepLink(ASSERTION_ID, step=step),))
