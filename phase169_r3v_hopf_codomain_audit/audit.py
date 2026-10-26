"""Phase169 R3V read-only: inspect cited pi_6^5 prerequisites for Hopf surjectivity."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r5_ehp_connection import expand_cited_ehp_terminal_goal
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation,
    expand_registered_eta_specialization,
    specialize_eta_group_relation,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule, Relation
from toda_rules import TodaHopfInvariantSurjectiveStatement, TodaProp51FiniteDimensionalStatement
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent


def _screened_context():
    bridge = build_shared_typed_bridge()
    target_candidates = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(target_candidates) != 1:
        raise AssertionError("Unique π_5^3 target is required")
    target = target_candidates[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, target)
    if not citing_id:
        raise AssertionError("Missing citing source assertion")
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise AssertionError("The completed π_5^3 baseline must remain available")
    screened = contexts[0]
    given_links = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == screened.registry.assertion(link.assertion_id).content
    )
    return screened, target, citing_id, result, given_links


def examine() -> dict:
    screened, target, citing_id, result, given_links = _screened_context()
    available = tuple(link.step.conclusion for link in given_links)
    hopf_goal = TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
    )
    hopf_options = expand_cited_ehp_terminal_goal(hopf_goal, available)
    if len(hopf_options) != 1 or len(hopf_options[0].subgoals) != 2:
        raise AssertionError("Current cited Hopf prerequisite baseline changed")
    hopf_relation, prop51 = hopf_options[0].subgoals
    if not isinstance(prop51, TodaProp51FiniteDimensionalStatement):
        raise AssertionError("Hopf source is not registered Prop5.1")
    general = prop51.higher_eta_group_relation
    if not _is_generic_eta_group_relation(general):
        raise AssertionError("Registered Prop5.1 contains no general η-group clause")
    concrete_goal = specialize_eta_group_relation(general, 5)
    if concrete_goal.lhs != hopf_goal.map.target_group:
        raise AssertionError("Specialized higher-eta group is not Hopf's codomain")
    generic_links = tuple(
        link for link in given_links
        if _is_generic_eta_group_relation(link.step.conclusion)
        and specialize_eta_group_relation(link.step.conclusion, 5) == concrete_goal
    )
    unique_generic = []
    for link in generic_links:
        if link.step.conclusion not in unique_generic:
            unique_generic.append(link.step.conclusion)
    eta_options = expand_registered_eta_specialization(concrete_goal, available)
    generator = concrete_goal.rhs.generator
    target_element = hopf_relation.rhs
    # Source spellings η_5 and η₅ need not match, but their typed generator must.
    generator_consistent = (
        generator.generator == getattr(target_element, "generator", None)
        and generator.dimension == getattr(target_element, "dimension", None)
        and generator.source == getattr(target_element, "source", None)
        and generator.target == getattr(target_element, "target", None)
    )
    proof_status = "not_attempted"
    proof_rule = None
    proof_sources = []
    proof_premise_types = []
    provider = shared_expansion_provider(screened, proof_target=target)
    try:
        proof = reconstruct_registered_goal(
            concrete_goal, screened, citing_id, provider,
            lookup_mode="typed_reference_publication",
        )
    except Exception as exc:
        proof_status = "unresolved:" + type(exc).__name__ + ": " + str(exc)
    else:
        proof_status = "proved"
        proof_rule = proof.rule.value
        proof_premise_types = [type(p.conclusion).__name__ for p in proof.premises]
        proof_sources = sorted({
            p.inference_rule.literature_reference.locator
            for p in proof.premises
            if p.inference_rule is not None
            and p.inference_rule.literature_reference is not None
        })
    records = []
    for link in generic_links:
        assertion = screened.registry.assertion(link.assertion_id)
        records.append({
            "assertion_id": link.assertion_id,
            "dependencies": list(assertion.dependencies),
            "component_position": assertion.component_position,
            "is_prior": precedes_citing_assertion(screened, link.assertion_id, citing_id),
            "source_locator": (
                link.step.inference_rule.literature_reference.locator
                if link.step.inference_rule is not None
                and link.step.inference_rule.literature_reference is not None else None
            ),
        })
    return {
        "phase": "169-R3V",
        "mode": "AUDIT_ONLY",
        "pi53_proof_status": result.status.value,
        "pi65_goal": repr(concrete_goal),
        "screened_generic_source_count": len(generic_links),
        "unique_generic_source_contents": len(unique_generic),
        "generic_source_records": records,
        "eta_specialization_option_count": len(eta_options),
        "pi65_proof_status": proof_status,
        "pi65_proof_rule": proof_rule,
        "pi65_proof_premise_types": proof_premise_types,
        "pi65_proof_sources": proof_sources,
        "hopf_current_subgoals": [type(s).__name__ for s in hopf_options[0].subgoals],
        "hopf_has_concrete_pi65_premise": any(
            isinstance(s, Relation) and s == concrete_goal
            for s in hopf_options[0].subgoals
        ),
        "eta_generator_matches_h_image": generator_consistent,
        "production_files_modified": False,
        "full_pytest_run": False,
    }


def main() -> None:
    report = examine()
    out = ROOT / "output" / "r3v_hopf_codomain_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for field in (
        "pi53_proof_status", "screened_generic_source_count",
        "unique_generic_source_contents", "eta_specialization_option_count",
        "pi65_proof_status", "pi65_proof_rule", "pi65_proof_sources",
        "hopf_current_subgoals", "hopf_has_concrete_pi65_premise",
        "eta_generator_matches_h_image",
    ):
        print("R3V_" + field.upper() + "=" + repr(report[field]))
    for record in report["generic_source_records"]:
        print("R3V_GENERIC_SOURCE=" + json.dumps(record, ensure_ascii=False))
    print("R3V_AUDIT_ONLY=True")
    print("R3V_FULL_PYTEST_RUN=False")
    print("R3V_REPORT=" + str(out))


if __name__ == "__main__":
    main()
