"""Audit completed direct-sum proof trees and their unchanged narrative text.

This is strictly observational: no ProofStep, citation, source registry, search
provider, renderer, or verification rule is added or modified.
"""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import DirectSumGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from proof import ProofRule, Relation
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations, render_report,
)

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
CASES = ((13, 9), (15, 8), (15, 9), (30, 9))



def audit_case(bridge: object, n: int, k: int) -> dict:
    """Repeat the actual public searched/screened trust-boundary handoff."""
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase168_r3_27_typed_statement_projection import element_tex

    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    is_complete = result.status is ProofSearchStatus.COMPLETE
    inferred_images = tuple(
        step.conclusion for step in result.proven_steps
        if step.rule is ProofRule.INFERENCE
        and isinstance(step.conclusion, GeneratorImage)
    )
    unsupported_images = tuple(
        image for image in inferred_images
        if element_tex(image.source_generator) is None
        or element_tex(image.target_generator) is None
    )
    item = {
        "goal": f"pi_{n+k}^{n}",
        "n": n,
        "k": k,
        "search_status": result.status.value,
        "open_goal_types": [type(goal).__name__ for goal in result.open_goals],
        "proven_steps": len(result.proven_steps),
        "inferred_generator_image_steps": len(inferred_images),
        "images_without_supported_element_tex": len(unsupported_images),
        "unsupported_image_examples": [
            {"source": repr(image.source_generator),
             "target": repr(image.target_generator)}
            for image in unsupported_images[:3]
        ],
        "screened_search_context_present": bool(contexts),
        "trust_boundary": "not_checked",
    }
    if not is_complete:
        return item
    if not contexts:
        item["trust_boundary"] = "REJECTED"
        item["trust_error"] = "search did not provide its screened context"
        return item

    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    item["citing_assertion_id"] = citing_id
    try:
        check_args = {"citing_assertion_id": citing_id}
        if citing_id is None:
            if (not isinstance(result.conclusion, Relation)
                    or result.conclusion.lhs != result.target):
                raise UnverifiedProofTree("uncited root is not the exact typed target")
            check_args["derived_target_without_citing_id"] = True
        inferred_count, given_count = verify_proof_tree_for_narrative(
            result, contexts[-1], **check_args,
        )
    except (UnverifiedProofTree, ValueError, TypeError) as exc:
        item["trust_boundary"] = "REJECTED"
        item["trust_error"] = f"{type(exc).__name__}: {exc}"
        return item

    item["trust_boundary"] = "PASS"
    item["trust_replayed_inference_steps"] = inferred_count
    item["trust_checked_given_steps"] = given_count
    model = build_linked_proof_narrative_model(result, contexts[-1])
    rendered = render_model_backed_narrative_markdown(result, model)
    item["root_is_direct_sum"] = (
        isinstance(result.conclusion, Relation)
        and isinstance(result.conclusion.rhs, DirectSumGroup)
    )
    item["used_reference_locators"] = [
        citation.reference.locator or citation.reference.label
        for citation in model.citations
    ]
    item["rendered_characters"] = len(rendered)
    item["rendered_nonempty_lines"] = sum(bool(line.strip()) for line in rendered.splitlines())
    item["rendered_image_equations"] = count_rendered_image_equations(rendered)
    item["displayed_terminal_square"] = rendered.rstrip().endswith("□")
    # Store the exact observed Markdown; never render an unverified proof.
    filename = f"pi_{n+k}_{n}.rendered.md"
    (OUTPUT / filename).write_text(rendered, encoding="utf-8")
    item["rendered_file"] = filename
    return item



def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    bridge = build_shared_typed_bridge()
    report = {
        "phase": "169 R10EA",
        "mode": "AUDIT_ONLY",
        "cases": [audit_case(bridge, n, k) for n, k in CASES],
        "production_files_changed": [],
        "full_pytest_run": False,
    }
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (OUTPUT / "audit.md").write_text(render_report(report), encoding="utf-8")
    for case in report["cases"]:
        prefix = "R10EA_" + case["goal"]
        print(prefix + "_STATUS=" + case["search_status"])
        print(prefix + "_TRUST=" + case["trust_boundary"])
        counts = case.get("rendered_image_equations", {})
        print(prefix + "_DUPLICATE_IMAGE_PROSE=" + str(
            counts.get("extra_duplicate_occurrences", "unavailable"),
        ))
        print(prefix + "_CHARACTERS=" + str(case.get("rendered_characters", "unavailable")))
        if "trust_error" in case:
            print(prefix + "_TRUST_ERROR=" + case["trust_error"])
    print("R10EA_AUDIT_JSON=" + str(OUTPUT / "audit.json"))
    print("R10EA_AUDIT_MD=" + str(OUTPUT / "audit.md"))
    print("R10EA_PRODUCTION_FILES_CHANGED=none")
    print("R10EA_FULL_PYTEST_RUN=False")
    if any(case["trust_boundary"] != "PASS" for case in report["cases"]):
        raise SystemExit("R10EA_PROOF_BOUNDARY=CHECK_REQUIRED")
    print("R10EA_AUDIT_AND_TRUST_BOUNDARY=PASS")


if __name__ == "__main__":
    main()
