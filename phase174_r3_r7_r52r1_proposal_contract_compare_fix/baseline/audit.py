"""R52: measure a generic SourceBoundGoal wrapper against the real public route.

No installation, direct mathematical assertions, Web overrides or fake proofs.
A candidate is not a proof: report the actual verified canonical DFS status.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r52_public_kernel_source_bound_probe.source_guard import verify_checkout


def inspect_public_kernel_source_bound_probe() -> dict[str, object]:
    """Run a fresh ordinary DFS with only the cited kernel-domain preference."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r3_recursive_search import SourceBoundGoal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME as ROOT_RULE, ehp_zero_inputs
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import upper_delta_surjectivity_inputs
    from phase174_r3_r7_r52_public_kernel_source_bound_probe.probe import (
        build_source_bound_kernel_probe,
    )
    from proof import ProofRule, ProofStep
    from web_group_proof import build_standard_web_group_proof_view

    n, k = 7, 5
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + k, n))
    original_bridge = build_shared_typed_bridge()
    contexts: list[object] = []
    public_result = search_group_from_registered_goal(
        n=n, k=k, bridge=original_bridge, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("R52 cannot identify the actual screened public context")
    screened = contexts[0]
    original = shared_expansion_provider(screened, proof_target=goal)
    probe = build_source_bound_kernel_probe(original, screened)
    root_options = tuple(x for x in original(goal) if x.rule.name == ROOT_RULE)
    if len(root_options) != 1 or root_options[0].subgoals != ehp_zero_inputs(goal):
        raise RuntimeError("R52 public root expansion changed")
    upper_options = upper_delta_surjectivity_inputs(root_options[0].subgoals[0])
    if upper_options is None:
        raise RuntimeError("R52 upper Delta typed prerequisites changed")
    kernel_goal = upper_options[2]
    if type(kernel_goal) is not KernelMultipleStatement:
        raise RuntimeError("R52 expected a typed R35 kernel obligation")
    original_kernel = tuple(x for x in original(kernel_goal) if x.rule.name == KERNEL_RULE)
    augmented = tuple(x for x in probe(kernel_goal) if x.rule.name == KERNEL_RULE)
    bound = tuple(x for x in augmented if any(
        isinstance(s, SourceBoundGoal) for s in x.subgoals
    ))
    if len(original_kernel) != 1:
        raise RuntimeError("R52 expected exactly one public R35 kernel proposal")
    if any(x.rule.name != KERNEL_RULE for x in bound):
        raise RuntimeError("R52 changed a non-R35 inference")
    if probe(goal) != original(goal):
        raise RuntimeError("R52 changed the public root expansion")
    citing_id = next(iter(original_bridge.registry._assertions)).assertion_id
    probed = search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=screened,
        citing_assertion_id=citing_id, expansion_provider=probe,
        lookup_mode="typed_reference",
    )
    root_steps = tuple(step for step in probed.proven_steps
                       if step.conclusion == goal and step.rule is ProofRule.INFERENCE)
    kernel_steps = tuple(step for step in probed.proven_steps
                         if step.conclusion == kernel_goal and step.rule is ProofRule.INFERENCE)
    domain_step_is_inferred = any(
        len(step.premises) == 3
        and step.premises[0].rule is ProofRule.INFERENCE
        and step.premises[1].rule is ProofRule.GIVEN
        and step.premises[2].rule is ProofRule.GIVEN
        for step in kernel_steps
    )
    root_has_four_inferred = any(
        len(step.premises) == 4
        and tuple(parent.conclusion for parent in step.premises) == root_options[0].subgoals
        and all(parent.rule is ProofRule.INFERENCE for parent in step.premises)
        for step in root_steps
    )
    expected_locators = {
        "(5.9)", "Proposition 4.2 (4.4)",
        "Proposition 5.8", "(5.10)",
        "Proposition 2.7", "(5.1)",
    }
    def ancestor_locators(step: ProofStep) -> set[str]:
        found: set[str] = set()
        visited: set[int] = set()
        def visit(current: ProofStep) -> None:
            if id(current) in visited:
                return
            visited.add(id(current))
            if current.rule is ProofRule.GIVEN:
                cite = getattr(getattr(current.inference_rule, "literature_reference", None),
                               "locator", None)
                if isinstance(cite, str):
                    found.add(cite)
            for parent in current.premises:
                visit(parent)
        visit(step)
        return found
    matching_citations = any(expected_locators.issubset(ancestor_locators(step))
                             for step in root_steps)
    actual_complete = probed.status is ProofSearchStatus.COMPLETE
    if actual_complete and (probed.conclusion != goal or not root_has_four_inferred
                            or not matching_citations or not domain_step_is_inferred):
        raise RuntimeError("R52 claims completion without the actual verified EHP root")
    if root_steps and not actual_complete:
        raise RuntimeError("R52 observed a root inference but returned partial status")
    web = build_standard_web_group_proof_view(
        n=n, k=k, mode="narrative", citation_source="model",
    )
    if (web.partial_result != (public_result.status is not ProofSearchStatus.COMPLETE)):
        raise RuntimeError("R52 public model and group search disagree")
    gate = (
        "PASS_R52_GENERIC_BOUND_PUBLIC_PROVIDER_PROBE_COMPLETE_NOT_INSTALLED"
        if actual_complete and bound else
        "PASS_R52_GENERIC_BOUND_ADDITIONAL_PUBLIC_GAP_IDENTIFIED"
    )
    return {
        "root": "pi_12^7 = 0",
        "public_status": public_result.status.value,
        "public_verified_steps": len(public_result.proven_steps),
        "public_web_key": web.key,
        "public_web_partial_result": web.partial_result,
        "public_web_http_checked": False,
        "public_provider_unchanged": True,
        "public_r35_unbound_candidates": len(original_kernel),
        "probe_r35_source_bound_candidates": len(bound),
        "probe_generic_rule_name": KERNEL_RULE,
        "probe_root_candidate_unchanged": True,
        "probe_status": probed.status.value,
        "probe_verified_steps": len(probed.proven_steps),
        "probe_open_goal_types": dict(sorted(Counter(type(x).__name__ for x in probed.open_goals).items())),
        "probe_proven_goal_types": dict(sorted(Counter(type(x.conclusion).__name__
                                                   for x in probed.proven_steps).items())),
        "probe_diagnostics": list(probed.diagnostics),
        "probe_kernel_inference_count": len(kernel_steps),
        "probe_kernel_domain_inferred": domain_step_is_inferred,
        "probe_root_inference_count": len(root_steps),
        "probe_root_four_inferred_parents": root_has_four_inferred,
        "probe_root_six_cited_ancestors": matching_citations,
        "probe_root_complete": actual_complete and root_has_four_inferred and matching_citations,
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
    observations = None if args.dry_run else inspect_public_kernel_source_bound_probe()
    gate = "PASS_R52_REVIEWED_R51_PREFLIGHT" if args.dry_run else observations["gate"]
    report = {
        "phase": "174-R3-R7-R52",
        "state": state,
        "observations": observations,
        "gate": gate,
    }
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r52"
    )
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / ("preflight.json" if args.dry_run else "public_kernel_bound_probe.json")
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R52_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if observations is not None:
        for key, value in observations.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
