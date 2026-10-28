"""R10EM read-only audit of generator-image citation provenance in four groups."""
from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10a_verified_stable_chain_projection.projection import (
    project_verified_stable_image_chain,
)
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from phase169_r10em_citation_provenance_audit.provenance import (
    summarize_image_provenance,
    trace_generator_image_citations,
)
from proof import ProofRule, Relation

CASES = (
    (22, 6, "cyclic", 14, 31),
    (22, 10, "cyclic", 10, 40),
    (15, 8, "direct_sum", 5, 10),
    (24, 9, "direct_sum", 13, 110),
)


def inspect_case(bridge: object, n: int, k: int, shape: str,
                 exponent: int, hidden_count: int, output: Path) -> dict:
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    name = f"pi_{n+k}^{n}"
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or len(contexts) != 1):
        raise RuntimeError(f"R10EM incomplete source proof: {name}")
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing_id is None and not (isinstance(result.conclusion, Relation)
                                and result.conclusion.lhs == result.target):
        raise RuntimeError(f"R10EM derived goal mismatch: {name}")
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
        derived_target_without_citing_id=citing_id is None,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    before_ids = tuple(id(step) for step in model.steps)
    before_edges = tuple(tuple(id(parent) for parent in step.premises)
                         for step in model.steps)
    display = (
        project_verified_stable_image_chain(model, order)
        if shape == "cyclic" else project_verified_direct_sum_transport(model, order)
    )
    if display is None or len(display.hidden_indices) != hidden_count:
        raise RuntimeError(f"R10EM projection regression: {name}")
    root = model.steps[model.root_index]
    if root.rule is not ProofRule.INFERENCE or len(root.premises) < 4:
        raise RuntimeError(f"R10EM unexpected proof root: {name}")
    image_steps = root.premises[2:]
    findings = trace_generator_image_citations(model, order, image_steps)
    if findings is None:
        raise RuntimeError(f"R10EM could not trace original proof ancestry: {name}")
    provenance = summarize_image_provenance(findings, display.citation_numbers)
    if (provenance["missing_ancestors"]
            or provenance["unregistered_citations"]
            or not provenance["projection_matches_union"]
            or not provenance["every_image_has_cited_given"]):
        raise RuntimeError(f"R10EM provenance contract differs: {name}: {provenance}")
    markdown = render_model_backed_narrative_markdown(result, model)
    metrics = count_rendered_image_equations(markdown)
    if (metrics["total_occurrences"] != 0
            or metrics["extra_duplicate_occurrences"] != 0
            or rf"E^{{{exponent}}}" not in markdown
            or not markdown.rstrip().endswith("□")):
        raise RuntimeError(f"R10EM narrative regression: {name}")
    if any(f"**[R{citation.number}] " not in markdown
           for citation in model.citations):
        raise RuntimeError(f"R10EM reference visibility regression: {name}")
    if (tuple(id(step) for step in model.steps) != before_ids
            or tuple(tuple(id(parent) for parent in step.premises)
                     for step in model.steps) != before_edges
            or model.steps != result.proven_steps
            or any(model.steps[index].rule is not ProofRule.INFERENCE
                   or model.step_citation_numbers[index]
                   for index in display.hidden_indices)):
        raise RuntimeError(f"R10EM Proof Tree or citation changed: {name}")
    (output / f"pi_{n+k}_{n}.md").write_text(markdown, encoding="utf-8")
    return {
        "group": name,
        "shape": shape,
        "status": "complete",
        "trust": "PASS",
        "inference_steps": inferred,
        "given_steps": given,
        "proof_step_count": len(model.steps),
        "suspensions": exponent,
        "hidden_display_only": len(display.hidden_indices),
        "reference_count": len(model.citations),
        "provenance_summary": provenance,
        "image_provenance": [asdict(item) for item in findings],
        "mathematical_inference_added": False,
        "proof_tree_unchanged": True,
        "rendered_file": f"pi_{n+k}_{n}.md",
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m phase169_r10em_citation_provenance_audit.audit OUTPUT_DIR")
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    bridge = build_shared_typed_bridge()
    cases = [inspect_case(bridge, *item, output) for item in CASES]
    for case in cases:
        prefix = "R10EM_" + case["group"]
        stats = case["provenance_summary"]
        print(prefix + "_STATUS=" + case["status"], flush=True)
        print(prefix + "_TRUST=" + case["trust"], flush=True)
        print(prefix + "_IMAGES=" + str(stats["image_count"]), flush=True)
        print(prefix + "_INDIVIDUALLY_CITED=" + str(stats["images_with_cited_given"]), flush=True)
        print(prefix + "_CITATIONS_MATCH=" + str(stats["projection_matches_union"]), flush=True)
        print(prefix + "_HIDDEN=" + str(case["hidden_display_only"]), flush=True)
    report = {
        "phase": "169 R10EM",
        "mode": "AUDIT_ONLY",
        "summary": "Citation provenance of already verified generator transport",
        "cases": cases,
        "inference_rules_changed": False,
        "production_files_changed": False,
        "full_pytest_run": False,
    }
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("R10EM_REPORT=" + str(output / "audit.json"), flush=True)
    print("R10EM_AUDIT_STATUS=PASS", flush=True)
    print("R10EM_FULL_PYTEST_RUN=False", flush=True)


if __name__ == "__main__":
    main()
