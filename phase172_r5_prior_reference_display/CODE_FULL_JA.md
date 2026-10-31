# Phase 172 R5：変更コード・新規コード全文

## 既存 Renderer の変更

- ファイル：`phase168_r3_5_model_renderer.py`
- 関数：`render_model_backed_narrative_markdown()` のみ。トップレベル import は変更しない。
- R4 の検証済み全文に `OLD`→`NEW` の厳格置換を1回だけ適用する。
- `-DryRun` が変更後の**関数全文**を `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r5_*\render_model_backed_narrative_markdown_FULL.py` に、**ファイル全文**を同じディレクトリの `phase168_r3_5_model_renderer_FULL.py` に出力する。両ファイルは省略なしで置換できる。
- 本 ZIP に元の Git blob を含めないため、関数全文はその実行環境で監査済みの R2→R3→R4 ベースを再構成したものから生成する。

### 変更箇所の作成ロジック（関数全文生成は `install.py` 内）

```python
def updated_renderer(source: bytes) -> bytes:
    original = normalize(source)
    if original.count(OLD) != 1 or NEW in original:
        raise RuntimeError("Renderer citation loop does not match reviewed R4 anchor")
    modified = original.replace(OLD, NEW, 1)
    tree = ast.parse(modified)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "render_model_backed_narrative_markdown"]
    if len(matches) != 1:
        raise RuntimeError("Renderer function identity changed")
    newline = "\r\n" if b"\r\n" in source else "\n"
    return modified.replace("\n", newline).encode("utf-8")
```

## 新規ファイル・関数・テスト全文

### `projection.py`

```python
"""Present authentic adopted prior DB citations without changing provenance.

The internal locator remains unchanged for proof verification, citation identity,
and historical consumers. Only the public Reference heading is projected.
"""
from __future__ import annotations

import re

from homotopy_groups import TodaPrimaryGroup
from phase168_r3_3_proof_narrative_model import (
    NarrativeCitation,
    ProofNarrativeModel,
    root_ancestor_step_indices,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase169_r10e4_ordered_db_prior.db_prior import (
    DB_LOCATOR_PREFIX,
    group_coordinates,
    precedes_db_goal,
)
from proof import ProofRule


_DB_LOCATOR = re.compile(
    re.escape(DB_LOCATOR_PREFIX)
    + r" \(n=([0-9]+), k=([0-9]+)\)(?: \[参考: ([^\]\r\n]+)\])?"
)
_DB_NOTE = "ADOPTED_DATABASE_PRIOR; independent reference not asserted"


def display_prior_reference_locator(
    citation: object, model: object,
) -> str | None:
    """Return a Japanese heading only for an actual verified DB prior leaf.

    A locator alone cannot authorize presentation as a DB assumption. Require
    exactly one cited GIVEN leaf in the completed root ancestry, the canonical
    adopted-prior marker, an unmodified inference-rule locator, and matching
    typed group coordinates. Never rewrite literature/registry citations.
    """
    if (not isinstance(citation, NarrativeCitation)
            or not isinstance(model, ProofNarrativeModel)
            or model.status is not ProofSearchStatus.COMPLETE
            or model.open_goals
            or not isinstance(model.target, TodaPrimaryGroup)):
        return None
    locator = citation.reference.locator or citation.reference.label
    if not isinstance(locator, str):
        return None
    match = _DB_LOCATOR.fullmatch(locator)
    if match is None:
        return None
    if (citation.assertion_ids or citation.reference_ids
            or citation.statement_bodies
            or len(citation.step_indices) != 1):
        return None
    if (not isinstance(model.steps, tuple)
            or not isinstance(model.step_citation_numbers, tuple)
            or len(model.step_citation_numbers) != len(model.steps)):
        return None
    index = citation.step_indices[0]
    if type(index) is not int or not 0 <= index < len(model.steps):
        return None
    if type(model.root_index) is not int:
        return None
    try:
        ancestry = root_ancestor_step_indices(model.steps, model.root_index)
    except ValueError:
        return None
    if index not in ancestry:
        return None
    step = model.steps[index]
    reference = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
    step_locator = getattr(reference, "locator", None)
    if (step.rule is not ProofRule.GIVEN
            or step.premises
            or step.note != _DB_NOTE
            or step_locator != locator
            or citation.number not in model.step_citation_numbers[index]):
        return None
    coordinates = group_coordinates(step.conclusion)
    if coordinates is None:
        return None
    n, k = coordinates
    if (str(n) != match.group(1) or str(k) != match.group(2)
            or type(model.target.sphere_dimension) is not int
            or type(model.target.group_dimension) is not int):
        return None
    target_n = model.target.sphere_dimension
    target_k = model.target.group_dimension - target_n
    if not precedes_db_goal(n, k, target_n, target_k):
        return None
    heading = (
        rf"先行データベース結果 $\pi_{{{n + k}}}^{{{n}}}$"
        f"（sphere.csv, n={n}, k={k}）"
    )
    if match.group(3) is not None:
        heading += f"［参考: {match.group(3)}］"
    return heading
```

### `tests/test_projection.py`

```python
"""Phase 172 R5: reference headings keep every original proof provenance."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase172_r5_prior_reference_display.projection import (
    display_prior_reference_locator,
)
from proof import LiteratureReference


@pytest.fixture(scope="module")
def verified_pi63():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    assert len(model.citations) == 8
    return result, model


def test_verified_prior_headings_identify_typed_groups_and_metadata(verified_pi63):
    result, model = verified_pi63
    headers = [display_prior_reference_locator(c, model) for c in model.citations]
    assert [i + 1 for i, value in enumerate(headers) if value is not None] == [2, 8]
    assert headers[1] == (
        r"先行データベース結果 $\pi_{7}^{5}$"
        "（sphere.csv, n=5, k=2）［参考: Proposition 5.3］"
    )
    assert headers[7] == (
        r"先行データベース結果 $\pi_{6}^{5}$"
        "（sphere.csv, n=5, k=1）［参考: Proposition 5.1］"
    )
    assert result.proven_steps == model.steps


def test_public_reference_headings_change_without_rewriting_source(verified_pi63):
    result, model = verified_pi63
    before_locators = tuple(c.reference.locator for c in model.citations)
    before_numbers = model.step_citation_numbers
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split("\n証明\n", 1)
    assert "DB prior: sphere.csv" not in reference
    assert "[R2] 先行データベース結果" in reference
    assert "[R8] 先行データベース結果" in reference
    assert "[R3] Chapter V, i)." in reference
    assert "[R4] Proposition 2.2." in reference
    assert "[R5] (5.3)." in reference
    assert r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$." in body
    assert r"\operatorname{ord}(\nu')=4" in body
    assert len(model.steps) == 50
    assert len(model.citations) == 8
    assert tuple(c.reference.locator for c in model.citations) == before_locators
    assert model.step_citation_numbers == before_numbers
    assert model.open_goals == ()


def test_unrelated_literature_reference_keeps_original_locator(verified_pi63):
    _, model = verified_pi63
    for citation in model.citations:
        if citation.number not in (2, 8):
            assert display_prior_reference_locator(citation, model) is None


def test_forged_prior_marker_is_not_presented_as_database(verified_pi63):
    _, model = verified_pi63
    citation = model.citations[1]
    index = citation.step_indices[0]
    changed_steps = list(model.steps)
    changed_steps[index] = replace(changed_steps[index], note="unverified")
    altered = replace(model, steps=tuple(changed_steps))
    assert display_prior_reference_locator(citation, altered) is None


def test_mismatched_coordinates_or_locator_fail_closed(verified_pi63):
    _, model = verified_pi63
    citation = model.citations[1]
    forged = replace(
        citation,
        reference=LiteratureReference(
            label="DB prior: sphere.csv (n=8, k=2)",
            locator="DB prior: sphere.csv (n=8, k=2)",
        ),
    )
    assert display_prior_reference_locator(forged, model) is None
    assert display_prior_reference_locator(
        replace(citation, step_indices=()), model,
    ) is None
    assert display_prior_reference_locator(
        replace(citation, assertion_ids=("invented",)), model,
    ) is None


def test_missing_reference_ownership_and_incomplete_model_fail_closed(verified_pi63):
    _, model = verified_pi63
    citation = model.citations[1]
    index = citation.step_indices[0]
    numbers = list(model.step_citation_numbers)
    numbers[index] = ()
    assert display_prior_reference_locator(
        citation, replace(model, step_citation_numbers=tuple(numbers)),
    ) is None
    assert display_prior_reference_locator(
        citation, replace(model, status=ProofSearchStatus.PARTIAL),
    ) is None
    assert display_prior_reference_locator(
        citation, replace(model, open_goals=("pending",)),
    ) is None


def test_no_prior_without_real_step_or_root(verified_pi63):
    _, model = verified_pi63
    citation = model.citations[7]
    assert display_prior_reference_locator(
        citation, replace(model, root_index=None),
    ) is None
    assert display_prior_reference_locator(
        citation, replace(model, steps=()),
    ) is None
```

### `install.py`

```python
"""Guarded Phase 172 R5 public Reference heading patch, focused tests and rollback.

The internal database locator and all proof/citation records are unchanged.
Only the complete-proof Renderer selects a validated Japanese display heading.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from phase172_r3_hopf_chain_display import install as r3_installer
from phase172_r4_hopf_surjectivity_display import install as r4_installer

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path("phase168_r3_5_model_renderer.py")
PROJECTION = Path("phase172_r5_prior_reference_display/projection.py")
TESTS = Path("phase172_r5_prior_reference_display/tests/test_projection.py")
R4_PROJECTION_SHA256 = "68983b5382eb82a66d0a0286b5cd5fbb2844b05694bbad910754b5cef4ba295c"
R4_TEST_SHA256 = "90e5b8629543d0f1bea280a855c360c400f66d4d8180db1be705322a11734bb7"
R4_INSTALL_SHA256 = "b7d13450d71de5417aa9f51c882320c6c98a7405839e27a157b727be38143722"
OLD = (
    "    for citation in model.citations:\n"
    "        locator = citation.reference.locator or citation.reference.label\n"
    "        # Display the cited locator verbatim; no series-specific alias.\n"
    '        lines.append(f"**[R{citation.number}] {locator}.**")\n'
)
NEW = (
    "    from phase172_r5_prior_reference_display.projection import (\n"
    "        display_prior_reference_locator,\n"
    "    )\n"
    "    for citation in model.citations:\n"
    "        locator = citation.reference.locator or citation.reference.label\n"
    "        if not incomplete:\n"
    "            displayed = display_prior_reference_locator(citation, model)\n"
    "            if displayed is not None:\n"
    "                locator = displayed\n"
    '        lines.append(f"**[R{citation.number}] {locator}.**")\n'
)
TEST_GROUPS = (
    ("phase172_r5_prior_reference_display/tests/test_projection.py",),
    ("phase172_r4_hopf_surjectivity_display/tests/test_projection.py",),
    ("phase172_r3_hopf_chain_display/tests/test_projection.py",),
    ("phase172_r2_suspension_relation_display/tests/test_projection.py",),
    ("phase171_r20r13_eta_sentence_layout/tests/test_projection.py",),
    ("phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py",),
)


def command(args: list[str], *, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False, timeout=timeout,
    )


def git(*args: str) -> str:
    if not args or args[0] not in {"branch", "rev-parse", "ls-remote"}:
        raise ValueError("read-only Git information only")
    process = command(["git", *args])
    if process.returncode:
        raise RuntimeError("Git command failed: " + repr(args) + process.stderr[-800:])
    return process.stdout.strip()


def normalize(source: bytes) -> str:
    text = source.decode("utf-8-sig")
    if "\r" in text.replace("\r\n", ""):
        raise ValueError("mixed line endings in reviewed source")
    return text.replace("\r\n", "\n")


def updated_renderer(source: bytes) -> bytes:
    original = normalize(source)
    if original.count(OLD) != 1 or NEW in original:
        raise RuntimeError("Renderer citation loop does not match reviewed R4 anchor")
    modified = original.replace(OLD, NEW, 1)
    tree = ast.parse(modified)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "render_model_backed_narrative_markdown"]
    if len(matches) != 1:
        raise RuntimeError("Renderer function identity changed")
    newline = "\r\n" if b"\r\n" in source else "\n"
    return modified.replace("\n", newline).encode("utf-8")


def full_function(source: bytes) -> str:
    text = normalize(source)
    tree = ast.parse(text)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == "render_model_backed_narrative_markdown"]
    if len(nodes) != 1:
        raise RuntimeError("Renderer function missing or duplicated")
    node = nodes[0]
    return "\n".join(text.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def preflight() -> dict[str, object]:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("R5 requires develop branch")
    for path, sha in (
        (Path("phase172_r4_hopf_surjectivity_display/projection.py"), R4_PROJECTION_SHA256),
        (Path("phase172_r4_hopf_surjectivity_display/tests/test_projection.py"), R4_TEST_SHA256),
        (Path("phase172_r4_hopf_surjectivity_display/install.py"), R4_INSTALL_SHA256),
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError("R4 prerequisite missing: " + str(path))
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != sha:
            raise RuntimeError("R4 prerequisite differs from reviewed content: " + str(path))
    if (r3_installer.REVIEWED_GIT_BLOB != r4_installer.BASE_R2_BLOB):
        raise RuntimeError("R3/R4 committed baseline mismatch")
    blob = subprocess.run(
        ["git", "cat-file", "blob", r4_installer.BASE_R2_BLOB],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    r3_expected = r3_installer.transformed(blob)
    r4_expected = r4_installer.updated_renderer(r3_expected)
    current = (ROOT / TARGET).read_bytes()
    if normalize(current) != normalize(r4_expected):
        raise RuntimeError("working Renderer is not reviewed R4 content")
    committed = subprocess.run(
        ["git", "show", "HEAD:" + TARGET.as_posix()],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    if normalize(committed) == normalize(r4_expected):
        state = "R4_COMMITTED"
    elif normalize(committed) == normalize(r3_expected):
        state = "R4_UNCOMMITTED"
    else:
        raise RuntimeError("committed Renderer is not reviewed R3/R4")
    for path in (PROJECTION, TESTS):
        if not (ROOT / path).is_file():
            raise RuntimeError("R5 payload is missing: " + str(path))
        ast.parse((ROOT / path).read_text(encoding="utf-8-sig"))
    updated_renderer(current)
    remote_result = command(["git", "ls-remote", "origin", "refs/heads/develop"], timeout=25)
    remote = (remote_result.stdout.split()[0]
              if remote_result.returncode == 0 and remote_result.stdout.strip() else None)
    if remote is not None and remote != head:
        raise RuntimeError("local HEAD differs from origin/develop")
    return {"branch": branch, "head": head, "remote": remote, "r4_state": state}


def output_directory() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "EHPProofTracerRecovery"
    output = base / ("phase172_r5_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ"))
    output.mkdir(parents=True, exist_ok=False)
    return output


def run_focused(output: Path) -> list[dict[str, object]]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    summary = []
    for number, paths in enumerate(TEST_GROUPS, 1):
        run = subprocess.run(
            [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
             "-p", "no:cacheprovider", *paths],
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=240,
        )
        log = run.stdout + "\n" + run.stderr
        (output / f"focused_{number}.log").write_text(log, encoding="utf-8")
        summary.append({"group": number, "paths": list(paths), "exit_code": run.returncode})
        print(f"PHASE172_R5_FOCUSED_{number}=" + ("PASS" if run.returncode == 0 else "FAIL"), flush=True)
        if run.returncode:
            raise RuntimeError(f"focused pytest group {number} failed:\n" + log[-3000:])
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-focused-tests", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.run_focused_tests:
        raise RuntimeError("R5 requires --run-focused-tests for write mode")
    state = preflight()
    print("PHASE172_R5_BRANCH=" + str(state["branch"]), flush=True)
    print("PHASE172_R5_HEAD=" + str(state["head"]), flush=True)
    print("PHASE172_R5_R4_RENDERER_STATE=" + str(state["r4_state"]), flush=True)
    print("PHASE172_R5_REVIEWED_CONTENT=PASS", flush=True)
    before = (ROOT / TARGET).read_bytes()
    after = updated_renderer(before)
    output = output_directory()
    (output / "render_model_backed_narrative_markdown_FULL.py").write_text(
        full_function(after), encoding="utf-8",
    )
    (output / "phase168_r3_5_model_renderer_FULL.py").write_bytes(after)
    if args.dry_run:
        print("PHASE172_R5_DRY_RUN=PASS", flush=True)
        print("PHASE172_R5_FULL_FUNCTION=" + str(output), flush=True)
        print("PHASE172_R5_SOURCE_CHANGES=0", flush=True)
        return 0
    (output / "renderer_before.py").write_bytes(before)
    report = {"phase": "172-R5", "mode": "PRESENTATION_ONLY", "state": state,
              "full_pytest_executed": False, "proof_tree_modified": False,
              "mathematical_rules_modified": False, "focused_tests": []}
    try:
        (ROOT / TARGET).write_bytes(after)
        report["focused_tests"] = run_focused(output)
        report["result"] = "PASS_R5_PRIOR_REFERENCE_DISPLAY_ONLY"
    except BaseException as exc:
        (ROOT / TARGET).write_bytes(before)
        report["result"] = "FAIL_RESTORED_SOURCE"
        report["exception"] = repr(exc)
        (output / "result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        print("PHASE172_R5_RESTORED=PASS", flush=True)
        print("PHASE172_R5_REPORT=" + str(output), flush=True)
        raise
    (output / "result.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE172_R5_REPORT=" + str(output), flush=True)
    print("PHASE172_R5_SOURCE_CHANGES=1", flush=True)
    print("PHASE172_R5_RESULT=PASS_R5_PRIOR_REFERENCE_DISPLAY_ONLY", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### `run.ps1`

```powershell
param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    if ($DryRun -and $RunFocusedTests) {
        throw 'Specify either -DryRun or -RunFocusedTests.'
    }
    if (-not $DryRun -and -not $RunFocusedTests) {
        throw 'Specify -DryRun or -RunFocusedTests.'
    }
    if ($DryRun) {
        python -B -m phase172_r5_prior_reference_display.install --dry-run
    }
    else {
        python -B -m phase172_r5_prior_reference_display.install --run-focused-tests
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R5 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
```

### `__init__.py`

```python
"""Phase 172 R5 presentation-only prior database citation projection."""
```
