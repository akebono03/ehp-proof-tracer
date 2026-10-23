"""Phase 165 R12-R15: cite Toda (5.1) below-diagonal zero schema.

No goal-specific zero theorem or unreferenced axiom is created. The sole
universal GIVEN is the exact adopted Toda (5.1) clause, and each concrete
zero-group statement is obtained by INFERENCE from that GIVEN.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion, RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r12_r12_ehp_consequences import proof_has_general_prop42_ancestor
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

GENERAL_ASSERTION_ID = "adopted:assertion:toda51:below_diagonal_zero"
GENERAL_REFERENCE_ID = "adopted:reference:toda51:below_diagonal_zero"
EXPECTED_CLAUSE = r"\pi^{n}_{i}=0\ (i<n)"


@dataclass(frozen=True)
class Toda51BelowDiagonalZeroStatement:
    """Toda (5.1): pi_i^n vanishes for 0 <= i < n."""
    locator: str = "(5.1)"


def build_adopted_toda51_zero_reference(tex_path: Path) -> RegistryBridgeResult:
    """Register exactly one universal zero assertion from the adopted source."""
    text = Path(tex_path).read_text(encoding="utf8")
    if (EXPECTED_CLAUSE not in text
            or r"\pi^{1}_{i}=0\ (i>1)" not in text
            or r"\begin{equation}\label{5.1}" not in text):
        raise ValueError("Toda (5.1) zero clause missing or changed")
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=GENERAL_REFERENCE_ID,
        kind=ReferenceKind.EQUATION,
        locator="(5.1)",
        source_id="Toda adopted Japanese TeX:(5.1) (original edition unverified)",
    ))
    statement = Toda51BelowDiagonalZeroStatement()
    registry.add_assertion(AssertionEntry(
        assertion_id=GENERAL_ASSERTION_ID,
        reference_id=GENERAL_REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=statement,
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    step = ProofStep(
        conclusion=statement,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda (5.1) universal below-diagonal vanishing",
            literature_reference=LiteratureReference(label="Toda (5.1)", locator="(5.1)"),
        ),
    )
    # Reuse the existing scalar-specialization rule for the circle clause.
    # Its i > 1 domain is checked in specialize_typed_statement().
    from expression import ScalarSymbol
    i = ScalarSymbol("i")
    circle_source = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(i, 1))
    circle_id = "adopted:assertion:toda51:circle_higher_zero"
    registry.add_assertion(AssertionEntry(
        assertion_id=circle_id,
        reference_id=GENERAL_REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=circle_source,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("i>1",),
    ))
    circle_step = ProofStep(
        conclusion=circle_source, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda (5.1) general circle higher vanishing",
            literature_reference=LiteratureReference(label="Toda (5.1)", locator="(5.1)"),
        ),
    )
    return RegistryBridgeResult(registry, (), (
        ProofStepLink(GENERAL_ASSERTION_ID, step=step),
        ProofStepLink(circle_id, step=circle_step),
    ))


def below_diagonal_zero_specialization_inference_rule(goal: TodaPrimaryGroupZeroStatement) -> InferenceRule:
    """Specialize the one cited general theorem to the requested indices."""
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        raise TypeError("zero-group goal required")
    group = goal.group
    i, n = group.group_dimension, group.sphere_dimension
    if type(i) is not int or type(n) is not int or i < 0 or n < 2 or i >= n:
        raise ValueError("indices must satisfy 0 <= i < n and n >= 2")
    def guard(premises, bindings):
        return (len(premises) == 1
                and isinstance(premises[0].conclusion, Toda51BelowDiagonalZeroStatement))
    return InferenceRule(
        name="Toda (5.1) general below-diagonal zero specialization",
        premise_patterns=(PremisePattern(statement_type=Toda51BelowDiagonalZeroStatement),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_toda51_zero(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Only expand when the citation-screened universal statement is present."""
    if not isinstance(available, tuple):
        raise TypeError("available must be tuple")
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        return ()
    sources = tuple(x for x in available if isinstance(x, Toda51BelowDiagonalZeroStatement))
    if len(sources) != 1:
        return ()
    try:
        rule = below_diagonal_zero_specialization_inference_rule(goal)
    except ValueError:
        return ()
    return (GoalExpansion(rule, (sources[0],)),)


def proof_has_toda51_zero_ancestor(step: ProofStep) -> bool:
    """Check that an actual GIVEN source occurs in the derivation tree."""
    visited: set[int] = set()
    def visit(node: ProofStep) -> bool:
        if id(node) in visited:
            return False
        visited.add(id(node))
        if node.rule is ProofRule.GIVEN and isinstance(node.conclusion, Toda51BelowDiagonalZeroStatement):
            return True
        return any(visit(parent) for parent in node.premises)
    return visit(step)


@dataclass(frozen=True)
class SurjectivityClosureResult:
    goal: MapSurjective
    proof: ProofStep | None
    status: str
    blocker: str | None


def prove_surjectivity_in_screened_context(
    goal: MapSurjective,
    bridge: RegistryBridgeResult,
    *,
    citing_assertion_id: str,
    proof_target: object,
) -> SurjectivityClosureResult:
    """Resolve surjectivity with both Prop 4.2 and Toda (5.1) provenance."""
    from homotopy_groups import TodaSuspensionMap
    from phase165_r52_r9_shared_math import shared_expansion_provider
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaSuspensionMap):
        raise TypeError("suspension-surjectivity goal required")
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("registry bridge required")
    screened = screen_shared_proof_context(
        bridge, goal=proof_target, citing_assertion_id=citing_assertion_id,
    )
    screened = prefer_universal_prop42_derivation(screened)
    expand = shared_expansion_provider(screened, proof_target=proof_target)
    try:
        proof = reconstruct_registered_goal(
            goal, screened, citing_assertion_id=citing_assertion_id,
            expansion_provider=expand, lookup_mode="typed_reference",
        )
    except RegisteredGoalUnresolved as exc:
        return SurjectivityClosureResult(goal, None, "UNRESOLVED", str(exc))
    if proof.conclusion != goal or proof.rule is not ProofRule.INFERENCE:
        return SurjectivityClosureResult(goal, None, "INVALID_ROOT", "unexpected conclusion")
    if not proof_has_general_prop42_ancestor(proof):
        return SurjectivityClosureResult(goal, None, "MISSING_PROP42", "Proposition 4.2 ancestry missing")
    if not proof_has_toda51_zero_ancestor(proof):
        return SurjectivityClosureResult(goal, None, "MISSING_TODA51", "Toda (5.1) ancestry missing")
    return SurjectivityClosureResult(goal, proof, "CERTIFIED", None)
