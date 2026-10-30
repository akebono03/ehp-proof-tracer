"""Run R2I with only screened references and the specifically reviewed rules."""
from __future__ import annotations

from expression import Composition, MapApplication
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import (
    TodaEtaFamilyGeneralDefinition,
    expand_cited_eta_definition,
)
from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase171_r2h_prop22_cited_hopf.source import (
    TodaProp22RightFormula,
    expand_cited_prop22_right_formula,
)
from phase171_r2i_eta_hopf_bridge.source import (
    eligible_eta_hopf_chains,
    expand_cited_eta_hopf_power,
)
from proof import ProofRule, Relation, RelationType
from toda_rules import TodaEtaFamilyDefinitionStatement
from unified_statement_registry import AssertionOrigin


def _screened_context():
    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=3, k=3)
    if len(targets) != 1:
        raise RuntimeError("pi_6^3 must have precisely one registered goal")
    group_goal = targets[0]
    citing = resolve_specialized_goal_citing_id(bridge, group_goal)
    if not citing:
        raise RuntimeError("pi_6^3 citing assertion not resolved")
    screened = screen_shared_proof_context(
        bridge, goal=group_goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    return screened, group_goal, citing


def _available(screened) -> tuple[object, ...]:
    return tuple(
        link.step.conclusion
        for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )


def _checked_chain(screened, citing):
    available = _available(screened)
    chains = tuple(
        chain for chain in eligible_eta_hopf_chains(available)
        if (chain.alpha.target == 3 and chain.alpha.source == 6
            and chain.beta.target == 5 and chain.beta.source == 6)
    )
    if len(chains) != 1:
        raise RuntimeError("no unique screened nu-prime/eta_5 Hopf chain")
    chain = chains[0]
    expected_types = (
        TodaEtaFamilyGeneralDefinition,
        TodaProp22RightFormula,
    )
    for expected in expected_types:
        links = tuple(
            link for link in screened.proof_links
            if link.step is not None
            and type(link.step.conclusion) is expected
        )
        if len(links) != 1:
            raise RuntimeError("required cited source is not unique: " + expected.__name__)
        link = links[0]
        assertion = screened.registry.assertion(link.assertion_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or not precedes_citing_assertion(screened, link.assertion_id, citing)):
            raise RuntimeError("source not earlier than citing goal")
    return chain, available


def _scoped_provider(available):
    def expand(goal):
        return (
            expand_cited_eta_hopf_power(goal, available)
            + expand_cited_prop22_right_formula(goal, available)
            + expand_cited_eta_definition(goal, available)
            + expand_cited_eta_generator(goal)
        )
    return expand


def build_cited_r2i_proof():
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    public_provider = shared_expansion_provider(screened, proof_target=group_goal)
    if not any(option.subgoals == (chain.intermediate, chain.beta_composition)
               for option in public_provider(chain.conclusion)):
        raise RuntimeError("R2I is not connected to the shared expansion provider")
    proof = reconstruct_registered_goal(
        chain.conclusion, screened, citing, _scoped_provider(available),
        lookup_mode="typed_reference_publication",
    )
    if proof.rule is not ProofRule.INFERENCE or proof.conclusion != chain.conclusion:
        raise RuntimeError("R2I returned no typed inference root")
    ancestry = []
    visited = set()

    def visit(step):
        if id(step) in visited:
            return
        visited.add(id(step))
        ancestry.append(step)
        for premise in step.premises:
            visit(premise)
    visit(proof)
    leaves = tuple(step for step in ancestry if step.rule is ProofRule.GIVEN)
    expected_leaves = (
        TodaEtaFamilyGeneralDefinition(),
        TodaProp22RightFormula(),
        Relation(
            MapApplication(EHP_H_MAP, chain.alpha),
            chain.beta,
            RelationType.EQUALITY,
        ),
    )
    if (len(leaves) != len(expected_leaves)
            or any(sum(step.conclusion == expected for step in leaves) != 1
                   for expected in expected_leaves)):
        raise RuntimeError("unexpected GIVEN ancestor in R2I proof")
    if not any(isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
               and step.conclusion.index == 5 and step.rule is ProofRule.INFERENCE
               for step in ancestry):
        raise RuntimeError("eta_5 cited Definition missing from ancestry")
    if not any(isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
               and step.conclusion.index == 6 and step.rule is ProofRule.INFERENCE
               for step in ancestry):
        raise RuntimeError("eta_6 cited Definition missing from ancestry")
    if not any(step.conclusion == chain.eta_forward
               and step.rule is ProofRule.INFERENCE for step in ancestry):
        raise RuntimeError("eta_6=E eta_5 not inferred")
    if not isinstance(chain.conclusion.rhs, Composition):
        raise RuntimeError("eta square is not a typed Composition")
    if any(step.conclusion == group_goal for step in ancestry):
        raise RuntimeError("group structure was promoted into a proof")
    return proof, chain, tuple(ancestry)


def run() -> None:
    proof, chain, ancestry = build_cited_r2i_proof()
    from phase169_r10eb_typed_composition_power.display import (
        typed_stable_composition_power_latex,
    )
    rendered = typed_stable_composition_power_latex(chain.conclusion.rhs)
    if rendered != r"\eta_{5}^{2}":
        raise RuntimeError("eta_5^2 typed display mismatch: " + str(rendered))
    print("PHASE171_R2I_PROVEN_DEFINITION=PASS", flush=True)
    print("PHASE171_R2I_PROP22_AND_53_ANCESTRY=PASS", flush=True)
    print("PHASE171_R2I_ETA6_EQUALS_E_ETA5=PASS", flush=True)
    print("PHASE171_R2I_TYPED_ETA_SQUARE=PASS", flush=True)
    print("PHASE171_R2I_INFERENCES=" + str(sum(
        step.rule is ProofRule.INFERENCE for step in ancestry)), flush=True)
    print("PHASE171_R2I_GIVEN_LEAVES=" + str(sum(
        step.rule is ProofRule.GIVEN for step in ancestry)), flush=True)
    print("PHASE171_R2I_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2I_RESULT=PASS_CITED_HOPF_IMAGE_ONLY", flush=True)


if __name__ == "__main__":
    run()
