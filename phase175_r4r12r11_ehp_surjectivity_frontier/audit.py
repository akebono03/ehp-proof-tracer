"""Read-only EHP quotient frontier inspection; never installs mathematical facts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

PACKAGE = "phase175_r4r12r11_ehp_surjectivity_frontier"
RULE_NAME = "EHP exact rank-two elementary 2-group quotient by a generated summand"


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R11_GIT_FAILED: " + " ".join(arguments) + ": " + result.stderr)
    return result.stdout.strip()


def describe(item: object) -> str:
    return repr(item)


def valid_zero_goal(statement: object) -> bool:
    """Reject a purported zero diagonal sphere group; no proof claim is created."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    if not isinstance(statement, TodaPrimaryGroupZeroStatement):
        return True
    group = statement.group
    if not isinstance(group, TodaPrimaryGroup):
        return True
    q, n = group.group_dimension, group.sphere_dimension
    return not (type(q) is int and type(n) is int and q == n and n >= 2)


def inspect() -> dict[str, object]:
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import MapSurjective, GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences
    root = exact_prior_database_result(5, 4)
    if root is None or not isinstance(root.rhs, FiniteCyclicGroup) or root.rhs.order != 2:
        raise RuntimeError("R11_ROOT_MISSING")
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    isolated = expand_public_two_summand_quotient(goal, proof_target=root)
    bridge = build_shared_typed_bridge()
    shared = shared_expansion_provider(bridge, proof_target=root)
    selected = tuple(item for item in shared(goal) if item.rule.name == RULE_NAME)
    if len(isolated) != 2 or len(selected) != 2:
        raise RuntimeError("R11_TWO_ORIENTATIONS_REQUIRED")
    paths = []
    for index, candidate in enumerate(selected):
        obligations = candidate.subgoals
        if len(obligations) != 6 or not isinstance(obligations[4], MapSurjective):
            raise RuntimeError("R11_SIX_OBLIGATIONS_MISSING")
        entries = []
        for position in (2, 3, 4, 5):
            statement = obligations[position]
            expansions = tuple(shared(statement))
            entries.append({
                "index": position,
                "statement_type": type(statement).__name__,
                "statement": describe(statement),
                "candidate_count": len(expansions),
                "candidate_rules": [x.rule.name for x in expansions],
                "candidate_subgoals": [
                    {"rule": x.rule.name, "subgoals": [describe(y) for y in x.subgoals]}
                    for x in expansions[:12]
                ],
                "proof_claimed": False,
            })
        surjectivity = obligations[4]
        zero_route = tuple(expand_ehp_exactness_consequences(surjectivity))
        zero_requisites = [y for x in zero_route for y in x.subgoals if isinstance(y, TodaPrimaryGroupZeroStatement)]
        paths.append({
            "orientation": index,
            "delta_image": describe(obligations[2]) if isinstance(obligations[2], GeneratorImage) else None,
            "suspension_image": describe(obligations[5]),
            "ehp_surjectivity_zero_route_count": len(zero_route),
            "zero_route_targets": [describe(x.group) for x in zero_requisites],
            "zero_route_has_false_diagonal_goal": any(not valid_zero_goal(x) for x in zero_requisites),
            "obligation_details": entries,
        })
    return {
        "isolated_count": len(isolated),
        "shared_count": len(selected),
        "paths": paths,
        "source_511_remains_cited": True,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "actual_recursive_search_executed": False,
        "group_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R11_WRONG_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R11_WRONG_BRANCH")
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "phase": "175-R4R12R11", "dry_run": dry_run,
        "gate": "FAIL_R11", "full_pytest_executed": False,
        "head": git(root, "rev-parse", "HEAD"),
        "production_dirty": "phase165_r52_r9_shared_math.py" in git(root, "diff", "--name-only").splitlines(),
    }
    try:
        report["frontier"] = inspect()
        report["gate"] = "PASS_R11_EHP_SURJECTIVITY_FRONTIER_AUDITED_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    filename = output / ("preflight.json" if dry_run else "audit_report.json")
    filename.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R12R11_GATE=" + report["gate"])
    print("PHASE175_R4R12R11_REPORT=" + str(filename))
    for entry in report.get("frontier", {}).get("paths", []):
        print("R11_ORIENTATION=" + str(entry["orientation"]))
        print("R11_FALSE_DIAGONAL_ZERO_PREMISE=" + str(entry["zero_route_has_false_diagonal_goal"]))
        for x in entry["obligation_details"]:
            print("R11_OBLIGATION_" + str(x["index"]) + "_CANDIDATES=" + str(x["candidate_count"]))
            print("R11_OBLIGATION_" + str(x["index"]) + "_RULES=" + repr(x["candidate_rules"]))
    if "error" in report:
        print("PHASE175_R4R12R11_ERROR=" + report["error"])
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args(argv)
    return run(arguments.root.resolve(), dry_run=arguments.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
