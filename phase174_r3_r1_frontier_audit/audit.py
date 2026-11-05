"""Inspect the first two search layers for pi_8^5 without granting proofs.

All proposals are search obligations, not verified ProofSteps. Citation-screened
GIVENs are counted for diagnostics only. No mathematics is inferred here.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Callable

R2_REPORT_HEAD = "3558d713fd7939ded656f2458aacc62d71c7e0b3"
REVIEWED_BASE = "3558d713fd7939ded656f2458aacc62d71c7e0b3"
REVIEWED_TIP = "1c6e6e594042f498e3cb4977ef9c72ce3d1da9f9"
ALLOWED_HEADS = (REVIEWED_BASE, REVIEWED_TIP)


def git(*arguments: str) -> str:
    completed = subprocess.run(
        ("git",) + arguments,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout.strip()


def r2_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r2" / "audit.json"


def validate_r2_record(data: object) -> dict[str, object]:
    """Validate the R2 evidence; never treat a proposal as proof."""
    if not isinstance(data, dict):
        raise ValueError("R2 report is not an object")
    if data.get("head") != R2_REPORT_HEAD or data.get("phase") != "174-R2":
        raise ValueError("R2 source report has an unreviewed HEAD or phase")
    if data.get("mode") != "READ_ONLY_SOURCE_FIRST":
        raise ValueError("R2 was not read-only")
    if any(data.get(key) != 0 for key in (
        "new_given", "new_inference_rules", "new_proof_steps", "new_completed_named_proofs",
    )):
        raise ValueError("R2 report unexpectedly claimed new proof evidence")
    if data.get("full_pytest_performed") is not False:
        raise ValueError("R2 report wrongly claims a whole-suite run")
    root = data.get("pi85_root_frontier")
    if not isinstance(root, dict):
        raise ValueError("R2 root frontier is missing")
    proposals = root.get("proposals")
    if root.get("proposal_count") != 3 or not isinstance(proposals, list) or len(proposals) != 3:
        raise ValueError("R2 root frontier must have three observed candidates")
    if root.get("screened_given_count") != 27 or root.get("target_direct_given_count") != 0:
        raise ValueError("R2 given source count or target exclusion changed")
    for proposal in proposals:
        if not isinstance(proposal, dict) or not isinstance(proposal.get("subgoals"), list):
            raise ValueError("R2 proposal record is malformed")
        if proposal.get("subgoal_count") != len(proposal["subgoals"]):
            raise ValueError("R2 proposal child count changed")
    return root


def signature(value: object) -> dict[str, str]:
    return {"type": type(value).__name__, "repr": repr(value)}


def same_statement(left: object, right: object) -> bool:
    return type(left) is type(right) and left == right


def is_screened_given(statement: object, admitted: tuple[object, ...]) -> bool:
    return any(same_statement(statement, source) for source in admitted)


def describe_first_two_hops(
    goal: object,
    expand: Callable[[object], tuple],
    admitted: tuple[object, ...],
    *,
    unwrap: Callable[[object], object] | None = None,
    branch_display_limit: int = 24,
) -> dict[str, object]:
    """Describe every immediate frontier; never execute inference match guards.

    SourceBoundGoal wrappers are unwrapped only for *diagnostic* expansion.
    Such a wrapper still requires scoped evidence during the real proof search.
    """
    if unwrap is None:
        unwrap = lambda value: value
    if branch_display_limit < 1:
        raise ValueError("branch_display_limit must be positive")
    root_proposals = expand(goal)
    if not isinstance(root_proposals, tuple):
        raise TypeError("root expansion provider did not return a tuple")
    root: list[dict[str, object]] = []
    for index, proposal in enumerate(root_proposals, start=1):
        children = getattr(proposal, "subgoals", None)
        if not isinstance(children, tuple):
            raise TypeError("invalid root expansion children")
        child_rows: list[dict[str, object]] = []
        for child in children:
            actual = unwrap(child)
            nested = expand(actual)
            if not isinstance(nested, tuple):
                raise TypeError("nested expansion provider did not return a tuple")
            options = []
            for candidate in nested[:branch_display_limit]:
                subtasks = getattr(candidate, "subgoals", None)
                if not isinstance(subtasks, tuple):
                    raise TypeError("invalid second-hop expansion children")
                options.append({
                    "rule": getattr(getattr(candidate, "rule", None), "name", None),
                    "subgoals": [
                        {
                            **signature(step),
                            "exact_screened_given": is_screened_given(unwrap(step), admitted),
                            "returns_to_root": same_statement(unwrap(step), goal),
                            "returns_to_parent": same_statement(unwrap(step), actual),
                        }
                        for step in subtasks
                    ],
                })
            child_rows.append({
                "goal": signature(child),
                "unwrapped_goal": signature(actual),
                "is_source_bound_wrapper": not same_statement(actual, child),
                "exact_screened_given": is_screened_given(actual, admitted),
                "returns_to_root": same_statement(actual, goal),
                "second_hop_proposal_count": len(nested),
                "second_hop_proposals_shown": len(options),
                "second_hop_proposals": options,
            })
        root.append({
            "ordinal": index,
            "rule": getattr(getattr(proposal, "rule", None), "name", None),
            "child_count": len(children),
            "children": child_rows,
        })
    return {
        "goal": signature(goal),
        "screened_given_count": len(admitted),
        "root_proposal_count": len(root_proposals),
        "root_proposals": root,
        "proofs_verified_by_this_audit": 0,
        "new_given": 0,
    }


def inspect_live_frontier() -> dict[str, object]:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase165_r3_recursive_search import SourceBoundGoal
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(candidates) != 1:
        raise ValueError("Expected exactly one pi_8^5 goal")
    goal = candidates[0]
    citation = resolve_specialized_goal_citing_id(bridge, goal)
    if citation is None:
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
        mode = "source_first"
    else:
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citation,
            explicit_publication_target=True,
        )
        mode = "publication_screened"
    screened = prefer_universal_prop42_derivation(screened)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if is_screened_given(goal, admitted):
        raise ValueError("Target goal is an invalid direct GIVEN")
    provider = shared_expansion_provider(screened, proof_target=goal)
    result = describe_first_two_hops(
        goal, provider, admitted,
        unwrap=lambda obj: obj.conclusion if isinstance(obj, SourceBoundGoal) else obj,
    )
    result["screening_mode"] = mode
    result["citing_assertion_id"] = citation
    return result


def verify_against_r2(live: dict[str, object], previous: dict[str, object]) -> None:
    if live["goal"] != previous["typed_goal"]:
        raise ValueError("Typed root goal does not match R2")
    if live["root_proposal_count"] != previous["proposal_count"]:
        raise ValueError("Root proposal count does not match R2")
    if live["screened_given_count"] != previous["screened_given_count"]:
        raise ValueError("Screened citation count does not match R2")
    if live["screening_mode"] != previous["source_screening"]:
        raise ValueError("Citation screening mode does not match R2")
    if live["citing_assertion_id"] != previous["citing_assertion_id"]:
        raise ValueError("Citing assertion does not match R2")
    for current, recorded in zip(live["root_proposals"], previous["proposals"]):
        if current["rule"] != recorded["rule_name"]:
            raise ValueError("Root expansion rule differs from R2")
        if current["child_count"] != recorded["subgoal_count"]:
            raise ValueError("Root expansion child count differs from R2")
        for child, originally in zip(current["children"], recorded["subgoals"]):
            if child["goal"] != {"type": originally["type"], "repr": originally["repr"]}:
                raise ValueError("Root expansion child differs from R2")
            if child["exact_screened_given"] != originally["exact_screened_given"]:
                raise ValueError("Root child admission differs from R2")


def main() -> int:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    if branch != "develop" or head not in ALLOWED_HEADS:
        raise RuntimeError("R3-R1 local HEAD is not reviewed")
    report_file = r2_report_path()
    if not report_file.is_file():
        raise FileNotFoundError("R2 audit JSON is missing: " + str(report_file))
    previous = validate_r2_record(json.loads(report_file.read_text(encoding="utf-8-sig")))
    live = inspect_live_frontier()
    verify_against_r2(live, previous)
    output = {
        "phase": "174-R3-R1",
        "mode": "READ_ONLY_TWO_HOP_FRONTIER",
        "local_head": head,
        "r2_original_head": R2_REPORT_HEAD,
        "r2_report_path": str(report_file),
        "pi85_frontier": live,
        "production_files_modified": False,
        "new_proof_steps": 0,
        "full_pytest_performed": False,
    }
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    directory = directory / "EHPProofTracerAudit" / "phase174_r3_r1"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "audit.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R3R1_BRANCH=" + branch)
    print("PHASE174_R3R1_LOCAL_HEAD=" + head)
    print("PHASE174_R3R1_R2_PROVENANCE=PASS")
    print("PHASE174_R3R1_ROOT_MATCH=PASS")
    print("PHASE174_R3R1_ROOT_COUNT=" + str(live["root_proposal_count"]))
    for row in live["root_proposals"]:
        print("PHASE174_R3R1_ROOT_{0}={1} CHILDREN={2}".format(
            row["ordinal"], row["rule"], row["child_count"],
        ))
        for item in row["children"]:
            print("PHASE174_R3R1_CHILD={0} GIVEN={1} SECOND_HOP={2} CYCLE={3}".format(
                item["unwrapped_goal"]["type"],
                item["exact_screened_given"],
                item["second_hop_proposal_count"],
                item["returns_to_root"],
            ))
    print("PHASE174_R3R1_NEW_PROOFS=0")
    print("PHASE174_R3R1_REPORT=" + str(path))
    print("PHASE174_R3R1_AUDIT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
