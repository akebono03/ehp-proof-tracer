"""Observe real shared Renderer reference filtering without patching production code."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown

WATCH = frozenset({
    "build_toda_group_proof_narrative_reference_entries",
    "filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary",
    "exclude_toda_group_proof_narrative_root_reference",
    "filter_toda_group_proof_narrative_reference_entries_by_step_usage",
    "filter_toda_group_proof_narrative_reference_entries_by_body_usage",
    "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage",
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    "link_toda_group_proof_narrative_reference_body_consumers",
})
WATCH_FILES = frozenset({
    "toda_group_proof_narrative_references.py",
    "toda_group_proof_narrative_contribution_renderer.py",
})


def summarize_entries(entries):
    """Reduce reference entries to stable locator and proof-step identities."""
    if not isinstance(entries, (tuple, list)):
        return None
    result = []
    for entry in entries:
        ref = getattr(entry, "reference", None)
        steps = getattr(entry, "proof_steps", None)
        if ref is None or not isinstance(steps, tuple):
            return None
        result.append({
            "number": entry.number,
            "locator": ref.locator,
            "step_ids": [id(s) for s in steps],
        })
    return result


def summarize_ids(ids):
    """Summarize an actual set of step identities, if present."""
    if isinstance(ids, (set, frozenset)) and all(type(v) is int for v in ids):
        return sorted(ids)
    return None


def summarize_event(function_name, locals_map, return_value):
    """Capture the live filtering inputs and outputs, not synthetic substitutions."""
    row = {"function": function_name}
    for name in (
        "entries", "reference_entries", "original_entries", "filtered_entries",
        "phase157_r4_reference_entries_before_usage_filter",
    ):
        if name in locals_map:
            row[name] = summarize_entries(locals_map[name])
    for name in (
        "used_step_ids", "generic_used_step_ids", "boundary_visible_used_step_ids",
        "frontier_step_ids", "reference_owned_step_ids", "reference_internal_step_ids",
    ):
        if name in locals_map:
            row[name] = summarize_ids(locals_map[name])
    for name in ("body_markdown", "rendered", "suppressed_body"):
        if isinstance(locals_map.get(name), str):
            body = locals_map[name]
            row[name + "_contains_reference_marker"] = "[R" in body
            row[name + "_contains_reference_section"] = "使用する結果" in body
    if function_name == "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown":
        row["rendered_has_reference_section"] = "使用する結果" in return_value if isinstance(return_value, str) else None
        row["rendered_has_marker"] = "[R" in return_value if isinstance(return_value, str) else None
        row["final_internal_rendered"] = return_value if isinstance(return_value, str) else None
    elif function_name == "build_toda_group_proof_narrative_reference_entries":
        row["output_entries"] = summarize_entries(return_value)
    elif function_name in {
        "filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary",
        "filter_toda_group_proof_narrative_reference_entries_by_step_usage",
    }:
        row["output_entries"] = summarize_entries(return_value)
    elif function_name in {
        "exclude_toda_group_proof_narrative_root_reference",
        "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage",
        "filter_toda_group_proof_narrative_reference_entries_by_body_usage",
    } and isinstance(return_value, tuple):
        row["output_entries"] = summarize_entries(return_value[0])
    return row


def trace_render(result):
    """Profile one real render and collect return-time locals from selected code."""
    events = []
    def profiler(frame, event, arg):
        if event != "return":
            return
        if Path(frame.f_code.co_filename).name not in WATCH_FILES:
            return
        name = frame.f_code.co_name
        if name in WATCH:
            events.append(summarize_event(name, frame.f_locals, arg))
    old_profiler = sys.getprofile()
    try:
        sys.setprofile(profiler)
        markdown = render_partial_proof_markdown(result)
    finally:
        sys.setprofile(old_profiler)
    return markdown, events


def main():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=2)
    if len(goals) != 1:
        raise RuntimeError(f"expected unique pi_4^2 goal, found {len(goals)}")
    result = search_group_from_registered_goal(n=2, k=2, bridge=bridge, goal=goals[0])
    if result.status is not ProofSearchStatus.COMPLETE:
        raise RuntimeError(f"expected existing complete search, found {result.status}")
    markdown, events = trace_render(result)
    root = next(s for s in result.proven_steps if s.conclusion == result.conclusion)
    proof_steps = []
    for step in result.proven_steps:
        ref = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
        proof_steps.append({
            "step_id": id(step),
            "is_root": step is root,
            "rule": step.rule.value,
            "conclusion_type": type(step.conclusion).__name__,
            "locator": ref.locator if ref is not None else None,
            "premise_ids": [id(p) for p in step.premises],
        })
    report = {
        "audit": "phase168-r2-8-9",
        "read_only": True,
        "production_code_modified": False,
        "search_status": result.status.value,
        "proof_steps": proof_steps,
        "events": events,
        "rendered_markdown": markdown,
        "render_has_reference_section": "使用する結果" in markdown,
        "render_has_reference_marker": "[R" in markdown,
    }
    target = Path(__file__).resolve().parent / "output" / "renderer_runtime_trace.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("SEARCH_STATUS", result.status.value)
    print("OBSERVED_EVENTS", len(events))
    for event in events:
        if "output_entries" in event:
            print("STAGE", event["function"], "output", [x["locator"] for x in event["output_entries"] or []])
    print("RENDER_REFERENCE_SECTION", report["render_has_reference_section"])
    print("REPORT:", target)


if __name__ == "__main__":
    main()
