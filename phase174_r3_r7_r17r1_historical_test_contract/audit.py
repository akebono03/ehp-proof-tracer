"""R17R1: fail-closed source/contract gate for an obsolete historical test fixture."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from phase174_r3_r7_r17r1_historical_test_contract.patch import (
    TARGET as TEST_TARGET, EXPECTED_BLOB, original_matches, patched_bytes,
    normalized,
)
from phase174_r3_r7_r17_typed_map_open_goal.patch import (
    TARGET as DISPLAY_TARGET, EXPECTED_BLOB as DISPLAY_BLOB,
    expected_patched_bytes, matches_git_blob,
)

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HEAD = "388f63797a6aba61418bb93e734b8ce5999dc7f6"
R17_HELPERS = {
    "phase174_r3_r7_r17_typed_map_open_goal/audit.py": "5d410158c4fc28aeaa2f326d5429c67f671c3489cb2aabcf7677426c01d83cc9",
    "phase174_r3_r7_r17_typed_map_open_goal/patch.py": "4f757bf2c28f150c01422a93631123b644fc4fc0e62cf65092a57cf676c72bdb",
    "phase174_r3_r7_r17_typed_map_open_goal/tests/test_public.py": "a0d6ca568840482393178c4b5a7db6e754c055468e9f64c1d6ab0a0485ba741d",
    "phase174_r3_r7_r17_typed_map_open_goal/tests/test_patch.py": "672fbc1d4104dc1533f5bf3a7849349327092e6274d1c41bf2c28736ac0bb8fd",
    "phase174_r3_r7_r17_typed_map_open_goal/tests/test_audit.py": "a13db50a2fb98738f50844a0c88119c889c638e2a37a93b3cb1050d070a3dbf5",
}


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(("git",) + args, cwd=root, check=True,
                          text=True, capture_output=True, encoding="utf-8",
                          errors="replace").stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(("git",) + args, cwd=root, check=True,
                          capture_output=True).stdout


def expected_tracked_paths(*, applied: bool) -> tuple[str, ...]:
    """Use Git's repository-relative forward slash paths on every OS."""
    if type(applied) is not bool:
        raise TypeError("applied must be bool")
    if not applied:
        return ()
    return tuple(sorted((TEST_TARGET.as_posix(), DISPLAY_TARGET.as_posix())))


def verify_source_and_state(*, applied: bool, root: Path = ROOT) -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract the package directly under the repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if local != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError("Unreviewed GitHub/local HEAD; abort without checkout or reset")
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Unexpected staged files")
    changed = tuple(git("diff", "--name-only", root=root).splitlines())
    expected_changed = expected_tracked_paths(applied=applied)
    if tuple(sorted(changed)) != expected_changed:
        raise RuntimeError("Unexpected tracked changes: " + str(changed))
    for relative, digest in R17_HELPERS.items():
        path = root / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError("R17 package differs from inspected original: " + relative)
    tracked_test = git_bytes("show", "HEAD:" + TEST_TARGET.as_posix(), root=root)
    if not original_matches(tracked_test):
        raise RuntimeError("Historical test Git blob no longer matches " + EXPECTED_BLOB)
    test_worktree = (root / TEST_TARGET).read_bytes()
    expected_test = patched_bytes(tracked_test) if applied else tracked_test
    if normalized(test_worktree)[0] != normalized(expected_test)[0]:
        raise RuntimeError("Historical test worktree changed unexpectedly")
    tracked_display = git_bytes("show", "HEAD:" + DISPLAY_TARGET.as_posix(), root=root)
    if not matches_git_blob(tracked_display, DISPLAY_BLOB):
        raise RuntimeError("Reviewed common formatter Git blob changed")
    local_display = (root / DISPLAY_TARGET).read_bytes()
    expected_display = expected_patched_bytes(tracked_display) if applied else tracked_display
    if normalized(local_display)[0] != normalized(expected_display)[0]:
        raise RuntimeError("Common formatter is not in the reviewed R17 state")
    return {"branch": "develop", "local_head": local, "remote_head": remote,
            "tracked_changes": list(changed), "source_guard": "PASS", "corrected_test_applied": applied,
            "source_hashes_checked": len(R17_HELPERS) + 2}


def verify_r17_proof_boundary() -> dict[str, object]:
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r17"
    path = directory / "typed_map_public_audit.json"
    if not path.is_file():
        raise RuntimeError("R17 public audit report missing: " + str(path))
    report = json.loads(path.read_text(encoding="utf-8-sig"))
    live = report.get("live") or {}
    if (report.get("phase") != "174-R3-R7-R17"
            or report.get("gate") != "PASS_TYPED_DELTA_OPEN_GOAL_SURJECTIVITY_STILL_PENDING"
            or report.get("new_group_given") != 0
            or report.get("new_math_rules") != 0
            or report.get("full_pytest_run") is not False
            or report.get("completion_claimed") is not False
            or live.get("public_root_candidates") != 1
            or live.get("public_delta_surjectivity_candidates") != 0
            or live.get("search_status") != "search_failed"
            or live.get("proven_steps") != 0):
        raise RuntimeError("R17 public proof boundary changed")
    return {"r17_gate": report["gate"], "root_candidates": 1,
            "delta_surjectivity_candidates": 0, "target_completed": False}


def report_path(*, applied: bool) -> Path:
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r17r1"
    return directory / ("historical_contract_audit.json" if applied else "historical_contract_preflight.json")


def make_report(*, applied: bool, root: Path = ROOT) -> dict[str, object]:
    state = verify_source_and_state(applied=applied, root=root)
    report = {"phase": "174-R3-R7-R17R1", "state": state,
              "source_guard": "PASS", "new_math_rules": 0,
              "new_group_given": 0, "full_pytest_run": False,
              "historical_case_pi8_5_now_complete": True,
              "gate": ("PASS_HISTORICAL_TEST_CONTRACT_CORRECTED_R17_PUBLIC_UNCHANGED"
                       if applied else "PASS_PREFLIGHT")}
    if applied:
        report["r17_boundary"] = verify_r17_proof_boundary()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--applied", action="store_true")
    args = parser.parse_args()
    report = make_report(applied=args.applied)
    path = report_path(applied=args.applied)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R17R1_"
    print(prefix + "LOCAL_HEAD=" + str(report["state"]["local_head"]))
    print(prefix + "REMOTE_HEAD=" + str(report["state"]["remote_head"]))
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "TRACKED_CHANGES=" + ",".join(report["state"]["tracked_changes"]))
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_MATH_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + str(report["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
