# R15R14 — 新規実装・テストコード全文

`patches.py` は既存コードの anchor を完全一致で検査する。`install.py` は GitHub HEAD と Git blob を確認してから二つの既存ファイルを変更する。`run.ps1` は DryRun と本実行を提供する。

## patches.py

```python
"""R15R14 minimal, source-guarded presentation changes.

There is no generator- or dimension-specific rendering branch. The public
Web model continues to own proof status, Goal collection, and source evidence.
"""
from __future__ import annotations


def patch_common(source: str) -> str:
    """Reuse the existing group Relation renderer for typed cyclic pending goals."""
    anchor = "  public_group_latex = (\n"
    replacement = """  from expression import Expression
  from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
  from phase165_r12_r2_quotient_rules import CyclicStructureStatement
  from proof import Relation, RelationType

  if (
    isinstance(statement, CyclicStructureStatement)
    and isinstance(statement.group, TodaPrimaryGroup)
    and isinstance(statement.generator, Expression)
    and (
      statement.order is None
      or (type(statement.order) is int and statement.order >= 1)
    )
  ):
    structure = (
      FreeCyclicGroup(statement.generator)
      if statement.order is None
      else FiniteCyclicGroup(statement.order, statement.generator)
    )
    try:
      cyclic_latex = render_toda_public_group_relation_latex(
        Relation(
          lhs=statement.group,
          rhs=structure,
          relation_type=RelationType.EQUALITY,
        )
      )
    except (TypeError, ValueError):
      cyclic_latex = None
    if cyclic_latex is not None:
      return cyclic_latex, None

""" + anchor
    if source.count(anchor) != 1 or '  from phase165_r12_r2_quotient_rules import CyclicStructureStatement\n' in source:
        raise ValueError('Common typed renderer anchor changed or patch already applied')
    return source.replace(anchor, replacement, 1)


def patch_layout(source: str) -> str:
    """Keep evidence text untouched; project diagnostics in the Web display only."""
    anchor = 'def canonicalize_proof_layout(markdown: str) -> str:\n'
    helper = """def _public_search_diagnostic_line(line: str) -> str:
    \"\"\"Present a recorded diagnostic without exposing a Python object repr.

    This only changes the public display. The original diagnostic remains in
    ProofNarrativeModel and PartialProofResult for inspection and auditing.
    \"\"\"
    if not line.startswith("- "):
        return line
    message = line[2:].strip()
    prefix = "expected a verified registered derivation for "
    if message.startswith(prefix):
        before, separator, count = message.rpartition(", found ")
        if separator and before.startswith(prefix) and count.isdecimal():
            return (
                "- 登録済みの前提から証明目標を導く検証済みの推論が見つかりませんでした"
                f"（導出候補 {count} 件）。"
            )
    if any(token in message for token in (
        "Relation(", "TodaPrimaryGroup(", "HomotopyElement(",
        "GeneratorSymbol(",
    )):
        return "- 型付き証明目標の内部診断があります。詳細は監査ログを参照してください。"
    return line


""" + anchor
    old = """    normalized = [*prelude, "## 使用する結果", "", *reference_body,
                  "", "---", "", *proof_body]
    result = "\\n".join(normalized)
"""
    new = """    normalized = [*prelude, "## 使用する結果", "", *reference_body,
                  "", "---", "", *proof_body]
    in_search_diagnostics = False
    for index, line in enumerate(normalized):
        if line.startswith(("## ", "### ")):
            in_search_diagnostics = line.strip() == "## 探索診断"
        elif in_search_diagnostics and line.startswith("- "):
            normalized[index] = _public_search_diagnostic_line(line)
    result = "\\n".join(normalized)
"""
    if source.count(anchor) != 1 or source.count(old) != 1 or 'def _public_search_diagnostic_line' in source:
        raise ValueError('Existing common layout contract anchor changed or patch already applied')
    return source.replace(anchor, helper, 1).replace(old,new,1)

```

## install.py

```python
"""Guarded apply/rollback. Source files are never downloaded or rewritten blindly."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

from .patches import patch_common, patch_layout


REVIEWED_HEAD = "9729d3ee51e93f26cf6b31a3880cb1a92a552f2c"
REVIEWED_BLOBS = {
    "web_group_proof_common.py": "045d2ae677c0e62c243270e760c786ce61224c59",
    "phase173_r4_r15r13_unified_presentation/layout.py":
        "809effb7fcb70361e5580d9716d4aa143685f275",
}
TRANSFORMERS = {
    "web_group_proof_common.py": patch_common,
    "phase173_r4_r15r13_unified_presentation/layout.py": patch_layout,
}
ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
STATE = PACKAGE / "installed_state.json"
BACKUP = PACKAGE / "backups"


def git(*args: str) -> str:
    process = subprocess.run(
        ("git", *args), cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True, check=False,
    )
    if process.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + ": " + process.stderr[:500])
    return process.stdout.strip()


def original_encoding(data: bytes) -> tuple[str, str]:
    """Reject mixed EOL, preserving exact original newline conventions."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM source requires review")
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n")
    if data.count(b"\r") != crlf or (crlf and crlf != lf):
        raise ValueError("Mixed EOL source requires review")
    return data.decode("utf-8"), "\r\n" if crlf else "\n"


def transformed_bytes(path: Path, transformer) -> bytes:
    raw = path.read_bytes()
    decoded, eol = original_encoding(raw)
    normalized = decoded.replace("\r\n", "\n")
    modified = transformer(normalized)
    return modified.replace("\n", eol).encode("utf-8")


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def check_checkout() -> None:
    root = Path(git("rev-parse", "--show-toplevel")).resolve()
    if root != ROOT.resolve():
        raise RuntimeError("Repository root does not match package parent")
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    print("R15R14_BRANCH=" + branch, flush=True)
    print("R15R14_LOCAL_HEAD=" + head, flush=True)
    print("R15R14_REMOTE_HEAD=" + remote, flush=True)
    if branch != "develop" or head != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Develop HEAD moved; review changes before installation")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")


def prepare_changes() -> dict[str, tuple[bytes, bytes]]:
    """Require exact reviewed source Git blobs and a clean tracked tree."""
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Tracked worktree changes require review")
    changes = {}
    for name, transformer in TRANSFORMERS.items():
        file = ROOT / name
        if not file.is_file():
            raise FileNotFoundError(name)
        reviewed = git("rev-parse", "HEAD:" + name)
        local = git("hash-object", "--path=" + name, "--", name)
        if reviewed != REVIEWED_BLOBS[name] or local != REVIEWED_BLOBS[name]:
            raise RuntimeError("Unreviewed source contents: " + name)
        before = file.read_bytes()
        after = transformed_bytes(file, transformer)
        if after == before:
            raise RuntimeError("Patch did not change: " + name)
        changes[name] = before, after
    return changes


def verify_installed() -> bool:
    if not STATE.is_file():
        return False
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state.get("reviewed_head") != REVIEWED_HEAD:
        raise RuntimeError("Installed state does not match reviewed HEAD")
    if sorted(state.get("modified", {})) != sorted(TRANSFORMERS):
        raise RuntimeError("Installed state is incomplete")
    for name, hash_value in state["modified"].items():
        if digest((ROOT / name).read_bytes()) != hash_value:
            raise RuntimeError("Previously installed source was changed: " + name)
        if not (BACKUP / name).is_file():
            raise RuntimeError("Missing backup: " + name)
    remaining_changes = set(git("diff", "--name-only").splitlines())
    if remaining_changes != set(TRANSFORMERS):
        raise RuntimeError("Unreviewed worktree modifications after installation")
    print("R15R14_ALREADY_INSTALLED=True", flush=True)
    return True


def apply(changes: dict[str, tuple[bytes, bytes]]) -> None:
    if STATE.exists():
        raise RuntimeError("Existing install state must be reviewed before install")
    for name, (before, after) in changes.items():
        saved = BACKUP / name
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(before)
    replaced = []
    try:
        for name, (before, after) in changes.items():
            target = ROOT / name
            temporary = target.with_name(target.name + ".r15r14-new")
            temporary.write_bytes(after)
            os.replace(temporary, target)
            replaced.append(name)
        state = {
            "reviewed_head": REVIEWED_HEAD,
            "modified": {name: digest(after) for name, (before, after) in changes.items()},
            "backups": {name: digest(before) for name, (before, after) in changes.items()},
            "proof_search_changed": False,
            "full_pytest_run": False,
        }
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        for name in replaced:
            (ROOT / name).write_bytes((BACKUP / name).read_bytes())
        raise


def restore() -> None:
    check_checkout()
    if not verify_installed():
        raise RuntimeError("No verified install to restore")
    record = json.loads(STATE.read_text(encoding="utf-8"))
    for name, expected in record["backups"].items():
        saved = (BACKUP / name).read_bytes()
        if digest(saved) != expected:
            raise RuntimeError("Backup integrity failure: " + name)
    for name in TRANSFORMERS:
        (ROOT / name).write_bytes((BACKUP / name).read_bytes())
    STATE.unlink()
    print("R15R14_RESTORED=PASS", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--install", action="store_true")
    mode.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    try:
        if args.restore:
            restore()
            return 0
        check_checkout()
        if verify_installed():
            print("R15R14_SOURCE_GUARD=PASS", flush=True)
            print("R15R14_DRY_RUN=PASS" if args.dry_run else "R15R14_INSTALLED=True", flush=True)
            return 0
        changes = prepare_changes()
        print("R15R14_SOURCE_GUARD=PASS", flush=True)
        print("R15R14_SOURCE_GUARD_FILES=" + str(len(changes)), flush=True)
        if args.dry_run:
            print("R15R14_DRY_RUN=PASS", flush=True)
            print("R15R14_PRODUCTION_EDIT=NONE", flush=True)
        else:
            apply(changes)
            print("R15R14_INSTALLED=True", flush=True)
        return 0
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        print("R15R14_ERROR=" + type(exc).__name__ + ": " + str(exc), file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

```

## tests/test_contract.py

```python
"""Pure common formatting tests; no proof search or inferred evidence."""
from __future__ import annotations

from pathlib import Path

from phase173_r4_r15r14_common_partial_presentation.patches import patch_layout


def load_reviewed_layout_contract():
    """Test the exact proposed layout without modifying production files in DryRun."""
    root = Path(__file__).resolve().parents[2]
    source_file = root / "phase173_r4_r15r13_unified_presentation" / "layout.py"
    source = source_file.read_text(encoding="utf-8")
    if "def _public_search_diagnostic_line" not in source:
        source = patch_layout(source)
    environment = {"__name__": "r15r14_layout_contract_preview"}
    exec(compile(source, str(source_file), "exec"), environment)
    return (environment["canonicalize_proof_layout"],
            environment["_public_search_diagnostic_line"])


canonicalize_proof_layout, _public_search_diagnostic_line = load_reviewed_layout_contract()


def test_registered_derivation_diagnostic_becomes_readable() -> None:
    diagnostic = (
        "expected a verified registered derivation for "
        "Relation(lhs=TodaPrimaryGroup(group_dimension=12, sphere_dimension=4)), found 0"
    )
    assert _public_search_diagnostic_line("- " + diagnostic) == (
        "- 登録済みの前提から証明目標を導く検証済みの推論が見つかりませんでした"
        "（導出候補 0 件）。"
    )


def test_non_diagnostic_text_is_preserved() -> None:
    untouched = "- Relation(lhs=TodaPrimaryGroup(group_dimension=12))"
    assert canonicalize_proof_layout(
        "使用する結果\n\n証明\n\n## 未解決 Goal\n\n" + untouched + "\n"
    ).endswith(untouched + "\n")


def test_public_diagnostics_do_not_affect_goals_or_references() -> None:
    raw = (
        "## 使用する結果\n\n**[R1] Lemma 5.4.**\n\n"
        "---\n\n## 証明\n\n## 未解決 Goal\n\n"
        "- $\\pi_{12}^{4}=\\mathbb{Z}/2\\{\\varepsilon_{4}\\}$\n\n"
        "## 探索診断\n\n"
        "- expected a verified registered derivation for Relation(lhs=some), found 0\n\n"
        "## 証明済みの抽象群構造\n\n$\\pi_{12}^{4}\\cong\\mathbb{Z}/2$.\n"
    )
    shown = canonicalize_proof_layout(raw)
    assert shown.count("[R1]") == 1
    assert r"- $\pi_{12}^{4}=\mathbb{Z}/2\{\varepsilon_{4}\}$" in shown
    assert r"$\pi_{12}^{4}\cong\mathbb{Z}/2$" in shown
    assert "## 探索診断" in shown
    assert "Relation(" not in shown
    assert "導出候補 0 件" in shown


def test_unrecognized_diagnostic_keeps_plain_text() -> None:
    line = "- 証明探索の範囲内に証明規則がありません"
    assert _public_search_diagnostic_line(line) == line


def test_unrecognized_object_repr_is_not_exposed_in_diagnostics() -> None:
    line = "- Relation(lhs=TodaPrimaryGroup(group_dimension=12))"
    shown = _public_search_diagnostic_line(line)
    assert "Relation(" not in shown
    assert "監査ログ" in shown


def test_no_citation_section_is_left_untouched() -> None:
    source = "## 探索診断\n\n- Relation(foo)\n"
    assert canonicalize_proof_layout(source) == source

```

## tests/test_integration.py

```python
"""Focused real typed partial and complete view regression tests."""
from __future__ import annotations

import pytest

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _group_proof_statement_latex


@pytest.mark.parametrize("k", (8, 15))
def test_typed_cyclic_open_goal_reuses_registered_latex(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None and isinstance(goal.rhs, FiniteCyclicGroup)
    typed = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    shown, fallback = _group_proof_statement_latex(typed)
    expected, expected_fallback = _group_proof_statement_latex(goal)
    assert fallback is None and expected_fallback is None
    assert shown == expected
    assert shown.startswith(r"\pi_{")
    assert r"\mathbb{Z}/2\{" in shown


def test_infinite_cyclic_statement_reuses_general_group_renderer() -> None:
    goal = exact_prior_database_result(4, 3)
    assert goal is not None
    free = next(component for component in goal.rhs.summands
                if isinstance(component, FreeCyclicGroup))
    typed = CyclicStructureStatement(goal.lhs, free.generator, None)
    result, fallback = _group_proof_statement_latex(typed)
    assert fallback is None
    assert r"\mathbb{Z}\{" in result
    assert r"\pi_{7}^{4}" in result


@pytest.mark.parametrize("k", (8, 15))
def test_real_partial_web_does_not_leak_internal_diagnostics(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None and len(result.open_goals) == 3
    assert result.abstract_structure is not None
    assert any("Relation(" in item for item in result.diagnostics)
    model = build_proof_narrative_model(result)
    # Preserve the internal model for audits; only the public view is projected.
    raw = render_model_backed_narrative_markdown(result, model)
    assert "expected a verified registered derivation" in raw
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-partial-proof" and view.partial_result
    assert sum(line.kind == "heading" and line.prefix == "未解決 Goal"
               for line in view.rendered_lines) == 1
    assert sum(line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
               for line in view.rendered_lines) == 1
    rendered = "\n".join(
        segment.value for line in view.rendered_lines for segment in line.segments
    )
    assert "CyclicStructureStatement（数式表示未対応）" not in rendered
    assert "Relation(lhs=" not in rendered
    assert "導出候補 0 件" in rendered
    assert r"\mathbb{Z}/2\{" in rendered
    assert r"\pi_{" in rendered


def test_multi_summand_pending_diagnostic_is_public_prose() -> None:
    goal = exact_prior_database_result(4, 9)
    result = search_group_from_registered_goal(n=4, k=9, goal=goal)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None and len(result.open_goals) == 2
    assert result.abstract_structure is not None
    view = build_standard_web_group_proof_view(
        n=4, k=9, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-partial-proof" and view.partial_result
    diagnostic_lines = []
    in_diagnostics = False
    for line in view.rendered_lines:
        if line.kind == "heading":
            in_diagnostics = line.prefix == "探索診断"
        elif in_diagnostics:
            diagnostic_lines.extend(segment.value for segment in line.segments)
    diagnostic = "\n".join(diagnostic_lines)
    assert "導出候補 0 件" in diagnostic
    assert "Relation(" not in diagnostic


def test_named_complete_proof_is_unchanged() -> None:
    view = build_standard_web_group_proof_view(
        n=4, k=4, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof" and not view.partial_result
    assert view.rendered_lines
    assert any("[R" in segment.value for line in view.rendered_lines
               for segment in line.segments)
    assert not any(line.kind == "heading" and line.prefix == "未解決 Goal"
                   for line in view.rendered_lines)

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R14 GitHub fetch failed' }

    python -m phase173_r4_r15r14_common_partial_presentation.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R14 source guard failed' }

    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r14_common_partial_presentation/tests/test_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R14 pure contract tests failed' }

    if ($DryRun) {
        Write-Output 'R15R14_DRY_RUN=PASS'
        Write-Output 'R15R14_PRODUCTION_CODE_EDIT=NONE'
        Write-Output 'R15R14_PHASE_COMPLETED=False'
        exit 0
    }

    python -m phase173_r4_r15r14_common_partial_presentation.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R14 installation failed' }

    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r14_common_partial_presentation/tests/test_contract.py `
            phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
            phase173_r4_r15r13_unified_presentation/tests/test_contract.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r12_reference_correction/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R14 focused pytest failed' }
        Write-Output 'R15R14_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R14_FULL_PYTEST_RUN=False'
        Write-Output 'R15R14_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r14_common_partial_presentation.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R14 rollback requires inspection' }
        throw
    }
} finally {
    Pop-Location
}

```

