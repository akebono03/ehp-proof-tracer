# R15R15 — 新規コード・テスト・実行スクリプト全文

新規追加先は `phase173_r4_r15r15_abstract_result_banner/`。既存の Production クラス・関数は `FULL_CHANGED_UNITS.md` に全体を掲載。

## patches.py

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

## install.py

```python
"""Apply or restore the R15R15 Web status banner with strict source guards."""
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
REVIEWED_HEAD = "9729d3ee51e93f26cf6b31a3880cb1a92a552f2c"
REVIEWED_BLOBS = {
    "web_group_proof_common.py": "045d2ae677c0e62c243270e760c786ce61224c59",
    "phase165_r52_r3_web_adapter.py": "211fdb73342019cee4503c01e549c118e286125a",
    "templates/index.html": "d84b9eed4c8d070c4ed98c5ed31fd9241987a42e",
    "phase173_r4_r15r13_unified_presentation/layout.py": "809effb7fcb70361e5580d9716d4aa143685f275",
}
RETAINED_R15R14_PATHS = {
    "web_group_proof_common.py",
    "phase173_r4_r15r13_unified_presentation/layout.py",
}


def git(*args: str) -> str:
    command = subprocess.run(
        ["git", *args], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding="utf-8", errors="replace", check=False,
    )
    if command.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {command.stderr.strip()[:400]}")
    return command.stdout.strip()


def normalized(raw: bytes) -> str:
    return raw.decode("utf-8").replace("\r\n", "\n")


def preserved_newlines(original: bytes, text: str) -> bytes:
    if b"\r\n" in original:
        return text.replace("\n", "\r\n").encode("utf-8")
    return text.encode("utf-8")


def baseline_for(path: str) -> str:
    return git("show", f"HEAD:{path}").replace("\r\n", "\n") + "\n"


def _expected_r15r14() -> tuple[str, str]:
    # The user installed R15R14 but has not committed that separate change.
    # Reuse its reviewed transform and compare the *whole* local source.
    from phase173_r4_r15r14_common_partial_presentation.patches import (
        patch_common, patch_layout,
    )
    return (
        patch_common(baseline_for("web_group_proof_common.py")),
        patch_layout(baseline_for("phase173_r4_r15r13_unified_presentation/layout.py")),
    )


def preflight(*, installed_allowed: bool = False) -> tuple[dict[str, bytes], dict[str, bytes]]:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if branch != "develop" or head != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError(f"source HEAD/branch guard mismatch: {branch} local={head} remote={remote}")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes require review")
    for path, expected_blob in REVIEWED_BLOBS.items():
        if git("rev-parse", f"HEAD:{path}") != expected_blob:
            raise RuntimeError("reviewed Git blob mismatch: " + path)
    expected_common, expected_layout = _expected_r15r14()
    layout_path = "phase173_r4_r15r13_unified_presentation/layout.py"
    if normalized((ROOT / layout_path).read_bytes()) != expected_layout:
        raise RuntimeError("R15R14 local layout has changed since review")
    expected_sources = {
        "web_group_proof_common.py": expected_common,
        "phase165_r52_r3_web_adapter.py": baseline_for("phase165_r52_r3_web_adapter.py"),
        "templates/index.html": baseline_for("templates/index.html"),
    }
    originals = {}
    modified = {}
    for path, expected in expected_sources.items():
        original = (ROOT / path).read_bytes()
        before = normalized(original)
        if before != expected:
            if not installed_allowed or before != TRANSFORMERS[path](expected):
                raise RuntimeError("unreviewed source content: " + path)
        originals[path] = original
        modified[path] = preserved_newlines(original, TRANSFORMERS[path](expected))
    changed = set(git("diff", "--name-only").splitlines())
    allowed = RETAINED_R15R14_PATHS | (set(TRANSFORMERS) if installed_allowed else set())
    if not changed.issubset(allowed):
        raise RuntimeError("unexpected tracked edits: " + ", ".join(sorted(changed - allowed)))
    print("R15R15_BRANCH=" + branch, flush=True)
    print("R15R15_LOCAL_HEAD=" + head, flush=True)
    print("R15R15_REMOTE_HEAD=" + remote, flush=True)
    print("R15R15_SOURCE_GUARD=PASS", flush=True)
    print("R15R15_R15R14_LOCAL_CHANGES_PRESERVED=True", flush=True)
    return originals, modified


def install() -> None:
    if STATE.exists():
        original, target = preflight(installed_allowed=True)
        if all(original[k] == target[k] for k in target):
            print("R15R15_ALREADY_INSTALLED=True", flush=True)
            return
        raise RuntimeError("install state exists but source content differs")
    originals, targets = preflight()
    BACKUP.mkdir(exist_ok=True)
    hashes = {}
    for i, (path, original) in enumerate(originals.items()):
        label = f"source_{i}.backup"
        destination = BACKUP / label
        if destination.exists():
            raise RuntimeError("pre-existing backup requires inspection: " + label)
        destination.write_bytes(original)
        hashes[path] = {"backup": label, "sha256": sha256(original).hexdigest(),
                        "target_sha256": sha256(targets[path]).hexdigest()}
    STATE.write_text(json.dumps({"head": REVIEWED_HEAD, "files": hashes}, indent=2) + "\n", encoding="utf-8")
    try:
        for path, target in targets.items():
            location = ROOT / path
            temporary = location.with_name(location.name + ".r15r15.tmp")
            temporary.write_bytes(target)
            os.replace(temporary, location)
    except BaseException:
        restore()
        raise
    print("R15R15_INSTALLED=True", flush=True)


def restore() -> None:
    if not STATE.exists():
        raise RuntimeError("no R15R15 installation state to restore")
    data = json.loads(STATE.read_text(encoding="utf-8"))
    if data["head"] != REVIEWED_HEAD:
        raise RuntimeError("installation state head changed")
    for path, saved in data["files"].items():
        previous = (BACKUP / saved["backup"]).read_bytes()
        current = (ROOT / path).read_bytes()
        if sha256(previous).hexdigest() != saved["sha256"]:
            raise RuntimeError("corrupt backup: " + path)
        if sha256(current).hexdigest() not in (saved["sha256"], saved["target_sha256"]):
            raise RuntimeError("edited installed file requires inspection: " + path)
    for path, saved in data["files"].items():
        (ROOT / path).write_bytes((BACKUP / saved["backup"]).read_bytes())
    STATE.unlink()
    for saved in data["files"].values():
        (BACKUP / saved["backup"]).unlink()
    BACKUP.rmdir()
    print("R15R15_RESTORED=True", flush=True)
    print("R15R15_R15R14_RETAINED=True", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--install", action="store_true")
    mode.add_argument("--restore", action="store_true")
    opts = parser.parse_args()
    try:
        if opts.restore:
            restore()
        elif opts.install:
            install()
        else:
            preflight(installed_allowed=STATE.exists())
            print("R15R15_DRY_RUN=PASS", flush=True)
            print("R15R15_PRODUCTION_EDIT=NONE", flush=True)
        return 0
    except (RuntimeError, ValueError, OSError, UnicodeError, KeyError) as exc:
        print("R15R15_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub fetch failed' }

    python -m phase173_r4_r15r15_abstract_result_banner.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R15 source guard failed' }
    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r15_abstract_result_banner/tests/test_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R15 contract tests failed' }
    if ($DryRun) {
        Write-Output 'R15R15_DRY_RUN=PASS'
        Write-Output 'R15R15_PHASE_COMPLETED=False'
        exit 0
    }

    python -m phase173_r4_r15r15_abstract_result_banner.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R15 installation failed' }
    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r15_abstract_result_banner/tests/test_contract.py `
            phase173_r4_r15r15_abstract_result_banner/tests/test_integration.py `
            phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r12_reference_correction/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py `
            tests/test_phase117_web_app.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R15 focused pytest failed' }
        Write-Output 'R15R15_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R15_FULL_PYTEST_RUN=False'
        Write-Output 'R15R15_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r15_abstract_result_banner.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R15 rollback failed; inspect backups' }
        throw
    }
} finally {
    Pop-Location
}
```

## tests/test_contract.py

```python
"""Source-independent contract for one evidence-driven Web result banner."""
from __future__ import annotations

import pytest

from phase173_r4_r15r15_abstract_result_banner.patches import (
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

## tests/test_integration.py

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
