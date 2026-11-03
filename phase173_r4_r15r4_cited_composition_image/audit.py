"""Audit source-cited named images without modifying the public proof tree."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from expression import Composition, IteratedSuspension
from phase169_r10b_registered_stable_family_binding.family_registry import (
    registered_stable_family_pair,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r4_typed_generator_audit.audit import _group_components
from phase173_r4_r15r2_generator_obligation_audit.audit import inspect_k as previous_inspect_k
from phase173_r4_r15r4_cited_composition_image.replay import (
    cited_source_steps,
    proof_tree_steps,
    replay_named_image,
)
from proof import ProofRule


def expression_atoms(expression: object) -> tuple[object, ...]:
    """Flatten a structurally typed composition; never conflate generator IDs."""
    if isinstance(expression, Composition):
        return expression_atoms(expression.left) + expression_atoms(expression.right)
    return (expression,)


def atom_evidence(
    source: object, target: object, cited_family_ids: frozenset[int],
) -> dict[str, object]:
    """Distinguish cited family identities, formal suspension and missing source."""
    from phase173_r4_r15r4_cited_composition_image.bridge import generator_image

    goal = generator_image(source, target)
    row: dict[str, object] = {
        "source": str(source),
        "target": str(target),
        "well_typed": goal is not None,
        "status": "UNSUPPORTED_ATOMIC_IMAGE",
        "family_id": None,
    }
    if goal is None:
        row["status"] = "INCORRECT_ATOMIC_IMAGE_TYPING"
        return row
    if isinstance(target, IteratedSuspension) and target.exponent == 1 and target.expression == source:
        row["status"] = "CANONICAL_FORMAL_IMAGE"
        return row
    family = registered_stable_family_pair(source, target)
    if family is None:
        return row
    row["family_id"] = family.family_id
    row["status"] = (
        "CITED_FAMILY_IMAGE_PROPOSAL"
        if family.family_id in cited_family_ids
        else "FAMILY_ID_KNOWN_BUT_SOURCE_NOT_CITED"
    )
    return row


def inspect_k(k: int) -> dict[str, object]:
    """Replay every plausible named image from all existing earlier DB factors."""
    base = previous_inspect_k(k)
    target = exact_prior_database_result(4, k)
    left = exact_prior_database_result(3, k)
    if not base.get("abstract_compatible") or target is None or left is None:
        return {
            "k": k, "status": "ABSTRACT_PREMISES_UNAVAILABLE", "candidate_pairs": [],
            "proved_named_images": 0, "public_completion": False,
        }
    source_steps = cited_source_steps()
    cited_ids = frozenset(
        step.conclusion.family_id
        for step in source_steps
        if isinstance(step.conclusion, CitedStableFamilyDefinition)
    )
    sources = _group_components(left)
    targets = _group_components(target)
    if sources is None or targets is None:
        raise RuntimeError("Reviewed abstract premises are not typed cyclic groups")
    candidates: list[dict[str, object]] = []
    certified_pairs: list[tuple[int, int]] = []
    for i, source in enumerate(sources):
        for j in base["residual_target_indices"]:
            proposed = targets[j]
            if type(source) is not type(proposed):
                continue
            if getattr(source, "order", None) != getattr(proposed, "order", None):
                continue
            from_atoms = expression_atoms(source.generator)
            to_atoms = expression_atoms(proposed.generator)
            if len(from_atoms) != len(to_atoms):
                continue
            factors = tuple(
                atom_evidence(x, y, cited_ids)
                for x, y in zip(from_atoms, to_atoms)
            )
            if not all(factor["well_typed"] for factor in factors):
                continue
            # Actual derivation may exist only if every factor has cited or
            # canonical-formal evidence; no shape match can grant a proof.
            step = replay_named_image(source.generator, proposed.generator, source_steps)
            if step is not None:
                certified_pairs.append((i, j))
            steps = proof_tree_steps(step) if step is not None else ()
            candidates.append({
                "source_index": i,
                "target_index": j,
                "source_generator": str(source.generator),
                "target_generator": str(proposed.generator),
                "factors": factors,
                "proof_engine_replayed": step is not None,
                "proof_step_count": len(steps),
                "cited_references": sorted({
                    proof.inference_rule.literature_reference.locator
                    for proof in steps
                    if proof.rule is ProofRule.GIVEN
                    and proof.inference_rule is not None
                    and proof.inference_rule.literature_reference is not None
                }),
                "missing_family_ids": sorted({
                    factor["family_id"] for factor in factors
                    if factor["status"] == "FAMILY_ID_KNOWN_BUT_SOURCE_NOT_CITED"
                    and type(factor["family_id"]) is int
                }),
            })
    return {
        "k": k,
        "status": "SOURCE_BACKED_IMAGE_AUDIT",
        "cited_stable_family_ids": sorted(cited_ids),
        "right_named_image_shape_matches": len(base["right_matched_target_indices"]),
        "left_source_count": len(sources),
        "residual_target_count": len(base["residual_target_indices"]),
        "candidate_pairs": candidates,
        "proved_named_images": len(certified_pairs),
        "certified_pairs": [list(value) for value in certified_pairs],
        "new_source_given": False,
        "public_completion": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "data" / "sphere.csv").is_file():
        raise RuntimeError("Expected EHP Proof Tracer repository root")
    observations = tuple(inspect_k(k) for k in (4, 7, 8, 31))
    report = {
        "phase": "173-R4-R15R4",
        "mode": "READ_ONLY_SOURCE_CITED_COMPOSITE_GENERATOR_IMAGE",
        "observations": observations,
        "proof_promoted_to_public": False,
        "full_pytest_performed": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in observations:
        print(
            "PHASE173_R4_R15R4_K=" + str(row["k"])
            + " LEFT=" + str(row.get("left_source_count", 0))
            + " NAMED_REPLAYED=" + str(row["proved_named_images"])
            + " CANDIDATES=" + str(len(row["candidate_pairs"])),
            flush=True,
        )
    last = observations[-1]
    blockers = sorted({
        fid for candidate in last["candidate_pairs"]
        for fid in candidate["missing_family_ids"]
    })
    print("PHASE173_R4_R15R4_K31_MISSING_FAMILY_SOURCE_IDS=" + ",".join(map(str, blockers)), flush=True)
    print("PHASE173_R4_R15R4_K31_NAMED_REPLAYED=" + str(last["proved_named_images"]), flush=True)
    passed = bool(
        last["left_source_count"] == 4
        and last["right_named_image_shape_matches"] == 4
        and last["residual_target_count"] == 4
        and last["public_completion"] is False
        and last["new_source_given"] is False
    )
    print("PHASE173_R4_R15R4_PRODUCTION_EDIT=NONE", flush=True)
    print("PHASE173_R4_R15R4_PUBLIC_COMPLETION=False", flush=True)
    print("PHASE173_R4_R15R4_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R4_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
