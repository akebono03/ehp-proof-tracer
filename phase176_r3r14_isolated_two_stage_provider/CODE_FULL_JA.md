# Phase 176 R3R14 変更コード全文

既存ファイルは変更しない。以下は新規ディレクトリ直下と `tests/` 配下への追加ファイル全文。省略なし。

## `__init__.py`（新規追加）

```python
"""Phase 176 R3R14: isolated two-stage provider evaluation."""

```

## `provider.py`（新規追加）

```python
"""Compose existing screened Lemma 5.7 and typed right-zero rules in isolation.

This callable is NOT registered in the shared production proof search.
It generates candidate goals, never completed steps or GIVEN statements.
"""
from __future__ import annotations

from typing import Callable

from expression import Composition, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
from phase175_r3r9_lemma57_explicit_public.rule import expand_cited_lemma57_explicit_zero
from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
from phase176_r3r8_lemma57_provider_binding.audit import source_bound_provider
from phase176_r3r10_right_zero_transport_isolated.rule import expand_right_zero_transport


def preceding_zero_image(goal: object) -> GeneratorImage | None:
    """Construct exactly one typed prefix zero-image obligation, when valid."""
    if (type(goal) is not GeneratorImage
            or type(goal.map) is not TodaSuspensionMap
            or type(goal.target_generator) is not Zero):
        return None
    factors = typed_composition_factors(goal.source_generator)
    if factors is None or len(factors) < 3:
        return None
    prefix = factors[0]
    for factor in factors[1:-1]:
        prefix = Composition(prefix, factor)
    from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
    ends = expression_endpoints(prefix)
    if ends is None:
        return None
    degree, sphere = ends
    if sphere != goal.map.source_group.sphere_dimension:
        return None
    return GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(degree, sphere),
                          TodaPrimaryGroup(degree + 1, sphere + 1)),
        prefix, Zero(),
    )


def build_isolated_two_stage_provider(
    ordinary: Callable[[object], object],
    screened_source_steps: tuple[object, ...],
) -> Callable[[object], tuple[object, ...]]:
    """Retain ordinary options and independently guarded inferred subgoals."""
    bound = source_bound_provider(
        ordinary,
        screened_source_steps,
        TodaLemma57ExplicitNuPrimeZero,
        expand_cited_lemma57_explicit_zero,
    )

    def expand(goal: object) -> tuple[object, ...]:
        options = tuple(bound(goal))
        base = preceding_zero_image(goal)
        if base is None:
            return options
        return tuple(expand_right_zero_transport(goal, base)) + options

    return expand

```

## `audit.py`（新規追加）

```python
"""Source-first, read-only R3R14 two-stage provider composition audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r14_isolated_two_stage_provider"
REVIEWED_HEAD = "51855066237e710c6715250478f9a731bc1c087f"
MARKER = "PHASE176_R3R14_WORKER_JSON="


def git(*args: str) -> str:
    process = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                             text=True, encoding="utf-8", errors="replace")
    if process.returncode:
        raise RuntimeError("GIT_ERROR " + str(args) + " " + process.stderr[-900:])
    return process.stdout.strip()


def preflight() -> dict:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    ancestor = subprocess.run(("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD"), cwd=ROOT)
    if ancestor.returncode:
        raise RuntimeError("REVIEWED_HEAD_NOT_ANCESTOR")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("TRACKED_FILES_DIRTY")
    required = {
        "phase176_r3r10_right_zero_transport_isolated/rule.py": "def expand_right_zero_transport(",
        "phase176_r3r8_lemma57_provider_binding/audit.py": "def source_bound_provider(",
        "phase175_r3r9_lemma57_explicit_public/rule.py": "def expand_cited_lemma57_explicit_zero(",
        "phase165_r52_r9_shared_math.py": "def shared_expansion_provider(",
        "sources/toda/Toda_05_2.tex": r"E(\eta_2\circ\nu')=0",
    }
    for filename, anchor in required.items():
        file = ROOT / filename
        if not file.is_file() or "".join(anchor.split()) not in "".join(file.read_text(encoding="utf-8-sig").split()):
            raise RuntimeError("SOURCE_MISSING_OR_CHANGED " + filename)
    return {"head": git("rev-parse", "HEAD"), "source_anchors": len(required)}


def observe() -> dict:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase175_r3r6_lemma57_general.source import merge_isolated_cited_source
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero, build_explicit_lemma57_source
    from phase176_r3r7_lemma57_derived_source_proof.audit import selected_source_steps, derive_from_existing_source
    from phase176_r3r14_isolated_two_stage_provider.provider import build_isolated_two_stage_provider, preceding_zero_image
    from phase176_r3r10_right_zero_transport_isolated.rule import RULE_NAME as RIGHT_RULE_NAME
    from proof import Relation, ProofRule, find_inference_matches_for_rule
    from phase164_r8_proofstep_factory import derive_inference_proof_step

    public = search_group_from_registered_goal(n=3, k=5)
    if public.status.value != "search_failed" or len(public.open_goals) != 3:
        raise RuntimeError("PUBLIC_FRONTIER_DRIFT")
    target = next((x for x in public.open_goals if type(x) is Relation
                   and x.lhs == TodaPrimaryGroup(8, 3)), None)
    if target is None:
        raise RuntimeError("TARGET_MISSING")
    prior = exact_prior_database_result(2, 5)
    if type(prior) is not Relation or prior.lhs != TodaPrimaryGroup(7, 2):
        raise RuntimeError("PRIOR_DRIFT")
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError("FACTORIZATION_DRIFT")
    whole = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        prior.rhs.generator, Zero(),
    )
    base = preceding_zero_image(whole)
    expected_base = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        Composition(factors[0], factors[1]), Zero(),
    )
    if base != expected_base:
        raise RuntimeError("PREFIX_NOT_EXACT")
    merged = merge_isolated_cited_source(
        build_shared_typed_bridge(), build_explicit_lemma57_source(ROOT))
    screened = screen_independent_sources_for_derived_goal(merged, goal=target)
    steps = selected_source_steps(screened, TodaLemma57ExplicitNuPrimeZero)
    if len(steps) != 1 or steps[0].rule is not ProofRule.GIVEN:
        raise RuntimeError("CITED_SOURCE_BOUNDARY")
    ordinary = shared_expansion_provider(screened, proof_target=target)
    isolated = build_isolated_two_stage_provider(ordinary, steps)
    root_options = tuple(isolated(target))
    base_options = tuple(isolated(base))
    whole_options = tuple(isolated(whole))
    cited_name = "extract explicit nu-prime zero-suspension clause of Toda Lemma 5.7"
    citations = [o for o in base_options if o.rule.name == cited_name]
    right = [o for o in whole_options if o.rule.name == RIGHT_RULE_NAME]
    if len(citations) != 1 or len(right) != 1 or right[0].subgoals != (base,):
        raise RuntimeError("TWO_STAGE_CANDIDATES_NOT_CONNECTED")
    base_step = derive_from_existing_source(citations[0], steps[0])
    if base_step.rule is not ProofRule.INFERENCE or base_step.conclusion != base:
        raise RuntimeError("INVALID_BASE_PROOF")
    matches = tuple(find_inference_matches_for_rule(right[0].rule, (base_step,)))
    if len(matches) != 1:
        raise RuntimeError("RIGHT_RULE_MATCH_FAILED")
    whole_step = derive_inference_proof_step(matches[0])
    if (whole_step.rule is not ProofRule.INFERENCE or whole_step.conclusion != whole
            or whole_step.premises != (base_step,)):
        raise RuntimeError("INVALID_PROOF_ANCESTRY")
    if root_options != tuple(ordinary(target)):
        raise RuntimeError("ROOT_OPTIONS_CHANGED")
    if tuple(ordinary(base)) or tuple(ordinary(whole)):
        raise RuntimeError("PUBLIC_FRONTIER_CHANGED")
    return {
        "screened_source_steps": len(steps),
        "base_ordinary_candidates": len(tuple(ordinary(base))),
        "base_isolated_cited_candidates": len(citations),
        "whole_ordinary_candidates": len(tuple(ordinary(whole))),
        "whole_isolated_right_candidates": len(right),
        "verified_nested_inference_steps": 2,
        "root_options_unchanged": True,
        "root_proof_complete": False,
        "production_modified": False,
        "new_given": 0,
        "public_mathematical_rules_added": 0,
        "full_pytest": "NOT_RUN",
    }


def report_path() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "report.json"


def execute(dry_run: bool, timeout: int) -> int:
    report = {"phase": "176_R3R14", "dry_run": dry_run,
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "gate": "FAIL_R3R14", "root_proof_complete": False,
              "new_given": 0, "public_mathematical_rules_added": 0,
              "full_pytest": "NOT_RUN"}
    try:
        report["preflight"] = preflight()
        if not dry_run:
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
            process = subprocess.run(
                (sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"),
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                errors="replace", env=env, timeout=timeout,
            )
            matches = [line[len(MARKER):] for line in process.stdout.splitlines()
                       if line.startswith(MARKER)]
            if process.returncode or len(matches) != 1:
                raise RuntimeError("WORKER_FAILED " + str(process.returncode) + " " + process.stderr[-4000:])
            report["observed"] = json.loads(matches[0])
            if (report["observed"].get("root_proof_complete") is not False
                    or report["observed"].get("verified_nested_inference_steps") != 2):
                raise RuntimeError("FALSE_INFERENCE_CLAIM")
        report["gate"] = "PASS_R3R14_READ_ONLY_DRYRUN" if dry_run else "PASS_R3R14_ISOLATED_TWO_STAGE_PROVIDER"
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
        report["traceback"] = traceback.format_exc()[-6000:]
    path = report_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R14_GATE=" + report["gate"])
    print("PHASE176_R3R14_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE176_R3R14_REPORT=" + str(path))
    if "observed" in report:
        for key, value in report["observed"].items():
            print("PHASE176_R3R14_" + key.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R14_ERROR=" + report["error"])
    print("PHASE176_R3R14_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return execute(args.dry_run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/test_provider.py`（新規追加）

```python
"""Minimal typed contracts for the isolated two-stage backward provider."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase176_r3r14_isolated_two_stage_provider.provider import preceding_zero_image
from phase176_r3r10_right_zero_transport_isolated.rule import right_zero_transport_inputs


def fixture():
    a = HomotopyElement("a", dimension=2, source=3, target=2)
    b = HomotopyElement("b", dimension=3, source=6, target=3)
    c = HomotopyElement("c", dimension=6, source=7, target=6)
    goal = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        Composition(a, Composition(b, c)), Zero(),
    )
    return goal


def test_generic_prefix_has_correct_typed_zero_image():
    goal = fixture()
    base = preceding_zero_image(goal)
    assert base is not None
    assert right_zero_transport_inputs(goal, base) == (base,)


def test_nonzero_target_rejected():
    goal = fixture()
    assert preceding_zero_image(replace(goal, target_generator=goal.source_generator)) is None


def test_two_factor_goal_rejected():
    goal = fixture()
    assert preceding_zero_image(replace(goal, source_generator=goal.source_generator.right)) is None


def test_no_candidate_for_non_generator_image():
    assert preceding_zero_image("untyped") is None

```

## `tests/test_audit.py`（新規追加）

```python
"""Focused fail-closed audit and dry-run contracts."""
from __future__ import annotations

import json

import pytest

from phase176_r3r14_isolated_two_stage_provider import audit


def test_dry_run_does_not_launch_worker(monkeypatch, tmp_path):
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "fixture", "source_anchors": 5})
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 0
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "PASS_R3R14_READ_ONLY_DRYRUN"
    assert "observed" not in report
    assert report["root_proof_complete"] is False


def test_failed_preflight_does_not_claim_success(monkeypatch, tmp_path):
    def fail():
        raise RuntimeError("GUARD_FAILED")
    monkeypatch.setattr(audit, "preflight", fail)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 1
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "FAIL_R3R14"
    assert "GUARD_FAILED" in report["error"]

```

## `run.ps1`（新規追加）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r14_isolated_two_stage_provider.audit --dry-run
        exit $LASTEXITCODE
    }
    python -B -m phase176_r3r14_isolated_two_stage_provider.audit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m pytest -q -p no:cacheprovider `
        phase176_r3r14_isolated_two_stage_provider/tests/test_provider.py `
        phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py `
        phase175_r3r9_lemma57_explicit_public/tests/test_rule.py
    exit $LASTEXITCODE
} finally {
    Pop-Location
}

```
