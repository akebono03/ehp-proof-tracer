"""Inspect canonical image claims and unresolved target-generator identifications."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r10_general_toda56_core.core import checked_abstract_inputs
from phase173_r4_r4_typed_generator_audit.audit import _group_components
from phase173_r4_r15r2_generator_obligation_audit.audit import inspect_k as inspect_r15r2
from phase173_r4_r15r3_formal_suspension_bridge.bridge import (
    canonical_formal_suspension,
    expand_canonical_formal_image,
    formal_image_goal,
)


def _component_kind(component: object) -> tuple[str, int] | None:
    if isinstance(component, FreeCyclicGroup):
        return ("free", 0)
    if isinstance(component, FiniteCyclicGroup) and type(component.order) is int:
        return ("finite", component.order)
    return None


def inspect_k(k: int) -> dict[str, object]:
    """Do not choose a named target when equal-order matches are ambiguous."""
    base = inspect_r15r2(k)
    goal = exact_prior_database_result(4, k)
    pair = checked_abstract_inputs(goal) if goal is not None else None
    row: dict[str, object] = {
        "k": k,
        "abstract_compatible": pair is not None,
        "canonical_formal_images": [],
        "named_generator_identifications_proved": 0,
        "group_proof_completed": False,
        "new_given_assertions": 0,
        "public_route_modified": False,
    }
    if pair is None:
        row["state"] = "ABSTRACT_PRIOR_UNAVAILABLE"
        return row
    left, _ = pair
    lparts = _group_components(left)
    targets = _group_components(goal)
    if lparts is None or targets is None:
        raise RuntimeError("Previously checked abstract group lost typed components")
    if base["right_pending_indices"]:
        row["state"] = "RIGHT_MATCH_PENDING"
        return row
    residual = tuple(base["residual_target_indices"])
    rows: list[dict[str, object]] = []
    all_valid = True
    for j, source in enumerate(lparts):
        formal_goal = formal_image_goal(source.generator)
        available = (
            expand_canonical_formal_image(formal_goal)
            if formal_goal is not None else ()
        )
        admissible = bool(
            len(available) == 1
            and available[0].subgoals == ()
            and available[0].rule.match_guard((), {})
        )
        all_valid = all_valid and admissible
        kind = _component_kind(source)
        possible = tuple(
            index for index in residual
            if _component_kind(targets[index]) == kind
        )
        if not possible:
            all_valid = False
        rows.append({
            "source_index": j,
            "source_generator": str(source.generator),
            "formal_target_generator": (
                str(canonical_formal_suspension(source.generator))
                if formal_goal is not None else None
            ),
            "formal_rule_admissible": admissible,
            "source_component_order": list(kind) if kind else None,
            "possible_named_target_indices_by_order_only": list(possible),
            "named_target_identification_proved": False,
        })
    row["canonical_formal_images"] = rows
    row["all_formal_rules_admissible"] = all_valid
    row["residual_target_count"] = len(residual)
    row["state"] = (
        "FORMAL_IMAGES_AVAILABLE_NAMED_IDENTITIES_PENDING"
        if all_valid and rows else
        "NO_LEFT_GENERATOR_IMAGE_OBLIGATIONS"
        if all_valid else
        "FORMAL_IMAGE_OR_COMPONENT_CHECK_PENDING"
    )
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "data" / "sphere.csv").is_file():
        raise RuntimeError("Expected repository root")
    result = tuple(inspect_k(k) for k in (4, 7, 8, 31))
    report = {
        "phase": "173-R4-R15R3",
        "mode": "FORMAL_TYPED_SUSPENSION_IMAGE_ONLY",
        "rows": result,
        "public_completion": False,
        "named_equalities_are_not_derived": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for row in result:
        count = len(row["canonical_formal_images"])
        print(
            f"PHASE173_R4_R15R3_K={row['k']} "
            f"FORMAL_IMAGES={count} "
            f"RULES={row.get('all_formal_rules_admissible', False)} "
            f"NAMED_PROVED={row['named_generator_identifications_proved']} "
            f"STATE={row['state']}",
            flush=True,
        )
    k31 = result[-1]
    passed = (
        k31["abstract_compatible"] is True
        and len(k31["canonical_formal_images"]) == 4
        and k31.get("all_formal_rules_admissible") is True
        and k31["named_generator_identifications_proved"] == 0
        and all(
            len(item["possible_named_target_indices_by_order_only"]) == 4
            for item in k31["canonical_formal_images"]
        )
    )
    print("PHASE173_R4_R15R3_K31_FORMAL_IMAGES=" + ("PASS" if passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R3_NO_NAMED_IMAGE_ASSUMPTION=True", flush=True)
    print("PHASE173_R4_R15R3_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R3_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
