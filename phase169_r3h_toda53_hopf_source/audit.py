"""R3H live source/citation audit, not a proof completion certificate."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r5_ehp_connection import expand_registered_ehp_terminal_goal
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3h_source_registry import ASSERTION_ID
from proof import ProofRule
from toda_rules import TodaDeltaInjectiveStatement, TodaHopfInvariantSurjectiveStatement

PACKAGE = Path(__file__).resolve().parent


def audit() -> int:
    bridge = build_shared_typed_bridge()
    lower = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    contexts = []
    upper = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if lower.status is not ProofSearchStatus.COMPLETE:
        raise AssertionError("pi4_2 completed source proof changed")
    if upper.status is not ProofSearchStatus.PARTIAL:
        raise AssertionError("R3H does not authorize a pi5_3 completion claim")
    if len(contexts) != 1:
        raise AssertionError("expected one actual screened pi5_3 context")
    screened = contexts[0]
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(goals) != 1:
        raise AssertionError("expected one pi5_3 database goal")
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if citing is None:
        raise AssertionError("pi5_3 actual citing ID unavailable")
    source_id = "shared:8:" + ASSERTION_ID
    a = bridge.registry.assertion(source_id)
    r = bridge.registry.reference(a.reference_id)
    if r.locator != "(5.3)" or r.publication_position != 8100:
        raise AssertionError("adopted equation (5.3) lacks reviewed source position")
    if not precedes_citing_assertion(bridge, source_id, citing):
        raise AssertionError("(5.3) is not prior to target")
    screened_links = tuple(
        link for link in screened.proof_links
        if link.assertion_id == source_id and link.step is not None
    )
    if len(screened_links) != 1 or screened_links[0].step.rule is not ProofRule.GIVEN:
        raise AssertionError("(5.3) exact source citation not screened as GIVEN")
    provider = shared_expansion_provider(screened, proof_target=target)
    seen = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    hopf = TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
    )
    delta = TodaDeltaInjectiveStatement(
        TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2)),
    )
    h_opts = expand_registered_ehp_terminal_goal(hopf, seen)
    d_opts = expand_registered_ehp_terminal_goal(delta, seen)
    if len(h_opts) != 1 or len(d_opts) != 1:
        raise AssertionError("EHP terminal candidate count changed")
    exact_hopf_relation = h_opts[0].subgoals[0]
    if a.content != exact_hopf_relation:
        raise AssertionError("(5.3) typed source does not match existing EHP prerequisite")
    result = reconstruct_registered_goal(
        exact_hopf_relation, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if result.rule is not ProofRule.GIVEN or result.premises:
        raise AssertionError("(5.3) has been mislabeled as inference")
    h_rules = tuple(p.proof_rule for p in h_opts[0].rule.premise_patterns)
    d_rules = tuple(p.proof_rule for p in d_opts[0].rule.premise_patterns)
    if h_rules != (ProofRule.INFERENCE, ProofRule.INFERENCE) or d_rules != (ProofRule.INFERENCE,):
        raise AssertionError("historical EHP premises changed without explicit review")
    report = {
        "phase": "169-R3H",
        "lower_status": lower.status.value,
        "upper_status": upper.status.value,
        "upper_proven_steps": len(upper.proven_steps),
        "source_assertion": source_id,
        "source_locator": r.locator,
        "publication_position": r.publication_position,
        "citing_assertion": citing,
        "prior": True,
        "source_screened_given_count": len(screened_links),
        "hopf_source_reconstruction": "given",
        "hopf_premises_still_required": [p.value for p in h_rules],
        "delta_premises_still_required": [p.value for p in d_rules],
        "new_unjustified_givens": 0,
        "proof_complete_claimed": False,
        "full_suite_run": False,
    }
    report_path = PACKAGE / "output" / "hopf_source_connection.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for k,v in report.items():
        print(k.upper() + "=" + repr(v))
    print("REPORT=" + str(report_path))
    print("R3H_SOURCE_SCREENED=True; no inference provenance reclassification")
    return 0


if __name__ == "__main__":
    raise SystemExit(audit())
