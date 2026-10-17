"""R12-R22: general free cyclic relation -> cyclic statement, proof-backed closure."""
from __future__ import annotations

from homotopy_groups import FreeCyclicGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from proof import (InferenceRule, PremisePattern, ProofRule, ProofStep, Relation,
                   RelationType, find_inference_matches_for_rule, apply_inference_match)
from phase165_r12_r17_quotient_chain import build_generic_quotient_chain


def free_cyclic_relation_to_structure_rule() -> InferenceRule:
    """A proved free-cyclic presentation gives an infinite cyclic structure."""
    def guard(premises, bindings):
        relation = premises[0].conclusion
        return (isinstance(relation, Relation)
                and relation.relation_type is RelationType.EQUALITY
                and isinstance(relation.rhs, FreeCyclicGroup))

    def build(premises):
        relation = premises[0].conclusion
        return CyclicStructureStatement(relation.lhs, relation.rhs.generator, None)

    return InferenceRule(
        name="proved free cyclic group relation implies infinite cyclic structure",
        premise_patterns=(PremisePattern(statement_type=Relation,
                                         relation_type=RelationType.EQUALITY),),
        match_guard=guard,
        conclusion_builder=build,
    )


def source_structure_from_proven_relation(group_proof: ProofStep) -> ProofStep:
    """Never use a bare goal or manufacture a new GIVEN."""
    if not isinstance(group_proof, ProofStep):
        raise TypeError("actual ProofStep required")
    matches = find_inference_matches_for_rule(
        free_cyclic_relation_to_structure_rule(), (group_proof,)
    )
    if len(matches) != 1:
        raise ValueError("source is not a proved free-cyclic relation")
    step = apply_inference_match(matches[0])
    if step.rule is not ProofRule.INFERENCE or step.premises != (group_proof,):
        raise ValueError("source relation ancestry not preserved")
    return step


def proof_ancestors(root: ProofStep, witnesses: tuple[ProofStep, ...]) -> bool:
    """Require identity of every independently verified proof in final ancestry."""
    if not isinstance(root, ProofStep):
        return False
    visited = set()
    def visit(node):
        if id(node) in visited:
            return
        visited.add(id(node))
        for premise in node.premises:
            visit(premise)
    visit(root)
    return all(id(w) in visited for w in witnesses)


def close_quotient_from_verified_steps(
    presentation: ProofStep, kernel: ProofStep, surjectivity: ProofStep,
    source_relation: ProofStep,
):
    """Return a chain only if all four actual proof objects occur in its root."""
    structure = source_structure_from_proven_relation(source_relation)
    result = build_generic_quotient_chain(presentation, kernel, surjectivity, structure)
    if result.proof is None:
        return result
    if not proof_ancestors(result.proof, (presentation, kernel, surjectivity, source_relation)):
        raise ValueError("quotient result loses an original proof ancestor")
    return result
