"""Phase 165 R57-R17: read-only runtime audit of ordinary typed group proof search.

No source files are modified. A short-lived spy records the existing calls to
search_registered_partial_proof; the real search function still runs unchanged.
"""
from __future__ import annotations

import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


TARGETS = ((2, 1), (3, 1), (4, 1))


def safe_string(value: object, limit: int = 600) -> str:
    try:
        result = str(value)
    except Exception as exc:
        result = f"<string-error: {type(exc).__name__}>"
    return result[:limit]


def summarize_result(result: object) -> dict:
    status = getattr(result, "status", None)
    steps = getattr(result, "proven_steps", ())
    goals = getattr(result, "open_goals", ())
    diagnostics = getattr(result, "diagnostics", ())
    return {
        "status": safe_string(getattr(status, "value", status)),
        "conclusion": safe_string(getattr(result, "conclusion", None)),
        "proven_step_count": len(steps or ()),
        "proven_step_rules": [safe_string(getattr(getattr(s, "rule", None), "value", getattr(s, "rule", None))) for s in (steps or ())],
        "open_goals": [safe_string(g) for g in (goals or ())],
        "diagnostics": [safe_string(d) for d in (diagnostics or ())],
    }


def diagnose(project: Path) -> dict:
    sys.path.insert(0, str(project))
    import phase165_r52_r9_shared_math as shared
    import phase165_r55_nk_only_goal as selector
    from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog

    evidence: dict = {
        "phase": "165 R57-R17",
        "mode": "READ_ONLY_RUNTIME_AUDIT",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(project),
        "source_modified": False,
        "full_pytest_run": False,
        "targets": [],
        "search_calls": [],
    }
    bridge = shared.build_shared_typed_bridge()
    evidence["bridge"] = {
        "references": len(bridge.registry._references),
        "assertions": len(bridge.registry._assertions),
        "proof_links": len(bridge.proof_links),
    }
    original_search = shared.search_registered_partial_proof

    def observed_search(*args, **kwargs):
        goal = kwargs.get("goal")
        context = kwargs.get("bridge")
        provider = kwargs.get("expansion_provider")
        call: dict = {
            "n": kwargs.get("n"), "k": kwargs.get("k"),
            "goal": safe_string(goal),
            "prior_completed_count": len(kwargs.get("completed_internal_proofs", ()) or ()),
            "screened_reference_links": len(getattr(context, "proof_links", ()) or ()),
        }
        try:
            expansions = provider(goal) if provider is not None else ()
            call["root_expansion_count"] = len(expansions)
            call["root_expansion_rules"] = [safe_string(getattr(x, "rule", None)) for x in expansions[:20]]
            call["root_expansion_subgoals"] = [
                [safe_string(g) for g in getattr(x, "subgoals", ())] for x in expansions[:10]
            ]
        except Exception as exc:
            call["expansion_inspection_error"] = f"{type(exc).__name__}: {exc}"
        evidence["search_calls"].append(call)
        try:
            result = original_search(*args, **kwargs)
            call["result"] = summarize_result(result)
            return result
        except Exception as exc:
            call["search_error"] = f"{type(exc).__name__}: {exc}"
            raise

    with patch.object(shared, "search_registered_partial_proof", observed_search):
        for n, k in TARGETS:
            target: dict = {"n": n, "k": k, "group": f"pi_{n+k}^{n}"}
            evidence["targets"].append(target)
            try:
                candidates = selector.registered_group_goal_candidates(bridge, n=n, k=k)
                target["candidate_count"] = len(candidates)
                target["candidates"] = [safe_string(x) for x in candidates[:10]]
                catalog, warning = resolve_reviewed_order_catalog(bridge, n=n, k=k)
                target["order_diagnostic"] = warning
                target["catalog_entries"] = [
                    {"position": record.position,
                     "statement": safe_string(record.statement),
                     "has_saved_proof": record.completed is not None}
                    for record in (catalog._records if catalog is not None else ())
                ]
                target["result"] = summarize_result(
                    selector.search_group_from_registered_goal(n=n, k=k, bridge=bridge)
                )
            except Exception as exc:
                target["error"] = f"{type(exc).__name__}: {exc}"
                target["traceback"] = traceback.format_exc(limit=8)
    return evidence


def render_report(info: dict) -> str:
    lines = ["Phase 165 R57-R17 — Read-only search audit", "", "Bridge: " + safe_string(info.get("bridge")), ""]
    for item in info.get("targets", ()):
        lines.append(f"{item['group']}: candidates={item.get('candidate_count', 'ERROR')}")
        lines.append("  order: " + safe_string(item.get("order_diagnostic")))
        lines.append("  catalog: " + safe_string(item.get("catalog_entries")))
        result = item.get("result", {})
        lines.append("  status: " + safe_string(result.get("status")))
        lines.append("  steps: " + safe_string(result.get("proven_step_count")))
        lines.append("  open_goals: " + safe_string(result.get("open_goals")))
        lines.append("  diagnostics: " + safe_string(result.get("diagnostics")))
        if "error" in item:
            lines.append("  ERROR: " + item["error"])
        lines.append("")
    lines.append("Actual calls to shared search:")
    for call in info.get("search_calls", ()):
        lines.append(f"  pi_{call.get('n', '?')} k={call.get('k', '?')} prior={call.get('prior_completed_count')} screened={call.get('screened_reference_links')} root_expansions={call.get('root_expansion_count', '?')}")
        lines.append("    expansion_rules: " + safe_string(call.get("root_expansion_rules"), 1500))
        lines.append("    result: " + safe_string(call.get("result", call.get("search_error")), 1500))
    lines.extend(["", "No code changed. This audit does not certify mathematical correctness."])
    return "\n".join(lines) + "\n"


def main() -> int:
    project = Path(__file__).resolve().parent.parent
    output = Path(__file__).resolve().parent
    try:
        evidence = diagnose(project)
    except Exception as exc:
        evidence = {"phase": "165 R57-R17", "fatal_error": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc(limit=15), "source_modified": False,
                    "full_pytest_run": False, "targets": [], "search_calls": []}
    (output / "audit_results.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    (output / "audit_results.txt").write_text(render_report(evidence), encoding="utf-8")
    print(render_report(evidence))
    if "fatal_error" in evidence:
        print(evidence["fatal_error"])
        return 1
    if any("error" in target for target in evidence["targets"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
