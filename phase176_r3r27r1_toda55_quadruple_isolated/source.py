"""Source-verified isolated Toda (5.5) quadruple nu relation; no public wiring."""
from __future__ import annotations

from dataclasses import dataclass

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple
from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    StableFamilyMemberDefinition,
    canonical_member,
)
from phase174_r3_r6_source_extension.source import ROOT, verify_extension_texts
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep, Relation, RelationType
from toda_rules import toda_eta_family_definition_statement
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

REFERENCE_ID = "toda:(5.5):quadruple_nu"
ASSERTION_ID = "toda:176:r3r27r1:universal:quadruple_nu"
RULE_NAME = "specialize cited Toda (5.5) quadruple nu-family identity"


@dataclass(frozen=True)
class Toda55UniversalQuadrupleStatement:
    """Source fact: 4 nu_n = eta_n eta_(n+1) eta_(n+2), n>=5."""
    minimum_index: int = 5
    coefficient: int = 4
    family: str = "ν"


def build_cited_toda55_quadruple_source() -> RegistryBridgeResult:
    """Check the reviewed source bytes and the *second* (5.5) clause."""
    positions = dict(verify_extension_texts())
    text = (ROOT / "sources" / "toda" / "Toda_05_2.tex").read_text(encoding="utf-8-sig")
    anchor = r"\begin{equation}\label{eq:5.5}"
    if text.count(anchor) != 1:
        raise ValueError("Toda (5.5) anchor must be unique")
    body = text.split(anchor, 1)[1].split(r"\end{equation}", 1)[0]
    if (r"n\ge5\ \text{に対して, } 2\nu_n=E^{\,n-3}\nu'" not in body
            or r"4\nu_{n}=\eta_n^{3}" not in body
            or r"4\nu=\eta^{3}" not in body):
        raise ValueError("Toda (5.5) quadruple clause missing")
    definition = r"\eta^{3}_{n}:=\eta_{n}\circ\eta_{n+1}\circ\eta_{n+2}"
    if definition not in text[:text.index(anchor)]:
        raise ValueError("eta-cube definition is not cited before Toda (5.5)")
    statement = Toda55UniversalQuadrupleStatement()
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.EQUATION,
        locator="(5.5)",
        source_id="sources/toda/Toda_05_2.tex (adopted transcription; original edition unverified)",
        publication_position=positions["(5.5)"],
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=statement,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("quadruple nu-family relation for n>=5 only",),
    ))
    step = ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Cited universal Toda (5.5) quadruple relation",
            literature_reference=LiteratureReference(label="Toda (5.5)", locator="(5.5)"),
        ),
    )
    return RegistryBridgeResult(
        registry,
        (MigrationRecord("phase176_r3r27r1", "(5.5):quadruple_nu",
                         ASSERTION_ID, MigrationStatus.STRUCTURED,
                         "source-blob-verified universal quadruple relation"),),
        (ProofStepLink(ASSERTION_ID, step=step),),
    )


def canonical_quadruple_goal(n: int) -> Relation | None:
    """A source-based schematic specialization; NEVER a proof certificate."""
    if type(n) is not int or n < 5:
        return None
    family = CitedStableFamilyDefinition(family_id=4, minimum_n=4, stem=3)
    member = canonical_member(family, n)
    if member is None:
        return None
    eta_elements = tuple(toda_eta_family_definition_statement(j).element
                         for j in (n, n + 1, n + 2))
    if not all(isinstance(e, HomotopyElement) and e.generator == GeneratorSymbol("η", index=j)
               and e.source == j + 1 and e.target == j for j, e in zip((n, n+1, n+2), eta_elements)):
        return None
    eta_cube = Composition(eta_elements[0], Composition(eta_elements[1], eta_elements[2]))
    if eta_cube.left.source != eta_cube.right.left.target or not eta_cube.right.is_type_compatible():
        return None
    if eta_elements[2].source != member.element.source or eta_elements[0].target != member.element.target:
        return None
    return Relation(Multiple(4, member.element), eta_cube, RelationType.EQUALITY)


def quadruple_inputs(goal: object) -> tuple[StableFamilyMemberDefinition, Toda55UniversalQuadrupleStatement, TodaEtaFamilyGeneralDefinition] | None:
    if not isinstance(goal, Relation) or not isinstance(goal.lhs, Multiple):
        return None
    nu = goal.lhs.expression
    if not isinstance(nu, HomotopyElement) or type(nu.dimension) is not int:
        return None
    if canonical_quadruple_goal(nu.dimension) != goal:
        return None
    family = CitedStableFamilyDefinition(family_id=4, minimum_n=4, stem=3)
    member = canonical_member(family, nu.dimension)
    if member is None:
        return None
    return member, Toda55UniversalQuadrupleStatement(), TodaEtaFamilyGeneralDefinition()


def cited_quadruple_rule(goal: Relation) -> InferenceRule:
    inputs = quadruple_inputs(goal)
    if inputs is None:
        raise ValueError("not a cited typed Toda (5.5) quadruple goal")

    def guard(premises, bindings):
        return (len(premises) == 3
                and premises[0].rule is ProofRule.INFERENCE
                and premises[1].rule is ProofRule.GIVEN
                and premises[2].rule is ProofRule.GIVEN
                and tuple(p.conclusion for p in premises) == inputs
                and quadruple_inputs(goal) == inputs)

    return InferenceRule(
        name=RULE_NAME,
        description="Specialize source-verified Toda (5.5) using separately proved ν-family member and cited η notation.",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=StableFamilyMemberDefinition, statement_pattern=inputs[0]),
            PremisePattern(proof_rule=ProofRule.GIVEN,
                           statement_type=Toda55UniversalQuadrupleStatement, statement_pattern=inputs[1]),
            PremisePattern(proof_rule=ProofRule.GIVEN,
                           statement_type=TodaEtaFamilyGeneralDefinition, statement_pattern=inputs[2]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
        literature_reference=LiteratureReference(label="Toda (5.5)", locator="(5.5)"),
    )


def expand_cited_quadruple(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Return a backward proof *candidate* only when BOTH citations were screened."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    inputs = quadruple_inputs(goal)
    if inputs is None:
        return ()
    if (available.count(inputs[0].source) != 1
            or available.count(inputs[1]) != 1
            or available.count(inputs[2]) != 1):
        return ()
    return (GoalExpansion(cited_quadruple_rule(goal), inputs),)
