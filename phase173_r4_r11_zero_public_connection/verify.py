"""Audit actual installed public zero proof and Web trust boundary."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import (
    exact_prior_database_result,
    verified_db_step,
)
from phase173_r4_r10_general_toda56_core.core import (
    GENERAL_ROOT_NAME,
    checked_general_inputs,
)
from phase173_r4_r11_zero_public_connection.install import git, preflight
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


def inspect_public_zero() -> dict[str, object]:
    """Require canonical public search, guarded root and verified model Web."""
    contexts: list[object] = []
    goal = exact_prior_database_result(4, 7)
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        raise RuntimeError("Registered pi_11^4 must be a zero-group goal")
    result = search_group_from_registered_goal(n=4, k=7, context_sink=contexts.append)
    roots = tuple(
        step for step in result.proven_steps
        if step.conclusion == goal
        and step.rule is ProofRule.INFERENCE
        and step.inference_rule is not None
        and step.inference_rule.name == GENERAL_ROOT_NAME
    )
    prior_certified = bool(
        len(contexts) == 1 and len(roots) == 1
        and len(roots[0].premises) == 4
        and roots[0].inference_rule.match_guard(roots[0].premises, {})
        and verified_db_step(roots[0].premises[1], proof_target=goal, bridge=contexts[0])
        and verified_db_step(roots[0].premises[2], proof_target=goal, bridge=contexts[0])
    )
    view = build_standard_web_group_proof_view(
        n=4, k=7, mode="narrative", max_depth=2, citation_source="model",
    )
    web_complete = bool(
        view.key == "generic-complete-proof"
        and not view.partial_result
        and view.steps
        and view.rendered_lines
    )
    passed = bool(
        result.status is ProofSearchStatus.COMPLETE
        and not result.open_goals
        and result.conclusion == goal
        and prior_certified and web_complete
    )
    return {
        "group": "pi_11^4",
        "status": result.status.value,
        "steps": len(result.proven_steps),
        "open_goals": len(result.open_goals),
        "root_certified": prior_certified,
        "web_complete": web_complete,
        "web_key": view.key,
        "passed": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    preflight(root, dry_run=False)
    baseline = git(root, "status", "--porcelain", "--untracked-files=no")
    row = inspect_public_zero()
    print("PHASE173_R4_R11_PUBLIC_STATUS=" + row["status"], flush=True)
    print("PHASE173_R4_R11_ROOT_CERTIFIED=" + str(row["root_certified"]), flush=True)
    print("PHASE173_R4_R11_OPEN=" + str(row["open_goals"]), flush=True)
    print("PHASE173_R4_R11_WEB_COMPLETE=" + str(row["web_complete"]), flush=True)
    print("PHASE173_R4_R11_WEB_KEY=" + row["web_key"], flush=True)
    goal12 = exact_prior_database_result(4, 8)
    epsilon_rejected = goal12 is not None and checked_general_inputs(goal12) is None
    print("PHASE173_R4_R11_EPSILON_UNPROVED_REJECTED=" + str(epsilon_rejected), flush=True)
    if baseline != git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Verification modified tracked sources")
    success = row["passed"] and epsilon_rejected
    report = Path(__file__).with_name("verification_result.json")
    report.write_text(json.dumps({
        "phase": "173 R4-R11",
        "mode": "STANDARD_PUBLIC_ZERO_GROUP_SEARCH_AND_WEB",
        "result": row,
        "epsilon_rejected": epsilon_rejected,
        "passed": success,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R11_REPORT=" + str(report), flush=True)
    print("PHASE173_R4_R11_RESULT=" + ("PASS" if success else "FAIL"), flush=True)
    return 0 if success else 2


if __name__ == "__main__":
    raise SystemExit(main())
