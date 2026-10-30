"""Audit real public cardinality expansion against independent R4-R6 evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r8_public_cardinality.source import (
    expand_cited_ehp_middle_cardinality,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*args: str) -> str:
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
    }
    if args not in allowed:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()


def has_exact_proposal(options: tuple, reference: object) -> bool:
    """Check one existing inferred rule and its ordered typed subgoals."""
    return sum(
        option.rule.name == reference.inference_rule.name
        and option.subgoals == tuple(item.conclusion for item in reference.premises)
        for option in options
    ) == 1


def inspect_public_cardinality() -> dict:
    screened, target, _ = _screened_context()
    original_root, _, original_report = build_cyclic_pi63_proof()
    if (
        original_root.rule is not ProofRule.INFERENCE
        or original_root.conclusion != target
        or original_report["new_given_added"] != 0
    ):
        raise RuntimeError("original R4-R8 proof must be independently inferred")
    cardinality_step = original_root.premises[0]
    if cardinality_step.rule is not ProofRule.INFERENCE:
        raise RuntimeError("original middle-group cardinality was not inferred")
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    derived_options = expand_cited_ehp_middle_cardinality(
        cardinality_step.conclusion, available,
    )
    if not has_exact_proposal(derived_options, cardinality_step):
        raise RuntimeError("generic end-group source candidates do not match R4-R6")
    shared = shared_expansion_provider(screened, proof_target=target)
    production_options = shared(cardinality_step.conclusion)
    if not has_exact_proposal(production_options, cardinality_step):
        raise RuntimeError("cardinality obligation is absent from the shared provider")
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
    )
    return {
        "phase": "171-R2J-R4-R9-R8",
        "mode": "GENERIC_PUBLIC_CARDINALITY_CONNECTION_ONLY",
        "registered_group_goal": repr(target),
        "cardinality_goal": repr(cardinality_step.conclusion),
        "source_anchored_cardinality_routes": len(derived_options),
        "shared_cardinality_routes": len(production_options),
        "shared_cardinality_connected": True,
        "short_exact_subgoal": repr(derived_options[0].subgoals[1]),
        "left_end_group": repr(derived_options[0].subgoals[0]),
        "right_end_group": repr(derived_options[0].subgoals[2]),
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
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("develop branch required")
    print("PHASE171_R2J_R4_R9_R8_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R8_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R8_RESULT=PASS_DRY_RUN", flush=True)
        return
    result = inspect_public_cardinality()
    result["git_head"] = head
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R8_SOURCE_ANCHORED_CARDINALITY=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R8_SHARED_CARDINALITY_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R8_PUBLIC_SEARCH=" + result["public_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R8_PUBLIC_COMPLETE=" + str(result["public_complete"]), flush=True)
    if result["public_open_goals"]:
        print("PHASE171_R2J_R4_R9_R8_FIRST_OPEN_GOAL=" + result["public_open_goals"][0], flush=True)
    print("PHASE171_R2J_R4_R9_R8_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R8_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R8_RESULT=PASS_CARDINALITY_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
