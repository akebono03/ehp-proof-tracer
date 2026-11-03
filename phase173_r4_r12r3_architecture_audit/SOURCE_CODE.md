# R4-R12R3 追加コード全文（省略なし）

本体コードの変更はない。以下は監査用の新規ファイルの完全な内容。

## `audit.py`

```python
"""Phase 173 R4-R12R3: read-only architecture audit of proof narratives.

This file reads tracked sources. It never modifies the repository, a proof,
its citations, or the outcome of a proof search.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import subprocess


REVIEWED_HEAD = "188f707e1fcd8fde7b22af02a6b4005986fb3c1e"
ACTIVE_FILES = (
    "phase165_r52_r3_web_adapter.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_5_model_renderer.py",
    "phase172_r5_prior_reference_display/projection.py",
    "phase173_r4_r12_common_narrative/projection.py",
    "phase173_r4_r1_narrative_source_fix/projection.py",
    "web_group_proof_common.py",
)
FOCUSED_TEST_FILES = (
    "phase173_r4_r12_common_narrative/tests/test_projection.py",
    "phase173_r4_r12_common_narrative/tests/test_install.py",
    "phase173_r4_r13_narrative_audit/tests/test_audit.py",
)
CORE_GATE_FILES = (
    "phase165_r52_r3_web_adapter.py",
    "phase168_r3_5_model_renderer.py",
    "phase173_r4_r12_common_narrative/projection.py",
)
DEDICATED_NAME = re.compile(r"(?:^|_)pi\d{2,}(?:_|$)")
PROSE_LITERAL = re.compile(r"(?:\\nu_4|生成元の対応|両側の先行群はいずれも零群)")


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    line: int
    detail: str


def _extract_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return _extract_name(node.value) + "." + node.attr
    return ""


def _numeric_dimension_dispatch(node: ast.AST) -> bool:
    """Recognize equality against a literal dimension in a conditional."""
    for item in ast.walk(node):
        if not isinstance(item, ast.Compare):
            continue
        operands = (item.left, *item.comparators)
        dimension = any(
            _extract_name(value).split(".")[-1]
            in {"sphere_dimension", "group_dimension", "n", "k"}
            for value in operands
        )
        literal = any(
            isinstance(value, ast.Constant) and type(value.value) is int
            for value in operands
        )
        if dimension and literal and any(
            isinstance(op, (ast.Eq, ast.NotEq)) for op in item.ops
        ):
            return True
    return False


def scan_source(source: str, path: str) -> tuple[Finding, ...]:
    """Report structural findings in a reviewed source, without altering it.

    Static checks are deliberately narrow: source and proof semantics cannot be
    validated by AST alone. The migration gate adds live proof tests.
    """
    tree = ast.parse(source, filename=path)
    lines = source.splitlines()
    findings: list[Finding] = []
    is_test = "/tests/" in "/" + path
    is_renderer = path in CORE_GATE_FILES or path.endswith("/projection.py")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if (is_renderer and DEDICATED_NAME.search(node.name)
                    and "narrative" in node.name):
                findings.append(Finding(
                    "DEDICATED_NARRATIVE_FUNCTION", path, node.lineno, node.name,
                ))
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            imports = (
                [alias.name for alias in node.names]
                if isinstance(node, ast.ImportFrom)
                else [alias.name for alias in node.names]
            )
            for imported in imports:
                if is_renderer and DEDICATED_NAME.search(imported) and "narrative" in imported:
                    findings.append(Finding(
                        "DEDICATED_NARRATIVE_IMPORT", path, node.lineno, imported,
                    ))
        if isinstance(node, (ast.If, ast.IfExp)) and is_renderer:
            if _numeric_dimension_dispatch(node.test):
                findings.append(Finding(
                    "LITERAL_DIMENSION_DISPATCH", path, node.lineno,
                    ast.unparse(node.test),
                ))
            if path.endswith("phase173_r4_r12_common_narrative/projection.py"):
                if "LEGACY_ROOT" in ast.unparse(node.test):
                    findings.append(Finding(
                        "LEGACY_RULE_DISPATCH", path, node.lineno,
                        ast.unparse(node.test),
                    ))
        if isinstance(node, ast.Call) and is_renderer:
            target = _extract_name(node.func)
            if target and DEDICATED_NAME.search(target) and "narrative" in target:
                findings.append(Finding(
                    "DEDICATED_NARRATIVE_CALL", path, node.lineno, target,
                ))
            if (path == "phase168_r3_5_model_renderer.py"
                    and target == "TodaPrimaryGroup"
                    and any(isinstance(arg, ast.Constant) and type(arg.value) is int
                            for arg in node.args)):
                findings.append(Finding(
                    "FIXED_SPHERE_CONSTRUCTOR", path, node.lineno,
                    ast.unparse(node),
                ))
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and path == "phase165_r52_r3_web_adapter.py":
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(_extract_name(target) == "markdown" for target in targets):
                value = node.value
                if (isinstance(value, ast.Call)
                        and "project_" in _extract_name(value.func)):
                    findings.append(Finding(
                        "POST_RENDER_NARRATIVE_OVERRIDE", path, node.lineno,
                        _extract_name(value.func),
                    ))
    if is_renderer:
        for number, line in enumerate(lines, 1):
            if PROSE_LITERAL.search(line) and not line.lstrip().startswith("#"):
                findings.append(Finding(
                    "HARDCODED_PRESENTATION_CANDIDATE", path, number,
                    line.strip()[:200],
                ))
    if is_test:
        for number, line in enumerate(lines, 1):
            if ("byte_equal" in line or "== expected" in line
                    or 'assert "零群" in shown' in line
                    or 'assert "生成元の対応" in shown' in line):
                findings.append(Finding(
                    "LEGACY_TEST_CONTRACT", path, number, line.strip(),
                ))
    return tuple(sorted(set(findings), key=lambda x: (x.path, x.line, x.code)))


def _git(root: Path, *args: str) -> str:
    finished = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return finished.stdout.strip()


def _tracked_python(root: Path) -> tuple[str, ...]:
    # Git can return historical patch snapshots. Report candidates, not false
    # production findings, for paths outside the reviewed live boundary.
    payload = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.py"], cwd=root,
        capture_output=True, check=True,
    ).stdout
    return tuple(sorted(path.decode("utf-8") for path in payload.split(b"\0") if path))


def _repository_candidates(root: Path) -> tuple[dict[str, object], ...]:
    result: list[dict[str, object]] = []
    excluded_parts = {
        "tests", "test", "fixtures", "output", "full_replacements",
        "full_functions", "artifacts", "snapshots", "examples",
    }
    for path in _tracked_python(root):
        parts = Path(path).parts
        if set(parts) & excluded_parts or path in ACTIVE_FILES:
            continue
        if parts[-1] in {"install.py", "apply.py", "verify.py", "audit.py", "repair.py"}:
            continue
        source_path = root / path
        try:
            source = source_path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            continue
        # Broad repository-wide screening is informational, not a brittle gate.
        found = re.findall(
            r"(?:def\s+\w*(?:narrative|projection)\w*|"
            r"(?:project|render)_verified_pi\d+_narrative)",
            source,
        )
        if found:
            result.append({"path": path, "matching_constructs": len(found)})
    return tuple(result)


def inspect_repository(root: Path, *, broad_scan: bool = True) -> dict[str, object]:
    root = root.resolve()
    head = _git(root, "rev-parse", "HEAD")
    branch = _git(root, "branch", "--show-current")
    changed = _git(root, "diff", "--name-only")
    staged = _git(root, "diff", "--cached", "--name-only")
    missing = [path for path in (*ACTIVE_FILES, *FOCUSED_TEST_FILES) if not (root / path).is_file()]
    if missing:
        raise FileNotFoundError("Missing reviewed files: " + ", ".join(missing))
    findings: list[Finding] = []
    for path in (*ACTIVE_FILES, *FOCUSED_TEST_FILES):
        findings.extend(scan_source((root / path).read_text(encoding="utf-8-sig"), path))
    return {
        "phase": "173 R4-R12R3",
        "mode": "audit_only",
        "reviewed_github_head": REVIEWED_HEAD,
        "local_head": head,
        "branch": branch,
        "local_matches_reviewed": head == REVIEWED_HEAD,
        "tracked_worktree_modifications": changed.splitlines() if changed else [],
        "staged_files": staged.splitlines() if staged else [],
        "findings": [asdict(item) for item in sorted(set(findings), key=lambda x: (x.path, x.line, x.code))],
        "repository_wide_candidates": list(_repository_candidates(root)) if broad_scan else [],
        "conclusion": "NOT_UNIFIED_WHILE_ACTIVE_FINDINGS_REMAIN",
        "proof_status_modified": False,
        "production_files_modified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fast", action="store_true", help="Skip repository-wide candidate inventory")
    args = parser.parse_args()
    report = inspect_repository(args.root, broad_scan=not args.fast)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print("PHASE173_R4_R12R3_MODE=AUDIT_ONLY")
    print("PHASE173_R4_R12R3_LOCAL_HEAD=" + report["local_head"])
    print("PHASE173_R4_R12R3_REVIEWED_HEAD=" + REVIEWED_HEAD)
    print("PHASE173_R4_R12R3_BRANCH=" + report["branch"])
    print("PHASE173_R4_R12R3_FINDINGS=" + str(len(report["findings"])))
    for finding in report["findings"]:
        print("FINDING={code}|{path}:{line}|{detail}".format(**finding))
    print("PHASE173_R4_R12R3_CANDIDATE_MODULES=" + str(len(report["repository_wide_candidates"])))
    print("PHASE173_R4_R12R3_ARCHITECTURE_UNIFIED=" + str(not report["findings"]))
    print("PHASE173_R4_R12R3_AUDIT_COMPLETED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/test_audit.py`

```python
"""Pure AST detector tests; no proof-search or renderer edits."""
from __future__ import annotations

from phase173_r4_r12r3_architecture_audit.audit import scan_source


def _codes(source: str, path: str) -> set[str]:
    return {finding.code for finding in scan_source(source, path)}


def test_dedicated_pi_narrative_function_is_detected() -> None:
    source = (
        "def project_verified_pi74_narrative(result, model, markdown):\n"
        "    return markdown\n"
    )
    codes = _codes(source, "phase173_r4_r12_common_narrative/projection.py")
    assert "DEDICATED_NARRATIVE_FUNCTION" in codes


def test_numeric_dispatch_is_detected_without_source_text_matching() -> None:
    source = (
        "def render(result):\n"
        "    if 7 == result.target.group_dimension:\n"
        "        return 'custom'\n"
        "    return 'generic'\n"
    )
    codes = _codes(source, "phase173_r4_r12_common_narrative/projection.py")
    assert "LITERAL_DIMENSION_DISPATCH" in codes


def test_legacy_rule_dispatch_is_detected() -> None:
    source = (
        "LEGACY_ROOT = 'previous'\n"
        "def project(result):\n"
        "    if root_name == LEGACY_ROOT:\n"
        "        return 'custom'\n"
        "    return 'generic'\n"
    )
    codes = _codes(source, "phase173_r4_r12_common_narrative/projection.py")
    assert "LEGACY_RULE_DISPATCH" in codes


def test_adapter_rewriting_derived_markdown_is_detected() -> None:
    source = (
        "def build(result, model):\n"
        "    markdown = render_model_backed_narrative_markdown(result, model)\n"
        "    markdown = project_verified_toda56_narrative(result, model, markdown)\n"
        "    return markdown\n"
    )
    codes = _codes(source, "phase165_r52_r3_web_adapter.py")
    assert "POST_RENDER_NARRATIVE_OVERRIDE" in codes


def test_generic_model_renderer_has_no_false_dimension_dispatch() -> None:
    source = (
        "def render(result, model):\n"
        "    for step in model.steps:\n"
        "        if step.rule == ProofRule.GIVEN:\n"
        "            return format_step(step)\n"
        "    return ''\n"
    )
    codes = _codes(source, "phase168_r3_5_model_renderer.py")
    assert "LITERAL_DIMENSION_DISPATCH" not in codes
    assert "DEDICATED_NARRATIVE_FUNCTION" not in codes


def test_test_contract_that_freezes_legacy_wording_is_detected() -> None:
    source = (
        "def test_pi74_existing_projection_remains_byte_equal():\n"
        "    assert shown == expected\n"
    )
    codes = _codes(
        source, "phase173_r4_r12_common_narrative/tests/test_projection.py",
    )
    assert "LEGACY_TEST_CONTRACT" in codes


def test_fixed_sphere_dimension_in_central_renderer_is_detected() -> None:
    source = (
        "def render(mapping, i):\n"
        "    if mapping.target_group == TodaPrimaryGroup(i, 4):\n"
        "        return 'custom'\n"
        "    return 'generic'\n"
    )
    codes = _codes(source, "phase168_r3_5_model_renderer.py")
    assert "FIXED_SPHERE_CONSTRUCTOR" in codes

```

## `future_gate/architecture_gate_spec.py`

```python
"""Migration acceptance gate. Expected to FAIL before dedicated paths are removed.

DO NOT run during the read-only audit. Enable only after implementing the
unified renderer and replacing legacy prose-exact tests with semantic tests.
"""
from __future__ import annotations

from pathlib import Path

from phase173_r4_r12r3_architecture_audit.audit import (
    CORE_GATE_FILES,
    scan_source,
)


ROOT = Path(__file__).resolve().parents[2]
PROHIBITED = {
    "DEDICATED_NARRATIVE_FUNCTION",
    "DEDICATED_NARRATIVE_IMPORT",
    "DEDICATED_NARRATIVE_CALL",
    "LITERAL_DIMENSION_DISPATCH",
    "LEGACY_RULE_DISPATCH",
    "POST_RENDER_NARRATIVE_OVERRIDE",
    "FIXED_SPHERE_CONSTRUCTOR",
    "HARDCODED_PRESENTATION_CANDIDATE",
}


def test_unified_renderer_contains_no_structural_special_cases() -> None:
    violations = []
    for path in CORE_GATE_FILES:
        source = (ROOT / path).read_text(encoding="utf-8-sig")
        violations.extend(
            finding for finding in scan_source(source, path)
            if finding.code in PROHIBITED
        )
    assert violations == [], "Specialized Narrative architecture is still active"


def test_complete_five_groups_keep_certified_sources_and_web() -> None:
    from phase173_r4_r13_narrative_audit.audit import inspect_dimension

    for dimension in (7, 8, 9, 10, 11):
        row = inspect_dimension(dimension, with_web=True)
        assert row["source_verified"] is True
        assert row["web_verified"] is True
        assert row["open_goals"] == 0
        assert row["source_reference_count"] >= 4


def test_unproved_pi12_is_still_refused() -> None:
    from phase173_r4_r13_narrative_audit.audit import inspect_unproven_epsilon

    assert inspect_unproven_epsilon() is True

```

## `run.ps1`

```powershell
param(
    [switch]$DryRun,
    [switch]$SkipBroadScan
)
$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$ExpectedHead = '188f707e1fcd8fde7b22af02a6b4005986fb3c1e'

function Assert-LastExit([string]$Step) {
    if ($LASTEXITCODE -ne 0) {
        throw "$Step failed with exit code $LASTEXITCODE"
    }
}

Push-Location $Root
try {
    $Branch = (git branch --show-current).Trim()
    Assert-LastExit 'git branch'
    if ($Branch -ne 'develop') {
        throw "Expected develop; current branch: $Branch"
    }
    git fetch origin develop
    Assert-LastExit 'git fetch origin develop'
    $RemoteHead = (git rev-parse origin/develop).Trim()
    Assert-LastExit 'git remote HEAD'
    $LocalHead = (git rev-parse HEAD).Trim()
    Assert-LastExit 'git local HEAD'
    Write-Output "PHASE173_R4_R12R3_REMOTE_HEAD=$RemoteHead"
    Write-Output "PHASE173_R4_R12R3_LOCAL_HEAD=$LocalHead"
    if ($RemoteHead -ne $ExpectedHead) {
        throw "GitHub develop advanced after review. Re-audit before running. Expected $ExpectedHead, got $RemoteHead"
    }
    if ($LocalHead -ne $ExpectedHead) {
        throw "Local HEAD differs from reviewed GitHub HEAD. No automatic checkout/merge is performed."
    }
    $Staged = @(git diff --cached --name-only)
    Assert-LastExit 'git staged diff'
    if ($Staged.Count -gt 0) {
        throw 'Staged changes detected; review before using the baseline.'
    }
    $TrackedChanges = @(git diff --name-only)
    Assert-LastExit 'git worktree diff'
    if ($TrackedChanges.Count -gt 0) {
        throw 'Tracked worktree modifications detected; review before using the baseline.'
    }
    Write-Output 'PHASE173_R4_R12R3_PREFLIGHT=PASS'
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R12R3_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R12R3_PRODUCTION_EDIT=NONE'
        exit 0
    }
    $ArgsList = @(
        (Join-Path $Package 'audit.py'), '--root', $Root,
        '--output', (Join-Path $Package 'audit_result.json')
    )
    if ($SkipBroadScan) {
        $ArgsList += '--fast'
    }
    python @ArgsList
    Assert-LastExit 'read-only structural audit'
    python -m pytest -q `
        phase173_r4_r12r3_architecture_audit/tests/test_audit.py `
        phase173_r4_r12_common_narrative/tests/test_projection.py `
        phase173_r4_r12_common_narrative/tests/test_install.py `
        phase173_r4_r13_narrative_audit/tests/test_audit.py
    Assert-LastExit 'focused pytest'
    Write-Output 'PHASE173_R4_R12R3_FOCUSED_PYTEST=PASS'
    Write-Output 'PHASE173_R4_R12R3_ONLY_AUDIT=PASS'
    Write-Output 'PHASE173_R4_R12R3_PRODUCTION_EDIT=NONE'
}
finally {
    Pop-Location
}

```
