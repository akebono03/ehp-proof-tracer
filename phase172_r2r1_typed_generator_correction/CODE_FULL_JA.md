# Phase 172 R2R1 — 変更コード全文

## 変更対象

1. `phase172_r2_suspension_relation_display/projection.py`：import 全文を含むファイル全文。新規 `same_typed_generator` を `redundant_suspension_relation_indices` の直前に追加し、後者を全文置換。
2. `phase172_r2_suspension_relation_display/tests/test_projection.py`：import 全文を含むファイル全文。ヘルパーを全文置換し、末尾にテストを1件追加。
3. `phase172_r2r1_typed_generator_correction/install.py`、`run.ps1`：新規追加。

**Renderer 本体について**：R2R1 では `phase168_r3_5_model_renderer.py` の変更は行わず、既存 R2 Installer による同一関数の変更を再適用する。既存 R2 `-DryRun` の生成物 `render_model_backed_narrative_markdown_FULL.py` と `phase168_r3_5_model_renderer_FULL.py` が、変更後の関数全文とファイル全文に該当する。今回の変更は新しいレンダラー関数置換を必要としない。

## 修正後 `projection.py` 全文・import 全文

```python
"""Suppress only redundant, proved suspension equalities in complete prose.

This is a display projection. It never constructs a proof, changes a ProofStep,
infers a new relation, or uses rendered strings to assert equality. A verified
and cited generator-suspension premise must remain visibly represented.
"""
from __future__ import annotations

from expression import HomotopyElement, Suspension
from homotopy_groups import TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from proof import ProofRule, Relation, RelationType


def same_typed_generator(left: object, right: object) -> bool:
    """Compare registered generator identity, degree and endpoints, not spelling.

    The repository can spell one eta generator with either a Unicode or
    underscore subscript. This structural check is family-independent and
    grants no mathematical equality outside an existing verified ProofStep.
    """
    return (
        isinstance(left, HomotopyElement)
        and isinstance(right, HomotopyElement)
        and left.generator is not None
        and left.generator == right.generator
        and left.dimension == right.dimension
        and left.source == right.source
        and left.target == right.target
    )


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
                and isinstance(relation.lhs, Suspension)
                and same_typed_generator(
                    relation.lhs.expression, generator.source_generator,
                )
                and same_typed_generator(
                    relation.rhs, generator.target_generator,
                )):
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

## 修正後 `tests/test_projection.py` 全文・import 全文

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
    same_typed_generator,
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
        and isinstance(step.conclusion.lhs, Suspension)
        and same_typed_generator(
            step.conclusion.lhs.expression,
            step.premises[0].conclusion.source_generator,
        )
        and same_typed_generator(
            step.conclusion.rhs,
            step.premises[0].conclusion.target_generator,
        )
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


def test_typed_identity_recognizes_a_display_alias_without_matching_others(
    verified_pi63,
):
    _, model = verified_pi63
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    suspension = model.steps[direct].premises[0].conclusion
    equality = model.steps[direct].conclusion
    assert isinstance(suspension, GeneratorSuspension)
    assert isinstance(equality.lhs, Suspension)
    # Two recorded names differ, but their registered structural types agree.
    assert suspension.source_generator.name != equality.lhs.expression.name
    assert same_typed_generator(
        suspension.source_generator, equality.lhs.expression,
    )
    assert not same_typed_generator(
        suspension.source_generator, suspension.target_generator,
    )
    assert not same_typed_generator(equality.lhs, suspension.source_generator)
    assert not same_typed_generator(object(), suspension.source_generator)
    assert symmetric != direct
```

## 新規 `install.py` 全文・import 全文

```python
"""Phase 172 R2R1: correct typed generator identity and replay R2 focused tests.

Only the two untracked Phase 172 R2 files are replaced. The original R2
installer alone applies the already reviewed one-function Renderer modification.
Every candidate source is content-guarded; all corrections are backed up.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
R2_PACKAGE = "phase172_r2_suspension_relation_display"
RENDERER = Path("phase168_r3_5_model_renderer.py")
REVIEWED_RENDERER_BLOB = "94996b403f1c01f81319824565db422463714f02"
FILES = {
    Path(R2_PACKAGE) / "projection.py": (
        "7795a363f315d3161d7bf4575cdadd9229cd90b8c765817ab16481f94ea01657",
        "a7d7072d2adfcdbc17e27200241b5240b0ab17148c60811388e2543df9c09818",
        PACKAGE / "payload/projection.py",
    ),
    Path(R2_PACKAGE) / "tests/test_projection.py": (
        "e9cca325dbc3e2f8eda67bf165f2c26ca83defeb3b32a59e581ae3a2804fa42d",
        "c021fae71c00e64589685e12061dbb6022ca22189c9ae7599f0a19a7a0ed4036",
        PACKAGE / "payload/test_projection.py",
    ),
}


def command(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if check and result.returncode:
        raise RuntimeError("command failed: " + repr(args) + "\n" + result.stderr[-1200:])
    return result


def git(*args: str) -> str:
    return command(["git", *args]).stdout.strip()


def normalized(source: bytes) -> bytes:
    text = source.decode("utf-8-sig")
    if "\r" in text.replace("\r\n", ""):
        raise RuntimeError("mixed or unreviewed newline convention")
    return text.replace("\r\n", "\n").encode("utf-8")


def digest(source: bytes) -> str:
    return hashlib.sha256(normalized(source)).hexdigest()


def output_directory() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    path = base / "EHPProofTracerRecovery" / ("phase172_r2r1_" + stamp)
    path.mkdir(parents=True, exist_ok=False)
    return path


def preflight() -> tuple[dict[str, object], str]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Phase 172 R2R1 requires develop")
    head = git("rev-parse", "HEAD")
    blob = git("rev-parse", "HEAD:" + RENDERER.as_posix())
    if blob != REVIEWED_RENDERER_BLOB:
        raise RuntimeError("Renderer HEAD content differs from reviewed baseline")
    from phase172_r2_suspension_relation_display.install import transformed
    committed = subprocess.run(
        ["git", "show", "HEAD:" + RENDERER.as_posix()],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    current = (ROOT / RENDERER).read_bytes()
    if normalized(current) == normalized(committed):
        renderer_state = "RESTORED_BASELINE"
    elif normalized(current) == normalized(transformed(committed)):
        renderer_state = "R2_ALREADY_INSTALLED"
    else:
        raise RuntimeError("Renderer has unrelated changes; no modification made")
    # Do not require the whole worktree to be clean; inspect only the target.
    tracked = command(["git", "status", "--porcelain", "--", RENDERER.as_posix()]).stdout
    if renderer_state == "RESTORED_BASELINE" and tracked.strip():
        raise RuntimeError("Renderer tracked status differs from baseline")
    rows: dict[str, object] = {}
    for relative, (old_hash, new_hash, payload) in FILES.items():
        path = ROOT / relative
        if not path.is_file() or not payload.is_file():
            raise RuntimeError("required R2 file/payload absent: " + str(relative))
        if digest(payload.read_bytes()) != new_hash:
            raise RuntimeError("correction payload hash mismatch: " + str(relative))
        current_hash = digest(path.read_bytes())
        if current_hash not in (old_hash, new_hash):
            raise RuntimeError("R2 file modified outside reviewed variants: " + str(relative))
        rows[str(relative)] = "ORIGINAL" if current_hash == old_hash else "CORRECTED"
    for extra in ("install.py", "run.ps1"):
        if not (ROOT / R2_PACKAGE / extra).is_file():
            raise RuntimeError("original R2 installer absent: " + extra)
    return {
        "branch": "develop", "head": head, "reviewed_renderer_blob": blob,
        "renderer_state": renderer_state, "files": rows,
    }, renderer_state


def run_r2_focused(output: Path, renderer_state: str) -> None:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    if renderer_state == "RESTORED_BASELINE":
        args = [sys.executable, "-B", "-m", R2_PACKAGE + ".install", "--run-focused-tests"]
    else:
        args = [sys.executable, "-B", "-c", (
            "from pathlib import Path; "
            "from phase172_r2_suspension_relation_display.install import run_focused; "
            "run_focused(Path(" + repr(str(output)) + "))"
        )]
    result = subprocess.run(
        args, cwd=ROOT, env=env, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    log = result.stdout + "\n" + result.stderr
    (output / "r2_focused_runner.log").write_text(log, encoding="utf-8")
    print(log[-8000:], flush=True)
    if result.returncode:
        raise RuntimeError("corrected R2 focused test run failed; see log")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-focused-tests", action="store_true")
    args = parser.parse_args()
    state, renderer_state = preflight()
    print("PHASE172_R2R1_BRANCH=" + str(state["branch"]), flush=True)
    print("PHASE172_R2R1_HEAD=" + str(state["head"]), flush=True)
    print("PHASE172_R2R1_REVIEWED_RENDERER=PASS", flush=True)
    print("PHASE172_R2R1_RENDERER_STATE=" + renderer_state, flush=True)
    print("PHASE172_R2R1_PAYLOAD_GUARD=PASS", flush=True)
    if args.dry_run:
        print("PHASE172_R2R1_DRY_RUN=PASS", flush=True)
        print("PHASE172_R2R1_SOURCE_CHANGES=0", flush=True)
        return 0
    output = output_directory()
    original = {rel: (ROOT / rel).read_bytes() for rel in FILES}
    report: dict[str, object] = {
        "phase": "172-R2R1", "mode": "TYPED_IDENTITY_CORRECTION",
        "preflight": state, "full_pytest_executed": False,
        "math_inference_changed": False, "proof_tree_changed": False,
    }
    try:
        for relative, (_, _, payload) in FILES.items():
            destination = ROOT / relative
            (output / (destination.name + "." + destination.parent.name + ".before")).write_bytes(original[relative])
            destination.write_bytes(payload.read_bytes())
        print("PHASE172_R2R1_TWO_FILES_CORRECTED=PASS", flush=True)
        if args.run_focused_tests:
            run_r2_focused(output, renderer_state)
        report["result"] = "PASS_R2R1_CORRECTION"
    except BaseException:
        for relative, content in original.items():
            (ROOT / relative).write_bytes(content)
        report["result"] = "FAILED_CORRECTION_FILES_RESTORED"
        (output / "result.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
        )
        print("PHASE172_R2R1_CORRECTION_RESTORED=PASS", flush=True)
        raise
    (output / "result.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    print("PHASE172_R2R1_REPORT=" + str(output), flush=True)
    print("PHASE172_R2R1_RESULT=PASS_R2R1_CORRECTION", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 新規 `run.ps1` 全文

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
    $Arguments = @('-B', '-m', 'phase172_r2r1_typed_generator_correction.install')
    if ($DryRun) {
        $Arguments += '--dry-run'
    }
    if ($RunFocusedTests) {
        $Arguments += '--run-focused-tests'
    }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R2R1 failed with exit code $LASTEXITCODE"
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

