"""Phase 168 R1: read-only audit of the active pi_4^2 proof route."""
from __future__ import annotations

import dataclasses
import json
import sys
import traceback
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "results"


def describe(value, *, limit=1800):
    try:
        rendered = repr(value)
    except Exception as exc:
        rendered = f"<repr error: {type(exc).__name__}: {exc}>"
    return rendered[:limit] + (" [TRUNCATED]" if len(rendered) > limit else "")


def capture_error(exc):
    return {"error_type": type(exc).__name__, "error": str(exc),
            "traceback": traceback.format_exc(limit=12)}


def goal_report(goals):
    return {"count": len(goals), "candidates": [describe(item) for item in goals]}


def result_report(result):
    return {
        "status": str(getattr(result, "status", None)),
        "structure_status": str(getattr(result, "structure_status", None)),
        "conclusion": describe(getattr(result, "conclusion", None)),
        "proven_count": len(getattr(result, "proven_steps", ())),
        "proven_steps": [{"rule": describe(getattr(step, "rule", None)),
                          "conclusion": describe(getattr(step, "conclusion", None))}
                         for step in getattr(result, "proven_steps", ())],
        "open_goals": [describe(goal) for goal in getattr(result, "open_goals", ())],
        "diagnostics": [str(d) for d in getattr(result, "diagnostics", ())],
        "references": [describe(r) for r in getattr(result, "references", ())],
    }


def main():
    sys.path.insert(0, str(ROOT))
    OUT.mkdir(exist_ok=True)
    report = {"phase": "168-R1", "target": "pi_4^2", "n": 2, "k": 2,
              "production_modified": False, "full_pytest_executed": False,
              "interpretation": "Goal data and search proposals are not evidence of a completed proof."}

    try:
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        bridge = build_shared_typed_bridge()
        assertions = tuple(bridge.registry._assertions.values())
        report["registry"] = {"assertion_count": len(assertions),
            "origin_counts": dict(Counter(str(a.origin) for a in assertions)),
            "related": [{"id": a.assertion_id,
                         "reference_id": a.reference_id,
                         "publication_position": getattr(a, "publication_position", None),
                         "component_position": getattr(a, "component_position", None),
                         "origin": str(a.origin), "content": describe(a.content)}
                        for a in assertions if any(token in (a.reference_id + ' ' + describe(a.content, limit=5000)).lower()
                                                 for token in ("5.2", "eta2_composition", "pi_4^3", "pi_4^2", "proposition 4.4"))][:100]}
        report["proof_links"] = {"count": len(bridge.proof_links),
           "related": [{"assertion_id": x.assertion_id, "step": describe(x.step)}
                       for x in bridge.proof_links if any(token in x.assertion_id.lower()
                                                         for token in ("5.2", "4.4", "pi4_3", "pi4_2"))][:60]}
    except Exception as exc:
        report["registry_error"] = capture_error(exc)
        bridge = None

    try:
        from phase166_r3af_goal_adapter import database_group_goal_candidates
        report["database_goal"] = goal_report(database_group_goal_candidates(n=2, k=2))
    except Exception as exc:
        report["database_goal_error"] = capture_error(exc)

    try:
        from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
        report["structured_goal"] = goal_report(database_structured_group_goal_candidates(n=2, k=2))
    except Exception as exc:
        report["structured_goal_error"] = capture_error(exc)

    try:
        from phase165_r55_nk_only_goal import registered_group_goal_candidates
        if bridge is not None:
            report["selected_goal"] = goal_report(registered_group_goal_candidates(bridge, n=2, k=2))
            report["pi43_goal"] = goal_report(registered_group_goal_candidates(bridge, n=3, k=1))
    except Exception as exc:
        report["selected_goal_error"] = capture_error(exc)

    try:
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        if bridge is not None:
            result = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
            report["active_search"] = result_report(result)
    except Exception as exc:
        report["active_search_error"] = capture_error(exc)

    try:
        from phase165_r52_r9_shared_math import shared_expansion_provider
        if bridge is not None:
            goals = registered_group_goal_candidates(bridge, n=2, k=2)
            if len(goals) == 1:
                provider = shared_expansion_provider(bridge, proof_target=goals[0])
                expansions = provider(goals[0])
                report["root_expansions"] = {
                    "count": len(expansions),
                    "items": [{"rule": describe(getattr(x, "rule", None)),
                               "premises": [describe(p) for p in getattr(x, "premises", ())]}
                              for x in expansions[:60]]}
            else:
                report["root_expansions"] = {"skipped": "selected Goal count != 1"}
    except Exception as exc:
        report["root_expansions_error"] = capture_error(exc)

    (OUT / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    active = report.get("active_search", {})
    issues = [key for key in report if key.endswith("_error")]
    lines = ["# Phase 168 R1 — pi_4^2 現状監査", "", "本監査は既存コード・DBを変更しない。", "",
             f"- Active status: `{active.get('status', 'not obtained')}`",
             f"- Proven steps: `{active.get('proven_count', 'not obtained')}`",
             f"- Open goals: `{len(active.get('open_goals', []))}`",
             f"- Root expansions: `{report.get('root_expansions', {}).get('count', 'not obtained')}`",
             f"- Errors: `{', '.join(issues) if issues else 'none'}`", "",
             "## 次の調査対象", ""]
    lines.extend(f"- `{item}`" for item in active.get("open_goals", [])[:30])
    lines.extend(["", "## 注意", "", "Goal の取得や Reference の登録は証明完了を意味しない。",
                  "探索で未解決が残れば R2 の実装判断はその結果に基づいて行う。", ""])
    (OUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"result": str(OUT / 'audit.json'),
                      "active_status": active.get("status"), "errors": issues}, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
