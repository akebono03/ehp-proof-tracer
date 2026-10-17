"""Source-checked universal eta-family definition and typed specialization."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep
from toda_rules import TodaEtaFamilyDefinitionStatement, toda_eta_family_definition_statement
from unified_statement_registry import (AssertionEntry, AssertionKind, AssertionOrigin,
    LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry)

REFERENCE_ID = "adopted:reference:toda5:eta_family_definition"
ASSERTION_ID = "adopted:assertion:toda5:eta_family_definition"
SOURCE_CLAUSE = r"\(n\ge2\) に対し, \eta_n=E^{\,n-2}\eta_2"

@dataclass(frozen=True)
class TodaEtaFamilyGeneralDefinition:
    """General notation: eta_n=E^(n-2)eta_2 for every integer n>=2."""
    lower_bound: int = 2


def build_cited_eta_family_definition(source_path: Path) -> RegistryBridgeResult:
    path = Path(source_path)
    data = path.read_text(encoding="utf-8-sig")
    # Verify full content, not a guessed citation inferred from the target.
    required = (r"\(n\ge2\) に対し", r"\eta_n=E^{\,n-2}\eta_2")
    if not all(part in data for part in required):
        raise ValueError("Toda chapter V general eta-family clause not verified")
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID, kind=ReferenceKind.DEFINITION,
        locator="Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation",
        source_id="sources/toda/Toda_05_2.tex (adopted transcription, original edition unverified)",
    ))
    general = TodaEtaFamilyGeneralDefinition()
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID, reference_id=REFERENCE_ID,
        kind=AssertionKind.DEFINITION, content=general,
        origin=AssertionOrigin.FIXED_STATEMENT, defined_symbol="eta_n", scope="n>=2",
    ))
    step = ProofStep(general, (), ProofRule.GIVEN, inference_rule=InferenceRule(
        name="Toda chapter V eta-family notation",
        literature_reference=LiteratureReference(label="Toda Chapter V eta notation", locator="Chapter V, i)"),
    ))
    return RegistryBridgeResult(registry, (), (ProofStepLink(ASSERTION_ID, step=step),))


def eta_definition_specialization_rule(goal: TodaEtaFamilyDefinitionStatement) -> InferenceRule:
    if not isinstance(goal, TodaEtaFamilyDefinitionStatement):
        raise TypeError("eta-family typed definition required")
    n = goal.index
    if type(n) is not int or n < 2 or goal != toda_eta_family_definition_statement(n):
        raise ValueError("invalid eta-family specialization")
    return InferenceRule(
        name="specialize cited eta-family general definition",
        premise_patterns=(PremisePattern(statement_type=TodaEtaFamilyGeneralDefinition),),
        match_guard=lambda premises, bindings: len(premises)==1 and premises[0].conclusion==TodaEtaFamilyGeneralDefinition(),
        conclusion_pattern=goal,
    )


def expand_cited_eta_definition(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    if not isinstance(goal, TodaEtaFamilyDefinitionStatement):
        return ()
    if available.count(TodaEtaFamilyGeneralDefinition()) != 1:
        return ()
    try:
        rule = eta_definition_specialization_rule(goal)
    except ValueError:
        return ()
    return (GoalExpansion(rule, (TodaEtaFamilyGeneralDefinition(),)),)
