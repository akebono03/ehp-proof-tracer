# Phase 174 R3-R7-R18R2：変更コード・関連テスト全文

変更する既存の関数は `phase174_r3_r7_r18_delta_image_surjectivity/audit.py` の `validate_prior_r17` のみです。既存 import は変更しません。新規ファイル・関数はすべて新規パッケージ内に追加します。

## 変更後の既存関数全文

```python
def validate_prior_r17() -> dict[str, Any]:
    """Validate prior evidence or recheck the live public proof boundary.

    Local audit JSON is per-Windows-profile state, not a mathematical axiom.
    Absence triggers fresh R17 public-search verification, never fabricated
    evidence or a silent transfer of another account's audit report.
    Present but invalid evidence is rejected instead of being bypassed.
    Git source pins and the corrected historical-test source are checked
    separately by verify_git_and_sources() before this function is called.
    """
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit"
    required = (
        ("phase174_r3_r7_r17/typed_map_public_audit.json",
         "174-R3-R7-R17", "PASS_TYPED_DELTA_OPEN_GOAL_SURJECTIVITY_STILL_PENDING"),
        ("phase174_r3_r7_r17r1/historical_contract_audit.json",
         "174-R3-R7-R17R1", "PASS_HISTORICAL_TEST_CONTRACT_CORRECTED_R17_PUBLIC_UNCHANGED"),
    )
    results: dict[str, Any] = {}
    missing: list[tuple[str, str]] = []
    for relative, phase, gate in required:
        path = base / relative
        if not path.is_file():
            missing.append((relative, phase))
            continue
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
        if (obj.get("phase") != phase or obj.get("gate") != gate
                or obj.get("new_group_given") != 0
                or obj.get("full_pytest_run") is not False):
            raise RuntimeError("Prior R17 evidence inconsistent: " + relative)
        results[phase] = gate

    if missing:
        from phase174_r3_r7_r17_typed_map_open_goal.audit import (
            inspect_public_map_display,
        )
        live = inspect_public_map_display()
        expected_delta = r"\Delta: \pi_{13}^{13} \twoheadrightarrow \pi_{11}^{6}"
        if (live.get("public_root_candidates") != 1
                or live.get("public_delta_surjectivity_candidates") != 0
                or live.get("generic_isomorphism_depends_on_surjectivity") is not True
                or live.get("direct_given_for_goal_or_delta") is not False
                or live.get("delta_latex") != expected_delta
                or live.get("search_status") != "search_failed"
                or live.get("proven_steps") != 0
                or live.get("completion_claimed") is not False):
            raise RuntimeError("Live R17 proof boundary cannot replace missing local evidence")
        for relative, phase in missing:
            if phase == "174-R3-R7-R17":
                results[phase] = "LIVE_PUBLIC_BOUNDARY_REVALIDATED_NO_LOCAL_REPORT"
            else:
                results[phase] = "CORRECTED_TEST_SOURCE_PINNED_NO_LOCAL_REPORT"
        results["recovery"] = {
            "mode": "LIVE_REVALIDATED_NO_SYNTHETIC_REPORT",
            "missing_local_reports": [relative for relative, _ in missing],
            "public_root_candidates": live["public_root_candidates"],
            "delta_surjectivity_candidates": live["public_delta_surjectivity_candidates"],
            "verified_steps": live["proven_steps"],
            "corrected_historical_test_pinned_by_source_guard": True,
        }
    return results
```

## `__init__.py` 全文

```python
"""Local-profile-independent R18 R17 evidence boundary revalidation."""
```

## `patch.py` 全文

```python
"""Exact, source-guarded replacement of R18's per-profile evidence dependency."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase174_r3_r7_r18_delta_image_surjectivity/audit.py")
R18R1_PACKAGE = Path("phase174_r3_r7_r18r1_git_mixed_eol_guard")
R18R1_SOURCE = R18R1_PACKAGE / "replacement_audit.py.txt"
REPLACEMENT_SOURCE = Path(__file__).resolve().parent / "EXPECTED_REPLACEMENT_AUDIT.py.txt"
REPLACEMENT_FUNCTION = Path(__file__).resolve().parent / "REVIEWED_REPLACEMENT_VALIDATE_R17.py.txt"
EXPECTED_R18_ORIGINAL_SHA256 = "e0e0c986762f76dc601b0cdf6c01d81eece696dc2bb5f593ca0fd2debf045c73"
EXPECTED_R18R1_SHA256 = "7ff6ab7b4f4b7595c6e16216e8c3a8e1edf3845cc4dcfdb3165879e4c7f57aaa"
EXPECTED_R18R2_SHA256 = "7a70bd1368828b13ce7950da8d5fb246af3ddbc4775457d5ea5ba99555131222"
EXPECTED_LOCAL_R17_HEAD = "4d59298949c14dc02d8bfb6ec28da4624ed980da"
EXPECTED_R18_HEAD = "7ecd12f28b5943b105ac6a953be69b44eae4a26e"
R18_PREFIX = "phase174_r3_r7_r18_delta_image_surjectivity/"
FUNCTION_START = "def validate_prior_r17() -> dict[str, Any]:\n"
FUNCTION_END = "\ndef inspect_live_frontier() -> dict[str, Any]:\n"
BACKUP = (
    Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    / "EHPProofTracerAudit" / "phase174_r3_r7_r18r2" / "audit_r18r1_original.py"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ("git",) + args, cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=root, check=True, capture_output=True,
    ).stdout


def checked_replacement(root: Path = ROOT) -> tuple[bytes, bytes]:
    old_file = root / R18R1_SOURCE
    if not old_file.is_file():
        raise RuntimeError("Reviewed R18R1 package is required")
    before = old_file.read_bytes()
    if sha256(before) != EXPECTED_R18R1_SHA256:
        raise RuntimeError("R18R1 replacement was not the reviewed source")
    function = REPLACEMENT_FUNCTION.read_text(encoding="utf-8")
    after = REPLACEMENT_SOURCE.read_bytes()
    if (sha256(after) != EXPECTED_R18R2_SHA256
            or before.decode("utf-8").count(FUNCTION_START) != 1
            or before.decode("utf-8").count(FUNCTION_END) != 1
            or after != transform(before, function)):
        raise RuntimeError("Unreviewed R18R2 replacement source")
    compile(after, str(TARGET), "exec")
    return before, after


def transform(before: bytes, function: str) -> bytes:
    """Replace one complete function with no other source changes."""
    source = before.decode("utf-8")
    if source.count(FUNCTION_START) != 1 or source.count(FUNCTION_END) != 1:
        raise RuntimeError("Reviewed R18R1 function anchors missing or duplicated")
    if not function.startswith(FUNCTION_START) or not function.endswith("\n"):
        raise RuntimeError("Replacement must be the entire function")
    start = source.index(FUNCTION_START)
    end = source.index(FUNCTION_END, start)
    result = source[:start] + function + "\n" + source[end:]
    compile(result, str(TARGET), "exec")
    return result.encode("utf-8")


def source_state(root: Path = ROOT) -> str:
    contents = (root / TARGET).read_bytes()
    value = sha256(contents)
    if value == EXPECTED_R18_ORIGINAL_SHA256:
        return "REVIEWED_R18_ORIGINAL"
    if value == EXPECTED_R18R1_SHA256:
        return "R18R1_MIXED_EOL_CORRECTED"
    if value == EXPECTED_R18R2_SHA256:
        _, expected = checked_replacement(root=root)
        if contents == expected:
            return "R18R2_EVIDENCE_REVALIDATION_INSTALLED"
    raise RuntimeError("R18 audit.py has unexpected content")


def verify_git_and_source(root: Path = ROOT) -> dict[str, str]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R18R2 directly below the repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Only the reviewed develop branch is allowed")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if remote != EXPECTED_R18_HEAD or local not in (
        EXPECTED_LOCAL_R17_HEAD, EXPECTED_R18_HEAD,
    ):
        raise RuntimeError("GitHub or local develop HEAD changed since review")
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged work requires separate review")
    changed = tuple(git("diff", "--name-only", root=root).splitlines())
    state = source_state(root=root)
    allowed = (TARGET.as_posix(),) if local == EXPECTED_R18_HEAD and state != "REVIEWED_R18_ORIGINAL" else ()
    if changed != allowed:
        raise RuntimeError("Unreviewed tracked changes: " + repr(changed))
    git_bytes("merge-base", "--is-ancestor", EXPECTED_LOCAL_R17_HEAD,
              EXPECTED_R18_HEAD, root=root)
    commits = git("rev-list", EXPECTED_LOCAL_R17_HEAD + ".." + EXPECTED_R18_HEAD,
                  root=root).splitlines()
    changed_in_commit = git("diff", "--name-only", EXPECTED_LOCAL_R17_HEAD,
                            EXPECTED_R18_HEAD, root=root).splitlines()
    if (len(commits) != 1 or not changed_in_commit
            or any(not name.startswith(R18_PREFIX) for name in changed_in_commit)):
        raise RuntimeError("Unreviewed R18 merge lineage")
    reviewed = git_bytes("show", "origin/develop:" + TARGET.as_posix(), root=root)
    if sha256(reviewed) != EXPECTED_R18_ORIGINAL_SHA256:
        raise RuntimeError("R18 original Git source was changed")
    if not (root / R18R1_PACKAGE / "patch.py").is_file():
        raise RuntimeError("Previously reviewed R18R1 patch is missing")
    checked_replacement(root=root)
    return {"local_head": local, "remote_head": remote, "source_state": state}


def apply(root: Path = ROOT) -> str:
    state = verify_git_and_source(root=root)["source_state"]
    if state == "R18R2_EVIDENCE_REVALIDATION_INSTALLED":
        if not BACKUP.is_file() or sha256(BACKUP.read_bytes()) != EXPECTED_R18R1_SHA256:
            raise RuntimeError("Prior R18R2 backup is missing or differs")
        return "ALREADY_APPLIED"
    if state != "R18R1_MIXED_EOL_CORRECTED":
        raise RuntimeError("Apply the R18R1 EOL correction first")
    before, after = checked_replacement(root=root)
    if (root / TARGET).read_bytes() != before:
        raise RuntimeError("R18R1 audit source differs from reviewed replacement")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.is_file() and BACKUP.read_bytes() != before:
        raise RuntimeError("Existing R18R2 backup requires review")
    BACKUP.write_bytes(before)
    temporary = (root / TARGET).with_suffix(".r18r2.tmp")
    if temporary.exists():
        raise RuntimeError("R18R2 temporary patch file already exists")
    try:
        temporary.write_bytes(after)
        os.replace(temporary, root / TARGET)
    finally:
        if temporary.exists():
            temporary.unlink()
    if verify_git_and_source(root=root)["source_state"] != "R18R2_EVIDENCE_REVALIDATION_INSTALLED":
        raise RuntimeError("R18R2 final source verification failed")
    return "APPLIED"


def rollback(root: Path = ROOT) -> str:
    state = source_state(root=root)
    if state in ("REVIEWED_R18_ORIGINAL", "R18R1_MIXED_EOL_CORRECTED"):
        return "NO_R18R2_CHANGE"
    if not BACKUP.is_file():
        raise RuntimeError("R18R2 backup missing; manual review required")
    old = BACKUP.read_bytes()
    if sha256(old) != EXPECTED_R18R1_SHA256:
        raise RuntimeError("R18R2 backup differs from reviewed R18R1 version")
    (root / TARGET).write_bytes(old)
    return "RESTORED_R18R1_SOURCE"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--dry-run", action="store_true")
    actions.add_argument("--apply", action="store_true")
    actions.add_argument("--verify", action="store_true")
    actions.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    if args.rollback:
        result = rollback()
    elif args.apply:
        result = apply()
    else:
        state = verify_git_and_source()["source_state"]
        if args.verify and state != "R18R2_EVIDENCE_REVALIDATION_INSTALLED":
            raise RuntimeError("R18R2 replacement not installed")
        result = "PREFLIGHT_" + state if args.dry_run else "VERIFIED_" + state
    print("PHASE174_R3R7R18R2_PATCH=" + result)
    print("PHASE174_R3R7R18R2_TARGET=" + TARGET.as_posix())
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `audit.py` 全文

```python
"""Check the completed R18 gate and truthful, profile-local evidence revalidation."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from phase174_r3_r7_r18r2_local_evidence_recovery.patch import (
    verify_git_and_source,
)

PHASE = "174-R3-R7-R18R2"
EXPECTED_R18_GATE = "PASS_ISOLATED_GENERIC_DELTA_IMAGE_SURJECTIVITY_FRONTIER"
EXPECTED_REPORT = (
    Path("EHPProofTracerAudit") / "phase174_r3_r7_r18" / "delta_image_frontier.json"
)


def verify_public_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R18"
            or report.get("gate") != EXPECTED_R18_GATE
            or report.get("new_group_given") != 0
            or report.get("new_math_rules_in_production") != 0
            or report.get("full_pytest_run") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R18 public mathematical boundary did not pass")
    prior = report.get("prior_evidence")
    live = report.get("live")
    if not isinstance(prior, dict) or not isinstance(live, dict):
        raise RuntimeError("R18 prior evidence or live frontier missing")
    expected_prior = ("174-R3-R7-R17", "174-R3-R7-R17R1")
    if not all(key in prior for key in expected_prior):
        raise RuntimeError("R17 and historical source cannot be silently omitted")
    recovery = prior.get("recovery")
    if recovery is not None:
        if (not isinstance(recovery, dict)
                or recovery.get("mode") != "LIVE_REVALIDATED_NO_SYNTHETIC_REPORT"
                or recovery.get("public_root_candidates") != 1
                or recovery.get("delta_surjectivity_candidates") != 0
                or recovery.get("verified_steps") != 0
                or recovery.get("corrected_historical_test_pinned_by_source_guard") is not True
                or not recovery.get("missing_local_reports")):
            raise RuntimeError("R17 live evidence recovery was not verified")
    if (live.get("public_root_proposals") != 1
            or live.get("public_delta_surjectivity_proposals") != 0
            or live.get("isolated_delta_surjectivity_proposals") != 1
            or live.get("new_proof_steps_created") != 0
            or live.get("completion_claimed") is not False
            or live.get("production_provider_changed") is not False
            or live.get("search_status") == "complete"):
        raise RuntimeError("R18 has lost its unfinished-proof boundary")
    return {
        "phase": PHASE,
        "r18_gate": report["gate"],
        "evidence_mode": "LIVE_RECOVERY" if recovery is not None else "VALIDATED_LOCAL_REPORTS",
        "missing_local_r17_reports": recovery.get("missing_local_reports", []) if recovery is not None else [],
        "public_root_candidates": live["public_root_proposals"],
        "public_delta_surjectivity_candidates": live["public_delta_surjectivity_proposals"],
        "isolated_delta_surjectivity_candidates": live["isolated_delta_surjectivity_proposals"],
        "root_complete": False,
        "new_group_given": 0,
        "new_production_rules": 0,
        "full_pytest_run": False,
        "gate": "PASS_R18_LIVE_R17_BOUNDARY_REVALIDATED_NO_PRIOR_JSON_COPY",
    }


def audit_path() -> Path:
    local = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return local / EXPECTED_REPORT


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    state = verify_git_and_source()
    if state["source_state"] != "R18R2_EVIDENCE_REVALIDATION_INSTALLED":
        raise RuntimeError("R18R2 source correction is not installed")
    report_file = audit_path()
    if not report_file.is_file():
        raise RuntimeError("R18 final live report is missing: " + str(report_file))
    report = json.loads(report_file.read_text(encoding="utf-8-sig"))
    verified = verify_public_report(report)
    print("PHASE174_R3R7R18R2_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R18R2_EVIDENCE_MODE=" + verified["evidence_mode"])
    print("PHASE174_R3R7R18R2_PUBLIC_ROOT_CANDIDATES=" + str(verified["public_root_candidates"]))
    print("PHASE174_R3R7R18R2_PUBLIC_DELTA_CANDIDATES=" + str(verified["public_delta_surjectivity_candidates"]))
    print("PHASE174_R3R7R18R2_ISOLATED_DELTA_CANDIDATES=" + str(verified["isolated_delta_surjectivity_candidates"]))
    print("PHASE174_R3R7R18R2_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R7R18R2_NEW_PRODUCTION_RULES=0")
    print("PHASE174_R3R7R18R2_FULL_PYTEST=False")
    print("PHASE174_R3R7R18R2_ROOT_COMPLETE=False")
    print("PHASE174_R3R7R18R2_GATE=" + verified["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/__init__.py` 全文

```python
"""R18R2 focused contract tests."""
```

## `tests/test_evidence.py` 全文

```python
"""Fail-closed tests for missing, present and invalid profile-local R17 records."""
from __future__ import annotations

import ast
import json
import os
import sys
import tempfile
import types
from pathlib import Path
from typing import Any

import pytest

from phase174_r3_r7_r18r2_local_evidence_recovery.patch import (
    EXPECTED_R18R1_SHA256,
    EXPECTED_R18R2_SHA256,
    REPLACEMENT_FUNCTION,
    checked_replacement,
    sha256,
    transform,
)


def _load_validator(monkeypatch: pytest.MonkeyPatch, local: Path, live: dict[str, Any]):
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    fake_parent = types.ModuleType("phase174_r3_r7_r17_typed_map_open_goal")
    fake_parent.__path__ = []
    fake = types.ModuleType("phase174_r3_r7_r17_typed_map_open_goal.audit")
    fake.inspect_public_map_display = lambda: dict(live)
    monkeypatch.setitem(sys.modules, "phase174_r3_r7_r17_typed_map_open_goal", fake_parent)
    monkeypatch.setitem(sys.modules, "phase174_r3_r7_r17_typed_map_open_goal.audit", fake)
    source = REPLACEMENT_FUNCTION.read_text(encoding="utf-8")
    context = {"Any": Any, "Path": Path, "json": json,
               "os": os, "tempfile": tempfile}
    exec(compile(source, "validate_prior_r17.py", "exec"), context)
    return context["validate_prior_r17"]


def _valid_live() -> dict[str, Any]:
    return {
        "public_root_candidates": 1,
        "public_delta_surjectivity_candidates": 0,
        "generic_isomorphism_depends_on_surjectivity": True,
        "direct_given_for_goal_or_delta": False,
        "delta_latex": r"\Delta: \pi_{13}^{13} \twoheadrightarrow \pi_{11}^{6}",
        "search_status": "search_failed",
        "proven_steps": 0,
        "completion_claimed": False,
    }


def _write_report(local: Path, index: int, *, gate: str | None = None) -> None:
    options = (
        ("phase174_r3_r7_r17/typed_map_public_audit.json", "174-R3-R7-R17",
         "PASS_TYPED_DELTA_OPEN_GOAL_SURJECTIVITY_STILL_PENDING"),
        ("phase174_r3_r7_r17r1/historical_contract_audit.json", "174-R3-R7-R17R1",
         "PASS_HISTORICAL_TEST_CONTRACT_CORRECTED_R17_PUBLIC_UNCHANGED"),
    )
    relative, phase, expected_gate = options[index]
    path = local / "EHPProofTracerAudit" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "phase": phase, "gate": expected_gate if gate is None else gate,
        "new_group_given": 0, "full_pytest_run": False,
    }), encoding="utf-8")


def test_exact_function_replacement_changes_no_other_definitions() -> None:
    base, patched = checked_replacement(root=Path(__file__).resolve().parents[2])
    assert sha256(base) == EXPECTED_R18R1_SHA256
    assert sha256(patched) == EXPECTED_R18R2_SHA256
    old_tree = ast.parse(base.decode("utf-8"))
    new_tree = ast.parse(patched.decode("utf-8"))
    for node in old_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "validate_prior_r17":
            old_tree.body.remove(node)
            break
    for node in new_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "validate_prior_r17":
            new_tree.body.remove(node)
            break
    assert ast.dump(old_tree, include_attributes=False) == ast.dump(new_tree, include_attributes=False)


def test_missing_reports_recheck_live_without_creating_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = _load_validator(monkeypatch, tmp_path, _valid_live())
    result = validator()
    assert result["recovery"]["mode"] == "LIVE_REVALIDATED_NO_SYNTHETIC_REPORT"
    assert len(result["recovery"]["missing_local_reports"]) == 2
    assert "LIVE_PUBLIC_BOUNDARY_REVALIDATED" in result["174-R3-R7-R17"]
    assert "CORRECTED_TEST_SOURCE_PINNED" in result["174-R3-R7-R17R1"]
    assert not tuple(tmp_path.rglob("*.json"))


def test_both_valid_reports_no_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _write_report(tmp_path, 0)
    _write_report(tmp_path, 1)
    validator = _load_validator(monkeypatch, tmp_path, _valid_live())
    result = validator()
    assert "recovery" not in result
    assert result["174-R3-R7-R17"].startswith("PASS_")
    assert result["174-R3-R7-R17R1"].startswith("PASS_")


def test_only_one_missing_report_rechecks_public_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_report(tmp_path, 0)
    validator = _load_validator(monkeypatch, tmp_path, _valid_live())
    result = validator()
    assert result["174-R3-R7-R17"].startswith("PASS_")
    assert len(result["recovery"]["missing_local_reports"]) == 1


@pytest.mark.parametrize("key,value", (
    ("public_root_candidates", 0),
    ("public_delta_surjectivity_candidates", 1),
    ("generic_isomorphism_depends_on_surjectivity", False),
    ("direct_given_for_goal_or_delta", True),
    ("search_status", "complete"),
    ("proven_steps", 1),
    ("completion_claimed", True),
    ("delta_latex", "unrecognized"),
))
def test_bad_live_frontier_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, key: str, value: object,
) -> None:
    live = _valid_live()
    live[key] = value
    validator = _load_validator(monkeypatch, tmp_path, live)
    with pytest.raises(RuntimeError, match="Live R17 proof boundary"):
        validator()


def test_existing_bad_report_is_never_silently_recovered(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_report(tmp_path, 0, gate="FORGED_PASS")
    validator = _load_validator(monkeypatch, tmp_path, _valid_live())
    with pytest.raises(RuntimeError, match="Prior R17 evidence inconsistent"):
        validator()


def test_duplicate_or_missing_function_anchor_fails_closed() -> None:
    new = REPLACEMENT_FUNCTION.read_text(encoding="utf-8")
    with pytest.raises(RuntimeError):
        transform(b"def other():\n    pass\n", new)
    with pytest.raises(RuntimeError):
        transform(b"def validate_prior_r17() -> dict[str, Any]:\n    pass\n", new)
```

## `tests/test_audit.py` 全文

```python
"""Final report acceptance requires live R18, including unresolved public Delta."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase174_r3_r7_r18r2_local_evidence_recovery.audit import verify_public_report


def _report() -> dict:
    return {
        "phase": "174-R3-R7-R18",
        "gate": "PASS_ISOLATED_GENERIC_DELTA_IMAGE_SURJECTIVITY_FRONTIER",
        "new_group_given": 0,
        "new_math_rules_in_production": 0,
        "full_pytest_run": False,
        "completion_claimed": False,
        "prior_evidence": {
            "174-R3-R7-R17": "LIVE_PUBLIC_BOUNDARY_REVALIDATED_NO_LOCAL_REPORT",
            "174-R3-R7-R17R1": "CORRECTED_TEST_SOURCE_PINNED_NO_LOCAL_REPORT",
            "recovery": {
                "mode": "LIVE_REVALIDATED_NO_SYNTHETIC_REPORT",
                "missing_local_reports": ["phase174_r3_r7_r17/typed_map_public_audit.json"],
                "public_root_candidates": 1,
                "delta_surjectivity_candidates": 0,
                "verified_steps": 0,
                "corrected_historical_test_pinned_by_source_guard": True,
            },
        },
        "live": {
            "public_root_proposals": 1,
            "public_delta_surjectivity_proposals": 0,
            "isolated_delta_surjectivity_proposals": 1,
            "new_proof_steps_created": 0,
            "completion_claimed": False,
            "production_provider_changed": False,
            "search_status": "search_failed",
        },
    }


def test_live_revalidation_gate_accepts_unfinished_frontier() -> None:
    result = verify_public_report(_report())
    assert result["gate"] == "PASS_R18_LIVE_R17_BOUNDARY_REVALIDATED_NO_PRIOR_JSON_COPY"
    assert result["evidence_mode"] == "LIVE_RECOVERY"
    assert result["root_complete"] is False


def test_existing_valid_report_mode_is_distinguished() -> None:
    data = _report()
    del data["prior_evidence"]["recovery"]
    assert verify_public_report(data)["evidence_mode"] == "VALIDATED_LOCAL_REPORTS"


@pytest.mark.parametrize("path,value", (
    (("gate",), "UNVERIFIED"),
    (("new_group_given",), 1),
    (("new_math_rules_in_production",), 1),
    (("full_pytest_run",), True),
    (("completion_claimed",), True),
    (("live", "public_delta_surjectivity_proposals"), 1),
    (("live", "public_root_proposals"), 0),
    (("live", "isolated_delta_surjectivity_proposals"), 0),
    (("live", "new_proof_steps_created"), 1),
    (("live", "search_status"), "complete"),
    (("prior_evidence", "recovery", "verified_steps"), 1),
    (("prior_evidence", "recovery", "mode"), "SKIP_VALIDATION"),
))
def test_broken_post_report_is_rejected(path: tuple[str, ...], value: object) -> None:
    data = deepcopy(_report())
    node = data
    for field in path[:-1]:
        node = node[field]
    node[path[-1]] = value
    with pytest.raises(RuntimeError):
        verify_public_report(data)
```

## `run.ps1` 全文

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$SavedPythonPath = $env:PYTHONPATH
$SavedNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$R18R1Attempted = $false
$R18R2Attempted = $false

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R18R2 git fetch failed' }

    $Preflight = @(& python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.patch --dry-run)
    if ($LASTEXITCODE -ne 0) { throw 'R18R2 guarded preflight failed' }
    $Preflight | Write-Output
    $StatusLine = @($Preflight | Where-Object { $_ -like 'PHASE174_R3R7R18R2_PATCH=PREFLIGHT_*' })
    if ($StatusLine.Count -ne 1) { throw 'R18R2 preflight state missing' }
    $InitialState = $StatusLine[0].Substring('PHASE174_R3R7R18R2_PATCH=PREFLIGHT_'.Length)

    if ($InitialState -eq 'REVIEWED_R18_ORIGINAL') {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R18R1 reviewed EOL preflight failed' }
    }
    elseif ($InitialState -eq 'R18R1_MIXED_EOL_CORRECTED') {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --verify
        if ($LASTEXITCODE -ne 0) { throw 'Existing R18R1 state failed verification' }
    }
    elseif ($InitialState -ne 'R18R2_EVIDENCE_REVALIDATION_INSTALLED') {
        throw 'Unsupported R18R2 source state'
    }

    Write-Output 'PHASE174_R3R7R18R2_PYTEST_GROUP=RECOVERY_CONTRACT'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
        '.\phase174_r3_r7_r18r2_local_evidence_recovery\tests\test_evidence.py' `
        '.\phase174_r3_r7_r18r2_local_evidence_recovery\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R18R2 recovery contract pytest failed' }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R18R2_GATE=PASS_PREFLIGHT_LOCAL_EVIDENCE_REVALIDATION'
    }
    else {
        if ($InitialState -eq 'REVIEWED_R18_ORIGINAL') {
            $R18R1Attempted = $true
            & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --apply
            if ($LASTEXITCODE -ne 0) { throw 'R18R1 EOL source correction failed' }
        }
        if ($InitialState -ne 'R18R2_EVIDENCE_REVALIDATION_INSTALLED') {
            $R18R2Attempted = $true
            & python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.patch --apply
            if ($LASTEXITCODE -ne 0) { throw 'R18R2 evidence recovery patch failed' }
        }
        & python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.patch --verify
        if ($LASTEXITCODE -ne 0) { throw 'R18R2 source verification failed' }

        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase174_r3_r7_r18_delta_image_surjectivity\run.ps1' -DryRun
        if ($LASTEXITCODE -ne 0) { throw 'R18 revalidated DryRun failed' }

        & powershell -NoProfile -ExecutionPolicy Bypass `
            -File '.\phase174_r3_r7_r18_delta_image_surjectivity\run.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'R18 live public audit failed' }

        Write-Output 'PHASE174_R3R7R18R2_PYTEST_GROUP=HISTORICAL_DISPLAY_CORRECTED'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase173_r4_r15r17r3r3_typed_goal_display\tests\test_open_goals.py'
        if ($LASTEXITCODE -ne 0) { throw 'Corrected historical display regression failed' }

        & python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.audit
        if ($LASTEXITCODE -ne 0) { throw 'R18R2 final public evidence verification failed' }
    }
    Write-Output '(END)'
}
catch {
    $Failure = $_
    if ($R18R2Attempted) {
        & python -B -m phase174_r3_r7_r18r2_local_evidence_recovery.patch --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Output 'PHASE174_R3R7R18R2_ROLLBACK=FAILED_MANUAL_REVIEW_REQUIRED'
        }
    }
    if ($R18R1Attempted) {
        & python -B -m phase174_r3_r7_r18r1_git_mixed_eol_guard.patch --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Output 'PHASE174_R3R7R18R1_ROLLBACK=FAILED_MANUAL_REVIEW_REQUIRED'
        }
    }
    throw $Failure
}
finally {
    $env:PYTHONPATH = $SavedPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $SavedNoBytecode
    Pop-Location
}
```

