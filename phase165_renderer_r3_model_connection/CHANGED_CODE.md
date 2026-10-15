# Phase 165 Renderer R3 変更コード全文

対象：`toda_group_proof_narrative_renderer.py` に `render_narrative_proof_model` を末尾追加。`phase165_r52_partial_proof.py` の `render_partial_proof_markdown` を関数単位で置換。両ファイルの既存 import は変更なし。新規補助ファイルは ZIP の該当ディレクトリに追加。

## render_narrative_proof_model.py.txt

```python
def render_narrative_proof_model(model) -> str:
    """Dispatch normalized evidence through the established Narrative implementation.

    The original completed adapter retains its historical fidelity safeguards.
    This function never creates, certifies, or changes a ProofStep.
    """
    from phase165_renderer_narrative_model import NarrativeProofModel
    from phase165_r52_partial_proof import ProofSearchStatus

    if not isinstance(model, NarrativeProofModel):
        raise TypeError("model must be NarrativeProofModel")
    if model.source_kind == "presentation":
        return render_toda_group_proof_narrative_markdown(model.source)
    if model.source_kind != "search_result":
        raise ValueError("unrecognized Narrative model source")
    if model.status is ProofSearchStatus.COMPLETE:
        from phase165_r56_presentation_adapter import render_completed_shared_narrative
        return render_completed_shared_narrative(model.source)
    return render_toda_partial_proof_narrative_markdown(model.source)
```

## render_partial_proof_markdown.py.txt

```python
def render_partial_proof_markdown(result: PartialProofResult) -> str:
    """Use the R2 shared model and the canonical Narrative dispatch for any state."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    from phase165_renderer_narrative_model import build_narrative_proof_model
    from toda_group_proof_narrative_renderer import render_narrative_proof_model

    return render_narrative_proof_model(build_narrative_proof_model(result))
```

## install.py

```python
"""Guarded R3 connector installation; no search or established prose modification."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def function_nodes(source: str, name: str) -> tuple[ast.FunctionDef, ...]:
    return tuple(
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )


def function_text(source: str, node: ast.FunctionDef) -> str:
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def replace_function(source: str, node: ast.FunctionDef, new: str) -> str:
    lines = source.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno - 1]) + new.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated


def install(project: Path, package: Path) -> str:
    primary = project / "toda_group_proof_narrative_renderer.py"
    partial = project / "phase165_r52_partial_proof.py"
    model = project / "phase165_renderer_narrative_model.py"
    if not all(path.is_file() for path in (primary, partial, model)):
        raise FileNotFoundError("R2 model or established Narrative sources missing")
    old_primary = primary.read_text(encoding="utf8")
    old_partial = partial.read_text(encoding="utf8")
    dispatcher = (package / "render_narrative_proof_model.py.txt").read_text(encoding="utf8")
    public = (package / "render_partial_proof_markdown.py.txt").read_text(encoding="utf8")
    assert len(function_nodes(dispatcher, "render_narrative_proof_model")) == 1
    assert len(function_nodes(public, "render_partial_proof_markdown")) == 1
    nodes = function_nodes(old_partial, "render_partial_proof_markdown")
    if len(nodes) != 1:
        raise RuntimeError("unexpected public renderer wrapper definitions")
    old_wrapper = function_text(old_partial, nodes[0])
    if old_wrapper.rstrip() != public.rstrip() and not all(
        token in old_wrapper for token in (
            "render_completed_shared_narrative",
            "render_toda_partial_proof_narrative_markdown",
        )
    ):
        raise RuntimeError("unrecognized public wrapper; refusing overwrite")
    if len(function_nodes(old_primary, "render_toda_group_proof_narrative_markdown")) < 1:
        raise RuntimeError("established complete renderer missing")
    if len(function_nodes(old_primary, "render_toda_partial_proof_narrative_markdown")) != 1:
        raise RuntimeError("established partial renderer missing")
    current = function_nodes(old_primary, "render_narrative_proof_model")
    if len(current) > 1:
        raise RuntimeError("duplicate dispatcher definitions")
    if current and function_text(old_primary, current[0]).rstrip() != dispatcher.rstrip():
        raise RuntimeError("conflicting existing dispatcher")
    new_primary = old_primary if current else old_primary.rstrip() + "\n\n\n" + dispatcher.rstrip() + "\n"
    new_partial = replace_function(old_partial, nodes[0], public)
    if new_primary == old_primary and new_partial == old_partial:
        return "ALREADY_INSTALLED"
    ast.parse(new_primary)
    ast.parse(new_partial)
    backup = project / ".phase165_renderer_r3_backup"
    if backup.exists():
        raise RuntimeError("R3 backup already exists: refusing overwrite")
    backup.mkdir()
    try:
        shutil.copy2(primary, backup / primary.name)
        shutil.copy2(partial, backup / partial.name)
        primary.write_text(new_primary, encoding="utf8")
        partial.write_text(new_partial, encoding="utf8")
    except BaseException:
        shutil.copy2(backup / primary.name, primary)
        shutil.copy2(backup / partial.name, partial)
        raise
    return "INSTALLED"


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    print("Phase165 Renderer R3:", install(folder.parent, folder))
    print("Only public entry and canonical dispatcher changed; full pytest NOT run")
```

## restore.py

```python
"""Restore the two R3-modified files from the guarded backup."""
from __future__ import annotations

from pathlib import Path
import shutil


def restore(project: Path) -> None:
    backup = project / ".phase165_renderer_r3_backup"
    for name in (
        "toda_group_proof_narrative_renderer.py",
        "phase165_r52_partial_proof.py",
    ):
        original = backup / name
        if not original.is_file():
            raise FileNotFoundError(f"missing backup: {original}")
        shutil.copy2(original, project / name)


if __name__ == "__main__":
    restore(Path(__file__).resolve().parent.parent)
    print("R3 original renderer entry files restored")
```

## snapshot.py

```python
"""Compare exact completed/partial markdown before/after the guarded install."""
from __future__ import annotations

import json
from pathlib import Path
import sys

from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def snapshot() -> dict[str, str]:
    complete = search_group_from_registered_goal(n=2, k=1)
    partial = search_group_from_registered_goal(n=3, k=1)
    return {
        "completed_public": render_partial_proof_markdown(complete),
        "completed_adapter": render_completed_shared_narrative(complete),
        "incomplete_public": render_partial_proof_markdown(partial),
    }


def main() -> None:
    mode, filename = sys.argv[1:]
    path = Path(filename)
    values = snapshot()
    if mode == "before":
        path.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf8")
        print("R3 baseline saved")
    elif mode == "after":
        baseline = json.loads(path.read_text(encoding="utf8"))
        if baseline != values:
            changed = [key for key in values if baseline.get(key) != values[key]]
            raise AssertionError(f"Narrative regression: {changed}")
        print("R3 exact completed/partial Narrative parity confirmed")
    else:
        raise ValueError("expected before or after")


if __name__ == "__main__":
    main()
```

## test_r3.py

```python
"""R3 focused routing and evidence-preservation checks."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase165_r52_partial_proof import (
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from phase165_renderer_narrative_model import build_narrative_proof_model
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative
from toda_group_proof_narrative_renderer import (
    render_narrative_proof_model,
    render_toda_partial_proof_narrative_markdown,
)


def test_r3_completed_public_uses_original_narrative():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    assert render_partial_proof_markdown(result) == render_completed_shared_narrative(result)


def test_r3_incomplete_public_uses_original_partial_narrative():
    result = search_group_from_registered_goal(n=3, k=1)
    assert result.status is not ProofSearchStatus.COMPLETE
    assert render_partial_proof_markdown(result) == render_toda_partial_proof_narrative_markdown(result)


def test_r3_large_unsearched_target_preserved():
    result = make_partial_proof_result(n=200, k=90, status=ProofSearchStatus.NOT_SEARCHED)
    markdown = render_partial_proof_markdown(result)
    assert r"\pi_{290}^{200}" in markdown
    assert "□" not in markdown


def test_r3_model_dispatch_identity():
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.SEARCH_FAILED,
        diagnostics=("missing premise",), open_goals=("goal",),
    )
    model = build_narrative_proof_model(result)
    assert model.source is result
    assert render_narrative_proof_model(model) == render_partial_proof_markdown(result)


def test_r3_dispatch_rejects_non_model():
    with pytest.raises(TypeError):
        render_narrative_proof_model(object())


def test_r3_public_only_dispatches_through_model():
    text = (Path(__file__).resolve().parent.parent / "phase165_r52_partial_proof.py").read_text(encoding="utf8")
    assert "render_narrative_proof_model(build_narrative_proof_model(result))" in text


def test_r3_does_not_restore_duplicate_generic_file():
    project = Path(__file__).resolve().parent.parent
    assert not (project / "toda_group_proof_generic_narrative_renderer.py").exists()
```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { $project } else { "$project$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
$baseline = Join-Path $package 'baseline.json'
& $python (Join-Path $package 'snapshot.py') before $baseline
if ($LASTEXITCODE -ne 0) { throw 'R3 baseline failed; no changes made' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R3 installation failed' }
& $python -m pytest -q (Join-Path $package 'test_r3.py')
$code = $LASTEXITCODE
if ($code -eq 0) {
    & $python (Join-Path $package 'snapshot.py') after $baseline
    $code = $LASTEXITCODE
}
if ($code -ne 0) {
    Write-Output 'R3 regression; restoring two files'
    & $python (Join-Path $package 'restore.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3 rollback failed; inspect .phase165_renderer_r3_backup' }
    throw 'R3 targeted test or exact Markdown regression; original files restored'
}
Write-Output 'R3 shared model entry connected; 7 targeted tests passed; full pytest NOT run.'
```

