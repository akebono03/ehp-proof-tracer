"""Read-only audit of database-backed typed target display; no proof search."""
from __future__ import annotations

import json
from pathlib import Path

from phase166_r3af_goal_adapter import (
    database_group_goal_candidates,
    database_zero_group_goal_candidates,
)
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from web_group_proof_common import _group_proof_statement_latex
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view


def audit_112_targets() -> dict:
    """Inspect all 112 requested (n,k) without reconstructing any proof."""
    records = []
    for n in range(2, 16):
        for k in range(8):
            zero = database_zero_group_goal_candidates(n=n, k=k)
            structured = database_structured_group_goal_candidates(n=n, k=k) if k >= 2 else ()
            simple = database_group_goal_candidates(n=n, k=k)
            selected = zero or structured or simple
            source = "zero" if zero else "structured" if structured else "simple" if simple else "missing"
            entry = {"n": n, "k": k, "source": source, "goal_count": len(selected)}
            if len(selected) == 1:
                goal = selected[0]
                latex, fallback = _group_proof_statement_latex(goal)
                partial = make_partial_proof_result(
                    n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED,
                    open_goals=(goal,), diagnostics=("表示のみ監査",),
                )
                view = build_partial_web_group_proof_view(partial, mode="narrative")
                entry.update({
                    "latex": latex,
                    "web_target": view.conclusion_latex,
                    "fallback": fallback,
                    "target_matches": latex == view.conclusion_latex,
                    "has_equality": " = " in view.conclusion_latex,
                    "status_unchanged": view.partial_result,
                })
                entry["ok"] = bool(latex and not fallback and entry["target_matches"]
                                   and entry["has_equality"] and entry["status_unchanged"])
            else:
                entry.update({"latex": None, "web_target": None, "ok": False,
                              "reason": "DBから単一の型付きGoalに変換できない"})
            records.append(entry)
    counts = {name: sum(r["source"] == name for r in records)
              for name in ("zero", "structured", "simple", "missing")}
    issues = [r for r in records if not r["ok"]]
    return {"phase": "166-r3al-112-target-audit", "count": len(records),
            "production_code_modified": False, "source_counts": counts,
            "display_ok": len(records)-len(issues), "display_issues": len(issues),
            "issues": issues, "records": records}


def main():
    report = audit_112_targets()
    folder = Path(__file__).resolve().parent / "results"
    folder.mkdir(exist_ok=True)
    (folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = ["# Phase 166 R3-AL: 112 typed proof target display audit", "",
            f"- Count: {report['count']}", f"- Display OK: {report['display_ok']}",
            f"- Remaining issues: {report['display_issues']}",
            f"- Sources: {report['source_counts']}", "",
            "| n | k | source | result | target |", "|---:|---:|---|---|---|"]
    for item in report["records"]:
        target = (item["web_target"] or "NO_TYPED_GOAL").replace("|", "\\|")
        rows.append(f"| {item['n']} | {item['k']} | {item['source']} | "
                    f"{'OK' if item['ok'] else 'ISSUE'} | `${target}` |")
    (folder / "report.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("phase", "count", "source_counts",
                   "display_ok", "display_issues", "production_code_modified")},
                     ensure_ascii=False, indent=2))
    print("REPORT:", folder / "report.json")
    print("Full pytest NOT run; proofs NOT searched")


if __name__ == "__main__":
    main()
