"""Phase 175 R13R4: install and audit general H-zero intermediate candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import traceback

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase175_r4r12r13r4_hopf_zero_public import installer
from phase175_r4r12r13r4_hopf_zero_public.rule import (
    DELTA_TO_H_ZERO, H_ZERO_TO_E_SURJ, hopf_zero_inputs,
    suspension_surjective_inputs,
)

PACKAGE = "phase175_r4r12r13r4_hopf_zero_public"


def git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", check=False)
    if done.returncode:
        raise RuntimeError("R13R4_GIT_FAILURE: " + " ".join(args) + " " + done.stderr.strip())
    return done.stdout.strip()


def audit_frontier() -> dict[str, object]:
    """Observe actual shared proposals; NEVER count a proposal as proof."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    e_goal = MapSurjective(TodaSuspensionMap(
        TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5),
    ))
    inputs = suspension_surjective_inputs(e_goal)
    if inputs is None:
        raise RuntimeError("R13R4_INVALID_EHP_GOAL")
    h_goal = inputs[0]
    delta_goal = hopf_zero_inputs(h_goal)
    if delta_goal is None:
        raise RuntimeError("R13R4_INVALID_H_DELTA_GOAL")
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase165_r52_r9_shared_math import shared_expansion_provider
    target = exact_prior_database_result(5, 4)
    if target is None:
        raise RuntimeError("R13R4_MISSING_TYPED_TARGET")
    bridge = build_shared_typed_bridge()
    expand = shared_expansion_provider(bridge, proof_target=target)
    e_options = tuple(expand(e_goal))
    h_options = tuple(expand(h_goal))
    delta_options = tuple(expand(delta_goal[0]))
    selected_e = tuple(x for x in e_options if x.rule.name == H_ZERO_TO_E_SURJ)
    selected_h = tuple(x for x in h_options if x.rule.name == DELTA_TO_H_ZERO)
    if len(selected_e) != 1 or len(selected_h) != 1:
        raise RuntimeError("R13R4_PUBLIC_H_ZERO_CHAIN_MISSING")
    if selected_e[0].subgoals != inputs or selected_h[0].subgoals != delta_goal:
        raise RuntimeError("R13R4_INCORRECT_PARENT_GOALS")
    return {
        "e_surjectivity_new_candidates": len(selected_e),
        "hopf_zero_new_candidates": len(selected_h),
        "delta_injectivity_candidates": len(delta_options),
        "hopf_zero_goal": repr(h_goal),
        "delta_injectivity_goal": repr(delta_goal[0]),
        "actual_recursive_proof_executed": False,
        "hopf_zero_proved": False,
        "e_surjectivity_proved": False,
        "target_group_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {
        "phase": "175-R4R12R13R4", "dry_run": dry_run,
        "gate": "FAIL_R13R4", "new_given": 0,
        "new_mathematical_rules": 2,
        "new_axioms": 0,
        "new_generic_inference_connections": 2,
        "full_pytest_executed": False,
        "target_proof_complete": False,
    }
    try:
        if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
            raise RuntimeError("R13R4_WRONG_REPOSITORY_ROOT")
        if git(root, "branch", "--show-current") != "develop":
            raise RuntimeError("R13R4_WRONG_BRANCH")
        result["head"] = git(root, "rev-parse", "HEAD")
        result["install"] = installer.install(root, dry_run=dry_run, output=output)
        if not dry_run:
            result["frontier"] = audit_frontier()
        result["gate"] = ("PASS_R13R4_DRYRUN_NOT_COMPLETE" if dry_run
                          else "PASS_R13R4_ZERO_HOPF_PUBLIC_CANDIDATES_NOT_COMPLETE")
    except Exception as exc:
        result["error"] = type(exc).__name__ + ": " + str(exc)
        result["traceback"] = traceback.format_exc()[-6000:]
    path = output / ("dry_run_report.json" if dry_run else "report.json")
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PHASE175_R13R4_GATE=" + str(result["gate"]))
    print("PHASE175_R13R4_HEAD=" + str(result.get("head", "UNVERIFIED")))
    if "frontier" in result:
        print("PHASE175_R13R4_H_ZERO_CANDIDATES=" + str(result["frontier"]["hopf_zero_new_candidates"]))
        print("PHASE175_R13R4_E_CANDIDATES=" + str(result["frontier"]["e_surjectivity_new_candidates"]))
        print("PHASE175_R13R4_DELTA_CANDIDATES=" + str(result["frontier"]["delta_injectivity_candidates"]))
    print("PHASE175_R13R4_NEW_GIVEN=0")
    print("PHASE175_R13R4_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R4_REPORT=" + str(path))
    if "error" in result:
        print("PHASE175_R13R4_ERROR=" + str(result["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
