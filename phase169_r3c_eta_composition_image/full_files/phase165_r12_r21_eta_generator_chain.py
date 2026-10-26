"""Generic eta-family definition -> suspension -> generator image evidence.

All resulting steps use R12-R20 cited definition proof ancestors; no new GIVENs.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofStep, ProofRule, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step
from toda_rules import TodaEtaFamilyDefinitionStatement, toda_eta_family_definition_statement


def _eta_pair(goal: GeneratorSuspension):
    if not isinstance(goal, GeneratorSuspension) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    n = getattr(getattr(goal.target_generator, "generator", None), "index", None)
    if type(n) is not int or n < 3:
        return None
    older = toda_eta_family_definition_statement(n - 1)
    newer = toda_eta_family_definition_statement(n)
    if (goal.map != TodaSuspensionMap(TodaPrimaryGroup(n, n - 1), TodaPrimaryGroup(n + 1, n))
            or goal.source_generator != older.element
            or goal.target_generator != newer.element):
        return None
    return older, newer


def eta_definition_to_suspension_rule(goal: GeneratorSuspension) -> InferenceRule:
    pair = _eta_pair(goal)
    if pair is None:
        raise ValueError("goal is not a consecutive eta-family suspension")
    def guard(premises, bindings):
        return (len(premises) == 2
                and tuple(step.conclusion for step in premises) == pair)
    return InferenceRule(
        name="consecutive cited eta definitions imply generator suspension",
        premise_patterns=(PremisePattern(statement_type=TodaEtaFamilyDefinitionStatement),
                          PremisePattern(statement_type=TodaEtaFamilyDefinitionStatement)),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def suspension_to_generator_image_rule() -> InferenceRule:
    def build(premises):
        src = premises[0].conclusion
        return GeneratorImage(src.map, src.source_generator, src.target_generator)
    return InferenceRule(
        name="proved suspension of generator supplies generator image",
        premise_patterns=(PremisePattern(statement_type=GeneratorSuspension),),
        match_guard=lambda premises, bindings: (
            len(premises) == 1
            and isinstance(premises[0].conclusion, GeneratorSuspension)
            and isinstance(premises[0].conclusion.map, TodaSuspensionMap)),
        conclusion_builder=build,
    )


def _composition_eta_suspensions(goal: object) -> tuple[GeneratorSuspension, GeneratorSuspension] | None:
    """Bind a suspended composition to its two separately provable eta steps.

    This checks typed source/target dimensions; it does not prove the steps.
    """
    if not isinstance(goal, GeneratorImage) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    source, target = goal.source_generator, goal.target_generator
    if not isinstance(source, Composition) or not isinstance(target, Composition):
        return None
    f, g = source.left, source.right
    ef, eg = target.left, target.right
    if not all(isinstance(item, HomotopyElement) for item in (f, g, ef, eg)):
        return None
    if (f.source != g.target or ef.source != eg.target
            or goal.map.source_group != TodaPrimaryGroup(g.source, f.target)
            or goal.map.target_group != TodaPrimaryGroup(eg.source, ef.target)):
        return None
    if not all(type(value) is int for value in (
        f.source, f.target, g.source, g.target, ef.source, ef.target, eg.source, eg.target,
    )):
        return None
    first = GeneratorSuspension(
        TodaSuspensionMap(TodaPrimaryGroup(f.source, f.target),
                          TodaPrimaryGroup(ef.source, ef.target)),
        f, ef,
    )
    second = GeneratorSuspension(
        TodaSuspensionMap(TodaPrimaryGroup(g.source, g.target),
                          TodaPrimaryGroup(eg.source, eg.target)),
        g, eg,
    )
    if _eta_pair(first) is None or _eta_pair(second) is None:
        return None
    return first, second


def composition_eta_suspension_image_rule(goal: GeneratorImage) -> InferenceRule:
    """Suspend a composite only from two verified component suspensions."""
    expected = _composition_eta_suspensions(goal)
    if expected is None:
        raise ValueError("goal must be a typed composite of consecutive eta suspensions")

    def guard(premises, bindings):
        return (len(premises) == 2
                and all(step.rule is ProofRule.INFERENCE for step in premises)
                and tuple(step.conclusion for step in premises) == expected)

    return InferenceRule(
        name="suspension preserves composition of proved eta generators",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=GeneratorSuspension),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=GeneratorSuspension),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_eta_generator(goal: object) -> tuple[GoalExpansion, ...]:
    if isinstance(goal, GeneratorSuspension):
        pair = _eta_pair(goal)
        if pair is None:
            return ()
        return (GoalExpansion(eta_definition_to_suspension_rule(goal), pair),)
    if isinstance(goal, GeneratorImage) and isinstance(goal.map, TodaSuspensionMap):
        witness = GeneratorSuspension(goal.map, goal.source_generator, goal.target_generator)
        if _eta_pair(witness) is not None:
            return (GoalExpansion(suspension_to_generator_image_rule(), (witness,)),)
        composite = _composition_eta_suspensions(goal)
        if composite is not None:
            return (GoalExpansion(composition_eta_suspension_image_rule(goal), composite),)
    return ()


def proof_has_cited_eta_general_ancestor(step: ProofStep) -> bool:
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    visited = set()
    def visit(node):
        if id(node) in visited:
            return False
        visited.add(id(node))
        return (node.rule is ProofRule.GIVEN
                and isinstance(node.conclusion, TodaEtaFamilyGeneralDefinition)) or any(visit(p) for p in node.premises)
    return visit(step)
