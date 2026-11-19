"""Read-only audit of actual torsion-generator representation in Toda (5.8)."""
from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
import json
from pathlib import Path
import subprocess
import traceback

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
    _linear_coordinates,
    delta_injective_inputs,
)
from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
    delta_free_coordinate_proposals,
    screened_toda58_available,
)
from proof import Relation, RelationType

PACKAGE = "phase175_r4r12r13r6_torsion_generator_audit"


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R13R6_GIT_FAILED: " + result.stderr)
    return result.stdout.strip()


def shape(value: object, depth: int = 0) -> dict[str, object]:
    """Show dataclass structure without assuming two notations are equal."""
    result: dict[str, object] = {"type": type(value).__name__, "repr": repr(value)}
    if depth >= 4:
        return result
    if is_dataclass(value) and not isinstance(value, type):
        result["fields"] = {
            field.name: shape(getattr(value, field.name), depth + 1)
            for field in fields(value)
        }
    elif isinstance(value, (tuple, list)):
        result["items"] = [shape(item, depth + 1) for item in value]
    return result


def inspect() -> dict[str, object]:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge

    signed = canonical_toda58()
    group = exact_prior_database_result(4, 3)
    if not isinstance(group, Relation) or not isinstance(group.rhs, DirectSumGroup):
        raise RuntimeError("R13R6_TYPED_PRIOR_GROUP_MISSING")
    free = [x for x in group.rhs.summands if isinstance(x, FreeCyclicGroup)]
    finite = [x for x in group.rhs.summands if isinstance(x, FiniteCyclicGroup)]
    if len(free) != 1 or len(finite) != 1:
        raise RuntimeError("R13R6_PRIOR_SUMMAND_SHAPE_CHANGED")
    source = Relation(signed.map.source_group, FreeCyclicGroup(signed.element), RelationType.EQUALITY)
    actual = finite[0].generator
    published = signed.positive_value.right.expression
    bridge = build_shared_typed_bridge()
    cited = screened_toda58_available(bridge)
    return {
        "signed_toda58": shape(signed),
        "source": shape(source),
        "target": shape(group),
        "db_torsion_generator": shape(actual),
        "toda58_torsion_expression": shape(published),
        "same_type": type(actual) is type(published),
        "exact_equality": actual == published,
        "same_repr": repr(actual) == repr(published),
        "free_generator_exact_equality": free[0].generator == signed.positive_value.left.expression,
        "linear_coordinates": _linear_coordinates(signed.positive_value, free[0].generator, actual),
        "guard_accepted": delta_injective_inputs(MapInjective(signed.map), source, group, signed) is not None,
        "cited58_screened": cited,
        "public_candidates": len(delta_free_coordinate_proposals(MapInjective(signed.map), cited58=cited)),
        "equivalence_proved": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_code_modified": False,
        "full_pytest_executed": False,
        "group_proof_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "175-R4R12R13R6", "dry_run": dry_run,
        "gate": "FAIL_R13R6", "full_pytest_executed": False,
    }
    try:
        if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
            raise RuntimeError("R13R6_WRONG_ROOT")
        if git(root, "branch", "--show-current") != "develop":
            raise RuntimeError("R13R6_WRONG_BRANCH")
        report["head"] = git(root, "rev-parse", "HEAD")
        report["diagnostics"] = inspect()
        report["gate"] = "PASS_R13R6_TYPED_GENERATOR_DIFFERENCE_AUDITED_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    filename = output / ("dry_run_report.json" if dry_run else "report.json")
    filename.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R13R6_GATE=" + str(report["gate"]))
    print("PHASE175_R13R6_HEAD=" + str(report.get("head", "UNVERIFIED")))
    if "diagnostics" in report:
        d = report["diagnostics"]
        for key in (
            "db_torsion_generator", "toda58_torsion_expression",
            "same_type", "exact_equality", "same_repr", "free_generator_exact_equality",
            "linear_coordinates", "guard_accepted", "cited58_screened", "public_candidates",
        ):
            value = d[key]
            if isinstance(value, dict):
                print("PHASE175_R13R6_" + key.upper() + "_TYPE=" + value["type"])
                print("PHASE175_R13R6_" + key.upper() + "_REPR=" + value["repr"])
            else:
                print("PHASE175_R13R6_" + key.upper() + "=" + str(value))
    print("PHASE175_R13R6_NEW_GIVEN=0")
    print("PHASE175_R13R6_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R13R6_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R6_REPORT=" + str(filename))
    if "error" in report:
        print("PHASE175_R13R6_ERROR=" + report["error"])
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
