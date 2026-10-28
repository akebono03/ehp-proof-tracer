"""Phase 170 R3-R2: read-only root expansion audit for five unfinished groups.

Read the certified R1/R2/R3 observations, then evaluate only the current
backward-expansion provider for each root typed goal. This is NOT a proof
search, an assertion of a missing theorem, or a Trust Boundary certificate.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

REVIEWED_R3_SHA256 = "514c74c560009a58c5301e3a86d35d4d1659ef30ca69f5225e9673c120575db7"
REVIEWED_HEAD = "f9e9a9d59970943d967e2cbcb0a98f13b2471407"
TARGETS = ((3, 3), (4, 3), (5, 3), (4, 4), (5, 4))
MAX_RECORDED_EXPANSIONS = 40


def clipped(value: object, limit: int = 1400) -> str:
    result = repr(value)
    return result if len(result) <= limit else result[:limit] + " [TRUNCATED]"


def load_reviewed_r3_code(root: Path):
    """Re-use, but do not silently alter, R3-R1's reviewed input guards."""
    source = root / "phase170_r3_r1_failure_frontier_audit" / "audit.py"
    if not source.is_file():
        raise RuntimeError("reviewed R3-R1 audit.py is missing")
    observed = hashlib.sha256(source.read_bytes()).hexdigest()
    if observed != REVIEWED_R3_SHA256:
        raise RuntimeError("R3-R1 audit source differs from reviewed package")
    spec = importlib.util.spec_from_file_location("phase170_r3_r1_reviewed", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the reviewed R3-R1 audit module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_reports(r3_module: Any, root: Path, r3_path: Path) -> tuple[dict, dict, dict, dict]:
    """Reject stale, partial or cross-HEAD observations before querying rules."""
    if r3_path.name != "audit.json" or not r3_path.is_file():
        raise RuntimeError("R3 report must be an existing audit.json")
    r3 = json.loads(r3_path.read_text(encoding="utf-8"))
    if (r3.get("phase") != "170 R3-R1" or r3.get("mode") != "AUDIT_ONLY"
            or r3.get("tracked_unchanged") is not True
            or r3.get("full_pytest_run") is not False
            or r3.get("review_required") is not False
            or r3.get("git", {}).get("head") != REVIEWED_HEAD):
        raise RuntimeError("R3 report is not a reviewed, successful read-only result")
    rows = r3.get("cases")
    expected = {f"pi_{n+k}^{n}" for n, k in TARGETS}
    if not isinstance(rows, list) or len(rows) != 5 or {x.get("group") for x in rows} != expected:
        raise RuntimeError("R3 cases are missing, duplicated or unexpected")
    if any("error" in row for row in rows):
        raise RuntimeError("R3 has case errors")
    r2_path = Path(r3.get("r2_report", "")).resolve()
    r1, r2, r1_map, r2_map, r1_path = r3_module.load_reports(root, r2_path)
    if Path(r3.get("r1_report", "")).resolve() != r1_path.resolve():
        raise RuntimeError("R3 and R2 disagree about the R1 record")
    for row in rows:
        label = row["group"]
        if (row.get("search_status") != "search_failed"
                or row.get("source_screen", {}).get("typed_goal_count") != 1
                or row.get("r2_blocker_classification") != r2_map[label]["blocker_classification"]
                or row.get("r1_diagnostics_exact") != r1_map[label].get("diagnostics", [])):
            raise RuntimeError(f"R3 does not reconcile with R1/R2: {label}")
    return r3, r1, r2, {row["group"]: row for row in rows}


def evaluate_root_proposals(proposals: tuple, screened: object, goal: object) -> dict[str, Any]:
    """Record root proposals and exact GIVEN matches, never prove their subgoals."""
    from phase165_r3_recursive_search import GoalExpansion
    from proof import ProofRule

    if not isinstance(proposals, tuple) or not all(isinstance(item, GoalExpansion) for item in proposals):
        raise TypeError("root expansion provider did not return typed GoalExpansion tuple")
    eligible_steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    exact_root_given = sum(type(s.conclusion) is type(goal) and s.conclusion == goal for s in eligible_steps)
    previews: list[dict[str, Any]] = []
    total_subgoals = 0
    matched_subgoals = 0
    for index, candidate in enumerate(proposals):
        matches = tuple(any(type(step.conclusion) is type(sub) and step.conclusion == sub
                            for step in eligible_steps) for sub in candidate.subgoals)
        total_subgoals += len(candidate.subgoals)
        matched_subgoals += sum(matches)
        if index >= MAX_RECORDED_EXPANSIONS:
            continue
        ref = getattr(candidate.rule, "literature_reference", None)
        previews.append({
            "index": index,
            "rule_name": str(getattr(candidate.rule, "name", type(candidate.rule).__name__)),
            "rule_type": type(candidate.rule).__name__,
            "rule_locator_metadata": (getattr(ref, "locator", None) or getattr(ref, "label", None)) if ref else None,
            "subgoal_count": len(candidate.subgoals),
            "subgoals": [
                {"type": type(sub).__name__, "repr": clipped(sub), "screened_exact_given": match}
                for sub, match in zip(candidate.subgoals, matches)
            ],
        })
    return {
        "root_expansion_count": len(proposals),
        "recorded_expansion_count": len(previews),
        "unrecorded_expansion_count": len(proposals) - len(previews),
        "screened_given_count": len(eligible_steps),
        "root_exact_given_count": exact_root_given,
        "proposed_subgoal_occurrences": total_subgoals,
        "directly_given_subgoal_occurrences": matched_subgoals,
        "proposals": previews,
    }


def classify_root_evidence(data: dict[str, Any]) -> str:
    """Classification of search coverage, not mathematical validity."""
    count = data.get("root_expansion_count")
    if type(count) is not int or count < 0:
        return "PROPOSAL_AUDIT_UNDETERMINED"
    if count == 0:
        return "NO_ROOT_EXPANSION_PROPOSED"
    if data.get("proposed_subgoal_occurrences", 0) > data.get("directly_given_subgoal_occurrences", 0):
        return "ROOT_EXPANSIONS_WITH_UNPROVED_SUBGOALS"
    return "ROOT_EXPANSIONS_PRESENT_REPLAY_UNRESOLVED"


def inspect_case(bridge: object, row: dict[str, Any], n: int, k: int) -> dict[str, Any]:
    """Rebuild precisely the production root provider, without recursive search."""
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r9_shared_math import shared_expansion_provider

    label = f"pi_{n+k}^{n}"
    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    if len(candidates) != 1:
        raise RuntimeError(f"{label} no longer has a unique typed goal")
    goal = candidates[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    observed = row["source_screen"]
    if observed["citation_ids"] != [citing_id]:
        raise RuntimeError(f"{label} citing assertion changed since R3")
    if citing_id is None:
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
        mode = "INDEPENDENTLY_POSITIONED_DERIVED_TARGET"
    else:
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing_id,
            explicit_publication_target=True,
        )
        mode = "POSITIONED_CITING_ASSERTION"
    if observed["source_screen_mode"] != mode:
        raise RuntimeError(f"{label} source screen mode changed since R3")
    # Apply the existing production context transformation before expansion.
    screened = prefer_universal_prop42_derivation(screened)
    provider = shared_expansion_provider(screened, proof_target=goal, prior_conclusions=())
    expansions = provider(goal)
    data = evaluate_root_proposals(expansions, screened, goal)
    return {
        "group": label, "n": n, "k": k, "goal_type": type(goal).__name__,
        "goal_repr": clipped(goal, 2500), "citing_assertion_id": citing_id,
        "source_screen_mode": mode,
        "r1_status": row["search_status"],
        "r1_diagnostics": row.get("r1_diagnostics_exact", []),
        "r1_open_goals": row.get("r1_open_goals_exact", []),
        "r3_classification": row["frontier"]["observed_category"],
        "root_evidence": data,
        "root_category": classify_root_evidence(data),
        "inference_replay_executed": False,
        "complete_proof_claimed": False,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 170 R3-R2 — 未完成5群の root expansion 監査", "",
        "既存 R1/R2/R3 の証拠を照合した上で、本番の根元 Goal に対する推論候補だけを検査した。",
        "候補の存在は証明の完成・再生成功・出典資格の保証ではない。", "",
        f"- HEAD: `{report['head']}`",
        f"- R3 report: `{report['r3_report']}`",
        f"- tracked/index 保持: `{report.get('tracked_unchanged')}`",
        "- 全体 pytest: 未実行", "",
        "| 群 | R3 の分類 | 根元推論候補 | 直接 GIVEN に一致した前提 / 全前提 | R3-R2 分類 |",
        "|---|---|---:|---:|---|",
    ]
    for row in report.get("cases", []):
        root = row.get("root_evidence", {})
        lines.append(
            f"| `{row['group']}` | `{row.get('r3_classification', '-')}` | "
            f"{root.get('root_expansion_count', '-')} | "
            f"{root.get('directly_given_subgoal_occurrences', '-')}/{root.get('proposed_subgoal_occurrences', '-')} | "
            f"`{row.get('root_category', 'AUDIT_ERROR')}` |"
        )
    lines.extend(["", "## 各群の根元推論候補", ""])
    for row in report.get("cases", []):
        lines.append(f"### `{row['group']}`")
        lines.append("")
        if "error" in row:
            lines.append(f"- 監査エラー: `{row['error']}`")
        else:
            lines.append(f"- Goal: `{row['goal_repr']}`")
            lines.append(f"- R1 diagnostic: `{clipped(row['r1_diagnostics'], 2400)}`")
            lines.append(f"- R1 open goals: `{clipped(row['r1_open_goals'], 2400)}`")
            lines.append(f"- 根元候補総数: `{row['root_evidence']['root_expansion_count']}`")
            for candidate in row["root_evidence"]["proposals"]:
                lines.append(f"- 候補{candidate['index']}: `{candidate['rule_name']}` / {candidate['subgoal_count']}前提")
                for sub in candidate["subgoals"]:
                    lines.append(f"  - `{sub['type']}` GIVEN={sub['screened_exact_given']}: `{sub['repr']}`")
            if row["root_evidence"]["unrecorded_expansion_count"]:
                lines.append(f"- 表示省略候補: {row['root_evidence']['unrecorded_expansion_count']}件（JSONに総数記録）")
        lines.append("")
    lines.extend([
        "## 判定の限界", "",
        "`NO_ROOT_EXPANSION_PROPOSED` は現行推論候補生成の未接続を示すにとどまり、数学定理が存在しないとはいえない。",
        "`ROOT_EXPANSIONS_WITH_UNPROVED_SUBGOALS` は直接 GIVEN に無い前提があるというだけで、再帰的に証明不能とはいえない。",
        "`ROOT_EXPANSIONS_PRESENT_REPLAY_UNRESOLVED` も実際の証明が完成したことを意味しない。",
        "新規の数学規則、Goal、ProofStep、出典、完成表示を追加しない。",
        "R4 実装に進む前に、未解決の下位 Goal と出典の精査が必要。", "",
    ])
    return "\n".join(lines)


def run(root: Path, r3_path: Path, output: Path) -> int:
    if not root.is_dir() or output.exists() or output == root or root in output.parents:
        raise RuntimeError("refusing missing repository or unsafe/previously used output path")
    reviewed = load_reviewed_r3_code(root)
    checked = reviewed.preflight(root)
    if checked["head"] != REVIEWED_HEAD:
        raise RuntimeError(f"unreviewed HEAD {checked['head']}; R3-R2 requires {REVIEWED_HEAD}")
    r3, _r1, _r2, indexed = check_reports(reviewed, root, r3_path)
    before = reviewed.tracked_snapshot(root)
    output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(root))
    report: dict[str, Any] = {
        "phase": "170 R3-R2", "mode": "AUDIT_ONLY", "head": checked["head"],
        "r3_report": str(r3_path),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "full_pytest_run": False, "production_changed": False,
        "recursive_search_executed": False, "cases": [],
    }
    try:
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        bridge = build_shared_typed_bridge()
        for n, k in TARGETS:
            label = f"pi_{n+k}^{n}"
            print(f"PHASE170_R3R2_CASE_START={label}", flush=True)
            try:
                case = inspect_case(bridge, indexed[label], n, k)
            except Exception as exc:
                case = {"group": label, "root_category": "AUDIT_ERROR",
                        "error": f"{type(exc).__name__}: {exc}",
                        "traceback": traceback.format_exc()}
            report["cases"].append(case)
            print(f"PHASE170_R3R2_{label}={case['root_category']}", flush=True)
    finally:
        report["tracked_unchanged"] = reviewed.tracked_snapshot(root) == before
        report["review_required"] = any("error" in c for c in report["cases"])
        (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output / "audit.md").write_text(render_markdown(report), encoding="utf-8")
        print(f"PHASE170_R3R2_REPORT={output / 'audit.md'}", flush=True)
        print(f"PHASE170_R3R2_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print("PHASE170_R3R2_FULL_PYTEST=False", flush=True)
    success = report["tracked_unchanged"] and not report["review_required"] and len(report["cases"]) == 5
    print(f"PHASE170_R3R2_AUDIT_EXECUTION={'PASS' if success else 'REVIEW_REQUIRED'}", flush=True)
    return 0 if success else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--r3-report", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        return run(args.root.resolve(), args.r3_report.resolve(), args.output.resolve())
    except Exception:
        print("PHASE170_R3R2_REFUSED=" + traceback.format_exc(), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
