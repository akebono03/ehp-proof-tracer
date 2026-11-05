"""Phase 174 R3-R6: source-verified universal Toda (4.8) and (5.5).

The only new GIVENs are the two source-level universal formulae.  The
index-two injection and each doubled generator relation require INFERENCE
ProofSteps from the existing canonical backward-search engine.  Neither
this module nor its caller registers a special pi_8^5 result.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import FiniteCyclicGroup
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase165_r3_recursive_search import GoalExpansion
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    StableFamilyMemberDefinition,
    canonical_member,
)
from phase174_r3_r5_finite_cyclic_extension.rule import Toda48UniversalConditionalStatement
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
)
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
SOURCES = (
    ("(4.8)", "04", "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7"),
    ("(5.5)", "05", "579661138928499ba04a51327f686d9b971b5314"),
)


@dataclass(frozen=True)
class Toda55UniversalDoubleStatement:
    """The cited general equation 2 nu_n = E^(n-3) nu-prime for n>=5."""

    minimum_index: int = 5
    coefficient: int = 2
    exponent_shift: int = 3
    family: str = "ν"
    base_decoration: str = "′"


def _git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def verify_extension_texts(
    root: Path = ROOT,
    manifest: Path = DEFAULT_MANIFEST,
) -> tuple[tuple[str, int], ...]:
    """Fail closed on modified source bytes, missing hypotheses and source order.

    CRLF checkouts are accepted only when their normalized content is exactly
    the reviewed Git blob.  A TeX snippet alone is not enough evidence.
    """
    if not isinstance(root, Path) or not isinstance(manifest, Path):
        raise TypeError("root and manifest must be pathlib.Path")
    text_by_locator: dict[str, str] = {}
    for locator, chapter, expected in SOURCES:
        path = root / "sources" / "toda" / f"Toda_{chapter}_2.tex"
        data = path.read_bytes()
        normalized = data.replace(b"\r\n", b"\n")
        candidates = (data, normalized, normalized.replace(b"\n", b"\r\n"))
        if not any(_git_blob_sha(value) == expected for value in candidates):
            raise ValueError(f"Unreviewed Toda source blob for {locator}")
        text_by_locator[locator] = normalized.decode("utf-8-sig")
    chapter4 = text_by_locator["(4.8)"]
    chapter5 = text_by_locator["(5.5)"]
    start48 = r"\begin{equation}\label{4.8}"
    end = r"\end{equation}"
    if chapter4.count(start48) != 1:
        raise ValueError("Toda (4.8) source anchor is not unique")
    block48 = chapter4.split(start48, 1)[1].split(end, 1)[0]
    for fragment in (
        r"n \ \text{を偶数とする.",
        r"\Delta(\iota_{2n-1})=0",
        r"E^{2}:\pit{2n-2}{\,n-1}\to\pit{2n}{\,n+1}",
        r"\ \text{は単射で, }",
        r"\pit{2n}{\,n+1}/E^{2}\pit{2n-2}{\,n-1}\cong\mathbb{Z}_2",
    ):
        if fragment not in block48:
            raise ValueError("Toda (4.8) conditional clause missing: " + fragment)
    start55 = r"\begin{equation}\label{eq:5.5}"
    if chapter5.count(start55) != 1:
        raise ValueError("Toda (5.5) source anchor is not unique")
    position55 = chapter5.index(start55)
    block55 = chapter5.split(start55, 1)[1].split(end, 1)[0]
    if (
        r"n\ge5\ \text{に対して, } 2\nu_n=E^{\,n-3}\nu'" not in block55
        or r"\nu_n:=E^{\,n-4}\nu_{4}" not in chapter5[:position55]
        or r"\begin{proposition}\label{prop:5.6}" not in chapter5[position55:]
    ):
        raise ValueError("Toda (5.5) general-double relation or source order invalid")
    positions, _, _ = _load_manifest_reference_order(manifest)
    found = (
        positions.get("toda:(4.8)"),
        positions.get("toda:(5.5)"),
        positions.get("toda:Proposition 5.6"),
    )
    if found != (7500, 8600, 8800):
        raise ValueError("Reviewed Toda publication-order boundary changed")
    return (("(4.8)", found[0]), ("(5.5)", found[1]))


def build_cited_extension_sources(
    root: Path = ROOT,
    manifest: Path = DEFAULT_MANIFEST,
) -> RegistryBridgeResult:
    """Register two universal source statements; no special group or relation."""
    positions = dict(verify_extension_texts(root, manifest))
    registry = UnifiedStatementRegistry()
    links = []
    records = []
    for locator, chapter, _ in SOURCES:
        source = (
            Toda48UniversalConditionalStatement()
            if locator == "(4.8)" else Toda55UniversalDoubleStatement()
        )
        ref_id = "toda:" + locator
        assertion_id = "toda:174:r3r6:universal:" + locator
        registry.add_reference(LiteratureEntry(
            reference_id=ref_id,
            kind=ReferenceKind.EQUATION,
            locator=locator,
            source_id=(f"sources/toda/Toda_{chapter}_2.tex "
                       "(adopted transcription; original edition unverified)"),
            publication_position=positions[locator],
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=ref_id,
            kind=AssertionKind.STATEMENT,
            content=source,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope=("universal formula only", "no direct group conclusion"),
        ))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=source,
            premises=(),
            rule=ProofRule.GIVEN,
            inference_rule=InferenceRule(
                name="Cited universal Toda " + locator,
                literature_reference=LiteratureReference(
                    label="Toda " + locator, locator=locator,
                ),
            ),
        )))
        records.append(MigrationRecord(
            "phase174_r3_r6", locator, assertion_id, MigrationStatus.STRUCTURED,
            "Source-blob-verified universal formula; no concrete goal asserted",
        ))
    return RegistryBridgeResult(registry, tuple(records), tuple(links))


def _cited_nu_member(goal: object) -> StableFamilyMemberDefinition | None:
    """A requested doubled relation must carry the complete typed nu identity."""
    if (
        not isinstance(goal, Relation)
        or goal.relation_type is not RelationType.EQUALITY
        or not isinstance(goal.lhs, Multiple)
        or type(goal.lhs.coefficient) is not int
        or goal.lhs.coefficient != 2
        or not isinstance(goal.lhs.expression, HomotopyElement)
        or not isinstance(goal.rhs, IteratedSuspension)
        or type(goal.rhs.exponent) is not int
        or not isinstance(goal.rhs.expression, HomotopyElement)
    ):
        return None
    target = goal.lhs.expression
    earlier = goal.rhs.expression
    n = target.dimension
    if (
        type(n) is not int or n < 5
        or goal.rhs.exponent != n - 3
        or target.source != n + 3 or target.target != n
        or target.generator != GeneratorSymbol("ν", index=n)
        or earlier.dimension != 3 or earlier.source != 6 or earlier.target != 3
        or goal.rhs.source != target.source
        or goal.rhs.target != target.target
    ):
        return None
    # Convert the registered HyoujiGen spelling (\nu') to the cited ν′
    # source identity through the existing conservative, typed ID resolver.
    # This tests symbol identity only; it does not assert any element order.
    from phase168_r2_8_3_generator_identity.identity import (
        same_registered_group_presentation,
    )
    nu_prime_cited = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol("ν", decoration="′"),
    )
    if not same_registered_group_presentation(
        FiniteCyclicGroup(4, earlier), FiniteCyclicGroup(4, nu_prime_cited),
    ):
        return None
    source = CitedStableFamilyDefinition(family_id=4, minimum_n=4, stem=3)
    member = canonical_member(source, n)
    if member is None or (
        member.element.dimension != n
        or member.element.source != target.source
        or member.element.target != target.target
        or member.element.generator != target.generator
    ):
        return None
    return member


def cited_toda55_double_inference_rule(
    goal: Relation,
) -> InferenceRule:
    """Conclude the concrete double only from cited (5.5) and a family member."""
    member = _cited_nu_member(goal)
    if member is None:
        raise ValueError("not a typed instance of the universal Toda (5.5)")
    theorem = Toda55UniversalDoubleStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.GIVEN
            and premises[0].conclusion == member
            and type(premises[1].conclusion) is Toda55UniversalDoubleStatement
            and premises[1].conclusion == theorem
            and _cited_nu_member(goal) == member
        )

    return InferenceRule(
        name="specialize cited Toda (5.5) doubled nu-family identity",
        description=(
            "The source equation for every n>=5 is specialized to the typed "
            "nu-family member from an independently cited Definition."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=StableFamilyMemberDefinition,
                statement_pattern=member,
            ),
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Toda55UniversalDoubleStatement,
                statement_pattern=theorem,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
        literature_reference=LiteratureReference(
            label="Toda (5.5)", locator="(5.5)",
        ),
    )


def expand_cited_toda55_double(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Backwards proposal only; screen the general equation and family source."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a screened tuple")
    member = _cited_nu_member(goal)
    if (
        member is None
        or available.count(Toda55UniversalDoubleStatement()) != 1
        or available.count(member.source) != 1
    ):
        return ()
    return (GoalExpansion(
        cited_toda55_double_inference_rule(goal),
        (member, Toda55UniversalDoubleStatement()),
    ),)
