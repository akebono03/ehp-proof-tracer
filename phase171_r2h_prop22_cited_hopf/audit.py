"""Verify the two-step cited Hopf derivation under publication-order screening."""
from __future__ import annotations

from expression import Composition, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase171_r2h_prop22_cited_hopf.source import (
    TodaProp22RightFormula, expand_cited_prop22_right_formula,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def run() -> None:
    complete = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(complete, n=3, k=3)
    if len(goals) != 1:
        raise RuntimeError("expected exactly one pi_6^3 goal")
    root = goals[0]
    citing = resolve_specialized_goal_citing_id(complete, root)
    if not citing:
        raise RuntimeError("pi_6^3 citing assertion unresolved")
    screened = screen_shared_proof_context(
        complete, goal=root, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    formula_links = tuple(
        link for link in screened.proof_links
        if link.assertion_id.endswith(":toda:adopted:prop2.2:right_hopf_formula")
        and link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == TodaProp22RightFormula()
    )
    hopf_links = tuple(
        link for link in screened.proof_links
        if link.assertion_id.endswith(":toda:adopted:eq5.3:nu_prime_hopf_relation")
        and link.step is not None
        and link.step.rule is ProofRule.GIVEN
    )
    if len(formula_links) != 1 or len(hopf_links) != 1:
        raise RuntimeError("one cited Prop2.2 and one (5.3) Hopf leaf required")
    assertion = screened.registry.assertion(formula_links[0].assertion_id)
    reference = screened.registry.reference(assertion.reference_id)
    if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or reference.locator != "Proposition 2.2"
            or reference.publication_position != 3700
            or not precedes_citing_assertion(screened, formula_links[0].assertion_id, citing)):
        raise RuntimeError("Proposition 2.2 citation position invalid")
    hopf = hopf_links[0].step.conclusion
    if (not isinstance(hopf, Relation)
            or hopf.relation_type is not RelationType.EQUALITY
            or not isinstance(hopf.lhs, MapApplication)
            or hopf.lhs.map != EHP_H_MAP):
        raise RuntimeError("(5.3) is not the typed H(nu-prime)=eta_5 equality")
    alpha, beta = hopf.lhs.expression, hopf.rhs
    final = Relation(
        lhs=MapApplication(EHP_H_MAP, Composition(alpha, Suspension(beta))),
        rhs=Composition(beta, Suspension(beta)),
        relation_type=RelationType.EQUALITY,
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=root)
    offered = provider(final)
    if not any(option.rule.name ==
               "substitute proved Hopf value into cited right formula"
               for option in offered):
        raise RuntimeError("new cited inference not connected to shared provider")
    # Audit only the newly introduced two-step chain, so unrelated generic
    # alternatives cannot be mistaken for a successful R2H witness.
    scoped_provider = lambda current: expand_cited_prop22_right_formula(
        current, available,
    )
    result = reconstruct_registered_goal(
        final, screened, citing, scoped_provider,
        lookup_mode="typed_reference_publication",
    )
    if (result.rule is not ProofRule.INFERENCE
            or result.conclusion != final
            or len(result.premises) != 2
            or result.premises[0].rule is not ProofRule.INFERENCE
            or result.premises[1].rule is not ProofRule.GIVEN
            or result.premises[1].conclusion != hopf
            or len(result.premises[0].premises) != 1
            or result.premises[0].premises[0].rule is not ProofRule.GIVEN
            or result.premises[0].premises[0].conclusion != TodaProp22RightFormula()):
        raise RuntimeError("right-Hopf dependency chain is not a verified two-step proof")
    if any(link.step is not None and link.step.conclusion == root for link in screened.proof_links):
        raise RuntimeError("group goal was incorrectly inserted as a source")
    print("PHASE171_R2H_PROP22_SOURCE=PASS", flush=True)
    print("PHASE171_R2H_PUBLICATION_POSITION=3700", flush=True)
    print("PHASE171_R2H_HOPF_DEPENDENCY=PASS", flush=True)
    print("PHASE171_R2H_FORMULA_INFERENCE=PASS", flush=True)
    print("PHASE171_R2H_COMBINED_INFERENCE=PASS", flush=True)
    print("PHASE171_R2H_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2H_RESULT=PASS_CITED_FORMULA_ONLY", flush=True)


if __name__ == "__main__":
    run()
