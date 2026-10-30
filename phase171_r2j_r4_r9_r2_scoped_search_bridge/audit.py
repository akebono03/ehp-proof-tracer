"""Phase 171 R2J-R4-R9-R2: scoped canonical search, no production changes.

R4-R8 supplies a validated *rule graph*; every conclusion is re-derived by the
normal registered-goal engine from publication-screened sources.  Completion
and trust-boundary acceptance are reported separately and never fabricated.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import (
    inference_expansion_catalog,
    scoped_expansion_provider,
    walk_proof_ancestry,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in allowed:
        raise ValueError("only read-only Git commands are permitted")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT,
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def replay_scoped_search() -> dict:
    screened, target, citing_id = _screened_context()
    root, _, r8_report = build_cyclic_pi63_proof()
    if (root.conclusion != target or root.rule is not ProofRule.INFERENCE
            or r8_report["new_given_added"] != 0):
        raise RuntimeError("R4-R8 did not prove the positioned registered goal")

    catalog = inference_expansion_catalog(root)
    ordinary = shared_expansion_provider(screened, proof_target=target)
    scoped = scoped_expansion_provider(root, ordinary)
    root_proposals = scoped(target)
    if (len(root_proposals) != 1
            or root_proposals[0].subgoals != tuple(
                parent.conclusion for parent in root.premises
            )):
        raise RuntimeError("scoped route does not match the R4-R8 root")

    result = search_registered_partial_proof(
        n=3, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing_id,
        expansion_provider=scoped,
        lookup_mode="typed_reference_publication",
    )
    complete = (result.status is ProofSearchStatus.COMPLETE
                and result.conclusion == target and not result.open_goals)
    verified = False
    verification_result = None
    if complete:
        try:
            verification_result = verify_proof_tree_for_narrative(
                result, screened, citing_assertion_id=citing_id,
            )
            verified = True
        except UnverifiedProofTree as error:
            verification_result = str(error)
    original_nodes = walk_proof_ancestry(root)
    if not original_nodes or len(catalog) < 2:
        raise RuntimeError("original inferred proof graph disappeared")
    # A limited-phase audit cannot confer a public COMPLETE status.  This
    # report never substitutes its scoped result into Web or production.
    return {
        "phase": "171-R2J-R4-R9-R2",
        "mode": "AUDIT_ONLY_SCOPED_CANONICAL_SEARCH",
        "target": repr(target),
        "citing_assertion_id": citing_id,
        "r8_inferred": True,
        "r8_rule_catalog_size": len(catalog),
        "r8_given_leaves": sum(node.rule is ProofRule.GIVEN for node in original_nodes),
        "scoped_root_options": len(root_proposals),
        "scoped_search_status": result.status.value,
        "scoped_search_complete": complete,
        "scoped_search_proven_steps": len(result.proven_steps),
        "scoped_open_goals": [repr(item)[:600] for item in result.open_goals[:20]],
        "scoped_diagnostics": list(result.diagnostics[:20]),
        "trust_boundary_accepted": verified,
        "trust_boundary_result": verification_result,
        "public_provider_modified": False,
        "public_web_verified": False,
        "new_given_added": 0,
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
        raise RuntimeError("R9-R2 requires develop")
    for required in (
        "phase171_r2j_r4_r8_cyclic_structure/audit.py",
        "phase171_r2j_r4_r7_nonzero_nu_order/audit.py",
    ):
        if not (ROOT / required).is_file():
            raise RuntimeError("missing R4 prerequisite: " + required)
    print("PHASE171_R2J_R4_R9_R2_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R2_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R2_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = replay_scoped_search()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked working tree changed during audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R9_R2_RULE_CATALOG=" + str(report["r8_rule_catalog_size"]), flush=True)
    print("PHASE171_R2J_R4_R9_R2_SCOPED_SEARCH=" + report["scoped_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R2_TRUST_VERIFIED=" + str(report["trust_boundary_accepted"]), flush=True)
    print("PHASE171_R2J_R4_R9_R2_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R2_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R2_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R2_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R2_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
