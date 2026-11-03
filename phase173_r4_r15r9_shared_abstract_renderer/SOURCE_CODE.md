# Phase 173 R4-R15R9 — 変更コード・テスト全文

## 対象

既存 `phase165_r52_r3_web_adapter.py` の `build_partial_web_group_proof_view` 関数全体のみ変更。
新規 `phase173_r4_r15r9_shared_abstract_renderer/` は `projection.py` などの実装・監査・テストを新設。
既存トップレベル import は変更しない。既存 API、数学的推論規則および完成判定に変更はない。

## 既存モジュールの import 全文・変更関数全文

# R4-R15R9 — 変更後の全 import・変更関数全文

変更ファイル：`phase165_r52_r3_web_adapter.py`。トップレベル import は変更なし。

## 完全な import 部分

```python
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
```

## `build_partial_web_group_proof_view` 関数全体

```python
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
        from phase173_r4_r15r9_shared_abstract_renderer.projection import (
            render_certified_abstract_section,
        )
        abstract_markdown = render_certified_abstract_section(result)
        if abstract_markdown:
            markdown = markdown.rstrip() + "\n\n" + abstract_markdown + "\n"
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


## 既存モジュール全体

`reviewed_source/phase165_r52_r3_web_adapter_PROPOSED.py.txt` に省略なしで格納。

## 新規 `projection.py` 全文

```python
"""Format an existing abstract certificate; do not infer mathematical facts.

The common Web adapter invokes this function after its usual narrative has
been rendered. No n/k special case and no alternate Narrative pipeline exists.
"""
from __future__ import annotations

from phase165_r52_partial_proof import (
    CertifiedAbstractStructure,
    PartialProofResult,
    ProofSearchStatus,
)


def abstract_invariants_latex(invariants: tuple[tuple[str, int], ...]) -> str:
    """Format *already certified* invariant summands without generator names."""
    if not isinstance(invariants, tuple):
        raise TypeError("abstract invariant summands must be a tuple")
    counts: dict[tuple[str, int], int] = {}
    for item in invariants:
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError("abstract invariant summand must be a pair")
        kind, order = item
        if not (
            (kind == "free" and type(order) is int and order == 0)
            or (kind == "finite" and type(order) is int and order >= 2)
        ):
            raise ValueError("unsupported abstract invariant summand")
        counts[item] = counts.get(item, 0) + 1
    if not counts:
        return "0"
    expressions: list[str] = []
    for (kind, order), count in sorted(counts.items()):
        atom = r"\mathbb{Z}" if kind == "free" else rf"\mathbb{{Z}}/{order}"
        if count > 1:
            atom = rf"\left({atom}\right)^{{{count}}}"
        expressions.append(atom)
    return r" \oplus ".join(expressions)


def render_certified_abstract_section(result: PartialProofResult) -> str:
    """Return one source-derived abstract-only section, or empty Markdown.

    The current named Goal, public COMPLETE flag, references and open goals
    remain entirely owned by the canonical search and Narrative renderer.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("expected canonical PartialProofResult")
    structure = result.abstract_structure
    if structure is None:
        return ""
    if (
        not isinstance(structure, CertifiedAbstractStructure)
        or structure.group != result.target
        or result.status not in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        or result.conclusion is not None
    ):
        raise ValueError("unverified abstract result cannot be presented as a certificate")
    target = result.target
    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:
        raise ValueError("abstract result has nonconcrete group dimensions")
    invariant_latex = abstract_invariants_latex(structure.invariant_summands)
    target_latex = rf"\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"
    return (
        "## 証明済みの抽象群構造\n\n"
        + rf"${target_latex} \cong {invariant_latex}$."
        + "\n\n"
        + "これは出典検査済みの抽象群 ProofStep による結論であり、"
        + "登録済みの先行 DB 群を前提とする。"
        + "記名生成元の対応は未証明であり、上記の未解決 Goal と探索状態は変わらない。"
    )

```

## 新規 `patch_source.py` 全文

```python
"""Guarded one-function edit to the canonical shared Web adapter."""
from __future__ import annotations

import ast
from pathlib import Path


ANCHOR = '''        rendered_lines = _build_group_proof_rendered_lines(markdown)
'''
REPLACEMENT = '''        from phase173_r4_r15r9_shared_abstract_renderer.projection import (
            render_certified_abstract_section,
        )
        abstract_markdown = render_certified_abstract_section(result)
        if abstract_markdown:
            markdown = markdown.rstrip() + "\\n\\n" + abstract_markdown + "\\n"
        rendered_lines = _build_group_proof_rendered_lines(markdown)
'''
BASELINE_BLOB = "b427ca5a1c1d0eb213f9a4c76fa559b849f8987c"


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def transform(source: bytes) -> bytes:
    """Replace one reviewed adapter statement, retaining all other functions."""
    eol = "\r\n" if b"\r\n" in source else "\n"
    if b"\r\n" in source and source.count(b"\r\n") != source.count(b"\n"):
        raise RuntimeError("Mixed line endings require review")
    original = source.decode("utf-8-sig").replace("\r\n", "\n")
    if original.count(ANCHOR) != 1 or "render_certified_abstract_section" in original:
        raise RuntimeError("Unreviewed or already patched shared Web adapter")
    tree = ast.parse(original)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1 or functions[0].name != "build_partial_web_group_proof_view":
        raise RuntimeError("Unexpected shared Web adapter module structure")
    updated = original.replace(ANCHOR, REPLACEMENT)
    ast.parse(updated)
    return updated.replace("\n", eol).encode("utf-8")


def complete_changed_units(baseline: bytes) -> str:
    """Output the entire revised function and full import section for review."""
    content = transform(baseline).decode("utf-8").replace("\r\n", "\n")
    tree = ast.parse(content)
    imports = []
    function = None
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append("".join(content.splitlines(keepends=True)[node.lineno-1:node.end_lineno]))
        elif isinstance(node, ast.FunctionDef) and node.name == "build_partial_web_group_proof_view":
            function = "".join(content.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
    if function is None:
        raise RuntimeError("Expected one full modified function")
    return (
        "# R4-R15R9 — 変更後の全 import・変更関数全文\n\n"
        "変更ファイル：`phase165_r52_r3_web_adapter.py`。"
        "トップレベル import は変更なし。\n\n"
        "## 完全な import 部分\n\n```python\n"
        + "\n".join(imports)
        + "```\n\n## `build_partial_web_group_proof_view` 関数全体\n\n```python\n"
        + function + "```\n"
    )


def write_complete_sources(baseline: bytes, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "phase165_r52_r3_web_adapter_FULL.py.txt").write_bytes(transform(baseline))
    (directory / "FULL_CHANGED_UNITS.md").write_text(
        complete_changed_units(baseline), encoding="utf-8",
    )

```

## 新規 `install.py` 全文

```python
"""Install one reviewed shared Web-adapter projection with full rollback."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from phase173_r4_r15r9_shared_abstract_renderer.patch_source import (
    BASELINE_BLOB,
    normalized,
    transform,
    write_complete_sources,
)


REVIEWED_HEAD = "e3fa8cf71777b1bf5bb431ec06cd2147bce69086"
TARGET = "phase165_r52_r3_web_adapter.py"
DEPENDENCY_BLOBS = {
    "phase168_r3_5_model_renderer.py": "6bfd5e992f6c9ee9441920e10e63e0db4bece289",
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase165_r52_partial_proof.py": "0af6b459ed5a136a8e30a9e349ccf9fa601d448b",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
}
ALLOWED_CHANGED_PREFIXES = (
    "phase173_r4_r15r8_public_abstract_sidecar/",
)
ALLOWED_CHANGED_PATHS = frozenset({
    ".pytest_cache/v/cache/nodeids",
    "phase165_r52_partial_proof.py",
    "phase165_r55_nk_only_goal.py",
})


def _run(root: Path, *args: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ("git", *args), cwd=root, check=False, capture_output=True,
        text=not binary, encoding=None if binary else "utf-8",
        errors=None if binary else "replace",
    )
    if result.returncode:
        raise RuntimeError("Git command failed: " + " ".join(args)
                           + " " + str(result.stderr)[:250])
    return result.stdout if binary else result.stdout.strip()


def sha(data: bytes) -> str:
    return hashlib.sha256(normalized(data)).hexdigest()


def preflight(root: Path) -> tuple[bytes, bytes, str]:
    """Guard committed R15R8 dependencies and unchanged shared renderer."""
    root = root.resolve()
    if Path(_run(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Wrong repository root")
    if _run(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = _run(root, "rev-parse", "HEAD")
    remote = _run(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local and origin/develop HEAD disagree")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, check=False, capture_output=True,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed Git HEAD lineage")
    changed = _run(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()
    if any(path not in ALLOWED_CHANGED_PATHS and not path.startswith(ALLOWED_CHANGED_PREFIXES)
           for path in changed):
        raise RuntimeError("Unreviewed committed change after R15R8: " + repr(changed))
    if _run(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged source changes require review")
    dirty = _run(root, "diff", "--name-only").splitlines()
    if any(path not in {TARGET, ".pytest_cache/v/cache/nodeids"} for path in dirty):
        raise RuntimeError("Unreviewed local tracked changes: " + repr(dirty))
    for path, blob in DEPENDENCY_BLOBS.items():
        if _run(root, "rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("Unreviewed dependency Git blob: " + path)
        if _run(root, "hash-object", "--", path) != blob:
            raise RuntimeError("Dependency file has local edits: " + path)
    if _run(root, "rev-parse", "HEAD:" + TARGET) != BASELINE_BLOB:
        raise RuntimeError("Shared Web adapter Git baseline was not reviewed")
    baseline = _run(root, "show", "HEAD:" + TARGET, binary=True)
    candidate = transform(baseline)
    existing = (root / TARGET).read_bytes()
    if normalized(existing) == normalized(baseline):
        state = "BASELINE"
    elif normalized(existing) == normalized(candidate):
        state = "PATCHED"
    else:
        raise RuntimeError("Unreviewed shared Web adapter content")
    package = Path(__file__).resolve().parent
    reviewed_source = package / "reviewed_source" / "phase165_r52_r3_web_adapter_BASELINE.py.txt"
    if not reviewed_source.is_file() or normalized(reviewed_source.read_bytes()) != normalized(baseline):
        raise RuntimeError("Packaged reviewed full adapter differs from Git baseline")
    print("PHASE173_R4_R15R9_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R9_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R9_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R9_INSTALL_STATE=" + state, flush=True)
    return baseline, candidate, state


def install(root: Path, *, dry_run: bool) -> None:
    baseline, candidate, state = preflight(root)
    package = Path(__file__).resolve().parent
    write_complete_sources(baseline, package / "reviewed_full_source")
    if dry_run:
        print("PHASE173_R4_R15R9_DRY_RUN=PASS", flush=True)
        print("PHASE173_R4_R15R9_PRODUCTION_EDIT=NONE", flush=True)
        return
    if state == "PATCHED":
        print("PHASE173_R4_R15R9_ALREADY_INSTALLED=True", flush=True)
        return
    backup = package / "reviewed_full_source" / "original_adapter.py.bak"
    original_bytes = (root / TARGET).read_bytes()
    backup.write_bytes(original_bytes)
    # Preserve a clean CRLF checkout rather than normalizing unrelated lines.
    candidate_for_worktree = transform(original_bytes)
    destination = root / TARGET
    temporary = destination.with_suffix(destination.suffix + ".r15r9_tmp")
    try:
        temporary.write_bytes(candidate_for_worktree)
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        destination.write_bytes(baseline)
        raise
    (package / "installed_state.json").write_text(json.dumps({
        "phase": "173-R4-R15R9",
        "original_sha256": sha(baseline),
        "patched_sha256": sha(candidate),
        "complete_named_proof_promoted": False,
        "public_web_partial_status_preserved": True,
    }, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R15R9_PATCHED=" + TARGET, flush=True)


def restore(root: Path) -> None:
    baseline, candidate, state = preflight(root)
    if state == "BASELINE":
        print("PHASE173_R4_R15R9_ROLLBACK=ALREADY_BASELINE", flush=True)
        return
    package = Path(__file__).resolve().parent
    backup = package / "reviewed_full_source" / "original_adapter.py.bak"
    if not backup.is_file() or normalized(backup.read_bytes()) != normalized(baseline):
        raise RuntimeError("Guarded rollback backup absent or incorrect")
    (root / TARGET).write_bytes(backup.read_bytes())
    print("PHASE173_R4_R15R9_ROLLBACK=PASS", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.restore:
        restore(root)
    else:
        install(root, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## 新規 `audit.py` 全文

```python
"""Check the canonical Web Group proof projection without completing named goals."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.install import preflight
from web_group_proof import build_standard_web_group_proof_view


def inspect_public(k: int) -> dict[str, object]:
    """Inspect both canonical search and model-backed shared Web projection."""
    goal = exact_prior_database_result(4, k)
    if goal is None:
        raise RuntimeError("Expected exact registered group target")
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    has_abstract = result.abstract_structure is not None
    headings = tuple(line.prefix for line in view.rendered_lines if line.kind == "heading")
    theorem_math = tuple(line.statement_latex or "" for line in view.rendered_lines)
    printed = (
        "証明済みの抽象群構造" in headings
        and any(rf"\pi_{{{k+4}}}^{{4}}" in latex and r"\cong" in latex
                for latex in theorem_math)
    )
    named_pending = bool(
        result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        and result.conclusion is None and result.open_goals
        and view.key == "generic-partial-proof" and view.partial_result
    )
    return {
        "k": k,
        "group": f"pi_{k+4}^4",
        "abstract_attached": has_abstract,
        "abstract_rendered": printed,
        "named_search_status": result.status.value,
        "named_open_goals": len(result.open_goals),
        "web_key": view.key,
        "web_partial": view.partial_result,
        "public_named_complete": not named_pending,
        "passed": has_abstract and printed and named_pending,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    preflight(args.root)
    rows = [inspect_public(k) for k in (8, 31)]
    if not all(row["passed"] for row in rows):
        raise RuntimeError("Canonical Web abstract evidence not rendered or named status changed")
    report = {
        "phase": "173-R4-R15R9",
        "mode": "COMMON_WEB_ABSTRACT_EVIDENCE_PROJECTION",
        "observations": rows,
        "named_complete_promoted": False,
        "specialized_narrative_added": False,
        "full_pytest_performed": False,
        "passed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    for row in rows:
        print("PHASE173_R4_R15R9_K=" + str(row["k"])
              + " ABSTRACT_RENDERED=" + str(row["abstract_rendered"])
              + " NAMED_PENDING=" + str(not row["public_named_complete"]), flush=True)
    print("PHASE173_R4_R15R9_K31_PUBLIC_ABSTRACT_RENDERED=PASS", flush=True)
    print("PHASE173_R4_R15R9_WEB_NAMED_COMPLETE=False", flush=True)
    print("PHASE173_R4_R15R9_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R9_AUDIT=PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## 新規 `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R9 git fetch failed' }
    python -m phase173_r4_r15r9_shared_abstract_renderer.install --root "$RepoRoot" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R9 Source Guard failed' }
    python -m pytest -q -p no:cacheprovider phase173_r4_r15r9_shared_abstract_renderer/tests/test_static.py `
        phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection_isolated.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R9 static tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R9_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R9_PRODUCTION_EDIT=NONE'
    } else {
        python -m phase173_r4_r15r9_shared_abstract_renderer.install --root "$RepoRoot"
        if ($LASTEXITCODE -ne 0) { throw 'R15R9 installation failed' }
        try {
            python -m pytest -q -p no:cacheprovider `
                phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py `
                phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py `
                phase173_r4_r15r7_source_first_abstract_certificate/tests/test_integration.py `
                phase173_r4_r11_zero_public_connection/tests/test_route.py
            if ($LASTEXITCODE -ne 0) { throw 'R15R9 focused pytest failed' }
            Write-Output 'PHASE173_R4_R15R9_FOCUSED_PYTEST=PASS'
            python -m phase173_r4_r15r9_shared_abstract_renderer.audit --root "$RepoRoot" `
                --output (Join-Path $PSScriptRoot 'shared_abstract_web_report.json')
            if ($LASTEXITCODE -ne 0) { throw 'R15R9 Web audit failed' }
            Write-Output 'PHASE173_R4_R15R9_PHASE_COMPLETED=False'
        } catch {
            python -m phase173_r4_r15r9_shared_abstract_renderer.install --root "$RepoRoot" --restore
            throw
        }
    }
} finally {
    Pop-Location
}

```

## 新規 `tests/test_static.py` 全文

```python
"""Standalone AST and source-patch checks; no mathematical stubs for evidence."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r9_shared_abstract_renderer.patch_source import (
    BASELINE_BLOB,
    ANCHOR,
    normalized,
    complete_changed_units,
    transform,
)


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "reviewed_source" / "phase165_r52_r3_web_adapter_BASELINE.py.txt"


def test_source_matches_reviewed_git_blob() -> None:
    import subprocess
    result = subprocess.run(("git", "hash-object", str(BASE)),
                            check=True, capture_output=True, text=True)
    assert result.stdout.strip() == BASELINE_BLOB


def test_exactly_one_shared_adapter_hook() -> None:
    source = BASE.read_bytes()
    patched = transform(source)
    assert normalized(patched).count(b"render_certified_abstract_section(result)") == 1
    assert normalized(patched).count(b"_build_group_proof_rendered_lines(markdown)") == 1


def test_full_module_compiles() -> None:
    ast.parse(transform(BASE.read_bytes()).decode("utf-8"))


def test_full_changed_function_is_exported() -> None:
    text = complete_changed_units(BASE.read_bytes())
    assert "def build_partial_web_group_proof_view(" in text
    assert "render_certified_abstract_section(result)" in text
    assert "from phase165_r52_partial_proof import " in text
    assert "return WebGroupProofView(" in text
    assert "```" in text


def test_existing_complete_and_trace_paths_remain() -> None:
    updated = transform(BASE.read_bytes()).decode("utf-8")
    assert 'if mode == "trace":' in updated
    assert 'if result.status is ProofSearchStatus.COMPLETE:' in updated
    assert 'key=("generic-complete-proof" if result.status is ProofSearchStatus.COMPLETE else "generic-partial-proof")' in updated
    assert 'partial_result=(result.status is not ProofSearchStatus.COMPLETE)' in updated


def test_tampered_reviewed_anchor_fails_closed() -> None:
    original = BASE.read_bytes()
    with pytest.raises(RuntimeError, match="Unreviewed"):
        transform(original.replace(ANCHOR.encode(), b"        rendered_lines = ()\n"))


def test_already_patched_source_fails_closed() -> None:
    with pytest.raises(RuntimeError, match="Unreviewed"):
        transform(transform(BASE.read_bytes()))


def test_crlf_patch_preserves_line_endings() -> None:
    source = BASE.read_bytes().replace(b"\n", b"\r\n")
    patched = transform(source)
    assert b"\r\n" in patched
    assert patched.count(b"\r\n") == patched.count(b"\n")
    ast.parse(patched.decode("utf-8"))


def test_mixed_line_endings_fail_closed() -> None:
    mixed = BASE.read_bytes().replace(b"\n", b"\r\n", 1)
    with pytest.raises(RuntimeError, match="Mixed"):
        transform(mixed)


def test_projection_source_has_no_stem_branches() -> None:
    source = (ROOT / "projection.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "k == 31" not in source
    assert "n == 4" not in source
    assert "ProofSearchStatus.COMPLETE" not in source
    assert "public_search" not in source
    assert "GIVEN" not in source
    assert {node.name for node in tree.body if isinstance(node, ast.FunctionDef)} == {
        "abstract_invariants_latex", "render_certified_abstract_section",
    }

```

## 新規 `tests/test_projection_isolated.py` 全文

```python
"""Offline formatter validation with inert result stubs, not mathematical evidence."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from types import ModuleType

import pytest


@pytest.fixture
def projection(monkeypatch):
    module = ModuleType("phase165_r52_partial_proof")

    class ProofSearchStatus(Enum):
        PARTIAL = "partial"
        SEARCH_FAILED = "search_failed"
        COMPLETE = "complete"
        NOT_SEARCHED = "not_searched"

    @dataclass(frozen=True)
    class Target:
        group_dimension: int
        sphere_dimension: int

    @dataclass(frozen=True)
    class CertifiedAbstractStructure:
        group: object
        invariant_summands: tuple

    @dataclass(frozen=True)
    class PartialProofResult:
        target: Target
        status: ProofSearchStatus
        abstract_structure: object | None = None
        conclusion: object | None = None

    module.CertifiedAbstractStructure = CertifiedAbstractStructure
    module.PartialProofResult = PartialProofResult
    module.ProofSearchStatus = ProofSearchStatus
    monkeypatch.setitem(sys.modules, module.__name__, module)
    path = Path(__file__).resolve().parents[1] / "projection.py"
    spec = spec_from_file_location("phase173_r4_r15r9_isolated_projection", path)
    assert spec is not None and spec.loader is not None
    loaded = module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded, module, Target


def test_multiple_finite_summands(projection) -> None:
    render, _, _ = projection
    assert render.abstract_invariants_latex((("finite", 2),) * 8) == (
        r"\left(\mathbb{Z}/2\right)^{8}"
    )


def test_empty_invariants_render_zero(projection) -> None:
    render, _, _ = projection
    assert render.abstract_invariants_latex(()) == "0"


def test_mixed_free_and_finite_summands(projection) -> None:
    render, _, _ = projection
    assert render.abstract_invariants_latex(
        (("free", 0), ("finite", 4), ("free", 0))
    ) == r"\mathbb{Z}/4 \oplus \left(\mathbb{Z}\right)^{2}"


def test_wrong_finite_order_is_rejected(projection) -> None:
    render, _, _ = projection
    for data in ((("finite", 0),), (("finite", True),), (("free", 2),)):
        with pytest.raises(ValueError):
            render.abstract_invariants_latex(data)


def test_verified_sidecar_is_rendered_as_abstract_only(projection) -> None:
    render, m, Target = projection
    group = Target(35, 4)
    sidecar = m.CertifiedAbstractStructure(group, (("finite", 2),) * 8)
    pending = m.PartialProofResult(group, m.ProofSearchStatus.SEARCH_FAILED, sidecar)
    markdown = render.render_certified_abstract_section(pending)
    assert r"\pi_{35}^{4} \cong \left(\mathbb{Z}/2\right)^{8}" in markdown
    assert "証明済みの抽象群構造" in markdown
    assert "記名生成元の対応は未証明" in markdown


def test_unproved_result_has_no_extra_section(projection) -> None:
    render, m, Target = projection
    pending = m.PartialProofResult(Target(35, 4), m.ProofSearchStatus.SEARCH_FAILED)
    assert render.render_certified_abstract_section(pending) == ""


def test_forged_complete_result_is_rejected(projection) -> None:
    render, m, Target = projection
    target = Target(35, 4)
    sidecar = m.CertifiedAbstractStructure(target, (("finite", 2),) * 8)
    complete = m.PartialProofResult(target, m.ProofSearchStatus.COMPLETE, sidecar)
    with pytest.raises(ValueError, match="unverified"):
        render.render_certified_abstract_section(complete)


def test_wrong_abstract_target_is_rejected(projection) -> None:
    render, m, Target = projection
    sidecar = m.CertifiedAbstractStructure(Target(36, 4), (("finite", 2),) * 8)
    pending = m.PartialProofResult(Target(35, 4), m.ProofSearchStatus.PARTIAL, sidecar)
    with pytest.raises(ValueError, match="unverified"):
        render.render_certified_abstract_section(pending)

```

## 新規 `tests/test_projection.py` 全文

```python
"""Repository-dependent real source-first certificates and common Web projection."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import (
    CertifiedAbstractStructure,
    ProofSearchStatus,
    make_partial_proof_result,
)
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    abstract_invariants_latex,
    render_certified_abstract_section,
)
from proof import ProofRule


@pytest.mark.parametrize("raw, expected", (
    ((), "0"),
    ((("finite", 2),) * 8, r"\left(\mathbb{Z}/2\right)^{8}"),
    ((("free", 0),), r"\mathbb{Z}"),
    ((("free", 0),) * 2 + (("finite", 4),),
     r"\mathbb{Z}/4 \oplus \left(\mathbb{Z}\right)^{2}"),
))
def test_abstract_invariants_render_without_generator_names(raw, expected) -> None:
    assert abstract_invariants_latex(raw) == expected


@pytest.mark.parametrize("invalid", (
    (("finite", 1),),
    (("free", 2),),
    (("finite", True),),
    (("unknown", 4),),
    (("finite", 2, 3),),
))
def test_invalid_invariants_not_rendered(invalid) -> None:
    with pytest.raises(ValueError):
        abstract_invariants_latex(invalid)


@pytest.fixture(scope="module")
def proved_abstract_result():
    bridge = build_shared_typed_bridge()
    source = search_source_first_abstract(k=31, bridge=bridge)
    assert source is not None
    assert source.root_step.rule is ProofRule.INFERENCE
    goal = exact_prior_database_result(4, 31)
    assert source.proof_target == goal
    abstract = CertifiedAbstractStructure(
        group=source.conclusion.group,
        invariant_summands=source.conclusion.invariant_summands,
        proof_step=source.root_step,
    )
    result = make_partial_proof_result(
        n=4, k=31, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(goal,), diagnostics=("記名生成元の証明は未解決",),
    )
    from dataclasses import replace
    return replace(result, abstract_structure=abstract)


def test_source_verified_abstract_markdown_is_explicitly_partial(proved_abstract_result) -> None:
    section = render_certified_abstract_section(proved_abstract_result)
    assert "証明済みの抽象群構造" in section
    assert r"\pi_{35}^{4} \cong \left(\mathbb{Z}/2\right)^{8}" in section
    assert "記名生成元の対応は未証明" in section
    assert proved_abstract_result.status is ProofSearchStatus.SEARCH_FAILED
    assert proved_abstract_result.conclusion is None
    assert len(proved_abstract_result.open_goals) == 1


def test_shared_model_backed_web_displays_abstract_and_keeps_named_pending(proved_abstract_result) -> None:
    model = build_proof_narrative_model(proved_abstract_result)
    view = build_partial_web_group_proof_view(
        proved_abstract_result, mode="narrative", narrative_model=model,
    )
    assert view.key == "generic-partial-proof"
    assert view.partial_result
    assert any(line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
               for line in view.rendered_lines)
    assert any(r"\pi_{35}^{4}" in (line.statement_latex or "")
               and r"\cong" in (line.statement_latex or "")
               for line in view.rendered_lines)
    assert any(line.kind == "heading" and line.prefix == "未解決 Goal"
               for line in view.rendered_lines)


def test_shared_fallback_web_uses_same_abstract_projection(proved_abstract_result) -> None:
    view = build_partial_web_group_proof_view(
        proved_abstract_result, mode="outline",
    )
    assert view.partial_result
    assert sum(line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
               for line in view.rendered_lines) == 1


def test_trace_route_remains_without_added_narrative(proved_abstract_result) -> None:
    view = build_partial_web_group_proof_view(proved_abstract_result, mode="trace")
    assert view.key == "generic-partial-proof"
    assert view.partial_result
    assert view.rendered_lines == ()


def test_no_abstract_sidecar_preserves_original_partial_text(proved_abstract_result) -> None:
    from dataclasses import replace
    bare = replace(proved_abstract_result, abstract_structure=None)
    assert render_certified_abstract_section(bare) == ""
    view = build_partial_web_group_proof_view(
        bare, mode="narrative", narrative_model=build_proof_narrative_model(bare),
    )
    assert view.key == "generic-partial-proof"
    assert not any(line.prefix == "証明済みの抽象群構造"
                   for line in view.rendered_lines)

```
