"""Opt-in, read-only check of a source-bound Toda (5.6) root provider."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
from typing import Any

REVIEWED_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_04_2.tex": "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r57_r11_proof_order_gate.py": "1ad9dfe8bb3da061cbee0dbd7a11c196f3f50604",
}


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, text=True, encoding="utf-8",
        capture_output=True, check=True,
    )
    return result.stdout.strip()


def preflight(root: Path) -> dict[str, Any]:
    """Allow audit-only HEAD advances, never production source drift."""
    if _git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only reviewed develop is supported")
    head = _git(root, "rev-parse", "HEAD")
    checked = []
    for path, expected in REVIEWED_BLOBS.items():
        actual = _git(root, "rev-parse", "HEAD:" + path)
        if actual != expected:
            raise RuntimeError("Reviewed production blob changed: " + path)
        diff = subprocess.run(
            ("git", "diff", "--quiet", "HEAD", "--", path),
            cwd=root, capture_output=True, check=False,
        )
        if diff.returncode != 0:
            raise RuntimeError("Reviewed production working file changed: " + path)
        checked.append(path)
    return {"head": head, "verified_files": checked, "tracked_file_changes": []}


def inspect_runtime() -> dict[str, Any]:
    """Use the existing source-screening and first-success search with one extra provider."""
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=3)
    if len(goals) != 1:
        raise RuntimeError("Expected one independently registered pi_7^4 goal")
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        raise RuntimeError("Pi_7^4 has no uniquely positioned citing assertion")
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )

    def local_provider(statement: object):
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    proposed = local_provider(goal)
    if len(proposed) > 1:
        raise RuntimeError("Ambiguous Toda (5.6) root proposals")
    combined = shared_expansion_provider(
        screened, extra_providers=(local_provider,), proof_target=goal,
    )
    root_rules = [option.rule.name for option in combined(goal)]
    result = search_shared_group_goal(
        n=4, k=3, group_structure=goal.rhs,
        bridge=bridge, citing_assertion_id=citing_id,
        expansion_provider=combined,
    )
    status = getattr(result.status, "value", str(result.status))
    complete = status == "complete"
    if complete and result.conclusion != goal:
        raise RuntimeError("A completed proof has an unexpected conclusion")
    return {
        "goal": repr(goal), "citing_assertion_id": citing_id,
        "source_bound_root_count": len(proposed),
        "source_bound_subgoals": [
            {"type": type(p).__name__, "statement": repr(p)}
            for option in proposed for p in option.subgoals
        ],
        "combined_root_rule_names": root_rules,
        "proof_search_status": status,
        "complete": complete,
        "open_goals": [repr(item) for item in getattr(result, "open_goals", ())],
        "diagnostics": [str(item) for item in getattr(result, "diagnostics", ())],
        "production_provider_changed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    pre = preflight(root)
    print("PHASE173_R4_R1_SOURCE_BOUND_SOURCE_GUARD=PASS")
    if args.dry_run:
        print("PHASE173_R4_R1_SOURCE_BOUND_DRY_RUN=PASS")
        return 0
    runtime = inspect_runtime()
    report = {
        "phase": "173-R4-R1", "scope": "ISOLATED_PROOF_PROPOSAL",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": pre,
        "runtime": runtime,
        "production_changes": [],
    }
    path = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_source_bound_56/audit.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PHASE173_R4_R1_SOURCE_BOUND_ROOTS=" + str(runtime["source_bound_root_count"]))
    for index, subgoal in enumerate(runtime["source_bound_subgoals"], 1):
        print("PHASE173_R4_R1_SUBGOAL_" + str(index) + "=" + subgoal["type"] + " " + subgoal["statement"])
    print("PHASE173_R4_R1_SEARCH_STATUS=" + str(runtime["proof_search_status"]))
    print("PHASE173_R4_R1_COMPLETE=" + str(runtime["complete"]))
    print("PHASE173_R4_R1_REPORT=" + str(path))
    print("PHASE173_R4_R1_NO_PRODUCTION_CHANGES=True")
    print("PHASE173_R4_R1_SOURCE_BOUND_AUDIT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
