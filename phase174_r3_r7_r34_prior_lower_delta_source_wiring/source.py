"""Cite two independently printed prior facts for the lower EHP Delta.

Only Toda Proposition 5.8 and equation (5.10) are added as FIXED_STATEMENT
leaves. Their generator is checked against the real structured DB prior, but
DB data does not independently certify the mathematics. No kernel, top Delta,
or root group is asserted; no proof search or renderer is overridden.
"""
from __future__ import annotations

from hashlib import sha1
from pathlib import Path

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3aj_structured_generator import structured_generator_from_ids
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from proof import (
    InferenceRule,
    LiteratureReference,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
)
from toda_rules import TodaDeltaImageUpToSignStatement
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
SOURCE = "sources/toda/Toda_05_2.tex"
SOURCE_BLOB = "579661138928499ba04a51327f686d9b971b5314"
PROP58 = r"\begin{proposition}\label{prop:5.8}"
PROP59 = r"\begin{proposition}\label{prop:5.9}"
EQ510 = r"\begin{equation}\label{eq:5.10}"
CODOMAIN_CLAUSE = r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}"
IMAGE_CLAUSE = r"\Delta(\iota_{11})=\nu_5\circ\eta_8"
MANIFEST_ROWS = (
    ("Proposition 5.8", "toda:Proposition 5.8", "toda:tex:ch5:0016", ReferenceKind.PROPOSITION),
    ("(5.10)", "toda:(5.10)", "toda:tex:ch5:0018", ReferenceKind.EQUATION),
)


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def pinned_source_text(root: Path = ROOT) -> str:
    """Require exact reviewed Toda bytes modulo whole-file CRLF/LF handling."""
    data = (root / SOURCE).read_bytes()
    normalized = data.replace(b"\r\n", b"\n")
    if SOURCE_BLOB not in (
        git_blob_sha(data), git_blob_sha(normalized),
        git_blob_sha(normalized.replace(b"\n", b"\r\n")),
    ):
        raise ValueError("Toda source bytes differ from reviewed GitHub blob")
    text = normalized.decode("utf-8-sig")
    if any(text.count(boundary) != 1 for boundary in (PROP58, EQ510, PROP59)):
        raise ValueError("Prior-source anchors are missing or ambiguous")
    i58, i510, i59 = (text.index(boundary) for boundary in (PROP58, EQ510, PROP59))
    if not (i58 < i510 < i59):
        raise ValueError("Printed prior-source order changed")
    end58 = text.find(r"\end{proposition}", i58)
    end510 = text.find(r"\end{equation}", i510)
    if end58 < 0 or end510 < 0 or not (end58 < i510 < end510 < i59):
        raise ValueError("Printed prior-source boundaries changed")
    if text[i58:end58].count(CODOMAIN_CLAUSE) != 1:
        raise ValueError("Printed finite cyclic codomain clause changed")
    if text[i510:end510].count(IMAGE_CLAUSE) != 1:
        raise ValueError("Printed lower Delta generator image clause changed")
    return text


def reviewed_source_positions(manifest: Path = DEFAULT_MANIFEST) -> tuple[int, int]:
    """Require exact source IDs; no hand-assigned order or new target citation."""
    positions, rows, _manifest = _load_manifest_reference_order(manifest)
    selected: list[int] = []
    for locator, ref_id, source_id, _kind in MANIFEST_ROWS:
        matches = rows.get(ref_id, ())
        if (len(matches) != 1
                or matches[0].get("statement_id") != source_id
                or matches[0].get("locator") != locator):
            raise ValueError("Reviewed prior citation ID changed: " + locator)
        position = positions.get(ref_id)
        if type(position) is not int or position <= 0:
            raise ValueError("Prior-source publication position not reviewed")
        selected.append(position)
    if selected[0] >= selected[1]:
        raise ValueError("Prior-source publication positions reversed")
    return selected[0], selected[1]


def checked_prior_statements(root: Path = ROOT) -> tuple[Relation, TodaDeltaImageUpToSignStatement]:
    """Transcribe printed prior claims with exact, checked structural generator."""
    pinned_source_text(root)
    domain = TodaPrimaryGroup(11, 11)
    codomain = TodaPrimaryGroup(9, 5)
    stored = exact_prior_database_result(
        5, 4, csv_path=root / "data" / "sphere.csv",
        generator_csv=root / "data" / "HyoujiGen.csv",
    )
    if (type(stored) is not Relation
            or stored.relation_type is not RelationType.EQUALITY
            or stored.lhs != codomain
            or type(stored.rhs) is not FiniteCyclicGroup
            or stored.rhs.order != 2
            or type(stored.rhs.generator) is not Composition
            or not stored.rhs.generator.is_type_compatible()):
        raise ValueError("Structured pi_9^5 presentation differs from the printed source")
    expected = structured_generator_from_ids(
        ids=(4, 2), start_dimension=5,
        generator_csv=root / "data" / "HyoujiGen.csv",
    )
    if (expected is None or stored.rhs.generator != expected):
        raise ValueError("Structured nu_5 eta_8 generator mismatches the adopted source")
    generator = HomotopyElement(
        name="ι_11", dimension=11, source=11, target=11,
        generator=GeneratorSymbol(family="ι", index=11),
    )
    lower = TodaDeltaMap(domain, codomain)
    image = TodaDeltaImageUpToSignStatement(
        map=lower, element=generator, positive_value=stored.rhs.generator,
    )
    return stored, image


def build_cited_lower_delta_sources(
    root: Path = ROOT, manifest: Path = DEFAULT_MANIFEST,
) -> RegistryBridgeResult:
    """Register exactly two earlier facts; no generated goal or inference rule."""
    positions = reviewed_source_positions(manifest)
    group, image = checked_prior_statements(root)
    registry = UnifiedStatementRegistry()
    links: list[ProofStepLink] = []
    records: list[MigrationRecord] = []
    for (locator, reference_id, source_id, kind), position, claim in zip(
        MANIFEST_ROWS, positions, (group, image)
    ):
        assertion_id = "toda:174:r3r7r34:prior:" + reference_id
        registry.add_reference(LiteratureEntry(
            reference_id=reference_id,
            kind=kind,
            locator=locator,
            source_id=source_id,
            publication_position=position,
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=reference_id,
            kind=AssertionKind.STATEMENT,
            content=claim,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope=("prior source only", "not Proposition 5.9 conclusion"),
        ))
        links.append(ProofStepLink(assertion_id=assertion_id, step=ProofStep(
            conclusion=claim,
            premises=(),
            rule=ProofRule.GIVEN,
            note="Adopted Toda transcription; original edition unverified",
            inference_rule=InferenceRule(
                name="Cited prior Toda " + locator,
                literature_reference=LiteratureReference(
                    label="Toda " + locator, locator=locator,
                ),
            ),
        )))
        records.append(MigrationRecord(
            source="phase174_r3_r7_r34",
            source_key=source_id,
            assertion_id=assertion_id,
            status=MigrationStatus.STRUCTURED,
            detail="Checked earlier source claim; no Proposition 5.9 conclusion admitted",
        ))
    return RegistryBridgeResult(registry, tuple(records), tuple(links))
