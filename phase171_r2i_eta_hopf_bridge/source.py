"""Compose the cited right-Hopf formula with a proved eta suspension.

Only a source-screened H(alpha)=eta_n and the cited universal eta Definition
can initiate the proof. Every returned object is a backward INFERENCE request;
no relation or group result is registered as GIVEN here.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import Composition, HomotopyElement, MapApplication, Suspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from hopf_rules import ehp_h_preserves_equality_inference_rule
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r12_r28_presentation_connection import _matching_eta_name
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import (
    TodaProp22RightFormula,
    _formula_parts,
)
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from relation_rules import (
    equality_preserved_under_left_composition_inference_rule,
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)
from toda_rules import toda_eta_family_definition_statement


@dataclass(frozen=True)
class EtaHopfChain:
    """Exactly typed goals; a schema, not a source or a proof certificate."""
    alpha: HomotopyElement
    beta: HomotopyElement
    eta_next: HomotopyElement
    generator_suspension: GeneratorSuspension
    eta_forward: Relation
    eta_backward: Relation
    alpha_composition: Relation
    hopf_composition: Relation
    cited_hopf: Relation
    intermediate: Relation
    beta_composition: Relation
    conclusion: Relation


def _eq(lhs: object, rhs: object) -> Relation:
    return Relation(lhs=lhs, rhs=rhs, relation_type=RelationType.EQUALITY)


def _make_chain(hopf: Relation) -> EtaHopfChain | None:
    """Check source, target, eta identity, and the R2H formula's domain."""
    if (not isinstance(hopf, Relation)
            or hopf.relation_type is not RelationType.EQUALITY
            or not isinstance(hopf.lhs, MapApplication)
            or hopf.lhs.map != EHP_H_MAP
            or not isinstance(hopf.lhs.expression, HomotopyElement)
            or not isinstance(hopf.rhs, HomotopyElement)):
        return None
    alpha, beta = hopf.lhs.expression, hopf.rhs
    generator = beta.generator
    if (generator is None or generator.family != "η"
            or generator.decoration is not None
            or type(generator.index) is not int or generator.index < 3):
        return None
    n = generator.index
    older = toda_eta_family_definition_statement(n).element
    newer = toda_eta_family_definition_statement(n + 1).element
    if not _matching_eta_name(beta, older):
        return None
    suspended = Suspension(beta)
    if (not Composition(alpha, suspended).is_type_compatible()
            or not Composition(alpha, newer).is_type_compatible()
            or not Composition(beta, suspended).is_type_compatible()
            or not Composition(beta, newer).is_type_compatible()):
        return None
    cited_hopf = _eq(
        MapApplication(EHP_H_MAP, Composition(alpha, suspended)),
        Composition(beta, suspended),
    )
    formula = _eq(
        cited_hopf.lhs,
        Composition(MapApplication(EHP_H_MAP, alpha), suspended),
    )
    if _formula_parts(formula) is None:
        return None
    witness = GeneratorSuspension(
        TodaSuspensionMap(
            TodaPrimaryGroup(n + 1, n),
            TodaPrimaryGroup(n + 2, n + 1),
        ),
        older,
        newer,
    )
    eta_forward = _eq(suspended, newer)
    eta_backward = _eq(newer, suspended)
    alpha_composition = _eq(
        Composition(alpha, newer), Composition(alpha, suspended),
    )
    hopf_composition = _eq(
        MapApplication(EHP_H_MAP, alpha_composition.lhs),
        MapApplication(EHP_H_MAP, alpha_composition.rhs),
    )
    intermediate = _eq(hopf_composition.lhs, cited_hopf.rhs)
    beta_composition = _eq(
        Composition(beta, suspended), Composition(beta, newer),
    )
    conclusion = _eq(intermediate.lhs, beta_composition.rhs)
    return EtaHopfChain(
        alpha, beta, newer, witness, eta_forward, eta_backward,
        alpha_composition, hopf_composition, cited_hopf, intermediate,
        beta_composition, conclusion,
    )


def eligible_eta_hopf_chains(available: tuple[object, ...]) -> tuple[EtaHopfChain, ...]:
    """Read earlier, screened GIVEN *conclusions* only; never inspect a DB goal."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (available.count(TodaEtaFamilyGeneralDefinition()) != 1
            or available.count(TodaProp22RightFormula()) != 1):
        return ()
    candidates = []
    for item in available:
        if available.count(item) != 1:
            continue
        chain = _make_chain(item)
        if chain is not None:
            candidates.append(chain)
    return tuple(candidates)


def cited_eta_suspension_equality_rule(
    goal: Relation, witness: GeneratorSuspension,
) -> InferenceRule:
    """Turn a DERIVED generator suspension into an equality of elements.

    `_matching_eta_name` handles only the repository's already typed Unicode
    and underscore spellings; the actual suspension assertion must be proved.
    """
    if (not isinstance(witness, GeneratorSuspension)
            or not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, Suspension)
            or not isinstance(goal.lhs.expression, HomotopyElement)
            or not isinstance(goal.rhs, HomotopyElement)):
        raise ValueError("expected a typed eta suspension equality")
    beta = goal.lhs.expression
    n = getattr(getattr(beta, "generator", None), "index", None)
    if type(n) is not int or n < 3:
        raise ValueError("expected a concrete eta-family index")
    from phase165_r12_r21_eta_generator_chain import _eta_pair
    pair = _eta_pair(witness)
    if (pair is None
            or pair[0].index != n
            or pair[1].index != n + 1
            or not _matching_eta_name(beta, pair[0].element)
            or not _matching_eta_name(goal.rhs, pair[1].element)
            or witness.source_generator != pair[0].element
            or witness.target_generator != pair[1].element):
        raise ValueError("generator suspension does not justify this equality")

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.INFERENCE
                and premises[0].conclusion == witness)

    return InferenceRule(
        name="proved consecutive eta suspension yields element equality",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.INFERENCE,
            statement_type=GeneratorSuspension,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_eta_hopf_power(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Backward chain using existing general congruence and equality rules.

    eta_n^2 is represented solely by the exact typed composition
    eta_n o eta_(n+1); its pretty-printed exponent grants no new fact.
    """
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return ()
    proposals = []
    for chain in eligible_eta_hopf_chains(available):
        if goal == chain.eta_forward:
            rule = cited_eta_suspension_equality_rule(goal, chain.generator_suspension)
            subgoals = (chain.generator_suspension,)
        elif goal == chain.eta_backward:
            rule = equality_symmetry_inference_rule()
            subgoals = (chain.eta_forward,)
        elif goal == chain.alpha_composition:
            rule = equality_preserved_under_left_composition_inference_rule(chain.alpha)
            subgoals = (chain.eta_backward,)
        elif goal == chain.hopf_composition:
            rule = ehp_h_preserves_equality_inference_rule()
            subgoals = (chain.alpha_composition,)
        elif goal == chain.intermediate:
            rule = equality_transitivity_inference_rule()
            subgoals = (chain.hopf_composition, chain.cited_hopf)
        elif goal == chain.beta_composition:
            rule = equality_preserved_under_left_composition_inference_rule(chain.beta)
            subgoals = (chain.eta_forward,)
        elif goal == chain.conclusion:
            rule = equality_transitivity_inference_rule()
            subgoals = (chain.intermediate, chain.beta_composition)
        else:
            continue
        if not any(x.subgoals == subgoals and x.rule.name == rule.name for x in proposals):
            proposals.append(GoalExpansion(rule, subgoals))
    return tuple(proposals)
