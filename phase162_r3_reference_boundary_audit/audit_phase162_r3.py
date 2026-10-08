"""Audit only: inspect Phase 162 R2's verified proof and literature boundary.

Does not classify an application as a fixed theorem merely because it has a
literature reference. Does not manufacture a general form from an instance.
"""

from __future__ import annotations

import json
from collections import Counter

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import reconstruct_phase161_r7_validated_goal
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_group_proof_narrative_references import (
    extract_toda_group_proof_step_literature_reference,
)
from toda_literature_statement_boundary import (
    TodaLiteratureStatementClassification,
    classify_toda_literature_statement_step,
)


def _build_validated():
    leaves = build_phase59_3_data()["premise_steps"]
    roots_by_id = {}
    seen = set()

    def walk(step):
        identity = id(step)
        if identity in seen:
            return
        seen.add(identity)
        if step.rule is ProofRule.GIVEN:
            roots_by_id[identity] = step
        for premise in step.premises:
            walk(premise)

    for leaf in leaves:
        walk(leaf)
    return reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), leaves, tuple(roots_by_id.values())
    )


def build_audit():
    validated = _build_validated()
    presentation = build_validated_backward_proof_presentation(validated)
    records = []
    for index, step in enumerate(presentation.nodes, 1):
        boundary = classify_toda_literature_statement_step(step)
        reference = extract_toda_group_proof_step_literature_reference(step)
        classification = (
            boundary.classification.value if boundary is not None else "untracked"
        )
        fixed = (
            boundary is not None
            and boundary.classification == TodaLiteratureStatementClassification.FIXED_STATEMENT
        )
        records.append({
            "index": index,
            "conclusion_type": type(step.conclusion).__name__,
            "proof_rule": step.rule.value,
            "inference_rule": step.inference_rule.name if step.inference_rule else None,
            "classification": classification,
            "boundary_locator": boundary.reference_locator if boundary else None,
            "component_key": boundary.component_key if boundary else None,
            "reference_locator": reference.locator if reference else None,
            "reference_candidate": fixed,
            "reference_present_but_not_fixed": reference is not None and not fixed,
            "premise_indices": [
                next(i for i, candidate in enumerate(presentation.nodes, 1) if candidate is premise)
                for premise in step.premises
            ],
            "is_root": step is presentation.root_step,
        })
    return {
        "scope": "Phase 162 R3 audit only: no reference rendering or general-form synthesis",
        "verified_steps": validated.provenance.verified_steps,
        "verified_inferences": validated.provenance.verified_inferences,
        "node_count": len(records),
        "counts": dict(Counter(row["classification"] for row in records)),
        "records": records,
        "current_r2_markdown": render_validated_backward_proof_markdown(presentation),
    }


def main():
    result = build_audit()
    print(json.dumps({key: value for key, value in result.items() if key != "current_r2_markdown"}, ensure_ascii=False, indent=2))
    print("\n=== CURRENT R2 PROOF BODY (NOT YET R3 REFERENCE-SPLIT) ===\n")
    print(result["current_r2_markdown"])


if __name__ == "__main__":
    main()
