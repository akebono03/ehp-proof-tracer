"""R12-R26: evidence-anchored generic quotient backward candidates.

This is a proposal provider, not a new theorem or a certified map fact.
Only a screened fixed eta-family definition authorizes this eta-family candidate.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r2_quotient_rules import (
    CyclicStructureStatement, QuotientIsomorphismStatement,
    infinite_cyclic_quotient_structure_inference_rule,
)
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r3_recursive_search import GoalExpansion
from proof import ProofRule
from toda_rules import toda_eta_family_definition_statement
from unified_statement_registry import AssertionOrigin


def cited_eta_source_count(bridge: object) -> int:
    """Count exactly matched, cited, fixed source leaves in the screened bridge."""
    matches = 0
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and step.conclusion == assertion.content
                and isinstance(step.conclusion, TodaEtaFamilyGeneralDefinition)):
            matches += 1
    return matches


def _same_eta_generator_name(element: object, canonical: HomotopyElement) -> bool:
    """Allow standard Unicode subscript and TeX-style underscore names only."""
    if not isinstance(element, HomotopyElement):
        return False
    if (element.dimension != canonical.dimension
            or element.source != canonical.source
            or element.target != canonical.target
            or element.generator != canonical.generator):
        return False
    n = canonical.generator.index
    subscripts = str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    return element.name in ("η" + subscripts, "η_" + str(n))


def expand_cited_eta_quotient(goal: object, source_count: int) -> tuple[GoalExpansion, ...]:
    """Reverse the EXISTING quotient rule using a cited eta-family map candidate.

    A candidate is not a ProofStep. All quotient and source-structure subgoals
    must be proved independently before the ordinary rule can fire.
    """
    if source_count != 1 or not isinstance(goal, CyclicStructureStatement):
        return ()
    target = goal.group
    if not isinstance(target, TodaPrimaryGroup):
        return ()
    n = target.sphere_dimension
    if (type(n) is not int or n < 3 or target.group_dimension != n + 1
            or type(goal.order) is not int or goal.order < 1):
        return ()
    source_eta = toda_eta_family_definition_statement(n - 1).element
    target_eta = toda_eta_family_definition_statement(n).element
    if not _same_eta_generator_name(goal.generator, target_eta):
        return ()
    domain = TodaPrimaryGroup(n, n - 1)
    mapping = TodaSuspensionMap(domain, target)
    quotient = QuotientIsomorphismStatement(
        mapping, domain, target, source_eta, goal.generator, goal.order,
    )
    source_structure = CyclicStructureStatement(domain, source_eta, None)
    return (GoalExpansion(infinite_cyclic_quotient_structure_inference_rule(),
                          (quotient, source_structure)),)


def build_cited_eta_quotient_provider(bridge: object):
    count = cited_eta_source_count(bridge)
    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        return expand_cited_eta_quotient(goal, count)
    return expand
