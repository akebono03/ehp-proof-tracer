"""Explain the failing database generator's exact typed endpoints without repairs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

PACKAGE = "phase175_r4r12r4_generator_endpoint_audit"
EXPECTED_HEAD = "6cdf40e089cb2950d2ae9a6aadb2a36188ca0e7d"


def classify_endpoint(actual: object, expected: tuple[int, int]) -> str:
    """Classify a mismatch; never treat an invalid generator as verified."""
    if actual == expected:
        return "MATCH"
    if actual is None:
        return "UNDEFINED_OR_NONCOMPOSABLE"
    if not isinstance(actual, tuple) or len(actual) != 2:
        return "UNEXPECTED_ENDPOINT_TYPE"
    return "DIFFERENT_TYPED_ENDPOINTS"


def generator_tree(element: object) -> dict[str, object]:
    """Read exact objects recursively; limit depth through recognized types."""
    from expression import Composition, HomotopyElement
    from phase169_r10e5_composite_generator_image.rule import _endpoints

    node: dict[str, object] = {
        "type": type(element).__name__,
        "repr": repr(element),
        "endpoints": repr(_endpoints(element)),
    }
    if isinstance(element, HomotopyElement):
        node.update({
            "name": repr(element.name),
            "dimension": element.dimension,
            "source": element.source,
            "target": element.target,
            "generator_symbol": repr(element.generator),
        })
    elif isinstance(element, Composition):
        node["left"] = generator_tree(element.left)
        node["right"] = generator_tree(element.right)
        left_endpoint = _endpoints(element.left)
        right_endpoint = _endpoints(element.right)
        node["composable"] = (
            left_endpoint is not None and right_endpoint is not None
            and left_endpoint[0] == right_endpoint[1]
        )
    return node


def inspect() -> dict[str, object]:
    from homotopy_groups import DirectSumGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import _endpoints
    from phase175_r4r12_public_two_summand_quotient.provider import (
        ordered_summand_inputs, expand_public_two_summand_quotient,
    )
    from proof import Relation

    root = exact_prior_database_result(5, 4)
    if not isinstance(root, Relation):
        raise RuntimeError("R4R12R4_ROOT_RELATION_MISSING")
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    sources = ordered_summand_inputs(goal, proof_target=root)
    if sources is None:
        raise RuntimeError("R4R12R4_PRIOR_DB_INPUTS_MISSING")
    middle, source = sources
    if not isinstance(middle.rhs, DirectSumGroup):
        raise RuntimeError("R4R12R4_MIDDLE_NOT_DIRECT_SUM")
    expected = (middle.lhs.group_dimension, middle.lhs.sphere_dimension)
    factors = []
    for i, summand in enumerate(middle.rhs.summands):
        generator = summand.generator
        endpoints = _endpoints(generator)
        factors.append({
            "index": i,
            "order": summand.order,
            "expected_endpoints": repr(expected),
            "actual_endpoints": repr(endpoints),
            "classification": classify_endpoint(endpoints, expected),
            "generator_tree": generator_tree(generator),
        })
    proposals = expand_public_two_summand_quotient(goal, proof_target=root)
    return {
        "group": repr(middle.lhs),
        "source": repr(source),
        "target": repr(goal),
        "summands": factors,
        "candidate_count": len(proposals),
        "root_complete": False,
        "source_modified": False,
        "given_added": 0,
        "mathematical_rules_added": 0,
    }


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True,
                            encoding="utf-8", errors="replace", capture_output=True,
                            check=False)
    if result.returncode:
        raise RuntimeError("R4R12R4_GIT_FAILED: " + " ".join(args))
    return result.stdout.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if Path(_git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R4R12R4_NOT_REPOSITORY_ROOT")
    if _git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R4R12R4_WRONG_BRANCH")
    head = _git(root, "rev-parse", "HEAD")
    if head != EXPECTED_HEAD:
        raise RuntimeError("R4R12R4_UNREVIEWED_HEAD: " + head)
    output = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) /
              "EHPProofTracerAudit" / PACKAGE /
              datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ"))
    output.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {"phase": "175-R4R12R4", "head": head,
                                 "dry_run": args.dry_run,
                                 "gate": "DIAGNOSTIC_ONLY_NOT_COMPLETE"}
    try:
        report["result"] = inspect()
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    report_file = output / "report.json"
    report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for factor in report.get("result", {}).get("summands", []):
        print("R4R12R4_SUMMAND_" + str(factor["index"]) + "_CLASS=" + factor["classification"])
        print("R4R12R4_SUMMAND_" + str(factor["index"]) + "_ACTUAL=" + factor["actual_endpoints"])
        print("R4R12R4_SUMMAND_" + str(factor["index"]) + "_TREE=" + json.dumps(factor["generator_tree"], ensure_ascii=False))
    print("R4R12R4_REPORT=" + str(report_file))
    if "error" in report:
        print("R4R12R4_ERROR=" + report["error"])
    print("R4R12R4_GATE=" + str(report["gate"]))
    return 1 if "error" in report else 0


if __name__ == "__main__":
    sys.exit(main())
