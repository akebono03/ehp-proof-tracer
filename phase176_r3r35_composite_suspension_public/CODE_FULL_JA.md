# R3R35 変更コード全文



## 変更内容

既存 `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` の内部関数 `expand()` に、R3R34 の候補を返す呼び出しを追加する。既存トップレベル import は変更しない。共有関数全文は DryRun 時にも `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r35_composite_suspension_public\CHANGED_FUNCTION_FULL_JA.md` に生成される。実際の関数全文は実行環境の現行ソースから AST 解析で抽出し、途中の省略をしない。

## 追加する import と候補生成

```python
        # Phase 176 R3R35: composite suspension equality; image stays an open goal.
        from phase176_r3r34_composite_suspension_isolated.source import (
            expand_composite_suspension_equality,
        )
        options.extend(expand_composite_suspension_equality(goal))
```

## installer.py — 全文

```python
"""Fail-closed public registration of the independently tested R3R34 bridge."""
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
PACKAGE = "phase176_r3r35_composite_suspension_public"
MARKER = "        options.extend(expand_generic_hopf_substitution(goal, tuple(available)))"
PATCH = (
    "        # Phase 176 R3R35: composite suspension equality; image stays an open goal.\n"
    "        from phase176_r3r34_composite_suspension_isolated.source import (\n"
    "            expand_composite_suspension_equality,\n"
    "        )\n"
    "        options.extend(expand_composite_suspension_equality(goal))\n"
)


def _shared_expand_location(source: str) -> tuple[int, int]:
    """Find the exact nested public provider; reject ambiguous refactors."""
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
    """Insert one hook, or accept an exact prior installation unchanged."""
    if not isinstance(source, str):
        raise TypeError("source must be str")
    lines = source.splitlines(keepends=True)
    anchors = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == MARKER]
    if len(anchors) != 1:
        raise ValueError("EXPECTED_ONE_R3R31_ANCHOR")
    low, high = _shared_expand_location(source)
    index = anchors[0]
    if not low <= index + 1 <= high:
        raise ValueError("R3R31_ANCHOR_OUTSIDE_NESTED_EXPAND")
    eol = "\r\n" if "\r\n" in source else "\n"
    patch = PATCH.replace("\n", eol)
    if "expand_composite_suspension_equality(goal)" in source:
        if source.count(patch) != 1 or index + 1 >= len(lines):
            raise ValueError("CONFLICTING_R3R35_PATCH")
        if "".join(lines[index + 1:index + 1 + len(PATCH.splitlines())]) != patch:
            raise ValueError("R3R35_PATCH_AT_UNEXPECTED_POSITION")
        return source
    lines.insert(index + 1, patch)
    candidate = "".join(lines)
    ast.parse(candidate)
    if candidate.count("options.extend(expand_composite_suspension_equality(goal))") != 1:
        raise ValueError("NEW_R3R35_PROVIDER_NOT_UNIQUE")
    return candidate


def changed_function_text(source: str) -> str:
    """Return the ENTIRE changed enclosing function for review."""
    module = ast.parse(source)
    nodes = [
        item for item in module.body
        if isinstance(item, ast.FunctionDef)
        and item.name == "shared_expansion_provider"
    ]
    if len(nodes) != 1:
        raise ValueError("SHARED_FUNCTION_MISSING")
    node = nodes[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def git(*args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=ROOT, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + result.stderr.strip())
    return result.stdout.strip()


def preflight() -> str:
    """Guard the target source and the required isolated rule."""
    actual = Path(git("rev-parse", "--show-toplevel")).resolve()
    if str(actual).casefold() != str(ROOT.resolve()).casefold():
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    for path in (
        "phase176_r3r34_composite_suspension_isolated/source.py",
        "phase176_r3r30_generic_hopf_substitution_isolated/source.py",
        "phase171_r2h_prop22_cited_hopf/source.py",
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError("MISSING_DEPENDENCY: " + path)
    if not TARGET.is_file():
        raise RuntimeError("SHARED_PROVIDER_MISSING")
    return git("rev-parse", "HEAD")


def install(dry_run: bool) -> dict:
    head = preflight()
    original_bytes = TARGET.read_bytes()
    bom = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
    original = original_bytes[len(bom):].decode("utf-8")
    revised = proposed_code(original)
    unchanged = revised == original
    if not unchanged and (
        git("diff", "--", TARGET.name)
        or git("diff", "--cached", "--", TARGET.name)
    ):
        raise RuntimeError("UNCOMMITTED_TARGET_EDITS_REFUSED")
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE)
    folder.mkdir(parents=True, exist_ok=True)
    full = changed_function_text(revised)
    (folder / "CHANGED_FUNCTION_FULL_JA.md").write_text(
        "# R3R35 変更後の関数全文\n\n"
        "対象: `phase165_r52_r9_shared_math.py` の "
        "`shared_expansion_provider()`（全文）。\n\n```python\n"
        + full + ("" if full.endswith("\n") else "\n") + "```\n",
        encoding="utf-8",
    )
    if not dry_run and not unchanged:
        backup = folder / "phase165_r52_r9_shared_math.py.before_R3R35"
        backup.write_bytes(original_bytes)
        TARGET.write_bytes(bom + revised.encode("utf-8"))
    return {
        "gate": ("PASS_R3R35_DRYRUN" if dry_run
                 else "PASS_R3R35_PATCH_INSTALLED_TESTS_PENDING"),
        "head": head,
        "changed_on_this_run": not dry_run and not unchanged,
        "already_connected": unchanged,
        "target": str(TARGET),
        "full_function": str(folder / "CHANGED_FUNCTION_FULL_JA.md"),
        "new_given": 0,
        "new_source_assertions": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        report = install(args.dry_run)
    except Exception as error:
        report = {
            "gate": "FAIL_R3R35_INSTALL",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE)
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / "install_report.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for key, value in report.items():
        print("PHASE176_R3R35_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    return 0 if report["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())

```

## audit.py — 全文

```python
"""Read-only, source-screened public frontier and local inference replay."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r35_composite_suspension_public"
RULE_NAME = "proved composite suspension image yields typed element equality"


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Suspension
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase176_r3r34_composite_suspension_isolated.source import (
        composite_suspension_equality_input,
    )
    from proof import Relation, RelationType, ProofRule, find_inference_match, apply_inference_match

    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    goal = Relation(
        Suspension(Composition(eta5, eta6)),
        Composition(eta6, eta7), RelationType.EQUALITY,
    )
    image = composite_suspension_equality_input(goal)
    if image is None:
        raise RuntimeError("INVALID_TYPED_COMPOSITE_SUSPENSION_GOAL")
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    provider = shared_expansion_provider(screened, proof_target=roots[0])
    candidates = tuple(item for item in provider(goal) if item.rule.name == RULE_NAME)
    if len(candidates) != 1 or candidates[0].subgoals != (image,):
        raise RuntimeError("PUBLIC_COMPOSITE_SUSPENSION_CANDIDATE_NOT_CONNECTED")

    # Explicitly replay only the locally available definitional inference chain.
    # This is not an assertion that DFS's source-order/citation gate has passed.
    image_options = provider(image)
    replayed = False
    replay_rules = []
    for option in image_options:
        if option.subgoals:
            continue
        first_match = find_inference_match(option.rule, ())
        if first_match is None:
            continue
        first_step = apply_inference_match(first_match)
        if first_step.rule is not ProofRule.INFERENCE or first_step.conclusion != image:
            continue
        second_match = find_inference_match(candidates[0].rule, (first_step,))
        if second_match is None:
            continue
        second_step = apply_inference_match(second_match)
        if (second_step.rule is ProofRule.INFERENCE
                and second_step.conclusion == goal
                and second_step.premises == (first_step,)):
            replayed = True
            replay_rules = [option.rule.name, candidates[0].rule.name]
            break
    return {
        "gate": "PASS_R3R35_PUBLIC_BRANCH_CONNECTED",
        "public_candidate_count": len(candidates),
        "public_subgoal_count": len(candidates[0].subgoals),
        "image_candidate_rules": [item.rule.name for item in image_options],
        "isolated_inference_replayed": replayed,
        "isolated_replay_rules": replay_rules,
        "source_screened_context_used": True,
        "shared_dfs_source_order_gate_verified": False,
        "hopf_image_proved": False,
        "root_group_proved": False,
        "new_given": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    try:
        result = probe()
    except Exception as error:
        result = {
            "gate": "FAIL_R3R35_PUBLIC_AUDIT",
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
        print("PHASE176_R3R35_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())

```

## tests/test_installer.py — 全文

```python
"""Installer guard tests: no dependency on a full project import graph."""
from __future__ import annotations

import ast
import pytest

from phase176_r3r35_composite_suspension_public.installer import (
    MARKER,
    PATCH,
    proposed_code,
    changed_function_text,
)


def baseline() -> str:
    return (
        "def shared_expansion_provider(bridge):\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + MARKER + "\n"
        "        return tuple(options)\n"
        "    return expand\n"
    )


def test_patch_adds_exactly_one_nested_provider() -> None:
    revised = proposed_code(baseline())
    ast.parse(revised)
    assert revised.count("options.extend(expand_composite_suspension_equality(goal))") == 1
    assert PATCH in revised
    assert "def shared_expansion_provider(" in changed_function_text(revised)


def test_patch_is_idempotent() -> None:
    revised = proposed_code(baseline())
    assert proposed_code(revised) == revised


def test_patch_rejects_missing_or_external_anchor() -> None:
    with pytest.raises(ValueError, match="EXPECTED_ONE_R3R31_ANCHOR"):
        proposed_code("def shared_expansion_provider():\n    return None\n")
    wrong = (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        return ()\n"
        "    return expand\n\n"
        "def unrelated():\n"
        + MARKER + "\n"
    )
    with pytest.raises(ValueError, match="R3R31_ANCHOR_OUTSIDE_NESTED_EXPAND"):
        proposed_code(wrong)


def test_patch_rejects_conflicting_insertion() -> None:
    incorrect = baseline() + "\n# expand_composite_suspension_equality(goal)\n"
    with pytest.raises(ValueError, match="CONFLICTING_R3R35_PATCH"):
        proposed_code(incorrect)

```

## tests/test_public.py — 全文

```python
"""Public-source-screened proposal tests; proof completion is not asserted."""
from __future__ import annotations

import pytest

from phase176_r3r35_composite_suspension_public.audit import probe
from phase176_r3r35_composite_suspension_public.installer import TARGET, PATCH


@pytest.fixture(scope="module")
def observed() -> dict:
    return probe()


def test_public_composite_suspension_candidate(observed: dict) -> None:
    assert observed["public_candidate_count"] == 1
    assert observed["public_subgoal_count"] == 1
    assert observed["source_screened_context_used"] is True


def test_public_connection_is_not_group_proof(observed: dict) -> None:
    assert observed["root_group_proved"] is False
    assert observed["hopf_image_proved"] is False
    assert observed["new_given"] == 0
    assert PATCH in TARGET.read_text(encoding="utf-8-sig")

```

## run.ps1 — 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $installArgs = @()
    if ($DryRun) { $installArgs += '--dry-run' }
    & python -B -m phase176_r3r35_composite_suspension_public.installer @installArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R35 installation or DryRun failed' }
    if (-not $DryRun) {
        & python -B -m phase176_r3r35_composite_suspension_public.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R35 public audit failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r35_composite_suspension_public/tests/test_installer.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R35 installer tests failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r35_composite_suspension_public/tests/test_public.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R35 public tests failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r34_composite_suspension_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R34 isolated regressions failed' }
        & python -B -m pytest -q -p no:cacheprovider tests/test_hopf_rules.py -k 'hopf_composition_formula or hopf_invariant_reaches_hopf_composition_formula'
        if ($LASTEXITCODE -ne 0) { throw 'Existing Hopf regressions failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Git diff check failed' }
        Write-Host 'PHASE176_R3R35_GATE=PASS_R3R35_PUBLIC_CONNECTED_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R35_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}

```
