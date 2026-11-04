# R15R15R2 — 新規コード・テスト・実行手順全文

変更した本番ファイルのクラス・関数全文は `FULL_CHANGED_UNITS.md` を参照。

## `__init__.py`

```python
"""Phase 173 R4-R15R15 status-aware Web banner without proof inference."""
```

## `patches.py`

```python
"""Minimal status-driven Web presentation patch, no mathematical inference."""
from __future__ import annotations


COMMON_FIELD = "  partial_result: bool = False\n"
COMMON_FIELD_NEW = (
    "  partial_result: bool = False\n"
    "  abstract_structure_certified: bool = False\n"
)
COMMON_GUARD = (
    '    if not isinstance(self.partial_result, bool):\n'
    '      raise TypeError("partial_result must be a bool")\n'
)
COMMON_GUARD_NEW = COMMON_GUARD + (
    '\n'
    '    if not isinstance(self.abstract_structure_certified, bool):\n'
    '      raise TypeError("abstract_structure_certified must be a bool")\n'
    '\n'
    '    if self.abstract_structure_certified and not self.partial_result:\n'
    '      raise ValueError("abstract certificate cannot mark a complete named proof")\n'
)
ADAPTER_ANCHOR = (
    '        partial_result=(result.status is not ProofSearchStatus.COMPLETE),\n'
)
ADAPTER_REPLACEMENT = ADAPTER_ANCHOR + (
    '        abstract_structure_certified=(result.abstract_structure is not None),\n'
)
TEMPLATE_ANCHOR = '''      {% elif view.status.value == "not_found" %}
        {% if group_proof_view and not group_proof_view.partial_result %}
          <p>Typed proof search completed. See Group proof below.</p>
        {% else %}
        <p>
          No proof-backed result found for this query.
        </p>
        {% endif %}
'''
TEMPLATE_REPLACEMENT = '''      {% elif view.status.value == "not_found" %}
        {% if group_proof_view and not group_proof_view.partial_result %}
          <p>Typed proof search completed. See Group proof below.</p>
        {% elif group_proof_view and group_proof_view.abstract_structure_certified %}
          <p>
            A verified abstract group structure is available, but the
            named-generator proof is incomplete. See Group proof below.
          </p>
        {% else %}
          <p>No proof-backed result found for this query.</p>
        {% endif %}
'''


def _replace_once(source: str, old: str, new: str, path: str) -> str:
    if not isinstance(source, str):
        raise TypeError(f"{path}: source must be str")
    count = source.count(old)
    if count != 1:
        raise ValueError(f"{path}: reviewed anchor mismatch (count={count})")
    if new in source:
        raise ValueError(f"{path}: patch already present")
    return source.replace(old, new, 1)


def patch_common(source: str) -> str:
    """Add an explicit evidence flag to the existing Web view contract."""
    output = _replace_once(source, COMMON_FIELD, COMMON_FIELD_NEW, "web_group_proof_common.py")
    return _replace_once(output, COMMON_GUARD, COMMON_GUARD_NEW, "web_group_proof_common.py")


def patch_adapter(source: str) -> str:
    """Project the already-verified certificate from PartialProofResult."""
    return _replace_once(source, ADAPTER_ANCHOR, ADAPTER_REPLACEMENT,
                         "phase165_r52_r3_web_adapter.py")


def patch_template(source: str) -> str:
    """Display the three distinct existing proof states, with no source inference."""
    return _replace_once(source, TEMPLATE_ANCHOR, TEMPLATE_REPLACEMENT,
                         "templates/index.html")


TRANSFORMERS = {
    "web_group_proof_common.py": patch_common,
    "phase165_r52_r3_web_adapter.py": patch_adapter,
    "templates/index.html": patch_template,
}
```

## `install.py`

```python
"""Safely install or restore a reviewed, presentation-only R15R15 patch.

R15R14 is committed at the reviewed baseline. Newer develop commits are
allowed only while the exact four reviewed Git blobs remain unchanged.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

from .patches import TRANSFORMERS

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
BACKUP = PACKAGE / "backups"
STATE = PACKAGE / "installed_state.json"
REVIEWED_HEAD = "5563a67008d097d08745481ee299dbb94e12c2b9"
REVIEWED_BLOBS = {
    "web_group_proof_common.py": "52ef8170874c714d4aa4bf4f8b525a7f9953154b",
    "phase165_r52_r3_web_adapter.py": "211fdb73342019cee4503c01e549c118e286125a",
    "templates/index.html": "d84b9eed4c8d070c4ed98c5ed31fd9241987a42e",
    "phase173_r4_r15r13_unified_presentation/layout.py":
        "05d2b3a0353c0ff1251f65dcd53d902c9ffbb140",
}


def command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )


def git(*args: str) -> str:
    result = command(*args)
    if result.returncode != 0:
        raise RuntimeError(
            "git " + " ".join(args) + ": " + result.stderr.strip()[:400]
        )
    return result.stdout.strip()


def normalized(original: bytes) -> str:
    return original.decode("utf-8").replace("\r\n", "\n")


def preserved_newlines(original: bytes, source: str) -> bytes:
    if b"\r\n" in original:
        return source.replace("\n", "\r\n").encode("utf-8")
    return source.encode("utf-8")


def source_guard(*, installed: bool) -> str:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if branch != "develop" or head != remote:
        raise RuntimeError(
            f"develop local/remote mismatch: branch={branch} local={head} remote={remote}"
        )
    lineage = command("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD")
    if lineage.returncode != 0:
        raise RuntimeError("HEAD is not a descendant of the reviewed R15R14 commit")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes require review")
    for path, blob in REVIEWED_BLOBS.items():
        if git("rev-parse", f"HEAD:{path}") != blob:
            raise RuntimeError("reviewed content changed on GitHub: " + path)
        if not (ROOT / path).is_file():
            raise RuntimeError("missing reviewed file: " + path)
    changed = set(filter(None, git("diff", "--name-only").splitlines()))
    allowed = set(TRANSFORMERS) if installed else set()
    if not changed.issubset(allowed):
        raise RuntimeError(
            "unreviewed tracked local changes: " + ", ".join(sorted(changed - allowed))
        )
    print("R15R15R2_BRANCH=" + branch, flush=True)
    print("R15R15R2_LOCAL_HEAD=" + head, flush=True)
    print("R15R15R2_REMOTE_HEAD=" + remote, flush=True)
    print("R15R15R2_REVIEWED_ANCESTOR=" + REVIEWED_HEAD, flush=True)
    print("R15R15R2_SOURCE_GUARD_FILES=" + str(len(REVIEWED_BLOBS)), flush=True)
    print("R15R15R2_SOURCE_GUARD=PASS", flush=True)
    return head


def project(before: bytes, path: str) -> bytes:
    return preserved_newlines(before, TRANSFORMERS[path](normalized(before)))


def read_backup(state: dict, path: str) -> bytes:
    entry = state["files"][path]
    previous = (BACKUP / entry["backup"]).read_bytes()
    if sha256(previous).hexdigest() != entry["original_sha256"]:
        raise RuntimeError("backup integrity failure: " + path)
    return previous


def preflight(*, installed_allowed: bool = False) -> tuple[dict[str, bytes], dict[str, bytes], str]:
    installed = STATE.is_file()
    if installed and not installed_allowed:
        raise RuntimeError("already installed; inspect installation state")
    if not installed and BACKUP.exists():
        raise RuntimeError("orphan backup directory requires inspection")
    head = source_guard(installed=installed)
    state = json.loads(STATE.read_text(encoding="utf-8")) if installed else None
    if state is not None and head != state["head"]:
        raise RuntimeError("HEAD changed after R15R15 install; inspect before proceeding")
    originals: dict[str, bytes] = {}
    targets: dict[str, bytes] = {}
    for path in TRANSFORMERS:
        current = (ROOT / path).read_bytes()
        original = read_backup(state, path) if state is not None else current
        target = project(original, path)
        if state is not None:
            entry = state["files"][path]
            if sha256(target).hexdigest() != entry["target_sha256"]:
                raise RuntimeError("expected patch changed: " + path)
            if current != target:
                raise RuntimeError("installed content has changed: " + path)
        else:
            if current != original:
                raise RuntimeError("local source changed: " + path)
        originals[path] = original
        targets[path] = target
    return originals, targets, head


def install() -> None:
    originals, targets, head = preflight(installed_allowed=True)
    if STATE.exists():
        print("R15R15R2_ALREADY_INSTALLED=True", flush=True)
        return
    BACKUP.mkdir(exist_ok=False)
    state: dict[str, object] = {"head": head, "files": {}}
    try:
        for i, (path, original) in enumerate(originals.items()):
            name = f"source_{i}.backup"
            (BACKUP / name).write_bytes(original)
            state["files"][path] = {
                "backup": name,
                "original_sha256": sha256(original).hexdigest(),
                "target_sha256": sha256(targets[path]).hexdigest(),
            }
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        for path, target in targets.items():
            location = ROOT / path
            temporary = location.with_name(location.name + ".r15r15r2.tmp")
            temporary.write_bytes(target)
            os.replace(temporary, location)
    except BaseException:
        if STATE.exists():
            restore()
        else:
            for backup in BACKUP.iterdir():
                backup.unlink()
            BACKUP.rmdir()
        raise
    print("R15R15R2_INSTALLED=True", flush=True)
    print("R15R15R2_FULL_PYTEST_RUN=False", flush=True)


def restore() -> None:
    if not STATE.is_file():
        raise RuntimeError("no R15R15R2 installation state")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if git("rev-parse", "HEAD") != state["head"]:
        raise RuntimeError("HEAD changed after patch; refusal to overwrite")
    files: dict = state["files"]
    originals: dict[str, bytes] = {}
    for path, entry in files.items():
        previous = read_backup(state, path)
        current = (ROOT / path).read_bytes()
        if sha256(current).hexdigest() not in (
            entry["original_sha256"], entry["target_sha256"]
        ):
            raise RuntimeError("local edit after install: " + path)
        originals[path] = previous
    for path, previous in originals.items():
        (ROOT / path).write_bytes(previous)
    STATE.unlink()
    for entry in files.values():
        (BACKUP / entry["backup"]).unlink()
    BACKUP.rmdir()
    print("R15R15R2_RESTORED=True", flush=True)
    print("R15R15R2_RESTORED_TO_COMMITTED_R15R14=True", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    options = parser.add_mutually_exclusive_group(required=True)
    options.add_argument("--dry-run", action="store_true")
    options.add_argument("--install", action="store_true")
    options.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    try:
        if args.restore:
            restore()
        elif args.install:
            install()
        else:
            preflight(installed_allowed=True)
            print("R15R15R2_DRY_RUN=PASS", flush=True)
            print("R15R15R2_PRODUCTION_EDIT=NONE", flush=True)
        return 0
    except (RuntimeError, TypeError, ValueError, OSError, UnicodeError, KeyError) as exc:
        print("R15R15R2_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub fetch failed' }

    python -m phase173_r4_r15r15r2_head_guard_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 source guard failed' }
    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r15r2_head_guard_fix/tests/test_contract.py `
        phase173_r4_r15r15r2_head_guard_fix/tests/test_guard.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 contract tests failed' }
    if ($DryRun) {
        Write-Output 'R15R15R2_DRY_RUN=PASS'
        Write-Output 'R15R15R2_PHASE_COMPLETED=False'
        exit 0
    }

    python -m phase173_r4_r15r15r2_head_guard_fix.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 install failed' }
    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r15r2_head_guard_fix/tests/test_contract.py `
            phase173_r4_r15r15r2_head_guard_fix/tests/test_guard.py `
            phase173_r4_r15r15r2_head_guard_fix/tests/test_integration.py `
            phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r12_reference_correction/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py `
            tests/test_phase117_web_app.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 focused pytest failed' }
        Write-Output 'R15R15R2_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R15R2_FULL_PYTEST_RUN=False'
        Write-Output 'R15R15R2_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r15r2_head_guard_fix.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R15R2 rollback requires inspection' }
        throw
    }
} finally {
    Pop-Location
}
```

## `tests/__init__.py`

```python
"""R15R15R2 focused contract and actual Web tests."""
```

## `tests/test_contract.py`

```python
"""Source-independent contract for one evidence-driven Web result banner."""
from __future__ import annotations

import pytest

from phase173_r4_r15r15r2_head_guard_fix.patches import (
    COMMON_FIELD,
    COMMON_GUARD,
    ADAPTER_ANCHOR,
    TEMPLATE_ANCHOR,
    patch_common,
    patch_adapter,
    patch_template,
)


def test_common_view_flag_is_optional_and_checked() -> None:
    source = (
        "@dataclass(frozen=True)\nclass WebGroupProofView:\n"
        + COMMON_FIELD + "  def __post_init__(self):\n" + COMMON_GUARD
    )
    patched = patch_common(source)
    assert patched.count("  abstract_structure_certified: bool = False\n") == 1
    assert patched.count("if not isinstance(self.abstract_structure_certified, bool)") == 1
    assert "if self.abstract_structure_certified and not self.partial_result" in patched
    assert source.count("abstract_structure_certified") == 0


def test_adapter_passes_only_existing_verified_certificate() -> None:
    source = "return WebGroupProofView(\n" + ADAPTER_ANCHOR + ")\n"
    patched = patch_adapter(source)
    assert "abstract_structure_certified=(result.abstract_structure is not None)" in patched
    assert patched.count("partial_result=(result.status is not ProofSearchStatus.COMPLETE)") == 1


def test_template_distinguishes_three_statuses() -> None:
    patched = patch_template(TEMPLATE_ANCHOR)
    assert patched.index("not group_proof_view.partial_result") < patched.index(
        "group_proof_view.abstract_structure_certified"
    ) < patched.index("No proof-backed result found")
    assert "named-generator proof is incomplete" in patched
    assert patched.count("No proof-backed result found") == 1


@pytest.mark.parametrize("transformer,source", (
    (patch_common, COMMON_FIELD + COMMON_GUARD),
    (patch_adapter, ADAPTER_ANCHOR),
    (patch_template, TEMPLATE_ANCHOR),
))
def test_duplicate_or_missing_anchors_fail_closed(transformer, source) -> None:
    with pytest.raises(ValueError, match="anchor mismatch"):
        transformer(source + source)
    with pytest.raises(ValueError, match="anchor mismatch"):
        transformer("unreviewed source")


def test_patch_rejects_invalid_input_types() -> None:
    with pytest.raises(TypeError):
        patch_template(None)
```

## `tests/test_integration.py`

```python
"""Real Web proof state, typed certificate, and Flask result banner regressions."""
from __future__ import annotations

from dataclasses import replace

import pytest

import web_app
from toda_calculation_result import TodaCalculationStatus
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import WebGroupProofView
from web_group_query import WebGroupQueryView


@pytest.mark.parametrize("n,k,certified", (
    (4, 3, False),
    (4, 8, True),
    (4, 31, True),
))
def test_certificate_flag_comes_from_actual_verified_partial_result(
    n: int, k: int, certified: bool,
) -> None:
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode="narrative", citation_source="model",
    )
    assert view.abstract_structure_certified is certified
    if certified:
        assert view.partial_result
        assert view.key == "generic-partial-proof"
        assert any(
            line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
            for line in view.rendered_lines
        )
    else:
        assert not view.partial_result
        assert view.key == "generic-complete-proof"


def test_complete_view_cannot_be_promoted_to_abstract_only() -> None:
    view = build_standard_web_group_proof_view(
        n=4, k=4, mode="narrative", citation_source="model",
    )
    assert not view.abstract_structure_certified
    assert not view.partial_result
    with pytest.raises(ValueError, match="cannot mark a complete named proof"):
        replace(view, abstract_structure_certified=True)
    with pytest.raises(TypeError, match="abstract_structure_certified must be a bool"):
        replace(view, abstract_structure_certified="yes")


def test_real_flask_result_explains_abstract_only_status(monkeypatch) -> None:
    # Avoid repeating the distinct old group-query search. The *real* typed
    # proof search and certificate-bound Web adapter remain in this test.
    def query_not_found(n: int, k: int) -> WebGroupQueryView:
        assert (n, k) == (4, 8)
        return WebGroupQueryView(
            n=n, k=k, status=TodaCalculationStatus.NOT_FOUND,
            result_latex=None, proof_available=False,
        )

    monkeypatch.setattr(web_app, "build_standard_web_group_query_view", query_not_found)
    app = web_app.create_app()
    app.config.update(TESTING=True)
    response = app.test_client().post("/", data={"n": "4", "k": "8"})
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "A verified abstract group structure is available" in text
    assert "named-generator proof is incomplete" in text
    assert "No proof-backed result found for this query" not in text
    assert "generic-partial-proof" in text
    assert "証明済みの抽象群構造" in text


def test_no_certificate_preserves_not_found_banner(monkeypatch) -> None:
    def query_not_found(n: int, k: int) -> WebGroupQueryView:
        return WebGroupQueryView(
            n=n, k=k, status=TodaCalculationStatus.NOT_FOUND,
            result_latex=None,
        )

    partial = WebGroupProofView(
        n=5, k=8, conclusion_latex=r"\pi_{13}^{5}",
        theorem=None, phase=None, key="generic-partial-proof",
        steps=(), max_depth=2, mode="trace", partial_result=True,
    )
    monkeypatch.setattr(web_app, "build_standard_web_group_query_view", query_not_found)
    monkeypatch.setattr(
        web_app, "build_group_proof_progress_view", lambda **kwargs: partial,
    )
    app = web_app.create_app()
    app.config.update(TESTING=True)
    response = app.test_client().post("/", data={"n": "5", "k": "8"})
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "No proof-backed result found for this query" in text
    assert "A verified abstract group structure is available" not in text
    assert "generic-partial-proof" in text
```

## `tests/test_guard.py`

```python
"""The guard permits reviewed descendants, never unreviewed source content."""
from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess

import pytest

from phase173_r4_r15r15r2_head_guard_fix import install


def _mock_source_tree(monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
                      *, changed: str | None = None, bad_blob: str | None = None) -> str:
    """Set up only the filesystem and git results consumed by Source Guard."""
    for path in install.REVIEWED_BLOBS:
        destination = tmp_path / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("reviewed source\n", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    head = "a" * 40

    def fake_git(*args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args in (("rev-parse", "HEAD"), ("rev-parse", "origin/develop")):
            return head
        if args == ("diff", "--cached", "--name-only"):
            return ""
        if args == ("diff", "--name-only"):
            return changed or ""
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            path = args[1][5:]
            if path not in install.REVIEWED_BLOBS:
                raise AssertionError("unexpected git path")
            if path == bad_blob:
                return "b" * 40
            return install.REVIEWED_BLOBS[path]
        raise AssertionError("unexpected git command: " + repr(args))

    def fake_command(*args: str) -> CompletedProcess[str]:
        assert args == ("merge-base", "--is-ancestor", install.REVIEWED_HEAD, "HEAD")
        return CompletedProcess(args=args, returncode=0, stdout="", stderr="")

    monkeypatch.setattr(install, "git", fake_git)
    monkeypatch.setattr(install, "command", fake_command)
    return head


def test_reviewed_descendant_is_accepted(monkeypatch: pytest.MonkeyPatch,
                                        tmp_path: Path) -> None:
    expected = _mock_source_tree(monkeypatch, tmp_path)
    assert install.source_guard(installed=False) == expected


def test_reviewed_blob_mismatch_is_rejected(monkeypatch: pytest.MonkeyPatch,
                                           tmp_path: Path) -> None:
    _mock_source_tree(monkeypatch, tmp_path, bad_blob="web_group_proof_common.py")
    with pytest.raises(RuntimeError, match="reviewed content changed"):
        install.source_guard(installed=False)


def test_unreviewed_local_tracked_edits_are_rejected(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    _mock_source_tree(monkeypatch, tmp_path, changed="templates/index.html")
    with pytest.raises(RuntimeError, match="unreviewed tracked local changes"):
        install.source_guard(installed=False)
```
