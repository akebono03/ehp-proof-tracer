"""Read-only audit of R11 equality-symmetry adoption in public proof search.

No proof step is installed, no GIVEN is created, and no repository source is
modified. The complete public search and the focused recursive searches are
independent invocations of the existing canonical searcher.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Callable

from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge,
    shared_expansion_provider,
)
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
from phase165_r57_r26_generic_search_connection import merge_backward_expansions
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase171_r2i_eta_hopf_bridge.audit import (
    _checked_chain,
    _screened_context,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (
    expand_reverse_cited_eta_hopf_equalities,
    reverse_equality,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
SOURCE = ROOT / "phase165_r52_r9_shared_math.py"
SOURCE_IN_GIT = "phase165_r52_r9_shared_math.py"
R11_BLOB_SHA = "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"


def git_read(*arguments: str) -> bytes:
    """Allow only source-inspection commands and current branch metadata."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
        ("show", f"HEAD:{SOURCE_IN_GIT}"),
    }
    if arguments not in allowed:
        raise ValueError("R12 audit permits read-only Git operations only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True, capture_output=True,
    ).stdout


def git_blob_sha(contents: bytes) -> str:
    """Return the canonical SHA-1 blob identifier for unmodified Git bytes."""
    header = f"blob {len(contents)}\0".encode("ascii")
    return hashlib.sha1(header + contents).hexdigest()


def normalized_source(contents: bytes) -> str:
    """Compare checked-out CRLF and Git LF without changing either file."""
    return contents.decode("utf-8-sig").replace("\r\n", "\n")


def preflight() -> dict:
    """Require reviewed committed R11 and a matching, unedited worktree."""
    branch = git_read("branch", "--show-current").decode().strip()
    head = git_read("rev-parse", "HEAD").decode().strip()
    head_blob = git_read("show", f"HEAD:{SOURCE_IN_GIT}")
    worktree_blob = SOURCE.read_bytes()
    if branch != "develop":
        raise RuntimeError("R12 requires the develop branch")
    actual_sha = git_blob_sha(head_blob)
    if actual_sha != R11_BLOB_SHA:
        raise RuntimeError(
            "R11 is not the committed reviewed baseline; first synchronize "
            "develop so HEAD contains the R11 provider hook. "
            f"actual blob={actual_sha}"
        )
    if normalized_source(worktree_blob) != normalized_source(head_blob):
        raise RuntimeError("tracked shared provider differs from committed HEAD")
    return {
        "branch": branch,
        "head": head,
        "shared_provider_blob": actual_sha,
        "tracked_status_before": git_read(
            "status", "--porcelain", "--untracked-files=no"
        ).decode("utf-8", errors="replace"),
    }


def route_profile(expansions: tuple[GoalExpansion, ...]) -> dict:
    """Describe proposals without treating a proposal as a proved ProofStep."""
    if not isinstance(expansions, tuple):
        raise TypeError("expansions must be a tuple")
    if any(not isinstance(item, GoalExpansion) for item in expansions):
        raise TypeError("each route must be GoalExpansion")
    names = tuple(str(getattr(item.rule, "name", "<unnamed>")) for item in expansions)
    return {
        "count": len(expansions),
        "rule_names": list(names[:30]),
        "symmetry_count": names.count("equality symmetry"),
        "proposals": [
            {
                "rule": str(getattr(item.rule, "name", "<unnamed>")),
                "subgoals": [repr(x)[:750] for x in item.subgoals],
            }
            for item in expansions[:20]
        ],
        "profile_truncated": len(expansions) > 20,
    }


def route_matches(
    expansions: tuple[GoalExpansion, ...],
    rule_name: str,
    subgoals: tuple[object, ...],
) -> int:
    """Count the exact R11 premise route through each inspected stage."""
    return sum(
        getattr(item.rule, "name", None) == rule_name
        and item.subgoals == subgoals
        for item in expansions
    )


class TracingProvider:
    """Log provider calls without changing their order or returned proposals."""

    def __init__(self, original: Callable[[object], tuple[GoalExpansion, ...]]):
        if not callable(original):
            raise TypeError("provider must be callable")
        self.original = original
        self.calls: list[dict] = []
        self.count = 0

    def __call__(self, goal: object) -> tuple[GoalExpansion, ...]:
        self.count += 1
        routes = self.original(goal)
        if len(self.calls) < 150:
            self.calls.append({
                "goal": repr(goal)[:950],
                "routes": route_profile(routes),
            })
        return routes


def focused_reconstruction(
    goal: object,
    screened: object,
    citing: str,
    provider: Callable[[object], tuple[GoalExpansion, ...]],
) -> dict:
    """Run canonical reconstruction on one goal with a progress observer."""
    traced = TracingProvider(provider)
    observations: list[dict] = []

    def observer(kind: str, target: object, step: object) -> None:
        if len(observations) < 250:
            observations.append({
                "event": kind,
                "goal": repr(target)[:950],
                "rule": getattr(getattr(step, "rule", None), "name", None),
            })

    try:
        result = reconstruct_registered_goal(
            goal,
            screened,
            citing,
            traced,
            lookup_mode="typed_reference_publication",
            progress_observer=observer,
            completed_internal_proofs=(),
        )
    except RegisteredGoalUnresolved as error:
        return {
            "status": "unresolved",
            "message": str(error),
            "provider_calls": traced.count,
            "calls": traced.calls,
            "observations": observations,
        }
    return {
        "status": "proved",
        "conclusion_matches": type(result.conclusion) is type(goal)
        and result.conclusion == goal,
        "root_rule": str(result.rule),
        "provider_calls": traced.count,
        "calls": traced.calls,
        "observations": observations,
    }


def inspect() -> dict:
    """Compare direct, merged, filtered, and actual public-search proposals."""
    original_bridge = build_shared_typed_bridge()
    screened_reference, target, citing = _screened_context()
    if not isinstance(citing, str) or not citing:
        raise RuntimeError("no resolved citation for pi_6^3")
    resolved_citing = resolve_specialized_goal_citing_id(original_bridge, target)
    if resolved_citing != citing:
        raise RuntimeError("the R2I and public citing goal IDs are different")
    public_contexts: list[object] = []
    public = search_group_from_registered_goal(
        n=3,
        k=3,
        bridge=original_bridge,
        goal=target,
        context_sink=public_contexts.append,
    )
    if len(public_contexts) > 1:
        raise RuntimeError("ambiguous root proof contexts captured")
    actual_context = public_contexts[0] if public_contexts else screened_reference
    context_captured = len(public_contexts) == 1
    chain, available = _checked_chain(actual_context, citing)
    forward_goal = chain.alpha_composition
    reverse_goal = reverse_equality(forward_goal)
    if reverse_goal is None:
        raise RuntimeError("first unresolved equality cannot be reversed")
    direct = expand_reverse_cited_eta_hopf_equalities(reverse_goal, available)
    merged = merge_backward_expansions(direct, ())
    gated = retain_ordered_root_expansions(target, reverse_goal, merged)
    provider = shared_expansion_provider(actual_context, proof_target=target)
    public_reverse_routes = provider(reverse_goal)
    public_forward_routes = provider(forward_goal)
    original_rule = "equality symmetry"
    obligations = (forward_goal,)
    counts = {
        "direct": route_matches(direct, original_rule, obligations),
        "deduplicated": route_matches(merged, original_rule, obligations),
        "root_gate": route_matches(gated, original_rule, obligations),
        "actual_public_provider": route_matches(
            public_reverse_routes, original_rule, obligations
        ),
    }
    forward = focused_reconstruction(forward_goal, actual_context, citing, provider)
    reverse = focused_reconstruction(reverse_goal, actual_context, citing, provider)
    first_open = public.open_goals[0] if public.open_goals else None
    observed_open_is_reverse = type(first_open) is type(reverse_goal) and first_open == reverse_goal
    if counts["direct"] == 0:
        classification = "R11_NOT_PROPOSED_FOR_PUBLIC_CONTEXT"
    elif counts["actual_public_provider"] == 0:
        classification = "R11_PROPOSAL_DROPPED_BEFORE_CANONICAL_SEARCH"
    elif forward["status"] == "unresolved":
        classification = "FORWARD_PREMISE_UNRESOLVED_IN_CANONICAL_SEARCH"
    elif reverse["status"] == "unresolved":
        classification = "REVERSE_UNRESOLVED_DESPITE_FORWARD_PROOF_CHECK_MATCH_OR_AMBIGUITY"
    elif public.status.value != "complete":
        classification = "FOCUSED_REVERSE_PROVED_BUT_ROOT_SEARCH_STILL_PARTIAL"
    else:
        classification = "PUBLIC_SEARCH_COMPLETE_NEEDS_TRUST_BOUNDARY_VERIFICATION"
    return {
        "phase": "171-R2J-R4-R9-R12",
        "mode": "AUDIT_ONLY",
        "target": repr(target),
        "context_captured_from_public_path": context_captured,
        "reference_source_count": len(screened_reference.proof_links),
        "public_source_count": len(actual_context.proof_links),
        "first_reported_open_is_reverse_goal": observed_open_is_reverse,
        "public_first_open": repr(first_open)[:1300],
        "public_status": public.status.value,
        "public_diagnostics": list(public.diagnostics[:12]),
        "public_proven_steps": len(public.proven_steps),
        "public_open_goal_count": len(public.open_goals),
        "forward_goal": repr(forward_goal),
        "reverse_goal": repr(reverse_goal),
        "r11_route_stage_counts": counts,
        "r11_direct": route_profile(direct),
        "r11_gate": route_profile(gated),
        "public_reverse": route_profile(public_reverse_routes),
        "public_forward": route_profile(public_forward_routes),
        "forward_search": forward,
        "reverse_search": reverse,
        "classification": classification,
        "new_given_added": 0,
        "completed_proof_replay": False,
        "existing_source_modified": False,
        "full_pytest": False,
        "public_web_verified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    meta = preflight()
    print("PHASE171_R12_BRANCH=" + meta["branch"], flush=True)
    print("PHASE171_R12_HEAD=" + meta["head"], flush=True)
    print("PHASE171_R12_REVIEWED_R11_BLOB=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R12_RESULT=PASS_DRY_RUN", flush=True)
        return
    result = inspect()
    after = git_read("status", "--porcelain", "--untracked-files=no").decode(
        "utf-8", errors="replace"
    )
    if meta["tracked_status_before"] != after:
        raise RuntimeError("tracked status changed during the read-only audit")
    result.update({
        "git_head": meta["head"],
        "shared_provider_blob": meta["shared_provider_blob"],
        "tracked_status_unchanged": True,
    })
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PHASE171_R12_PUBLIC_SEARCH=" + result["public_status"], flush=True)
    print("PHASE171_R12_FIRST_OPEN_IS_REVERSE=" + str(
        result["first_reported_open_is_reverse_goal"]
    ), flush=True)
    print("PHASE171_R12_ROUTE_COUNTS=" + json.dumps(
        result["r11_route_stage_counts"], ensure_ascii=False
    ), flush=True)
    print("PHASE171_R12_FORWARD=" + result["forward_search"]["status"], flush=True)
    print("PHASE171_R12_REVERSE=" + result["reverse_search"]["status"], flush=True)
    print("PHASE171_R12_CLASSIFICATION=" + result["classification"], flush=True)
    print("PHASE171_R12_NEW_GIVEN=0", flush=True)
    print("PHASE171_R12_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R12_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R12_REPORT=" + str(destination), flush=True)
    print("PHASE171_R12_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
