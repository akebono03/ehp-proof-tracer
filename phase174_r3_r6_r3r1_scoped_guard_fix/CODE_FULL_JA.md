# Phase 174 R3-R6-R3R1 — 追加・修正コード全文

変更対象の既存クラス・関数はありません。新規クラスと関数の全文を以下に示します。
R3-R6-R3 で変更予定の既存関数全文は、このパッケージの DryRun 成功後に
`output/CODE_FULL_JA.md`、`output/typed_sentence_FULL.py`、
`output/render_model_backed_narrative_markdown_FULL.py` に生成します。

新規ファイルの import は以下のコード内で省略せず掲載しています。

## patch.py

```python
"""Source-reviewed, function-scoped installer for the preceding R3-R6-R3 patch.

This repair writes only inserted lines into two previously reviewed functions.
Other local text (including mixed Windows newlines) is preserved byte for byte.
Unreviewed changes *inside* either target function or its imports fail closed.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from difflib import SequenceMatcher, unified_diff
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from phase174_r3_r6_r3_common_narrative import patch as previous

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
REVIEWED_HEAD = "ecbb2fea225c5b88000629d9c025934fcc2d7075"
TARGETS = (
    ("phase168_r3_27_typed_statement_projection.py", "typed_sentence", previous.transform_typed),
    ("phase168_r3_5_model_renderer.py", "render_model_backed_narrative_markdown", previous.transform_renderer),
)


@dataclass(frozen=True)
class ScopedChange:
    path: str
    original: bytes
    updated: bytes
    original_normalized: str
    updated_normalized: str
    unrelated_worktree_difference: bool


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
    ).hexdigest()


def git_head_file(root: Path, path: str) -> bytes:
    result = subprocess.run(
        ("git", "show", "HEAD:" + path),
        cwd=root, capture_output=True, check=True,
    )
    return result.stdout


def normalize_text(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def statement_ast(text: str, function_name: str) -> tuple[str, tuple[str, ...]]:
    tree = ast.parse(text)
    matches = tuple(
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    )
    if len(matches) != 1:
        raise ValueError("Reviewed function missing or ambiguous: " + function_name)
    import_asts = tuple(
        ast.dump(node, include_attributes=False)
        for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
    )
    return ast.dump(matches[0], include_attributes=False), import_asts


def preserve_original_lines(original: bytes, old_text: str, updated_text: str) -> bytes:
    """Insert only new lines; never rewrite a pre-existing line or its ending."""
    had_bom = original.startswith(b"\xef\xbb\xbf")
    raw_text = original.decode("utf-8-sig")
    raw_lines = raw_text.splitlines(keepends=True)
    old_lines = old_text.splitlines(keepends=True)
    updated_lines = updated_text.splitlines(keepends=True)
    if len(raw_lines) != len(old_lines):
        raise ValueError("Raw and normalized line counts disagree; refusing rewrite")
    if any(normalize_text(line.encode("utf-8")) != normalized
           for line, normalized in zip(raw_lines, old_lines)):
        raise ValueError("Original bytes do not map to normalized source lines")
    opcodes = SequenceMatcher(
        a=old_lines, b=updated_lines, autojunk=False,
    ).get_opcodes()
    if not any(tag == "insert" for tag, _, _, _, _ in opcodes):
        raise ValueError("Expected at least one guarded insertion")
    if any(tag not in ("equal", "insert") for tag, _, _, _, _ in opcodes):
        raise ValueError("Installer attempted to replace or delete existing source")

    out: list[str] = []
    for tag, a, b, c, d in opcodes:
        if tag == "equal":
            out.extend(raw_lines[a:b])
        else:
            neighbor = raw_lines[a - 1] if a else raw_lines[0]
            ending = "\r\n" if neighbor.endswith("\r\n") else (
                "\r" if neighbor.endswith("\r") else "\n"
            )
            additions = updated_lines[c:d]
            for added in additions:
                if not added.endswith("\n"):
                    raise ValueError("Added line is missing a newline")
                out.append(added[:-1] + ending)
    modified = ("\ufeff" if had_bom else "") + "".join(out)
    result = modified.encode("utf-8")
    if normalize_text(result) != updated_text:
        raise ValueError("Applied code differs from the reviewed transformation")
    return result


def inspect_scoped_change(
    root: Path, path: str, function_name: str, transform,
    reviewed_blob_sha: str,
) -> ScopedChange:
    baseline = git_head_file(root, path)
    observed_head = git_blob_sha(baseline)
    if observed_head != reviewed_blob_sha:
        raise ValueError(
            f"Unreviewed Git HEAD blob for {path}: "
            f"expected {reviewed_blob_sha}, observed {observed_head}"
        )
    original = (root / path).read_bytes()
    baseline_text = normalize_text(baseline)
    local_text = normalize_text(original)
    baseline_function, baseline_imports = statement_ast(baseline_text, function_name)
    local_function, local_imports = statement_ast(local_text, function_name)
    if baseline_imports != local_imports:
        raise ValueError(
            f"Unreviewed import changes in {path}; source must be reviewed first"
        )
    if baseline_function != local_function:
        raise ValueError(
            f"Unreviewed changes inside {function_name} in {path}; "
            "source must be reviewed first"
        )
    expected_updated = transform(baseline_text)
    actual_updated = transform(local_text)
    if statement_ast(expected_updated, function_name)[0] != statement_ast(
        actual_updated, function_name
    )[0]:
        raise ValueError("Transformed function differs from reviewed target")
    updated = preserve_original_lines(original, local_text, actual_updated)
    return ScopedChange(
        path=path, original=original, updated=updated,
        original_normalized=local_text, updated_normalized=actual_updated,
        unrelated_worktree_difference=baseline_text != local_text,
    )


def reviewed_changes(root: Path = ROOT) -> tuple[ScopedChange, ...]:
    changes = []
    for path, function, transform in TARGETS:
        changes.append(inspect_scoped_change(
            root, path, function, transform, previous.REVIEWED_BLOBS[path],
        ))
    return tuple(changes)


def write_atomically(path: Path, data: bytes) -> None:
    handle = tempfile.NamedTemporaryFile(
        mode="wb", dir=path.parent, prefix=path.name + ".",
        suffix=".tmp", delete=False,
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(data)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_outputs(changes: tuple[ScopedChange, ...]) -> None:
    output = PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    previous.generate_full_outputs({
        change.path: (change.original, change.updated_normalized)
        for change in changes
    })
    names = (
        ("typed_sentence_FULL.py", "typed_sentence"),
        ("render_model_backed_narrative_markdown_FULL.py", "render_model_backed_narrative_markdown"),
    )
    text = ["# Phase 174 R3-R6-R3R1 置換可能な完全コード", "",
            "既存 import に変更はありません。新規クラス・関数は本 ZIP の `patch.py` に全文収録しています。", ""]
    for change, (filename, function) in zip(changes, names):
        function_source = previous.extract_full_function(change.updated_normalized, function)
        (output / filename).write_text(function_source.rstrip() + "\n", encoding="utf-8")
        text.extend(("## " + change.path + " — " + function, "", "```python",
                     function_source.rstrip(), "```", ""))
    (output / "CODE_FULL_JA.md").write_text("\n".join(text), encoding="utf-8")
    report = {
        "reviewed_head": REVIEWED_HEAD,
        "guard": "complete target-function and import AST match HEAD; unrelated bytes preserved",
        "changes": [{
            "path": change.path,
            "local_differs_from_HEAD": change.unrelated_worktree_difference,
            "before_sha256": hashlib.sha256(change.original).hexdigest(),
            "after_sha256": hashlib.sha256(change.updated).hexdigest(),
            "only_inserted_lines": True,
        } for change in changes],
        "full_pytest_performed": False,
    }
    (output / "audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    flags = parser.add_mutually_exclusive_group(required=True)
    flags.add_argument("--dry-run", action="store_true")
    flags.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    changes = reviewed_changes()
    write_outputs(changes)
    print("PHASE174_R3R6R3R1_SCOPED_SOURCE_GUARD=PASS")
    for change in changes:
        print("PHASE174_R3R6R3R1_LOCAL_DIFFERENCE_" +
              Path(change.path).stem + "=" + str(change.unrelated_worktree_difference))
    print("PHASE174_R3R6R3R1_TARGET_FILES=" + str(len(changes)))
    if args.dry_run:
        print("PHASE174_R3R6R3R1_DRY_RUN=PASS")
        return 0
    applied: list[ScopedChange] = []
    try:
        for change in changes:
            write_atomically(ROOT / change.path, change.updated)
            applied.append(change)
    except Exception:
        for change in reversed(applied):
            write_atomically(ROOT / change.path, change.original)
        raise
    print("PHASE174_R3R6R3R1_APPLIED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_patch.py

```python
"""Verify that a local edit is never silently replaced by the installer."""
from __future__ import annotations

import subprocess

import pytest

from phase174_r3_r6_r3_common_narrative.patch import (
    transform_renderer,
    transform_typed,
)
from phase174_r3_r6_r3r1_scoped_guard_fix.patch import (
    git_blob_sha,
    inspect_scoped_change,
    normalize_text,
)

TYPED = (
    "from __future__ import annotations\n"
    "import math\n"
    "\n"
    "def unrelated_helper():\n"
    "    return 1\n"
    "\n"
    "def typed_sentence(statement, step):\n"
    "    map_sentence = map_property_sentence(statement, step)\n"
    "    return map_sentence\n"
)

RENDERER = (
    "from __future__ import annotations\n"
    "import math\n"
    "\n"
    "def unrelated_helper():\n"
    "    return 1\n"
    "\n"
    "def render_model_backed_narrative_markdown(result, model):\n"
    "    for citation in model.citations:\n"
    "        if not incomplete:\n"
    "            displayed = display_prior_reference_locator(citation, model)\n"
    "            if displayed is not None:\n"
    "                locator = displayed\n"
    "        lines.append(f\"**[R{citation.number}] {locator}.**\")\n"
    "        body_line = body_by_step.get(index)\n"
    "        sentence = typed_sentence(step.conclusion, step)\n"
    "        if sentence is not None:\n"
    "            pass\n"
)


def _repo(tmp_path, path: str, baseline: str):
    subprocess.run(("git", "init", "-q"), cwd=tmp_path, check=True)
    subprocess.run(("git", "config", "user.name", "Test"), cwd=tmp_path, check=True)
    subprocess.run(("git", "config", "user.email", "test@example.invalid"), cwd=tmp_path, check=True)
    target = tmp_path / path
    target.write_text(baseline, encoding="utf-8", newline="\n")
    subprocess.run(("git", "add", path), cwd=tmp_path, check=True)
    subprocess.run(("git", "commit", "-qm", "reviewed baseline"), cwd=tmp_path, check=True)
    return target, git_blob_sha(baseline.encode("utf-8"))


def test_preserves_unrelated_local_semantic_edits_and_crlf(tmp_path) -> None:
    path = "phase168_r3_27_typed_statement_projection.py"
    target, blob = _repo(tmp_path, path, TYPED)
    modified = TYPED.replace("return 1", "return 17").replace("\n", "\r\n")
    target.write_bytes(modified.encode("utf-8"))
    change = inspect_scoped_change(
        tmp_path, path, "typed_sentence", transform_typed, blob,
    )
    assert change.unrelated_worktree_difference
    assert b"    return 17\r\n" in change.updated
    assert b"    return 1\r\n" not in change.updated
    assert b"    return 17\r\n" in change.original
    assert b"project_verified_index_two_statement" in change.updated
    assert change.updated.count(b"\r\n") == change.updated.count(b"\n")
    assert target.read_bytes() == change.original  # even DryRun never writes


def test_preserves_mixed_newlines_and_bom_without_normalizing_unrelated_lines(tmp_path) -> None:
    path = "phase168_r3_5_model_renderer.py"
    target, blob = _repo(tmp_path, path, RENDERER)
    raw = "\ufeff" + RENDERER.replace("return 1\n", "return 20\r\n")
    target.write_bytes(raw.encode("utf-8"))
    change = inspect_scoped_change(
        tmp_path, path, "render_model_backed_narrative_markdown", transform_renderer, blob,
    )
    assert change.updated.startswith(b"\xef\xbb\xbf")
    assert b"return 20\r\n" in change.updated
    assert b"display_cited_nu_family_locator" in change.updated
    assert b"project_verified_cyclic_extension_reason" in change.updated
    assert normalize_text(change.updated) == transform_renderer(normalize_text(change.original))


def test_rejects_locally_modified_target_function(tmp_path) -> None:
    path = "phase168_r3_27_typed_statement_projection.py"
    target, blob = _repo(tmp_path, path, TYPED)
    modified = TYPED.replace("return map_sentence", "return None")
    target.write_text(modified, encoding="utf-8")
    with pytest.raises(ValueError, match="inside typed_sentence"):
        inspect_scoped_change(tmp_path, path, "typed_sentence", transform_typed, blob)
    assert target.read_text(encoding="utf-8") == modified


def test_rejects_unreviewed_import_changes(tmp_path) -> None:
    path = "phase168_r3_27_typed_statement_projection.py"
    target, blob = _repo(tmp_path, path, TYPED)
    target.write_text(TYPED.replace("import math", "import cmath"), encoding="utf-8")
    with pytest.raises(ValueError, match="import changes"):
        inspect_scoped_change(tmp_path, path, "typed_sentence", transform_typed, blob)


def test_rejects_unknown_reviewed_git_blob(tmp_path) -> None:
    path = "phase168_r3_27_typed_statement_projection.py"
    target, _ = _repo(tmp_path, path, TYPED)
    with pytest.raises(ValueError, match="Unreviewed Git HEAD blob"):
        inspect_scoped_change(tmp_path, path, "typed_sentence", transform_typed, "0" * 40)
    assert target.read_text(encoding="utf-8") == TYPED
```

## run.ps1

```powershell
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    $reviewedHead = 'ecbb2fea225c5b88000629d9c025934fcc2d7075'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
        throw 'R3-R6-R3R1 requires develop.'
    }
    git fetch origin
    if ($LASTEXITCODE -ne 0) { throw 'Cannot verify remote develop.' }
    $head = (git rev-parse HEAD).Trim()
    $remote = (git rev-parse origin/develop).Trim()
    if ($head -ne $reviewedHead -or $remote -ne $reviewedHead) {
        throw "Unreviewed HEAD: local=$head remote=$remote expected=$reviewedHead"
    }
    $originalPatch = Join-Path $repo 'phase174_r3_r6_r3_common_narrative/patch.py'
    $originalProjection = Join-Path $repo 'phase174_r3_r6_r3_common_narrative/projection.py'
    if (-not (Test-Path $originalPatch) -or -not (Test-Path $originalProjection)) {
        throw 'The original R3-R6-R3 package must remain installed.'
    }
    if ((Get-FileHash $originalPatch -Algorithm SHA256).Hash.ToLowerInvariant() -ne '6b79153c208724c179ae6c57fea2fb79507875d3c22f09dc822f25272a1fe01b') {
        throw 'The original R3-R6-R3 patch.py has unreviewed changes.'
    }
    if ((Get-FileHash $originalProjection -Algorithm SHA256).Hash.ToLowerInvariant() -ne '28f629b1b163ecd55402f0e4d3a71b1d0640b029c59c8a739b5800e3741af995') {
        throw 'The original R3-R6-R3 projection.py has unreviewed changes.'
    }
    $staged = @(git diff --cached --name-only)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect git index.' }
    foreach ($path in @('phase168_r3_27_typed_statement_projection.py', 'phase168_r3_5_model_renderer.py')) {
        if ($staged -contains $path) {
            throw "Staged changes must be reviewed before R3R1: $path"
        }
    }
    Write-Output "PHASE174_R3R6R3R1_BRANCH=$branch"
    Write-Output "PHASE174_R3R6R3R1_LOCAL_HEAD=$head"
    Write-Output "PHASE174_R3R6R3R1_REMOTE_HEAD=$remote"
    if ($DryRun) {
        python -m phase174_r3_r6_r3r1_scoped_guard_fix.patch --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R3R1 DryRun failed; no production files changed.' }
    } else {
        python -m phase174_r3_r6_r3r1_scoped_guard_fix.patch --apply
        if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R3R1 Apply failed.' }
        Write-Output 'PHASE174_R3R6R3R1_FOCUSED_PYTEST_START'
        python -m pytest -q `
            phase174_r3_r6_r3r1_scoped_guard_fix/tests/test_patch.py `
            phase174_r3_r6_r3_common_narrative/tests/test_projection.py `
            phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
            phase174_r3_r6_source_extension/tests/test_source.py `
            phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py `
            phase172_r5_prior_reference_display/tests/test_projection.py
        if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed; Gate not certified.' }
        Write-Output 'PHASE174_R3R6R3R1_FOCUSED_PYTEST=PASS'
        Write-Output 'PHASE174_R3R6R3R1_GATE=PASS'
    }
} finally {
    Pop-Location
}
```
