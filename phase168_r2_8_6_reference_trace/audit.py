"""Read-only trace of pi_4^2 proof-step reference provenance."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_references import (
    build_toda_group_proof_narrative_reference_entries,
    extract_toda_group_proof_step_literature_reference,
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def describe_step(step):
    """Retain observed reference and rule metadata without fabricating citations."""
    rule = getattr(step, "inference_rule", None)
    literature = getattr(rule, "literature_reference", None)
    extracted = extract_toda_group_proof_step_literature_reference(step)
    return {
        "rule": str(getattr(step.rule, "value", step.rule)),
        "conclusion": repr(step.conclusion),
        "premise_count": len(step.premises),
        "inference_rule_name": getattr(rule, "name", None),
        "inference_literature_locator": getattr(literature, "locator", None),
        "extracted_locator": getattr(extracted, "locator", None),
        "extracted_label": getattr(extracted, "label", None),
    }


def describe_entries(entries):
    return [{"number": e.number, "locator": e.reference.locator,
             "step_count": len(e.proof_steps),
             "conclusions": [repr(s.conclusion) for s in e.proof_steps]}
            for e in entries]


def inspect():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=2)
    report = {"audit": "phase168-r2-8-6", "read_only": True,
              "production_code_modified": False, "goal_count": len(goals)}
    if len(goals) != 1:
        return report
    goal = goals[0]
    report["citing_assertion_id"] = resolve_specialized_goal_citing_id(bridge, goal)
    result = search_group_from_registered_goal(n=2, k=2, bridge=bridge, goal=goal)
    report["search_status"] = result.status.value
    report["result_references"] = list(result.references)
    report["proven_steps"] = [describe_step(s) for s in result.proven_steps]
    report["completed"] = result.status.value == "complete"
    if not report["completed"]:
        report["diagnostics"] = list(result.diagnostics)
        return report
    roots = [s for s in result.proven_steps if s.conclusion == result.conclusion]
    report["root_count"] = len(roots)
    if len(roots) != 1:
        return report
    root = roots[0]
    report["root"] = describe_step(root)
    structure = result.conclusion.rhs
    if isinstance(structure, (FiniteCyclicGroup, FreeCyclicGroup)):
        generators = (structure.generator,)
        orders = (structure.order,) if isinstance(structure, FiniteCyclicGroup) else (None,)
    else:
        report["replay_skipped"] = "unsupported structure type"
        return report
    entry = ProofRepositoryEntry(key="phase165:typed:completed", step=root, phase="165")
    group_result = TodaGroupResult(target=result.target, group_structure=structure,
                                   generators=generators, generator_orders=orders,
                                   source_entry=entry, proof_step=root)
    replay = build_complete_toda_group_result_proof_replay(group_result)
    presentation = build_toda_group_proof_presentation(replay)
    report["replay_steps"] = [dict(depth=node.depth, **describe_step(node.proof_step))
                              for node in replay.steps]
    report["presentation_edge_count"] = len(presentation.edges)
    raw_entries = build_toda_group_proof_narrative_reference_entries(presentation)
    report["raw_reference_entries"] = describe_entries(raw_entries)
    try:
        fixed_entries = filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
            raw_entries, presentation.root_step)
        report["fixed_boundary_entries"] = describe_entries(fixed_entries)
    except Exception as exc:
        report["fixed_boundary_error"] = f"{type(exc).__name__}: {exc}"
    try:
        report["rendered_markdown"] = render_toda_group_proof_narrative_markdown(presentation)
    except Exception as exc:
        report["render_error"] = f"{type(exc).__name__}: {exc}"
    return report


def main():
    report = inspect()
    path = Path(__file__).resolve().parent / "output" / "reference_trace.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key in ("search_status", "root_count", "presentation_edge_count"):
        print(key.upper(), report.get(key))
    for key in ("proven_steps", "replay_steps", "raw_reference_entries", "fixed_boundary_entries"):
        print(key.upper(), len(report.get(key, ())))
    print("REPORT:", path)


if __name__ == "__main__":
    main()
