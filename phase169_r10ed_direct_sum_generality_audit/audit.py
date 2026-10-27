"""R10ED: audit five independently verified, differently shaped direct sums.

This script does not patch source files, change search, infer statements or
promote presentation strings into proof evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import DirectSumGroup, TodaIteratedSuspensionMap
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from phase169_r10ed_direct_sum_generality_audit.adversarial import rejection_checks
from phase169_r10ed_direct_sum_generality_audit.profile import CASES, AuditCase, validate_coverage
from proof import ProofRule, Relation

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"


def inspect_case(bridge: object, case: AuditCase) -> dict:
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=case.n, k=case.k, bridge=bridge, context_sink=contexts.append,
    )
    name = f"pi_{case.n+case.k}^{case.n}"
    if result.status is not ProofSearchStatus.COMPLETE or result.open_goals or not contexts:
        raise RuntimeError(f"R10ED searched proof incomplete or unscreened: {name}")
    if not isinstance(result.conclusion, Relation) or not isinstance(result.conclusion.rhs, DirectSumGroup):
        raise RuntimeError(f"R10ED non-direct-sum target: {name}")
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing_id is None and result.conclusion.lhs != result.target:
        raise RuntimeError(f"R10ED derived proof target mismatch: {name}")
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[-1], citing_assertion_id=citing_id,
        derived_target_without_citing_id=(citing_id is None),
    )
    model = build_linked_proof_narrative_model(result, contexts[-1])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    before_ids = tuple(id(item) for item in model.steps)
    before_links = tuple(tuple(id(parent) for parent in item.premises) for item in model.steps)
    before_given = sum(item.rule is ProofRule.GIVEN for item in model.steps)

    display = project_verified_direct_sum_transport(model, order)
    if display is None:
        raise RuntimeError(f"R10ED missing verified direct-sum projection: {name}")
    root = model.steps[model.root_index]
    prior, iso, *images = root.premises
    mapping = getattr(iso.conclusion, "map", None)
    if (not isinstance(mapping, TodaIteratedSuspensionMap)
            or mapping.exponent != case.expected_suspensions
            or len(root.conclusion.rhs.summands) != case.expected_summands
            or len(prior.conclusion.rhs.summands) != case.expected_summands
            or len(images) != case.expected_suspensions * case.expected_summands):
        raise RuntimeError(f"R10ED suspension / summand cardinality mismatch: {name}")
    expected_prefix = rf"$E^{{{case.expected_suspensions}}}("
    if display.statement.count(expected_prefix) != case.expected_summands:
        raise RuntimeError(f"R10ED aggregate displays wrong number of summands: {name}")

    body = render_model_backed_narrative_markdown(result, model)
    if body.count(display.statement) != 1:
        raise RuntimeError(f"R10ED verified equation not shown exactly once: {name}")
    if any(
        f"**[R{citation.number}] {citation.reference.locator or citation.reference.label}.**"
        not in body
        for citation in model.citations
    ):
        raise RuntimeError(f"R10ED citation lost from Reference section: {name}")
    if not set(display.citation_numbers).issubset({c.number for c in model.citations}):
        raise RuntimeError(f"R10ED aggregate citations not registered: {name}")
    metrics = count_rendered_image_equations(body)
    if metrics["extra_duplicate_occurrences"]:
        raise RuntimeError(f"R10ED duplicate image prose: {name}")
    if (before_ids != tuple(id(item) for item in model.steps)
            or before_links != tuple(tuple(id(parent) for parent in item.premises)
                                     for item in model.steps)
            or before_given != sum(item.rule is ProofRule.GIVEN for item in model.steps)
            or len(model.steps) != len(result.proven_steps)):
        raise RuntimeError(f"R10ED projection modified the Proof Tree: {name}")
    if any(model.steps[i].rule is not ProofRule.INFERENCE or model.step_citation_numbers[i]
           for i in display.hidden_indices):
        raise RuntimeError(f"R10ED hid a GIVEN or separately cited step: {name}")
    if not body.rstrip().endswith("□"):
        raise RuntimeError(f"R10ED completed narrative lost its closing mark: {name}")

    refusal = rejection_checks(model, order)
    if not all(refusal.values()):
        failed = [key for key, passed in refusal.items() if not passed]
        raise RuntimeError(f"R10ED unsafe compression in {name}: {failed}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    filename = f"pi_{case.n+case.k}_{case.n}.md"
    (OUTPUT / filename).write_text(body, encoding="utf-8")
    return {
        "group": name,
        "status": result.status.value,
        "trust_boundary": "PASS",
        "inference_steps_verified": inferred,
        "given_steps_verified": given,
        "stem": case.k,
        "suspensions": mapping.exponent,
        "summands": len(root.conclusion.rhs.summands),
        "certified_images": len(images),
        "hidden_in_narrative_only": len(display.hidden_indices),
        "proof_steps_retained": len(model.steps),
        "reference_count": len(model.citations),
        "aggregate_citations": list(display.citation_numbers),
        "rendered_chars": len(body),
        "duplicate_image_prose": metrics["extra_duplicate_occurrences"],
        "fail_closed": refusal,
        "rendered_file": filename,
    }


def main() -> None:
    validate_coverage(CASES)
    bridge = build_shared_typed_bridge()
    cases = [inspect_case(bridge, item) for item in CASES]
    report = {
        "phase": "169 R10ED",
        "mode": "AUDIT_ONLY",
        "requires_prior_verified_r10ec": True,
        "original_public_web_trust_boundary_unchanged": True,
        "all_full_suite_tests_run": False,
        "cases": cases,
        "limits": [
            "Positive coverage covers 8-stem and 9-stem, with 2 and 3 summands; it is not a proof for every stem.",
            "Projection is callable only behind the established complete-proof Web trust boundary; audit mutations are never treated as proofs.",
            "Compression requires at least two suspensions and a cited image for every summand at every stage.",
        ],
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    dest = OUTPUT / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in cases:
        key = "R10ED_" + item["group"]
        print(key + "_STATUS=" + item["status"])
        print(key + "_TRUST=" + item["trust_boundary"])
        print(key + "_STEM=" + str(item["stem"]))
        print(key + "_SUSPENSIONS=" + str(item["suspensions"]))
        print(key + "_SUMMANDS=" + str(item["summands"]))
        print(key + "_FAIL_CLOSED=" + str(sum(item["fail_closed"].values()))
              + "/" + str(len(item["fail_closed"])))
        print(key + "_DUPLICATES=" + str(item["duplicate_image_prose"]))
    print("R10ED_AUDIT_JSON=" + str(dest))
    print("R10ED_PRODUCTION_FILES_CHANGED=none")
    print("R10ED_PROOF_RULES_CHANGED=False")
    print("R10ED_FULL_PYTEST_RUN=False")
    print("R10ED_GENERALITY_AUDIT=PASS")


if __name__ == "__main__":
    main()
