"""R15R5: correlate actual k=31 proof blockers with source-definition text hits.

This is an observational source-audit, not a public search rule or new GIVEN.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase173_r4_r15r4_cited_composition_image.audit import inspect_k
from phase173_r4_r15r4_cited_composition_image.replay import cited_source_steps
from phase173_r4_r15r5_family_source_frontier.source_scan import (
    FAMILY_LABELS,
    scan_adopted_toda_sources,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
)


def inspect_family_source_frontier(root: Path, k: int = 31) -> dict[str, object]:
    """Report exact unresolved pairs and source candidates without proof promotion."""
    if type(k) is not int or k < 3:
        raise ValueError("Expected k>=3")
    image_audit = inspect_k(k)
    if image_audit.get("status") != "SOURCE_BACKED_IMAGE_AUDIT":
        raise RuntimeError("No live source-backed image audit available")
    source_ids = frozenset(
        step.conclusion.family_id for step in cited_source_steps()
        if isinstance(step.conclusion, CitedStableFamilyDefinition)
    )
    registered = {family.family_id: family for family in read_registered_stable_families()}
    blocker_ids = sorted({
        number for candidate in image_audit["candidate_pairs"]
        if not candidate["proof_engine_replayed"]
        for number in candidate["missing_family_ids"]
    })
    unresolved = [
        {
            "source_index": entry["source_index"],
            "target_index": entry["target_index"],
            "source_generator": entry["source_generator"],
            "target_generator": entry["target_generator"],
            "factor_obligations": entry["factors"],
            "missing_family_ids": entry["missing_family_ids"],
            "proof_engine_replayed": False,
        }
        for entry in image_audit["candidate_pairs"]
        if not entry["proof_engine_replayed"]
    ]
    family_sources: list[dict[str, object]] = []
    for family_id in blocker_ids:
        family = registered.get(family_id)
        if family is None or family_id not in FAMILY_LABELS:
            raise RuntimeError("Unreviewed missing stable-family ID")
        if family_id in source_ids:
            raise RuntimeError("Source definition already cited: re-audit this blocker")
        scan = scan_adopted_toda_sources(root, family_id=family_id)
        family_sources.append({
            **scan,
            "stem": family.stem,
            "minimum_n": family.minimum_n,
            "registered_family_name": family.display,
            "cited_family_definition_available": False,
        })
    return {
        "phase": "173-R4-R15R5",
        "mode": "READ_ONLY_UNRESOLVED_GENERATOR_SOURCE_FRONTIER",
        "n": 4,
        "k": k,
        "target": f"pi_{k + 4}^4",
        "named_image_candidates": len(image_audit["candidate_pairs"]),
        "named_images_replayed": image_audit["proved_named_images"],
        "unresolved_pairs": unresolved,
        "unresolved_family_ids": blocker_ids,
        "family_sources": family_sources,
        "new_proof_steps_created": False,
        "new_given_created": False,
        "public_completion": False,
        "full_pytest_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect_family_source_frontier(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE173_R4_R15R5_K31_NAMED_REPLAYED=" + str(result["named_images_replayed"]), flush=True)
    print("PHASE173_R4_R15R5_K31_UNRESOLVED_PAIRS=" + str(len(result["unresolved_pairs"])), flush=True)
    print("PHASE173_R4_R15R5_FAMILY_IDS=" + ",".join(map(str, result["unresolved_family_ids"])), flush=True)
    for family in result["family_sources"]:
        print(
            "PHASE173_R4_R15R5_FAMILY_" + str(family["family_id"])
            + "_TEXT_HITS=" + str(len(family["candidate_text_hits"]))
            + " CITED=False",
            flush=True,
        )
    print("PHASE173_R4_R15R5_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R5_PUBLIC_COMPLETION=False", flush=True)
    passed = (
        result["named_image_candidates"] == 4
        and result["named_images_replayed"] == 1
        and len(result["unresolved_pairs"]) == 3
        and result["unresolved_family_ids"] == [56, 88]
        and all(not f["source_definition_certified"] for f in result["family_sources"])
        and result["new_given_created"] is False
    )
    print("PHASE173_R4_R15R5_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
