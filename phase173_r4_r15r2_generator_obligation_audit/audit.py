"""Decompose named-generator obstruction without asserting any new identities.

No ProofStep, rule, GIVEN, or public-completion status is constructed here.
Existing generic functoriality is not treated as proof of atomic suspension images.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from expression import Composition, IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r4_typed_generator_audit.audit import (
    _group_components,
    _nu4_composed_image,
    _suspend_verified_shape,
    _typed_endpoints,
)
from phase173_r4_r6_alias_source_audit.audit import alias_equal
from phase173_r4_r10_general_toda56_core.core import checked_abstract_inputs
from phase169_r10eq_r1_universal_stable_definition.definition import (
    is_defined_stable_suspension,
)


def _factors(expression: object) -> tuple[object, ...]:
    """Flatten typed compositions only; preserve the original factor objects."""
    if isinstance(expression, Composition):
        return _factors(expression.left) + _factors(expression.right)
    return (expression,)


def _component_order(component: object) -> tuple[str, int] | None:
    """Distinguish free and finite cyclic terms without comparing generators."""
    if isinstance(component, FreeCyclicGroup):
        return ("free", 0)
    if isinstance(component, FiniteCyclicGroup):
        return ("finite", component.order) if type(component.order) is int else None
    return None


def _select_right_images(
    right: tuple[object, ...], target: tuple[object, ...],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Match only unambiguous exact/approved-alias right images.

    The result is a matching *audit*, not a homotopy group proof.
    An unmatched, ambiguously matching, or untyped image is left unresolved.
    """
    used: set[int] = set()
    matched: list[int] = []
    pending: list[int] = []
    for index, component in enumerate(right):
        image = _nu4_composed_image(component.generator)
        if image is None:
            pending.append(index)
            continue
        candidates = [
            j for j, item in enumerate(target)
            if j not in used
            and type(item) is type(component)
            and _component_order(item) == _component_order(component)
            and alias_equal(item.generator, image)
        ]
        if len(candidates) != 1:
            pending.append(index)
            continue
        selected = candidates[0]
        used.add(selected)
        matched.append(selected)
    residual = tuple(j for j in range(len(target)) if j not in used)
    return tuple(matched), tuple(pending), residual


def inspect_k(k: int) -> dict[str, object]:
    """Inspect any integer k>=3 without turning a DB candidate into a proof."""
    if type(k) is not int or k < 3:
        raise ValueError("The n=4 domain requires integer k>=3")
    dimension = 4 + k
    goal = exact_prior_database_result(4, k)
    pair = checked_abstract_inputs(goal) if goal is not None else None
    row: dict[str, object] = {
        "k": k,
        "dimension": dimension,
        "registered": goal is not None,
        "abstract_compatible": pair is not None,
        "proof_completed_by_this_audit": False,
        "new_proof_steps": 0,
        "new_given_assertions": 0,
    }
    if pair is None:
        row["state"] = "ABSTRACT_PRIORS_NOT_CERTIFIED"
        row["left_obligations"] = []
        row["right_matched_target_indices"] = []
        row["right_pending_indices"] = []
        row["residual_target_indices"] = []
        return row
    left, right = pair
    lparts = _group_components(left)
    rparts = _group_components(right)
    targets = _group_components(goal)
    if lparts is None or rparts is None or targets is None:
        raise RuntimeError("Certified abstract inputs lost typed cyclic components")
    matched, right_pending, residual = _select_right_images(rparts, targets)
    obligations: list[dict[str, object]] = []
    for index, component in enumerate(lparts):
        generator = component.generator
        factors = _factors(generator)
        factor_rows: list[dict[str, object]] = []
        for j, factor in enumerate(factors):
            span = _typed_endpoints(factor)
            suspended = IteratedSuspension(expression=factor, exponent=1)
            factor_rows.append({
                "factor_index": j,
                "factor_type": type(factor).__name__,
                "factor_display": str(factor),
                "source_target_dimensions": list(span) if span is not None else None,
                "formal_suspension_display": str(suspended),
                "formal_suspension_span": (
                    list(_typed_endpoints(suspended))
                    if _typed_endpoints(suspended) is not None else None
                ),
                "stable_definition_applies_to_formal_suspension": (
                    is_defined_stable_suspension(factor, suspended)
                ),
            })
        shape = _suspend_verified_shape(generator)
        obligations.append({
            "source_index": index,
            "source_order": list(_component_order(component) or ()),
            "source_generator": str(generator),
            "source_span": list(_typed_endpoints(generator) or ()),
            "named_target_shape_available": shape is not None,
            "named_target_shape": str(shape) if shape is not None else None,
            "required_equality": (
                "Prove that the actual named target generator equals E(source_generator); "
                "source order, target group and generator types must match"
            ),
            "factorization": factor_rows,
            "atomic_images_or_normalization_pending": shape is None,
        })
    matched_residual_orders = sorted(
        _component_order(targets[index]) for index in residual
    )
    left_orders = sorted(_component_order(component) for component in lparts)
    residual_orders_match = matched_residual_orders == left_orders
    row.update({
        "state": (
            "RIGHT_IMAGES_AMBIGUOUS_OR_UNMATCHED" if right_pending else
            "LEFT_GENERATOR_IDENTITIES_PENDING" if obligations else
            "NO_GENERATOR_OBLIGATIONS"
        ),
        "left_component_count": len(lparts),
        "right_component_count": len(rparts),
        "target_component_count": len(targets),
        "right_matched_target_indices": list(matched),
        "right_pending_indices": list(right_pending),
        "residual_target_indices": list(residual),
        "residual_abstract_orders_match_left": residual_orders_match,
        "left_obligations": obligations,
        "all_named_generators_proved": False,
    })
    return row


def inspect_selected(ks: tuple[int, ...]) -> tuple[dict[str, object], ...]:
    """Return focused diagnostic rows; the inspector itself has no k whitelist."""
    if not ks or len(set(ks)) != len(ks):
        raise ValueError("Select distinct k values")
    return tuple(inspect_k(k) for k in ks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "data" / "sphere.csv").is_file():
        raise RuntimeError("Expected repository root")
    selected = inspect_selected((4, 7, 8, 31))
    report = {
        "phase": "173-R4-R15R2",
        "mode": "READ_ONLY_TYPED_GENERATOR_OBLIGATIONS",
        "groups": selected,
        "proof_completed_by_this_audit": False,
        "source_group_results_are_adopted_database_priors": True,
        "missing_atomic_images_are_not_given": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    for item in selected:
        print(
            "PHASE173_R4_R15R2_K=" + str(item["k"])
            + " ABSTRACT=" + str(item["abstract_compatible"])
            + " LEFT=" + str(item.get("left_component_count", 0))
            + " RIGHT_MATCH=" + str(len(item["right_matched_target_indices"]))
            + " RIGHT_PENDING=" + str(len(item["right_pending_indices"]))
            + " RESIDUAL_ORDER=" + str(item.get("residual_abstract_orders_match_left", False))
            + " STATE=" + str(item["state"]), flush=True,
        )
    k31 = selected[-1]
    if (not k31["abstract_compatible"]
            or k31.get("left_component_count") != 4
            or k31.get("right_component_count") != 4):
        print("PHASE173_R4_R15R2_K31_BASELINE=FAIL", flush=True)
        return 2
    print("PHASE173_R4_R15R2_K31_BASELINE=PASS", flush=True)
    print("PHASE173_R4_R15R2_NO_PROOF_PROMOTION=True", flush=True)
    print("PHASE173_R4_R15R2_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R2_AUDIT=PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
