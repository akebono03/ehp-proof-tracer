"""Read-only Phase 168 R3-2 runtime boundary audit."""
from __future__ import annotations

import json
import sys
import traceback
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

WATCHED = {
    "web_group_proof",
    "phase165_r55_nk_only_goal",
    "phase165_r52_r9_shared_math",
    "phase165_r52_r3_web_adapter",
    "toda_group_proof_narrative_renderer",
    "toda_group_proof_narrative_contribution_renderer",
    "toda_group_proof_narrative_references",
    "phase165_r52_partial_proof",
    "phase165_r52_r2_search_adapter",
}


def describe(value):
    if value is None:
        return None
    return {"type": type(value).__name__, "repr": repr(value)[:600]}


def inspect_step(step):
    rule = getattr(step, "rule", None)
    return {
        "step_type": type(step).__name__,
        "conclusion": describe(getattr(step, "conclusion", None)),
        "rule": describe(rule),
        "step_literature_reference": describe(getattr(step, "literature_reference", None)),
        "rule_literature_reference": describe(getattr(rule, "literature_reference", None)),
        "premise_count": len(getattr(step, "premises", ()) or ()),
        "attribute_names": [name for name in ("premises", "dependencies", "rule", "literature_reference", "conclusion") if hasattr(step, name)],
    }


def run_one(n, k):
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

    events = Counter()
    ordered = []
    def profile(frame, event, arg):
        if event != "call":
            return
        module = frame.f_globals.get("__name__", "")
        if module not in WATCHED:
            return
        function = frame.f_code.co_name
        key = f"{module}.{function}"
        events[key] += 1
        if len(ordered) < 400:
            ordered.append({"function": key, "line": frame.f_code.co_firstlineno})

    sys.setprofile(profile)
    try:
        result = search_group_from_registered_goal(n=n, k=k)
        view = build_partial_web_group_proof_view(result, max_depth=2, mode="narrative")
    finally:
        sys.setprofile(None)

    steps = tuple(getattr(result, "proven_steps", ()) or ())
    return {
        "goal": f"pi_{n+k}^{n}",
        "status": str(getattr(result, "status", None)),
        "step_count": len(steps),
        "steps": [inspect_step(step) for step in steps],
        "root_conclusion": describe(getattr(result, "conclusion", None)),
        "open_goals": [describe(x) for x in (getattr(result, "open_goals", ()) or ())],
        "view_key": getattr(view, "key", None),
        "rendered_lines": [{"prefix": str(x.prefix), "latex": str(x.statement_latex), "suffix": str(x.suffix)} for x in view.rendered_lines],
        "called_functions": dict(sorted(events.items())),
        "call_order_first_400": ordered,
    }


def main():
    outputs = []
    for n, k in ((2, 2), (2, 1), (3, 1), (4, 1)):
        label = f"pi_{n+k}^{n}"
        print("AUDIT", label, flush=True)
        try:
            outputs.append(run_one(n, k))
        except Exception as exc:
            sys.setprofile(None)
            outputs.append({"goal": label, "error": type(exc).__name__ + ": " + str(exc), "traceback": traceback.format_exc()})
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    path = out / "runtime_boundary.json"
    path.write_text(json.dumps({"kind": "READ_ONLY_RUNTIME_AUDIT", "results": outputs}, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    lines = ["# Phase 168 R3-2 実行経路監査", "", "本監査は変更・修正を行いません。", ""]
    for result in outputs:
        lines.extend([f"## {result['goal']}", ""])
        if "error" in result:
            lines.extend([f"- ERROR: `{result['error']}`", ""])
            continue
        lines.extend([f"- status: `{result['status']}`", f"- proven_steps: {result['step_count']}", f"- rendered_lines: {len(result['rendered_lines'])}", "", "### 出典付きステップ", ""])
        for index, step in enumerate(result["steps"]):
            lines.append(f"- step {index}: rule={step['rule']['repr'][:120] if step['rule'] else None}; step_ref={step['step_literature_reference']}; rule_ref={step['rule_literature_reference']}")
        lines.extend(["", "### 呼び出し回数", ""])
        for name, count in result["called_functions"].items():
            if any(word in name.lower() for word in ("reference", "narrative", "search", "adapter", "partial_proof")):
                lines.append(f"- `{name}`: {count}")
        lines.append("")
    md = out / "runtime_boundary.md"
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("AUDIT_ONLY: no production files modified")
    print("JSON:", path)
    print("MARKDOWN:", md)
    if any("error" in x for x in outputs):
        print("WARNING: one or more goals failed; inspect the JSON traceback")


if __name__ == "__main__":
    main()
