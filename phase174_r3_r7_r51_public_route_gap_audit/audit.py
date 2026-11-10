"""R51: compare the actual public group search and Web model with R50.

Read-only. Do not replace the public provider with R50's curated provider, or
make any group-specific Narrative. Inspect real source-linked candidate shapes
and the canonical public search's observed ProofStep list.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r51_public_route_gap_audit.source_guard import verify_checkout


def inspect_public_route_gap() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r3_recursive_search import SourceBoundGoal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME as ROOT_RULE, ehp_zero_inputs
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE, upper_delta_surjectivity_inputs,
    )
    from phase174_r3_r7_r50_root_exactness_terminal_zero_frontier.audit import (
        inspect_integrated_root_frontier,
    )
    from proof import ProofRule, Relation
    from web_group_proof import build_standard_web_group_proof_view

    n, k = 7, 5
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + k, n))

    # This is the EXACT public group search entry, with its ordinary bridge
    # and context sink. No preselected R50 provider is passed to it.
    contexts = []
    original = build_shared_typed_bridge()
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=original, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("Public group search did not expose one screened context")
    screened = contexts[0]
    provider = shared_expansion_provider(screened, proof_target=goal)

    root_options = tuple(option for option in provider(goal)
                         if option.rule.name == ROOT_RULE)
    if len(root_options) != 1 or root_options[0].subgoals != ehp_zero_inputs(goal):
        raise RuntimeError("Public EHP root candidate differs from reviewed R50")
    upper = root_options[0].subgoals[0]
    upper_options = tuple(option for option in provider(upper)
                          if option.rule.name == UPPER_RULE)
    if len(upper_options) != 1 or upper_options[0].subgoals != upper_delta_surjectivity_inputs(upper):
        raise RuntimeError("Public upper Delta proof candidate differs from reviewed R50")
    kernel_goal = upper_options[0].subgoals[2]
    if not isinstance(kernel_goal, KernelMultipleStatement):
        raise RuntimeError("Upper Delta no longer demands a kernel multiple")
    kernel_options = tuple(option for option in provider(kernel_goal)
                           if option.rule.name == KERNEL_RULE)
    if len(kernel_options) != 1 or len(kernel_options[0].subgoals) != 3:
        raise RuntimeError("Public R35 cited three-premise kernel proposal missing")
    domain = kernel_options[0].subgoals[0]
    if not isinstance(domain, Relation):
        raise RuntimeError("Kernel domain is no longer a typed group Relation")
    direct_domain_steps = tuple(link.step for link in screened.proof_links
                                if link.step is not None
                                and link.step.rule is ProofRule.GIVEN
                                and link.step.conclusion == domain)
    from phase165_r52_r9_shared_math import shared_expansion_provider as build_provider
    domain_options = tuple(x for x in build_provider(screened, proof_target=goal)(domain)
                           if x.rule.name == "generic cited typed scalar specialization"
                           and len(x.subgoals) == 1)
    public_source_bound = tuple(option for option in kernel_options
                                if any(isinstance(x, SourceBoundGoal)
                                       for x in option.subgoals))

    # This is the public model-backed view (same entry called by Group query).
    # A complete view must pass the existing proof-tree trust boundary, which
    # we do not bypass, stub or replace.
    web_view = build_standard_web_group_proof_view(
        n=n, k=k, max_depth=2, mode="narrative", citation_source="model",
    )
    if web_view.n != n or web_view.k != k:
        raise RuntimeError("Public Web view target differs")
    web_complete = web_view.key == "generic-complete-proof" and not web_view.partial_result
    result_complete = result.status is ProofSearchStatus.COMPLETE
    if result_complete != web_complete:
        raise RuntimeError("Public search and Web model disagree on completion")
    if result_complete and result.conclusion != goal:
        raise RuntimeError("Completed public result differs from target")

    # Independent observation: R50's source-checked, scoped inference proof.
    # This is NOT installed in the public search and is not injected as steps.
    r50 = inspect_integrated_root_frontier()
    if (r50["canonical_status"] != "complete"
            or r50["canonical_root_verified_complete"] is not True
            or r50["canonical_root_four_independent_inference_parents"] is not True
            or r50["canonical_root_has_all_six_cited_facts"] is not True
            or r50["canonical_open_goal_types"] != {}):
        raise RuntimeError("R50 certified scoped root proof contract changed")

    original_types = dict(sorted(Counter(type(x).__name__ for x in result.open_goals).items()))
    proven_types = dict(sorted(Counter(type(x.conclusion).__name__
                                    for x in result.proven_steps).items()))
    same_scoped_public = result_complete and web_complete
    gap = not same_scoped_public
    # No mathematical rule is changed here. An inferred-domain requirement
    # may need a generic SourceBoundGoal in ordinary search, not the R50-only
    # goal-by-goal provider filtering. This is a diagnostic, NOT a proof.
    source_bound_missing = bool(direct_domain_steps and domain_options and
                                not public_source_bound)
    if gap and source_bound_missing:
        gate = "PASS_R51_PUBLIC_SOURCE_BOUND_KERNEL_GAP_IDENTIFIED"
    elif gap:
        gate = "PASS_R51_PUBLIC_SCOPED_SEARCH_GAP_RECORDED"
    else:
        gate = "PASS_R51_PUBLIC_ROOT_PROOF_PRESENT_HTTP_PENDING"
    return {
        "target": "pi_12^7 = 0",
        "r50_scoped_complete": True,
        "r50_scoped_verified_steps": r50["canonical_verified_steps"],
        "r50_scoped_root_has_six_cited_facts": True,
        "r50_proof_not_injected_into_public": True,
        "public_result_status": result.status.value,
        "public_result_verified_steps": len(result.proven_steps),
        "public_result_open_goal_types": original_types,
        "public_result_proven_goal_types": proven_types,
        "public_result_diagnostics": list(result.diagnostics),
        "public_root_proof_complete": result_complete,
        "public_root_inference_count": sum(
            step.conclusion == goal and step.rule is ProofRule.INFERENCE
            for step in result.proven_steps
        ),
        "public_screened_source_links": len(screened.proof_links),
        "public_root_ehp_candidates": len(root_options),
        "public_upper_delta_candidates": len(upper_options),
        "public_r35_kernel_candidates": len(kernel_options),
        "public_r35_kernel_requires_bare_relation": any(
            isinstance(x, Relation) for x in kernel_options[0].subgoals
        ),
        "public_r35_kernel_source_bound_candidates": len(public_source_bound),
        "public_kernel_domain_direct_givens": len(direct_domain_steps),
        "public_kernel_domain_cited_specializations": len(domain_options),
        "public_source_bound_kernel_gap_candidate": source_bound_missing,
        "public_web_key": web_view.key,
        "public_web_partial_result": web_view.partial_result,
        "public_web_rendered_lines": len(web_view.rendered_lines),
        "public_web_model_route_checked": True,
        "public_http_checked": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_files_changed": 0,
        "full_pytest": False,
        "gate": gate,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    audit = None if args.dry_run else inspect_public_route_gap()
    data = {
        "phase": "174-R3-R7-R51",
        "git_state": state,
        "observations": audit,
        "new_given": 0,
        "production_files_changed": 0,
        "full_pytest": False,
        "gate": "PASS_R51_PUBLIC_ROUTE_PREFLIGHT" if args.dry_run else audit["gate"],
    }
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    folder = base / "EHPProofTracerAudit" / "phase174_r3_r7_r51"
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / ("preflight.json" if args.dry_run else "public_route_gap.json")
    dest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tag = "PHASE174_R3R7R51_"
    for key, value in state.items():
        print(tag + key.upper() + "=" + str(value))
    if audit is not None:
        for key, value in audit.items():
            print(tag + key.upper() + "=" + str(value))
    print(tag + "REPORT=" + str(dest))
    print(tag + "GATE=" + data["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
