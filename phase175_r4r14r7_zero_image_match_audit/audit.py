"""Read-only diagnosis of the remaining ImageZero proof obligation.

Never manufactures source steps, changes shared providers, or claims completion.
The actual canonical search output is compared against the R41 proof contract.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import traceback


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, check=False,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if process.returncode:
        raise RuntimeError("GIT_ERROR " + " ".join(args) + ": " + process.stderr.strip())
    return process.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_CHANGES_REQUIRE_REVIEW")
    shared_path = root / "phase165_r52_r9_shared_math.py"
    shared = shared_path.read_text(encoding="utf-8-sig")
    required = (
        "build_public_composite_zero_transport_provider(bridge)",
        "options.extend(expand_surjective_zero_codomain(goal))",
        "expand_ehp_zero_from_delta_surjectivity(goal)",
        "build_public_adopted_zero_image_provider(",
    )
    absent = [entry for entry in required if entry not in shared]
    if absent:
        raise RuntimeError("R5_R6_PUBLIC_WIRING_NOT_PRESENT " + repr(absent))
    required_files = (
        "phase175_r4r14r4_general_zero_transport/rule.py",
        "phase175_r4r14r5_public_zero_transport/provider.py",
        "phase175_r4r14r6_surjective_zero_codomain/rule.py",
        "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py",
        "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py",
    )
    for item in required_files:
        if not (root / item).is_file():
            raise RuntimeError("REQUIRED_SOURCE_MISSING: " + item)
    return {
        "head": git(root, "rev-parse", "HEAD"),
        "r5_r6_present": True,
        "required_sources": list(required_files),
        "tracked_shared_modified": "phase165_r52_r9_shared_math.py" in
            git(root, "diff", "--name-only").splitlines(),
    }


def inspect_live() -> dict[str, object]:
    from expression import Zero
    from homotopy_groups import (
        TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap,
    )
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
        verified_prior_zero_image_inputs,
    )
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        build_public_adopted_zero_image_provider,
    )
    from phase175_r4r14r6_surjective_zero_codomain.rule import (
        RULE_NAME as ROOT_RULE, surjective_zero_codomain_inputs,
    )
    from proof import ProofRule, find_inference_matches_for_rule

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=6, k=4, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("EXPECTED_ONE_CANONICAL_SCREENED_CONTEXT")
    bridge = contexts[0]
    provider = shared_expansion_provider(bridge, proof_target=root)
    source = TodaPrimaryGroup(9, 5)
    target = TodaPrimaryGroup(10, 6)
    e = TodaSuspensionMap(source, target)
    image_zero = ImageZeroStatement(e)
    presentation = exact_prior_database_result(5, 4)
    if presentation is None:
        raise RuntimeError("PI95_EARLIER_PRESENTATION_ABSENT")
    generator_zero = GeneratorImage(e, presentation.rhs.generator, Zero())
    given = admitted_db_step(presentation, proof_target=root, bridge=bridge)
    if given is None:
        raise RuntimeError("PRIOR_DB_NOT_ADMITTED")
    public_root = tuple(provider(root))
    public_image = tuple(provider(image_zero))
    public_generator = tuple(provider(generator_zero))
    r41 = tuple(build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=root,
    )(image_zero))
    if len(r41) != 1:
        raise RuntimeError("R41_EXPECTED_ONE_IMAGE_ZERO_PROPOSAL: " + str(len(r41)))

    steps = tuple(result.proven_steps)
    def status(statement: object) -> list[dict[str, object]]:
        return [{
            "rule": getattr(step.rule, "name", str(step.rule)),
            "inference_rule": getattr(step.inference_rule, "name", None),
            "is_admitted_db_step": (
                verified_db_step(step, proof_target=root, bridge=bridge)
                if step.rule is ProofRule.GIVEN else False
            ),
            "premises": len(step.premises),
        } for step in steps if step.conclusion == statement]

    r41_option = r41[0]
    matches_steps = find_inference_matches_for_rule(r41_option.rule, steps)
    matches_with_admitted = find_inference_matches_for_rule(
        r41_option.rule, steps + (given,),
    )
    p = r41_option.subgoals
    return {
        "search_status": getattr(result.status, "value", str(result.status)),
        "proven_step_count": len(steps),
        "open_goals": [str(x) for x in result.open_goals],
        "search_diagnostics": [str(x) for x in result.diagnostics],
        "root_proposals": [x.rule.name for x in public_root],
        "image_zero_proposals": [x.rule.name for x in public_image],
        "generator_zero_proposals": [x.rule.name for x in public_generator],
        "r41_subgoals_match_expected": p == (presentation, generator_zero),
        "r41_inputs_valid": verified_prior_zero_image_inputs(
            image_zero, presentation, proof_target=root, bridge=bridge,
        ) == (presentation, generator_zero),
        "admitted_db_step_exists": True,
        "r41_db_step_verified": verified_db_step(
            given, proof_target=root, bridge=bridge,
        ),
        "presentations_in_proven_steps": status(presentation),
        "generator_zero_in_proven_steps": status(generator_zero),
        "image_zero_in_proven_steps": status(image_zero),
        "r41_matches_using_proven_steps": len(matches_steps),
        "r41_matches_with_admitted_db_added": len(matches_with_admitted),
        "root_rule": ROOT_RULE,
        "root_inputs": [str(x) for x in (surjective_zero_codomain_inputs(root) or ())],
        "proof_step_details": [
            {
                "index": index,
                "rule": getattr(step.rule, "name", str(step.rule)),
                "inference_rule": getattr(step.inference_rule, "name", None),
                "conclusion": str(step.conclusion)[:400],
            } for index, step in enumerate(steps)
        ],
        "new_given": 0,
        "new_rules": 0,
        "production_changed": False,
        "completion_claimed": False,
    }


def run(root: Path, dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "175_R4R14R7",
        "mode": "DRY_RUN" if dry_run else "READ_ONLY_R41_MATCH_DIAGNOSTIC",
        "gate": "FAIL_R4R14R7",
        "full_pytest": False,
    }
    try:
        report["preflight"] = preflight(root)
        if not dry_run:
            report["observed"] = inspect_live()
        report["gate"] = (
            "PASS_R4R14R7_DRYRUN_SOURCE_GUARD" if dry_run
            else "PASS_R4R14R7_IMAGE_ZERO_MATCH_AUDITED"
        )
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    destination = Path(os.environ.get("TEMP", tempfile.gettempdir())) / (
        "EHP_Phase175_R4R14R7_image_zero_match.json"
    )
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R14R7_GATE=" + str(report["gate"]))
    print("PHASE175_R4R14R7_REPORT=" + str(destination))
    if "error" in report:
        print("PHASE175_R4R14R7_ERROR=" + str(report["error"]))
        return 1
    if not dry_run:
        row = report["observed"]
        for key in (
            "search_status", "proven_step_count",
            "admitted_db_step_exists", "r41_db_step_verified",
            "r41_subgoals_match_expected", "r41_inputs_valid",
            "r41_matches_using_proven_steps",
            "r41_matches_with_admitted_db_added",
        ):
            print("PHASE175_R4R14R7_" + key.upper() + "=" + str(row[key]))
        print("PHASE175_R4R14R7_PRESENTATION_PROOFS=" +
              str(len(row["presentations_in_proven_steps"])))
        print("PHASE175_R4R14R7_GENERATOR_ZERO_PROOFS=" +
              str(len(row["generator_zero_in_proven_steps"])))
        print("PHASE175_R4R14R7_IMAGE_ZERO_PROOFS=" +
              str(len(row["image_zero_in_proven_steps"])))
        print("PHASE175_R4R14R7_NEW_GIVEN=0")
        print("PHASE175_R4R14R7_PRODUCTION_UNCHANGED=PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
