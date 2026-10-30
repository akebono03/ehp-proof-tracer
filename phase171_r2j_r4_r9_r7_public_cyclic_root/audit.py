"""Measure real shared-provider root integration and public search state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r1_public_path_audit.audit import has_exact_root_route
from phase171_r2j_r4_r9_r7_public_cyclic_root.source import expand_cited_double_cyclic_root
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*args: str) -> str:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
    }
    if args not in permitted:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout.strip()


def inspect_public_root() -> dict:
    screened, goal, _ = _screened_context()
    root, _, report = build_cyclic_pi63_proof()
    if root.rule is not ProofRule.INFERENCE or report["new_given_added"] != 0:
        raise RuntimeError("R4-R8 original root is not independently proved")
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    candidates = expand_cited_double_cyclic_root(goal, available)
    if not has_exact_root_route(candidates, root):
        raise RuntimeError("source-anchored generic root did not match R4-R8")
    public = shared_expansion_provider(screened, proof_target=goal)(goal)
    if not has_exact_root_route(public, root):
        raise RuntimeError("new generic root is absent from shared provider")
    # Observe the real public engine; no results or inferred ProofSteps injected.
    actual = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=goal,
    )
    return {
        "phase": "171-R2J-R4-R9-R7",
        "mode": "GENERIC_PUBLIC_ROOT_CONNECTION_ONLY",
        "source_anchored_root_options": len(candidates),
        "shared_root_expansion_count": len(public),
        "shared_root_connected": True,
        "target": repr(goal),
        "root_rule_name": root.inference_rule.name,
        "canonical_public_status": actual.status.value,
        "public_complete": actual.status.value == "complete" and actual.conclusion == goal,
        "open_goals": [repr(x)[:900] for x in actual.open_goals[:15]],
        "diagnostics": list(actual.diagnostics[:15]),
        "new_given_added": 0,
        "completed_proof_imported": False,
        "trust_boundary_modified": False,
        "web_modified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print("PHASE171_R2J_R4_R9_R7_BRANCH=" + _git("branch", "--show-current"), flush=True)
    print("PHASE171_R2J_R4_R9_R7_HEAD=" + _git("rev-parse", "HEAD"), flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R7_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_public_root()
    OUTPUT.mkdir(exist_ok=True)
    dest = OUTPUT / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R7_SOURCE_ANCHORED_ROOT=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R7_SHARED_ROOT_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R7_PUBLIC_SEARCH=" + report["canonical_public_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R7_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    print("PHASE171_R2J_R4_R9_R7_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R7_REPORT=" + str(dest), flush=True)
    print("PHASE171_R2J_R4_R9_R7_RESULT=PASS_ROOT_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
