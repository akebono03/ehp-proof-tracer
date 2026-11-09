"""Audit actual R34 cited steps, R35 rule and R36 shared provider integration."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r36_cited_kernel_provider_wiring.install import verify_checkout

ROOT = Path(__file__).resolve().parents[1]


def audit_public_connection() -> dict[str, object]:
    """Require real screened source facts and reconstruct only cited inferences."""
    from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import checked_prior_statements
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME
    from proof import (
        ProofRule, Relation, RelationType, apply_inference_match,
        find_inference_matches_for_rule,
    )

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    cited_steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == screened.registry.assertion(link.assertion_id).content
    )
    codomain, signed_image = checked_prior_statements(ROOT)
    codomain_step = next((step for step in cited_steps if step.conclusion == codomain), None)
    image_step = next((step for step in cited_steps if step.conclusion == signed_image), None)
    if codomain_step is None or image_step is None or codomain_step is image_step:
        raise RuntimeError("R34 cited codomain / signed image must be two distinct steps")
    for step, locator in ((codomain_step, "Proposition 5.8"), (image_step, "(5.10)")):
        parent = step.inference_rule
        if (parent is None or parent.literature_reference is None
                or parent.literature_reference.locator != locator):
            raise RuntimeError("Missing independently cited source: " + locator)
    domain = signed_image.map.source_group
    diagonal = Relation(
        domain, FreeCyclicGroup(signed_image.element), RelationType.EQUALITY,
    )
    kernel_goal = KernelMultipleStatement(signed_image.map, domain, signed_image.element, 2)
    provider = shared_expansion_provider(screened, proof_target=root)
    proposals = tuple(
        item for item in provider(kernel_goal)
        if item.rule.name == RULE_NAME
        and item.subgoals == (diagonal, codomain, signed_image)
    )
    if not proposals:
        raise RuntimeError("R35 kernel rule not reached through the shared provider")
    diagonal_proposals = tuple(
        item for item in provider(diagonal)
        if item.rule.name == "generic cited typed scalar specialization"
        and len(item.subgoals) == 1
    )
    diagonal_step = None
    for proposal in diagonal_proposals:
        source_step = next(
            (step for step in cited_steps if step.conclusion == proposal.subgoals[0]),
            None,
        )
        if source_step is None or source_step.inference_rule is None:
            continue
        if source_step.inference_rule.literature_reference is None:
            continue
        matches = find_inference_matches_for_rule(proposal.rule, (source_step,))
        if not matches:
            continue
        candidate = apply_inference_match(matches[0])
        if candidate.rule is ProofRule.INFERENCE and candidate.conclusion == diagonal:
            diagonal_step = candidate
            break
    if diagonal_step is None:
        raise RuntimeError("Diagonal group cannot be inferred from a cited general source")
    matches = find_inference_matches_for_rule(
        proposals[0].rule, (diagonal_step, codomain_step, image_step),
    )
    if not matches:
        raise RuntimeError("Cited three-premise kernel inference did not match")
    inferred_kernel = apply_inference_match(matches[0])
    if (inferred_kernel.rule is not ProofRule.INFERENCE
            or inferred_kernel.conclusion != kernel_goal
            or inferred_kernel.premises != (diagonal_step, codomain_step, image_step)):
        raise RuntimeError("Kernel proof ancestry differs from the actual cited premises")
    if any(step.conclusion == kernel_goal or step.conclusion == root for step in cited_steps):
        raise RuntimeError("Forbidden kernel/root direct GIVEN was introduced")
    return {
        "screened_cited_codomain": 1,
        "screened_cited_generator_image": 1,
        "shared_kernel_proposals": len(proposals),
        "diagonal_source_inferred": True,
        "three_real_cited_premises_form_inference": True,
        "kernel_inference_in_audit": True,
        "kernel_inference_inserted_as_given": False,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def report(dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if not dry_run and state["tracked_mode"] != "INSTALLED":
        raise RuntimeError("Install R36 provider before running public audit")
    observations = None if dry_run else audit_public_connection()
    return {
        "phase": "174-R3-R7-R36",
        "git_state": state,
        "observations": observations,
        "new_givens": 0,
        "new_direct_kernel_givens": 0,
        "new_direct_root_givens": 0,
        "new_general_rules": 0,
        "shared_provider_connections": 1 if observations is not None else 0,
        "root_complete": False,
        "full_pytest": False,
        "gate": (
            "PASS_R36_SOURCE_PREFLIGHT_ONLY" if dry_run else
            "PASS_R36_CITED_CYCLIC_KERNEL_PUBLIC_PROVIDER_CONNECTED_ROOT_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(args.dry_run)
    outdir = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r36"
    )
    outdir.mkdir(parents=True, exist_ok=True)
    output = outdir / ("preflight.json" if args.dry_run else "public_kernel_provider.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R36_"
    for key, value in result["git_state"].items():
        if key != "reviewed_successor_files":
            print(p + key.upper() + "=" + str(value))
    if result["observations"] is not None:
        for key, value in result["observations"].items():
            print(p + key.upper() + "=" + str(value))
    print(p + "NEW_GIVENS=0")
    print(p + "NEW_MATH_RULES=0")
    print(p + "ROOT_COMPLETE=False")
    print(p + "FULL_PYTEST=False")
    print(p + "REPORT=" + str(output))
    print(p + "GATE=" + str(result["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
