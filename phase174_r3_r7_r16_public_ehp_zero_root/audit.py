"""Phase 174 R3-R7-R16: source-guarded public EHP zero-root integration.

The root becomes an unproved backward candidate with four independent goals.
Neither an isolated proposal nor a displayed open goal is a certified proof.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from phase174_r3_r7_r16_public_ehp_zero_root.patch import (
    BASE_BLOB, TARGET, blob_sha, normalize_and_style, transform_source,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R16"
PRE_R15_HEAD = "380a5b17414075e7ec5ebbb17c310e8dad49fa60"
REVIEWED_HEAD = "e7bcd34a526b3f885a8e3be81c4aac362d8834c7"
R15_PREFIX = "phase174_r3_r7_r15_chain_frontier_audit/"
PINS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py": "54ae4d4430c99895e0687ea8c56fd711284465f1",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase174_r3_r7_r15_chain_frontier_audit/audit.py": "64256bb7b3fda9dc2ad12f78e2bef92df01ce27d",
    "phase174_r3_r7_r14_public_annihilator_connection/tests/test_public.py": "a5a798b5c7b7ae148c45db5ffc3be86654fdf69b",
}


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
    ).stdout


def matches_blob(source: bytes, expected: str) -> bool:
    if len(expected) != 40 or any(ch not in "0123456789abcdef" for ch in expected):
        return False
    try:
        normalized, _ = normalize_and_style(source)
    except (RuntimeError, UnicodeError):
        return False
    text_bytes = normalized.encode("utf-8")
    return any(blob_sha(x) == expected for x in (
        source, text_bytes, text_bytes.replace(b"\n", b"\r\n"),
    ))


def validate_lineage(local: str, remote: str, paths: tuple[str, ...],
                     modified: tuple[str, ...], patched: bool) -> str:
    if remote != REVIEWED_HEAD or local not in (PRE_R15_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Unreviewed GitHub/local develop HEAD; refuse modification")
    if not paths or any(not p.startswith(R15_PREFIX) for p in paths):
        raise RuntimeError("R15 merge changed paths outside the audited package")
    expected = (TARGET.as_posix(),) if patched else ()
    if modified != expected:
        raise RuntimeError("Unexpected tracked changes: " + str(modified))
    return "R15_MERGED_CLEAN" if local == REVIEWED_HEAD else "R15_MERGED_REMOTE_LOCAL_R14"


def verify_git_and_sources(*, patched: bool, root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R16 immediately below the repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Expected develop branch")
    remote = git("ls-remote", "origin", "refs/heads/develop", root=root).split()[0]
    local = git("rev-parse", "HEAD", root=root)
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged changes require separate review")
    changed = tuple(git("diff", "--name-only", root=root).splitlines())
    git_bytes("merge-base", "--is-ancestor", PRE_R15_HEAD, REVIEWED_HEAD, root=root)
    commits = git("rev-list", "--reverse", PRE_R15_HEAD + ".." + REVIEWED_HEAD, root=root).splitlines()
    if len(commits) != 1:
        raise RuntimeError("Expected exactly one reviewed R15 merge-lineage commit")
    paths = tuple(git("diff", "--name-only", PRE_R15_HEAD, REVIEWED_HEAD, root=root).splitlines())
    lineage = validate_lineage(local, remote, paths, changed, patched)
    for path, sha in PINS.items():
        file = root / path
        if not file.is_file() or not matches_blob(file.read_bytes(), sha):
            raise RuntimeError("R16 source guard mismatch: " + path)
    head_source = git_bytes("show", "HEAD:" + TARGET.as_posix(), root=root)
    if not matches_blob(head_source, BASE_BLOB):
        raise RuntimeError("R14 shared-math base SHA not pinned")
    original, _ = normalize_and_style(head_source)
    live = (root / TARGET).read_bytes()
    checked, _ = normalize_and_style(live)
    expected = transform_source(original) if patched else original
    if checked != expected:
        raise RuntimeError("Working tree is not the exact R16 patch state")
    return {
        "branch": "develop", "local_head": local, "remote_head": remote,
        "head_lineage": lineage, "source_guard": "PASS",
        "pinned_source_files": len(PINS) + 1,
        "tracked_changed": list(changed),
        "patched": patched,
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r15" / "chain_frontier_audit.json"


def validate_r15_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R15"
            or report.get("gate") != "PASS_READ_ONLY_CHAIN_FRONTIER_NO_ROOT_CLAIM"
            or report.get("full_pytest_run") is not False
            or report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R15 handoff evidence mismatch")
    live = report.get("live") or {}
    frontier = (live.get("public_goal_frontiers") or {}).get("final_pi12_7_zero") or {}
    if (frontier.get("count") != 0
            or live.get("new_verified_proof_steps") != 0
            or live.get("public_provider_changed") is not False):
        raise RuntimeError("R15 actual root proposal baseline changed")
    return {"prior_gate": report["gate"], "root_candidates_before": 0,
            "new_verifications_before": 0}


def inspect_public_root() -> dict[str, Any]:
    """Check actual public provider after patch; do not forge proof premises."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        RULE_NAME, ehp_zero_inputs, expand_ehp_zero_from_delta_surjectivity,
    )
    from proof import ProofRule, ProofStep
    from unified_statement_registry import AssertionOrigin

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    exact_given = tuple(
        link.step for link in screened.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == root
    )
    if exact_given:
        raise RuntimeError("Target zero group must not be a direct GIVEN")
    provider = shared_expansion_provider(screened, proof_target=root)
    options = tuple(provider(root))
    named = tuple(x for x in options if x.rule.name == RULE_NAME)
    isolated = expand_ehp_zero_from_delta_surjectivity(root)
    children = ehp_zero_inputs(root)
    if (len(named) != 1 or len(options) != 1 or len(isolated) != 1
            or children is None or len(children) != 4
            or named[0].subgoals != isolated[0].subgoals
            or named[0].subgoals != children
            or root in children
            or any(isinstance(c, ProofStep) for c in children)):
        raise RuntimeError("Public EHP root did not preserve the isolated 4-goal contract")
    frontiers = [tuple(provider(child)) for child in children]
    return {
        "public_root_proposal_count": len(options),
        "public_rule_name": RULE_NAME,
        "unproved_root_child_count": len(children),
        "child_types": [type(x).__name__ for x in children],
        "child_proposal_counts": [len(x) for x in frontiers],
        "child_goals": [repr(x)[:800] for x in children],
        "root_direct_given": False,
        "new_group_given": 0,
        "new_math_rule": 0,
        "proof_completed_claimed": False,
        "verified_proof_step_from_candidate": False,
    }


def inspect_standard_search() -> dict[str, Any]:
    """Check the real standard path; unresolved goals remain unresolved."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    result = search_group_from_registered_goal(
        n=7, k=5, bridge=build_shared_typed_bridge(), goal=goal,
    )
    if (result.status is ProofSearchStatus.COMPLETE or result.conclusion is not None
            or not any(item == goal for item in result.open_goals)):
        raise RuntimeError("R16 cannot claim or silently discard unresolved zero root")
    return {
        "status": result.status.value,
        "open_goal_count": len(result.open_goals),
        "open_goal_types": [type(x).__name__ for x in result.open_goals],
        "open_goals": [repr(x)[:800] for x in result.open_goals],
        "verified_steps_from_search": len(result.proven_steps),
        "conclusion": None,
    }


def output_path(dry_run: bool) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r16" / (
        "public_ehp_root_preflight.json" if dry_run else "public_ehp_root_audit.json"
    )


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(patched=not dry_run, root=root)
    previous = previous_report_path()
    if not previous.is_file():
        raise RuntimeError("R15 completed evidence missing: " + str(previous))
    handoff = validate_r15_report(json.loads(previous.read_text(encoding="utf-8-sig")))
    public = None if dry_run else inspect_public_root()
    search = None if dry_run else inspect_standard_search()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "PUBLIC_EHP_ZERO_ROOT",
        "git_state": state,
        "previous_report": handoff,
        "public": public,
        "search": search,
        "modified_production_functions": [] if dry_run else ["shared_expansion_provider"],
        "new_group_given": 0,
        "new_mathematical_inference_rules": 0,
        "full_pytest_run": False,
        "root_proof_completed_claimed": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_PUBLIC_GENERIC_EHP_ROOT_PREMISES_OPEN",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = output_path(args.dry_run)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R16_"
    state = report["git_state"]
    for key in ("local_head", "remote_head", "head_lineage", "source_guard"):
        print(prefix + key.upper() + "=" + str(state[key]))
    if report["public"] is not None:
        live = report["public"]
        print(prefix + "PUBLIC_ROOT_PROPOSALS=" + str(live["public_root_proposal_count"]))
        print(prefix + "UNPROVED_CHILD_GOALS=" + str(live["unproved_root_child_count"]))
        for index, (name, count) in enumerate(zip(live["child_types"], live["child_proposal_counts"]), 1):
            print(prefix + "CHILD_" + str(index) + "=" + name + ":" + str(count))
        search = report["search"]
        print(prefix + "SEARCH_STATUS=" + search["status"])
        print(prefix + "SEARCH_OPEN_GOALS=" + str(search["open_goal_count"]))
        print(prefix + "SEARCH_PROVEN_STEPS=" + str(search["verified_steps_from_search"]))
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_MATH_RULES=0")
    print(prefix + "ROOT_COMPLETE=False")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
