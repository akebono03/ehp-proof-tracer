# Phase 173 R4-R15R16R3 — 変更部分とコード全文

## 変更対象

- `phase173_r4_r15r16r3_staged_guard_fix/install.py`: `source_guard()` — staged 対象の検査と index 保全.
- `phase173_r4_r15r16r3_staged_guard_fix/run.ps1`: DryRun / 限定 pytest / ロールバック.
- `phase173_r4_r15r16r3_staged_guard_fix/tests/test_staged_guard.py`: 新規の staged 操作テスト.
- `phase173_r4_r15r16r3_staged_guard_fix/tree_adapter.py`: R15R16R2 と同じ検証済み証明木 adapter.
- `phase173_r4_r15r16r3_staged_guard_fix/patches.py`: R15R16R2 と同じ本番パッチ (呼出先のパッケージ名のみ更新).
- 本番側の2ファイルへの適用内容は R15R16R2 と同じ. 証明探索への変更なし.

## `install.py` の import 全文

```python
from __future__ import annotations
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
from .patches import TRANSFORMERS, patch_progress, patch_test
from phase173_r4_r15r16_verified_progress_punctuation.projection_patch import (
    patch_projection, patch_layout,
)
```

## `source_guard()` の全文

```python
def source_guard() -> str:
    branch = git("branch", "--show-current")
    local = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if branch != "develop" or local != remote:
        raise RuntimeError("develop branch or local/remote HEAD mismatch")
    if command("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD").returncode != 0:
        raise RuntimeError("HEAD is not descended from reviewed R15R15")
    # A staged change is not inherently unsafe. Never alter the index. Review
    # only overlaps with the files this installer reads or replaces. Unrelated
    # staged edits are left in place without being examined or rewritten.
    staged_paths = set(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    reviewed_paths = {PROJECTION, LAYOUT, PREVIOUS_PATCH, PREVIOUS_TEST}
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.is_file() else None
    for name in sorted(staged_paths & reviewed_paths):
        indexed = subprocess.run(
            ["git", "show", ":" + name], cwd=ROOT, capture_output=True,
            check=False,
        )
        if indexed.returncode != 0:
            raise RuntimeError("staged reviewed file cannot be read: " + name)
        if state is not None and name in TRANSFORMERS:
            # On a rerun after installation, the index may still contain the
            # original R15R16 bytes while the working tree has R15R16R3.
            expected_index = read_backup(state, name)
        else:
            expected_index = (ROOT / name).read_bytes()
        # Git may store LF-normalized blobs while the Windows worktree uses
        # CRLF. Only newline normalization is allowed; content must still match.
        if clean_text(indexed.stdout) != clean_text(expected_index):
            raise RuntimeError(
                "staged reviewed file differs from expected original: " + name
            )
    print("R15R16R3_STAGED_PATH_COUNT=" + str(len(staged_paths)), flush=True)
    print("R15R16R3_REVIEWED_STAGED_FILES=" + str(len(staged_paths & reviewed_paths)), flush=True)
    print("R15R16R3_INDEX_MODIFIED=False", flush=True)
    for name, expected in REVIEWED_BLOBS.items():
        if git("rev-parse", "HEAD:" + name) != expected:
            raise RuntimeError("reviewed GitHub code changed: " + name)
    changed = set(filter(None, git("diff", "--name-only").splitlines()))
    allowed = {PROJECTION, LAYOUT}
    if STATE.is_file():
        allowed.update(TRANSFORMERS)
    if not changed.issubset(allowed):
        raise RuntimeError("unexpected local changes: " + ", ".join(sorted(changed - allowed)))
    if not (ROOT / PREVIOUS_PATCH).is_file() or (
        sha256((ROOT / PREVIOUS_PATCH).read_bytes()).hexdigest()
        != PREVIOUS_PATCH_SHA256
    ):
        raise RuntimeError("R15R16 prior patch file is missing or changed")
    for name in (PROJECTION, LAYOUT, PREVIOUS_TEST):
        path = ROOT / name
        if not path.is_file():
            raise RuntimeError("reviewed R15R16 source missing: " + name)
        if STATE.exists() and name in TRANSFORMERS:
            continue
        expected = expected_prior_local(name, path.read_bytes())
        if path.read_bytes() != expected:
            raise RuntimeError("R15R16 previous patch not applied as reviewed: " + name)
    print("R15R16R3_BRANCH=" + branch, flush=True)
    print("R15R16R3_LOCAL_HEAD=" + local, flush=True)
    print("R15R16R3_REMOTE_HEAD=" + remote, flush=True)
    print("R15R16R3_REVIEWED_ANCESTOR=" + REVIEWED_HEAD, flush=True)
    print("R15R16R3_SOURCE_GUARD=PASS", flush=True)
    return local
```

## `run.ps1` の全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 git fetch failed' }

    python -m phase173_r4_r15r16r3_staged_guard_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 source guard failed' }

    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r16r3_staged_guard_fix/tests/test_preview.py `
        phase173_r4_r15r16r3_staged_guard_fix/tests/test_staged_guard.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 preview tests failed' }

    if ($DryRun) {
        Write-Output 'R15R16R3_DRY_RUN=PASS'
        Write-Output 'R15R16R3_PHASE_COMPLETED=False'
        exit 0
    }

    python -m phase173_r4_r15r16r3_staged_guard_fix.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 install failed' }
    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r16r3_staged_guard_fix/tests/test_preview.py `
            phase173_r4_r15r16r3_staged_guard_fix/tests/test_adapter_unit.py `
            phase173_r4_r15r16r3_staged_guard_fix/tests/test_integration.py `
            phase173_r4_r15r16_verified_progress_punctuation/tests/test_contract.py `
            phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py `
            phase173_r4_r15r15_abstract_result_banner/tests/test_integration.py `
            phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 focused regression failed' }
        Write-Output 'R15R16R3_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R16R3_FULL_PYTEST_RUN=False'
        Write-Output 'R15R16R3_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r16r3_staged_guard_fix.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R16R3 rollback requires inspection' }
        throw
    }
} finally {
    Pop-Location
}
```

## 新規 staged テストの全文 (import を含む)

```python
"""Index preservation and overlap validation in an isolated repository."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

from phase173_r4_r15r16r3_staged_guard_fix import install as installer


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=root, check=True,
        capture_output=True, text=True, encoding="utf-8",
    )
    return proc.stdout.strip()


def _setup_repo(tmp_path: Path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", "develop")
    _git(root, "config", "user.email", "tester@example.org")
    _git(root, "config", "user.name", "Guard Test")
    for name in (installer.PROJECTION, installer.LAYOUT, installer.PREVIOUS_PATCH,
                 installer.PREVIOUS_TEST):
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("fixed prior reviewed content\n", encoding="utf-8")
    (root / "other.txt").write_text("original\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "baseline")
    head = _git(root, "rev-parse", "HEAD")
    (root / ".git" / "refs" / "remotes" / "origin").mkdir(parents=True)
    _git(root, "update-ref", "refs/remotes/origin/develop", head)
    monkeypatch.setattr(installer, "ROOT", root)
    monkeypatch.setattr(installer, "REVIEWED_HEAD", head)
    monkeypatch.setattr(installer, "REVIEWED_BLOBS", {
        name: _git(root, "rev-parse", "HEAD:" + name)
        for name in (installer.PROJECTION, installer.LAYOUT)
    })
    monkeypatch.setattr(installer, "PREVIOUS_PATCH_SHA256", installer.sha256(
        (root / installer.PREVIOUS_PATCH).read_bytes()).hexdigest()
    )
    monkeypatch.setattr(installer, "PREVIOUS_TEST_SHA256", installer.sha256(
        (root / installer.PREVIOUS_TEST).read_bytes()).hexdigest()
    )
    monkeypatch.setattr(installer, "STATE", root / "state.json")
    monkeypatch.setattr(installer, "BACKUP", root / "backups")
    monkeypatch.setattr(
        installer, "expected_prior_local", lambda name, current: current,
    )
    return root


def test_unrelated_staged_edits_are_preserved(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    (root / "other.txt").write_text("user staged edit\n", encoding="utf-8")
    _git(root, "add", "other.txt")
    before = _git(root, "write-tree")
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")
    assert _git(root, "write-tree") == before
    assert (root / "other.txt").read_text() == "user staged edit\n"


def test_reviewed_staged_file_equal_worktree_is_allowed(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    # A real staged change is allowed only if the staged bytes and the
    # reviewed pre-install working tree bytes are exactly equal.
    target = root / installer.PROJECTION
    target.write_text("staged and reviewed prior state\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    before = _git(root, "write-tree")
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")
    assert _git(root, "write-tree") == before


def test_reviewed_staged_file_divergence_is_rejected(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    target = root / installer.PROJECTION
    target.write_text("staged prior candidate\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    target.write_text("fixed prior reviewed content\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="staged reviewed file differs"):
        installer.source_guard()


def test_stage_safe_restore_reads_original_backup(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    target = root / installer.PROJECTION
    target.write_text("newly staged reviewed change\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    target.write_text("installed patch output\n", encoding="utf-8")
    backup = root / "backups"
    backup.mkdir()
    (backup / "source_0.backup").write_bytes(b"newly staged reviewed change\n")
    state = {"files": {installer.PROJECTION: {
        "backup": "source_0.backup", "original_sha256": installer.sha256(
            b"newly staged reviewed change\n").hexdigest(),
    }}}
    installer.STATE.write_text(json.dumps(state), encoding="utf-8")
    # Here source_guard must skip the worktree equality test for staged
    # patched files, while proving the staged index is still the backup.
    monkeypatch.setattr(installer, "expected_prior_local", lambda name, current: current)
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")


def test_install_and_restore_preserve_staged_index(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    target = root / installer.PROJECTION
    target.write_text("VALUE = 1\n", encoding="utf-8")
    _git(root, "add", installer.PROJECTION)
    (root / "other.txt").write_text("user work kept in index\n", encoding="utf-8")
    _git(root, "add", "other.txt")
    index_before = _git(root, "write-tree")
    original = target.read_bytes()
    monkeypatch.setattr(installer, "TRANSFORMERS", {
        installer.PROJECTION: lambda source: source + "# tested patch\n",
    })

    installer.install()
    assert target.read_bytes() == original + b"# tested patch\n"
    assert _git(root, "write-tree") == index_before
    assert _git(root, "show", ":" + installer.PROJECTION) == "VALUE = 1"
    assert (root / "other.txt").read_text() == "user work kept in index\n"

    # Re-running preflight is allowed even though the staged index keeps the
    # reviewed R15R16 bytes and the worktree contains the installed patch.
    installer.preflight()
    assert _git(root, "write-tree") == index_before

    installer.restore()
    assert target.read_bytes() == original
    assert _git(root, "write-tree") == index_before
    assert not installer.STATE.exists()


def test_windows_crlf_staged_blob_is_semantically_identical(tmp_path, monkeypatch):
    root = _setup_repo(tmp_path, monkeypatch)
    _git(root, "config", "core.autocrlf", "true")
    target = root / installer.PROJECTION
    target.write_bytes(b"VALUE = 2\r\n")
    _git(root, "add", installer.PROJECTION)
    assert installer.source_guard() == _git(root, "rev-parse", "HEAD")
    assert target.read_bytes() == b"VALUE = 2\r\n"
```

## 既存の証明木 adapter の全文 (import を含む)

```python
"""Render any already-verified proof subtree with the canonical Narrative Model.

This adapter owns no statement-specific sentences and no source discovery.
The original searched result remains intact; the scoped display view exists
only to feed a second verified tree to the *same* public model renderer.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule, ProofStep


def verified_tree_postorder(root: ProofStep) -> tuple[ProofStep, ...]:
    """Visit every actual premise once, with cycle and inference guards."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    active: set[int] = set()
    visited: set[int] = set()
    ordered: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise TypeError("proof ancestry contains a non-ProofStep")
        identity = id(step)
        if identity in active:
            raise ValueError("cyclic proof ancestry")
        if identity in visited:
            return
        active.add(identity)
        if step.rule is ProofRule.GIVEN and step.premises:
            raise ValueError("a given step cannot consume premises")
        if step.rule is ProofRule.INFERENCE:
            rule = step.inference_rule
            if rule is None:
                raise ValueError("an inferred step requires its actual inference rule")
            guard = rule.match_guard
            if guard is not None and not guard(step.premises, ()):
                raise ValueError("unverified inference guard in proof ancestry")
        for premise in step.premises:
            visit(premise)
        active.remove(identity)
        visited.add(identity)
        ordered.append(step)

    visit(root)
    if not ordered or ordered[-1] is not root:
        raise ValueError("verified root missing from the ordered ancestry")
    return tuple(ordered)


def render_verified_tree_progress(
    target: TodaPrimaryGroup,
    root: ProofStep,
) -> tuple[str, ...]:
    """Reuse the exact canonical model-backed renderer for a certified tree.

    This presentation-only scope is not a second search and cannot create a
    named-group conclusion. Its public output is limited to source-backed
    Reference entries and renderable ProofSteps. Unsupported GIVEN types stay
    in the proof tree but are not fabricated into mathematical assertions.
    """
    if not isinstance(target, TodaPrimaryGroup):
        raise TypeError("target must be a TodaPrimaryGroup")
    steps = verified_tree_postorder(root)
    if root.rule is not ProofRule.INFERENCE:
        raise ValueError("a verified evidence root must be an inference")
    # This view is never published as a search result or used to decide status.
    # The real PartialProofResult retains all named open goals and diagnostics.
    scope = PartialProofResult(
        target=target,
        status=ProofSearchStatus.PARTIAL,
        proven_steps=steps,
    )
    model = build_proof_narrative_model(scope)
    markdown = render_model_backed_narrative_markdown(scope, model)
    reference_header = "## 使用する結果"
    proof_header = "## 証明"
    step_header = "### 確認済み ProofStep（与件を含む）"
    heading_lines = markdown.splitlines()
    if (heading_lines.count(reference_header) != 1
            or heading_lines.count(proof_header) != 1
            or heading_lines.count(step_header) != 1):
        raise ValueError("canonical renderer output has changed")
    source_section = markdown.split(reference_header, 1)[1].split("\n---\n", 1)[0]
    body_section = markdown.split(step_header, 1)[1]
    source_lines = [line.strip() for line in source_section.splitlines() if line.strip()]
    if "参照情報を持つ ProofStep はありません。" in source_lines:
        source_lines.remove("参照情報を持つ ProofStep はありません。")
    if not model.citations:
        raise ValueError("verified tree has no source-backed Reference")
    if not any(f"[R{citation.number}]" in line for line in source_lines
               for citation in model.citations):
        raise ValueError("the shared renderer dropped proof-tree citations")
    proof_lines = [
        line.strip() for line in body_section.splitlines()
        if line.lstrip().startswith(("- 与件:", "- 推論:"))
        and "（数式表示未対応）" not in line
    ]
    if not proof_lines:
        raise ValueError("verified evidence tree has no renderable ProofStep")
    return tuple([
        "### 検証済み証明木の Reference", "",
        *source_lines, "",
        "### 検証済み ProofStep", "",
        *proof_lines,
    ])
```

## 本番パッチの全文 (import を含む)

```python
"""Strict, literal patches against R15R16 installed local files and tests."""
from __future__ import annotations

from phase173_r4_r15r16_verified_progress_punctuation.projection_patch import (
    PROJECTION_NEW,
    PROJECTION_OLD,
    patch_projection,
    patch_layout,
)

PROGRESS_NEW = 'def _verified_abstract_progress_lines(\n    structure: CertifiedAbstractStructure,\n) -> tuple[str, ...]:\n    """Render the existing certificate via the same common Narrative renderer.\n\n    No proof-specific prose, four-premise assumption, or new inference.\n    """\n    from phase173_r4_r15r16r3_staged_guard_fix.tree_adapter import (\n        render_verified_tree_progress,\n    )\n\n    return render_verified_tree_progress(\n        structure.group, structure.proof_step,\n    )\n'
REPLACEMENT_TEST = '@pytest.mark.parametrize("k", (8, 9, 15, 31))\ndef test_abstract_certificate_displays_actual_verified_milestones(k: int) -> None:\n    goal = exact_prior_database_result(4, k)\n    assert goal is not None\n    result = search_group_from_registered_goal(n=4, k=k, goal=goal)\n    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)\n    assert result.conclusion is None and result.open_goals\n    assert result.abstract_structure is not None\n    assert result.abstract_structure.proof_step not in result.proven_steps\n\n    model = build_proof_narrative_model(result)\n    progress = render_certified_abstract_model_section(model)\n    assert progress == render_certified_abstract_section(result)\n    assert "## 検証済みの途中経過" in progress\n    assert "### 検証済み証明木の Reference" in progress\n    assert "### 検証済み ProofStep" in progress\n    assert "Proposition 4.4" in progress\n    assert "Lemma 5.4" in progress\n    assert progress.count("DB prior: sphere.csv") >= 2\n    assert "## 証明済みの抽象群構造" in progress\n    assert "記名生成元の対応は未証明" in progress\n    assert "先行データベースの " not in progress\n    assert "Proposition 4.4 の適用前提となる定理を検証した" not in progress\n    assert progress in render_model_backed_narrative_markdown(result, model)\n\n    view = build_standard_web_group_proof_view(\n        n=4, k=k, goal=goal, mode="narrative", citation_source="model",\n    )\n    assert view.partial_result and view.abstract_structure_certified\n    assert view.key == "generic-partial-proof"\n    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]\n    assert headings.count("検証済みの途中経過") == 1\n    assert headings.count("証明済みの抽象群構造") == 1\n    assert headings.count("未解決 Goal") == 1\n    shown = "\\n".join(\n        seg.value for line in view.rendered_lines for seg in line.segments\n    )\n    assert "sphere.csv" in shown and "Lemma 5.4" in shown\n    assert "Relation(lhs=" not in shown\n    assert "、" not in shown and "。" not in shown\n    assert result.conclusion is None and result.open_goals\n'


def patch_progress(source: str) -> str:
    # R15R16 generated this exact installed source from the reviewed HEAD.
    marker = "def _verified_abstract_progress_lines("
    end = "\n\ndef _render_abstract_claim("
    if source.count(marker) != 1 or source.count(end) != 1:
        raise RuntimeError("R15R16 progress function boundary not found")
    before, rest = source.split(marker, 1)
    _, after = rest.split(end, 1)
    return before + PROGRESS_NEW + "\n" + end.lstrip("\n") + after


def patch_test(source: str) -> str:
    prefix = '@pytest.mark.parametrize("k", (8, 9, 15, 31))\ndef test_abstract_certificate_displays_actual_verified_milestones'
    suffix = "\n\ndef test_completed_view_has_no_abstract_progress_sidecar()"
    if source.count(prefix) != 1 or source.count(suffix) != 1:
        raise RuntimeError("R15R16 test function boundary changed")
    before, rest = source.split(prefix, 1)
    _, after = rest.split(suffix, 1)
    return before + REPLACEMENT_TEST + "\n" + suffix.lstrip("\n") + after


TRANSFORMERS = {
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py": patch_progress,
    "phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py": patch_test,
}
```
