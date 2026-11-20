# Phase 176 R3R28 — コード全文

新規コードを全文掲載。既存2関数は installer が現行チェックアウトを読み、**置換後の全関数**を `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r28_toda55_quadruple_public\CHANGED_FUNCTIONS_FULL_JA.md` に生成します。module-level import は変更しません。

## install.py

```python
"""Install only the Phase 176 R3R28 shared Toda (5.5) connection.

The source of the two existing functions is preserved byte for byte except
for two bounded insertions.  Dry-run makes no repository code modifications.
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

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r28_toda55_quadruple_public"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
SOURCE = ROOT / "phase176_r3r27r1_toda55_quadruple_isolated" / "source.py"
SOURCE_ANCHOR = "    registry = UnifiedStatementRegistry()\n    links = []\n    records = []\n"
SOURCE_PATCH = (
    "    # Phase 176 R3R28: append a separate source-checked (5.5) quadruple clause.\n"
    "    # Existing source indices remain unchanged; no target group is GIVEN.\n"
    "    if default_sources:\n"
    "        from phase176_r3r27r1_toda55_quadruple_isolated.source import (\n"
    "            build_cited_toda55_quadruple_source,\n"
    "        )\n"
    "        sources = sources + (build_cited_toda55_quadruple_source(),)\n"
)
PROVIDER_ANCHOR = "    from phase165_r12_r15_toda51 import expand_cited_toda51_zero\n"
PROVIDER_PATCH = (
    "    # Phase 176 R3R28: conditional general right-hand side of Toda (5.5).\n"
    "    # The source and both definitions must survive source-first screening.\n"
    "    from phase176_r3r27r1_toda55_quadruple_isolated.source import (\n"
    "        expand_cited_quadruple,\n"
    "    )\n"
    "    def expand_public_toda55_quadruple(goal: object):\n"
    "        return expand_cited_quadruple(goal, tuple(available))\n"
    "    extra_providers = (expand_public_toda55_quadruple,) + tuple(extra_providers)\n"
)


def git(*args: str) -> str:
    result = subprocess.run(("git", *args), cwd=ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + ": " + result.stderr.strip())
    return result.stdout.strip()


def checked_root() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    if not SOURCE.is_file():
        raise RuntimeError("PREVIOUS_ISOLATED_SOURCE_MISSING")
    return git("rev-parse", "HEAD")


def functions_in(source: str) -> dict[str, str]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    return {node.name: "".join(lines[node.lineno - 1:node.end_lineno])
            for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def proposed(current: str) -> str:
    funcs = functions_in(current)
    for name in ("build_shared_typed_bridge", "shared_expansion_provider"):
        if name not in funcs:
            raise RuntimeError("FUNCTION_MISSING: " + name)
    if SOURCE_PATCH.strip() in current and PROVIDER_PATCH.strip() in current:
        return current
    if SOURCE_PATCH.strip() in current or PROVIDER_PATCH.strip() in current:
        raise RuntimeError("PARTIAL_PATCH_DETECTED")
    if funcs["build_shared_typed_bridge"].count(SOURCE_ANCHOR) != 1:
        raise RuntimeError("SOURCE_INSERTION_ANCHOR_CHANGED")
    if funcs["shared_expansion_provider"].count(PROVIDER_ANCHOR) != 1:
        raise RuntimeError("PROVIDER_INSERTION_ANCHOR_CHANGED")
    replacement = funcs["build_shared_typed_bridge"].replace(SOURCE_ANCHOR, SOURCE_PATCH + SOURCE_ANCHOR, 1)
    current = current.replace(funcs["build_shared_typed_bridge"], replacement, 1)
    funcs = functions_in(current)
    replacement = funcs["shared_expansion_provider"].replace(PROVIDER_ANCHOR, PROVIDER_PATCH + PROVIDER_ANCHOR, 1)
    current = current.replace(funcs["shared_expansion_provider"], replacement, 1)
    ast.parse(current)
    return current


def full_code_md(source: str) -> str:
    funcs = functions_in(source)
    return ("# R3R28 変更後の関数全文\n\n"
            "対象: `phase165_r52_r9_shared_math.py`。module-level import は変更しません。\n\n"
            "## build_shared_typed_bridge()\n\n```python\n"
            + funcs["build_shared_typed_bridge"] + "\n```\n\n"
            "## shared_expansion_provider()\n\n```python\n"
            + funcs["shared_expansion_provider"] + "\n```\n")


def output_dir() -> Path:
    path = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    path.mkdir(parents=True, exist_ok=True)
    return path


def execute(dry_run: bool) -> int:
    report = {"phase": "176_R3R28", "gate": "FAIL_R3R28", "full_pytest": "NOT_RUN",
              "new_direct_group_given": 0, "production_target": "phase165_r52_r9_shared_math.py"}
    try:
        report["head"] = checked_root()
        original = TARGET.read_bytes()
        if b"\r\n" in original:
            newline = "\r\n"
        else:
            newline = "\n"
        normalized = original.decode("utf-8-sig").replace("\r\n", "\n")
        output = proposed(normalized)
        report["changed"] = normalized != output
        report["new_source_assertions"] = 1
        report["new_mathematical_rules"] = 0
        if not dry_run:
            if output != normalized:
                # Atomic write without touching unrelated source content.
                data = output.replace("\n", newline).encode("utf-8")
                temporary = TARGET.with_suffix(".r3r28.tmp")
                temporary.write_bytes(data)
                temporary.replace(TARGET)
            (output_dir() / "CHANGED_FUNCTIONS_FULL_JA.md").write_text(full_code_md(output), encoding="utf-8")
            report["gate"] = "PASS_R3R28_PATCH_INSTALLED_TESTS_PENDING"
        else:
            report["gate"] = "PASS_R3R28_DRYRUN"
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
    path = output_dir() / "report.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key in ("gate", "head", "changed", "new_source_assertions", "new_mathematical_rules"):
        if key in report:
            print("PHASE176_R3R28_" + key.upper() + "=" + str(report[key]))
    if "error" in report:
        print("PHASE176_R3R28_ERROR=" + report["error"])
    print("PHASE176_R3R28_REPORT=" + str(path))
    print("PHASE176_R3R28_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())

```

## tests/test_public.py

```python
"""Phase 176 R3R28 focused contracts for source-first public wiring."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase176_r3r28_toda55_quadruple_public import install
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement,
    canonical_quadruple_goal,
)
from proof import ProofRule


def test_patch_both_functions_and_idempotent() -> None:
    current = install.TARGET.read_text(encoding="utf-8-sig")
    result = install.proposed(current.replace("\r\n", "\n"))
    functions = install.functions_in(result)
    assert "build_cited_toda55_quadruple_source" in functions["build_shared_typed_bridge"]
    assert "expand_public_toda55_quadruple" in functions["shared_expansion_provider"]
    assert install.proposed(result) == result


def test_partial_patch_fails_closed() -> None:
    current = install.TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    without = current.replace(install.PROVIDER_PATCH, "")
    if install.SOURCE_PATCH in without:
        with pytest.raises(RuntimeError, match="PARTIAL_PATCH_DETECTED"):
            install.proposed(without)


def test_full_source_contains_complete_functions() -> None:
    current = install.TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    text = install.full_code_md(install.proposed(current))
    assert "def build_shared_typed_bridge" in text
    assert "def shared_expansion_provider" in text


def test_default_shared_bridge_has_one_screened_quadruple_source() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    assert len(roots) == 1
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    statements = tuple(link.step.conclusion for link in screened.proof_links
                       if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert statements.count(Toda55UniversalQuadrupleStatement()) == 1
    assert roots[0] not in statements


def test_shared_provider_proposes_and_proves_nu5_quadruple() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    assert len(roots) == 1
    root = roots[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    goal = canonical_quadruple_goal(5)
    assert goal is not None
    choices = tuple(item for item in provider(goal)
                    if item.rule.name == "specialize cited Toda (5.5) quadruple nu-family identity")
    assert len(choices) == 1
    assert len(choices[0].subgoals) == 3
    citing = resolve_specialized_goal_citing_id(bridge, root)
    assert citing is not None
    result = reconstruct_registered_goal(goal, screened, citing, provider, lookup_mode="typed_reference")
    assert result is not None and result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert len(result.premises) == 3
    assert not any(step.conclusion == root for step in result.premises)

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    if ($DryRun) {
        python -B -m phase176_r3r28_toda55_quadruple_public.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R28 DryRun failed' }
    } else {
        python -B -m phase176_r3r28_toda55_quadruple_public.install
        if ($LASTEXITCODE -ne 0) { throw 'R3R28 installation failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r28_toda55_quadruple_public\tests `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests `
            .\phase174_r3_r6_source_extension\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R28 focused tests failed' }
        Write-Host 'PHASE176_R3R28_GATE=PASS_R3R28_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R28_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}

```
