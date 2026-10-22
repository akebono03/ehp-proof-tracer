"""Read-only probe of reference usage filtering for pi_4^2."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from homotopy_groups import FiniteCyclicGroup
from phase165_r52_partial_proof import ProofSearchStatus
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_references import (
    build_toda_group_proof_narrative_reference_entries,
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
    exclude_toda_group_proof_narrative_root_reference,
    filter_toda_group_proof_narrative_reference_entries_by_step_usage,
)
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def entry_records(entries, used_step_ids=None):
    """Describe provenance only; no claims of mathematical derivation."""
    return [
        {
            "number": item.number,
            "locator": item.reference.locator,
            "label": item.reference.label,
            "step_ids": [id(step) for step in item.proof_steps],
            "used": None if used_step_ids is None else any(id(step) in used_step_ids for step in item.proof_steps),
        }
        for item in entries
    ]


def inspect():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=2)
    if len(goals) != 1:
        raise ValueError(f"expected unique pi_4^2 goal, got {len(goals)}")
    goal = goals[0]
    result = search_group_from_registered_goal(n=2, k=2, bridge=bridge, goal=goal)
    if result.status is not ProofSearchStatus.COMPLETE:
        raise ValueError(f"pi_4^2 is not complete: {result.status}")
    roots = [step for step in result.proven_steps if step.conclusion == goal]
    if len(roots) != 1:
        raise ValueError(f"expected unique root, got {len(roots)}")
    root = roots[0]
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        raise ValueError("expected finite cyclic target")
    group_result = TodaGroupResult(
        target=result.target,
        group_structure=goal.rhs,
        generators=(goal.rhs.generator,),
        generator_orders=(goal.rhs.order,),
        source_entry=ProofRepositoryEntry(key="phase168:reference:read-only", step=root, phase="168"),
        proof_step=root,
    )
    presentation = build_toda_group_proof_presentation(build_complete_toda_group_result_proof_replay(group_result))
    raw = build_toda_group_proof_narrative_reference_entries(presentation)
    fixed = filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(raw, root)
    eligible, statement_lines = exclude_toda_group_proof_narrative_root_reference(fixed, {}, root)
    premise_ids = frozenset(id(edge.premise_step) for edge in presentation.edges)
    retained_if_premises_used, _ = filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        eligible, statement_lines, premise_ids, root
    )
    retained_if_no_step_visible, _ = filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        eligible, statement_lines, frozenset(), root
    )
    rendered = render_toda_group_proof_narrative_markdown(presentation)
    return {
        "audit": "phase168-r2-8-8",
        "read_only": True,
        "search_status": result.status.value,
        "raw_entries": entry_records(raw),
        "fixed_entries": entry_records(fixed),
        "root_excluded_entries": entry_records(eligible),
        "premise_used_entries": entry_records(retained_if_premises_used, premise_ids),
        "empty_used_entries": entry_records(retained_if_no_step_visible, frozenset()),
        "note": "Synthetic premise/empty usage comparisons; actual internal generic_used_step_ids are not instrumented.",
        "rendered_markdown": rendered,
        "render_has_marker": "[R" in rendered,
        "render_has_reference_section": "使用する結果" in rendered,
    }


def main():
    result = inspect()
    dest = Path(__file__).resolve().parent / "output" / "reference_usage.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key in ("raw_entries", "fixed_entries", "root_excluded_entries", "premise_used_entries", "empty_used_entries"):
        print(key.upper(), len(result[key]))
    print("RENDER_MARKER", result["render_has_marker"])
    print("RENDER_REFERENCE_SECTION", result["render_has_reference_section"])
    print("REPORT:", dest)


if __name__ == "__main__":
    main()
