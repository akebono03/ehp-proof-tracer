# Phase 175 R4R12R3 — 実装・テスト全文

## 新規 diagnose.py（追加位置：新規パッケージ直下）

```python
"""Read-only typed root-candidate diagnostic for Phase 175 R4R12."""
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


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", check=False)
    if completed.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + ": " + completed.stderr.strip())
    return completed.stdout.strip()


def equal_check(name: str, actual: object, expected: object) -> dict[str, object]:
    return {"check": name, "equal": actual == expected,
            "actual": repr(actual), "expected": repr(expected),
            "actual_type": type(actual).__name__, "expected_type": type(expected).__name__}


def inspect_candidate() -> dict[str, object]:
    from homotopy_groups import (DirectSumGroup, FiniteCyclicGroup, TodaDeltaMap,
                                 TodaEHPExactnessWindow, TodaPrimaryGroup, TodaSuspensionMap)
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import _endpoints
    from phase175_r4r3_two_summand_quotient.rule import two_summand_quotient_inputs
    from phase175_r4r12_public_two_summand_quotient.provider import (
        ordered_summand_inputs, expand_public_two_summand_quotient)
    from proof import Relation, RelationType
    from toda_rules import TodaProp42ExactnessStatement

    root = exact_prior_database_result(5, 4)
    if not isinstance(root, Relation) or not isinstance(root.rhs, FiniteCyclicGroup):
        raise RuntimeError("ROOT_GOAL_NOT_FINITE_CYCLIC_RELATION")
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    sources = ordered_summand_inputs(goal, proof_target=root)
    result: dict[str, object] = {"root": repr(root), "goal": repr(goal),
                                 "sources_present": sources is not None,
                                 "actual_proof_search_executed": False,
                                 "new_given": 0, "new_mathematical_rules": 0}
    if sources is None:
        result["failure_boundary"] = "ORDERED_SOURCE_INPUTS_MISSING"
        return result
    middle, source = sources
    result["middle"] = repr(middle)
    result["source"] = repr(source)
    result["middle_type"] = type(middle).__name__
    result["source_type"] = type(source).__name__
    result["middle_sum"] = repr(getattr(middle, "rhs", None))
    checks: list[dict[str, object]] = []
    result["checks"] = checks
    parts = getattr(getattr(middle, "rhs", None), "summands", None)
    checks.append({"check": "two_distinct_order_two_summands",
                   "equal": isinstance(parts, tuple) and len(parts) == 2
                   and all(isinstance(item, FiniteCyclicGroup) and item.order == 2 for item in parts)
                   and parts[0].generator != parts[1].generator if isinstance(parts, tuple) and len(parts) == 2 else False,
                   "actual": repr(parts)})
    checks.append({"check": "delta_source_order_two",
                   "equal": isinstance(getattr(source, "rhs", None), FiniteCyclicGroup)
                   and source.rhs.order == 2, "actual": repr(getattr(source, "rhs", None))})
    if not (isinstance(parts, tuple) and len(parts) == 2
            and isinstance(getattr(source, "rhs", None), FiniteCyclicGroup)):
        result["failure_boundary"] = "GROUP_SOURCE_SHAPE"
        return result
    delta_map = TodaDeltaMap(source.lhs, middle.lhs)
    e_map = TodaSuspensionMap(middle.lhs, goal.group)
    exactness = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=source.lhs, middle_term=middle.lhs, target_term=goal.group,
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP))
    result["exactness_indices"] = repr(prop42_exactness_indices(exactness))
    result["delta_map"] = repr(delta_map)
    result["e_map"] = repr(e_map)
    result["source_generator"] = repr(source.rhs.generator)
    result["target_generator"] = repr(goal.generator)
    for i, part in enumerate(parts):
        result[f"summand_{i}_generator"] = repr(part.generator)
        result[f"summand_{i}_endpoints"] = repr(_endpoints(part.generator))
    result["source_generator_endpoints"] = repr(_endpoints(source.rhs.generator))
    result["target_generator_endpoints"] = repr(_endpoints(goal.generator))
    checks.append({"check": "exactness_indices_available",
                   "equal": prop42_exactness_indices(exactness) is not None,
                   "actual": repr(prop42_exactness_indices(exactness))})
    checks.append(equal_check("middle_generator_0_endpoints", _endpoints(parts[0].generator),
                              (middle.lhs.group_dimension, middle.lhs.sphere_dimension)))
    checks.append(equal_check("middle_generator_1_endpoints", _endpoints(parts[1].generator),
                              (middle.lhs.group_dimension, middle.lhs.sphere_dimension)))
    checks.append(equal_check("source_generator_endpoints", _endpoints(source.rhs.generator),
                              (source.lhs.group_dimension, source.lhs.sphere_dimension)))
    checks.append(equal_check("target_generator_endpoints", _endpoints(goal.generator),
                              (goal.group.group_dimension, goal.group.sphere_dimension)))
    for killed_index in (0, 1):
        survivor_index = 1-killed_index
        delta = GeneratorImage(delta_map, source.rhs.generator, parts[killed_index].generator)
        suspension = GeneratorImage(e_map, parts[survivor_index].generator, goal.generator)
        result[f"orientation_{killed_index}_typed_inputs"] = (
            two_summand_quotient_inputs(goal, middle, source, delta, suspension) is not None)
    try:
        options = expand_public_two_summand_quotient(goal, proof_target=root)
        result["actual_candidate_count"] = len(options)
        result["actual_candidate_rule_names"] = [getattr(getattr(option, "rule", None), "name", "")
                                                 for option in options]
        result["actual_candidate_subgoals"] = [repr(getattr(option, "subgoals", None)) for option in options]
    except Exception as exc:
        result["provider_error"] = type(exc).__name__ + ": " + str(exc)
        result["provider_traceback"] = traceback.format_exc()[-4000:]
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")
    if head != "344fc101fdfcce49ec80f867f80a0614d96c214e":
        raise RuntimeError("UNREVIEWED_HEAD: " + head)
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) /
              "EHPProofTracerAudit" / "phase175_r4r12r3_candidate_diagnostic" /
              datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ"))
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {"head": head, "gate": "DIAGNOSTIC_ONLY_NOT_COMPLETE"}
    try:
        report["candidate"] = inspect_candidate()
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    path = folder / "report.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R12R3_HEAD=" + head)
    if isinstance(report.get("candidate"), dict):
        candidate = report["candidate"]
        print("PHASE175_R4R12R3_CANDIDATES=" + str(candidate.get("actual_candidate_count", "UNKNOWN")))
        for check in candidate.get("checks", []):
            print("CHECK " + str(check["check"]) + "=" + str(check["equal"]))
        for i in (0, 1):
            print("ORIENTATION_" + str(i) + "=" + str(candidate.get(f"orientation_{i}_typed_inputs", "UNKNOWN")))
        if "provider_error" in candidate:
            print("PHASE175_R4R12R3_PROVIDER_ERROR=" + str(candidate["provider_error"]))
    if "error" in report:
        print("PHASE175_R4R12R3_ERROR=" + str(report["error"]))
    print("PHASE175_R4R12R3_REPORT=" + str(path))
    print("PHASE175_R4R12R3_GATE=DIAGNOSTIC_ONLY_NOT_COMPLETE")
    return 1 if "error" in report else 0


if __name__ == "__main__":
    sys.exit(main())

```

## 新規 tests/test_diagnose.py（追加位置：tests ディレクトリ）

```python
"""Focused non-mathematical diagnostic helper tests."""
from __future__ import annotations

from phase175_r4r12r3_candidate_diagnostic.diagnose import equal_check


def test_equal_check_reports_match() -> None:
    result = equal_check("generator", (9, 5), (9, 5))
    assert result["equal"] is True
    assert result["check"] == "generator"


def test_equal_check_reports_mismatch_without_asserting_proof() -> None:
    result = equal_check("generator", (9, 4), (9, 5))
    assert result["equal"] is False
    assert result["actual"] != result["expected"]

```
