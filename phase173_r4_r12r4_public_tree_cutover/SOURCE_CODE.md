# Phase 173 R4-R12R4R1 — Source code (full replacement units)

This package includes complete, directly replaceable files or complete functions. No ellipses are used to omit code.

Changed code in R4-R12R4R1: `install.py` and `tests/test_install.py`. The other files remain as in R4-R12R4.

## Updated installer (complete source)

Path: `phase173_r4_r12r4_public_tree_cutover/install.py`

```python
"""Phase 173 R4-R12R4: guarded Web narrative cutover to ProofNarrativeModel.

Only three reviewed files are changed. Never edits proof search, proof steps,
references, or the actual model renderer. Historical projector APIs stay intact.
"""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess


REVIEWED_HEAD = "188f707e1fcd8fde7b22af02a6b4005986fb3c1e"
ADAPTER = "phase165_r52_r3_web_adapter.py"
AUDIT = "phase173_r4_r13_narrative_audit/audit.py"
AUDIT_TEST = "phase173_r4_r13_narrative_audit/tests/test_audit.py"
BASELINE_BLOBS = {
    ADAPTER: "57b079d51d6d5810ab0be6884feae1ed117a386c",
    AUDIT: "6cb7fcd18e3bb7af2a376e656b2bef44b22d3e6e",
    AUDIT_TEST: "ccc746376f900c49c46751f6fa7cd1c89e6fa37b",
}
FIXTURES = {
    ADAPTER: "web_adapter_FULL.py",
    AUDIT: "inspect_dimension_FULL.py",
    AUDIT_TEST: "test_audit_FULL.py",
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return completed.stdout.strip()


def git_bytes(root: Path, *args: str) -> bytes:
    return subprocess.run(
        ("git", *args), cwd=root, capture_output=True, check=True,
    ).stdout


def replace_function(source: str, func_name: str, complete_function: str) -> str:
    """Replace one complete top-level function; never edit a partial body."""
    tree = ast.parse(source)
    expected = tuple(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == func_name
    )
    fixture = ast.parse(complete_function)
    if (len(expected) != 1 or len(fixture.body) != 1
            or not isinstance(fixture.body[0], ast.FunctionDef)
            or fixture.body[0].name != func_name):
        raise RuntimeError("Full function replacement does not match reviewed code")
    old = expected[0]
    lines = source.splitlines(keepends=True)
    newline = "\r\n" if "\r\n" in source else "\n"
    replacement = complete_function.replace("\n", newline)
    updated = "".join(lines[:old.lineno - 1]) + replacement + "".join(lines[old.end_lineno:])
    ast.parse(updated)
    return updated


def replacement_bytes(root: Path, path: str, fixture_dir: Path) -> bytes:
    original = git_bytes(root, "show", "HEAD:" + path)
    fixture = (fixture_dir / FIXTURES[path]).read_text(encoding="utf-8")
    ast.parse(fixture, filename=FIXTURES[path])
    if path == AUDIT:
        return replace_function(
            original.decode("utf-8-sig"), "inspect_dimension", fixture,
        ).encode("utf-8")
    return fixture.encode("utf-8")


def reviewed_head_lineage_allowed(root: Path, head: str) -> bool:
    """Allow only verified audit-only descendants of the reviewed production tree.

    Changing HEAD alone never authorizes a patch. The three target blobs are
    separately verified by preflight. Any other intervening repository change
    (including a renderer, proof rule, or test outside the audit directory)
    requires a new review and this function intentionally fails closed.
    """
    if head == REVIEWED_HEAD:
        return True
    ancestry = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestry.returncode != 0:
        return False
    committed_paths = git(
        root, "diff", "--name-only", REVIEWED_HEAD + ".." + head,
    ).splitlines()
    return all(
        path == ".pytest_cache/v/cache/nodeids"
        or path.startswith("phase173_r4_r12r3_architecture_audit/")
        for path in committed_paths
    )


def preflight(root: Path, fixture_dir: Path) -> dict[str, tuple[bytes, bytes]]:
    """Require reviewed Git ancestry and unchanged target blobs."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Run from the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("develop branch is required")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError(f"GitHub/local HEAD mismatch: local={head} remote={remote}")
    if not reviewed_head_lineage_allowed(root, head):
        raise RuntimeError(
            "HEAD is not a reviewed audit-only descendant: " + head
        )
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes must be reviewed first")
    dirty = set(git(root, "diff", "--name-only").splitlines())
    allowed = set(BASELINE_BLOBS) | {".pytest_cache/v/cache/nodeids"}
    if not dirty.issubset(allowed):
        raise RuntimeError("Unexpected tracked worktree changes: " + ", ".join(sorted(dirty - allowed)))
    content = {}
    for path, blob in BASELINE_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("Reviewed blob differs: " + path)
        original = git_bytes(root, "show", "HEAD:" + path)
        replacement = replacement_bytes(root, path, fixture_dir)
        compile(replacement, path, "exec")
        current = (root / path).read_bytes()
        if current not in (original, replacement):
            raise RuntimeError("Unreviewed local target content: " + path)
        content[path] = original, replacement
    adapter_source = content[ADAPTER][1].decode("utf-8")
    if "project_verified_toda56_narrative" in adapter_source:
        raise RuntimeError("Post-render projector is still reachable from Web adapter")
    print("PHASE173_R4_R12R4_HEAD=" + head)
    print("PHASE173_R4_R12R4_REVIEWED_BASE_HEAD=" + REVIEWED_HEAD)
    print("PHASE173_R4_R12R4_HEAD_LINEAGE=PASS")
    print("PHASE173_R4_R12R4_PREFLIGHT=PASS")
    return content


def update_files(root: Path, content: dict[str, tuple[bytes, bytes]], *, rollback: bool) -> None:
    """Apply the checked replacements; undo partial writes on any exception."""
    changed: list[tuple[Path, bytes, bytes]] = []
    try:
        for path, (original, replacement) in content.items():
            target = root / path
            present = target.read_bytes()
            expected = replacement if rollback else original
            desired = original if rollback else replacement
            if present == desired:
                print("PHASE173_R4_R12R4_ALREADY_DESIRED=" + path)
                continue
            if present != expected:
                raise RuntimeError("Refusing to overwrite an unexpected file: " + path)
            staged_file = target.with_name(target.name + ".r4r12r4_tmp")
            staged_file.write_bytes(desired)
            staged_file.replace(target)
            changed.append((target, present, desired))
            print(("PHASE173_R4_R12R4_ROLLED_BACK=" if rollback else "PHASE173_R4_R12R4_PATCHED=") + path)
    except Exception:
        for target, before, after in reversed(changed):
            if target.read_bytes() == after:
                target.write_bytes(before)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--apply", action="store_true")
    action.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    fixture_dir = Path(__file__).resolve().parent / "fixtures"
    content = preflight(root, fixture_dir)
    if args.dry_run:
        print("PHASE173_R4_R12R4_DRY_RUN=PASS")
        print("PHASE173_R4_R12R4_PRODUCTION_EDIT=NONE")
        return 0
    update_files(root, content, rollback=args.rollback)
    print("PHASE173_R4_R12R4_RESULT=" + ("ROLLED_BACK" if args.rollback else "PATCHED"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Updated installer tests (complete source)

Path: `phase173_r4_r12r4_public_tree_cutover/tests/test_install.py`

```python
"""Focused structural protection for the model-backed public cutover."""
from __future__ import annotations

import ast
from pathlib import Path
import subprocess

import pytest

from phase173_r4_r12r4_public_tree_cutover import install
from phase173_r4_r12r4_public_tree_cutover.install import (
    replace_function,
)


def test_full_adapter_does_not_use_post_render_narrative_override() -> None:
    fixture = (Path(__file__).resolve().parents[1] / "fixtures"
               / "web_adapter_FULL.py").read_text(encoding="utf-8")
    parsed = ast.parse(fixture)
    matches = tuple(node for node in parsed.body
                    if isinstance(node, ast.FunctionDef)
                    and node.name == "build_partial_web_group_proof_view")
    assert len(matches) == 1
    assert "render_model_backed_narrative_markdown(result, narrative_model)" in fixture
    assert "project_verified_pi74_narrative" not in fixture
    assert "project_verified_toda56_narrative" not in fixture
    assert not any(isinstance(node, ast.Constant) and node.value is Ellipsis
                   for node in ast.walk(parsed))


def test_replacement_requires_full_single_function() -> None:
    source = "def inspect_dimension(value):\n    return value\n"
    full = "def inspect_dimension(value):\n    return value + 1\n"
    assert replace_function(source, "inspect_dimension", full) == full
    with pytest.raises(RuntimeError, match="Full function replacement"):
        replace_function(source, "inspect_dimension", "x = 3\n")


def test_all_patch_fixtures_compile() -> None:
    folder = Path(__file__).resolve().parents[1] / "fixtures"
    for filename in (
        "web_adapter_FULL.py", "inspect_dimension_FULL.py", "test_audit_FULL.py",
    ):
        source = (folder / filename).read_text(encoding="utf-8")
        assert ast.parse(source)


def _git_in_test_repo(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", check=True,
    )
    return completed.stdout.strip()


def _new_reviewed_test_repo(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "repository"
    root.mkdir()
    _git_in_test_repo(root, "init", "-q")
    _git_in_test_repo(root, "config", "user.name", "Audit Test")
    _git_in_test_repo(root, "config", "user.email", "audit@example.invalid")
    (root / "seed.txt").write_text("reviewed baseline\n", encoding="utf-8")
    _git_in_test_repo(root, "add", "seed.txt")
    _git_in_test_repo(root, "commit", "-q", "-m", "reviewed baseline")
    return root, _git_in_test_repo(root, "rev-parse", "HEAD")


def test_reviewed_head_lineage_allows_only_audit_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, base = _new_reviewed_test_repo(tmp_path)
    monkeypatch.setattr(install, "REVIEWED_HEAD", base)
    audit = root / "phase173_r4_r12r3_architecture_audit" / "audit_result.json"
    audit.parent.mkdir(parents=True)
    audit.write_text("{}\n", encoding="utf-8")
    _git_in_test_repo(root, "add", str(audit.relative_to(root)))
    _git_in_test_repo(root, "commit", "-q", "-m", "audit only")
    head = _git_in_test_repo(root, "rev-parse", "HEAD")
    assert install.reviewed_head_lineage_allowed(root, base) is True
    assert install.reviewed_head_lineage_allowed(root, head) is True


def test_reviewed_head_lineage_rejects_production_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, base = _new_reviewed_test_repo(tmp_path)
    monkeypatch.setattr(install, "REVIEWED_HEAD", base)
    production = root / "phase168_r3_5_model_renderer.py"
    production.write_text("# changed renderer\n", encoding="utf-8")
    _git_in_test_repo(root, "add", production.name)
    _git_in_test_repo(root, "commit", "-q", "-m", "unexpected renderer change")
    head = _git_in_test_repo(root, "rev-parse", "HEAD")
    assert install.reviewed_head_lineage_allowed(root, head) is False
```

## PowerShell runner (unchanged, complete source)

Path: `phase173_r4_r12r4_public_tree_cutover/run.ps1`

```powershell
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Module = 'phase173_r4_r12r4_public_tree_cutover.install'
$Applied = $false
Push-Location $RepoRoot
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 173 R4-R12R4 git fetch failed'
    }

    python -m $Module --root . --dry-run
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 173 R4-R12R4 Preflight failed'
    }

    if ($DryRun) {
        python -m pytest -q phase173_r4_r12r4_public_tree_cutover/tests/test_install.py
        if ($LASTEXITCODE -ne 0) {
            throw 'Phase 173 R4-R12R4 static fixture tests failed'
        }
        Write-Output 'PHASE173_R4_R12R4_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R12R4_PRODUCTION_EDIT=NONE'
        return
    }

    python -m $Module --root . --apply
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 173 R4-R12R4 apply failed'
    }
    $Applied = $true

    python -m pytest -q `
        phase173_r4_r12r4_public_tree_cutover/tests `
        phase173_r4_r12_common_narrative/tests/test_projection.py `
        phase173_r4_r12_common_narrative/tests/test_install.py `
        phase173_r4_r13_narrative_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 173 R4-R12R4 focused pytest failed'
    }
    Write-Output 'PHASE173_R4_R12R4_FOCUSED_PYTEST=PASS'
    Write-Output 'PHASE173_R4_R12R4_PUBLIC_MODEL_RENDERER=CUTOVER'
    Write-Output 'PHASE173_R4_R12R4_PHASE_COMPLETED=False'
    Write-Output 'PHASE173_R4_R12R4_CENTRAL_RENDERER_REVIEW_PENDING=True'
}
catch {
    if ($Applied) {
        Write-Output 'PHASE173_R4_R12R4_FOCUSED_PYTEST_FAILED_ROLLBACK_START'
        python -m $Module --root . --rollback
        if ($LASTEXITCODE -ne 0) {
            Write-Output 'PHASE173_R4_R12R4_ROLLBACK_FAILED_MANUAL_REVIEW_REQUIRED'
        }
        else {
            Write-Output 'PHASE173_R4_R12R4_ROLLBACK=PASS'
        }
    }
    throw
}
finally {
    Pop-Location
}
```

## Web adapter replacement (complete source)

Path: `phase173_r4_r12r4_public_tree_cutover/fixtures/web_adapter_FULL.py`

```python
"""Phase 165 R52-R3: common WebGroupProofView for partial proof states.

The adapter does not search for evidence, infer mathematical statements or
promote unproved goals into proven steps. Complete proof narratives use the
verified ProofNarrativeModel renderer without a post-render override.
"""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus, render_partial_proof_markdown
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from web_group_proof_common import (
    WebGroupProofStepView,
    WebGroupProofView,
    _build_group_proof_rendered_lines,
    _group_proof_rule_name,
    _group_proof_statement_latex,
)


def build_partial_web_group_proof_view(
    result: PartialProofResult,
    *,
    max_depth: int = 2,
    mode: str = "narrative",
    narrative_model: ProofNarrativeModel | None = None,
) -> WebGroupProofView:
    """Adapt searched steps; render a supplied proof model without rewriting it."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an int")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")
    if narrative_model is not None and not isinstance(narrative_model, ProofNarrativeModel):
        raise TypeError("narrative_model must be ProofNarrativeModel or None")

    n = result.target.sphere_dimension
    dimension = result.target.group_dimension
    k = dimension - n
    target_latex = rf"\pi_{{{dimension}}}^{{{n}}}"
    if result.status is ProofSearchStatus.COMPLETE:
        target_statement = result.conclusion
    else:
        target_statement = next(
            (
                item for item in reversed(result.open_goals)
                if getattr(item, "lhs", None) == result.target
                or getattr(item, "group", None) == result.target
            ),
            None,
        )
    if target_statement is not None:
        statement_latex, fallback_type = _group_proof_statement_latex(target_statement)
        if statement_latex is not None and fallback_type is None:
            target_latex = statement_latex

    steps = []
    for step in result.proven_steps:
        statement_latex, fallback_type_name = _group_proof_statement_latex(step.conclusion)
        steps.append(WebGroupProofStepView(
            depth=0,
            statement_latex=statement_latex,
            fallback_type_name=fallback_type_name,
            rule_name=_group_proof_rule_name(step),
            role_name="derived",
        ))

    if mode == "trace":
        rendered_lines = ()
    else:
        if narrative_model is None:
            markdown = render_partial_proof_markdown(result)
        else:
            from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
            markdown = render_model_backed_narrative_markdown(result, narrative_model)
        rendered_lines = _build_group_proof_rendered_lines(markdown)

    return WebGroupProofView(
        n=n,
        k=k,
        conclusion_latex=target_latex,
        theorem=None,
        phase="165 R52-R3",
        key=("generic-complete-proof" if result.status is ProofSearchStatus.COMPLETE else "generic-partial-proof"),
        steps=tuple(steps),
        max_depth=max_depth,
        mode=mode,
        rendered_lines=rendered_lines,
        partial_result=(result.status is not ProofSearchStatus.COMPLETE),
    )
```

## R4-R13 inspect_dimension replacement (complete function)

Path: `phase173_r4_r12r4_public_tree_cutover/fixtures/inspect_dimension_FULL.py`

```python
def inspect_dimension(dimension: int, *, with_web: bool = True) -> dict:
    """Audit certified sources, and compare Web output to the model renderer."""
    if type(dimension) is not int or dimension not in (7, 8, 9, 10, 11):
        raise ValueError("R4-R13 concerns only five already-completed dimensions")
    bridge = build_shared_typed_bridge()
    contexts: list = []
    result = search_group_from_registered_goal(
        n=4, k=dimension - 4, bridge=bridge,
        context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or len(contexts) != 1):
        raise ValueError(f"pi_{dimension}^4 no longer has a completed screened proof")
    model = build_linked_proof_narrative_model(result, contexts[0])
    if model.root_index is None:
        raise ValueError("A complete proof lacks a narrative root")
    root = model.steps[model.root_index]
    name = getattr(getattr(root, "inference_rule", None), "name", None)
    expected_name = LEGACY_ROOT if dimension == 7 else (
        SOURCE_FIRST_ROOT if dimension in (8, 9, 10) else GENERIC_ROOT
    )
    if (root.rule is not ProofRule.INFERENCE
            or name != expected_name
            or root.conclusion != result.conclusion
            or root.inference_rule is None
            or len(root.premises) != 4
            or not root.inference_rule.match_guard(root.premises, {})):
        raise ValueError(f"Unexpected typed proof root for pi_{dimension}^4")
    if dimension > 7:
        theorem, left, right, hopf = root.premises
        first = exact_prior_database_result(3, dimension - 4)
        second = exact_prior_database_result(7, dimension - 7)
        if (left.conclusion != first or right.conclusion != second
                or not verified_db_step(left, proof_target=result.conclusion,
                                        bridge=contexts[0])
                or not verified_db_step(right, proof_target=result.conclusion,
                                        bridge=contexts[0])):
            raise ValueError("One or both adopted database priors lost certification")
        sources = (
            _source_number(model, theorem, locator="Proposition 4.4"),
            _source_number(model, left, db_prior=True),
            _source_number(model, right, db_prior=True),
            _source_number(model, hopf.premises[0], locator="Lemma 5.4"),
        )
        if len(set(sources)) != 4:
            raise ValueError("Cited source identities were conflated")
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    ancestors = root_ancestor_step_indices(model.steps, model.root_index)
    citations = tuple({
        "number": citation.number,
        "locator": citation.reference.locator or citation.reference.label,
        "step_indices": list(citation.step_indices),
    } for citation in model.citations)
    if len(citations) != 4 or any(
        not set(citation["step_indices"]).issubset(ancestors)
        for citation in citations
    ):
        raise ValueError("Source references are not bound to the proof ancestry")
    base = render_model_backed_narrative_markdown(result, model)
    if ("使用する結果" not in base
            or base.count("\n証明\n") != 1
            or not base.endswith("□\n")):
        raise ValueError("Common narrative sections are missing or malformed")
    if with_web:
        from web_group_proof_common import _build_group_proof_rendered_lines
        view = build_standard_web_group_proof_view(
            n=4, k=dimension - 4,
            mode="narrative", citation_source="model",
        )
        if (view.key != "generic-complete-proof" or view.partial_result
                or not view.rendered_lines
                or view.rendered_lines != _build_group_proof_rendered_lines(base)):
            raise ValueError("Web narrative diverges from the verified model renderer")
    row = {
        "group": f"pi_{dimension}^4",
        "dimension": dimension,
        "root_rule": name,
        "source_verified": True,
        "source_reference_count": len(citations),
        "source_references": citations,
        "open_goals": len(result.open_goals),
        "web_verified": with_web,
        "narrative_markdown": base,
    }
    print(
        f"PHASE173_R4_R13_PI_{dimension}_4"
        f" ROOT_CERTIFIED=True REFERENCES={len(citations)}"
        f" OPEN=0 WEB_CHECKED={with_web}",
        flush=True,
    )
    return row
```

## R4-R13 test replacement (complete source)

Path: `phase173_r4_r12r4_public_tree_cutover/fixtures/test_audit_FULL.py`

```python
"""Focused assertions about certified sources and the common Web narrative."""
from __future__ import annotations

import pytest

from phase173_r4_r13_narrative_audit.audit import (
    inspect_dimension,
    inspect_unproven_epsilon,
)


@pytest.mark.parametrize("dimension", (7, 8, 9, 10, 11))
def test_five_proven_toda_narratives_preserve_sources_and_web(
    dimension: int,
) -> None:
    row = inspect_dimension(dimension, with_web=True)
    assert row["source_verified"] is True
    assert row["web_verified"] is True
    assert row["open_goals"] == 0
    assert row["source_reference_count"] == 4
    assert "使用する結果" in row["narrative_markdown"]
    assert row["narrative_markdown"].endswith("□\n")


def test_zero_group_has_no_fake_generator_image() -> None:
    row = inspect_dimension(11, with_web=False)
    assert row["source_verified"] is True
    assert row["source_reference_count"] == 4
    assert r"\Phi_{11}(" not in row["narrative_markdown"]


def test_unproved_epsilon_does_not_enter_common_root() -> None:
    assert inspect_unproven_epsilon() is True


def test_audit_rejects_unreviewed_group_dimensions() -> None:
    with pytest.raises(ValueError):
        inspect_dimension(12, with_web=False)
```

## Public contract tests (complete source)

Path: `phase173_r4_r12r4_public_tree_cutover/tests/test_public_contract.py`

```python
"""Live source-owned public narrative tests for the five completed n=4 groups."""
from __future__ import annotations

import ast
from pathlib import Path
import re

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _build_group_proof_rendered_lines


@pytest.mark.parametrize("dimension", (7, 8, 9, 10, 11))
def test_public_matches_common_renderer_and_certified_root(dimension: int) -> None:
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=dimension - 4, bridge=build_shared_typed_bridge(),
        context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert len(contexts) == 1
    model = build_linked_proof_narrative_model(result, contexts[0])
    assert model.root_index is not None
    root = model.steps[model.root_index]
    assert root.conclusion == result.conclusion
    assert root.inference_rule.match_guard(root.premises, {})
    ancestors = root_ancestor_step_indices(model.steps, model.root_index)
    assert len(model.citations) == 4
    for citation in model.citations:
        assert set(citation.step_indices).issubset(ancestors)
        assert citation.number >= 1
    rendered = render_model_backed_narrative_markdown(result, model)
    view = build_standard_web_group_proof_view(
        n=4, k=dimension - 4, mode="narrative", citation_source="model",
    )
    assert "先行データベース結果" in rendered or "DB prior: sphere.csv" in rendered
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert "\\pi_" in view.conclusion_latex
    assert view.rendered_lines == _build_group_proof_rendered_lines(rendered)
    for citation in model.citations:
        assert f"[R{citation.number}]" in rendered


def test_active_web_adapter_cannot_depend_on_pi_specific_narrative() -> None:
    source = Path("phase165_r52_r3_web_adapter.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = tuple(node for node in tree.body if isinstance(node, ast.FunctionDef)
                      and node.name == "build_partial_web_group_proof_view")
    assert len(functions) == 1
    assert "project_verified_toda56_narrative" not in source
    assert "project_verified_pi74_narrative" not in source
    assert "render_model_backed_narrative_markdown(result, narrative_model)" in source
    function = functions[0]
    for node in ast.walk(function):
        if isinstance(node, ast.ImportFrom):
            assert not re.search(r"pi[0-9]+.*narrative", node.module or "")
            for name in node.names:
                assert not re.search(r"pi[0-9]+.*narrative", name.name)
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "markdown"
                   for target in node.targets):
                if isinstance(node.value, ast.Call):
                    called = node.value.func
                    assert isinstance(called, ast.Name)
                    assert called.id in (
                        "render_partial_proof_markdown",
                        "render_model_backed_narrative_markdown",
                    )
        if isinstance(node, ast.If):
            for compare in ast.walk(node.test):
                if not isinstance(compare, ast.Compare):
                    continue
                fields = (compare.left, *compare.comparators)
                names = {value.id for value in fields if isinstance(value, ast.Name)}
                has_literal = any(isinstance(value, ast.Constant)
                                  and type(value.value) is int for value in fields)
                if names & {"n", "k", "dimension"} and has_literal:
                    assert not any(isinstance(op, (ast.Eq, ast.NotEq))
                                   for op in compare.ops)
```
