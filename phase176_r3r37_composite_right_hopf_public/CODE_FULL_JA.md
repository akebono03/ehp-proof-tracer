# Phase 176 R3R37 — コード全文

既存の `phase165_r52_r9_shared_math.py` は `shared_expansion_provider()` の内部だけを変更する。既存 import の変更はない。

## 既存関数の変更

変更後の `shared_expansion_provider()` **全体**は、インストーラーが作業ツリーの正確な現行コードから生成し、`%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r37_composite_right_hopf_public\CHANGED_FUNCTION_FULL_JA.md` に出力する。これは GitHub の過去版を一括上書きしないための仕様である。

追加位置は R3R35 の `options.extend(expand_composite_suspension_equality(goal))` 直後。追加する5行：

```python
        # Phase 176 R3R37: source-screened composite-right Hopf candidates.
        from phase176_r3r36_composite_right_hopf_isolated.source import (
            expand_cited_composite_right_hopf,
        )
        options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))
```

## 新規 `installer.py` — 全文（import、関数、テストを含む）

```python
"""Phase 176 R3R37: fail-closed additive hookup for composite right-Hopf candidates.

No mathematics, citation, or root proof is installed by this script.  It
patches exactly one existing nested provider and preserves prior hooks.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
PACKAGE = "phase176_r3r37_composite_right_hopf_public"
MARKER = "        options.extend(expand_composite_suspension_equality(goal))"
R3R31_MARKER = "        options.extend(expand_generic_hopf_substitution(goal, tuple(available)))"
PATCH = (
    "        # Phase 176 R3R37: source-screened composite-right Hopf candidates.\n"
    "        from phase176_r3r36_composite_right_hopf_isolated.source import (\n"
    "            expand_cited_composite_right_hopf,\n"
    "        )\n"
    "        options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))\n"
)
PATCH_CALL = "options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))"


def _nested_expand_location(source: str) -> tuple[int, int]:
    """Return one-based line bounds for the exact public nested expand()."""
    module = ast.parse(source)
    outer = [
        node for node in module.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(outer) != 1:
        raise ValueError("EXPECTED_ONE_SHARED_EXPANSION_PROVIDER")
    nested = [
        node for node in ast.walk(outer[0])
        if isinstance(node, ast.FunctionDef) and node.name == "expand"
    ]
    if len(nested) != 1:
        raise ValueError("EXPECTED_ONE_NESTED_EXPAND")
    return nested[0].lineno, nested[0].end_lineno


def proposed_code(source: str) -> str:
    """Insert exactly once after R3R35 or accept identical prior insertion."""
    if not isinstance(source, str):
        raise TypeError("source must be str")
    lines = source.splitlines(keepends=True)
    marker_indexes = [
        index for index, line in enumerate(lines)
        if line.rstrip("\r\n") == MARKER
    ]
    if len(marker_indexes) != 1:
        raise ValueError("R3R35_ANCHOR_NOT_UNIQUE")
    if sum(line.rstrip("\r\n") == R3R31_MARKER for line in lines) != 1:
        raise ValueError("R3R31_ANCHOR_NOT_UNIQUE")
    start, end = _nested_expand_location(source)
    index = marker_indexes[0]
    if not start <= index + 1 <= end:
        raise ValueError("R3R35_ANCHOR_OUTSIDE_NESTED_EXPAND")
    eol = "\r\n" if "\r\n" in source else "\n"
    patch = PATCH.replace("\n", eol)
    patch_lines = patch.splitlines(keepends=True)
    already = PATCH_CALL in source
    if already:
        if source.count(PATCH_CALL) != 1:
            raise ValueError("DUPLICATE_R3R37_PROVIDER")
        if "".join(lines[index + 1:index + 1 + len(patch_lines)]) != patch:
            raise ValueError("CONFLICTING_R3R37_PATCH")
        return source
    if "expand_cited_composite_right_hopf" in source:
        raise ValueError("PARTIAL_R3R37_PATCH")
    lines.insert(index + 1, patch)
    result = "".join(lines)
    ast.parse(result)
    if result.count(PATCH_CALL) != 1:
        raise ValueError("R3R37_PROVIDER_NOT_UNIQUE")
    return result


def changed_function_text(source: str) -> str:
    """Extract the entire enclosing public function, including nested expand."""
    module = ast.parse(source)
    outer = [
        node for node in module.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(outer) != 1:
        raise ValueError("SHARED_FUNCTION_NOT_UNIQUE")
    node = outer[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def git(*args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True,
    )
    if completed.returncode:
        raise RuntimeError("GIT_FAILED: " + completed.stderr.strip())
    return completed.stdout.strip()


def preflight() -> str:
    """Require develop, current proof-source files, and a matching repository root."""
    checkout = Path(git("rev-parse", "--show-toplevel")).resolve()
    if str(checkout).casefold() != str(ROOT.resolve()).casefold():
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    for relative, signatures in {
        "phase176_r3r36_composite_right_hopf_isolated/source.py": (
            "def expand_cited_composite_right_hopf(",
            "def composite_hopf_substitution_inputs(",
        ),
        "phase176_r3r34_composite_suspension_isolated/source.py": (
            "def expand_composite_suspension_equality(",
        ),
        "phase171_r2h_prop22_cited_hopf/source.py": (
            "class TodaProp22RightFormula:",
        ),
        "phase176_r3r30_generic_hopf_substitution_isolated/source.py": (
            "def expand_generic_hopf_substitution(",
        ),
    }.items():
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError("DEPENDENCY_MISSING: " + relative)
        content = path.read_text(encoding="utf-8-sig")
        if not all(signature in content for signature in signatures):
            raise RuntimeError("DEPENDENCY_SIGNATURE_CHANGED: " + relative)
    if not TARGET.is_file():
        raise RuntimeError("SHARED_PROVIDER_MISSING")
    return git("rev-parse", "HEAD")


def report_folder() -> Path:
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def install(dry_run: bool) -> dict:
    head = preflight()
    original_bytes = TARGET.read_bytes()
    bom = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
    original = original_bytes[len(bom):].decode("utf-8")
    updated = proposed_code(original)
    unchanged = updated == original
    if not unchanged and (
        git("diff", "--", "phase165_r52_r9_shared_math.py")
        or git("diff", "--cached", "--", "phase165_r52_r9_shared_math.py")
    ):
        raise RuntimeError("EXISTING_SHARED_SOURCE_EDITS_REFUSED")
    output = report_folder()
    full = changed_function_text(updated)
    artifact = output / "CHANGED_FUNCTION_FULL_JA.md"
    artifact.write_text(
        "# Phase 176 R3R37 — 変更後の関数全文\n\n"
        "対象：`phase165_r52_r9_shared_math.py` の "
        "`shared_expansion_provider()`（内部の `expand()` を含む全文）。\n\n"
        "```python\n" + full + ("" if full.endswith("\n") else "\n") + "```\n",
        encoding="utf-8",
    )
    if not dry_run and not unchanged:
        (output / "phase165_r52_r9_shared_math.py.before_R3R37").write_bytes(original_bytes)
        TARGET.write_bytes(bom + updated.encode("utf-8"))
    return {
        "gate": "PASS_R3R37_DRYRUN" if dry_run else "PASS_R3R37_PATCH_INSTALLED_TESTS_PENDING",
        "head": head,
        "changed_on_this_run": not dry_run and not unchanged,
        "already_connected": unchanged,
        "target": str(TARGET),
        "full_function": str(artifact),
        "new_given": 0,
        "new_source_assertions": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    try:
        result = install(arguments.dry_run)
    except Exception as error:
        result = {
            "gate": "FAIL_R3R37_INSTALL",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    destination = report_folder() / "install_report.json"
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for key, value in result.items():
        print("PHASE176_R3R37_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## 新規 `audit.py` — 全文（import、関数、テストを含む）

```python
"""Phase 176 R3R37: source-screened public candidate and local inference replay.

The report does not claim that the shared DFS citation/order gate was checked.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r37_composite_right_hopf_public"


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
    from map_facts import EHP_H_MAP
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import (
        TodaProp22RightFormula, _formula_parts,
    )
    from phase176_r3r34_composite_suspension_isolated.source import (
        composite_suspension_equality_input,
    )
    from phase176_r3r36_composite_right_hopf_isolated.source import (
        COMPOSITE_FORMULA_RULE_NAME, COMPOSITE_SUBSTITUTION_RULE_NAME,
        composite_hopf_substitution_inputs,
    )
    from proof import ProofRule, Relation, RelationType, find_inference_match, apply_inference_match
    from unified_statement_registry import AssertionOrigin

    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    beta = Composition(eta5, eta6)
    suspended_beta = Suspension(beta)
    lhs = MapApplication(EHP_H_MAP, Composition(nu, suspended_beta))
    formula = Relation(
        lhs, Composition(MapApplication(EHP_H_MAP, nu), suspended_beta),
        RelationType.EQUALITY,
    )
    substituted = Relation(
        lhs, Composition(eta5, suspended_beta), RelationType.EQUALITY,
    )
    hopf = Relation(MapApplication(EHP_H_MAP, nu), eta5, RelationType.EQUALITY)

    if composite_hopf_substitution_inputs(substituted) != (formula, hopf):
        raise RuntimeError("R3R36_TYPED_SUBSTITUTION_CONTRACT_CHANGED")

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    source_steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    available = tuple(step.conclusion for step in source_steps)
    if available.count(TodaProp22RightFormula()) != 1 or available.count(hopf) != 1:
        raise RuntimeError("SCREENED_SOURCE_WITNESSES_NOT_UNIQUE")

    provider = shared_expansion_provider(screened, proof_target=roots[0])
    formula_candidates = tuple(
        item for item in provider(formula)
        if item.rule.name == COMPOSITE_FORMULA_RULE_NAME
    )
    substitution_candidates = tuple(
        item for item in provider(substituted)
        if item.rule.name == COMPOSITE_SUBSTITUTION_RULE_NAME
    )
    if (len(formula_candidates) != 1
            or formula_candidates[0].subgoals != (TodaProp22RightFormula(),)
            or len(substitution_candidates) != 1
            or substitution_candidates[0].subgoals != (formula, hopf)):
        raise RuntimeError("PUBLIC_COMPOSITE_HOPF_CANDIDATES_NOT_CONNECTED")

    universal = next(step for step in source_steps
                     if step.conclusion == TodaProp22RightFormula())
    source_hopf = next(step for step in source_steps
                       if step.conclusion == hopf)
    first_match = find_inference_match(formula_candidates[0].rule, (universal,))
    if first_match is None:
        raise RuntimeError("NO_FORMULA_INFERENCE_REPLAY")
    formula_step = apply_inference_match(first_match)
    second_match = find_inference_match(
        substitution_candidates[0].rule, (formula_step, source_hopf),
    )
    if second_match is None:
        raise RuntimeError("NO_HOPF_SUBSTITUTION_REPLAY")
    substituted_step = apply_inference_match(second_match)
    if (substituted_step.conclusion != substituted
            or substituted_step.rule is not ProofRule.INFERENCE
            or substituted_step.premises != (formula_step, source_hopf)):
        raise RuntimeError("INVALID_HOPF_REPLAY_CHAIN")

    # Regression: R3R35 stays visible and the historical single-factor path works.
    suspension_goal = Relation(
        Suspension(beta), Composition(eta6, eta7), RelationType.EQUALITY,
    )
    image = composite_suspension_equality_input(suspension_goal)
    if image is None:
        raise RuntimeError("R3R35_SUSPENSION_GOAL_TYPE_INVALID")
    suspension_candidates = tuple(
        item for item in provider(suspension_goal)
        if item.rule.name == "proved composite suspension image yields typed element equality"
    )
    if len(suspension_candidates) != 1 or suspension_candidates[0].subgoals != (image,):
        raise RuntimeError("R3R35_PUBLIC_BRANCH_LOST")
    single = Relation(
        MapApplication(EHP_H_MAP, Composition(nu, Suspension(eta5))),
        Composition(MapApplication(EHP_H_MAP, nu), Suspension(eta5)),
        RelationType.EQUALITY,
    )
    if _formula_parts(single) != (nu, eta5):
        raise RuntimeError("SINGLE_FACTOR_FORMULA_TYPE_INVALID")
    single_candidates = tuple(
        item for item in provider(single)
        if item.rule.name == "specialize cited Toda Proposition 2.2 right formula"
    )
    if len(single_candidates) != 1:
        raise RuntimeError("SINGLE_FACTOR_PROVIDER_REGRESSION")
    return {
        "gate": "PASS_R3R37_PUBLIC_COMPOSITE_HOPF_CONNECTED",
        "screened_prop22_count": available.count(TodaProp22RightFormula()),
        "screened_hopf_nu_prime_count": available.count(hopf),
        "public_formula_candidate_count": len(formula_candidates),
        "public_substitution_candidate_count": len(substitution_candidates),
        "public_substitution_subgoals": len(substitution_candidates[0].subgoals),
        "local_formula_replayed": formula_step.conclusion == formula,
        "local_substitution_replayed": substituted_step.conclusion == substituted,
        "r3r35_public_candidate_preserved": True,
        "legacy_single_factor_candidate_preserved": True,
        "source_screened_context_used": True,
        "shared_dfs_source_order_gate_verified": False,
        "transport_to_eta_cube_proved": False,
        "hopf_image_goal_proved": False,
        "root_group_proved": False,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    try:
        result = probe()
    except Exception as error:
        result = {
            "gate": "FAIL_R3R37_PUBLIC_AUDIT",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE)
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / "public_report.json"
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for key, value in result.items():
        print("PHASE176_R3R37_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## 新規 `tests/test_installer.py` — 全文（import、関数、テストを含む）

```python
"""Focused regression for the R3R37 minimal public-hook installer."""
from __future__ import annotations

import ast

import pytest

from phase176_r3r37_composite_right_hopf_public.installer import (
    MARKER, PATCH, PATCH_CALL, R3R31_MARKER, changed_function_text,
    proposed_code,
)


def _baseline() -> str:
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + R3R31_MARKER + "\n"
        + MARKER + "\n"
        "        return tuple(options)\n"
        "    return expand\n"
    )


def test_inserts_once_without_changing_prior_hooks() -> None:
    original = _baseline()
    proposed = proposed_code(original)
    assert proposed.replace(PATCH, "", 1) == original
    assert proposed.count(PATCH_CALL) == 1
    assert proposed.count(R3R31_MARKER) == 1
    assert proposed.count(MARKER) == 1
    assert proposed_code(proposed) == proposed
    ast.parse(proposed)
    assert PATCH_CALL in changed_function_text(proposed)


def test_handles_windows_line_endings() -> None:
    original = _baseline().replace("\n", "\r\n")
    changed = proposed_code(original)
    assert changed.count(PATCH_CALL) == 1
    assert proposed_code(changed) == changed
    assert "\n" not in changed.replace("\r\n", "")


def test_missing_r3r35_anchor_fails_closed() -> None:
    with pytest.raises(ValueError, match="R3R35_ANCHOR_NOT_UNIQUE"):
        proposed_code(_baseline().replace(MARKER + "\n", ""))


def test_anchor_outside_nested_expand_fails_closed() -> None:
    original = (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + R3R31_MARKER + "\n"
        "        return tuple(options)\n"
        "    return expand\n"
        "def unrelated():\n"
        "    if True:\n"
        "        options = []\n"
        + MARKER + "\n"
        "        return options\n"
    )
    with pytest.raises(ValueError, match="OUTSIDE_NESTED_EXPAND"):
        proposed_code(original)


def test_duplicate_or_conflicting_patch_fails_closed() -> None:
    proposed = proposed_code(_baseline())
    with pytest.raises(ValueError, match="DUPLICATE_R3R37_PROVIDER"):
        proposed_code(proposed + "\n# " + PATCH_CALL + "\n")
    conflicting = proposed.replace(
        "        # Phase 176 R3R37: source-screened composite-right Hopf candidates.\n",
        "        # changed without review\n",
    )
    with pytest.raises(ValueError, match="CONFLICTING_R3R37_PATCH"):
        proposed_code(conflicting)


def test_non_source_or_duplicate_anchor_fails_closed() -> None:
    with pytest.raises(TypeError, match="source must be str"):
        proposed_code(None)
    duplicate = _baseline().replace(MARKER + "\n", MARKER + "\n" + MARKER + "\n")
    with pytest.raises(ValueError, match="R3R35_ANCHOR_NOT_UNIQUE"):
        proposed_code(duplicate)
```

## 新規 `tests/test_public.py` — 全文（import、関数、テストを含む）

```python
"""Live shared-provider integration in the user's source-first checkout."""
from __future__ import annotations

from phase176_r3r37_composite_right_hopf_public.audit import probe


def test_screened_composite_formula_substitution_and_old_branches() -> None:
    result = probe()
    assert result["gate"] == "PASS_R3R37_PUBLIC_COMPOSITE_HOPF_CONNECTED"
    assert result["public_formula_candidate_count"] == 1
    assert result["public_substitution_candidate_count"] == 1
    assert result["public_substitution_subgoals"] == 2
    assert result["local_formula_replayed"] is True
    assert result["local_substitution_replayed"] is True
    assert result["r3r35_public_candidate_preserved"] is True
    assert result["legacy_single_factor_candidate_preserved"] is True
    assert result["shared_dfs_source_order_gate_verified"] is False
    assert result["root_group_proved"] is False
```

## 新規 `run.ps1` — 全文（import、関数、テストを含む）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $installArgs = @()
    if ($DryRun) { $installArgs += '--dry-run' }
    & python -B -m phase176_r3r37_composite_right_hopf_public.installer @installArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R37 installer or DryRun failed' }
    if (-not $DryRun) {
        & python -B -m phase176_r3r37_composite_right_hopf_public.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R37 public audit failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r37_composite_right_hopf_public/tests/test_installer.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R37 installer pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r37_composite_right_hopf_public/tests/test_public.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R37 public pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r36_composite_right_hopf_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R36 isolated regression failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r35_composite_suspension_public/tests/test_public.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R35 public regression failed' }
        & python -B -m pytest -q -p no:cacheprovider phase171_r2h_prop22_cited_hopf/tests/test_cited_formula.py -k 'right_formula_requires_screened_source or right_formula_rejects_wrong_rhs_and_bad_dimensions'
        if ($LASTEXITCODE -ne 0) { throw 'Legacy Proposition 2.2 regression failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Git diff check failed' }
        Write-Host 'PHASE176_R3R37_GATE=PASS_R3R37_PUBLIC_CONNECTED_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R37_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
```

