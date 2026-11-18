"""Read-only diagnostic of the exact typed Orientation 1 mismatch."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import traceback

PACKAGE = "phase175_r4r12r10r1r3_orientation_type_diagnostic"


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True,
                            capture_output=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise RuntimeError("R10R1R3_GIT_FAILED: " + result.stderr.strip())
    return result.stdout.strip()


def describe_tree(value: object, path: str = "root", depth: int = 0) -> dict[str, object]:
    """Record dataclass fields recursively, without altering any expression."""
    from dataclasses import fields, is_dataclass
    result: dict[str, object] = {
        "path": path,
        "type": type(value).__module__ + "." + type(value).__qualname__,
        "repr": repr(value)[:2500],
    }
    if depth < 8 and is_dataclass(value) and not isinstance(value, type):
        result["children"] = [
            describe_tree(getattr(value, field.name), path + "." + field.name, depth + 1)
            for field in fields(value)
        ]
    elif depth < 8 and isinstance(value, (tuple, list)):
        result["children"] = [
            describe_tree(item, path + "[" + str(index) + "]", depth + 1)
            for index, item in enumerate(value)
        ]
    return result


def differences(left: object, right: object, path: str = "root", depth: int = 0) -> list[dict[str, str]]:
    """Enumerate structural mismatch paths without semantic normalization."""
    from dataclasses import fields, is_dataclass
    if left == right:
        return []
    if depth >= 12 or type(left) is not type(right):
        return [{"path": path, "left_type": type(left).__name__,
                 "right_type": type(right).__name__, "left": repr(left)[:500],
                 "right": repr(right)[:500]}]
    if is_dataclass(left) and not isinstance(left, type):
        output: list[dict[str, str]] = []
        for field in fields(left):
            output.extend(differences(getattr(left, field.name), getattr(right, field.name),
                                      path + "." + field.name, depth + 1))
        return output
    if isinstance(left, (tuple, list)) and len(left) == len(right):
        output = []
        for index, (a, b) in enumerate(zip(left, right)):
            output.extend(differences(a, b, path + "[" + str(index) + "]", depth + 1))
        return output
    return [{"path": path, "left_type": type(left).__name__,
             "right_type": type(right).__name__, "left": repr(left)[:500],
             "right": repr(right)[:500]}]


def inspect(root: Path) -> dict[str, object]:
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
    from phase175_r4r12r10r1_cited_511_public.source import canonical_511, verify_cited_511
    from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
    from phase165_r14_r6_generic_iso import GeneratorImage

    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R10R1R3_WRONG_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R10R1R3_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")
    prior = "bf0d7be3081c61f2feec075a3c82c2004c29bbf2"
    check = subprocess.run(["git", "merge-base", "--is-ancestor", prior, head],
                           cwd=root, capture_output=True)
    if check.returncode:
        raise RuntimeError("R10R1R3_R9_COMMIT_NOT_ANCESTOR")
    source_position = verify_cited_511(root)
    target = exact_prior_database_result(5, 4)
    if target is None:
        raise RuntimeError("R10R1R3_MISSING_TARGET_DB_ROW")
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, 2)
    routes = expand_public_two_summand_quotient(cyclic, proof_target=target)
    if len(routes) != 2:
        raise RuntimeError("R10R1R3_TWO_ROUTES_CHANGED")
    expected = canonical_511()
    reports = []
    for index, route in enumerate(routes):
        candidate = route.subgoals[2]
        if not isinstance(candidate, GeneratorImage):
            raise RuntimeError("R10R1R3_DELTA_IMAGE_TYPE_CHANGED")
        actual = delta_image_equality(candidate)
        if actual is None:
            raise RuntimeError("R10R1R3_R9_DELTA_BRIDGE_REJECTED_GOAL")
        reports.append({
            "orientation": index,
            "equation_equals_citation": actual == expected,
            "lhs_equals_citation": actual.lhs == expected.lhs,
            "rhs_equals_citation": actual.rhs == expected.rhs,
            "lhs_differences": differences(expected.lhs, actual.lhs, "lhs"),
            "rhs_differences": differences(expected.rhs, actual.rhs, "rhs"),
            "delta_goal": describe_tree(candidate),
            "actual_equation": describe_tree(actual),
            "source_equation": describe_tree(expected),
            "source_endpoints": typed_endpoints(candidate.source_generator),
            "target_endpoints": typed_endpoints(candidate.target_generator),
            "subgoal_types": [type(x).__name__ for x in route.subgoals],
        })
    return {"phase": PACKAGE, "head": head, "source_position": source_position,
            "routes": reports, "new_given": 0, "new_mathematical_rules": 0,
            "production_files_modified": 0, "recursive_search_run": False,
            "full_pytest_executed": False, "group_complete": False,
            "gate": "PASS_R4R12R10R1R3_TYPED_MISMATCH_DIAGNOSED_NOT_COMPLETE"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    report_file = output / ("preflight.json" if args.dry_run else "audit_report.json")
    try:
        report = inspect(root)
        report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE175_R4R12R10R1R3_GATE=" + report["gate"])
        for route in report["routes"]:
            print("ORIENTATION=" + str(route["orientation"]))
            print("EQUATION_MATCH=" + str(route["equation_equals_citation"]))
            print("LHS_MATCH=" + str(route["lhs_equals_citation"]))
            print("RHS_MATCH=" + str(route["rhs_equals_citation"]))
            print("LHS_DIFFERENCES=" + json.dumps(route["lhs_differences"], ensure_ascii=False))
            print("RHS_DIFFERENCES=" + json.dumps(route["rhs_differences"], ensure_ascii=False))
        print("PHASE175_R4R12R10R1R3_REPORT=" + str(report_file))
        return 0
    except Exception as exc:
        report_file.write_text(json.dumps({"gate": "FAIL_R4R12R10R1R3",
            "error": str(exc), "traceback": traceback.format_exc()},
            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE175_R4R12R10R1R3_GATE=FAIL_R4R12R10R1R3")
        print("PHASE175_R4R12R10R1R3_ERROR=" + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
