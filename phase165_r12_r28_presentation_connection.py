"""Evidence-preserving backward connection for eta suspension presentations."""
from __future__ import annotations

from expression import HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r2_quotient_rules import HomomorphismPresentationStatement
from phase165_r12_r21_eta_generator_chain import _eta_pair
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern
from toda_rules import toda_eta_family_definition_statement


def _matching_eta_name(actual: object, expected: HomotopyElement) -> bool:
    if not isinstance(actual, HomotopyElement):
        return False
    if (actual.generator != expected.generator or actual.dimension != expected.dimension
            or actual.source != expected.source or actual.target != expected.target):
        return False
    index = expected.generator.index
    subscripts = str(index).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    return actual.name in ("η" + subscripts, "η_" + str(index))


def eta_presentation_from_suspension_rule(goal: HomomorphismPresentationStatement,
                                          witness: GeneratorSuspension) -> InferenceRule:
    """A proven generator suspension implies a presentation with equivalent notation."""
    if _eta_pair(witness) is None:
        raise ValueError("witness must be an indexed eta suspension")

    def guard(premises, bindings):
        return (len(premises) == 1 and premises[0].conclusion == witness)

    return InferenceRule(
        name="cited eta generator suspension yields presentation in target notation",
        premise_patterns=(PremisePattern(statement_type=GeneratorSuspension),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_eta_presentation(goal: object) -> tuple[GoalExpansion, ...]:
    """Propose a canonical suspension witness; do not promote it to a given fact."""
    if not isinstance(goal, HomomorphismPresentationStatement):
        return ()
    mapping = goal.map
    if not isinstance(mapping, TodaSuspensionMap):
        return ()
    if mapping.source_group != goal.domain or mapping.target_group != goal.codomain:
        return ()
    if not isinstance(goal.codomain, TodaPrimaryGroup):
        return ()
    n = goal.codomain.sphere_dimension
    if type(n) is not int or n < 3 or goal.codomain.group_dimension != n + 1:
        return ()
    if goal.domain != TodaPrimaryGroup(n, n - 1):
        return ()
    source_eta = toda_eta_family_definition_statement(n - 1).element
    target_eta = toda_eta_family_definition_statement(n).element
    if (not _matching_eta_name(goal.source_generator, source_eta)
            or not _matching_eta_name(goal.target_generator, target_eta)):
        return ()
    canonical_map = TodaSuspensionMap(goal.domain, goal.codomain)
    witness = GeneratorSuspension(canonical_map, source_eta, target_eta)
    if _eta_pair(witness) is None:
        return ()
    return (GoalExpansion(eta_presentation_from_suspension_rule(goal, witness), (witness,)),)
