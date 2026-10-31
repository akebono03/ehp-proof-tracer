# Phase 172 R2 — 新規コード全文と変更関数の取り出し方法

## 既存の変更対象

- `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()`（関数全体）。

- 既存クラス変更なし。トップレベル import 節変更なし。

- **関数全文は `-DryRun` の時点で外部出力する**。出力名 `render_model_backed_narrative_markdown_FULL.py`、加えて `phase168_r3_5_model_renderer_FULL.py`。古い全文を持ち込むのではなく、HEAD 内容から完全な置換後関数を生成する。

## 新規ファイル・関数の追加位置

- すべて `phase172_r2_suspension_relation_display/` 以下に追加。Projection とテストの import は省略せず記載。


## `projection.py` 全文

```python

"""Suppress only redundant, proved suspension equalities in complete prose.

This is a display projection. It never constructs a proof, changes a ProofStep,
infers a new relation, or uses rendered strings to assert equality. A verified
and cited generator-suspension premise must remain visibly represented.
"""
from __future__ import annotations

from expression import Suspension
from homotopy_groups import TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from proof import ProofRule, Relation, RelationType


def redundant_suspension_relation_indices(
    model: object,
    display_order: tuple[int, ...],
    already_hidden: set[int] | frozenset[int] = frozenset(),
) -> frozenset[int]:
    """Identify exact suspension-equality and symmetry steps safe to omit.

    A source GeneratorSuspension must be an inference in the completed root
    ancestry, have a visible typed sentence, and depend on an actually cited
    GIVEN. Both follow-up relations must be uncited INFERENCE steps and have
    precisely the checked typed premises. Nothing is removed from the model.
    Other equality chains and hidden/uncited source sentences remain intact.
    """
    steps = getattr(model, "steps", None)
    numbers = getattr(model, "step_citation_numbers", None)
    root_index = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(numbers, tuple)
            or len(steps) != len(numbers) or type(root_index) is not int):
        return frozenset()
    try:
        ancestry = root_ancestor_step_indices(steps, root_index)
    except ValueError:
        return frozenset()
    order = tuple(display_order)
    if (any(type(index) is not int or index not in ancestry for index in order)
            or len(set(order)) != len(order)):
        return frozenset()
    eligible = set(order).difference(already_hidden)

    def unique_index(node: object) -> int | None:
        same_identity = [index for index, step in enumerate(steps) if step is node]
        if len(same_identity) == 1:
            return same_identity[0]
        if same_identity:
            return None
        same_value = [index for index, step in enumerate(steps) if step == node]
        return same_value[0] if len(same_value) == 1 else None

    def has_cited_given_ancestor(node: object) -> bool:
        pending = [node]
        visited: set[int] = set()
        while pending:
            step = pending.pop()
            if id(step) in visited:
                continue
            visited.add(id(step))
            index = unique_index(step)
            if index is None or index not in ancestry:
                return False
            if step.rule is ProofRule.GIVEN and numbers[index]:
                return True
            pending.extend(step.premises)
        return False

    redundant: set[int] = set()
    direct_indices: set[int] = set()
    for index in order:
        step = steps[index]
        relation = step.conclusion
        if (index not in eligible or index == root_index
                or step.rule is not ProofRule.INFERENCE
                or numbers[index]
                or len(step.premises) != 1
                or not isinstance(relation, Relation)
                or relation.relation_type is not RelationType.EQUALITY):
            continue
        parent = step.premises[0]
        parent_index = unique_index(parent)
        if parent_index is None or parent_index not in ancestry:
            continue
        generator = parent.conclusion
        if (parent_index in eligible
                and parent.rule is ProofRule.INFERENCE
                and isinstance(generator, GeneratorSuspension)
                and isinstance(generator.map, TodaSuspensionMap)
                and typed_sentence(generator, parent) is not None
                and has_cited_given_ancestor(parent)
                and relation.lhs == Suspension(generator.source_generator)
                and relation.rhs == generator.target_generator):
            redundant.add(index)
            direct_indices.add(index)

    for index in order:
        step = steps[index]
        relation = step.conclusion
        if (index not in eligible or index == root_index
                or step.rule is not ProofRule.INFERENCE
                or numbers[index]
                or len(step.premises) != 1
                or not isinstance(relation, Relation)
                or relation.relation_type is not RelationType.EQUALITY):
            continue
        parent = step.premises[0]
        parent_index = unique_index(parent)
        if parent_index not in direct_indices:
            continue
        previous = parent.conclusion
        if (parent.rule is ProofRule.INFERENCE
                and isinstance(previous, Relation)
                and previous.relation_type is RelationType.EQUALITY
                and relation.lhs == previous.rhs
                and relation.rhs == previous.lhs):
            redundant.add(index)
    return frozenset(redundant)

```


## `tests/test_projection.py` 全文

```python

"""Phase 172 R2: exact proof-ancestry-only suspension prose suppression."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Suspension
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase172_r2_suspension_relation_display.projection import (
    redundant_suspension_relation_indices,
)
from proof import ProofRule, Relation, RelationType


@pytest.fixture(scope="module")
def verified_pi63():
    original = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=original, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(original, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    return result, build_linked_proof_narrative_model(result, contexts[0])


def _verified_direct_and_symmetric_relation_indices(model):
    direct = [
        index for index, step in enumerate(model.steps)
        if isinstance(step.conclusion, Relation)
        and step.conclusion.relation_type is RelationType.EQUALITY
        and len(step.premises) == 1
        and isinstance(step.premises[0].conclusion, GeneratorSuspension)
        and step.conclusion.lhs == Suspension(
            step.premises[0].conclusion.source_generator
        )
        and step.conclusion.rhs == step.premises[0].conclusion.target_generator
    ]
    assert len(direct) == 1
    source_index = direct[0]
    symmetric = [
        index for index, step in enumerate(model.steps)
        if isinstance(step.conclusion, Relation)
        and step.conclusion.relation_type is RelationType.EQUALITY
        and len(step.premises) == 1
        and (step.premises[0] is model.steps[source_index]
             or step.premises[0] == model.steps[source_index])
        and step.conclusion.lhs == model.steps[source_index].conclusion.rhs
        and step.conclusion.rhs == model.steps[source_index].conclusion.lhs
    ]
    assert len(symmetric) == 1
    return source_index, symmetric[0]


def test_real_public_tree_hides_only_derived_suspension_equation_and_symmetry(
    verified_pi63,
):
    result, model = verified_pi63
    assert model.root_index is not None
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_26_exactness_projection import project_exactness_chains
    chains = project_exactness_chains(model)
    omitted = {index for chain in chains for index in chain.step_indices}
    order = tuple(row.step_index for row in project_narrative_order(model, omitted))
    indices = redundant_suspension_relation_indices(model, order)
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    assert indices == frozenset({direct, symmetric})
    assert all(model.steps[i].rule is ProofRule.INFERENCE for i in indices)
    assert all(not model.step_citation_numbers[i] for i in indices)
    assert any(
        child is not model.steps[symmetric]
        and any(parent is model.steps[direct] or parent == model.steps[direct]
                for parent in child.premises)
        for child in model.steps
    )
    assert any(
        any(parent is model.steps[symmetric] or parent == model.steps[symmetric]
            for parent in child.premises)
        for child in model.steps
    )
    assert result.proven_steps == model.steps


def test_real_complete_narrative_retains_cited_source_and_hopf_conclusion(
    verified_pi63,
):
    result, model = verified_pi63
    markdown = render_model_backed_narrative_markdown(result, model)
    references, body = markdown.split("\n証明\n", 1)
    assert "[R3] Chapter V, i)." in references
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert r"$E\eta_{5} = \eta_{6}$." not in body
    assert r"$\eta_{6} = E\eta_{5}$." not in body
    assert r"$\nu'\eta_{6} = \nu'E\eta_{5}$." in body
    assert r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$." in body
    assert r"\operatorname{ord}(\nu')=4" in body
    assert len(model.citations) == 8


def test_citation_on_relation_prevents_suppression(verified_pi63):
    _, model = verified_pi63
    edited = list(model.step_citation_numbers)
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    edited[direct] = (3,)
    changed = replace(model, step_citation_numbers=tuple(edited))
    order = tuple(range(len(model.steps)))
    hidden = redundant_suspension_relation_indices(changed, order)
    assert direct not in hidden and symmetric not in hidden


def test_missing_source_citation_preserves_both_lines(verified_pi63):
    _, model = verified_pi63
    edited = list(model.step_citation_numbers)
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    cited_family_source = next(
        index for index, step in enumerate(model.steps)
        if type(step.conclusion).__name__ == "TodaEtaFamilyGeneralDefinition"
        and model.step_citation_numbers[index]
    )
    edited[cited_family_source] = ()
    changed = replace(model, step_citation_numbers=tuple(edited))
    order = tuple(range(len(model.steps)))
    hidden = redundant_suspension_relation_indices(changed, order)
    assert direct not in hidden and symmetric not in hidden


def test_hidden_source_or_missing_root_does_not_suppress(verified_pi63):
    _, model = verified_pi63
    order = tuple(range(len(model.steps)))
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    source = model.steps[direct].premises[0]
    source_index = next(index for index, step in enumerate(model.steps)
                        if step is source or step == source)
    hidden = redundant_suspension_relation_indices(model, order, {source_index})
    assert direct not in hidden and symmetric not in hidden
    partial_like = replace(model, root_index=None)
    assert redundant_suspension_relation_indices(partial_like, order) == frozenset()

```


## `install.py` 全文

```python

"""Guarded Phase 172 R2 single-function insertion and focused verification.

Only phase168_r3_5_model_renderer.py is an existing production modification.
No mathematical proof or inference registration changes. Outputs and backup
are placed outside the Git worktree. On failure, source bytes are restored.
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

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path("phase168_r3_5_model_renderer.py")
PROJECTION = Path("phase172_r2_suspension_relation_display/projection.py")
REVIEWED_BLOB = "94996b403f1c01f81319824565db422463714f02"
ORIGINAL_ANCHOR = (
    "    if direct_sum_display is not None:\n"
    "        suppressed_body_indices.update(direct_sum_display.hidden_indices)\n"
    "    for index in order:\n"
)
UPDATED_ANCHOR = (
    "    if direct_sum_display is not None:\n"
    "        suppressed_body_indices.update(direct_sum_display.hidden_indices)\n"
    "    if not incomplete:\n"
    "        from phase172_r2_suspension_relation_display.projection import (\n"
    "            redundant_suspension_relation_indices,\n"
    "        )\n"
    "        suppressed_body_indices.update(\n"
    "            redundant_suspension_relation_indices(\n"
    "                model, order, suppressed_body_indices,\n"
    "            )\n"
    "        )\n"
    "    for index in order:\n"
)
TEST_GROUPS = (
    ("phase172_r2_suspension_relation_display/tests/test_projection.py",),
    ("phase171_r20r13_eta_sentence_layout/tests/test_projection.py",),
    ("phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py",),
    ("phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py",),
    ("phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py",),
)


def command(*args: str, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, check=False, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
        timeout=timeout,
    )


def checked(*args: str) -> str:
    result = command(*args)
    if result.returncode:
        raise RuntimeError("command failed: " + repr(args) + " " + result.stderr)
    return result.stdout.strip()


def lf(source: bytes) -> str:
    text = source.decode("utf-8-sig")
    if "\r" in text.replace("\r\n", ""):
        raise RuntimeError("unreviewed/mixed newline convention")
    return text.replace("\r\n", "\n")


def transformed(source: bytes) -> bytes:
    current = lf(source)
    if current.count(ORIGINAL_ANCHOR) != 1 or UPDATED_ANCHOR in current:
        raise RuntimeError("reviewed renderer anchor not found exactly once")
    updated = current.replace(ORIGINAL_ANCHOR, UPDATED_ANCHOR, 1)
    tree = ast.parse(updated)
    targets = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == "render_model_backed_narrative_markdown"]
    if len(targets) != 1:
        raise RuntimeError("renderer function identity changed")
    newline = "\r\n" if b"\r\n" in source else "\n"
    return updated.replace("\n", newline).encode("utf-8")


def function_text(source: bytes) -> str:
    updated = lf(source)
    tree = ast.parse(updated)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "render_model_backed_narrative_markdown"]
    if len(functions) != 1:
        raise RuntimeError("exactly one renderer function is required")
    node = functions[0]
    lines = updated.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def report_dir() -> Path:
    home = os.environ.get("LOCALAPPDATA")
    base = Path(home) if home else Path.home()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    target = base / "EHPProofTracerRecovery" / ("phase172_r2_" + stamp)
    target.mkdir(parents=True, exist_ok=False)
    return target


def preflight() -> dict[str, str]:
    branch = checked("git", "branch", "--show-current")
    head = checked("git", "rev-parse", "HEAD")
    blob = checked("git", "rev-parse", "HEAD:" + TARGET.as_posix())
    if branch != "develop":
        raise RuntimeError("R2 requires the develop branch")
    if blob != REVIEWED_BLOB:
        raise RuntimeError("reviewed source Git blob differs; do not patch")
    if not (ROOT / PROJECTION).is_file():
        raise RuntimeError("R2 projection module is absent")
    result = command("git", "status", "--porcelain", "--", TARGET.as_posix())
    if result.returncode:
        raise RuntimeError("unable to inspect tracked renderer status")
    if result.stdout.strip():
        raise RuntimeError("existing renderer has local changes; do not overwrite")
    tracked_result = subprocess.run(
        ("git", "show", "HEAD:" + TARGET.as_posix()),
        cwd=ROOT, check=True, capture_output=True,
    )
    tracked = tracked_result.stdout
    # Binary worktree comparison below is intentionally newline-tolerant;
    # HEAD blob identity remains the immutable reviewed-source guard.
    source = (ROOT / TARGET).read_bytes()
    if lf(source) != lf(tracked):
        raise RuntimeError("local renderer differs from reviewed HEAD content")
    if source.decode("utf-8-sig").startswith("\ufeff"):
        raise RuntimeError("unexpected source encoding")
    updated = transformed(source)
    return {
        "branch": branch,
        "head": head,
        "reviewed_git_blob": blob,
        "before_sha256": hashlib.sha256(source).hexdigest(),
        "after_sha256": hashlib.sha256(updated).hexdigest(),
    }


def run_focused(output: Path) -> list[dict[str, object]]:
    results = []
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    for i, paths in enumerate(TEST_GROUPS, 1):
        process = subprocess.run(
            [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
             "-p", "no:cacheprovider", *paths],
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False,
        )
        log = process.stdout + "\n" + process.stderr
        (output / f"focused_{i}.log").write_text(log, encoding="utf-8")
        results.append({"group": i, "paths": paths, "returncode": process.returncode,
                        "last_lines": log.splitlines()[-8:]})
        print(f"PHASE172_R2_FOCUSED_{i}=" +
              ("PASS" if process.returncode == 0 else "FAIL"), flush=True)
        if process.returncode:
            raise RuntimeError(f"focused pytest group {i} failed: " + log[-2000:])
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-focused-tests", action="store_true")
    args = parser.parse_args()
    state = preflight()
    print("PHASE172_R2_BRANCH=" + state["branch"], flush=True)
    print("PHASE172_R2_HEAD=" + state["head"], flush=True)
    print("PHASE172_R2_REVIEWED_BLOB=PASS", flush=True)
    original = (ROOT / TARGET).read_bytes()
    updated = transformed(original)
    if args.dry_run:
        output = report_dir()
        (output / "render_model_backed_narrative_markdown_FULL.py").write_text(
            function_text(updated) + "\n", encoding="utf-8",
        )
        (output / "phase168_r3_5_model_renderer_FULL.py").write_bytes(updated)
        print("PHASE172_R2_DRY_RUN=PASS", flush=True)
        print("PHASE172_R2_FULL_FUNCTION=" + str(output), flush=True)
        print("PHASE172_R2_SOURCE_CHANGES=0", flush=True)
        return 0

    output = report_dir()
    (output / "renderer_before.py").write_bytes(original)
    report: dict[str, object] = {
        "phase": "172-R2", "mode": "GUARDED_PRESENTATION_ONLY",
        "source": str(TARGET), "state": state,
        "focused": [], "full_pytest_executed": False,
        "proof_tree_changed": False, "math_inference_changed": False,
    }
    try:
        (ROOT / TARGET).write_bytes(updated)
        (output / "render_model_backed_narrative_markdown_FULL.py").write_text(
            function_text(updated) + "\n", encoding="utf-8",
        )
        (output / "phase168_r3_5_model_renderer_FULL.py").write_bytes(updated)
        if args.run_focused_tests:
            report["focused"] = run_focused(output)
        report["result"] = "PASS_R2_PRESENTATION_ONLY"
    except BaseException:
        (ROOT / TARGET).write_bytes(original)
        report["result"] = "FAILED_RESTORED_ORIGINAL_SOURCE"
        (output / "result.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("PHASE172_R2_RESTORED=PASS", flush=True)
        raise
    (output / "result.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("PHASE172_R2_REPORT=" + str(output), flush=True)
    print("PHASE172_R2_SOURCE_CHANGES=1", flush=True)
    print("PHASE172_R2_RESULT=PASS_R2_PRESENTATION_ONLY", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

```


## `run.ps1` 全文

```powershell

param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousLocation = (Get-Location).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousPythonUtf8 = $env:PYTHONUTF8
$PreviousPythonIoEncoding = $env:PYTHONIOENCODING
$PreviousDontWriteBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$PreviousPythonPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '-m', 'phase172_r2_suspension_relation_display.install')
    if ($DryRun) {
        $Arguments += '--dry-run'
    }
    if ($RunFocusedTests) {
        $Arguments += '--run-focused-tests'
    }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R2 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Set-Location $PreviousLocation
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONUTF8 = $PreviousPythonUtf8
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
    $env:PYTHONDONTWRITEBYTECODE = $PreviousDontWriteBytecode
}

```


## Renderer 内の置換アンカー全文

```python

    if direct_sum_display is not None:
        suppressed_body_indices.update(direct_sum_display.hidden_indices)
    if not incomplete:
        from phase172_r2_suspension_relation_display.projection import (
            redundant_suspension_relation_indices,
        )
        suppressed_body_indices.update(
            redundant_suspension_relation_indices(
                model, order, suppressed_body_indices,
            )
        )
    for index in order:

```
