# Phase 173 R4-R15R10 — Full source code

All executable units and new tests are reproduced in full below. Existing production modules are unchanged.

## `__init__.py`

```python
"""Phase 173 R4-R15R10: read-only common Narrative regression audit."""
```

## `audit.py`

```python
"""Read-only audit of the verified abstract/group Narrative boundary.

This audit does not infer generator relations, alter proof results, or write
production source files. It records remaining Narrative Model integration debt.
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path


EXPECTED_HEAD = "8bfa13946251c5618530641c572e8c756bb49af4"
REVIEWED_BLOBS = {
    "phase165_r52_r3_web_adapter.py": "a5c402c86e624010e5521ceda0cb1734ab32bcae",
    "phase165_r52_partial_proof.py": "0af6b459ed5a136a8e30a9e349ccf9fa601d448b",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_5_model_renderer.py": "6bfd5e992f6c9ee9441920e10e63e0db4bece289",
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py": "777db698e8da026571c8046b84fc3b875ee6dfe0",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
}


def git_output(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ("git", *arguments), cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return completed.stdout.strip()


def specialized_dimensions(tree: ast.AST) -> tuple[str, ...]:
    """Detect new n/k numeric equality tests in the two shared display units."""
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        operands = (node.left, *node.comparators)
        has_dimension = any(
            isinstance(inner, ast.Name) and inner.id in ("n", "k")
            for operand in operands for inner in ast.walk(operand)
        )
        has_literal = any(
            isinstance(operand, ast.Constant) and type(operand.value) is int
            for operand in operands
        )
        if has_dimension and has_literal:
            findings.append(f"line {node.lineno}: n/k literal comparison")
    return tuple(findings)


def preflight(root: Path) -> dict[str, object]:
    """Require reviewed GitHub objects, allowing a locally uncommitted R15R9 patch."""
    root = root.resolve()
    if git_output(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R15R10 requires the develop branch")
    remote = git_output(root, "rev-parse", "origin/develop")
    if remote != EXPECTED_HEAD:
        raise RuntimeError(
            f"GitHub develop changed: expected {EXPECTED_HEAD}, found {remote}; review before rerun"
        )
    blobs: dict[str, str] = {}
    for relative, expected in REVIEWED_BLOBS.items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"Required reviewed file is missing: {relative}")
        actual = git_output(root, "hash-object", f"--path={relative}", relative)
        if actual != expected:
            raise RuntimeError(
                f"Unreviewed source in {relative}: expected {expected}, found {actual}"
            )
        blobs[relative] = actual

    adapter = (root / "phase165_r52_r3_web_adapter.py").read_text(
        encoding="utf-8-sig"
    )
    projection = (root / "phase173_r4_r15r9_shared_abstract_renderer" / "projection.py").read_text(
        encoding="utf-8-sig"
    )
    model = (root / "phase168_r3_3_proof_narrative_model.py").read_text(
        encoding="utf-8-sig"
    )
    adapter_tree = ast.parse(adapter)
    projection_tree = ast.parse(projection)
    model_tree = ast.parse(model)
    hooks = sum(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "render_certified_abstract_section"
        for node in ast.walk(adapter_tree)
    )
    if hooks != 1:
        raise RuntimeError("The common Web adapter must use exactly one abstract-section hook")
    if adapter.count("_build_group_proof_rendered_lines(markdown)") != 1:
        raise RuntimeError("Common Markdown-to-Web projection is not single-pass")
    if "generic-complete-proof" not in adapter or "generic-partial-proof" not in adapter:
        raise RuntimeError("Complete/partial Web proof keys changed")
    branch_findings = specialized_dimensions(adapter_tree) + specialized_dimensions(projection_tree)
    if branch_findings:
        raise RuntimeError("Dedicated n/k presentation branch: " + "; ".join(branch_findings))
    narrative_class = next(
        (node for node in model_tree.body
         if isinstance(node, ast.ClassDef) and node.name == "ProofNarrativeModel"),
        None,
    )
    if narrative_class is None:
        raise RuntimeError("Canonical ProofNarrativeModel class missing")
    fields = tuple(
        node.target.id
        for node in narrative_class.body
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    )
    return {
        "reviewed_head": remote,
        "reviewed_blob_count": len(blobs),
        "shared_abstract_hook_count": hooks,
        "stem_specific_branch_count": len(branch_findings),
        "model_has_abstract_structure": "abstract_structure" in fields,
        "model_fields": fields,
        "production_files_edited_by_audit": False,
    }


def inspect_partial(k: int) -> dict[str, object]:
    """Check the normal search and Web entry with real registered evidence."""
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase173_r4_r15r9_shared_abstract_renderer.projection import (
        render_certified_abstract_section,
    )
    from web_group_proof import build_standard_web_group_proof_view
    from web_group_proof_common import _build_group_proof_rendered_lines

    n = 4
    goal = exact_prior_database_result(n, k)
    if goal is None:
        raise RuntimeError(f"No registered Group Goal for n={n}, k={k}")
    result = search_group_from_registered_goal(n=n, k=k, goal=goal)
    baseline = (
        result.status, result.conclusion, result.open_goals, result.proven_steps,
        result.references, result.diagnostics, result.abstract_structure,
    )
    model = build_proof_narrative_model(result)
    original_markdown = render_model_backed_narrative_markdown(result, model)
    abstract_markdown = render_certified_abstract_section(result)
    model_view = build_partial_web_group_proof_view(
        result, mode="narrative", narrative_model=model,
    )
    expected_lines = _build_group_proof_rendered_lines(
        original_markdown.rstrip() + "\n\n" + abstract_markdown + "\n"
    )
    model_projection_exact = model_view.rendered_lines == expected_lines
    view = build_standard_web_group_proof_view(
        n=n, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    after = (
        result.status, result.conclusion, result.open_goals, result.proven_steps,
        result.references, result.diagnostics, result.abstract_structure,
    )
    headings = tuple(
        line.prefix for line in view.rendered_lines if line.kind == "heading"
    )
    abstract_count = headings.count("証明済みの抽象群構造")
    goal_count = headings.count("未解決 Goal")
    structure = result.abstract_structure
    source_root_in_named_steps = bool(
        structure is not None
        and any(step is structure.proof_step for step in result.proven_steps)
    )
    pending = result.status in (
        ProofSearchStatus.SEARCH_FAILED, ProofSearchStatus.PARTIAL,
    )
    passed = (
        structure is not None
        and pending and result.conclusion is None and bool(result.open_goals)
        and baseline == after and model_projection_exact
        and abstract_count == 1 and goal_count == 1
        and view.key == "generic-partial-proof" and view.partial_result
        and any(
            rf"\pi_{{{n+k}}}^{{{n}}}" in (line.statement_latex or "")
            and r"\cong" in (line.statement_latex or "")
            for line in view.rendered_lines
        )
    )
    return {
        "n": n, "k": k, "group": f"pi_{n+k}^{n}",
        "status": result.status.value,
        "open_goals": len(result.open_goals),
        "references_in_search_result": len(result.references),
        "narrative_model_citations": len(model.citations),
        "abstract_heading_count": abstract_count,
        "unresolved_heading_count": goal_count,
        "abstract_root_is_named_proven_step": source_root_in_named_steps,
        "web_key": view.key, "web_partial": view.partial_result,
        "result_unchanged": baseline == after,
        "existing_citation_and_goal_projection_preserved": model_projection_exact,
        "passed": passed,
    }


def inspect_complete(n: int, k: int) -> dict[str, object]:
    """Check representative pre-existing completed groups through public Web."""
    from web_group_proof import build_standard_web_group_proof_view

    view = build_standard_web_group_proof_view(
        n=n, k=k, mode="narrative", citation_source="model",
    )
    headings = tuple(
        line.prefix for line in view.rendered_lines if line.kind == "heading"
    )
    passed = (
        view.key == "generic-complete-proof"
        and not view.partial_result
        and "証明済みの抽象群構造" not in headings
        and len(view.rendered_lines) > 0
    )
    return {
        "n": n, "k": k, "group": f"pi_{n+k}^{n}",
        "web_key": view.key,
        "web_partial": view.partial_result,
        "abstract_heading_count": headings.count("証明済みの抽象群構造"),
        "rendered_line_count": len(view.rendered_lines),
        "passed": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = preflight(args.root)
    print("PHASE173_R4_R15R10_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R10_MODEL_HAS_ABSTRACT=" +
          str(source["model_has_abstract_structure"]), flush=True)
    if args.preflight:
        print("PHASE173_R4_R15R10_PREFLIGHT=PASS", flush=True)
        return 0
    if args.output is None:
        parser.error("--output is required for normal audit")

    partial = [inspect_partial(k) for k in (8, 31)]
    complete = [inspect_complete(n, k) for n, k in ((3, 3), (4, 3))]
    passed = all(row["passed"] for row in partial + complete)
    report = {
        "phase": "173-R4-R15R10",
        "mode": "READ_ONLY_COMMON_NARRATIVE_REGRESSION_AUDIT",
        "source": source,
        "partial": partial,
        "complete": complete,
        "architecture_finding": (
            "Certified abstract proof is retained in PartialProofResult.abstract_structure; "
            "the existing ProofNarrativeModel has no abstract_structure field. "
            "The shared Web adapter appends one section after normal model rendering. "
            "Its abstract proof-root citations are not automatically included in "
            "ProofNarrativeModel.citations unless already present as named proof steps. "
            "Do not infer named-generator equalities or mark COMPLETE."
        ),
        "full_pytest_performed": False,
        "production_changed": False,
        "passed": passed,
    }
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    for row in partial:
        print(
            f"PHASE173_R4_R15R10_K={row['k']} "
            f"ABSTRACT_SECTION_COUNT={row['abstract_heading_count']} "
            f"OPEN_GOALS={row['open_goals']} "
            f"NAMED_PENDING={row['web_partial']}", flush=True,
        )
    for row in complete:
        print(
            f"PHASE173_R4_R15R10_COMPLETE_N={row['n']}_K={row['k']}="
            f"{row['passed']}", flush=True,
        )
    print("PHASE173_R4_R15R10_REPORT=" + str(output), flush=True)
    print("PHASE173_R4_R15R10_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/__init__.py`

```python
"""Focused regression tests for the read-only common Web/Narrative audit."""
```

## `tests/test_contract.py`

```python
"""Small regression checks for shared Web Adapter contracts; no source edits."""
from __future__ import annotations

import ast
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase173_r4_r15r10_common_route_audit.audit import specialized_dimensions


ROOT = Path(__file__).resolve().parents[2]


def test_shared_adapter_contains_single_abstract_projection_hook() -> None:
    path = ROOT / "phase165_r52_r3_web_adapter.py"
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    calls = tuple(
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "render_certified_abstract_section"
    )
    assert len(calls) == 1
    assert specialized_dimensions(tree) == ()


def test_abstract_projection_has_no_n_or_k_literal_branches() -> None:
    path = (ROOT / "phase173_r4_r15r9_shared_abstract_renderer" / "projection.py")
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    assert specialized_dimensions(tree) == ()


def test_bare_partial_result_keeps_unresolved_goal_and_original_key() -> None:
    result = make_partial_proof_result(
        n=4, k=8, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("unresolved named-generator relation",),
        diagnostics=("no registered proof",),
    )
    model = build_proof_narrative_model(result)
    view = build_partial_web_group_proof_view(
        result, mode="narrative", narrative_model=model,
    )
    assert view.key == "generic-partial-proof"
    assert view.partial_result is True
    assert result.conclusion is None
    assert result.open_goals == model.open_goals
    assert not any(
        line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
        for line in view.rendered_lines
    )
    assert any(
        line.kind == "heading" and line.prefix == "未解決 Goal"
        for line in view.rendered_lines
    )


def test_trace_mode_does_not_inject_any_abstract_narrative() -> None:
    result = make_partial_proof_result(
        n=4, k=8, status=ProofSearchStatus.PARTIAL,
        open_goals=("pending",), diagnostics=("awaiting source",),
    )
    view = build_partial_web_group_proof_view(result, mode="trace")
    assert view.key == "generic-partial-proof"
    assert view.partial_result is True
    assert view.rendered_lines == ()
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedHead = '8bfa13946251c5618530641c572e8c756bb49af4'
Push-Location $RepoRoot
try {
    if ((git branch --show-current).Trim() -ne 'develop') {
        throw 'R15R10 requires develop branch'
    }
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R10 git fetch failed' }
    $RemoteHead = (git rev-parse origin/develop).Trim()
    if ($RemoteHead -ne $ExpectedHead) {
        throw "GitHub develop HEAD changed: $RemoteHead (expected $ExpectedHead). Reaudit required."
    }
    python -m phase173_r4_r15r10_common_route_audit.audit --root "$RepoRoot" --preflight
    if ($LASTEXITCODE -ne 0) { throw 'R15R10 reviewed-source preflight failed' }
    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r10_common_route_audit/tests/test_contract.py `
        phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection_isolated.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R10 small focused tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R10_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R10_PRODUCTION_EDIT=NONE'
    } else {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py `
            phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py `
            phase173_r4_r15r7_source_first_abstract_certificate/tests/test_integration.py `
            phase173_r4_r11_zero_public_connection/tests/test_route.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R10 repository regression tests failed' }
        Write-Output 'PHASE173_R4_R15R10_FOCUSED_PYTEST=PASS'
        python -m phase173_r4_r15r10_common_route_audit.audit `
            --root "$RepoRoot" `
            --output (Join-Path $PSScriptRoot 'regression_report.json')
        if ($LASTEXITCODE -ne 0) { throw 'R15R10 public Web audit failed' }
        Write-Output 'PHASE173_R4_R15R10_PHASE_COMPLETED=False'
        Write-Output 'PHASE173_R4_R15R10_PRODUCTION_EDIT=NONE'
    }
} finally {
    Pop-Location
}
```
