"""Two independently pinned Toda source statements, never a pi_9^5 leaf.

(5.8) is cited as a signed Delta image. Proposition 2.5 is cited as a
universal conditional composition law. Both are adopted Japanese TeX
transcriptions; the original publication has not been independently checked.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement, Multiple, Sum, Suspension
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
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

PACKAGE = "phase175_r4r10_cited_58_prop25_public"
ROOT = Path(__file__).resolve().parents[1]
CHAPTER_2 = "sources/toda/Toda_02_2.tex"
CHAPTER_5 = "sources/toda/Toda_05_2.tex"
CHAPTER_2_BLOB = "ed3667788805a429140dedf5d183736e43e0f2c3"
CHAPTER_5_BLOB = "579661138928499ba04a51327f686d9b971b5314"
EQUATION_REFERENCE_ID = "toda:(5.8)"
PROPOSITION_REFERENCE_ID = "toda:Proposition 2.5"
EQUATION_ASSERTION_ID = "toda:175:r4r10:equation58"
PROPOSITION_ASSERTION_ID = "toda:175:r4r10:proposition25"


@dataclass(frozen=True)
class CitedToda58SignedDelta:
    """The typed, signed *published premise*, not an inferred group result."""

    statement: TodaDeltaImageUpToSignStatement
    locator: str = "(5.8)"


@dataclass(frozen=True)
class CitedTodaProp25:
    """Source identity of the universal conditional Delta composition law."""

    locator: str = "Proposition 2.5"


def git_blob_sha(value: bytes) -> str:
    return sha1(b"blob " + str(len(value)).encode("ascii") + b"\x00" + value).hexdigest()


def vetted_source(path: Path, expected_blob: str) -> str:
    data = path.read_bytes()
    normalized = data.replace(b"\r\n", b"\n")
    choices = (data, normalized, normalized.replace(b"\n", b"\r\n"))
    if not any(git_blob_sha(value) == expected_blob for value in choices):
        raise ValueError("R4R10_SOURCE_BLOB_DRIFT: " + str(path))
    return normalized.decode("utf-8-sig")


def source_positions(root: Path = ROOT, manifest: Path = DEFAULT_MANIFEST) -> dict[str, int]:
    """Verify both complete source blocks and the recorded source order."""
    if not isinstance(root, Path) or not isinstance(manifest, Path):
        raise TypeError("root and manifest must be pathlib.Path")
    ch2 = vetted_source(root / CHAPTER_2, CHAPTER_2_BLOB)
    ch5 = vetted_source(root / CHAPTER_5, CHAPTER_5_BLOB)
    label25 = r"\begin{proposition}\label{prop:2.5}"
    label58 = r"\begin{equation}\label{eq:5.8}"
    if ch2.count(label25) != 1 or ch5.count(label58) != 1:
        raise ValueError("R4R10_TODA_ANCHOR_NOT_UNIQUE")
    prop25 = ch2.split(label25, 1)[1].split(r"\end{proposition}", 1)[0]
    eq58 = ch5.split(label58, 1)[1].split(r"\end{equation}", 1)[0]
    if not all(part in prop25 for part in (
        r"\alpha\in\pi_{i+1}(S^{2m+1})",
        r"\beta\in \pi_{j-1}(S^{i-1})",
        r"\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)",
        r"j<3m-1", r"2\)-primary", "等号",
    )):
        raise ValueError("R4R10_PROP25_SOURCE_CHANGED")
    if r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" not in eq58:
        raise ValueError("R4R10_EQ58_SOURCE_CHANGED")
    if ch5.index(label58) >= ch5.index(r"\begin{proposition}\label{prop:5.8}"):
        raise ValueError("R4R10_EQ58_SOURCE_ORDER_CHANGED")
    positions, _, _ = _load_manifest_reference_order(manifest)
    expected = (
        positions.get(PROPOSITION_REFERENCE_ID),
        positions.get(EQUATION_REFERENCE_ID),
        positions.get("toda:Proposition 5.8"),
    )
    if (not all(type(v) is int and v > 0 for v in expected)
            or not (expected[0] < expected[1] < expected[2])):
        raise ValueError("R4R10_SOURCE_POSITION_INVALID")
    return {PROPOSITION_REFERENCE_ID: expected[0], EQUATION_REFERENCE_ID: expected[1]}


def canonical_toda58() -> TodaDeltaImageUpToSignStatement:
    """Literal typed interpretation of (5.8), retaining the unresolved ±."""
    iota9 = HomotopyElement("ι₉", 9, 9, 9, GeneratorSymbol("ι", index=9))
    nu4 = HomotopyElement("ν₄", 4, 7, 4, GeneratorSymbol("ν", index=4))
    nu_prime = HomotopyElement(
        "ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"),
    )
    return TodaDeltaImageUpToSignStatement(
        map=TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(7, 4)),
        element=iota9,
        positive_value=Sum(Multiple(2, nu4), Multiple(-1, Suspension(nu_prime))),
    )


def build_cited_58_prop25_sources(
    root: Path = ROOT, manifest: Path = DEFAULT_MANIFEST,
) -> RegistryBridgeResult:
    positions = source_positions(root, manifest)
    eq = CitedToda58SignedDelta(canonical_toda58())
    prop = CitedTodaProp25()
    registry = UnifiedStatementRegistry()
    links = []
    for ref_id, assertion_id, kind, statement in (
        (EQUATION_REFERENCE_ID, EQUATION_ASSERTION_ID, ReferenceKind.EQUATION, eq),
        (PROPOSITION_REFERENCE_ID, PROPOSITION_ASSERTION_ID, ReferenceKind.PROPOSITION, prop),
    ):
        locator = statement.locator
        registry.add_reference(LiteratureEntry(
            reference_id=ref_id,
            kind=kind,
            locator=locator,
            source_id=(CHAPTER_5 if kind is ReferenceKind.EQUATION else CHAPTER_2)
            + " (adopted Japanese TeX; original edition unverified)",
            publication_position=positions[ref_id],
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=ref_id,
            kind=AssertionKind.STATEMENT,
            content=statement,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope="source formula only; not pi_9^5 group result",
        ))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=statement,
            premises=(),
            rule=ProofRule.GIVEN,
            inference_rule=InferenceRule(
                name="Cited Toda " + locator,
                literature_reference=LiteratureReference(
                    label="Toda " + locator, locator=locator,
                ),
            ),
        )))
    return RegistryBridgeResult(registry, (), tuple(links))
