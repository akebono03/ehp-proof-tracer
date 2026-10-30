"""Audit public finite-cyclic-structure expansion using genuine R4-R8 sources."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import (
    expand_cited_full_order_cyclic_structure,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*args: str) -> str:
    if args not in {("branch", "--show-current"), ("rev-parse", "HEAD")}:
        raise ValueError("only read-only Git commands permitted")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.strip()


def matching_cyclic_route(options: tuple, parents: tuple[ProofStep, ...]) -> bool:
    """Require exactly one reconstructed route for the original two hypotheses."""
    return sum(
        proposal.rule.name
        == "proved finite cardinality and full element order imply cyclic structure"
        and proposal.subgoals == tuple(parent.conclusion for parent in parents)
        for proposal in options
    ) == 1


def inspect_public_cyclic_structure() -> dict:
    screened, target, _ = _screened_context()
    original, _, original_report = build_cyclic_pi63_proof()
    if (
        original.rule is not ProofRule.INFERENCE
        or original.conclusion != target
        or len(original.premises) != 2
        or original_report["new_given_added"] != 0
    ):
        raise RuntimeError("source R4-R8 proof must be genuine inference")
    goal = CyclicStructureStatement(
        target.lhs, target.rhs.generator, target.rhs.order,
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    proposed = expand_cited_full_order_cyclic_structure(goal, available)
    if not matching_cyclic_route(proposed, original.premises):
        raise RuntimeError("screened source lacks exact cyclic structure route")
    shared = shared_expansion_provider(screened, proof_target=target)(goal)
    if not matching_cyclic_route(shared, original.premises):
        raise RuntimeError("public provider lacks cyclic structure obligation")
    matches = tuple(
        item for item in find_inference_matches_for_rule(
            proposed[0].rule, original.premises,
        )
        if item.premises == original.premises
    )
    if len(matches) != 1:
        raise RuntimeError("full-order structure does not match genuine premises")
    structure_step = derive_inference_proof_step(matches[0])
    if (
        structure_step.conclusion != goal
        or structure_step.rule is not ProofRule.INFERENCE
        or structure_step.premises != original.premises
    ):
        raise RuntimeError("cyclic structure was not a real typed inference")
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
    )
    return {
        "phase": "171-R2J-R4-R9-R9",
        "mode": "PUBLIC_CYCLIC_STRUCTURE_PROPOSAL_ONLY",
        "registered_target": repr(target),
        "cyclic_structure_goal": repr(goal),
        "structure_inference_matched": True,
        "screened_structure_routes": len(proposed),
        "shared_structure_connected": True,
        "shared_structure_routes": len(shared),
        "structure_subgoals": [repr(item) for item in proposed[0].subgoals],
        "public_search_status": public.status.value,
        "public_complete": public.status.value == "complete" and public.conclusion == target,
        "public_open_goals": [repr(item)[:1200] for item in public.open_goals[:15]],
        "public_diagnostics": list(public.diagnostics[:15]),
        "new_given_added": 0,
        "completed_proof_imported": False,
        "web_modified": False,
        "trust_boundary_modified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch, head = _git("branch", "--show-current"), _git("rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("develop branch required")
    print("PHASE171_R2J_R4_R9_R9_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R9_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R9_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_public_cyclic_structure()
    report["git_head"] = head
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R9_STRUCTURE_INFERENCE=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R9_SHARED_STRUCTURE_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R9_PUBLIC_SEARCH=" + report["public_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R9_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    if report["public_open_goals"]:
        print("PHASE171_R2J_R4_R9_R9_FIRST_OPEN_GOAL=" + report["public_open_goals"][0], flush=True)
    print("PHASE171_R2J_R4_R9_R9_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R9_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R9_RESULT=PASS_STRUCTURE_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
