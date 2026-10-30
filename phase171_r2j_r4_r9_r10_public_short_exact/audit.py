"""Audit canonical EHP short-exact backward proposals after R10 integration.

An earlier fully inferred R4-R5 tree is used only to check the proposed rule
and subgoal shape. The public search is run independently, never fed that tree.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r5_short_exact_sequence.audit import build_short_exact_proof
from phase171_r2j_r4_r5_short_exact_sequence.source import expand_ehp_short_exact
from proof import ProofRule, find_inference_matches_for_rule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()


def equivalent_short_exact_routes(options: tuple, root: object) -> int:
    """Count exactly matching rule-and-subgoal routes (not rule names alone)."""
    return sum(
        option.rule.name == root.inference_rule.name
        and option.subgoals == tuple(parent.conclusion for parent in root.premises)
        for option in options
    )


def inspect_public_short_exact() -> dict:
    """Require a genuine original inference and independently query public search."""
    screened, target, _ = _screened_context()
    short_exact_root, ancestors, original_report = build_short_exact_proof()
    if (
        short_exact_root.rule is not ProofRule.INFERENCE
        or short_exact_root.inference_rule is None
        or len(short_exact_root.premises) != 3
        or any(parent.rule is not ProofRule.INFERENCE for parent in short_exact_root.premises)
        or original_report["new_given_added"] != 0
        or not ancestors
        or any(node.conclusion == target for node in ancestors)
    ):
        raise RuntimeError("R4-R5 short exact proof ancestry is untrusted")
    expected = expand_ehp_short_exact(short_exact_root.conclusion)
    if len(expected) != 1 or equivalent_short_exact_routes(expected, short_exact_root) != 1:
        raise RuntimeError("existing generic short-exact rule is unavailable")
    shared = shared_expansion_provider(screened, proof_target=target)(
        short_exact_root.conclusion,
    )
    if equivalent_short_exact_routes(shared, short_exact_root) != 1:
        raise RuntimeError("common provider did not expose exactly one EHP short-exact route")
    matches = tuple(
        match for match in find_inference_matches_for_rule(
            expected[0].rule, short_exact_root.premises,
        ) if match.premises == short_exact_root.premises
    )
    if len(matches) != 1:
        raise RuntimeError("short exact inference failed matching real R4-R5 premises")
    derived = derive_inference_proof_step(matches[0])
    if derived.rule is not ProofRule.INFERENCE or derived.conclusion != short_exact_root.conclusion:
        raise RuntimeError("generic rule failed to infer the short exact conclusion")
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
    )
    complete = (public.status.value == "complete" and public.conclusion == target
                and not public.open_goals)
    return {
        "phase": "171-R2J-R4-R9-R10",
        "mode": "PUBLIC_SHORT_EXACT_PROPOSAL_INTEGRATION",
        "short_exact_goal": repr(short_exact_root.conclusion),
        "proof_rule": short_exact_root.inference_rule.name,
        "original_source_inferences": original_report["inferences"],
        "original_source_given": original_report["given_leaves"],
        "short_exact_proposed": True,
        "short_exact_inference_matched": True,
        "shared_short_exact_connected": True,
        "shared_short_exact_route_count": equivalent_short_exact_routes(shared, short_exact_root),
        "short_exact_subgoals": [repr(item) for item in expected[0].subgoals],
        "public_search_status": public.status.value,
        "public_complete": complete,
        "public_proven_steps": len(public.proven_steps),
        "public_open_goals": [repr(item)[:1500] for item in public.open_goals[:20]],
        "public_diagnostics": list(public.diagnostics[:20]),
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
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if branch != "develop":
        raise RuntimeError("develop branch required")
    print("PHASE171_R2J_R4_R9_R10_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R10_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R10_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_public_short_exact()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files changed during read-only audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R10_SHORT_EXACT_INFERENCE=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R10_SHARED_SHORT_EXACT_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R10_PUBLIC_SEARCH=" + report["public_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R10_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    if report["public_open_goals"]:
        print("PHASE171_R2J_R4_R9_R10_FIRST_OPEN_GOAL=" + report["public_open_goals"][0], flush=True)
    print("PHASE171_R2J_R4_R9_R10_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R10_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R10_REPORT=" + str(path), flush=True)
    print("PHASE171_R2J_R4_R9_R10_RESULT=PASS_SHORT_EXACT_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
