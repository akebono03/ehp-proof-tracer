"""Read-only comparison of k-unbounded abstract and named-generator gates."""
from __future__ import annotations

import json
from pathlib import Path

from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r10_general_toda56_core.core import (
    _abstract_group_signature,
    checked_abstract_inputs,
    checked_general_inputs,
)
from phase173_r4_r4_typed_generator_audit.audit import (
    _group_components,
    _map_components,
    _nu4_composed_image,
    _suspend_verified_shape,
)


def inspect_k(k: int) -> dict[str, object]:
    """Describe actual DB and typed frontier, without creating a proof leaf."""
    if type(k) is not int or k < 3:
        raise ValueError("This n=4 split requires integer k>=3")
    dimension = k + 4
    goal = exact_prior_database_result(4, k)
    first = exact_prior_database_result(3, k)
    second = exact_prior_database_result(7, dimension - 7)
    abstract = checked_abstract_inputs(goal) if goal is not None else None
    named = checked_general_inputs(goal) if goal is not None else None
    images = _map_components(*abstract) if abstract is not None else None
    target_components = _group_components(goal) if goal is not None else None
    left_components = _group_components(first) if first is not None else None
    right_components = _group_components(second) if second is not None else None
    left_pending = tuple(
        index for index, component in enumerate(left_components)
        if _suspend_verified_shape(component.generator) is None
    ) if left_components is not None else ()
    right_pending = tuple(
        index for index, component in enumerate(right_components)
        if _nu4_composed_image(component.generator) is None
    ) if right_components is not None else ()
    row = {
        "k": k,
        "group": f"pi_{dimension}^4",
        "registered": goal is not None,
        "first_prior": first is not None,
        "second_prior": second is not None,
        "target_signature": _abstract_group_signature(goal) if goal is not None else None,
        "first_signature": _abstract_group_signature(first) if first is not None else None,
        "second_signature": _abstract_group_signature(second) if second is not None else None,
        "abstract_inputs_eligible": abstract is not None,
        "named_generator_inputs_eligible": named is not None,
        "mapped_generator_components": len(images) if images is not None else None,
        "left_component_count": len(left_components) if left_components is not None else None,
        "right_component_count": len(right_components) if right_components is not None else None,
        "left_suspension_shape_pending_indices": left_pending,
        "right_nu4_composition_shape_pending_indices": right_pending,
        "target_generator_components": len(target_components) if target_components is not None else None,
        "public_proof_complete_by_this_change": False,
    }
    row["frontier"] = (
        "MISSING_REGISTERED_SOURCE" if (goal is None or first is None or second is None)
        else "ABSTRACT_PRIOR_MISMATCH" if abstract is None
        else "NAMED_IMAGE_MATCH" if named is not None
        else "GENERATOR_IMAGE_PROOF_PENDING"
    )
    return row


def write_report(root: Path, output: Path) -> tuple[dict[str, object], ...]:
    rows = tuple(inspect_k(k) for k in (3, 4, 5, 6, 7, 8, 31))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "phase": "173-R4-R15R1",
        "mode": "ABSTRACT_STRUCTURE_ONLY",
        "rows": rows,
        "all_named_generator_claims_require_separate_proof": True,
        "no_proof_steps_created": True,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print("PHASE173_R4_R15R1_K=" + str(row["k"])
              + " ABSTRACT=" + str(row["abstract_inputs_eligible"])
              + " GENERATORS=" + str(row["named_generator_inputs_eligible"])
              + " FRONTIER=" + str(row["frontier"]), flush=True)
    print("PHASE173_R4_R15R1_REPORT=" + str(output), flush=True)
    return rows


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = Path(__file__).with_name("frontier_result.json")
    rows = write_report(root, report)
    selected = next(row for row in rows if row["k"] == 31)
    if not selected["registered"]:
        print("PHASE173_R4_R15R1_K31_REGISTERED=False", flush=True)
        return 2
    print("PHASE173_R4_R15R1_K31_ABSTRACT="
          + str(selected["abstract_inputs_eligible"]), flush=True)
    print("PHASE173_R4_R15R1_PUBLIC_COMPLETION=False", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
