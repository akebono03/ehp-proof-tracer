"""Read-only audit of the Phase 168 one-stem freeze against Phase 169 search.

The historical Phase 168 counts are reference observations, not axioms or a
reason to change a live ProofSearchStatus. No proof inference is performed here.
"""
from __future__ import annotations

import json
from pathlib import Path

CASES = ((2, 1), (3, 1), (4, 1), (5, 1), (8, 2))
FROZEN_PHASE168 = {(2, 1): 18, (3, 1): 25, (4, 1): 10}
OUTPUT = Path(__file__).resolve().parent / "output"


def status_assessment(cases: list[dict]) -> str:
    """Flag a regression without promoting partial or failed results to proofs."""
    by_case = {(item["n"], item["k"]): item for item in cases}
    for coords in FROZEN_PHASE168:
        item = by_case.get(coords)
        if (item is None or item["status"] != "complete"
                or item["trust"] != "PASS"
                or item.get("phase168_step_count_equal") is not True):
            return "BLOCKED_ONE_STEM_REGRESSION"
    return "ONE_STEM_STATUS_STEP_COUNTS_AND_TRUST_MATCH"


def _text(value: object, limit: int = 1600) -> str:
    rendered = repr(value)
    return rendered[:limit] + (" [truncated]" if len(rendered) > limit else "")


def inspect_case(n: int, k: int, bridge: object) -> dict:
    """Re-run exactly one registered Goal with the existing screened context."""
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates,
        search_group_from_registered_goal,
    )
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase166_r3af_goal_adapter import database_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from proof import ProofRule

    registered = registered_group_goal_candidates(bridge, n=n, k=k)
    database = database_group_goal_candidates(n=n, k=k)
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    citing_target = (
        result.conclusion if result.conclusion is not None
        else registered[0] if len(registered) == 1 else None
    )
    citing_id = (
        resolve_specialized_goal_citing_id(bridge, citing_target)
        if citing_target is not None else None
    )
    trust = "NOT_APPLICABLE_INCOMPLETE"
    trust_counts = None
    if result.status is ProofSearchStatus.COMPLETE:
        if len(contexts) != 1:
            trust = "FAIL_NO_SINGLE_SCREENED_CONTEXT"
        else:
            from phase168_r3_41p13_trust_boundary import (
                UnverifiedProofTree,
                verify_proof_tree_for_narrative,
            )
            try:
                if citing_id is None:
                    trust_counts = verify_proof_tree_for_narrative(
                        result, contexts[0], citing_assertion_id=None,
                        derived_target_without_citing_id=True,
                    )
                else:
                    trust_counts = verify_proof_tree_for_narrative(
                        result, contexts[0], citing_assertion_id=citing_id,
                    )
                trust = "PASS"
            except (UnverifiedProofTree, ValueError, TypeError) as exc:
                trust = "FAIL_" + type(exc).__name__ + ": " + str(exc)
    key = (n, k)
    expected_steps = FROZEN_PHASE168.get(key)
    return {
        "group": f"pi_{n+k}^{n}",
        "n": n,
        "k": k,
        "registered_goal_candidate_count": len(registered),
        "registered_goal_candidates": [_text(item) for item in registered],
        "database_goal_candidate_count": len(database),
        "database_goal_candidates": [_text(item) for item in database],
        "status": result.status.value,
        "structure_status": result.structure_status.value,
        "open_goal_types": [type(goal).__name__ for goal in result.open_goals],
        "open_goal_details": [_text(goal) for goal in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "proof_steps": len(result.proven_steps),
        "inference_steps": sum(step.rule is ProofRule.INFERENCE for step in result.proven_steps),
        "given_steps": sum(step.rule is ProofRule.GIVEN for step in result.proven_steps),
        "root_conclusion": _text(result.conclusion),
        "screened_context_count": len(contexts),
        "citing_assertion_id": citing_id,
        "screened_proof_links": len(contexts[0].proof_links) if contexts else None,
        "trust": trust,
        "trust_replay_counts": list(trust_counts) if trust_counts is not None else None,
        "phase168_frozen_step_count": expected_steps,
        "phase168_step_count_equal": (
            len(result.proven_steps) == expected_steps
            if expected_steps is not None and result.status is ProofSearchStatus.COMPLETE
            else None
        ),
        "source_of_frozen_count": "Phase 168 documentation, 2026-10-25",
    }


def make_report() -> dict:
    """Gather observations; a status mismatch remains a reported blocker."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge

    bridge = build_shared_typed_bridge()
    cases = [inspect_case(n, k, bridge) for n, k in CASES]
    return {
        "phase": "169 R10EE",
        "mode": "AUDIT_ONLY",
        "purpose": "Phase168 one-stem baseline regression diagnosis",
        "cases": cases,
        "phase169_closeout": status_assessment(cases),
        "production_files_changed": [],
        "proof_inference_rules_changed": False,
        "full_pytest_run": False,
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = make_report()
    json_path = OUTPUT / "audit.json"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    rows = [
        "# Phase 169 R10EE — 1-stem 回帰監査", "",
        "現行の探索結果を Phase 168 の固定基準と比較する読み取り専用監査。",
        "", "| 群 | 現行状態 | ProofStep | Phase168 | Trust | 診断 |",
        "|---|---|---:|---:|---|---|",
    ]
    for case in report["cases"]:
        key = "R10EE_" + case["group"]
        print(key + "_STATUS=" + case["status"], flush=True)
        print(key + "_TRUST=" + case["trust"], flush=True)
        print(key + "_GOAL_CANDIDATES=" + str(case["registered_goal_candidate_count"]), flush=True)
        print(key + "_PROOF_STEPS=" + str(case["proof_steps"]), flush=True)
        for diagnostic in case["diagnostics"]:
            print(key + "_DIAGNOSTIC=" + diagnostic, flush=True)
        expected = case["phase168_frozen_step_count"]
        diagnostic = "; ".join(case["diagnostics"]).replace("|", r"\|")
        rows.append(
            "| " + case["group"] + " | " + case["status"] + " | "
            + str(case["proof_steps"]) + " | "
            + (str(expected) if expected is not None else "—") + " | "
            + case["trust"] + " | " + diagnostic + " |"
        )
    rows += [
        "", "## 判定", "",
        "**" + report["phase169_closeout"] + "**", "",
        "`partial` を `complete` に読み替えない。候補数と診断から原因を特定するまで、",
        "Phase 169 全体の終了を認定しない。", "",
        "Proof Tree や引用命題の真偽をこの監査で新規証明しない。", "",
        "全体 pytest は実施していない。", "",
    ]
    md_path = OUTPUT / "audit.md"
    md_path.write_text("\n".join(rows), encoding="utf-8")
    print("R10EE_PHASE169_CLOSEOUT=" + report["phase169_closeout"])
    print("R10EE_AUDIT_JSON=" + str(json_path))
    print("R10EE_AUDIT_MD=" + str(md_path))
    print("R10EE_PRODUCTION_FILES_CHANGED=none")
    print("R10EE_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
