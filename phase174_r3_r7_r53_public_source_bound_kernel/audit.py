"""R53: verify the real public zero-group search and shared verified Web route.

No precomputed R50 or R52 proof is injected. Only the production public entry
is called; the common proof engine checks every sourced candidate normally.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r53_public_source_bound_kernel.source_guard import verify_checkout


def inspect_public_root_completion() -> dict[str, object]:
    """Compare real public search and source-verified model-backed Web view."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r3_recursive_search import SourceBoundGoal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import upper_delta_surjectivity_inputs
    from phase174_r3_r7_r53_public_source_bound_kernel.provider import build_public_source_bound_kernel_provider
    from proof import ProofRule, ProofStep
    from web_group_proof import build_standard_web_group_proof_view

    n, k = 7, 5
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + k, n))
    bridge = build_shared_typed_bridge()
    contexts = []
    public = search_group_from_registered_goal(n=n, k=k, bridge=bridge,
                                               context_sink=contexts.append)
    if len(contexts) != 1:
        raise RuntimeError("R53 could not observe the exact screened context")
    screened = contexts[0]
    provider = shared_expansion_provider(screened, proof_target=goal)
    wrapped = build_public_source_bound_kernel_provider(provider, screened)
    root_inputs = ehp_zero_inputs(goal)
    if root_inputs is None:
        raise RuntimeError("EHP zero root changed")
    upper_inputs = upper_delta_surjectivity_inputs(root_inputs[0])
    if upper_inputs is None:
        raise RuntimeError("Upper Delta exactness contract changed")
    kernel_goal = upper_inputs[2]
    if not isinstance(kernel_goal, KernelMultipleStatement):
        raise RuntimeError("R53 missing typed lower Delta kernel")
    original = tuple(item for item in provider(kernel_goal)
                     if item.rule.name == KERNEL_RULE)
    offered = tuple(item for item in wrapped(kernel_goal)
                    if item.rule.name == KERNEL_RULE)
    bound = tuple(item for item in offered
                  if any(type(sub) is SourceBoundGoal for sub in item.subgoals))
    if not original or not bound:
        raise RuntimeError("R53 missing checked source-bound kernel option")

    proof_root = tuple(step for step in public.proven_steps
                       if step.conclusion == goal and step.rule is ProofRule.INFERENCE)
    kernel_steps = tuple(step for step in public.proven_steps
                         if step.conclusion == kernel_goal and step.rule is ProofRule.INFERENCE)
    four = any(len(step.premises) == 4
               and tuple(parent.conclusion for parent in step.premises) == root_inputs
               and all(parent.rule is ProofRule.INFERENCE for parent in step.premises)
               for step in proof_root)
    three = any(len(step.premises) == 3
                and step.premises[0].rule is ProofRule.INFERENCE
                and step.premises[1].rule is ProofRule.GIVEN
                and step.premises[2].rule is ProofRule.GIVEN
                for step in kernel_steps)

    def cited_ancestors(step: ProofStep) -> set[str]:
        found: set[str] = set()
        seen: set[int] = set()
        def walk(node: ProofStep) -> None:
            if id(node) in seen:
                return
            seen.add(id(node))
            if node.rule is ProofRule.GIVEN:
                reference = getattr(getattr(node.inference_rule, "literature_reference", None),
                                    "locator", None)
                if isinstance(reference, str):
                    found.add(reference)
            for ancestor in node.premises:
                walk(ancestor)
        walk(step)
        return found

    required = {
        "(5.9)", "Proposition 4.2 (4.4)",
        "Proposition 5.8", "(5.10)",
        "Proposition 2.7", "(5.1)",
    }
    provenance = any(required.issubset(cited_ancestors(step)) for step in proof_root)
    web = build_standard_web_group_proof_view(
        n=n, k=k, max_depth=2, mode="narrative", citation_source="model",
    )
    complete = (public.status is ProofSearchStatus.COMPLETE
                and public.conclusion == goal and not public.open_goals)
    web_complete = web.key == "generic-complete-proof" and web.partial_result is False
    if (web_complete != complete or (complete and (not four or not three or not provenance))):
        raise RuntimeError("R53 public model or citation proof trust contract failed")
    return {
        "root": "pi_12^7 = 0",
        "public_status": public.status.value,
        "public_verified_steps": len(public.proven_steps),
        "public_open_goal_types": dict(sorted(Counter(type(x).__name__ for x in public.open_goals).items())),
        "public_diagnostics": list(public.diagnostics),
        "public_root_inference_count": len(proof_root),
        "public_kernel_inference_count": len(kernel_steps),
        "public_kernel_domain_cited_inference": three,
        "public_root_four_inferred_parents": four,
        "public_root_six_cited_ancestors": provenance,
        "public_r35_original_candidates": len(original),
        "public_r35_source_bound_candidates": len(bound),
        "public_web_key": web.key,
        "public_web_partial_result": web.partial_result,
        "public_web_rendered_lines": len(web.rendered_lines),
        "public_web_model_route_checked": True,
        "public_http_checked": False,
        "public_root_complete": complete,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest": False,
        "gate": (
            "PASS_R53_GENERIC_PUBLIC_ROOT_COMPLETE_HTTP_PENDING"
            if complete and web_complete else
            "PASS_R53_PUBLIC_ROOT_STILL_UNRESOLVED"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    observations = None if args.dry_run else inspect_public_root_completion()
    gate = ("PASS_R53_SOURCE_PREFLIGHT" if args.dry_run else observations["gate"])
    report = {
        "phase": "174-R3-R7-R53",
        "state": state,
        "observations": observations,
        "gate": gate,
    }
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r53"
    )
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / ("preflight.json" if args.dry_run else "public_source_bound_root.json")
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R53_"
    for name, value in state.items():
        print(prefix + name.upper() + "=" + str(value))
    if observations is not None:
        for name, value in observations.items():
            print(prefix + name.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
