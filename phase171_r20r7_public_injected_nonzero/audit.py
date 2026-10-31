"""Read-only confirmation of the public E-injectivity/nonzero-generator route."""
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
from phase171_r20r7_public_injected_nonzero.install import checked_worktree
from proof import ProofRule, find_inference_matches_for_rule

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def audit() -> dict:
    """Compare only verified proposal semantics, not an injected completed proof."""
    head, _, _, _ = checked_worktree()
    before = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    screened, target, _ = _screened_context()
    doubled, order_four, nodes, old_report = build_nonzero_nu_order_proof()
    if (
        doubled.rule is not ProofRule.INFERENCE
        or order_four.rule is not ProofRule.INFERENCE
        or old_report["new_given_added"] != 0
        or old_report["nu_prime_order_four_proven"] is not True
        or not nodes
    ):
        raise RuntimeError("independent R4-R7 inference ancestry is invalid")
    nonzero = doubled.premises[1]
    if nonzero.rule is not ProofRule.INFERENCE or len(nonzero.premises) != 2:
        raise RuntimeError("the independently proved E-image nonzero node is missing")
    provider = shared_expansion_provider(screened, proof_target=target)
    proposed = provider(nonzero.conclusion)
    if not isinstance(proposed, tuple):
        raise RuntimeError("shared provider returned invalid options")
    matched = tuple(
        option for option in proposed
        if option.rule.name == nonzero.inference_rule.name
        and option.subgoals == tuple(parent.conclusion for parent in nonzero.premises)
    )
    certified = 0
    for option in matched:
        matches = find_inference_matches_for_rule(option.rule, nonzero.premises)
        if any(
            tuple(match.premises) == nonzero.premises
            and derive_inference_proof_step(match).conclusion == nonzero.conclusion
            for match in matches
        ):
            certified += 1
    if certified != 1:
        raise RuntimeError("a unique certified injected nonzero public proposal was not found")
    after = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    if before != after:
        raise RuntimeError("tracked worktree changed during read-only audit")
    return {
        "phase": "171-R20R7",
        "mode": "READ_ONLY_PUBLIC_INJECTED_NONZERO_CONNECTION",
        "git_head": head,
        "nonzero_goal": repr(nonzero.conclusion),
        "source_and_injectivity_subgoals": [repr(x.conclusion) for x in nonzero.premises],
        "provider_options": len(proposed),
        "matching_options": len(matched),
        "certified_options": certified,
        "injected_eta_image_nonzero": "CERTIFIED_PUBLIC_PROPOSAL_PRESENT",
        "nu_order_four_rule_connected": True,
        "not_yet_connected": ["double_nonzero", "typed_double_equality"],
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
    print("PHASE171_R20R7_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R20R7_DRY_RUN=PASS", flush=True)
        return
    report = audit()
    directory = PACKAGE / "output" / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    directory.mkdir(parents=True, exist_ok=False)
    dest = directory / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20R7_INJECTED_ETA_IMAGE_NONZERO=" + report["injected_eta_image_nonzero"], flush=True)
    print("PHASE171_R20R7_NU_ORDER_FOUR=RULE_CONNECTED", flush=True)
    print("PHASE171_R20R7_NOT_YET_CONNECTED=" + ",".join(report["not_yet_connected"]), flush=True)
    print("PHASE171_R20R7_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R7_PUBLIC_COMPLETE_ASSERTED=False", flush=True)
    print("PHASE171_R20R7_REPORT=" + str(dest), flush=True)
    print("PHASE171_R20R7_RESULT=PASS_IMAGE_NONZERO_CONNECTED", flush=True)


if __name__ == "__main__":
    main()
