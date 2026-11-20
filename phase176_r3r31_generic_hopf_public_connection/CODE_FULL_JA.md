# R3R31 新規コード全文

## installer.py

```python
"""Minimal, fail-closed public hookup for the audited R3R30 rule."""
from __future__ import annotations

import ast
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
MARKER = "        options.extend(expand_cited_prop22_right_formula(goal, tuple(available)))"
NEW_LINES = (
    "        # Phase 176 R3R31: general Hopf substitution with two open proof obligations.\n"
    "        from phase176_r3r30_generic_hopf_substitution_isolated.source import (\n"
    "            expand_generic_hopf_substitution,\n"
    "        )\n"
    "        options.extend(expand_generic_hopf_substitution(goal, tuple(available)))\n"
)


def proposed_code(source: str) -> str:
    """Insert one additive provider call, preserving all existing source text."""
    if not isinstance(source, str):
        raise TypeError("source must be str")
    if source.count(MARKER) != 1:
        raise ValueError("EXPECTED_SINGLE_PROP22_PROVIDER_ANCHOR")
    if "options.extend(expand_generic_hopf_substitution(goal, tuple(available)))" in source:
        raise ValueError("R3R31_ALREADY_APPLIED")
    tree = ast.parse(source)
    funcs = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "shared_expansion_provider"
    ]
    if len(funcs) != 1:
        raise ValueError("SHARED_PROVIDER_FUNCTION_NOT_UNIQUE")
    original_lines = source.splitlines(keepends=True)
    position = next(
        i for i, line in enumerate(original_lines)
        if MARKER in line
    )
    if not funcs[0].lineno - 1 <= position < funcs[0].end_lineno:
        raise ValueError("ANCHOR_OUTSIDE_SHARED_PROVIDER")
    eol = "\r\n" if "\r\n" in source else "\n"
    inserted = NEW_LINES.replace("\n", eol)
    original_lines.insert(position + 1, inserted)
    candidate = "".join(original_lines)
    ast.parse(candidate)
    if candidate.count("expand_generic_hopf_substitution(goal, tuple(available))") != 1:
        raise ValueError("NEW_PROVIDER_NOT_UNIQUE")
    return candidate


def git(*args: str) -> str:
    p = subprocess.run(("git", *args), cwd=ROOT, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if p.returncode:
        raise RuntimeError("GIT_COMMAND_FAILED: " + p.stderr.strip())
    return p.stdout.strip()


def verify_checkout() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if not (ROOT / "phase176_r3r30_generic_hopf_substitution_isolated" / "source.py").is_file():
        raise RuntimeError("R3R30_DEPENDENCY_MISSING")
    if not (ROOT / "phase176_r3r28_toda55_quadruple_public" / "tests" / "test_public.py").is_file():
        raise RuntimeError("R3R28_DEPENDENCY_MISSING")
    if git("diff", "--", "phase165_r52_r9_shared_math.py"):
        raise RuntimeError("TARGET_ALREADY_HAS_UNSTAGED_EDITS")
    if git("diff", "--cached", "--", "phase165_r52_r9_shared_math.py"):
        raise RuntimeError("TARGET_ALREADY_HAS_STAGED_EDITS")
    return git("rev-parse", "HEAD")


def changed_function_text(source: str) -> str:
    tree = ast.parse(source)
    node = next(
        item for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == "shared_expansion_provider"
    )
    return "".join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])


def install(dry_run: bool) -> dict:
    head = verify_checkout()
    current = TARGET.read_bytes()
    encoding = "utf-8-sig" if current.startswith(b"\xef\xbb\xbf") else "utf-8"
    original = current.decode(encoding)
    proposed = proposed_code(original)
    report_dir = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                  / "EHPProofTracerAudit" / "phase176_r3r31_generic_hopf_public_connection")
    report_dir.mkdir(parents=True, exist_ok=True)
    # Full function output for direct replacement review.
    if not dry_run:
        artifact = report_dir / "CHANGED_FUNCTION_FULL_JA.md"
        artifact.write_text(
            "# R3R31 変更後の関数全文\n\n対象: `phase165_r52_r9_shared_math.py` "
            "の `shared_expansion_provider()`\n\n```python\n"
            + changed_function_text(proposed) + "\n```\n",
            encoding="utf-8",
        )
        TARGET.write_bytes(proposed.encode(encoding))
    return {"gate": "PASS_R3R31_DRYRUN" if dry_run
            else "PASS_R3R31_PUBLIC_PATCH_INSTALLED_TESTS_PENDING",
            "head": head,
            "production_target": str(TARGET),
            "production_changed": not dry_run,
            "new_given": 0,
            "new_source_statements": 0,
            "new_math_rules": 0,
            "full_pytest": "NOT_RUN"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        report = install(args.dry_run)
    except Exception as err:
        report = {"gate": "FAIL_R3R31", "error": type(err).__name__ + ": " + str(err),
                  "full_pytest": "NOT_RUN"}
    report_dir = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                  / "EHPProofTracerAudit" / "phase176_r3r31_generic_hopf_public_connection")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "report.json"
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    for k, v in report.items():
        print("PHASE176_R3R31_" + k.upper() + "=" + str(v))
    print("PHASE176_R3R31_REPORT=" + str(report_file))
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## audit.py

```python
"""Read-only proof-search probe after the additive R3R31 public hookup."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from proof import ProofRule, Relation, RelationType
from phase176_r3r30_generic_hopf_substitution_isolated.source import generic_hopf_substitution_inputs


def probe() -> dict:
    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    alpha = Composition(nu, eta6)
    suspension = Suspension(eta6)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, suspension)),
        Composition(Composition(eta5, eta6), suspension),
        RelationType.EQUALITY,
    )
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    context = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    provider = shared_expansion_provider(context, proof_target=roots[0])
    expansions = tuple(x for x in provider(goal)
                       if x.rule.name ==
                       "substitute independently proved Hopf value into cited right formula")
    if len(expansions) != 1:
        raise RuntimeError("EXPECTED_ONE_GENERAL_HOPF_SUBSTITUTION_CANDIDATE")
    inputs = generic_hopf_substitution_inputs(goal)
    if inputs is None or expansions[0].subgoals != inputs:
        raise RuntimeError("INCORRECT_HOPF_SUBGOALS")
    result = {
        "gate": "PASS_R3R31_PUBLIC_CANDIDATE_CONNECTED",
        "candidate_count": len(expansions),
        "subgoal_count": len(inputs),
        "subgoal_rule_names": [
            [item.rule.name for item in provider(child)]
            for child in inputs
        ],
        "root_rule_names": [item.rule.name for item in provider(roots[0])],
        "hopf_image_complete_claimed": False,
        "root_group_complete_claimed": False,
        "new_given": 0,
        "full_pytest": "NOT_RUN",
    }
    # A source ID provides a search context, not a forged group citation.
    matching_ids = [
        a.assertion_id for a in context.registry._assertions.values()
        if a.origin.value == "fixed_statement"
        and a.content in tuple(
            link.step.conclusion for link in context.proof_links if link.step is not None
        )
        and isinstance(a.assertion_id, str)
        and "right_hopf_formula" in a.assertion_id
    ]
    if matching_ids:
        try:
            step = reconstruct_registered_goal(
                goal, context, matching_ids[0], provider,
                lookup_mode="typed_reference",
            )
            result["complete_proof"] = step.rule is ProofRule.INFERENCE
            result["proved_step_rule"] = step.rule.value
        except RegisteredGoalUnresolved as exc:
            result["complete_proof"] = False
            result["unresolved_reason"] = str(exc)[:400]
    else:
        result["complete_proof"] = False
        result["unresolved_reason"] = "NO_SOURCE_CONTEXT_ID"
    return result


def main() -> int:
    try:
        result = probe()
    except Exception as exc:
        result = {"gate": "FAIL_R3R31_PUBLIC_AUDIT",
                  "error": type(exc).__name__ + ": " + str(exc),
                  "full_pytest": "NOT_RUN"}
    path = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
            / "EHPProofTracerAudit" / "phase176_r3r31_generic_hopf_public_connection")
    path.mkdir(parents=True, exist_ok=True)
    file = path / "public_report.json"
    file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    for k,v in result.items():
        print("PHASE176_R3R31_" + k.upper() + "=" + str(v))
    print("PHASE176_R3R31_PUBLIC_REPORT=" + str(file))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## tests/test_installer.py

```python
"""Focused public hookup guardrails."""
from __future__ import annotations

import pytest

from phase176_r3r31_generic_hopf_public_connection.installer import (
    MARKER, NEW_LINES, proposed_code, changed_function_text,
)


def baseline():
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + MARKER + "\n"
        "        return options\n"
        "    return expand\n"
    )


def test_additive_patch_inserts_once() -> None:
    proposed = proposed_code(baseline())
    assert proposed.count("expand_generic_hopf_substitution(goal, tuple(available))") == 1
    assert MARKER in proposed
    assert "def shared_expansion_provider" in changed_function_text(proposed)


def test_patch_rejects_repeated_insertion() -> None:
    with pytest.raises(ValueError, match="ALREADY_APPLIED"):
        proposed_code(proposed_code(baseline()))


def test_patch_rejects_missing_anchor() -> None:
    with pytest.raises(ValueError, match="EXPECTED_SINGLE"):
        proposed_code("def shared_expansion_provider():\n    return None\n")


def test_patch_rejects_outside_function() -> None:
    incorrect = "def shared_expansion_provider():\n    return None\n" + MARKER + "\n"
    with pytest.raises(ValueError, match="OUTSIDE"):
        proposed_code(incorrect)


def test_patch_keeps_existing_code_unchanged() -> None:
    initial = baseline()
    result = proposed_code(initial)
    assert result.replace(NEW_LINES, "") == initial
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
try {
    if ($DryRun) {
        python -B -m phase176_r3r31_generic_hopf_public_connection.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw "R3R31 DryRun failed" }
    } else {
        python -B -m phase176_r3r31_generic_hopf_public_connection.installer
        if ($LASTEXITCODE -ne 0) { throw "R3R31 installation failed" }
        python -B -m phase176_r3r31_generic_hopf_public_connection.audit
        if ($LASTEXITCODE -ne 0) { throw "R3R31 public audit failed" }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r31_generic_hopf_public_connection\tests `
            .\phase176_r3r30_generic_hopf_substitution_isolated\tests `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw "R3R31 focused pytest failed" }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw "R3R31 git diff check failed" }
        Write-Host "PHASE176_R3R31_GATE=PASS_R3R31_FOCUSED_TESTS"
        Write-Host "PHASE176_R3R31_FULL_PYTEST=NOT_RUN"
        Write-Host "(END)"
    }
} finally {
    Pop-Location
}
```

既存 `shared_expansion_provider()` の変更後全文は本実行時に `CHANGED_FUNCTION_FULL_JA.md` に出力する。
