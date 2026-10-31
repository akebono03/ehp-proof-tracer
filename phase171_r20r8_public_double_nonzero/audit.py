"""Read-only verification of public nonzero-double backward proposal."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r7_nonzero_nu_order.audit import build_nonzero_nu_order_proof
from phase171_r20r8_public_double_nonzero.install import checked_worktree
from proof import ProofRule, find_inference_matches_for_rule

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def audit() -> dict:
    """Use old proof only as an independent oracle, not as a search premise."""
    head, _, _, _ = checked_worktree()
    before = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    screened, target, _ = _screened_context()
    doubled, order, nodes, report = build_nonzero_nu_order_proof()
    if (
        doubled.rule is not ProofRule.INFERENCE
        or order.rule is not ProofRule.INFERENCE
        or report["new_given_added"] != 0
        or len(doubled.premises) != 2
        or any(parent.rule is not ProofRule.INFERENCE for parent in doubled.premises)
        or not nodes
    ):
        raise RuntimeError("the previously established R4-R7 proof ancestry is invalid")
    provider = shared_expansion_provider(screened, proof_target=target)
    proposals = provider(doubled.conclusion)
    matching = tuple(
        proposal for proposal in proposals
        if proposal.rule.name == doubled.inference_rule.name
        and proposal.subgoals == tuple(parent.conclusion for parent in doubled.premises)
    )
    certified = 0
    for proposal in matching:
        matches = find_inference_matches_for_rule(proposal.rule, doubled.premises)
        for match in matches:
            if (
                tuple(match.premises) == doubled.premises
                and derive_inference_proof_step(match).conclusion == doubled.conclusion
            ):
                certified += 1
                break
    if len(matching) != 1 or certified != 1:
        raise RuntimeError(
            "public nonzero-double route missing or not certified: "
            + str((len(proposals), len(matching), certified))
        )
    after = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    if before != after:
        raise RuntimeError("tracked worktree changed during read-only audit")
    return {
        "phase": "171-R20R8",
        "mode": "PUBLIC_NONZERO_DOUBLE_PROPOSAL_ONLY",
        "git_head": head,
        "nonzero_double_goal": repr(doubled.conclusion),
        "matching_proposals": len(matching),
        "certified_proposals": certified,
        "nonzero_double": "CERTIFIED_PUBLIC_PROPOSAL_PRESENT",
        "typed_double_equality_connected": False,
        "new_given_added": 0,
        "completed_proofs_imported": False,
        "public_complete_asserted": False,
        "web_verified": False,
        "tracked_worktree_unchanged": True,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head, _, _, _ = checked_worktree()
    print("PHASE171_R20R8_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R20R8_DRY_RUN=PASS", flush=True)
        return
    report = audit()
    directory = PACKAGE / "output" / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    directory.mkdir(parents=True, exist_ok=False)
    dest = directory / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20R8_DOUBLE_NONZERO=" + report["nonzero_double"], flush=True)
    print("PHASE171_R20R8_TYPED_DOUBLE_EQUALITY=NOT_YET_CONNECTED", flush=True)
    print("PHASE171_R20R8_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R8_PUBLIC_COMPLETE_ASSERTED=False", flush=True)
    print("PHASE171_R20R8_REPORT=" + str(dest), flush=True)
    print("PHASE171_R20R8_RESULT=PASS_DOUBLE_NONZERO_CONNECTED", flush=True)


if __name__ == "__main__":
    main()
