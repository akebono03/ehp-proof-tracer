"""Phase 173 R4-R9: read-only, source-pinned Toda (5.6) generalization audit.

This package does not create a proof, a source assertion, or a Group query result.
It only examines previously registered typed goals and independent prior order.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Any

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
)
from phase173_r4_r4_typed_generator_audit.audit import (
    _group_components,
    _map_components,
)
from phase173_r4_r6_alias_source_audit.audit import components_match_alias
from phase173_r4_r7_source_first_rule.rule import checked_inputs


REVIEWED_REMOTE_HEAD = "7158a7f544cd7c6750ebdf82a3b946caa980ea04"
PREVIOUS_REMOTE_HEAD = "72c66346b07cfc5517543627e010fd0db9842274"
REVIEWED_BLOBS = {
    "phase173_r4_r1_source_bound_56/rule.py": "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
    "phase173_r4_r7_source_first_rule/rule.py": "5113c88e263c28b748c1543ec57bbcedb3eff5bf",
    "phase173_r4_r7_source_first_rule/source.py": "abdc05c731e5ede1258962705bc577b5307b6f38",
    "phase173_r4_r1_narrative_source_fix/projection.py": "ef81a01df157075bc2a21b91bc4ad5fcd56d2cd1",
    "phase165_r52_r3_web_adapter.py": "cfe2c244567535ffaf1e1c2e3ac27dc539ed3c21",
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "phase173_r4_r8_public_connection/route.py": "06a402083a23595861f2856255947e4d26a2cc88",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase166_r3af_goal_adapter.py": "d85f595c9c8be18a2db760b8a20868b40eb15300",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
}


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed: {completed.stderr.strip()[:500]}"
        )
    return completed.stdout.strip()


def preflight(root: Path) -> dict[str, Any]:
    """Check all reviewed worktree bytes; do not reset, pull, stage or commit."""
    if Path(_git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("The audit must be located directly under the repository root")
    branch = _git(root, "branch", "--show-current")
    local_head = _git(root, "rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError(f"Expected develop, got {branch}")
    if local_head not in (PREVIOUS_REMOTE_HEAD, REVIEWED_REMOTE_HEAD):
        raise RuntimeError(f"Unreviewed local HEAD: {local_head}")
    remote_line = _git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
    remote_head = remote_line.split()[0] if remote_line else ""
    if remote_head != REVIEWED_REMOTE_HEAD:
        raise RuntimeError(
            f"Remote HEAD changed: {remote_head}; reviewed {REVIEWED_REMOTE_HEAD}"
        )
    staged = _git(root, "diff", "--cached", "--name-only")
    if staged:
        raise RuntimeError("Staged files require user review: " + staged)
    changed = tuple(filter(None, _git(root, "diff", "--name-only").splitlines()))
    permitted_local = ("phase165_r52_r9_shared_math.py",)
    if any(path not in permitted_local for path in changed):
        raise RuntimeError("Unreviewed tracked worktree changes: " + ", ".join(changed))
    if local_head == REVIEWED_REMOTE_HEAD and changed:
        raise RuntimeError("Unexpected tracked change on reviewed HEAD")
    if local_head == PREVIOUS_REMOTE_HEAD and changed != permitted_local:
        raise RuntimeError("Expected only the preserved R4-R8 11-line local change")
    for relative, blob in REVIEWED_BLOBS.items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"Missing reviewed file: {relative}")
        actual = _git(root, "hash-object", "--", relative)
        if actual != blob:
            raise RuntimeError(
                f"Reviewed worktree blob mismatch: {relative}: {actual} != {blob}"
            )
    return {
        "branch": branch,
        "local_head": local_head,
        "remote_head": remote_head,
        "reviewed_blobs": len(REVIEWED_BLOBS),
        "tracked_worktree_changes": list(changed),
        "source_guard": "PASS",
        "worktree_preserved": True,
    }


def _short(value: object) -> str | None:
    if value is None:
        return None
    result = repr(value)
    return result[:800]


def inspect_dimension(dimension: int) -> dict[str, Any]:
    """Classify obligations; structural matches are never classified as proof."""
    if type(dimension) is not int or dimension < 7:
        raise ValueError("dimension must be an integer >= 7")
    stem = dimension - 4
    goal = exact_prior_database_result(4, stem)
    first = exact_prior_database_result(3, stem)
    second = exact_prior_database_result(7, dimension - 7)
    first_step = (
        admitted_db_step(first, proof_target=goal)
        if first is not None and goal is not None else None
    )
    second_step = (
        admitted_db_step(second, proof_target=goal)
        if second is not None and goal is not None else None
    )
    proposed = (
        _map_components(first, second)
        if first is not None and second is not None else None
    )
    target = _group_components(goal) if goal is not None else None
    shape_match = (
        components_match_alias(proposed, target)
        if proposed is not None and target is not None else False
    )
    eligible_bounded = checked_inputs(goal) is not None if goal is not None else False
    blockers = []
    if goal is None:
        blockers.append("target_typed_database_goal_missing")
    if first_step is None:
        blockers.append("first_earlier_db_prior_not_admitted")
    if second_step is None:
        blockers.append("second_earlier_db_prior_not_admitted")
    if proposed is None:
        blockers.append("generator_image_shape_not_supported")
    elif not shape_match:
        blockers.append("source_image_and_target_presentation_do_not_match")
    if dimension == 7:
        blockers.append("existing_seven_step_root_must_be_preserved")
    elif not eligible_bounded:
        blockers.append("source_first_rule_currently_excludes_this_target")
    if dimension >= 11:
        blockers.append("source_first_screen_and_public_route_currently_exclude_this_target")
    if isinstance(goal, TodaPrimaryGroupZeroStatement):
        blockers.append("zero_goal_bypasses_shared_group_goal_public_route")
    if dimension >= 8:
        blockers.append("detailed_narrative_projector_is_pi7_4_only")
    return {
        "dimension": dimension,
        "n": 4,
        "k": stem,
        "target_type": type(goal).__name__ if goal is not None else None,
        "first_type": type(first).__name__ if first is not None else None,
        "second_type": type(second).__name__ if second is not None else None,
        "first_prior_admitted": first_step is not None,
        "second_prior_admitted": second_step is not None,
        "source_components": (
            [len(_group_components(first)), len(_group_components(second))]
            if first is not None and second is not None
            and _group_components(first) is not None
            and _group_components(second) is not None else None
        ),
        "target_components": len(target) if target is not None else None,
        "mapped_components": len(proposed) if proposed is not None else None,
        "generator_image_shape_matches": shape_match,
        "bounded_source_first_rule_accepts": eligible_bounded,
        "first_goal": _short(first),
        "second_goal": _short(second),
        "target_goal": _short(goal),
        "unresolved_implementation_conditions": blockers,
        "proof_certified_by_this_audit": False,
    }


def inspect_public(dimension: int) -> dict[str, Any]:
    """Optional live search only; preserve partial or failed statuses unchanged."""
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from web_group_proof import build_standard_web_group_proof_view
    result = search_group_from_registered_goal(n=4, k=dimension - 4)
    view = build_standard_web_group_proof_view(
        n=4, k=dimension - 4, max_depth=2, mode="narrative",
        citation_source="model",
    )
    return {
        "dimension": dimension,
        "search_status": result.status.value,
        "proven_steps": len(result.proven_steps),
        "open_goals": len(result.open_goals),
        "web_key": view.key,
        "web_complete": view.key == "generic-complete-proof" and not view.partial_result,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--include-public", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    before_status = _git(root, "status", "--porcelain", "--untracked-files=no")
    gate = preflight(root)
    print("PHASE173_R4_R9_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R9_REMOTE_HEAD=" + gate["remote_head"], flush=True)
    print("PHASE173_R4_R9_LOCAL_HEAD=" + gate["local_head"], flush=True)
    rows = tuple(inspect_dimension(i) for i in range(7, 13))
    for row in rows:
        print(
            "PHASE173_R4_R9_PI_" + str(row["dimension"]) + "_4"
            + " TARGET=" + str(row["target_type"])
            + " PRIOR1=" + str(row["first_prior_admitted"])
            + " PRIOR2=" + str(row["second_prior_admitted"])
            + " SHAPE=" + str(row["generator_image_shape_matches"])
            + " BOUNDED=" + str(row["bounded_source_first_rule_accepts"]),
            flush=True,
        )
    public = ()
    if args.include_public and not args.dry_run:
        public = tuple(inspect_public(i) for i in range(7, 13))
        for row in public:
            print("PHASE173_R4_R9_PUBLIC=" + json.dumps(row, ensure_ascii=False), flush=True)
    after_status = _git(root, "status", "--porcelain", "--untracked-files=no")
    if before_status != after_status:
        raise RuntimeError("Unexpected tracked worktree modification during audit")
    report = {
        "phase": "173 R4-R9 audit only",
        "read_only": True,
        "preflight": gate,
        "typed_frontier": rows,
        "public_checks": public,
        "interpretation": (
            "Compatibility of stored generator shapes does not constitute "
            "a proof of generator images or an independently verified literature theorem."
        ),
    }
    if args.dry_run:
        print("PHASE173_R4_R9_DRY_RUN=PASS", flush=True)
    else:
        output = Path(__file__).resolve().parent / "audit_result.json"
        output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("PHASE173_R4_R9_AUDIT_REPORT=" + str(output), flush=True)
        print("PHASE173_R4_R9_AUDIT_ONLY=PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
