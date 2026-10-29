"""Verified general right-Hopf formula and conservative typed derivations.

The registered general formula is a cited leaf, NOT a proof of any group.
Concrete formulas and Hopf-value substitutions must be INFERENCE steps.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from expression import Composition, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase165_r3_recursive_search import GoalExpansion
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

SOURCE_ID = "toda:tex:ch2:0009"
SOURCE_SHA256 = "5560fe950f06dea97bd152bc97dd29661576697a7d7e58b41c938f0b3e373146"
REFERENCE_ID = "toda:Proposition 2.2"
ASSERTION_ID = "toda:adopted:prop2.2:right_hopf_formula"
RIGHT_FORMULA = r"H(\alpha\circ E\beta)\ =\ H(\alpha)\circ E\beta"


@dataclass(frozen=True)
class TodaProp22RightFormula:
    """The universal formula H(alpha o E beta) = H(alpha) o E beta."""


def build_cited_prop22_right_reference(source_bridge: RegistryBridgeResult) -> RegistryBridgeResult:
    """Adopt the exact prior formula from the one reviewed archival source."""
    if not isinstance(source_bridge, RegistryBridgeResult):
        raise TypeError("source_bridge must be RegistryBridgeResult")
    candidates = tuple(
        assertion for assertion in source_bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
        and isinstance(assertion.content, dict)
        and assertion.content.get("source_statement_id") == SOURCE_ID
    )
    if len(candidates) != 1:
        raise ValueError("Proposition 2.2 must have exactly one archived source")
    source = candidates[0].content
    text = source.get("source_text")
    if (not isinstance(text, str)
            or source.get("source_sha256") != SOURCE_SHA256
            or sha256(text.encode("utf-8")).hexdigest() != SOURCE_SHA256
            or r"\begin{proposition}\label{prop:2.2}" not in text
            or RIGHT_FORMULA not in text
            or r"\end{proposition}" not in text):
        raise ValueError("archived Proposition 2.2 formula failed source verification")

    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.PROPOSITION,
        locator="Proposition 2.2",
        source_id=SOURCE_ID,
    ))
    general = TodaProp22RightFormula()
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=general,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("right composition formula only",),
    ))
    step = ProofStep(
        conclusion=general,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda Proposition 2.2 right-Hopf source",
            literature_reference=LiteratureReference(
                label="Toda Proposition 2.2", locator="Proposition 2.2",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry,
        (MigrationRecord(
            "phase171_r2h", SOURCE_ID, ASSERTION_ID,
            MigrationStatus.STRUCTURED,
            "adopted-source hash verified; original edition independently unverified",
        ),),
        (ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )


def _formula_parts(goal: object) -> tuple[HomotopyElement, HomotopyElement] | None:
    """Recognize only the literal right-formula shape with compatible degrees."""
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return None
    if not isinstance(goal.lhs, MapApplication) or goal.lhs.map != EHP_H_MAP:
        return None
    product = goal.lhs.expression
    if not isinstance(product, Composition):
        return None
    alpha, right = product.left, product.right
    if (not isinstance(alpha, HomotopyElement)
            or not isinstance(right, Suspension)
            or not isinstance(right.expression, HomotopyElement)
            or not product.is_type_compatible()):
        return None
    beta = right.expression
    if (type(alpha.dimension) is not int or type(beta.dimension) is not int
            or type(alpha.source) is not int or type(alpha.target) is not int
            or type(beta.source) is not int or type(beta.target) is not int
            or alpha.dimension != alpha.target or beta.dimension != beta.target
            or alpha.source != beta.target + 1):
        return None
    expected = Composition(MapApplication(EHP_H_MAP, alpha), right)
    return (alpha, beta) if goal.rhs == expected else None


def cited_prop22_right_specialization_rule(goal: Relation) -> InferenceRule:
    """Specialize the cited universal formula, never infer a citation from a name."""
    if _formula_parts(goal) is None:
        raise ValueError("goal is not a degree-compatible right-Hopf formula")

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].conclusion == TodaProp22RightFormula())

    return InferenceRule(
        name="specialize cited Toda Proposition 2.2 right formula",
        premise_patterns=(PremisePattern(statement_type=TodaProp22RightFormula),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def _combined_premises(goal: object, available: tuple[object, ...]) -> tuple[tuple[Relation, Relation], ...]:
    """Resolve only a screened H(alpha)=beta witness with beta the right factor."""
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)):
        return ()
    product = goal.lhs.expression
    if (not isinstance(product.right, Suspension)
            or not isinstance(product.right.expression, HomotopyElement)
            or not isinstance(product.left, HomotopyElement)):
        return ()
    alpha = product.left
    beta = product.right.expression
    formula = Relation(
        lhs=goal.lhs,
        rhs=Composition(MapApplication(EHP_H_MAP, alpha), product.right),
        relation_type=RelationType.EQUALITY,
    )
    if _formula_parts(formula) != (alpha, beta):
        return ()
    if goal.rhs != Composition(beta, product.right):
        return ()
    hopf = Relation(
        lhs=MapApplication(EHP_H_MAP, alpha),
        rhs=beta,
        relation_type=RelationType.EQUALITY,
    )
    return ((formula, hopf),) if available.count(hopf) == 1 else ()


def cited_prop22_hopf_substitution_rule(goal: Relation, formula: Relation, hopf: Relation) -> InferenceRule:
    """Apply the independently proved Hopf image to the proved right formula."""
    if _combined_premises(goal, (hopf,)) != ((formula, hopf),):
        raise ValueError("formula/Hopf premises are not the verified typed pair")

    def guard(premises, bindings):
        return (len(premises) == 2
                and premises[0].rule is ProofRule.INFERENCE
                and premises[0].conclusion == formula
                and premises[1].conclusion == hopf)

    return InferenceRule(
        name="substitute proved Hopf value into cited right formula",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation),
            PremisePattern(statement_type=Relation),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_prop22_right_formula(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Supply backward proposals only when the cited source survives screening."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if available.count(TodaProp22RightFormula()) != 1:
        return ()
    if _formula_parts(goal) is not None:
        return (GoalExpansion(
            cited_prop22_right_specialization_rule(goal),
            (TodaProp22RightFormula(),),
        ),)
    if not isinstance(goal, Relation):
        return ()
    options = []
    for formula, hopf in _combined_premises(goal, available):
        options.append(GoalExpansion(
            cited_prop22_hopf_substitution_rule(goal, formula, hopf),
            (formula, hopf),
        ))
    return tuple(options)
