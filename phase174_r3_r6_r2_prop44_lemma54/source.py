"""Typed, independently cited pre-Proposition-4.4 splitting and Lemma-5.4 access.

The source paragraph asserts E+h_* is an isomorphism; it does NOT assert
H(h)=+/-iota. Lemma 5.4 is preferred whenever its cited source precedes
an actual proof target. No particular group result is imported as GIVEN.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import verify_prop44_hopf_fibration_source
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase169_r4b_prop44_injectivity.rule import _is_hopf_four_suspension
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    SOURCE_ID,
    TodaLemma54TypedSource,
    add_verified_lemma54_source,
)
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parents[1]
PRELUDE_REFERENCE_ID = "phase174:r3r6r2:preprop44:reference"
PRELUDE_ASSERTION_ID = "phase174:r3r6r2:preprop44:assertion"
PRELUDE_LOCATOR = "Chapter IV, immediately before Proposition 4.4"


@dataclass(frozen=True)
class TodaPreProp44SplittingStatement:
    """The *printed* E+h_* splitting for n=2,4,8; not a claim about H(h)."""

    dimensions: tuple[int, ...] = (2, 4, 8)
    assertion: str = "E+h_* is an isomorphism for every i"


def verify_prelude_source(
    root: Path = ROOT,
    manifest: Path = DEFAULT_MANIFEST,
) -> int:
    """Pin the transcribed prelude and place it strictly before Proposition 4.4."""
    if not isinstance(root, Path) or not isinstance(manifest, Path):
        raise TypeError("root and manifest must be paths")
    verify_prop44_hopf_fibration_source(root / "sources/toda/Toda_04_2.tex")
    text = (root / "sources/toda/Toda_04_2.tex").read_text(encoding="utf-8-sig")
    start = "$n=2,4,8$ のとき, Hopf fibration"
    stop = r"\begin{proposition}\label{prop:4.4}"
    if text.count(start) != 1 or text.count(stop) != 1:
        raise ValueError("Pre-Proposition 4.4 source boundaries changed")
    passage = text.split(start, 1)[1].split(stop, 1)[0]
    if any(part not in passage for part in (
        r"S^n\hookrightarrow S^{2n-1}\xrightarrow{h} S^n",
        r"E+h_*:",
        r"\xrightarrow{\ \cong\ }",
        r"\cite{Steenrod1951}",
    )):
        raise ValueError("The cited pre-Proposition 4.4 splitting was changed")
    positions, _, _ = _load_manifest_reference_order(manifest)
    before = positions.get("toda:(4.7)")
    after = positions.get("toda:Proposition 4.4")
    if (before, after) != (7200, 7300):
        raise ValueError("Reviewed source order around Proposition 4.4 changed")
    return (before + after) // 2


def build_cited_preprop44_splitting() -> RegistryBridgeResult:
    """A separate sourced remark (one GIVEN); no Proposition 4.4 hypothesis."""
    position = verify_prelude_source()
    source = TodaPreProp44SplittingStatement()
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=PRELUDE_REFERENCE_ID,
        kind=ReferenceKind.REMARK,
        locator=PRELUDE_LOCATOR,
        source_id="sources/toda/Toda_04_2.tex (adopted transcription, original edition unverified)",
        publication_position=position,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=PRELUDE_ASSERTION_ID,
        reference_id=PRELUDE_REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=source,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("source paragraph E+h_* splitting", "n=2,4,8"),
    ))
    link = ProofStepLink(
        PRELUDE_ASSERTION_ID,
        step=ProofStep(source, (), ProofRule.GIVEN, inference_rule=InferenceRule(
            name="Cited pre-Proposition 4.4 E+h_* splitting",
            literature_reference=LiteratureReference(
                label="Toda Chapter IV prelude", locator=PRELUDE_LOCATOR,
            ),
        )),
    )
    return RegistryBridgeResult(registry, (), (link,))


def prelude_splitting_injectivity_rule(goal: MapInjective) -> InferenceRule:
    """E is a split injection when (E,h_*) is a cited isomorphism."""
    if not _is_hopf_four_suspension(goal):
        raise ValueError("Only the reviewed n=4 suspension is supported")
    source = TodaPreProp44SplittingStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == source
            and _is_hopf_four_suspension(goal)
        )

    return InferenceRule(
        name="cited Hopf-fibration splitting implies suspension injectivity",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaPreProp44SplittingStatement,
            statement_pattern=source,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Chapter IV prelude", locator=PRELUDE_LOCATOR,
        ),
    )


def expand_cited_preprop44_splitting(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Use the earlier independent splitting only when Lemma 5.4 is unavailable."""
    if not isinstance(available, tuple):
        raise TypeError("available must be screened citation statements")
    if not _is_hopf_four_suspension(goal):
        return ()
    if any(isinstance(item, TodaLemma54TypedSource) for item in available):
        return ()
    source = TodaPreProp44SplittingStatement()
    if available.count(source) != 1:
        return ()
    return (GoalExpansion(prelude_splitting_injectivity_rule(goal), (source,)),)


def attach_earlier_verified_lemma54(
    bridge: RegistryBridgeResult, citing_assertion_id: str,
) -> RegistryBridgeResult:
    """Adopt Lemma 5.4 only if its existing archive actually precedes the target.

    This is a common citation-screening operation, independent of n, k,
    target generator spelling or the eventual proof outcome.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be a typed registry bridge")
    if ADOPTED_ASSERTION_ID in bridge.registry._assertions:
        return bridge
    citing = bridge.registry.assertion(citing_assertion_id)
    citing_reference = bridge.registry.reference(citing.reference_id)
    archives = tuple(
        item for item in bridge.registry._assertions.values()
        if item.origin is AssertionOrigin.SOURCE_ARCHIVE
        and isinstance(item.content, dict)
        and item.content.get("source_statement_id") == SOURCE_ID
    )
    if len(archives) != 1:
        return bridge
    archive_reference = bridge.registry.reference(archives[0].reference_id)
    source_position = archive_reference.publication_position
    target_position = citing_reference.publication_position
    if (type(source_position) is not int or type(target_position) is not int
            or source_position >= target_position):
        return bridge
    chapter = (ROOT / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    return add_verified_lemma54_source(
        bridge, citing_assertion_id=citing_assertion_id, chapter=chapter,
    )
