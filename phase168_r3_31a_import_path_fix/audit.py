"""Read-only runtime instrumentation for the standard Web narrative route."""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parent.parent
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))
OUT = Path(__file__).resolve().parent / "output"
CASES = ((2, 1), (3, 1), (4, 1))


def static_route_check():
    entry = ast.parse((PROJECT / "web_group_proof.py").read_text(encoding="utf-8"))
    adapter = ast.parse((PROJECT / "phase165_r52_r3_web_adapter.py").read_text(encoding="utf-8"))
    entry_source = ast.get_source_segment((PROJECT / "web_group_proof.py").read_text(encoding="utf-8"), next(
        node for node in entry.body if isinstance(node, ast.FunctionDef)
        and node.name == "build_standard_web_group_proof_view"))
    adapter_source = ast.get_source_segment(
        (PROJECT / "phase165_r52_r3_web_adapter.py").read_text(encoding="utf-8"),
        next(node for node in adapter.body if isinstance(node, ast.FunctionDef)
             and node.name == "build_partial_web_group_proof_view"))
    return {
        "standard_entry_builds_linked_model": "build_linked_proof_narrative_model" in entry_source,
        "model_renderer_called_by_adapter": "render_model_backed_narrative_markdown" in adapter_source,
        "compatibility_path_still_present": 'citation_source == "legacy"' in entry_source,
        "trace_path_uses_compatibility": 'mode == "trace"' in entry_source,
        "model_missing_uses_partial_markdown": 'if narrative_model is None:' in adapter_source,
    }


def audit_one(n, k):
    import web_group_proof
    import phase165_r52_r3_web_adapter as adapter
    import phase168_r3_4_link_bridge as linker
    import phase168_r3_5_model_renderer as renderer

    events = []
    originals = (linker.build_linked_proof_narrative_model,
                 renderer.render_model_backed_narrative_markdown,
                 adapter.render_partial_proof_markdown)

    def linked(result, bridge):
        model = originals[0](result, bridge)
        events.append({"stage": "build_linked_model",
                       "same_proven_steps": model.steps == result.proven_steps,
                       "step_count": len(model.steps),
                       "citation_count": len(model.citations),
                       "citation_numbers": [c.number for c in model.citations]})
        return model

    def model_render(result, model):
        events.append({"stage": "model_renderer",
                       "same_proven_steps": model.steps == result.proven_steps,
                       "citation_count": len(model.citations)})
        value = originals[1](result, model)
        events.append({"stage": "model_renderer_output",
                       "reference_header": "使用する結果" in value,
                       "reference_marker_count": value.count("**[R"),
                       "complete_sequence_count": value.count("次の完全列を考える")})
        return value

    def fallback(result):
        events.append({"stage": "fallback_partial_markdown"})
        return originals[2](result)

    error = None
    view = None
    with (patch.object(linker, "build_linked_proof_narrative_model", linked),
          patch.object(renderer, "render_model_backed_narrative_markdown", model_render),
          patch.object(adapter, "render_partial_proof_markdown", fallback)):
        try:
            view = web_group_proof.build_standard_web_group_proof_view(
                n=n, k=k, max_depth=2, mode="narrative", citation_source="model")
        except Exception as exc:
            error = {"type": type(exc).__name__, "message": str(exc)}

    model_calls = sum(e["stage"] == "model_renderer" for e in events)
    linked_calls = sum(e["stage"] == "build_linked_model" for e in events)
    fallback_calls = sum(e["stage"] == "fallback_partial_markdown" for e in events)
    ok = (error is None and linked_calls == model_calls == 1 and
          fallback_calls == 0 and all(e.get("same_proven_steps", True) for e in events))
    return {
        "n": n, "k": k, "group": f"pi_{n+k}^{n}", "ok": ok,
        "error": error, "view_type": type(view).__name__ if view else None,
        "partial_result": getattr(view, "partial_result", None),
        "rendered_lines_count": len(view.rendered_lines) if view else None,
        "linked_model_calls": linked_calls, "model_renderer_calls": model_calls,
        "fallback_calls": fallback_calls,
        "events": events,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    static = static_route_check()
    cases = [] if args.static_only else [audit_one(*pair) for pair in CASES]
    passed = all(c["ok"] for c in cases) and all([
        static["standard_entry_builds_linked_model"],
        static["model_renderer_called_by_adapter"],
    ])
    outcome = {
        "status": "PASS" if passed else "FAIL",
        "audit_only": True,
        "scope": "standard Web narrative mode with citation_source=model",
        "static": static,
        "cases": cases,
        "limitations": [
            "This instruments the public Python Web entry, not an HTTP browser request.",
            "It does not prove the real Web UI selects this entry in every configuration.",
            "Compatibility paths (legacy citation and trace) remain explicitly available.",
            "Only entry-to-renderer calls are observed; nested source correctness is not proved.",
            "No global pytest suite is run.",
        ],
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "runtime_route_audit.json").write_text(
        json.dumps(outcome, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8")
    lines = ["# Phase 168 R3-31 — 実行経路監査", "",
             f"監査結果: **{outcome['status']}**", "",
             "対象: 標準 Web Narrative (`citation_source=model`)", "",
             "## 実行記録", "",
             "| 対象 | Model生成 | 共通Renderer | fallback | 判定 |",
             "|---|---:|---:|---:|---|"]
    for c in cases:
        lines.append(f"| {c['group']} | {c['linked_model_calls']} | "
                     f"{c['model_renderer_calls']} | {c['fallback_calls']} | "
                     f"{'PASS' if c['ok'] else 'FAIL'} |")
    lines.extend(["", "## 静的確認", ""])
    lines.extend(f"- {k}: {v}" for k, v in static.items())
    lines.extend(["", "## 限界", ""])
    lines.extend(f"- {note}" for note in outcome["limitations"])
    (OUT / "runtime_route_audit.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    print("\n".join(lines))
    print("JSON:", OUT / "runtime_route_audit.json")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
