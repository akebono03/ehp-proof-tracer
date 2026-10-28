"""Source-backed, family-ID-based suspension definitions; no family-specific rules.

HyoujiGen identity is naming/type metadata, never an axiom. A checked Toda
clause is registered as a fixed GIVEN; concrete definitions and GeneratorImage
are separate inferred proof steps. A family without checked source is not
registered and cannot receive any automatic proof.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10b_registered_stable_family_binding.family_registry import (
    RegisteredStableFamily,
    read_registered_stable_families,
    registered_family_of,
    registered_stable_family_pair,
)
from phase169_r10e8_hyoujigen_generic_suspension.source_records import (
    CHAPTER_VI_SOURCE_RECORDS,
)
from proof import (
    InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep,
)
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "sources" / "toda" / "Toda_05_2.tex"
MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"


@dataclass(frozen=True)
class FamilySourceRecord:
    """Reviewed transcription locations; adding a row adds NO proof rule."""

    family_id: int
    minimum_n: int
    stem: int
    defining_clause: str
    left_anchor: str
    right_anchor: str
    left_locator: str
    right_locator: str
    locator: str


# Additional families require an independently inspected source clause and
# reviewed ordering anchors, not just a row in the generator database.
# η retains its established cited proof path for backward compatibility.
SOURCE_RECORDS = (
    FamilySourceRecord(
        4, 4, 3,
        r"\nu_n:=E^{\,n-4}\nu_{4},\ (n\ge 4)",
        r"\begin{lemma}\label{lem:5.5}",
        r"\begin{equation}\label{eq:5.5}",
        "toda:Lemma 5.5", "toda:(5.5)",
        "Chapter V, ν-family definition (after Lemma 5.5)",
    ),
    FamilySourceRecord(
        9, 8, 7,
        r"\sigma_n :=E^{n-8}\sigma_8\ , \ (n\geq8)",
        r"\sigma_{8}:=x\alpha^{\ast}",
        r"\begin{equation}\label{eq:5.15}",
        "toda:Lemma 5.14", "toda:(5.15)",
        "Chapter V, σ-family definition (after Lemma 5.14)",
    ),
)


@dataclass(frozen=True)
class CitedStableFamilyDefinition:
    """An asserted naming convention from a cited source, not a DB result."""

    family_id: int
    minimum_n: int
    stem: int


@dataclass(frozen=True)
class StableFamilyMemberDefinition:
    """A derived, typed instance of α_n=E^(n-n0)α_n0."""

    source: CitedStableFamilyDefinition
    index: int
    element: HomotopyElement
    suspension_exponent: int


def _registered_family(family_id: int) -> RegisteredStableFamily | None:
    matches = tuple(row for row in read_registered_stable_families()
                    if row.family_id == family_id)
    return matches[0] if len(matches) == 1 else None


def _source_for(family: RegisteredStableFamily) -> CitedStableFamilyDefinition:
    return CitedStableFamilyDefinition(family.family_id, family.minimum_n, family.stem)


def verified_source_positions(
    source_path: Path = SOURCE, manifest_path: Path = MANIFEST,
) -> tuple[tuple[int, int], ...]:
    """Check clauses and ordered source anchors; no inferred publication rank."""
    source_text = Path(source_path).read_text(encoding="utf-8-sig")
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))
    if (manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or manifest.get("publication_order_scope")
            != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise ValueError("unexpected source-order manifest")
    rows = manifest.get("assertions", ())
    result = []
    used_positions = set()
    for record in SOURCE_RECORDS:
        family = _registered_family(record.family_id)
        if (family is None or family.minimum_n != record.minimum_n
                or family.stem != record.stem):
            raise ValueError("reviewed family ID/type and checked source disagree")
        if source_text.count(record.defining_clause) != 1:
            raise ValueError("cited family clause missing or repeated")
        middle = source_text.index(record.defining_clause)
        left = source_text.rfind(record.left_anchor, 0, middle)
        right = source_text.find(record.right_anchor, middle + len(record.defining_clause))
        if not (0 <= left < middle < right):
            raise ValueError("cited family moved outside reviewed source anchors")
        left_rows = [row for row in rows if row.get("reference_id") == record.left_locator]
        right_rows = [row for row in rows if row.get("reference_id") == record.right_locator]
        if len(left_rows) != 1 or len(right_rows) != 1:
            raise ValueError("source-order reference anchor missing or ambiguous")
        a = left_rows[0].get("publication_position")
        b = right_rows[0].get("publication_position")
        if type(a) is not int or type(b) is not int or b - a < 2:
            raise ValueError("cannot place cited definition in source order")
        rank = (a + b) // 2
        if rank in used_positions:
            raise ValueError("source position duplicated")
        used_positions.add(rank)
        result.append((record.family_id, rank))
    return tuple(result)


def build_cited_stable_family_definitions(
    source_path: Path = SOURCE, manifest_path: Path = MANIFEST,
) -> RegistryBridgeResult:
    """Register only source-checked family formulas with exact typed DB IDs."""
    positions = dict(verified_source_positions(source_path, manifest_path))
    registry = UnifiedStatementRegistry()
    links = []
    for record in SOURCE_RECORDS:
        family = _registered_family(record.family_id)
        if family is None:
            raise ValueError("registered source family unexpectedly missing")
        source = _source_for(family)
        ref_id = f"adopted:reference:toda5:stable_family:{record.family_id}"
        assertion_id = f"adopted:assertion:toda5:stable_family:{record.family_id}"
        registry.add_reference(LiteratureEntry(
            reference_id=ref_id, kind=ReferenceKind.DEFINITION,
            locator=record.locator,
            source_id=("sources/toda/Toda_05_2.tex "
                       "(adopted transcription, original edition unverified)"),
            publication_position=positions[record.family_id],
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id, reference_id=ref_id,
            kind=AssertionKind.DEFINITION, content=source,
            origin=AssertionOrigin.FIXED_STATEMENT,
            defined_symbol=f"stable_family_{family.family_id}",
            scope=f"n>={family.minimum_n}",
        ))
        step = ProofStep(source, (), ProofRule.GIVEN, inference_rule=InferenceRule(
            name="Cited stable-family definition",
            literature_reference=LiteratureReference(
                label="Toda stable-family definition", locator=record.locator,
            ),
        ))
        links.append(ProofStepLink(assertion_id, step=step))
    return RegistryBridgeResult(registry, (), tuple(links))


def canonical_member(source: CitedStableFamilyDefinition, index: int
                     ) -> StableFamilyMemberDefinition | None:
    """Generate an instance from a cited type signature, without a GIVEN."""
    if not isinstance(source, CitedStableFamilyDefinition) or type(index) is not int:
        return None
    # Registration is explicit: a DB row alone never authorizes a definition.
    if source.family_id not in {record.family_id for record in SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS}:
        return None
    family = _registered_family(source.family_id)
    if (family is None or _source_for(family) != source
            or index < family.minimum_n):
        return None
    element = HomotopyElement(
        name=family.name_at(index), dimension=index,
        source=index + family.stem, target=index,
        generator=GeneratorSymbol(family=family.symbol_family, index=index),
    )
    if registered_family_of(element) != family:
        return None
    return StableFamilyMemberDefinition(source, index, element,
                                        index - family.minimum_n)


def _member_instance_rule(goal: StableFamilyMemberDefinition) -> InferenceRule:
    source = goal.source
    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.GIVEN
                and premises[0].conclusion == source
                and canonical_member(source, goal.index) == goal)
    return InferenceRule(
        name="specialize cited stable-family definition",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=CitedStableFamilyDefinition,
            statement_pattern=source,
        ),),
        match_guard=guard, conclusion_pattern=goal,
    )


def _image_members(goal: GeneratorImage) -> tuple[StableFamilyMemberDefinition,
                                                    StableFamilyMemberDefinition] | None:
    if not isinstance(goal, GeneratorImage) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    family = registered_stable_family_pair(goal.source_generator, goal.target_generator)
    if family is None or goal.target_generator.dimension != goal.source_generator.dimension + 1:
        return None
    source = _source_for(family)
    first = canonical_member(source, goal.source_generator.dimension)
    second = canonical_member(source, goal.target_generator.dimension)
    if first is None or second is None:
        return None
    n = first.index
    if goal.map != TodaSuspensionMap(
        TodaPrimaryGroup(n + family.stem, n),
        TodaPrimaryGroup(n + family.stem + 1, n + 1),
    ):
        return None
    # Allow only spelling aliases, never changing generator typing or series ID.
    for observed, canonical in ((goal.source_generator, first.element),
                                (goal.target_generator, second.element)):
        if not (isinstance(observed, HomotopyElement)
                and observed.dimension == canonical.dimension
                and observed.source == canonical.source
                and observed.target == canonical.target
                and observed.generator == canonical.generator):
            return None
    if (second.suspension_exponent != first.suspension_exponent + 1
            or second.source != first.source):
        return None
    return first, second


def _family_image_rule(goal: GeneratorImage,
                       pair: tuple[StableFamilyMemberDefinition, StableFamilyMemberDefinition]
                       ) -> InferenceRule:
    def guard(premises, bindings):
        return (len(premises) == 2
                and all(p.rule is ProofRule.INFERENCE for p in premises)
                and tuple(p.conclusion for p in premises) == pair
                and _image_members(goal) == pair)
    return InferenceRule(
        name="consecutive cited stable-family instances imply generator image",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=StableFamilyMemberDefinition,
                           statement_pattern=pair[0]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=StableFamilyMemberDefinition,
                           statement_pattern=pair[1]),
        ), match_guard=guard, conclusion_pattern=goal,
    )


def expand_cited_stable_family(goal: object,
                               available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """One rule engine for every cited family; unknown μ/etc fail closed."""
    if not isinstance(available, tuple):
        raise TypeError("available must be tuple")
    if isinstance(goal, StableFamilyMemberDefinition):
        source = goal.source
        if canonical_member(source, goal.index) != goal or available.count(source) != 1:
            return ()
        return (GoalExpansion(_member_instance_rule(goal), (source,)),)
    if isinstance(goal, GeneratorImage):
        pair = _image_members(goal)
        if pair is None:
            return ()
        if available.count(pair[0].source) != 1:
            return ()
        return (GoalExpansion(_family_image_rule(goal, pair), pair),)
    return ()


def cited_family_reference_sentence(statement: object) -> str | None:
    """General definition only in Reference; concrete instances stay in proof."""
    if not isinstance(statement, CitedStableFamilyDefinition):
        return None
    if statement.family_id not in {record.family_id for record in SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS}:
        return None
    family = _registered_family(statement.family_id)
    if family is None or _source_for(family) != statement:
        return None
    return (
        rf"$n\ge {family.minimum_n}$ に対し, "
        rf"${family.latex}_n=E^{{n-{family.minimum_n}}}"
        rf"{family.latex}_{{{family.minimum_n}}}$ と定義する."
    )
