"""Read-only Phase 175 R4R12R12 audit of the EHP Hopf and suspension-image frontier.

This module neither asserts an odd-dimensional Hopf theorem nor adds any
proof leaf. The external theorem requires separately reviewed source wiring.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

PACKAGE = "phase175_r4r12r12_odd_hopf_and_e_image_frontier"
QUOTIENT_RULE = "EHP exact rank-two elementary 2-group quotient by a generated summand"


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("R12_GIT_FAILED: " + " ".join(args) + ": " + process.stderr.strip())
    return process.stdout.strip()


def inspect() -> dict[str, object]:
    """Inspect the live shared provider without running a recursive proof or mutating state."""
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences

    root = exact_prior_database_result(5, 4)
    if root is None or not isinstance(root.rhs, FiniteCyclicGroup):
        raise RuntimeError("R12_ROOT_MISSING")
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    bridge = build_shared_typed_bridge()
    shared = shared_expansion_provider(bridge, proof_target=root)
    isolated = expand_public_two_summand_quotient(goal, proof_target=root)
    selected = tuple(x for x in shared(goal) if x.rule.name == QUOTIENT_RULE)
    if len(isolated) != 2 or len(selected) != 2:
        raise RuntimeError("R12_TWO_ORIENTATIONS_REQUIRED")

    entries = []
    for orientation, path in enumerate(selected):
        if len(path.subgoals) != 6:
            raise RuntimeError("R12_SIX_OBLIGATIONS_REQUIRED")
        delta_image, surjective, e_image = (path.subgoals[i] for i in (2, 4, 5))
        decomposition = component_image_obligations(e_image)
        factors = []
        if decomposition is not None:
            for factor in decomposition:
                options = tuple(shared(factor))
                factors.append({
                    "goal": repr(factor),
                    "candidate_count": len(options),
                    "candidate_rules": [x.rule.name for x in options],
                    "candidate_subgoals": [list(map(repr, x.subgoals)) for x in options[:6]],
                    "proved": False,
                })
        e_options = tuple(shared(e_image))
        s_options = tuple(shared(surjective))
        zero_dependencies = [
            x for option in expand_ehp_exactness_consequences(surjective)
            for x in option.subgoals if isinstance(x, TodaPrimaryGroupZeroStatement)
        ]
        false_zero = any(
            isinstance(x.group, TodaPrimaryGroup)
            and x.group.group_dimension == x.group.sphere_dimension
            for x in zero_dependencies
        )
        entries.append({
            "orientation": orientation,
            "delta_image": repr(delta_image),
            "suspension_image": repr(e_image),
            "suspension_image_candidate_count": len(e_options),
            "suspension_image_rule_names": [x.rule.name for x in e_options],
            "component_count": len(factors),
            "component_candidates": factors,
            "surjectivity_candidate_count": len(s_options),
            "surjectivity_rule_names": [x.rule.name for x in s_options],
            "zero_route_requires_false_diagonal_zero": false_zero,
            "zero_route_requisites": list(map(repr, zero_dependencies)),
            "group_complete": False,
        })
    return {
        "paths": entries,
        "odd_sphere_target_dimension": 5,
        "hopf_target_group": repr(TodaPrimaryGroup(9, 9)),
        "external_odd_hopf_theorem_not_registered": True,
        "external_math_reference": "Ordinary integral Hopf invariant vanishes for odd-dimensional sphere targets; verify applicability to the EHP H map before implementation",
        "source_claim_added": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "recursive_search_performed": False,
        "full_pytest_executed": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R12_WRONG_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R12_WRONG_BRANCH")
    target = root / PACKAGE / "output"
    target.mkdir(exist_ok=True, parents=True)
    report = {"phase": "175-R4R12R12", "dry_run": dry_run,
              "head": git(root, "rev-parse", "HEAD"),
              "gate": "FAIL_R12", "full_pytest_executed": False}
    try:
        report["frontier"] = inspect()
        report["gate"] = "PASS_R12_ODD_HOPF_AND_E_IMAGE_FRONTIER_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    path = target / ("preflight.json" if dry_run else "audit_report.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R12R12_GATE=" + report["gate"])
    print("PHASE175_R4R12R12_REPORT=" + str(path))
    for entry in report.get("frontier", {}).get("paths", []):
        print("R12_ORIENTATION=" + str(entry["orientation"]))
        print("R12_FALSE_DIAGONAL_ZERO_ROUTE=" + str(entry["zero_route_requires_false_diagonal_zero"]))
        print("R12_E_IMAGE_CANDIDATES=" + str(entry["suspension_image_candidate_count"]))
        print("R12_COMPONENT_COUNT=" + str(entry["component_count"]))
        for index, factor in enumerate(entry["component_candidates"]):
            print("R12_FACTOR_" + str(index) + "_CANDIDATES=" + str(factor["candidate_count"]))
            print("R12_FACTOR_" + str(index) + "_RULES=" + repr(factor["candidate_rules"]))
    if "error" in report:
        print("PHASE175_R4R12R12_ERROR=" + report["error"])
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
