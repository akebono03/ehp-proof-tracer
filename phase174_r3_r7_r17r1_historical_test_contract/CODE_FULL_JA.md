# Phase 174 R3-R7-R17R1 — 新規コード・変更関数の全文

## 対象ファイル・関数

変更する既存テストは `phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py`。既存関数 `test_real_typed_pending_goals_are_grouped_only_in_public_display` のデコレータと新規関数 `test_pi8_5_completed_case_is_not_reported_as_an_open_goal` を変更・追加します。新規関数はその既存テスト関数の**直後**に挿入します。

R17 が未適用の `web_group_proof_common._group_proof_statement_latex` を、そのまま R17 の既存 guarded patch で適用します。R17R1 は元の R17 数式表示関数を変更せず、R17 本来のコード全文は `phase174_r3_r7_r17_typed_map_open_goal/MODIFIED_FUNCTION_FULL_JA.md` に出力されます。

### 既存テストの import ブロック全文（変更なし）

```python
"""Real typed pending goals and public Narrative across status boundaries."""
from __future__ import annotations

import pytest

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import (
    project_typed_open_goal_displays,
    render_model_backed_narrative_markdown,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from proof import Relation, RelationType
from web_group_proof import build_standard_web_group_proof_view

```

### 変更後の既存テスト関数全文

```python
@pytest.mark.parametrize('n,k,expected', ((4, 8, 3), (4, 9, 2)))
def test_real_typed_pending_goals_are_grouped_only_in_public_display(
    n: int, k: int, expected: int,
) -> None:
    typed = exact_prior_database_result(n, k)
    assert typed is not None
    result = search_group_from_registered_goal(n=n, k=k, goal=typed)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    original = result.open_goals
    assert len(original) == expected
    model = build_proof_narrative_model(result)
    assert model.open_goals == original
    groups = project_typed_open_goal_displays(original)
    assert len(groups) == 1
    assert groups[0][0] is original[0]
    assert groups[0][1] == expected
    markdown = render_model_backed_narrative_markdown(result, model)
    block = markdown.split('## 未解決 Goal', 1)[1].split('## 探索診断', 1)[0]
    goal_lines = [line for line in block.splitlines() if line.startswith('- ')]
    assert len(goal_lines) == 1
    assert f'未解決 Goal {expected} 件' in goal_lines[0]
    assert result.open_goals == original
    assert model.open_goals == original
    assert result.conclusion is None
    assert len(model.steps) >= len(result.proven_steps)
    view = build_standard_web_group_proof_view(
        n=n, k=k, goal=typed, mode='narrative', citation_source='model',
    )
    assert view.partial_result
    assert view.key == 'generic-partial-proof'
    assert any(line.kind == 'heading' and line.prefix == '未解決 Goal'
               for line in view.rendered_lines)

```

### 追加するテスト関数全文

```python
def test_pi8_5_completed_case_is_not_reported_as_an_open_goal() -> None:
    """The formerly partial (n=5,k=3) case must retain its completed proof."""
    typed = exact_prior_database_result(5, 3)
    assert typed is not None
    result = search_group_from_registered_goal(n=5, k=3, goal=typed)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == typed
    assert result.open_goals == ()
    assert any(step.conclusion == typed for step in result.proven_steps)
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    assert model.root_index is not None
    assert project_typed_open_goal_displays(result.open_goals) == ()
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "## 未解決 Goal" not in markdown
    view = build_standard_web_group_proof_view(
        n=5, k=3, goal=typed, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert not any(line.kind == "heading" and line.prefix == "未解決 Goal"
                   for line in view.rendered_lines)
```

## 新規ファイル `patch.py` 全文

```python
"""R17R1: exact historical test-contract correction; never touch production proof logic."""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py")
EXPECTED_BLOB = "b085e0c93878d08245beed6d675cf4531f139234"
BACKUP = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) /
          "EHPProofTracerAudit" / "phase174_r3_r7_r17r1" / "test_open_goals.original.py")
OLD_PARAMS = "@pytest.mark.parametrize('n,k,expected', ((4, 8, 3), (4, 9, 2), (5, 3, 3)))"
NEW_PARAMS = "@pytest.mark.parametrize('n,k,expected', ((4, 8, 3), (4, 9, 2)))"
NEXT_FUNCTION = "\n\ndef test_same_latex_is_not_sufficient_to_merge_distinct_typed_structures() -> None:\n"
NEW_TEST = '''\n\ndef test_pi8_5_completed_case_is_not_reported_as_an_open_goal() -> None:
    """The formerly partial (n=5,k=3) case must retain its completed proof."""
    typed = exact_prior_database_result(5, 3)
    assert typed is not None
    result = search_group_from_registered_goal(n=5, k=3, goal=typed)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == typed
    assert result.open_goals == ()
    assert any(step.conclusion == typed for step in result.proven_steps)
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    assert model.root_index is not None
    assert project_typed_open_goal_displays(result.open_goals) == ()
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "## 未解決 Goal" not in markdown
    view = build_standard_web_group_proof_view(
        n=5, k=3, goal=typed, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert not any(line.kind == "heading" and line.prefix == "未解決 Goal"
                   for line in view.rendered_lines)
'''


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def normalized(raw: bytes) -> tuple[str, bytes]:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected BOM")
    remains = raw.replace(b"\r\n", b"")
    if b"\r" in remains or (b"\r\n" in raw and b"\n" in remains):
        raise RuntimeError("Mixed or malformed EOL")
    return raw.replace(b"\r\n", b"\n").decode("utf-8"), (b"\r\n" if b"\r\n" in raw else b"\n")


def original_matches(raw: bytes) -> bool:
    try:
        source, _ = normalized(raw)
    except (UnicodeError, RuntimeError):
        return False
    lf = source.encode("utf-8")
    return any(blob_sha(v) == EXPECTED_BLOB for v in (raw, lf, lf.replace(b"\n", b"\r\n")))


def transform(source: str) -> str:
    """Replace a stale parametrization and add a real completed-case test."""
    before = ast.parse(source)
    functions = [x.name for x in before.body if isinstance(x, ast.FunctionDef)]
    if (source.count(OLD_PARAMS) != 1 or source.count(NEXT_FUNCTION) != 1
            or NEW_PARAMS in source or "test_pi8_5_completed_case_is_not_reported_as_an_open_goal" in source
            or functions.count("test_real_typed_pending_goals_are_grouped_only_in_public_display") != 1):
        raise RuntimeError("Reviewed historical test anchors changed or already patched")
    out = source.replace(OLD_PARAMS, NEW_PARAMS, 1).replace(
        NEXT_FUNCTION, NEW_TEST + NEXT_FUNCTION, 1,
    )
    new_functions = [x.name for x in ast.parse(out).body if isinstance(x, ast.FunctionDef)]
    added = [x for x in new_functions if x not in functions]
    if (added != ["test_pi8_5_completed_case_is_not_reported_as_an_open_goal"]
            or len(new_functions) != len(functions) + 1):
        raise RuntimeError("Unexpected test functions changed")
    compile(out, str(TARGET), "exec")
    return out


def patched_bytes(original: bytes) -> bytes:
    if not original_matches(original):
        raise RuntimeError("Historical test source does not match reviewed GitHub blob")
    source, eol = normalized(original)
    return transform(source).encode("utf-8").replace(b"\n", eol)


def run(*, mode: str, root: Path = ROOT) -> str:
    target = root / TARGET
    if not target.is_file():
        raise RuntimeError("Historical typed Goal test is missing")
    if mode in ("dry-run", "apply"):
        original = target.read_bytes()
        expected = patched_bytes(original)
        if mode == "dry-run":
            return "PASS_PREFLIGHT"
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        if BACKUP.is_file() and BACKUP.read_bytes() != original:
            raise RuntimeError("Conflicting backup; do not overwrite")
        BACKUP.write_bytes(original)
        target.write_bytes(expected)
        if target.read_bytes() != expected:
            target.write_bytes(original)
            raise RuntimeError("Historical test write verification failed")
        return "PASS_APPLIED"
    if mode == "rollback":
        if not BACKUP.is_file():
            return "NO_BACKUP"
        original = BACKUP.read_bytes()
        candidate = patched_bytes(original)
        current = target.read_bytes()
        if current == original:
            return "ALREADY_ORIGINAL"
        if current != candidate:
            raise RuntimeError("Refusing rollback of unreviewed file content")
        target.write_bytes(original)
        return "RESTORED"
    raise ValueError("Unknown mode")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--dry-run", action="store_true")
    modes.add_argument("--apply", action="store_true")
    modes.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    mode = "dry-run" if args.dry_run else "apply" if args.apply else "rollback"
    print("PHASE174_R3R7R17R1_TEST_PATCH=" + run(mode=mode))
    print("PHASE174_R3R7R17R1_TEST_PATH=" + str(TARGET))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規ファイル `audit.py` 全文

```python
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
    expected_changed = tuple(sorted((str(TEST_TARGET), str(DISPLAY_TARGET)))) if applied else ()
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
```

## 新規ファイル `rollback.py` 全文

```python
"""Restore only the exact reviewed R17 formatter patch after a failed R17R1 run."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from phase174_r3_r7_r17_typed_map_open_goal.patch import (
    EXPECTED_BLOB, TARGET, expected_patched_bytes, matches_git_blob,
    normalize_and_style,
)

ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r17" / "web_group_proof_common.original.py"


def main() -> int:
    if not BACKUP.is_file():
        print("PHASE174_R3R7R17R1_FORMATTER_ROLLBACK=NO_BACKUP")
        return 0
    original = BACKUP.read_bytes()
    if not matches_git_blob(original, EXPECTED_BLOB):
        raise RuntimeError("R17 formatter backup not equal to reviewed source")
    live = ROOT / TARGET
    current = live.read_bytes()
    text, _ = normalize_and_style(current)
    old_text, _ = normalize_and_style(original)
    patched_text, _ = normalize_and_style(expected_patched_bytes(original))
    if text == old_text:
        print("PHASE174_R3R7R17R1_FORMATTER_ROLLBACK=ALREADY_ORIGINAL")
        return 0
    if text != patched_text:
        raise RuntimeError("Refusing to overwrite an unreviewed formatter")
    live.write_bytes(original)
    print("PHASE174_R3R7R17R1_FORMATTER_ROLLBACK=RESTORED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規ファイル `tests/test_patch.py` 全文

```python
"""Tests must never manufacture a mathematical proof or weaken the regression gate."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r7_r17r1_historical_test_contract.patch import (
    NEW_PARAMS, NEW_TEST, OLD_PARAMS, NEXT_FUNCTION, transform,
)


def fixture() -> str:
    return (
        '"""Sample module."""\nimport pytest\n\n' + OLD_PARAMS + '\n'
        'def test_real_typed_pending_goals_are_grouped_only_in_public_display(n, k, expected):\n'
        '    assert n == n\n'
        + NEXT_FUNCTION + '    assert True\n'
    )


def test_only_historical_parameter_expectation_changes() -> None:
    original = fixture()
    corrected = transform(original)
    ast.parse(corrected)
    assert OLD_PARAMS not in corrected
    assert corrected.count(NEW_PARAMS) == 1
    assert corrected.count("def test_pi8_5_completed_case_is_not_reported_as_an_open_goal") == 1
    assert "assert result.status is ProofSearchStatus.COMPLETE" in corrected
    assert "assert result.open_goals == ()" in corrected
    assert "assert view.key == \"generic-complete-proof\"" in corrected
    assert corrected.count("def test_real_typed_pending_goals_are_grouped_only_in_public_display") == 1
    assert NEW_TEST in corrected


def test_no_repeat_or_unreviewed_changes() -> None:
    corrected = transform(fixture())
    with pytest.raises(RuntimeError):
        transform(corrected)
    with pytest.raises(RuntimeError):
        transform(fixture().replace(OLD_PARAMS, OLD_PARAMS + "\n" + OLD_PARAMS))
    with pytest.raises(RuntimeError):
        transform(fixture().replace(NEXT_FUNCTION, "\n\ndef test_different() -> None:\n"))


def test_new_complete_case_is_not_a_skipped_regression() -> None:
    assert "@pytest.mark.skip" not in NEW_TEST
    assert "pytest.xfail" not in NEW_TEST
    assert "5, k=3" in NEW_TEST
    assert "build_standard_web_group_proof_view" in NEW_TEST
    assert "project_typed_open_goal_displays" in NEW_TEST
```

## 新規ファイル `run.ps1` 全文

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$AttemptedWebPatch = $false
$AttemptedTestPatch = $false

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R17R1 Git fetch failed' }

    # All source gates run before any tracked file is modified.
    & python -B -m phase174_r3_r7_r17r1_historical_test_contract.audit
    if ($LASTEXITCODE -ne 0) { throw 'R17R1 source guard failed' }
    & python -B -m phase174_r3_r7_r17r1_historical_test_contract.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Historical contract patch preflight failed' }
    & python -B -m phase174_r3_r7_r17_typed_map_open_goal.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Original R17 source guard failed' }
    & python -B -m phase174_r3_r7_r17_typed_map_open_goal.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Original R17 formatter patch preflight failed' }

    # Targeted tests only: the obsolete historical parametrization is fixed
    # in this package after the original R17 audit, not silently skipped.
    $Groups = @(
        @{ Name = 'R17R1_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r17r1_historical_test_contract\tests\test_patch.py'
        ) },
        @{ Name = 'R17_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_patch.py',
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_audit.py'
        ) },
        @{ Name = 'R16_ROOT'; Paths = @(
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_public.py'
        ) },
        @{ Name = 'R3_EHP_RULE'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Missing reviewed test: $TestPath"
            }
        }
        Write-Output "PHASE174_R3R7R17R1_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "R17R1 focused pytest failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R17R1_PREFLIGHT_PYTEST=PASS'

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R17R1_STALE_HISTORICAL_CASE=DOCUMENTED_NOT_EXECUTED_BEFORE_CORRECTION'
        Write-Output 'PHASE174_R3R7R17R1_GATE=PASS_PREFLIGHT'
    }
    else {
        # 1. Complete the originally intended R17 formatting patch while its
        # original strict source guard still sees an unchanged historical test.
        $AttemptedWebPatch = $true
        & python -B -m phase174_r3_r7_r17_typed_map_open_goal.patch
        if ($LASTEXITCODE -ne 0) { throw 'R17 original formatting patch failed' }
        Write-Output 'PHASE174_R3R7R17R1_PYTEST_GROUP=R17_PUBLIC'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'Original R17 public display test failed' }
        & python -B -m phase174_r3_r7_r17_typed_map_open_goal.audit
        if ($LASTEXITCODE -ne 0) { throw 'Original R17 public audit failed' }

        # 2. Update the obsolete Phase 173 test contract. Never skip the
        # completed pi_8^5 case: it now has an explicit completed-proof test.
        $AttemptedTestPatch = $true
        & python -B -m phase174_r3_r7_r17r1_historical_test_contract.patch --apply
        if ($LASTEXITCODE -ne 0) { throw 'R17R1 historical test correction failed' }
        Write-Output 'PHASE174_R3R7R17R1_PYTEST_GROUP=PHASE173_TYPED_DISPLAY_CORRECTED'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase173_r4_r15r17r3r3_typed_goal_display\tests\test_open_goals.py'
        if ($LASTEXITCODE -ne 0) { throw 'Corrected historical typed display tests failed' }
        & python -B -m phase174_r3_r7_r17r1_historical_test_contract.audit --applied
        if ($LASTEXITCODE -ne 0) { throw 'R17R1 final source-first gate failed' }
    }
    Write-Output '(END)'
}
catch {
    $Failure = $_.ToString()
    if ($AttemptedTestPatch) {
        & python -B -m phase174_r3_r7_r17r1_historical_test_contract.patch --rollback
        if ($LASTEXITCODE -ne 0) { Write-Warning 'Historical test rollback needs manual review' }
    }
    if ($AttemptedWebPatch) {
        & python -B -m phase174_r3_r7_r17r1_historical_test_contract.rollback
        if ($LASTEXITCODE -ne 0) { Write-Warning 'Common formatter rollback needs manual review' }
    }
    throw $Failure
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
```
