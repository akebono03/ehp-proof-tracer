# Phase 173 R4-R15R11R2 — Complete source code

This file contains every executable package source file in full, including the repaired repeated-patch guard, the new regression test, and unchanged import blocks. No `...` omissions.

Production modules are changed only after the installer verifies their reviewed Git blobs. DryRun exports the complete changed class/function/import units to `FULL_CHANGED_UNITS.md`.

Reviewed GitHub develop HEAD: `7e9e00f42e8b125480cd2928b0ee7ec2c5269d3a`.

## `patch.py`

```python
"""Guarded, minimal R15R11 display-only transformations of reviewed sources."""
from __future__ import annotations

import ast
from pathlib import Path

EXPECTED_BLOBS = {
    "phase165_r52_r3_web_adapter.py": "a5c402c86e624010e5521ceda0cb1734ab32bcae",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_5_model_renderer.py": "6bfd5e992f6c9ee9441920e10e63e0db4bece289",
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py": "777db698e8da026571c8046b84fc3b875ee6dfe0",
}
EXPECTED_HEAD = "7e9e00f42e8b125480cd2928b0ee7ec2c5269d3a"


def _replace_once(source: str, before: str, after: str, *, label: str) -> str:
    """Reject already-applied replacements, even when the old anchor remains."""
    if after in source:
        raise RuntimeError(f"Unreviewed source or already patched anchor: {label}")
    if source.count(before) != 1:
        raise RuntimeError(f"Unreviewed source or duplicate anchor: {label}")
    return source.replace(before, after, 1)


def _patch_model(source: str) -> str:
    source = _replace_once(
        source,
        "from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus",
        "from phase165_r52_partial_proof import CertifiedAbstractStructure, PartialProofResult, ProofSearchStatus",
        label="model import",
    )
    source = _replace_once(
        source,
        "    diagnostics: tuple[str, ...] = ()\n\n\ndef root_ancestor_step_indices(",
        "    diagnostics: tuple[str, ...] = ()\n"
        "    abstract_structure: CertifiedAbstractStructure | None = None\n\n\n"
        "def root_ancestor_step_indices(",
        label="model dataclass field",
    )
    source = _replace_once(
        source,
        "        open_goals=result.open_goals,\n"
        "        diagnostics=result.diagnostics,\n"
        "    )",
        "        open_goals=result.open_goals,\n"
        "        diagnostics=result.diagnostics,\n"
        "        abstract_structure=result.abstract_structure,\n"
        "    )",
        label="model builder result",
    )
    return source


def _patch_model_renderer(source: str) -> str:
    source = _replace_once(
        source,
        "    incomplete = result.status is not ProofSearchStatus.COMPLETE\n",
        "    if model.abstract_structure is not result.abstract_structure:\n"
        "        raise ValueError(\"Narrative Model abstract certificate must match searched result\")\n"
        "    incomplete = result.status is not ProofSearchStatus.COMPLETE\n",
        label="model evidence identity check",
    )
    source = _replace_once(
        source,
        '        lines.extend(("", "未解決 Goal は証明済みの結論ではありません。"))\n'
        '    else:\n'
        '        lines.append("□")',
        '        if model.abstract_structure is not None:\n'
        '            from phase173_r4_r15r9_shared_abstract_renderer.projection import (\n'
        '                render_certified_abstract_model_section,\n'
        '            )\n'
        '            lines.extend(("", render_certified_abstract_model_section(model)))\n'
        '        lines.extend(("", "未解決 Goal は証明済みの結論ではありません。"))\n'
        '    else:\n'
        '        lines.append("□")',
        label="existing common Model Renderer terminal section",
    )
    return source


_WEB_BEFORE = '''        if narrative_model is None:\n            markdown = render_partial_proof_markdown(result)\n        else:\n            from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown\n            markdown = render_model_backed_narrative_markdown(result, narrative_model)\n        from phase173_r4_r15r9_shared_abstract_renderer.projection import (\n            render_certified_abstract_section,\n        )\n        abstract_markdown = render_certified_abstract_section(result)\n        if abstract_markdown:\n            markdown = markdown.rstrip() + "\\n\\n" + abstract_markdown + "\\n"\n        rendered_lines = _build_group_proof_rendered_lines(markdown)'''

_WEB_AFTER = '        if narrative_model is None:\n            # Preserve the existing legacy/compatibility narrative route.\n            markdown = render_partial_proof_markdown(result)\n            from phase173_r4_r15r9_shared_abstract_renderer.projection import (\n                render_certified_abstract_section,\n            )\n            abstract_markdown = render_certified_abstract_section(result)\n            if abstract_markdown:\n                markdown = markdown.rstrip() + "\\n\\n" + abstract_markdown + "\\n"\n        else:\n            from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown\n            markdown = render_model_backed_narrative_markdown(result, narrative_model)\n        rendered_lines = _build_group_proof_rendered_lines(markdown)'

def _patch_web(source: str) -> str:
    return _replace_once(source, _WEB_BEFORE, _WEB_AFTER, label="common web adapter block")


_PROJECTION_BEFORE = '''    target = result.target\n    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:\n        raise ValueError("abstract result has nonconcrete group dimensions")\n    invariant_latex = abstract_invariants_latex(structure.invariant_summands)\n    target_latex = rf"\\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"\n    return (\n        "## 証明済みの抽象群構造\\n\\n"\n        + rf"${target_latex} \\cong {invariant_latex}$."\n        + "\\n\\n"\n        + "これは出典検査済みの抽象群 ProofStep による結論であり、"\n        + "登録済みの先行 DB 群を前提とする。"\n        + "記名生成元の対応は未証明であり、上記の未解決 Goal と探索状態は変わらない。"\n    )\n'''

_PROJECTION_AFTER = '''    return _render_abstract_claim(result.target, structure)\n\n\ndef _render_abstract_claim(target: object, structure: CertifiedAbstractStructure) -> str:\n    """Format only an already certified abstract structure, never identify generators."""\n    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:\n        raise ValueError("abstract result has nonconcrete group dimensions")\n    invariant_latex = abstract_invariants_latex(structure.invariant_summands)\n    target_latex = rf"\\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"\n    return (\n        "## 証明済みの抽象群構造\\n\\n"\n        + rf"${target_latex} \\cong {invariant_latex}$."\n        + "\\n\\n"\n        + "これは出典検査済みの抽象群 ProofStep による結論であり、"\n        + "登録済みの先行 DB 群を前提とする。"\n        + "記名生成元の対応は未証明であり、上記の未解決 Goal と探索状態は変わらない。"\n    )\n\n\ndef render_certified_abstract_model_section(model: object) -> str:\n    """Render only certificate evidence explicitly carried by ProofNarrativeModel."""\n    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel\n\n    if not isinstance(model, ProofNarrativeModel):\n        raise TypeError("expected canonical ProofNarrativeModel")\n    structure = model.abstract_structure\n    if structure is None:\n        return ""\n    if (\n        not isinstance(structure, CertifiedAbstractStructure)\n        or structure.group != model.target\n        or model.status not in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)\n        or model.root_index is not None\n    ):\n        raise ValueError("unverified Model abstract result cannot be presented")\n    return _render_abstract_claim(model.target, structure)\n'''


def _patch_projection(source: str) -> str:
    source = _replace_once(
        source,
        "The common Web adapter invokes this function after its usual narrative has\n"
        "been rendered. No n/k special case and no alternate Narrative pipeline exists.",
        "The default Model-backed renderer and legacy Web adapter share this\n"
        "formatter. No n/k special case or alternate Narrative pipeline exists.",
        label="projection module purpose",
    )
    return _replace_once(source, _PROJECTION_BEFORE, _PROJECTION_AFTER, label="abstract projection formatter")


PATCHES = {
    "phase165_r52_r3_web_adapter.py": _patch_web,
    "phase168_r3_3_proof_narrative_model.py": _patch_model,
    "phase168_r3_5_model_renderer.py": _patch_model_renderer,
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py": _patch_projection,
}


def apply_to_source(relative: str, source: bytes) -> bytes:
    """Return proposed full-source replacement, preserving its original line ending."""
    if relative not in PATCHES:
        raise ValueError("unexpected target file")
    if b"\r\n" in source and b"\n" in source.replace(b"\r\n", b""):
        raise RuntimeError("Mixed EOLs in reviewed file")
    eol = b"\r\n" if b"\r\n" in source else b"\n"
    original = source.decode("utf-8")
    normalized = original.replace("\r\n", "\n")
    proposed = PATCHES[relative](normalized)
    if proposed == normalized:
        raise RuntimeError("Expected nonempty change")
    ast.parse(proposed, filename=relative)
    if eol == b"\r\n":
        proposed = proposed.replace("\n", "\r\n")
    return proposed.encode("utf-8")


def changed_units(relative: str, patched: bytes) -> str:
    """Export actual complete changed class/function and import block (not snippets)."""
    content = patched.decode("utf-8").replace("\r\n", "\n")
    tree = ast.parse(content)
    lines = content.splitlines()
    output = [f"## {relative}"]
    imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    if relative == "phase168_r3_3_proof_narrative_model.py":
        # All top-level imports appear before the first class definition.
        last_import = max(node.end_lineno for node in imports)
        output.extend(("### Changed complete import block", "```python", "\n".join(lines[:last_import]), "```"))
        names = {"ProofNarrativeModel", "build_proof_narrative_model"}
    elif relative == "phase165_r52_r3_web_adapter.py":
        last_import = max(node.end_lineno for node in imports)
        output.extend(("### Complete unchanged import block", "```python", "\n".join(lines[:last_import]), "```"))
        names = {"build_partial_web_group_proof_view"}
    elif relative == "phase168_r3_5_model_renderer.py":
        names = {"render_model_backed_narrative_markdown"}
    else:
        names = {"render_certified_abstract_section", "_render_abstract_claim", "render_certified_abstract_model_section"}
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name in names:
            start = min((dec.lineno for dec in node.decorator_list), default=node.lineno)
            output.extend((f"### Complete {node.name}", "```python", "\n".join(lines[start-1:node.end_lineno]), "```"))
    assert all(any(f"### Complete {name}" == item for item in output) for name in names)
    return "\n\n".join(output) + "\n"
```

## `install.py`

```python
"""R15R11 guarded, reversible integration of abstract certificates into Narrative Model."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from .patch import EXPECTED_BLOBS, EXPECTED_HEAD, apply_to_source, changed_units


def _git(root: Path, *args: str) -> str:
    p = subprocess.run(("git", *args), cwd=root, check=True,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout.strip()


def _hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        tmp.write(raw)
        temp = Path(tmp.name)
    os.replace(temp, path)


def preflight(root: Path) -> dict[str, tuple[bytes, bytes]]:
    root = root.resolve()
    if _git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R15R11 requires develop")
    if _git(root, "rev-parse", "origin/develop") != EXPECTED_HEAD:
        raise RuntimeError("GitHub develop HEAD changed; rereview before applying")
    if _git(root, "rev-parse", "HEAD") != EXPECTED_HEAD:
        raise RuntimeError("Local HEAD does not match reviewed GitHub HEAD")
    if _git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Review staged changes before applying")
    proposal: dict[str, tuple[bytes, bytes]] = {}
    for rel, sha in EXPECTED_BLOBS.items():
        path = root / rel
        if not path.is_file():
            raise RuntimeError(f"Missing reviewed file: {rel}")
        actual = _git(root, "hash-object", f"--path={rel}", rel)
        if actual != sha:
            raise RuntimeError(f"Unreviewed {rel}: expected {sha}; got {actual}")
        original = path.read_bytes()
        new = apply_to_source(rel, original)
        proposal[rel] = (original, new)
    return proposal


def emit_review(package: Path, proposal: dict[str, tuple[bytes, bytes]]) -> None:
    sections = ["# Phase 173 R4-R15R11 — Full changed units (reviewed proposed code)",
                "", "Every changed class/function is shown in full. No omitted code.", ""]
    for rel, (_, patched) in proposal.items():
        sections.append(changed_units(rel, patched))
    _atomic_write(package / "FULL_CHANGED_UNITS.md", "\n".join(sections).encode("utf-8"))


def apply(root: Path, package: Path) -> None:
    proposal = preflight(root)
    state = package / "installed_state.json"
    backup_dir = package / "backups"
    if state.exists() or backup_dir.exists():
        raise RuntimeError("Existing R15R11 installation state requires review")
    emit_review(package, proposal)
    backups: dict[str, dict[str, str]] = {}
    for rel, (original, proposed) in proposal.items():
        backups[rel] = {"original_sha256": _hash(original), "patched_sha256": _hash(proposed)}
    written = []
    try:
        for rel, (original, proposed) in proposal.items():
            backup = backup_dir / rel
            _atomic_write(backup, original)
            _atomic_write(root / rel, proposed)
            written.append(rel)
        _atomic_write(state, json.dumps(backups, indent=2, ensure_ascii=False).encode("utf-8"))
    except Exception:
        for rel in reversed(written):
            _atomic_write(root / rel, proposal[rel][0])
        raise
    print("PHASE173_R4_R15R11_PATCHED_FILES=" + str(len(proposal)), flush=True)


def restore(root: Path, package: Path) -> None:
    state = package / "installed_state.json"
    if not state.is_file():
        raise RuntimeError("No prior R15R11 installation state")
    data = json.loads(state.read_text(encoding="utf-8"))
    if set(data) != set(EXPECTED_BLOBS):
        raise RuntimeError("Installation state does not match reviewed target files")
    for rel, checks in data.items():
        original = (package / "backups" / rel).read_bytes()
        current = (root / rel).read_bytes()
        if _hash(original) != checks["original_sha256"]:
            raise RuntimeError("Backup mismatch, refusing restore")
        if _hash(current) != checks["patched_sha256"]:
            raise RuntimeError(f"User has modified {rel}; refusing to overwrite")
    for rel in data:
        _atomic_write(root / rel, (package / "backups" / rel).read_bytes())
    state.unlink()
    print("PHASE173_R4_R15R11_RESTORED=PASS", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--restore", action="store_true")
    opts = p.parse_args()
    if sum((opts.dry_run, opts.apply, opts.restore)) != 1:
        p.error("Choose one operation")
    package = Path(__file__).resolve().parent
    if opts.restore:
        restore(opts.root, package)
        return
    proposal = preflight(opts.root)
    emit_review(package, proposal)
    print("PHASE173_R4_R15R11_SOURCE_GUARD=PASS", flush=True)
    if opts.dry_run:
        print("PHASE173_R4_R15R11_DRY_RUN=PASS", flush=True)
        print("PHASE173_R4_R15R11_PRODUCTION_EDIT=NONE", flush=True)
        return
    apply(opts.root, package)


if __name__ == "__main__":
    main()
```

## `audit.py`

```python
"""Post-install audit of proof/status and Web Narrative Model integration."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


def inspect(k: int) -> dict[str, object]:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    model = build_proof_narrative_model(result)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    ready = (
        result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        and result.conclusion is None and bool(result.open_goals)
        and model.abstract_structure is result.abstract_structure
        and model.abstract_structure is not None
        and headings.count("証明済みの抽象群構造") == 1
        and headings.count("未解決 Goal") == 1
        and view.key == "generic-partial-proof" and view.partial_result
    )
    return {
        "k": k, "model_abstract_certified": model.abstract_structure is not None,
        "model_same_certificate": model.abstract_structure is result.abstract_structure,
        "citations": len(model.citations), "open_goals": len(result.open_goals),
        "abstract_section_count": headings.count("証明済みの抽象群構造"),
        "web_key": view.key, "named_pending": view.partial_result,
        "passed": ready,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    opts = p.parse_args()
    rows = [inspect(k) for k in (8, 31)]
    complete = []
    for n, k in ((3, 3), (4, 3)):
        view = build_standard_web_group_proof_view(
            n=n, k=k, mode="narrative", citation_source="model",
        )
        complete.append({"n": n, "k": k,
                         "passed": view.key == "generic-complete-proof"
                                   and not view.partial_result})
    if not all(r["passed"] for r in rows + complete):
        raise RuntimeError("Source-first Narrative Model regression")
    report = {"phase": "173-R4-R15R11", "model_abstract_integrated": True,
              "normal_model_route_owns_abstract_section": True,
              "legacy_route_preserved": True, "named_proof_promoted": False,
              "phase_completed": False, "full_pytest_performed": False,
              "abstract_rows": rows, "complete_rows": complete, "passed": True}
    opts.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(f"PHASE173_R4_R15R11_K={row['k']} MODEL_HAS_ABSTRACT={row['model_abstract_certified']} "
              f"ABSTRACT_SECTION_COUNT={row['abstract_section_count']} "
              f"OPEN_GOALS={row['open_goals']} NAMED_PENDING={row['named_pending']}", flush=True)
    print("PHASE173_R4_R15R11_AUDIT=PASS", flush=True)
    print("PHASE173_R4_R15R11_PHASE_COMPLETED=False", flush=True)


if __name__ == "__main__":
    main()
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedHead = '7e9e00f42e8b125480cd2928b0ee7ec2c5269d3a'
Push-Location $RepoRoot
try {
    if ((git branch --show-current).Trim() -ne 'develop') {
        throw 'R15R11 requires the develop branch'
    }
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R11 git fetch failed' }
    $RemoteHead = (git rev-parse origin/develop).Trim()
    if ($RemoteHead -ne $ExpectedHead) {
        throw "GitHub develop HEAD changed: $RemoteHead (expected $ExpectedHead). Review again."
    }
    $LocalHead = (git rev-parse HEAD).Trim()
    if ($LocalHead -ne $ExpectedHead) {
        throw "Local HEAD $LocalHead differs from reviewed GitHub HEAD $ExpectedHead. Inspect git status and use git pull --ff-only only when safe."
    }
    Write-Output 'PHASE173_R4_R15R11R1_HEAD_LINEAGE=PASS'

    if ($DryRun) {
        python -m phase173_r4_r15r11_model_abstract_integration.install --root "$RepoRoot" --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R15R11 source guard failed' }
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r11_model_abstract_integration/tests/test_static.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R11 dry-run source tests failed' }
        Write-Output 'PHASE173_R4_R15R11_DRY_RUN_TESTS=PASS'
        Write-Output 'PHASE173_R4_R15R11_PRODUCTION_EDIT=NONE'
    } else {
        python -m phase173_r4_r15r11_model_abstract_integration.install --root "$RepoRoot" --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R15R11 source guard failed' }
        python -m phase173_r4_r15r11_model_abstract_integration.install --root "$RepoRoot" --apply
        if ($LASTEXITCODE -ne 0) { throw 'R15R11 installation failed' }
        try {
            python -m pytest -q -p no:cacheprovider `
                phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py `
                phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py `
                phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection_isolated.py `
                phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py `
                phase173_r4_r11_zero_public_connection/tests/test_route.py `
                phase173_r4_r15r10_common_route_audit/tests/test_contract.py
            if ($LASTEXITCODE -ne 0) { throw 'R15R11 focused pytest failed' }
            Write-Output 'PHASE173_R4_R15R11_FOCUSED_PYTEST=PASS'
            python -m phase173_r4_r15r11_model_abstract_integration.audit `
                --output (Join-Path $PSScriptRoot 'model_abstract_report.json')
            if ($LASTEXITCODE -ne 0) { throw 'R15R11 Web/Model audit failed' }
            Write-Output 'PHASE173_R4_R15R11_PRODUCTION_EDIT=4_FILES'
        } catch {
            python -m phase173_r4_r15r11_model_abstract_integration.install --root "$RepoRoot" --restore
            throw
        }
    }
} finally {
    Pop-Location
}
```

## `tests/test_static.py`

```python
"""Source guards and syntactic contracts before installing a production patch."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r11_model_abstract_integration.install import preflight
from phase173_r4_r15r11_model_abstract_integration.patch import (
    EXPECTED_BLOBS,
    apply_to_source,
    changed_units,
)

ROOT = Path(__file__).resolve().parents[2]


def test_reviewed_source_can_be_replaced_atomically_and_parses() -> None:
    proposal = preflight(ROOT)
    assert set(proposal) == set(EXPECTED_BLOBS)
    for rel, (original, changed) in proposal.items():
        assert changed != original
        ast.parse(changed.decode("utf-8"), filename=rel)
        full = changed_units(rel, changed)
        assert "### Complete" in full
        assert "```python" in full


def test_patch_is_fail_closed_on_repetition_and_crlf() -> None:
    for rel, (original, updated) in preflight(ROOT).items():
        with pytest.raises(RuntimeError, match="Unreviewed"):
            apply_to_source(rel, updated)
        if b"\r\n" not in original:
            crlf = original.replace(b"\n", b"\r\n")
            rewritten = apply_to_source(rel, crlf)
            assert b"\r\n" in rewritten
            assert rewritten.count(b"\n") == rewritten.count(b"\r\n")
            ast.parse(rewritten.decode("utf-8"))


def test_renderer_reapplication_rejected_when_old_anchor_survives() -> None:
    """An inserted block must not be duplicated if it contains the old anchor."""
    source = (
        "def render_model_backed_narrative_markdown(result, model):\n"
        "    incomplete = result.status is not ProofSearchStatus.COMPLETE\n"
        "    if incomplete:\n"
        '        lines.extend(("", "未解決 Goal は証明済みの結論ではありません。"))\n'
        "    else:\n"
        '        lines.append("□")\n'
    ).encode("utf-8")
    relative = "phase168_r3_5_model_renderer.py"
    updated = apply_to_source(relative, source)
    assert updated.count(b"if model.abstract_structure is not result.abstract_structure:") == 1
    with pytest.raises(RuntimeError, match="already patched"):
        apply_to_source(relative, updated)


def test_model_and_web_have_no_dimension_specific_branches() -> None:
    proposal = preflight(ROOT)
    for rel in (
        "phase165_r52_r3_web_adapter.py",
        "phase168_r3_3_proof_narrative_model.py",
        "phase173_r4_r15r9_shared_abstract_renderer/projection.py",
    ):
        new_source = proposal[rel][1].decode("utf-8")
        tree = ast.parse(new_source)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare):
                continue
            operands = (node.left, *node.comparators)
            has_nk = any(
                isinstance(term, ast.Name) and term.id in ("n", "k")
                for operand in operands for term in ast.walk(operand)
            )
            has_integer = any(
                isinstance(term, ast.Constant) and type(term.value) is int
                for operand in operands for term in ast.walk(operand)
            )
            assert not (has_nk and has_integer), f"Specialized display: {rel}:{node.lineno}"


def test_old_adapter_model_branch_does_not_append_abstract_twice() -> None:
    web_source = preflight(ROOT)["phase165_r52_r3_web_adapter.py"][1].decode("utf-8")
    assert web_source.count("render_certified_abstract_section(result)") == 1
    assert web_source.count("render_model_backed_narrative_markdown(result, narrative_model)") == 1
    renderer = preflight(ROOT)["phase168_r3_5_model_renderer.py"][1].decode("utf-8")
    assert renderer.count("render_certified_abstract_model_section(model)") == 1
    assert web_source.count("_build_group_proof_rendered_lines(markdown)") == 1
    assert '"generic-complete-proof"' in web_source
    assert '"generic-partial-proof"' in web_source
```

## `tests/test_integration.py`

```python
"""Real source-first abstract evidence through the one canonical Narrative Model."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import (
    render_model_backed_narrative_markdown,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    render_certified_abstract_section,
    render_certified_abstract_model_section,
)
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _build_group_proof_rendered_lines


@pytest.mark.parametrize("k", (8, 31))
def test_source_first_certificate_is_owned_by_model_and_rendered_once(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    model = build_proof_narrative_model(result)
    assert result.abstract_structure is not None
    assert model.abstract_structure is result.abstract_structure
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    abstract = render_certified_abstract_model_section(model)
    assert abstract == render_certified_abstract_section(result)
    after = render_model_backed_narrative_markdown(result, model)
    assert after.count("## 証明済みの抽象群構造") == 1
    assert abstract in after
    assert "## 未解決 Goal" in after
    direct_view = build_partial_web_group_proof_view(
        result, mode="narrative", narrative_model=model,
    )
    assert direct_view.rendered_lines == _build_group_proof_rendered_lines(after)
    assert direct_view.key == "generic-partial-proof" and direct_view.partial_result
    assert result.abstract_structure.proof_step not in result.proven_steps
    assert model.open_goals == result.open_goals
    assert model.diagnostics == result.diagnostics


@pytest.mark.parametrize("k", (8, 31))
def test_public_default_path_and_legacy_path_keep_one_abstract_section(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    for citation_source in ("model", "legacy"):
        view = build_standard_web_group_proof_view(
            n=4, k=k, goal=goal, mode="narrative", citation_source=citation_source,
        )
        headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
        assert headings.count("証明済みの抽象群構造") == 1
        if citation_source == "model":
            assert headings.count("未解決 Goal") == 1
        assert view.key == "generic-partial-proof"
        assert view.partial_result


def test_mismatched_narrative_model_fails_closed() -> None:
    goal = exact_prior_database_result(4, 8)
    result = search_group_from_registered_goal(n=4, k=8, goal=goal)
    model = build_proof_narrative_model(result)
    assert model.abstract_structure is not None
    with pytest.raises(ValueError, match="abstract certificate must match"):
        render_model_backed_narrative_markdown(
            result, replace(model, abstract_structure=None),
        )
    with pytest.raises(ValueError, match="partial state must match"):
        render_model_backed_narrative_markdown(
            result, replace(model, status=ProofSearchStatus.COMPLETE),
        )
    with pytest.raises(ValueError, match="unverified Model abstract"):
        render_certified_abstract_model_section(replace(model, root_index=0))


@pytest.mark.parametrize("n,k", ((3, 3), (4, 3)))
def test_existing_completed_web_proofs_remain_complete(n: int, k: int) -> None:
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert view.rendered_lines
    assert not any(
        line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
        for line in view.rendered_lines
    )
```

## `__init__.py`

```python
"""Phase 173 R4-R15R11 common Narrative Model abstract integration."""
```

## `tests/__init__.py`

```python
"""R15R11 regression tests."""
```
