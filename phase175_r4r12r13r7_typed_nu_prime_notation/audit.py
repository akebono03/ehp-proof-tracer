"""Verify strict notation matching and real public Delta candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r7_typed_nu_prime_notation.installer import install
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import same_typed_generator_notation

PACKAGE = "phase175_r4r12r13r7_typed_nu_prime_notation"


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", *args], cwd=root, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", check=False)
    if p.returncode != 0:
        raise RuntimeError("R13R7_GIT_FAILED " + repr(args) + ": " + p.stderr)
    return p.stdout.strip()


def inspect(*, proof_before_patch: bool) -> dict[str, object]:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
        delta_free_coordinate_proposals, screened_toda58_available,
    )
    signed = canonical_toda58()
    relation = exact_prior_database_result(4, 3)
    if relation is None or not isinstance(relation.rhs, DirectSumGroup):
        raise RuntimeError("R13R7_DB_GROUP_MISSING")
    parts = [x for x in relation.rhs.summands if isinstance(x, FiniteCyclicGroup)]
    if len(parts) != 1:
        raise RuntimeError("R13R7_TORSION_PART_NOT_UNIQUE")
    cited = screened_toda58_available(build_shared_typed_bridge())
    goal = MapInjective(signed.map)
    count = len(delta_free_coordinate_proposals(goal, cited58=cited))
    return {
        "toda58_citation_screened": cited,
        "raw_torsion_equal": signed.positive_value.right.expression == parts[0].generator,
        "strict_notation_alias": same_typed_generator_notation(
            signed.positive_value.right.expression, parts[0].generator),
        "public_delta_candidates": count,
        "requires_positive_count_after_install": not proof_before_patch,
        "group_proof_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R13R7_ROOT_MISMATCH")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R13R7_BRANCH_MISMATCH")
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    report = {"phase": "175-R4R12R13R7", "dry_run": dry_run,
              "head": git(root, "rev-parse", "HEAD"), "new_given": 0,
              "new_mathematical_rules": 0, "full_pytest": "NOT_RUN",
              "gate": "FAIL_R13R7"}
    try:
        report["patch"] = install(root, dry_run=dry_run, output=output)
        # DryRun intentionally examines the unpatched process without
        # ever claiming a public proof is available.
        report["frontier"] = inspect(proof_before_patch=dry_run)
        f = report["frontier"]
        if not f["toda58_citation_screened"] or not f["strict_notation_alias"]:
            raise RuntimeError("R13R7_SOURCE_OR_NOTATION_GUARD_FAILED")
        if not dry_run and f["public_delta_candidates"] != 1:
            raise RuntimeError("R13R7_DELTA_CANDIDATE_NOT_CONNECTED")
        report["gate"] = ("PASS_R13R7_DRYRUN_NOT_COMPLETE" if dry_run else
                          "PASS_R13R7_DELTA_CANDIDATE_CONNECTED_NOT_COMPLETE")
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    path = output / ("dry_run_report.json" if dry_run else "report.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R13R7_GATE=" + report["gate"])
    print("PHASE175_R13R7_HEAD=" + report["head"])
    for key, val in report.get("frontier", {}).items():
        print("PHASE175_R13R7_" + key.upper() + "=" + str(val))
    print("PHASE175_R13R7_NEW_GIVEN=0")
    print("PHASE175_R13R7_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R13R7_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R7_REPORT=" + str(path))
    if "error" in report:
        print("PHASE175_R13R7_ERROR=" + report["error"])
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
