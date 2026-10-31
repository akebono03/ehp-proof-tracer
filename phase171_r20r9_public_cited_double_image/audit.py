"""Read-only public cited double-image inference and genuine search audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r3_double_image_bridge.audit import build_double_image_proof
from phase171_r20r9_public_cited_double_image.install import checked_worktree
from proof import ProofRule, find_inference_matches_for_rule

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def audit_public_double() -> dict:
    """Check inference proposals and run public search without importing old proofs."""
    head, _, _, _ = checked_worktree()
    before = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    screened, target, _ = _screened_context()
    old_root, old_nodes, old_report = build_double_image_proof()
    if (
        old_root.rule is not ProofRule.INFERENCE
        or old_report["new_given_added"] != 0
        or len(old_root.premises) != 2
        or old_root.premises[0].rule is not ProofRule.GIVEN
        or old_root.premises[1].rule is not ProofRule.INFERENCE
        or not old_nodes
    ):
        raise RuntimeError("independent R4-R3 typed-double proof ancestry invalid")
    options = shared_expansion_provider(screened, proof_target=target)(old_root.conclusion)
    matching = tuple(
        item for item in options
        if item.rule.name == old_root.inference_rule.name
        and item.subgoals == tuple(parent.conclusion for parent in old_root.premises)
    )
    certified = 0
    for item in matching:
        for match in find_inference_matches_for_rule(item.rule, old_root.premises):
            if (
                tuple(match.premises) == old_root.premises
                and derive_inference_proof_step(match).conclusion == old_root.conclusion
            ):
                certified += 1
                break
    if not matching or not certified:
        raise RuntimeError("public typed-double image proposal missing or cannot match inference")
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
    )
    public_complete = (
        public.status.value == "complete"
        and public.conclusion == target
        and not public.open_goals
    )
    after = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    if before != after:
        raise RuntimeError("tracked worktree changed during public proof audit")
    return {
        "phase": "171-R20R9",
        "mode": "PUBLIC_TYPED_DOUBLE_IMAGE_ROUTE_AUDIT",
        "git_head": head,
        "typed_double_inference_matching_proposals": len(matching),
        "typed_double_inference_certified_proposals": certified,
        "typed_double_equality": "CERTIFIED_PUBLIC_PROPOSAL_PRESENT",
        "public_status": public.status.value,
        "public_complete": public_complete,
        "public_open_goals": [repr(goal)[:1500] for goal in public.open_goals[:12]],
        "public_diagnostics": list(public.diagnostics[:12]),
        "new_given_added": 0,
        "completed_proofs_imported": False,
        "web_verified": False,
        "tracked_worktree_unchanged": True,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head, _, _, _ = checked_worktree()
    print("PHASE171_R20R9_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R20R9_DRY_RUN=PASS", flush=True)
        return
    report = audit_public_double()
    folder = PACKAGE / "output" / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    folder.mkdir(parents=True, exist_ok=False)
    dest = folder / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20R9_TYPED_DOUBLE_EQUALITY=" + report["typed_double_equality"], flush=True)
    print("PHASE171_R20R9_PUBLIC_STATUS=" + report["public_status"], flush=True)
    print("PHASE171_R20R9_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    print("PHASE171_R20R9_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R9_REPORT=" + str(dest), flush=True)
    print("PHASE171_R20R9_RESULT=PASS_TYPED_DOUBLE_ROUTE_CONNECTED", flush=True)


if __name__ == "__main__":
    main()
