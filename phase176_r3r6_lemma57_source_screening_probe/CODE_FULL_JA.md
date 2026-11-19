# Phase 176 R3R6 — 追加コード全文

変更対象は新規ディレクトリのみ。既存コードは変更しない。新規関数は各ファイルの以下の定義位置へ追加。

## audit.py

```python
"""Phase 176 R3R6: read-only Lemma 5.7 source-screening and source-first bridge probe.

This package never installs a source, registers a proof, or edits production code.
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
PACKAGE = "phase176_r3r6_lemma57_source_screening_probe"
REVIEWED_HEAD = "3a4d1351c9aad5f472c2bac3aa464f8796b2edf2"
MARKER = "PHASE176_R3R6_WORKER_JSON="
REQUIRED = {
    "phase175_r3r9_lemma57_explicit_public/source.py": (
        "def build_explicit_lemma57_source(",
        "def verify_explicit_lemma57_source(",
    ),
    "phase175_r3r9_lemma57_explicit_public/rule.py": (
        "def exact_lemma57_zero_image_goal(",
        "def expand_cited_lemma57_explicit_zero(",
    ),
    "phase175_r3r6_lemma57_general/source.py": (
        "def merge_isolated_cited_source(",
    ),
    "phase165_r52_r16_web_citation_gate.py": (
        "def screen_shared_proof_context(",
    ),
    "phase166_r3t_goal_source_binding/goal_source.py": (
        "def resolve_specialized_goal_citing_id(",
    ),
    "phase176_r3r5_lemma57_right_composition_frontier/audit.py": (
        "def observe(",
    ),
    "sources/toda/Toda_05_2.tex": (
        r"\label{lemma:5.7}",
        r"E(\eta_2\circ\nu')=0",
    ),
}


def git(*args: str, check: bool = True) -> tuple[int, str]:
    result = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                            encoding="utf-8", text=True, errors="replace", check=False)
    if check and result.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + ": " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def source_contract(root: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for name, anchors in REQUIRED.items():
        file = root / name
        if not file.is_file():
            raise RuntimeError("REQUIRED_SOURCE_MISSING: " + name)
        contents = "".join(file.read_text(encoding="utf-8-sig").split())
        missing = [a for a in anchors if "".join(a.split()) not in contents]
        if missing:
            raise RuntimeError("SOURCE_ANCHORS_MISSING: " + name + ": " + repr(missing))
        found[name] = hashlib.sha256(file.read_bytes()).hexdigest()
    return found


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    if git("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD", check=False)[0] != 0:
        raise RuntimeError("R3R5_REVIEWED_HEAD_NOT_ANCESTOR")
    if git("status", "--porcelain", "--untracked-files=no")[1]:
        raise RuntimeError("TRACKED_WORKTREE_DIRTY")
    return {"head": git("rev-parse", "HEAD")[1], "tracked_clean": True,
            "source_hashes": source_contract(ROOT), "full_pytest": "NOT_RUN",
            "legacy_source_guards": "FOUR_KNOWN_FAILURES_NOT_PASSING"}


def eligible_source_steps(bridge: object, cls: type) -> tuple[object, ...]:
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    matched = []
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and assertion.content == step.conclusion
                and type(step.conclusion) is cls):
            matched.append(step)
    return tuple(matched)


def option_details(options: tuple[object, ...]) -> dict[str, object]:
    return {"count": len(options), "status": "UNVERIFIED_PROPOSALS",
            "options": [{"rule": getattr(option.rule, "name", None),
                         "subgoals": [repr(s)[:900] for s in option.subgoals]}
                        for option in options[:8]]}


def observe() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase175_r3r6_lemma57_general.source import merge_isolated_cited_source
    from phase175_r3r9_lemma57_explicit_public.rule import (
        exact_lemma57_zero_image_goal, expand_cited_lemma57_explicit_zero,
    )
    from phase175_r3r9_lemma57_explicit_public.source import (
        ASSERTION_ID, TodaLemma57ExplicitNuPrimeZero, build_explicit_lemma57_source,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from proof import Relation

    result = search_group_from_registered_goal(n=3, k=5)
    prior = exact_prior_database_result(2, 5)
    if not isinstance(prior, Relation) or prior.lhs != TodaPrimaryGroup(7, 2):
        raise RuntimeError("PRECEDING_GROUP_PRESENTATION_DRIFT")
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError("PRECEDING_GENERATOR_THREE_FACTORS_REQUIRED")
    first_two = Composition(factors[0], factors[1])
    base_map = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    base_goal = GeneratorImage(base_map, first_two, Zero())
    if not exact_lemma57_zero_image_goal(base_goal):
        raise RuntimeError("LEMMA57_TYPED_BASE_GOAL_DRIFT")
    bridge = build_shared_typed_bridge()
    selected = [g for g in result.open_goals if isinstance(g, Relation)]
    if not selected:
        raise RuntimeError("NO_REGISTERED_RELATION_GOAL")
    target = next((g for g in selected if g.lhs == TodaPrimaryGroup(8, 3)), None)
    if target is None:
        raise RuntimeError("TARGET_GOAL_NOT_FOUND")
    citing = resolve_specialized_goal_citing_id(bridge, target)
    extra = build_explicit_lemma57_source(ROOT)
    combined = merge_isolated_cited_source(bridge, extra)
    original = eligible_source_steps(bridge, TodaLemma57ExplicitNuPrimeZero)
    merged = eligible_source_steps(combined, TodaLemma57ExplicitNuPrimeZero)
    screened_rows: dict[str, object] = {"status": "NO_TARGET_CITING_ID", "source_count": None}
    if citing is not None:
        screened = screen_shared_proof_context(
            combined, goal=target, citing_assertion_id=citing,
            explicit_publication_target=True,
        )
        accepted = eligible_source_steps(screened, TodaLemma57ExplicitNuPrimeZero)
        screened_rows = {"status": "SCREENED", "source_count": len(accepted),
                         "source_assertion_ids": [link.assertion_id for link in screened.proof_links
                                                  if link.step in accepted]}
    prior_admitted = admitted_db_step(prior, proof_target=target, bridge=bridge)
    result_data: dict[str, object] = {
        "search_status": result.status.value,
        "open_goals": len(result.open_goals),
        "lemma57_source_default_count": len(original),
        "lemma57_isolated_registered_count": len(eligible_source_steps(extra, TodaLemma57ExplicitNuPrimeZero)),
        "lemma57_merged_count": len(merged),
        "lemma57_extra_assertion_id": ASSERTION_ID,
        "target_citation_id": citing,
        "screened": screened_rows,
        "base_goal": repr(base_goal),
        "base_direct_match": True,
        "base_candidate_default": option_details(expand_cited_lemma57_explicit_zero(base_goal, tuple(s.conclusion for s in original))),
        "base_candidate_merged": option_details(expand_cited_lemma57_explicit_zero(base_goal, tuple(s.conclusion for s in merged))),
        "prior_db_admitted": prior_admitted is not None,
        "prior_db_verified": (verified_db_step(prior_admitted, proof_target=target, bridge=bridge)
                              if prior_admitted is not None else False),
        "composed_generator_requires_right_composition": True,
        "source_installed_into_production": False,
        "any_proof_claimed": False,
        "new_given": 0, "new_rules": 0,
    }
    return result_data


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    try:
        p = subprocess.run((sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"),
                           cwd=ROOT, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired as e:
        raise RuntimeError("R3R6_WORKER_TIMEOUT") from e
    matches = [x[len(MARKER):] for x in p.stdout.splitlines() if x.startswith(MARKER)]
    if p.returncode or len(matches) != 1:
        raise RuntimeError("R3R6_WORKER_ERROR: code=" + str(p.returncode)
                           + " stderr=" + p.stderr[-4000:])
    data = json.loads(matches[0])
    if data.get("new_given") != 0 or data.get("any_proof_claimed") is not False:
        raise RuntimeError("AUDIT_MUST_NOT_CLAIM_PROOF")
    return data


def report_path() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = root / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "report.json"


def execute(dry_run: bool, timeout: int) -> int:
    report: dict[str, object] = {
        "phase": "176_R3R6", "dry_run": dry_run,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "FAIL_R3R6", "full_pytest": "NOT_RUN",
        "source_first": True, "new_given": 0, "new_rules": 0,
    }
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["observed"] = worker(timeout)
        report["gate"] = "PASS_R3R6_READ_ONLY_DRYRUN" if dry_run else "PASS_R3R6_SOURCE_SCREENING_FRONTIER"
    except Exception as e:
        report["error"] = type(e).__name__ + ": " + str(e)
        report["traceback"] = traceback.format_exc()[-7000:]
    target = report_path()
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R6_GATE=" + report["gate"])
    print("PHASE176_R3R6_REPORT=" + str(target))
    print("PHASE176_R3R6_HEAD=" + report.get("preflight", {}).get("head", "UNVERIFIED"))
    if "observed" in report:
        x = report["observed"]
        for name in ("search_status", "open_goals", "lemma57_source_default_count", "lemma57_merged_count", "prior_db_admitted", "prior_db_verified"):
            print("PHASE176_R3R6_" + name.upper() + "=" + str(x[name]))
        print("PHASE176_R3R6_SCREENED=" + str(x["screened"]["status"]))
        print("PHASE176_R3R6_BASE_CANDIDATES=" + str(x["base_candidate_merged"]["count"]))
    if "error" in report:
        print("PHASE176_R3R6_ERROR=" + report["error"])
    print("PHASE176_R3R6_FULL_PYTEST=NOT_RUN")
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

## tests/test_audit.py

```python
"""R3R6 read-only source audit regression tests."""
from __future__ import annotations

import json

import pytest

from phase176_r3r6_lemma57_source_screening_probe import audit


def test_source_contract_accepts_fixture(tmp_path) -> None:
    for name, anchors in audit.REQUIRED.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(anchors), encoding="utf-8")
    assert set(audit.source_contract(tmp_path)) == set(audit.REQUIRED)


def test_missing_source_anchor_fails_closed(tmp_path) -> None:
    for name in audit.REQUIRED:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("unrelated", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_ANCHORS_MISSING"):
        audit.source_contract(tmp_path)


def test_expansion_is_not_proof() -> None:
    class Rule:
        name = "fixture rule"

    class Expansion:
        rule = Rule()
        subgoals = ("still open",)

    summary = audit.option_details((Expansion(),))
    assert summary["count"] == 1
    assert summary["status"] == "UNVERIFIED_PROPOSALS"
    assert summary["options"][0]["subgoals"] == ["'still open'"]


def test_empty_expansion_is_distinguished() -> None:
    assert audit.option_details(())["count"] == 0


def test_worker_rejects_false_proof_claim(monkeypatch) -> None:
    import subprocess

    class Process:
        returncode = 0
        stdout = audit.MARKER + json.dumps({"new_given": 0, "any_proof_claimed": True})
        stderr = ""

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: Process())
    with pytest.raises(RuntimeError, match="AUDIT_MUST_NOT_CLAIM_PROOF"):
        audit.worker(5)


def test_dry_run_has_no_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "test"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker must not run"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 0
    path = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["full_pytest"] == "NOT_RUN"
    assert report["new_given"] == 0

```

## run.ps1

```powershell
param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 120
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r6_lemma57_source_screening_probe.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R6 DryRun failed' }
    } else {
        & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r3r6_lemma57_source_screening_probe/tests
        if ($LASTEXITCODE -ne 0) { throw 'R3R6 focused pytest failed' }
        & python -B -m phase176_r3r6_lemma57_source_screening_probe.audit --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'R3R6 source audit failed' }
    }
} finally {
    Pop-Location
}

```

## __init__.py

```python

```

## tests/__init__.py

```python

```

