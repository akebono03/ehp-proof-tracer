# R16 新規コード全文と既存関数の出力方法

既存の `shared_expansion_provider` 全文は DryRun 時に現行 Git HEAD を検証し、`MODIFIED_FUNCTION_FULL_JA.md` へ AST から全文出力する。出典未確認の推測コードをこのファイルに重複保存しない。

## `patch.py`

```python
"""Guarded one-function Phase 174 R3-R7-R16 public EHP root connection.

The existing generic zero-group inference is only proposed. This patch does not
register any GIVEN, discharge premises, or change any proof renderer.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase165_r52_r9_shared_math.py")
BASE_BLOB = "7f81769776278b46a220fb90771970a9dd7c73c2"
PACKAGE = ROOT / "phase174_r3_r7_r16_public_ehp_zero_root"
BACKUP_DIR = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r16"
BACKUP = BACKUP_DIR / "phase165_r52_r9_shared_math.original.py"

OLD = (
    "        options = []\n"
    "        from phase166_r3q_hopf_image_relation import expand_hopf_image_relation\n"
)
NEW = (
    "        options = []\n"
    "        from phase174_r3_r7_r3_ehp_zero_rule.rule import (\n"
    "            expand_ehp_zero_from_delta_surjectivity,\n"
    "        )\n"
    "        options.extend(expand_ehp_zero_from_delta_surjectivity(goal))\n"
    "        from phase166_r3q_hopf_image_relation import expand_hopf_image_relation\n"
)


def blob_sha(value: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(value)).encode("ascii") + b"\0" + value).hexdigest()


def normalize_and_style(value: bytes) -> tuple[str, bytes]:
    """Preserve uniform checkout EOL; reject BOM, bare-CR, mixed EOL."""
    if value.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected BOM in tracked production source")
    rest = value.replace(b"\r\n", b"")
    if b"\r" in rest or (b"\r\n" in value and b"\n" in rest):
        raise RuntimeError("Mixed or malformed tracked production line endings")
    eol = b"\r\n" if b"\r\n" in value else b"\n"
    return value.replace(b"\r\n", b"\n").decode("utf-8"), eol


def transform_source(source: str) -> str:
    """Replace one exact anchor inside the already reviewed shared provider."""
    if source.count(OLD) != 1 or NEW in source:
        raise RuntimeError("R16 requires one unmodified shared-provider anchor")
    before = ast.parse(source)
    before_function = next((x for x in before.body
                            if isinstance(x, ast.FunctionDef) and x.name == "shared_expansion_provider"), None)
    if before_function is None or not any(isinstance(x, ast.FunctionDef) and x.name == "expand"
                                           for x in ast.walk(before_function)):
        raise RuntimeError("Expected shared expand function not found")
    result = source.replace(OLD, NEW, 1)
    after = ast.parse(result)
    before_names = [x.name for x in before.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))]
    after_names = [x.name for x in after.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))]
    if before_names != after_names:
        raise RuntimeError("Unexpected public API change")
    compile(result, str(TARGET), "exec")
    return result


def patched_bytes(original: bytes) -> bytes:
    source, style = normalize_and_style(original)
    if blob_sha(source.encode("utf-8")) != BASE_BLOB and blob_sha(original) != BASE_BLOB:
        raise RuntimeError("Pinned R15 production source differs")
    return transform_source(source).encode("utf-8").replace(b"\n", style)


def expected_from_head(root: Path = ROOT) -> tuple[bytes, bytes]:
    """Read the tracked source only; never trust an unreviewed working tree."""
    import subprocess
    result = subprocess.run(
        ["git", "show", "HEAD:" + TARGET.as_posix()],
        cwd=root, check=True, capture_output=True,
    )
    original = result.stdout
    patched = patched_bytes(original)
    local = (root / TARGET).read_bytes()
    local_normalized, local_eol = normalize_and_style(local)
    head_normalized, _ = normalize_and_style(original)
    if local_normalized != head_normalized:
        raise RuntimeError("Local tracked file differs from reviewed HEAD")
    return local, transform_source(local_normalized).encode("utf-8").replace(b"\n", local_eol)


def export_complete_function(source: str, path: Path) -> None:
    """Emit the entire replacement function, never a short line-level diff."""
    tree = ast.parse(source)
    names = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "shared_expansion_provider"]
    if len(names) != 1:
        raise RuntimeError("Expected one shared_expansion_provider")
    node = names[0]
    lines = source.splitlines()
    body = "\n".join(lines[node.lineno - 1:node.end_lineno])
    path.write_text(
        "# R16 変更後の関数全文\n\n"
        "変更対象: `phase165_r52_r9_shared_math.py` → "
        "`shared_expansion_provider`（内部の `expand` を含む）。\n\n"
        "import はファイル先頭で変更なし。\n\n"
        "```python\n" + body + "\n```\n",
        encoding="utf-8",
    )


def guarded_apply(*, dry_run: bool, root: Path = ROOT) -> dict[str, str]:
    original, expected = expected_from_head(root)
    output_source, _ = normalize_and_style(expected)
    output = root / "phase174_r3_r7_r16_public_ehp_zero_root" / "MODIFIED_FUNCTION_FULL_JA.md"
    export_complete_function(output_source, output)
    info = {
        "before_sha": blob_sha(normalize_and_style(original)[0].encode("utf-8")),
        "after_sha": blob_sha(output_source.encode("utf-8")),
        "full_function_file": str(output),
    }
    if dry_run:
        return info
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() and BACKUP.read_bytes() != original:
        raise RuntimeError("A conflicting prior R16 backup exists; manual review needed")
    BACKUP.write_bytes(original)
    path = root / TARGET
    path.write_bytes(expected)
    if path.read_bytes() != expected:
        path.write_bytes(original)
        raise RuntimeError("R16 write verification failed")
    info["backup"] = str(BACKUP)
    return info


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    info = guarded_apply(dry_run=args.dry_run)
    for key, value in info.items():
        print("PHASE174_R3R7R16_PATCH_" + key.upper() + "=" + value)
    print("PHASE174_R3R7R16_PATCH_GATE=" + ("PASS_PREFLIGHT" if args.dry_run else "PASS_APPLIED"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `audit.py`

```python
"""Phase 174 R3-R7-R16: source-guarded public EHP zero-root integration.

The root becomes an unproved backward candidate with four independent goals.
Neither an isolated proposal nor a displayed open goal is a certified proof.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from phase174_r3_r7_r16_public_ehp_zero_root.patch import (
    BASE_BLOB, TARGET, blob_sha, normalize_and_style, transform_source,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R16"
PRE_R15_HEAD = "380a5b17414075e7ec5ebbb17c310e8dad49fa60"
REVIEWED_HEAD = "e7bcd34a526b3f885a8e3be81c4aac362d8834c7"
R15_PREFIX = "phase174_r3_r7_r15_chain_frontier_audit/"
PINS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py": "54ae4d4430c99895e0687ea8c56fd711284465f1",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase174_r3_r7_r15_chain_frontier_audit/audit.py": "64256bb7b3fda9dc2ad12f78e2bef92df01ce27d",
    "phase174_r3_r7_r14_public_annihilator_connection/tests/test_public.py": "a5a798b5c7b7ae148c45db5ffc3be86654fdf69b",
}


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
    ).stdout


def matches_blob(source: bytes, expected: str) -> bool:
    if len(expected) != 40 or any(ch not in "0123456789abcdef" for ch in expected):
        return False
    try:
        normalized, _ = normalize_and_style(source)
    except (RuntimeError, UnicodeError):
        return False
    text_bytes = normalized.encode("utf-8")
    return any(blob_sha(x) == expected for x in (
        source, text_bytes, text_bytes.replace(b"\n", b"\r\n"),
    ))


def validate_lineage(local: str, remote: str, paths: tuple[str, ...],
                     modified: tuple[str, ...], patched: bool) -> str:
    if remote != REVIEWED_HEAD or local not in (PRE_R15_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Unreviewed GitHub/local develop HEAD; refuse modification")
    if not paths or any(not p.startswith(R15_PREFIX) for p in paths):
        raise RuntimeError("R15 merge changed paths outside the audited package")
    expected = (TARGET.as_posix(),) if patched else ()
    if modified != expected:
        raise RuntimeError("Unexpected tracked changes: " + str(modified))
    return "R15_MERGED_CLEAN" if local == REVIEWED_HEAD else "R15_MERGED_REMOTE_LOCAL_R14"


def verify_git_and_sources(*, patched: bool, root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R16 immediately below the repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Expected develop branch")
    remote = git("ls-remote", "origin", "refs/heads/develop", root=root).split()[0]
    local = git("rev-parse", "HEAD", root=root)
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged changes require separate review")
    changed = tuple(git("diff", "--name-only", root=root).splitlines())
    git_bytes("merge-base", "--is-ancestor", PRE_R15_HEAD, REVIEWED_HEAD, root=root)
    commits = git("rev-list", "--reverse", PRE_R15_HEAD + ".." + REVIEWED_HEAD, root=root).splitlines()
    if len(commits) != 1:
        raise RuntimeError("Expected exactly one reviewed R15 merge-lineage commit")
    paths = tuple(git("diff", "--name-only", PRE_R15_HEAD, REVIEWED_HEAD, root=root).splitlines())
    lineage = validate_lineage(local, remote, paths, changed, patched)
    for path, sha in PINS.items():
        file = root / path
        if not file.is_file() or not matches_blob(file.read_bytes(), sha):
            raise RuntimeError("R16 source guard mismatch: " + path)
    head_source = git_bytes("show", "HEAD:" + TARGET.as_posix(), root=root)
    if not matches_blob(head_source, BASE_BLOB):
        raise RuntimeError("R14 shared-math base SHA not pinned")
    original, _ = normalize_and_style(head_source)
    live = (root / TARGET).read_bytes()
    checked, _ = normalize_and_style(live)
    expected = transform_source(original) if patched else original
    if checked != expected:
        raise RuntimeError("Working tree is not the exact R16 patch state")
    return {
        "branch": "develop", "local_head": local, "remote_head": remote,
        "head_lineage": lineage, "source_guard": "PASS",
        "pinned_source_files": len(PINS) + 1,
        "tracked_changed": list(changed),
        "patched": patched,
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r15" / "chain_frontier_audit.json"


def validate_r15_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R15"
            or report.get("gate") != "PASS_READ_ONLY_CHAIN_FRONTIER_NO_ROOT_CLAIM"
            or report.get("full_pytest_run") is not False
            or report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R15 handoff evidence mismatch")
    live = report.get("live") or {}
    frontier = (live.get("public_goal_frontiers") or {}).get("final_pi12_7_zero") or {}
    if (frontier.get("count") != 0
            or live.get("new_verified_proof_steps") != 0
            or live.get("public_provider_changed") is not False):
        raise RuntimeError("R15 actual root proposal baseline changed")
    return {"prior_gate": report["gate"], "root_candidates_before": 0,
            "new_verifications_before": 0}


def inspect_public_root() -> dict[str, Any]:
    """Check actual public provider after patch; do not forge proof premises."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        RULE_NAME, ehp_zero_inputs, expand_ehp_zero_from_delta_surjectivity,
    )
    from proof import ProofRule, ProofStep
    from unified_statement_registry import AssertionOrigin

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    exact_given = tuple(
        link.step for link in screened.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == root
    )
    if exact_given:
        raise RuntimeError("Target zero group must not be a direct GIVEN")
    provider = shared_expansion_provider(screened, proof_target=root)
    options = tuple(provider(root))
    named = tuple(x for x in options if x.rule.name == RULE_NAME)
    isolated = expand_ehp_zero_from_delta_surjectivity(root)
    children = ehp_zero_inputs(root)
    if (len(named) != 1 or len(options) != 1 or len(isolated) != 1
            or children is None or len(children) != 4
            or named[0].subgoals != isolated[0].subgoals
            or named[0].subgoals != children
            or root in children
            or any(isinstance(c, ProofStep) for c in children)):
        raise RuntimeError("Public EHP root did not preserve the isolated 4-goal contract")
    frontiers = [tuple(provider(child)) for child in children]
    return {
        "public_root_proposal_count": len(options),
        "public_rule_name": RULE_NAME,
        "unproved_root_child_count": len(children),
        "child_types": [type(x).__name__ for x in children],
        "child_proposal_counts": [len(x) for x in frontiers],
        "child_goals": [repr(x)[:800] for x in children],
        "root_direct_given": False,
        "new_group_given": 0,
        "new_math_rule": 0,
        "proof_completed_claimed": False,
        "verified_proof_step_from_candidate": False,
    }


def inspect_standard_search() -> dict[str, Any]:
    """Check the real standard path; unresolved goals remain unresolved."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    result = search_group_from_registered_goal(
        n=7, k=5, bridge=build_shared_typed_bridge(), goal=goal,
    )
    if (result.status is ProofSearchStatus.COMPLETE or result.conclusion is not None
            or not any(item == goal for item in result.open_goals)):
        raise RuntimeError("R16 cannot claim or silently discard unresolved zero root")
    return {
        "status": result.status.value,
        "open_goal_count": len(result.open_goals),
        "open_goal_types": [type(x).__name__ for x in result.open_goals],
        "open_goals": [repr(x)[:800] for x in result.open_goals],
        "verified_steps_from_search": len(result.proven_steps),
        "conclusion": None,
    }


def output_path(dry_run: bool) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r16" / (
        "public_ehp_root_preflight.json" if dry_run else "public_ehp_root_audit.json"
    )


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(patched=not dry_run, root=root)
    previous = previous_report_path()
    if not previous.is_file():
        raise RuntimeError("R15 completed evidence missing: " + str(previous))
    handoff = validate_r15_report(json.loads(previous.read_text(encoding="utf-8-sig")))
    public = None if dry_run else inspect_public_root()
    search = None if dry_run else inspect_standard_search()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "PUBLIC_EHP_ZERO_ROOT",
        "git_state": state,
        "previous_report": handoff,
        "public": public,
        "search": search,
        "modified_production_functions": [] if dry_run else ["shared_expansion_provider"],
        "new_group_given": 0,
        "new_mathematical_inference_rules": 0,
        "full_pytest_run": False,
        "root_proof_completed_claimed": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_PUBLIC_GENERIC_EHP_ROOT_PREMISES_OPEN",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = output_path(args.dry_run)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R16_"
    state = report["git_state"]
    for key in ("local_head", "remote_head", "head_lineage", "source_guard"):
        print(prefix + key.upper() + "=" + str(state[key]))
    if report["public"] is not None:
        live = report["public"]
        print(prefix + "PUBLIC_ROOT_PROPOSALS=" + str(live["public_root_proposal_count"]))
        print(prefix + "UNPROVED_CHILD_GOALS=" + str(live["unproved_root_child_count"]))
        for index, (name, count) in enumerate(zip(live["child_types"], live["child_proposal_counts"]), 1):
            print(prefix + "CHILD_" + str(index) + "=" + name + ":" + str(count))
        search = report["search"]
        print(prefix + "SEARCH_STATUS=" + search["status"])
        print(prefix + "SEARCH_OPEN_GOALS=" + str(search["open_goal_count"]))
        print(prefix + "SEARCH_PROVEN_STEPS=" + str(search["verified_steps_from_search"]))
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_MATH_RULES=0")
    print(prefix + "ROOT_COMPLETE=False")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$PatchAttempted = $false
$Backup = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r3_r7_r16\phase165_r52_r9_shared_math.original.py'
$Target = Join-Path $RepoRoot 'phase165_r52_r9_shared_math.py'

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw "R16 git fetch failed" }

    & python -B -m phase174_r3_r7_r16_public_ehp_zero_root.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R16 source-first preflight failed" }
    & python -B -m phase174_r3_r7_r16_public_ehp_zero_root.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R16 guarded patch dry-run failed" }

    $Groups = @(
        @{ Name = 'R16_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_patch.py',
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_audit.py'
        ) },
        @{ Name = 'R3_EHP_RULE'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py'
        ) },
        @{ Name = 'R14_PUBLIC_SOURCE'; Paths = @(
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_public.py'
        ) },
        @{ Name = 'EHP_EXACTNESS'; Paths = @(
            '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "R16 focused test missing: $TestPath"
            }
        }
        Write-Output "PHASE174_R3R7R16_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "R16 focused pytest failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R16_FOCUSED_PYTEST=PASS'
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R16_GATE=PASS_PREFLIGHT'
    }
    else {
        $PatchAttempted = $true
        & python -B -m phase174_r3_r7_r16_public_ehp_zero_root.patch
        if ($LASTEXITCODE -ne 0) { throw 'R16 guarded apply failed' }
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R16 public provider integration failed' }
        & python -B -m phase174_r3_r7_r16_public_ehp_zero_root.audit
        if ($LASTEXITCODE -ne 0) { throw 'R16 public source-first audit failed' }
    }
    Write-Output '(END)'
}
catch {
    if ($PatchAttempted -and (Test-Path -LiteralPath $Backup)) {
        $Changed = @(git diff --name-only)
        if ($Changed -contains 'phase165_r52_r9_shared_math.py') {
            Copy-Item -LiteralPath $Backup -Destination $Target -Force
            Write-Output 'PHASE174_R3R7R16_ROLLBACK=RESTORED_REVIEWED_SOURCE'
        }
    }
    throw
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
```

## `tests/test_patch.py`

```python
"""Guarded replacement tests; no production imports or public proof claims."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r16_public_ehp_zero_root.patch import (
    BASE_BLOB, NEW, OLD, blob_sha, normalize_and_style, transform_source,
)


def sample_source() -> str:
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        + OLD
        + "        options.append(expand_hopf_image_relation(goal, ()))\n"
        + "        return tuple(options)\n"
        + "    return expand\n"
    )


def test_single_whole_function_preserves_existing_api_and_old_rule() -> None:
    text = transform_source(sample_source())
    assert text.count(NEW) == 1
    assert OLD not in text
    assert "def shared_expansion_provider():" in text
    assert "        options.append(expand_hopf_image_relation(goal, ()))" in text
    assert "expand_ehp_zero_from_delta_surjectivity(goal)" in text


def test_no_second_apply_and_no_nonmatching_anchor() -> None:
    updated = transform_source(sample_source())
    with pytest.raises(RuntimeError):
        transform_source(updated)
    with pytest.raises(RuntimeError):
        transform_source("def shared_expansion_provider():\n    return None\n")


def test_unique_function_and_anchor_required() -> None:
    with pytest.raises(RuntimeError):
        transform_source(sample_source().replace("def shared_expansion_provider():", "def unrelated():"))
    with pytest.raises(RuntimeError):
        transform_source(sample_source().replace("    return expand", OLD + "    return expand"))


@pytest.mark.parametrize("content", (
    b"a\r\nb\n", b"a\rb\r", b"\xef\xbb\xbfa\n",
))
def test_mixed_eol_or_bom_is_rejected(content: bytes) -> None:
    with pytest.raises(RuntimeError):
        normalize_and_style(content)


def test_uniform_line_endings_are_preserved() -> None:
    assert normalize_and_style(b"a\nb\n") == ("a\nb\n", b"\n")
    assert normalize_and_style(b"a\r\nb\r\n") == ("a\nb\n", b"\r\n")
    assert blob_sha(b"a\nb\n") != blob_sha(b"a\r\nb\r\n")
    assert len(BASE_BLOB) == 40


def test_full_function_export_is_not_an_abbreviated_diff(tmp_path) -> None:
    from phase174_r3_r7_r16_public_ehp_zero_root.patch import export_complete_function

    path = tmp_path / "MODIFIED_FUNCTION_FULL_JA.md"
    export_complete_function(transform_source(sample_source()), path)
    result = path.read_text(encoding="utf-8")
    assert "def shared_expansion_provider():" in result
    assert "    def expand(goal):" in result
    assert "        return tuple(options)" in result
    assert "    return expand" in result
    assert "expand_ehp_zero_from_delta_surjectivity(goal)" in result


def test_patched_bytes_require_exact_sha_and_retain_crlf(monkeypatch) -> None:
    import phase174_r3_r7_r16_public_ehp_zero_root.patch as target

    original = sample_source().encode("utf-8")
    monkeypatch.setattr(target, "BASE_BLOB", blob_sha(original))
    expected = transform_source(sample_source()).encode("utf-8")
    assert target.patched_bytes(original) == expected
    assert target.patched_bytes(original.replace(b"\n", b"\r\n")) == expected.replace(b"\n", b"\r\n")
    with pytest.raises(RuntimeError):
        target.patched_bytes(original + b"# unexpected edit\n")
```

## `tests/test_audit.py`

```python
"""R16 reviewed lineage, source pins, and R15 evidence contract tests."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase174_r3_r7_r16_public_ehp_zero_root.audit import (
    PINS, PRE_R15_HEAD, REVIEWED_HEAD, R15_PREFIX,
    matches_blob, validate_lineage, validate_r15_report,
)
from phase174_r3_r7_r16_public_ehp_zero_root.patch import TARGET, blob_sha


def sample_r15() -> dict:
    return {
        "phase": "174-R3-R7-R15",
        "gate": "PASS_READ_ONLY_CHAIN_FRONTIER_NO_ROOT_CLAIM",
        "full_pytest_run": False,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "completion_claimed": False,
        "live": {
            "new_verified_proof_steps": 0,
            "public_provider_changed": False,
            "public_goal_frontiers": {"final_pi12_7_zero": {"count": 0}},
        },
    }


def test_r15_evidence_never_becomes_root_proof() -> None:
    result = validate_r15_report(sample_r15())
    assert result["root_candidates_before"] == 0
    assert result["new_verifications_before"] == 0


@pytest.mark.parametrize("field,value", (
    ("gate", "PASS_PREFLIGHT"),
    ("full_pytest_run", True),
    ("new_group_given", 1),
    ("new_production_inference_rules", 1),
    ("completion_claimed", True),
))
def test_prior_report_corruption_fails_closed(field: str, value: object) -> None:
    report = sample_r15()
    report[field] = value
    with pytest.raises(RuntimeError):
        validate_r15_report(report)


@pytest.mark.parametrize("field,value", (
    ("new_verified_proof_steps", 1),
    ("public_provider_changed", True),
))
def test_r15_live_candidate_cannot_be_promoted(field: str, value: object) -> None:
    report = deepcopy(sample_r15())
    report["live"][field] = value
    with pytest.raises(RuntimeError):
        validate_r15_report(report)


def test_r15_zero_root_baseline_must_be_real() -> None:
    report = sample_r15()
    report["live"]["public_goal_frontiers"]["final_pi12_7_zero"]["count"] = 1
    with pytest.raises(RuntimeError):
        validate_r15_report(report)


def test_reviewed_two_local_layouts_accept_only_one_r15_successor() -> None:
    paths = (R15_PREFIX + "audit.py", R15_PREFIX + "tests/test_contract.py")
    assert validate_lineage(PRE_R15_HEAD, REVIEWED_HEAD, paths, (), False) == "R15_MERGED_REMOTE_LOCAL_R14"
    assert validate_lineage(REVIEWED_HEAD, REVIEWED_HEAD, paths, (), False) == "R15_MERGED_CLEAN"
    assert validate_lineage(PRE_R15_HEAD, REVIEWED_HEAD, paths, (TARGET.as_posix(),), True) == "R15_MERGED_REMOTE_LOCAL_R14"
    assert validate_lineage(REVIEWED_HEAD, REVIEWED_HEAD, paths, (TARGET.as_posix(),), True) == "R15_MERGED_CLEAN"


@pytest.mark.parametrize("local,remote,paths,modified,patched", (
    (PRE_R15_HEAD, PRE_R15_HEAD, (R15_PREFIX + "audit.py",), (), False),
    ("f" * 40, REVIEWED_HEAD, (R15_PREFIX + "audit.py",), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, ("proof.py",), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, (), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, (R15_PREFIX + "audit.py",), ("proof.py",), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, (R15_PREFIX + "audit.py",), (), True),
))
def test_unreviewed_git_state_never_passes(
    local: str, remote: str, paths: tuple[str, ...],
    modified: tuple[str, ...], patched: bool,
) -> None:
    with pytest.raises(RuntimeError):
        validate_lineage(local, remote, paths, modified, patched)


def test_pinned_git_blobs_reject_mixed_endings_and_mutations() -> None:
    reference = b"Toda source\nnext line\n"
    sha = blob_sha(reference)
    assert matches_blob(reference, sha)
    assert matches_blob(b"Toda source\r\nnext line\r\n", sha)
    assert not matches_blob(b"Toda source\r\nnext line\n", sha)
    assert not matches_blob(reference + b"change", sha)
    assert not matches_blob(reference, sha[:-1])
    assert len(PINS) >= 6
    assert all(len(s) == 40 for s in PINS.values())
```

## `tests/test_public.py`

```python
"""Integration check after the exact guarded production connection only."""
from __future__ import annotations

from phase174_r3_r7_r16_public_ehp_zero_root.audit import inspect_public_root
from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME


def test_zero_root_is_exactly_one_unproved_generic_ehp_branch() -> None:
    status = inspect_public_root()
    assert status["public_root_proposal_count"] == 1
    assert status["public_rule_name"] == RULE_NAME
    assert status["unproved_root_child_count"] == 4
    assert status["root_direct_given"] is False
    assert status["new_group_given"] == 0
    assert status["new_math_rule"] == 0
    assert status["proof_completed_claimed"] is False
    assert status["verified_proof_step_from_candidate"] is False
```

## `tests/__init__.py`

```python
"""Focused contracts for the Phase 174 R3-R7-R16 public EHP root."""
```

## `__init__.py`

```python
"""One-function public connection for the pre-existing generic EHP zero rule."""
```

