"""Read-only trace: isolate R4R12 candidate generation from shared dispatch/filtering."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import tempfile
import traceback
from unittest.mock import patch

EXPECTED_HEADS = (
    "9203e1a8c077320a58214bda40d9bfeb17704f58",
)
RULE_NAME = "EHP exact rank-two elementary 2-group quotient by a generated summand"
PACKAGE = "phase175_r4r12r6_public_candidate_trace"


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R4R12R6_GIT_FAILED: " + " ".join(args) + ": " + result.stderr)
    return result.stdout.strip()


def verify_environment(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R4R12R6_WRONG_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R4R12R6_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")
    # Deliberately do not silently accept unknown commits; diagnostic may be
    # re-reviewed after new commits are made.
    if head not in EXPECTED_HEADS:
        raise RuntimeError("R4R12R6_UNREVIEWED_HEAD: " + head)
    changed = set(git(root, "diff", "--name-only").splitlines())
    changed.update(git(root, "diff", "--cached", "--name-only").splitlines())
    allowed = {".pytest_cache/v/cache/nodeids", "phase175_r4r3_two_summand_quotient/rule.py"}
    if changed - allowed:
        raise RuntimeError("R4R12R6_UNREVIEWED_TRACKED_CHANGE: " + repr(sorted(changed - allowed)))
    from phase175_r4r12r5_iterated_suspension_endpoints.installer import render, TARGET, git as installer_git
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("R4R12R6_RULE_MISSING")
    actual = path.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
    final, _, _ = render(actual)
    if actual != final:
        raise RuntimeError("R4R12R6_ENDPOINT_REPAIR_NOT_INSTALLED")
    # Require the typed shared-search provider wiring to actually exist.
    import inspect
    from phase165_r52_r9_shared_math import shared_expansion_provider
    if "build_public_two_summand_quotient_provider" not in inspect.getsource(shared_expansion_provider):
        raise RuntimeError("R4R12R6_PUBLIC_PROVIDER_NOT_WIRED")
    return {"head": head, "tracked_changes": sorted(changed), "endpoint_repair_verified": True}


def collect() -> dict[str, object]:
    from homotopy_groups import FiniteCyclicGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase175_r4r12_public_two_summand_quotient import provider as quotient
    from phase175_r4r3_two_summand_quotient.rule import two_summand_quotient_inputs

    root = exact_prior_database_result(5, 4)
    if root is None or not isinstance(root.rhs, FiniteCyclicGroup) or root.rhs.order != 2:
        raise RuntimeError("R4R12R6_ROOT_NOT_TYPED")
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    sources = quotient.ordered_summand_inputs(goal, proof_target=root)
    if sources is None:
        raise RuntimeError("R4R12R6_EARLIER_DB_MISSING")
    isolated = quotient.expand_public_two_summand_quotient(goal, proof_target=root)
    seen: list[dict[str, object]] = []
    original = quotient.build_public_two_summand_quotient_provider

    def wrapped_factory(*, proof_target: object):
        inner = original(proof_target=proof_target)
        def observed(candidate_goal: object):
            output = inner(candidate_goal)
            if candidate_goal == goal:
                seen.append({"count": len(output), "rules": [x.rule.name for x in output]})
            return output
        return observed

    bridge = build_shared_typed_bridge()
    with patch.object(quotient, "build_public_two_summand_quotient_provider", wrapped_factory):
        expansion = shared_expansion_provider(bridge, proof_target=root)
        returned = tuple(expansion(goal))
    selected = tuple(item for item in returned if item.rule.name == RULE_NAME)
    return {
        "isolated_count": len(isolated),
        "shared_wrapper_calls": len(seen),
        "shared_wrapper_details": seen,
        "shared_returned_count": len(returned),
        "shared_selected_count": len(selected),
        "shared_selected_match_isolated": all(x in isolated for x in selected),
        "expected_six_obligations": all(len(x.subgoals) == 6 for x in isolated),
        "source_0": repr(sources[0].lhs),
        "source_1": repr(sources[1].lhs),
        "candidate_rule": RULE_NAME,
        "rule_preconditions": [
            two_summand_quotient_inputs(goal, sources[0], sources[1],
                                        x.subgoals[2], x.subgoals[5]) == x.subgoals
            for x in isolated
        ],
        "new_given": 0,
        "new_mathematical_rules": 0,
        "proof_claimed": False,
    }


def run(root: Path, dry_run: bool) -> int:
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE
              / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ"))
    folder.mkdir(parents=True, exist_ok=False)
    report = {"phase": "175-R4R12R6", "dry_run": dry_run,
              "gate": "FAIL_R4R12R6", "full_pytest_executed": False,
              "pi95_proof_complete": False}
    try:
        report["environment"] = verify_environment(root)
        report["trace"] = collect()
        report["gate"] = "PASS_R4R12R6_READ_ONLY_TRACE_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    (folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R12R6_GATE=" + str(report["gate"]))
    if "environment" in report:
        print("PHASE175_R4R12R6_HEAD=" + str(report["environment"]["head"]))
    for key, value in report.get("trace", {}).items():
        print("PHASE175_R4R12R6_" + key.upper() + "=" + str(value))
    print("PHASE175_R4R12R6_REPORT=" + str(folder / "report.json"))
    if "error" in report:
        print("PHASE175_R4R12R6_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
