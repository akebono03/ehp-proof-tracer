"""Read-only audit of the existing two-factor Toda (5.9) to EHP zero chain.

Does not register mathematical rules, GIVENs, proof steps or renderer content.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

SOURCE_BLOBS = {
    "phase165_r52_r9_shared_math.py": "f5329594a8298af34cd05932bf4a7b6c59d6e4de",
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py": "6aa48096b41714fbdf588c3ba423d264a4a13bb9",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py": "9cf9dfa4b77a22bcbbe60b0c0b85dbf25cad50b2",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r12_toda59_annihilator_source/source.py": "10b03ec879cb6f5ad1ae01f3e8ffa1dd0af6c01f",
}
TARGET = (6, 4)
PRIOR = (5, 4)


def git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", check=False)
    if done.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + ": " + done.stderr.strip())
    return done.stdout.strip()


def source_guard(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("EXPECTED_DEVELOP")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_CHANGES_NEED_REVIEW")
    for path, expected in SOURCE_BLOBS.items():
        if not (root / path).is_file():
            raise RuntimeError("MISSING_FILE: " + path)
        for actual in (git(root, "rev-parse", "HEAD:" + path),
                       git(root, "hash-object", path)):
            if actual != expected:
                raise RuntimeError("SOURCE_BLOB_CHANGED: " + path + " actual=" + actual)
    return {"head": git(root, "rev-parse", "HEAD"),
            "source_blobs": SOURCE_BLOBS, "staged_changes": 0}


def inspect_live() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import canonical_annihilator_instance
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        left_associated, lifted_stable_composition, expand_source_bound_zero_image_chain,
    )
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        build_public_adopted_zero_image_provider,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
    from proof import ProofRule
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus

    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=target)
    laws = tuple(link.step.conclusion for link in bridge.proof_links
                 if link.step is not None and link.step.rule is ProofRule.GIVEN
                 and type(link.step.conclusion) is CitedFamilyAnnihilator)
    if len(laws) != 1:
        raise RuntimeError("TODA59_SOURCE_COUNT: " + str(len(laws)))
    law = laws[0]
    instance = canonical_annihilator_instance(law, 6)
    if instance is None:
        raise RuntimeError("N6_INSTANCE_NOT_FOUND")
    presentation = exact_prior_database_result(*PRIOR)
    if presentation is None or not hasattr(presentation.rhs, "generator"):
        raise RuntimeError("PRIOR_PRESENTATION_MISSING")
    generator = presentation.rhs.generator
    mapping = TodaSuspensionMap(TodaPrimaryGroup(9, 5), TodaPrimaryGroup(10, 6))
    image_zero_goal = ImageZeroStatement(mapping)
    generator_zero_goal = GeneratorImage(mapping, generator, Zero())
    lifted = lifted_stable_composition(generator)
    associated = left_associated(lifted) if type(lifted) is Composition else None
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    factors = typed_composition_factors(lifted) if type(lifted) is Composition else None
    provided = shared_expansion_provider(bridge, proof_target=target)
    root_options = tuple(provided(target))
    image_options = tuple(provided(image_zero_goal))
    generator_options = tuple(provided(generator_zero_goal))
    r38_image = expand_source_bound_zero_image_chain(image_zero_goal, (law,))
    r38_generator = expand_source_bound_zero_image_chain(generator_zero_goal, (law,))
    r41 = build_public_adopted_zero_image_provider(bridge=bridge, proof_target=target)
    r41_image = tuple(r41(image_zero_goal))
    root_ehp = ehp_zero_inputs(target)
    if root_ehp is None:
        raise RuntimeError("TYPED_EHP_WINDOW_MISSING")
    contexts = []
    search = search_group_from_registered_goal(n=6, k=4, context_sink=contexts.append)
    if search.status is ProofSearchStatus.COMPLETE:
        state = "COMPLETE_ALREADY"
    else:
        state = "PARTIAL_CONFIRMED"
    return {
        "target": "pi_10^6", "prior": "pi_9^5",
        "toda59_cited_general_given_count": len(laws),
        "toda59_n6_relation_type": type(instance).__name__,
        "prior_presentation_type": type(presentation.rhs).__name__,
        "generator_type": type(generator).__name__,
        "lifted_type": type(lifted).__name__ if lifted is not None else None,
        "lifted_factor_count": len(factors) if factors is not None else None,
        "left_associated_available": associated is not None,
        "r38_image_zero_proposals": [x.rule.name for x in r38_image],
        "r38_generator_zero_proposals": [x.rule.name for x in r38_generator],
        "r41_image_zero_proposals": [x.rule.name for x in r41_image],
        "shared_image_zero_proposals": [x.rule.name for x in image_options],
        "shared_generator_zero_proposals": [x.rule.name for x in generator_options],
        "root_proposal_names": [x.rule.name for x in root_options],
        "root_ehp_premises": [type(x).__name__ for x in root_ehp],
        "root_ehp_delta_goal": str(root_ehp[0]),
        "actual_search_state": state,
        "actual_open_goals": [str(x) for x in search.open_goals],
        "new_given": 0, "new_rules": 0,
    }


def run(root: Path, dry_run: bool = False) -> int:
    report = {"phase": "175_R4R14R2", "mode": "READ_ONLY_FRONTIER",
              "gate": "FAIL_R4R14R2", "full_pytest": False,
              "new_given": 0, "new_rules": 0}
    try:
        report["source_guard"] = source_guard(root)
        if dry_run:
            report["gate"] = "PASS_R4R14R2_DRYRUN_SOURCE_GUARD"
        else:
            report["observed"] = inspect_live()
            report["gate"] = "PASS_R4R14R2_TWO_FACTOR_FRONTIER_AUDITED"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
    path = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "EHP_Phase175_R4R14R2_frontier.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R4R14R2_GATE=" + report["gate"])
    print("PHASE175_R4R14R2_REPORT=" + str(path))
    if "error" in report:
        print("PHASE175_R4R14R2_ERROR=" + report["error"])
        return 1
    if not dry_run:
        row = report["observed"]
        for key in ("lifted_factor_count", "left_associated_available", "r38_generator_zero_proposals", "r41_image_zero_proposals", "shared_generator_zero_proposals", "actual_search_state"):
            print("PHASE175_R4R14R2_" + key.upper() + "=" + str(row[key]))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
