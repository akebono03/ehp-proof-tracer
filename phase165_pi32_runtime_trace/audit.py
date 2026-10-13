"""Read-only runtime trace for the existing pi_3^2 public narrative pipeline.

No production source changes, no pytest, and no proof reconstruction shortcuts.
"""
from __future__ import annotations

import functools
import json
import sys
import traceback
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
# The script resides in a subdirectory; make project modules importable.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
OUT = ROOT / "phase165_pi32_runtime_trace_output"
OUT.mkdir(exist_ok=True)
EVENTS = []
PATCHES = []


def text_excerpt(value, limit=1200):
    if not isinstance(value, str):
        return None
    return value[:limit]


def summary(value):
    if isinstance(value, str):
        return {
            "type": "str", "length": len(value),
            "delta_zero": [line[:450] for line in value.splitlines() if "\\Delta" in line or "零写像" in line][:16],
            "hopf_iso": [line[:450] for line in value.splitlines() if "同型" in line and ("$H" in line or "Hopf" in line)][:12],
            "reason_markers": {
                "完全性より": value.count("完全性より"),
                "これより": value.count("これより"),
                "単射": value.count("単射"),
                "全射": value.count("全射"),
                "使用する結果": value.count("使用する結果"),
                "[R": value.count("[R"),
            },
            "reference_section_excerpt": text_excerpt(value.split("## 使用する結果", 1)[1].split("## 証明", 1)[0], 1700) if "## 使用する結果" in value else None,
            "excerpt": text_excerpt(value, 420),
        }
    if isinstance(value, tuple):
        if len(value) <= 5:
            return {"type": "tuple", "count": len(value), "items": [summary(x) for x in value]}
        return {"type": "tuple", "count": len(value), "item_types": dict(Counter(type(x).__name__ for x in value))}
    if isinstance(value, list):
        return {"type": "list", "count": len(value), "item_types": dict(Counter(type(x).__name__ for x in value))}
    if isinstance(value, dict):
        return {"type": "dict", "count": len(value), "keys": [str(k) for k in list(value)[:15]]}
    if hasattr(value, "reasons"):
        reasons = tuple(value.reasons)
        return {"type": type(value).__name__, "count": len(reasons), "kinds": dict(Counter(getattr(getattr(r, "kind", None), "name", "unknown") for r in reasons)), "selected": [reason_detail(r) for r in reasons if selected_step(getattr(r, "conclusion_step", None))]}
    if hasattr(value, "nodes") and hasattr(value, "edges"):
        nodes = tuple(value.nodes)
        return {"type": type(value).__name__, "nodes": len(nodes), "edges": len(value.edges), "selected_steps": [step_detail(n.proof_step) for n in nodes if selected_step(n.proof_step)]}
    if hasattr(value, "proof_steps") and hasattr(value, "reference"):
        return {"type": type(value).__name__, "number": getattr(value, "number", None), "locator": str(getattr(value.reference, "locator", "")), "steps": len(value.proof_steps)}
    return {"type": type(value).__name__, "repr": repr(value)[:350]}


def selected_step(step):
    name = type(getattr(step, "conclusion", None)).__name__
    return name in {"TodaDeltaZeroStatement", "MapIsomorphism", "MapInjective", "MapSurjective", "TodaSuspensionIsomorphismStatement", "TodaHopfInvariantIsomorphismStatement"}


def step_detail(step):
    statement = step.conclusion
    return {"step_id": id(step), "type": type(statement).__name__, "conclusion": repr(statement)[:600], "rule": str(getattr(getattr(step, "rule", None), "name", "")), "inference_rule": getattr(getattr(step, "inference_rule", None), "name", None), "premise_ids": [id(p) for p in step.premises], "premise_types": [type(p.conclusion).__name__ for p in step.premises]}


def reason_detail(reason):
    return {"kind": getattr(reason.kind, "name", "unknown"), "conclusion": step_detail(reason.conclusion_step), "premises": [step_detail(p) for p in reason.premise_steps]}


def install(module, name, label=None):
    original = getattr(module, name, None)
    if original is None or not callable(original):
        EVENTS.append({"stage": label or name, "status": "NOT_FOUND"})
        return
    label = label or (module.__name__ + "." + name)
    @functools.wraps(original)
    def traced(*args, **kwargs):
        entry = {"stage": label, "status": "enter"}
        EVENTS.append(entry)
        try:
            result = original(*args, **kwargs)
        except Exception as exc:
            entry.update({"status": "ERROR", "error": repr(exc), "traceback": traceback.format_exc()[-2500:]})
            raise
        entry.update({"status": "ok", "result": summary(result)})
        return result
    setattr(module, name, traced)
    PATCHES.append((module, name, original))


def full_step_walk(root):
    seen = set()
    output = []
    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        if selected_step(step):
            output.append(step_detail(step))
        for premise in step.premises:
            visit(premise)
    visit(root)
    return {"total_unique_steps": len(seen), "selected": output}


def main():
    result = {"phase": "165 pi3^2 renderer runtime trace", "mode": "READ_ONLY_RUNTIME_STAGE_TRACE", "production_files_modified": False, "pytest_run": False, "status": "unstarted", "events": EVENTS}
    try:
        import web_group_proof as web
        import toda_group_proof_narrative_renderer as narrative
        import toda_group_proof_narrative_contribution_renderer as contribution
        import toda_group_proof_narrative_reason_renderer as reason_render
        import toda_group_proof_narrative_reasons as reasons

        # Instrument aliases where the pipeline looks up each function.
        install(web, "build_toda_group_proof_presentation", "web.presentation")
        install(web, "render_toda_group_proof_narrative_markdown", "web.narrative")
        install(narrative, "_phase158_baseline_render_toda_group_proof_narrative_markdown", "narrative.baseline")
        install(narrative, "_phase158_normalize_public_narrative_contract", "narrative.phase158_contract")
        install(narrative, "_phase159_r1_7c_r4_normalize_public_map_property_prose", "narrative.phase159_map_property")
        install(narrative, "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning", "narrative.phase159_numbered_reason")
        install(narrative, "_phase159_r1_7c_r4_reorder_public_equation_reference_conclusions", "narrative.phase159_reorder")
        install(narrative, "_phase160_r7_render_stable_finite_cyclic_transport_narrative", "narrative.stable_shortcut")
        install(narrative, "normalize_public_narrative_contract", "narrative.phase164_contract")
        install(narrative, "suppress_toda_group_proof_narrative_dangling_connectors", "narrative.final_connector_cleanup")
        install(narrative, "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown", "narrative.contributions")
        install(contribution, "build_toda_group_proof_narrative_reason_sidecar", "contrib.build_reason_sidecar")
        install(contribution, "insert_toda_group_proof_narrative_reason_prose", "contrib.insert_reasons")
        install(contribution, "build_toda_group_proof_narrative_reference_entries", "contrib.references_initial")
        install(contribution, "filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary", "contrib.references_fixed_boundary")
        install(contribution, "_select_toda_group_proof_narrative_reference_entries_and_statement_lines", "contrib.references_statement_selection")
        install(contribution, "exclude_toda_group_proof_narrative_root_reference", "contrib.references_exclude_root")
        install(contribution, "suppress_toda_group_proof_narrative_reference_internal_body", "contrib.suppress_reference_internal")
        install(contribution, "suppress_toda_group_proof_narrative_reference_body_duplicates", "contrib.suppress_reference_duplicates")
        install(contribution, "link_toda_group_proof_narrative_reference_body_consumers", "contrib.link_body_consumers")
        install(contribution, "normalize_toda_group_proof_narrative_connectors", "contrib.normalize_connectors")
        install(contribution, "merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows", "contrib.merge_exactness")
        install(contribution, "filter_toda_group_proof_narrative_reference_entries_by_body_usage", "contrib.references_body_usage")
        install(contribution, "order_toda_group_proof_narrative_injective_image_order_reason", "contrib.order_reason")
        install(contribution, "render_toda_group_proof_narrative_reference_entries_markdown", "contrib.reference_section")
        install(contribution, "suppress_toda_group_proof_narrative_dangling_connectors", "contrib.dangling_connectors")
        install(contribution, "render_toda_group_proof_narrative_multi_argument_markdown", "contrib.base_argument_markdown")
        install(contribution, "_insert_toda_group_proof_narrative_argument_contributions", "contrib.insert_contributions")

        view = web.build_standard_web_group_proof_view(n=2, k=1, max_depth=2, mode="narrative")
        result["status"] = "ok"
        result["web"] = {"rendered_lines": len(view.rendered_lines), "steps": len(view.steps), "markdown_line_sample": [str(x)[:350] for x in view.rendered_lines[:12]]}
        from toda_calculation_facade import build_standard_toda_report
        from phase164_r5_r2_common_replay import build_phase164_r5_r2_common_replay
        report = build_standard_toda_report(n=2, k=1)
        group_result = report.candidates[0].source_candidate.group_result
        replay = build_phase164_r5_r2_common_replay(n=2, k=1, group_result=group_result, max_depth=2, mode="narrative")
        result["proof"] = full_step_walk(replay.root_step)
    except Exception as exc:
        result["status"] = "error"
        result["error"] = repr(exc)
        result["traceback"] = traceback.format_exc()
    finally:
        for module, name, original in reversed(PATCHES):
            setattr(module, name, original)

    (OUT / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    lines = ["# Phase 165 pi3^2 Renderer Runtime Trace", "", "## 結果", "", f"- 状態: `{result['status']}`", f"- 取得したイベント: {len(EVENTS)}", "- 本番コード変更: なし", "- pytest: 未実施", "", "## ステージ別記録", ""]
    for i, event in enumerate(EVENTS, 1):
        s = event.get("result", {})
        lines.append(f"### {i}. {event['stage']} — {event['status']}")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(s if event["status"] == "ok" else event, ensure_ascii=False, indent=2, default=str)[:7200])
        lines.append("```")
        lines.append("")
    if result.get("error"):
        lines.extend(["## 実行時例外", "", "```text", result["traceback"], "```", ""])
    (OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"phase": "165 pi3^2 runtime trace", "status": result["status"], "events": len(EVENTS), "output_json": str(OUT / "audit.json"), "output_md": str(OUT / "report.md"), "production_files_modified": False, "pytest_run": False, "error": result.get("error")}, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
