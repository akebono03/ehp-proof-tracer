# Phase 176 R3R7 — 追加コード全文

既存ファイルは変更しない。以下のファイルをパッケージ中に新規追加する。省略なし。

## audit.py

新規監査モジュール全文

```python
"""Phase 176 R3R7: isolated, source-screened Lemma 5.7 proof-step audit.

The normal public search is observed unchanged. The isolated derivation uses
an existing source leaf and an existing inference rule, never a fabricated GIVEN.
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
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r7_lemma57_derived_source_proof"
REVIEWED_HEAD = "a47b073f2d1f730e6037c0cb57aaee27852a5d86"
MARKER = "PHASE176_R3R7_WORKER_JSON="
REQUIRED = {
    "phase169_r10e2_unpositioned_citation/source_first.py": (
        "def screen_independent_sources_for_derived_goal(",
    ),
    "phase175_r3r9_lemma57_explicit_public/source.py": (
        "def build_explicit_lemma57_source(", "def verify_explicit_lemma57_source(",
    ),
    "phase175_r3r9_lemma57_explicit_public/rule.py": (
        "def expand_cited_lemma57_explicit_zero(",
        "def exact_lemma57_zero_image_goal(",
    ),
    "phase175_r3r6_lemma57_general/source.py": (
        "def merge_isolated_cited_source(",
    ),
    "phase169_r10e4_ordered_db_prior/db_prior.py": (
        "def admitted_db_step(", "def verified_db_step(",
    ),
    "phase176_r3r6_lemma57_source_screening_probe/audit.py": (
        "def observe(",
    ),
    "sources/toda/Toda_05_2.tex": (
        r"\label{lemma:5.7}", r"E(\eta_2\circ\nu')=0",
    ),
}


def git(*args: str, check: bool = True) -> tuple[int, str]:
    process = subprocess.run(
        ("git",) + args, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if check and process.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + ": " + process.stderr.strip())
    return process.returncode, process.stdout.strip()


def check_sources(root: Path = ROOT) -> dict[str, str]:
    hashes = {}
    for name, anchors in REQUIRED.items():
        path = root / name
        if not path.is_file():
            raise RuntimeError("SOURCE_MISSING: " + name)
        text = "".join(path.read_text(encoding="utf-8-sig").split())
        missing = [anchor for anchor in anchors if "".join(anchor.split()) not in text]
        if missing:
            raise RuntimeError("SOURCE_ANCHOR_MISSING: " + name + ": " + repr(missing))
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD", check=False)[0]:
        raise RuntimeError("R3R6_HEAD_NOT_ANCESTOR")
    if git("status", "--porcelain", "--untracked-files=no")[1]:
        raise RuntimeError("TRACKED_FILES_DIRTY")
    return {
        "head": git("rev-parse", "HEAD")[1],
        "source_sha256": check_sources(),
        "tracked_clean": True,
        "historical_guards": "FOUR_KNOWN_FAILURES_NOT_PASSING",
        "full_pytest": "NOT_RUN",
    }


def selected_source_steps(bridge: object, cls: type) -> tuple[object, ...]:
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    steps = []
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        ref = bridge.registry.reference(assertion.reference_id)
        if (
            assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and assertion.content == step.conclusion
            and type(step.conclusion) is cls
            and ref.publication_position is not None
        ):
            steps.append(step)
    return tuple(steps)


def derive_from_existing_source(expansion: object, source_step: object) -> object:
    """Use the canonical matcher and factory on one genuinely screened source."""
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    from proof import ProofRule, ProofStep, find_inference_matches_for_rule

    if not isinstance(source_step, ProofStep) or source_step.rule is not ProofRule.GIVEN:
        raise RuntimeError("SCREENED_GIVEN_REQUIRED")
    if tuple(expansion.subgoals) != (source_step.conclusion,):
        raise RuntimeError("EXACT_SOURCE_PREMISE_REQUIRED")
    matches = find_inference_matches_for_rule(expansion.rule, (source_step,))
    if len(matches) != 1:
        raise RuntimeError("EXACTLY_ONE_INFERENCE_MATCH_REQUIRED")
    inferred = derive_inference_proof_step(matches[0])
    if (
        not isinstance(inferred, ProofStep)
        or inferred.rule is not ProofRule.INFERENCE
        or inferred.conclusion != expansion.rule.conclusion_pattern
        or len(inferred.premises) != 1
        or inferred.premises[0] is not source_step
    ):
        raise RuntimeError("INVALID_INFERRED_STEP")
    return inferred


def observe() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase175_r3r6_lemma57_general.source import merge_isolated_cited_source
    from phase175_r3r9_lemma57_explicit_public.rule import (
        exact_lemma57_zero_image_goal, expand_cited_lemma57_explicit_zero,
    )
    from phase175_r3r9_lemma57_explicit_public.source import (
        TodaLemma57ExplicitNuPrimeZero, build_explicit_lemma57_source,
    )
    from proof import ProofRule, Relation

    normal = search_group_from_registered_goal(n=3, k=5)
    target = next((g for g in normal.open_goals if isinstance(g, Relation)
                   and g.lhs == TodaPrimaryGroup(8, 3)), None)
    if target is None or normal.status.value != "search_failed":
        raise RuntimeError("TARGET_PROOF_STATUS_DRIFT")
    prior = exact_prior_database_result(2, 5)
    if not isinstance(prior, Relation) or prior.lhs != TodaPrimaryGroup(7, 2):
        raise RuntimeError("PRIOR_PRESENTATION_DRIFT")
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError("PRIOR_GENERATOR_FACTORS_DRIFT")
    base_goal = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        Composition(factors[0], factors[1]), Zero(),
    )
    if not exact_lemma57_zero_image_goal(base_goal):
        raise RuntimeError("LEMMA57_BASE_GOAL_TYPE_MISMATCH")

    original = build_shared_typed_bridge()
    source = build_explicit_lemma57_source(ROOT)
    merged = merge_isolated_cited_source(original, source)
    screened = screen_independent_sources_for_derived_goal(merged, goal=target)
    actual = selected_source_steps(screened, TodaLemma57ExplicitNuPrimeZero)
    source_count = len(actual)
    if source_count != 1:
        raise RuntimeError("DERIVED_SOURCE_SCREENING_NOT_UNIQUE: " + str(source_count))
    source_step = actual[0]
    citation = getattr(getattr(source_step, "inference_rule", None), "literature_reference", None)
    if citation is None or citation.locator != "Lemma 5.7":
        raise RuntimeError("LEMMA57_CITATION_MISSING")
    options = expand_cited_lemma57_explicit_zero(
        base_goal, (source_step.conclusion,)
    )
    if len(options) != 1:
        raise RuntimeError("LEMMA57_BASE_INFERENCE_UNAVAILABLE")
    proved = derive_from_existing_source(options[0], source_step)
    if proved.conclusion != base_goal or proved.rule is not ProofRule.INFERENCE:
        raise RuntimeError("BASE_GOAL_NOT_ACTUALLY_DERIVED")
    prior_step = admitted_db_step(prior, proof_target=target, bridge=screened)
    if prior_step is None or not verified_db_step(
        prior_step, proof_target=target, bridge=screened
    ):
        raise RuntimeError("PRIOR_DB_NOT_VERIFIED")

    # Separate public-search availability from isolated proof-step existence.
    common = shared_expansion_provider(screened, proof_target=target)
    shared_options = tuple(common(base_goal))
    return {
        "target": [3, 5],
        "public_status": normal.status.value,
        "public_open_goals": len(normal.open_goals),
        "no_target_citing_id_required": True,
        "screening_mode": "INDEPENDENT_POSITIONED_SOURCE_FOR_DERIVED_GOAL",
        "lemma57_screened_source_count": source_count,
        "source_locator": citation.locator,
        "lemma57_base_candidates": len(options),
        "base_step_inferred_in_isolation": True,
        "base_step_rule": proved.rule.value,
        "base_step_premises": len(proved.premises),
        "base_step_source_rule": source_step.rule.value,
        "base_goal": repr(base_goal)[:1800],
        "shared_base_candidates_after_screening": len(shared_options),
        "shared_base_rule_names": [x.rule.name for x in shared_options[:8]],
        "prior_db_admitted": True,
        "prior_db_verified": True,
        "target_goal_installed_as_given": False,
        "source_installed_into_production": False,
        "root_proof_complete": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
    }


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    try:
        process = subprocess.run(
            (sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"),
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False, timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("WORKER_TIMEOUT") from exc
    markers = [line[len(MARKER):] for line in process.stdout.splitlines()
               if line.startswith(MARKER)]
    if process.returncode or len(markers) != 1:
        raise RuntimeError(
            "WORKER_FAILED: code=" + str(process.returncode)
            + " stderr=" + process.stderr[-4000:]
            + " stdout=" + process.stdout[-1600:]
        )
    result = json.loads(markers[0])
    if (
        result.get("base_step_inferred_in_isolation") is not True
        or result.get("root_proof_complete") is not False
        or result.get("new_given") != 0
        or result.get("source_installed_into_production") is not False
    ):
        raise RuntimeError("WORKER_FALSE_PROOF_OR_SOURCE_CLAIM")
    return result


def report_path() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    target = folder / "EHPProofTracerAudit" / PACKAGE
    target.mkdir(parents=True, exist_ok=True)
    return target / "report.json"


def execute(dry_run: bool, timeout: int) -> int:
    report = {
        "phase": "176_R3R7",
        "mode": "ISOLATED_SOURCE_SCREENED_PROOF_STEP_AUDIT",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "gate": "FAIL_R3R7",
        "full_pytest": "NOT_RUN",
        "new_given": 0,
        "new_mathematical_rules": 0,
        "root_proof_complete": False,
    }
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["observed"] = worker(timeout)
        report["gate"] = (
            "PASS_R3R7_READ_ONLY_DRYRUN" if dry_run
            else "PASS_R3R7_ISOLATED_LEMMA57_INFERENCE"
        )
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    location = report_path()
    location.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("PHASE176_R3R7_GATE=" + report["gate"])
    print("PHASE176_R3R7_REPORT=" + str(location))
    print("PHASE176_R3R7_HEAD=" + report.get("preflight", {}).get("head", "UNVERIFIED"))
    if "observed" in report:
        o = report["observed"]
        print("PHASE176_R3R7_SOURCE_COUNT=" + str(o["lemma57_screened_source_count"]))
        print("PHASE176_R3R7_BASE_STEP_INFERRED=" + str(o["base_step_inferred_in_isolation"]))
        print("PHASE176_R3R7_SHARED_BASE_PROPOSALS=" + str(o["shared_base_candidates_after_screening"]))
        print("PHASE176_R3R7_GROUP=(3,5) STATUS=" + o["public_status"]
              + " OPEN=" + str(o["public_open_goals"]))
    if "error" in report:
        print("PHASE176_R3R7_ERROR=" + report["error"])
    print("PHASE176_R3R7_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
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

## run.ps1

PowerShell 実行スクリプト全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r7_lemma57_derived_source_proof.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R7 DryRun failed' }
    } else {
        python -B -m pytest -q phase176_r3r7_lemma57_derived_source_proof/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R7 focused pytest failed' }
        python -B -m phase176_r3r7_lemma57_derived_source_proof.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R7 audit failed' }
    }
} finally {
    Pop-Location
}
```

## tests/test_audit.py

限定テスト関数・import 全文

```python
"""Focused regression tests for Phase 176 R3R7."""
from __future__ import annotations

import json

import pytest

from phase176_r3r7_lemma57_derived_source_proof import audit


def test_source_contract_matches_fixture(tmp_path) -> None:
    for name, anchors in audit.REQUIRED.items():
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("\n".join(anchors), encoding="utf-8")
    assert set(audit.check_sources(tmp_path)) == set(audit.REQUIRED)


def test_missing_source_text_rejected(tmp_path) -> None:
    for name in audit.REQUIRED:
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("unrelated", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.check_sources(tmp_path)


def test_lemma57_anchor_preserves_nu_prime() -> None:
    anchors = audit.REQUIRED["sources/toda/Toda_05_2.tex"]
    assert r"E(\eta_2\circ\nu')=0" in anchors
    assert r"\nu\'" not in "".join(anchors)


def fake_proof_modules(monkeypatch):
    import sys
    from enum import Enum
    from types import ModuleType

    class ProofRule(Enum):
        GIVEN = "given"
        INFERENCE = "inference"

    class ProofStep:
        def __init__(self, conclusion, premises, rule):
            self.conclusion = conclusion
            self.premises = premises
            self.rule = rule

    proof = ModuleType("proof")
    proof.ProofRule = ProofRule
    proof.ProofStep = ProofStep
    proof.find_inference_matches_for_rule = lambda rule, premises: ()
    factory = ModuleType("phase164_r8_proofstep_factory")
    factory.derive_inference_proof_step = lambda match: None
    monkeypatch.setitem(sys.modules, "proof", proof)
    monkeypatch.setitem(sys.modules, "phase164_r8_proofstep_factory", factory)
    return ProofRule, ProofStep


def test_derived_step_rejects_nonproof_source(monkeypatch) -> None:
    fake_proof_modules(monkeypatch)

    class Expansion:
        subgoals = ("cited",)

    with pytest.raises(RuntimeError, match="SCREENED_GIVEN_REQUIRED"):
        audit.derive_from_existing_source(Expansion(), "cited")


def test_derived_step_rejects_unrelated_source(monkeypatch) -> None:
    ProofRule, ProofStep = fake_proof_modules(monkeypatch)

    class Expansion:
        subgoals = ("correct",)

    with pytest.raises(RuntimeError, match="EXACT_SOURCE_PREMISE_REQUIRED"):
        audit.derive_from_existing_source(
            Expansion(), ProofStep("wrong", (), ProofRule.GIVEN)
        )


def test_worker_rejects_false_completion(monkeypatch) -> None:
    class Completed:
        returncode = 0
        stdout = audit.MARKER + json.dumps({
            "base_step_inferred_in_isolation": True,
            "root_proof_complete": True,
            "new_given": 0,
            "source_installed_into_production": False,
        }) + "\n"
        stderr = ""

    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: Completed())
    with pytest.raises(RuntimeError, match="WORKER_FALSE_PROOF_OR_SOURCE_CLAIM"):
        audit.worker(5)


def test_dry_run_does_not_call_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "fixture"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker launched"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 0
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text())
    assert report["gate"] == "PASS_R3R7_READ_ONLY_DRYRUN"
    assert report["new_given"] == 0
    assert report["root_proof_complete"] is False
    assert report["full_pytest"] == "NOT_RUN"
```

## __init__.py

パッケージ定義全文

```python
"""Phase 176 R3R7 isolated source-screened proof audit."""
```

## tests/__init__.py

テストパッケージ定義全文

```python
"""Focused audit tests."""
```

