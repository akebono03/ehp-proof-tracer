"""Compare R4-R8's genuine proof tree with canonical search and Web handoff.

This is NOT a public wiring implementation. In particular, it never inserts
an already completed ProofStep into search, does not construct a synthetic
COMPLETE PartialProofResult, and does not bypass the public trust boundary.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from proof import ProofRule, Relation, RelationType
from web_group_proof import build_standard_web_group_proof_view

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    """Restrict the audit to a small, read-only Git command allowlist."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in allowed:
        raise ValueError("only read-only Git commands are allowed")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def has_exact_root_route(options: tuple[object, ...], root: object) -> bool:
    """Distinguish the R4-R8 inference from unrelated legacy proposals."""
    return any(
        getattr(getattr(option, "rule", None), "name", None)
        == getattr(getattr(root, "inference_rule", None), "name", None)
        and getattr(option, "subgoals", None)
        == tuple(parent.conclusion for parent in root.premises)
        for option in options
    )


def public_completion_observed(
    status: ProofSearchStatus, result_conclusion: object,
    requested_goal: object, web_partial: bool | None,
) -> bool:
    """Report only genuine public search+Web completion, never R4-R8 replay alone."""
    return (
        status is ProofSearchStatus.COMPLETE
        and isinstance(requested_goal, Relation)
        and requested_goal.relation_type is RelationType.EQUALITY
        and result_conclusion == requested_goal
        and web_partial is False
    )


def inspect_public_path() -> dict:
    """Independently measure R4-R8, the common provider, search, and Web.

    A previously inferred local root is NOT offered to the canonical search
    as a completed result or a GIVEN. Only normal repository entry points are
    called, and all missing states remain observable in the report.
    """
    screened, requested_goal, citing = _screened_context()
    root, ancestors, root_report = build_cyclic_pi63_proof()
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != requested_goal
        or root_report["new_given_added"] != 0
        or not root_report["pi63_cyclic_group_proven"]
        or not ancestors
        or not all(step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
                   for step in ancestors)
    ):
        raise RuntimeError("R4-R8 must be a genuine inferred proof of the registered goal")

    common = shared_expansion_provider(screened, proof_target=requested_goal)
    options = common(requested_goal)
    if not isinstance(options, tuple):
        raise RuntimeError("common provider returned a non-tuple of proposals")
    route_found = has_exact_root_route(options, root)

    original_bridge = build_shared_typed_bridge()
    contexts: list[object] = []
    search = search_group_from_registered_goal(
        n=3, k=3,
        bridge=original_bridge,
        goal=requested_goal,
        context_sink=contexts.append,
    )
    if not isinstance(search.status, ProofSearchStatus):
        raise RuntimeError("canonical search produced an invalid status")
    search_complete = (
        search.status is ProofSearchStatus.COMPLETE
        and search.conclusion == requested_goal
        and not search.open_goals
    )
    if search.status is ProofSearchStatus.COMPLETE and not search_complete:
        raise RuntimeError("canonical completed result does not match registered pi_6^3")

    web_error = None
    web_partial = None
    web_lines = 0
    web_steps = 0
    try:
        view = build_standard_web_group_proof_view(
            n=3, k=3, mode="narrative", citation_source="model",
            goal=requested_goal,
        )
        web_partial = view.partial_result
        web_lines = len(view.rendered_lines)
        web_steps = len(view.steps)
    except Exception as error:
        web_error = type(error).__name__ + ": " + str(error)[:1200]

    web_complete = public_completion_observed(
        search.status, search.conclusion, requested_goal, web_partial,
    ) and web_error is None and web_steps > 0
    if web_partial is False and not search_complete and web_error is None:
        raise RuntimeError("public Web claimed completion while search was unfinished")

    return {
        "phase": "171-R2J-R4-R9-R1",
        "mode": "AUDIT_ONLY_PUBLIC_PATH",
        "requested_goal": repr(requested_goal),
        "citing_assertion_id": citing,
        "r8_inferred": True,
        "r8_inferences": root_report["inferences"],
        "r8_given_leaves": root_report["given_leaves"],
        "r8_new_given": 0,
        "public_root_expansion_count": len(options),
        "public_root_expansion_rule_names": [
            getattr(option.rule, "name", "<unnamed>") for option in options[:30]
        ],
        "exact_r8_root_expansion_connected": route_found,
        "search_status": search.status.value,
        "search_complete": search_complete,
        "search_observed_proven_steps": len(search.proven_steps),
        "search_open_goals": [repr(item)[:600] for item in search.open_goals[:15]],
        "search_diagnostics": list(search.diagnostics[:15]),
        "screened_context_observed": bool(contexts),
        "web_partial_result": web_partial,
        "web_rendered_lines": web_lines,
        "web_proof_steps": web_steps,
        "web_error": web_error,
        "public_web_complete_verified": web_complete,
        "production_modified": False,
        "existing_tests_modified": False,
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
        raise RuntimeError("R4-R9-R1 requires the develop branch")
    if not (ROOT / "phase171_r2j_r4_r8_cyclic_structure" / "audit.py").is_file():
        raise RuntimeError("the verified R4-R8 proof source is not present")
    print("PHASE171_R2J_R4_R9_R1_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R1_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R1_RESULT=PASS_DRY_RUN", flush=True)
        return
    result = inspect_public_path()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files changed during public-path audit")
    result.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R9_R1_R8_INFERRED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R1_ROOT_OPTIONS=" + str(result["public_root_expansion_count"]), flush=True)
    print("PHASE171_R2J_R4_R9_R1_R8_ROUTE_CONNECTED=" + str(result["exact_r8_root_expansion_connected"]), flush=True)
    print("PHASE171_R2J_R4_R9_R1_PUBLIC_SEARCH=" + result["search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R1_PUBLIC_WEB_COMPLETE=" + str(result["public_web_complete_verified"]), flush=True)
    if result["web_error"]:
        print("PHASE171_R2J_R4_R9_R1_WEB_ERROR=" + result["web_error"], flush=True)
    print("PHASE171_R2J_R4_R9_R1_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R1_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R1_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R1_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
