# Phase 175 R4R12R7R1 置換コード全文

## audit.py（全体）

```python
"""Read-only Phase 175 R4R12R7 audit of six quotient obligations.

No proof search, source claim registration or production modification occurs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import tempfile
import traceback

PACKAGE = "phase175_r4r12r7_six_obligation_frontier"
BASE_HEAD = "9203e1a8c077320a58214bda40d9bfeb17704f58"
RULE_NAME = "EHP exact rank-two elementary 2-group quotient by a generated summand"
ALLOWED_DIRTY = {".pytest_cache/v/cache/nodeids", "phase175_r4r3_two_summand_quotient/rule.py"}
REVIEWED_HEAD = "94c5d6839889bbfa03aad166ac9c6fd1558b8c5b"
REVIEWED_COMMITTED_PATHS = frozenset(
    frozenset(('.pytest_cache/v/cache/nodeids', 'phase175_r4r12r5_iterated_suspension_endpoints/AUDIT_PLAN_JA.md', 'phase175_r4r12r5_iterated_suspension_endpoints/CODE_FULL_JA.md', 'phase175_r4r12r5_iterated_suspension_endpoints/README.md', 'phase175_r4r12r5_iterated_suspension_endpoints/__init__.py', 'phase175_r4r12r5_iterated_suspension_endpoints/audit.py', 'phase175_r4r12r5_iterated_suspension_endpoints/installer.py', 'phase175_r4r12r5_iterated_suspension_endpoints/run.ps1', 'phase175_r4r12r5_iterated_suspension_endpoints/tests/test_endpoints.py', 'phase175_r4r12r5_iterated_suspension_endpoints/tests/test_installer.py', 'phase175_r4r12r6_public_candidate_trace/AUDIT_PLAN_JA.md', 'phase175_r4r12r6_public_candidate_trace/CODE_FULL_JA.md', 'phase175_r4r12r6_public_candidate_trace/README.md', 'phase175_r4r12r6_public_candidate_trace/__init__.py', 'phase175_r4r12r6_public_candidate_trace/run.ps1', 'phase175_r4r12r6_public_candidate_trace/tests/test_trace.py', 'phase175_r4r12r6_public_candidate_trace/trace.py', 'phase175_r4r3_two_summand_quotient/rule.py', 'r4r12r5r1_build/phase175_r4r12r5_iterated_suspension_endpoints/AUDIT_PLAN_JA.md', 'r4r12r5r1_build/phase175_r4r12r5_iterated_suspension_endpoints/CODE_FULL_JA.md', 'r4r12r5r1_build/phase175_r4r12r5_iterated_suspension_endpoints/README.md', 'r4r12r5r1_build/phase175_r4r12r5_iterated_suspension_endpoints/__init__.py', 'r4r12r5r1_build/phase175_r4r12r5_iterated_suspension_endpoints/audit.py', 'r4r12r5r1_build/phase175_r4r12r5_iterated_suspension_endpoints/installer.py', 'r4r12r5r1_build/phase175_r4r12r5_iterated_suspension_endpoints/run.ps1', 'r4r12r5r1_build/phase175_r4r12r5_iterated_suspension_endpoints/tests/test_endpoints.py', 'r4r12r5r1_build/phase175_r4r12r5_iterated_suspension_endpoints/tests/test_installer.py'))
)



def git(root: Path, *arguments: str, allow_failure: bool = False) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode and not allow_failure:
        raise RuntimeError("R4R12R7_GIT_FAILED: " + " ".join(arguments) + " " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def verify_environment(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")[1]).resolve() != root.resolve():
        raise RuntimeError("R4R12R7_WRONG_ROOT")
    if git(root, "branch", "--show-current")[1] != "develop":
        raise RuntimeError("R4R12R7_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")[1]
    # Permit descendants only if all previously reviewed tracked source blobs remain unchanged.
    ancestor = git(root, "merge-base", "--is-ancestor", BASE_HEAD, head, allow_failure=True)[0]
    if ancestor:
        raise RuntimeError("R4R12R7_UNREVIEWED_LINEAGE: " + head)
    changed_since = set(git(root, "diff", "--name-only", BASE_HEAD, head)[1].splitlines())
    if head != REVIEWED_HEAD or changed_since != REVIEWED_COMMITTED_PATHS:
        raise RuntimeError(
            "R4R12R7_UNREVIEWED_COMMITTED_CHANGES: "
            + repr(sorted(changed_since))
            + "; head=" + head
        )
    dirty = set(git(root, "diff", "--name-only")[1].splitlines())
    dirty.update(git(root, "diff", "--cached", "--name-only")[1].splitlines())
    if dirty - ALLOWED_DIRTY:
        raise RuntimeError("R4R12R7_UNREVIEWED_TRACKED_CHANGES: " + repr(sorted(dirty)))
    from phase175_r4r12r5_iterated_suspension_endpoints.installer import render, TARGET
    current = (root / TARGET).read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
    updated, _, _ = render(current)
    if current != updated:
        raise RuntimeError("R4R12R7_ENDPOINT_REPAIR_NOT_INSTALLED")
    from phase165_r52_r9_shared_math import shared_expansion_provider
    import inspect
    if "build_public_two_summand_quotient_provider" not in inspect.getsource(shared_expansion_provider):
        raise RuntimeError("R4R12R7_PUBLIC_PROVIDER_MISSING")
    return {"head": head, "changed_since_reviewed": sorted(changed_since), "dirty": sorted(dirty)}


def describe(value: object) -> str:
    result = repr(value)
    return result if len(result) <= 450 else result[:447] + "..."


def audit_obligations() -> dict[str, object]:
    from homotopy_groups import FiniteCyclicGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient

    root = exact_prior_database_result(5, 4)
    if root is None or not isinstance(root.rhs, FiniteCyclicGroup) or root.rhs.order != 2:
        raise RuntimeError("R4R12R7_ROOT_NOT_TYPED")
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    isolated = expand_public_two_summand_quotient(goal, proof_target=root)
    bridge = build_shared_typed_bridge()
    shared = shared_expansion_provider(bridge, proof_target=root)
    selected = tuple(item for item in shared(goal) if item.rule.name == RULE_NAME)
    if len(isolated) != 2 or len(selected) != 2:
        raise RuntimeError("R4R12R7_TWO_CANDIDATES_REQUIRED")
    # Compare substantive subgoal values, not inference-rule function identities.
    isolated_signatures = tuple(tuple(item.subgoals) for item in isolated)
    shared_signatures = tuple(tuple(item.subgoals) for item in selected)
    if (len(isolated_signatures) != len(shared_signatures)
            or any(not any(item == other for other in shared_signatures)
                   for item in isolated_signatures)):
        raise RuntimeError("R4R12R7_ACTUAL_PREMISE_MISMATCH")
    paths: list[dict[str, object]] = []
    for index, candidate in enumerate(selected):
        if len(candidate.subgoals) != 6:
            raise RuntimeError("R4R12R7_INVALID_OBLIGATION_COUNT")
        detail: list[dict[str, object]] = []
        for position, obligation in enumerate(candidate.subgoals):
            prior_verified = False
            if position < 2:
                prior = admitted_db_step(obligation, proof_target=root)
                prior_verified = prior is not None and verified_db_step(prior, proof_target=root)
                option_count = 0
                rules: list[str] = []
            else:
                # Search *expansion candidates* only. No recursive search and no proof assertion.
                proposals = tuple(shared(obligation))
                option_count = len(proposals)
                rules = [item.rule.name for item in proposals][:20]
            detail.append({
                "index": position,
                "statement_type": type(obligation).__name__,
                "statement": describe(obligation),
                "admitted_prior_verified": prior_verified,
                "backward_candidate_count": option_count,
                "backward_rule_names_first20": rules,
                "proved": False,
            })
        paths.append({"orientation": index, "obligations": detail})
    return {
        "isolated_count": len(isolated),
        "shared_count": len(selected),
        "same_typed_subgoals": True,
        "six_obligations_per_route": True,
        "paths": paths,
        "actual_recursive_proof_search_executed": False,
        "group_proof_complete": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
    }


def run(root: Path, dry_run: bool) -> int:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    result: dict[str, object] = {"phase": "175-R4R12R7", "dry_run": dry_run,
                                  "gate": "FAIL_R4R12R7", "full_pytest_executed": False}
    try:
        result["environment"] = verify_environment(root)
        result["frontier"] = audit_obligations()
        result["gate"] = "PASS_R4R12R7_SIX_OBLIGATION_FRONTIER_NOT_COMPLETE"
    except Exception as error:
        result["error"] = type(error).__name__ + ": " + str(error)
        result["traceback"] = traceback.format_exc()[-7000:]
    (folder / "report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R12R7_GATE=" + str(result["gate"]))
    if "environment" in result:
        print("PHASE175_R4R12R7_HEAD=" + str(result["environment"]["head"]))
    if "frontier" in result:
        f = result["frontier"]
        print("PHASE175_R4R12R7_SHARED_SAME_SUBGOALS=" + str(f["same_typed_subgoals"]))
        for path in f["paths"]:
            print("PHASE175_R4R12R7_ORIENTATION=" + str(path["orientation"]))
            for obj in path["obligations"]:
                print("  OBLIGATION_" + str(obj["index"]) + "_TYPE=" + obj["statement_type"])
                print("  OBLIGATION_" + str(obj["index"]) + "_PRIOR=" + str(obj["admitted_prior_verified"]))
                print("  OBLIGATION_" + str(obj["index"]) + "_CANDIDATES=" + str(obj["backward_candidate_count"]))
                print("  OBLIGATION_" + str(obj["index"]) + "_RULES=" + repr(obj["backward_rule_names_first20"]))
                print("  OBLIGATION_" + str(obj["index"]) + "_STATEMENT=" + obj["statement"])
    print("PHASE175_R4R12R7_REPORT=" + str(folder / "report.json"))
    if "error" in result:
        print("PHASE175_R4R12R7_ERROR=" + str(result["error"]))
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

```

## tests/test_audit.py（全体）

```python
"""Read-only contract tests for Phase 175 R4R12R7."""
from pathlib import Path
import pytest
from phase175_r4r12r7_six_obligation_frontier import audit


def test_git_failure_is_not_silently_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    class Failed:
        returncode = 1
        stdout = ""
        stderr = "failure"
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="GIT_FAILED"):
        audit.git(Path("."), "rev-parse", "HEAD")


def test_describe_truncates_long_statements() -> None:
    assert audit.describe("x" * 800).endswith("...")
    assert len(audit.describe("x" * 800)) == 450


def test_dirty_allowlist_is_not_broad() -> None:
    assert audit.ALLOWED_DIRTY == {
        ".pytest_cache/v/cache/nodeids", "phase175_r4r3_two_summand_quotient/rule.py"
    }


def test_reviewed_commit_pin_and_exact_diff() -> None:
    assert audit.REVIEWED_HEAD == "94c5d6839889bbfa03aad166ac9c6fd1558b8c5b"
    assert "phase175_r4r12r6_public_candidate_trace/trace.py" in audit.REVIEWED_COMMITTED_PATHS
    assert "phase175_r4r3_two_summand_quotient/rule.py" in audit.REVIEWED_COMMITTED_PATHS
    assert "phase175_r4r12r7_six_obligation_frontier/audit.py" not in audit.REVIEWED_COMMITTED_PATHS

```
