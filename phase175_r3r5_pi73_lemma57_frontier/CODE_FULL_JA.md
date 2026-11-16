# Phase 175 R3R5 — 新規コード・テスト全文

既存の import・クラス・関数は変更しない。すべて新規ディレクトリ `phase175_r3r5_pi73_lemma57_frontier/` に追加する。各コードブロックはファイル全体で、省略なし。

## `__init__.py`

```python
"""Read-only Phase 175 R3R5 EHP injectivity and Toda Lemma 5.7 frontier."""
```

## `source.py`

```python
"""Read-only verification of the printed Toda Lemma 5.7, before Proposition 5.8.

The TeX text is evidence for a source statement, not a verified ProofStep.
"""
from __future__ import annotations

from hashlib import sha1
from pathlib import Path
import subprocess

SOURCE_PATH = "sources/toda/Toda_05_2.tex"
SOURCE_BLOB = "579661138928499ba04a51327f686d9b971b5314"
LEMMA_START = r"\begin{lemma}\label{lemma:5.7}"
LEMMA_END = r"\end{lemma}"
PROPOSITION_START = r"\begin{proposition}\label{prop:5.8}"


def source_clause_positions(source: str) -> dict[str, int]:
    """Require the exact Lemma 5.7 hypotheses and particular consequence."""
    if not isinstance(source, str):
        raise TypeError("source must be a str")
    if source.count(LEMMA_START) != 1 or source.count(PROPOSITION_START) != 1:
        raise ValueError("Toda Lemma 5.7 / Proposition 5.8 source anchor is not unique")
    start = source.index(LEMMA_START)
    if source.count(LEMMA_END, start, source.index(PROPOSITION_START)) != 1:
        raise ValueError("Toda Lemma 5.7 not closed before Proposition 5.8")
    end = source.index(LEMMA_END, start) + len(LEMMA_END)
    proposition = source.index(PROPOSITION_START)
    if not start < end < proposition:
        raise ValueError("Toda Lemma 5.7 must precede Proposition 5.8")
    lemma = source[start:end]
    for clause in (
        r"\alpha\in\pi_i(S^3)",
        r"E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5)",
        r"E(\eta_2\circ\alpha)=0",
        r"E(\eta_2\circ\nu')=0",
    ):
        if lemma.count(clause) != 1:
            raise ValueError("Missing or duplicated Lemma 5.7 clause: " + clause)
    between = source[end:proposition]
    for fragment in (
        r"E^2\nu'=2\nu_5",
        r"\pi^{2}_{6}=\Delta(\pi^{5}_{8})",
        r"E\pi_6^2=\gen{E(\eta_2\circ\nu')}=0",
    ):
        if fragment not in between:
            raise ValueError("Missing prerequisite argument following Lemma 5.7: " + fragment)
    return {
        "lemma_start": start,
        "lemma_end": end,
        "proposition_58_start": proposition,
        "general_conditional_count": 1,
        "particular_consequence_count": 1,
    }


def verify_reviewed_toda_source(root: Path) -> dict[str, object]:
    """Pin the committed blob; reject semantic changes in the checked-out file."""
    root = Path(root)
    path = root / SOURCE_PATH
    if not path.is_file():
        raise RuntimeError("R3R5_TODA_SOURCE_MISSING")
    actual = subprocess.run(
        ["git", "rev-parse", "HEAD:" + SOURCE_PATH],
        cwd=root, capture_output=True, text=True, check=True,
    ).stdout.strip()
    if actual != SOURCE_BLOB:
        raise RuntimeError("R3R5_TODA_SOURCE_PIN_CHANGED")
    raw = path.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n")
    candidates = (raw, normalized, normalized.replace(b"\n", b"\r\n"))
    def blob(data: bytes) -> str:
        return sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if not any(blob(data) == SOURCE_BLOB for data in candidates):
        raise RuntimeError("R3R5_TODA_WORKTREE_SOURCE_CHANGED")
    source = normalized.decode("utf-8-sig")
    clauses = source_clause_positions(source)
    return {
        "source_path": SOURCE_PATH,
        "source_blob": actual,
        "locator": "Lemma 5.7",
        "original_print_independently_verified": False,
        "direct_given_added": False,
        **clauses,
    }
```

## `frontier.py`

```python
"""Observe the EHP E-H proof prerequisites for pi_7^3 without new GIVENs."""
from __future__ import annotations

from expression import Zero
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from map_property_rules import ImageZeroStatement
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase170_r3_r6_prop58_source import _source_checked_pi73_relation
from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
    expand_hopf_injective_from_zero_image, hopf_injectivity_from_zero_image_inputs,
)
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase175_r3_pi73_hopf_lift.frontier import inspect_independent_obligation
from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def inspect_ehp_injectivity_frontier() -> dict[str, object]:
    """Locate the first missing E-image proof, using actual canonical searches."""
    bridge = build_shared_typed_bridge()
    target = exact_prior_database_result(3, 4)
    if (not isinstance(target, Relation)
            or target.lhs != TodaPrimaryGroup(7, 3)
            or not isinstance(target.rhs, FiniteCyclicGroup)
            or target.rhs.order != 2
            or _source_checked_pi73_relation(bridge) != target):
        raise RuntimeError("R3R5_PI73_TYPED_TARGET_CHANGED")
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if not isinstance(citing, str) or not citing:
        raise RuntimeError("R3R5_CITING_ASSERTION_MISSING")
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    if target in available:
        raise RuntimeError("R3R5_TARGET_GIVEN_FORBIDDEN")
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    lifts = expand_cited_hopf_lift(cyclic, available)
    if len(lifts) != 1:
        raise RuntimeError("R3R5_EXPECT_ONE_REVIEWED_HOPF_LIFT")
    injectivity = lifts[0].subgoals[0]
    if not isinstance(injectivity, MapInjective):
        raise RuntimeError("R3R5_EXPECT_TYPED_HOPF_INJECTIVITY")
    inputs = hopf_injectivity_from_zero_image_inputs(injectivity)
    if inputs is None or len(expand_hopf_injective_from_zero_image(injectivity)) != 1:
        raise RuntimeError("R3R5_EHP_INJECTIVITY_RULE_CHANGED")
    zero_image, exactness = inputs
    if not isinstance(zero_image, ImageZeroStatement):
        raise RuntimeError("R3R5_EXPECT_TYPED_ZERO_IMAGE")
    prior = exact_prior_database_result(2, 4)
    if (not isinstance(prior, Relation)
            or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != TodaPrimaryGroup(6, 2)
            or not isinstance(prior.rhs, FiniteCyclicGroup)
            or prior.rhs.order != 4):
        raise RuntimeError("R3R5_PRIOR_PI62_CYCLIC_GOAL_UNAVAILABLE")
    bridge_options = expand_zero_image_from_cyclic_generator(zero_image, prior)
    if len(bridge_options) != 1:
        raise RuntimeError("R3R5_EXISTING_CYCLIC_ZERO_IMAGE_RULE_UNAVAILABLE")
    generator_goal = bridge_options[0].subgoals[1]
    if (bridge_options[0].subgoals[0] != prior
            or not isinstance(generator_goal, GeneratorImage)
            or generator_goal.map != zero_image.map
            or generator_goal.source_generator != prior.rhs.generator
            or not isinstance(generator_goal.target_generator, Zero)):
        raise RuntimeError("R3R5_ZERO_GENERATOR_IMAGE_NOT_TYPED")
    ordinary = shared_expansion_provider(screened, proof_target=target)

    def scoped(goal: object):
        if goal == zero_image:
            return bridge_options + ordinary(goal)
        return ordinary(goal)

    questions = (
        ("ehp_exactness", exactness, ordinary),
        ("lower_pi62_group", prior, ordinary),
        ("zero_generator_image", generator_goal, ordinary),
        ("zero_suspension_image", zero_image, scoped),
        ("hopf_injectivity", injectivity, scoped),
    )
    records = [
        inspect_independent_obligation(name, goal, screened, citing, provider)
        for name, goal, provider in questions
    ]
    return {
        "target": repr(target),
        "earlier_screened_givens": len(available),
        "target_direct_given_excluded": True,
        "hopf_lift_proposals": len(lifts),
        "zero_image_generic_bridge_candidates": len(bridge_options),
        "zero_image_ordinarily_offered_routes": len(ordinary(zero_image)),
        "source_lemma57_new_given": False,
        "new_mathematical_rules": 0,
        "production_modified": False,
        "obligations": records,
    }
```

## `audit.py`

```python
"""Phase 175 R3R5: source-first read-only pi7^3 EHP injectivity frontier."""
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

from phase175_r3r5_pi73_lemma57_frontier.source import verify_reviewed_toda_source

PACKAGE = "phase175_r3r5_pi73_lemma57_frontier"
MARKER = "__PHASE175_R3R5_WORKER__="


def latest_verified_r3_report() -> Path:
    """Require actual R3R4 successful normal-run evidence, never DryRun data."""
    local = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = local / "EHPProofTracerAudit" / "phase175_r3_pi73_hopf_lift"
    for path in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
            result = report.get("worker", {}).get("data", {})
            rows = result.get("subgoal_observations", [])
            statuses = {item["name"]: item["status"] for item in rows}
            if (
                report.get("phase") == "175-R3"
                and report.get("dry_run") is False
                and report.get("result") == "PASS_R3_PI73_HOPF_FRONTIER_RECORDED"
                and report.get("tracked_unchanged") is True
                and report.get("new_given") == 0
                and result.get("target_direct_given_excluded") is True
                and result.get("hopf_lift_candidate_count") == 1
                and statuses.get("hopf_injectivity") == "UNRESOLVED"
                and statuses.get("cyclic_codomain") == "INFERRED"
                and statuses.get("hopf_generator_image") == "INFERRED"
                and statuses.get("source_bound_cyclic_codomain") == "INFERRED"
            ):
                return path
        except (ValueError, OSError, TypeError, KeyError, UnicodeError):
            continue
    raise RuntimeError("R3R5_NO_VERIFIED_R3R4_NORMAL_REPORT")


def scoped_preflight(root: Path) -> dict[str, object]:
    """Reuse the exact R3R4 reviewed source, worktree, R2 lineage guards."""
    from phase175_r3_pi73_hopf_lift import audit as r3

    checked = r3.preflight(root)
    r2_path = r3.select_r2_report(None)
    previous = json.loads(r2_path.read_text(encoding="utf-8"))
    r3.validate_r2(previous)
    lineage = r3.verify_lineage(root, previous, checked)
    source = verify_reviewed_toda_source(root)
    return {
        "r3_source_guard": checked,
        "r2_lineage": lineage,
        "r2_report_path": str(r2_path),
        "toda_lemma57_source": source,
    }


def worker() -> int:
    """Run independent typed searches without inserting any theorem facts."""
    try:
        from phase175_r3r5_pi73_lemma57_frontier.frontier import inspect_ehp_injectivity_frontier
        payload = {"status": "INSPECTED", "data": inspect_ehp_injectivity_frontier()}
    except Exception as exc:
        payload = {
            "status": "WORKER_ERROR",
            "error": type(exc).__name__ + ": " + str(exc),
            "traceback": traceback.format_exc()[-6000:],
        }
    print(MARKER + json.dumps(payload, ensure_ascii=False), flush=True)
    return 0


def launch_worker(root: Path, seconds: int, folder: Path) -> dict[str, object]:
    """Bound long recursive proof search; preserve its diagnostics."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker", "--root", str(root)],
            cwd=root, env=env, capture_output=True,
            text=True, encoding="utf-8", errors="replace",
            timeout=seconds, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        output = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        (folder / "worker.log").write_text(output, encoding="utf-8")
        return {"status": "TIMEOUT", "seconds": seconds}
    (folder / "worker.log").write_text(
        result.stdout + "\nSTDERR:\n" + result.stderr, encoding="utf-8",
    )
    lines = [line[len(MARKER):] for line in result.stdout.splitlines() if line.startswith(MARKER)]
    if result.returncode or len(lines) != 1:
        return {"status": "INVALID_WORKER", "return_code": result.returncode, "markers": len(lines)}
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_JSON"}
    return payload if isinstance(payload, dict) else {"status": "INVALID_PAYLOAD"}


def write_report(folder: Path, report: dict[str, object]) -> None:
    """Persist evidence outside the repository and show individual open goals."""
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    rows = [
        "# Phase 175 R3R5 — $\\pi_7^3$ / Toda Lemma 5.7 source frontier",
        "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- No production changes; no new GIVEN and no complete proof imported",
        "- Full pytest: not run",
        "",
    ]
    source = report.get("preflight", {}).get("toda_lemma57_source", {})
    if isinstance(source, dict):
        rows.extend([
            "## 出典の照合", "",
            "- Toda " + str(source.get("locator")),
            "- Git blob: `" + str(source.get("source_blob")) + "`",
            "- Lemma 5.7 is earlier than Proposition 5.8",
            "- TeX source text alone is not a new GIVEN", "",
        ])
    result = report.get("worker", {}).get("data", {})
    if isinstance(result, dict):
        rows += ["## 既存規則と前提の独立探索", ""]
        for entry in result.get("obligations", []):
            rows.append("- **" + str(entry["name"]) + "**: " + str(entry["status"])
                        + " (routes=" + str(entry["offered_routes"]) + ")")
            if entry.get("diagnostic"):
                rows.append("  - " + str(entry["diagnostic"]))
            for name in entry.get("observed_unresolved", [])[:5]:
                rows.append("  - open: `" + str(name).replace("`", "'") + "`")
    if report.get("error"):
        rows += ["", "## エラー", "", "`" + str(report["error"]) + "`"]
    (folder / "report.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    """Check source pins and R3 evidence before a bounded, read-only audit."""
    local = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = local / "EHPProofTracerAudit" / PACKAGE / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    )
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3R5", "mode": "READ_ONLY_LEMMA57_SOURCE_FRONTIER",
        "dry_run": dry_run, "new_given": 0,
        "new_math_rules": 0, "production_changes": [], "full_pytest_executed": False,
        "result": "NOT_STARTED",
    }
    checked = None
    code = 2
    print("PHASE175_R3R5_OUTPUT=" + str(folder), flush=True)
    try:
        checked = scoped_preflight(root)
        report["preflight"] = checked
        prior = latest_verified_r3_report()
        report["r3r4_report"] = str(prior)
        print("PHASE175_R3R5_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R5_LEMMA57_SOURCE=PASS", flush=True)
        print("PHASE175_R3R5_R3R4_EVIDENCE=PASS", flush=True)
        if dry_run:
            report["result"] = "PASS_R3R5_READ_ONLY_DRYRUN"
            code = 0
        else:
            outcome = launch_worker(root, timeout_seconds, folder)
            report["worker"] = outcome
            if outcome.get("status") != "INSPECTED":
                raise RuntimeError("R3R5_TYPED_WORKER_FAILED: " + str(outcome))
            data = outcome.get("data", {})
            if (data.get("target_direct_given_excluded") is not True
                    or data.get("source_lemma57_new_given") is not False
                    or data.get("new_mathematical_rules") != 0
                    or data.get("production_modified") is not False
                    or data.get("hopf_lift_proposals") != 1
                    or data.get("zero_image_generic_bridge_candidates") != 1):
                raise RuntimeError("R3R5_UNSUPPORTED_TYPED_RESULT")
            statuses = {row["name"]: row["status"] for row in data["obligations"]}
            expected = {
                "ehp_exactness", "lower_pi62_group", "zero_generator_image",
                "zero_suspension_image", "hopf_injectivity",
            }
            if set(statuses) != expected:
                raise RuntimeError("R3R5_MISSING_OBLIGATION_OBSERVATION")
            for name in (
                "ehp_exactness", "lower_pi62_group", "zero_generator_image",
                "zero_suspension_image", "hopf_injectivity",
            ):
                print("PHASE175_R3R5_" + name.upper() + "=" + statuses[name], flush=True)
            print("PHASE175_R3R5_PUBLIC_PROVIDER_MODIFIED=False", flush=True)
            report["result"] = "PASS_R3R5_LEMMA57_FRONTIER_RECORDED"
            code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
        report["result"] = "R3R5_REFUSED_OR_WORKER_ERROR"
        print("PHASE175_R3R5_ERROR=" + report["error"], flush=True)
    finally:
        if checked is not None:
            try:
                report["tracked_unchanged"] = scoped_preflight(root) == checked
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)
            if report["tracked_unchanged"] is not True:
                report["result"] = "R3R5_TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(folder, report)
        print("PHASE175_R3R5_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R5_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE175_R3R5_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("positive timeout required")
    if args.worker:
        return worker()
    return run(args.root.resolve(), args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param(
    [switch]$DryRun,
    [ValidateRange(1, 7200)][int]$TimeoutSeconds = 300
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldPythonEncoding = $env:PYTHONIOENCODING
$OldPythonUtf8 = $env:PYTHONUTF8
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    $env:PYTHONPATH = "$RepoRoot;$OldPythonPath"
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location $RepoRoot
    try {
        Write-Output 'PHASE175_R3R5_GIT_STATUS_BEFORE'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R3R5 git status failed' }

        & python -B -m pytest -q --disable-warnings -p no:cacheprovider -o addopts= `
            --import-mode=importlib `
            '.\phase175_r3r5_pi73_lemma57_frontier\tests\test_source.py' `
            '.\phase175_r3r5_pi73_lemma57_frontier\tests\test_audit.py' `
            '.\phase175_r3r5_pi73_lemma57_frontier\tests\test_frontier.py' `
            '.\phase175_r3_pi73_hopf_lift\tests\test_audit.py' `
            '.\phase175_r3_pi73_hopf_lift\tests\test_rule.py' `
            '.\phase175_r3_pi73_hopf_lift\tests\test_frontier.py' `
            '.\phase175_r2_k4_frontier_audit\tests\test_audit.py' `
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3R5 focused pytest failed' }
        Write-Output 'PHASE175_R3R5_FOCUSED_PYTEST=PASS'

        $Arguments = @(
            '-B', '-m', 'phase175_r3r5_pi73_lemma57_frontier.audit',
            '--root', $RepoRoot, '--timeout-seconds', [string]$TimeoutSeconds
        )
        if ($DryRun) { $Arguments += '--dry-run' }
        & python @Arguments
        $AuditExit = $LASTEXITCODE
        Write-Output 'PHASE175_R3R5_GIT_STATUS_AFTER'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R3R5 git status after failed' }
        if ($AuditExit -ne 0) { throw "R3R5 audit failed: $AuditExit" }
        Write-Output 'PHASE175_R3R5=PASS'
        Write-Output '(END)'
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldPythonEncoding
    $env:PYTHONUTF8 = $OldPythonUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
```

## `tests/__init__.py`

```python
"""Focused Phase 175 R3R5 tests."""
```

## `tests/test_source.py`

```python
"""Source-first safeguards for the printed general Toda Lemma 5.7."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r3r5_pi73_lemma57_frontier import source


def sample_source() -> str:
    return "\n".join((
        r"\pi^{2}_{6}=\mathbb Z_4\gen{\eta_2\circ\nu'}",
        r"\begin{lemma}\label{lemma:5.7}",
        r"\alpha\in\pi_i(S^3)",
        r"E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5)",
        r"E(\eta_2\circ\alpha)=0",
        r"E(\eta_2\circ\nu')=0",
        r"\end{lemma}",
        r"E^2\nu'=2\nu_5",
        r"\pi^{2}_{6}=\Delta(\pi^{5}_{8})",
        r"E\pi_6^2=\gen{E(\eta_2\circ\nu')}=0",
        r"\begin{proposition}\label{prop:5.8}",
    ))


def test_lemma57_precedes_prop58_and_has_real_conditional() -> None:
    positions = source.source_clause_positions(sample_source())
    assert positions["lemma_start"] < positions["lemma_end"]
    assert positions["lemma_end"] < positions["proposition_58_start"]
    assert positions["general_conditional_count"] == 1
    assert positions["particular_consequence_count"] == 1


@pytest.mark.parametrize("old,new", [
    (r"E(\eta_2\circ\alpha)=0", r"E(\eta_2\circ\alpha)\ne0"),
    (r"E(\eta_2\circ\nu')=0", r"E(\eta_2\circ\nu')\ne0"),
    (r"E^2\nu'=2\nu_5", r"E^2\nu'=3\nu_5"),
    (r"\pi^{2}_{6}=\Delta(\pi^{5}_{8})", r"\pi^{2}_{6}=0"),
    (r"E\pi_6^2=\gen{E(\eta_2\circ\nu')}=0", "Unproved statement"),
])
def test_missing_or_changed_source_refused(old: str, new: str) -> None:
    with pytest.raises(ValueError):
        source.source_clause_positions(sample_source().replace(old, new))


def test_duplicate_lemma_source_refused() -> None:
    with pytest.raises(ValueError):
        source.source_clause_positions(sample_source().replace(
            source.LEMMA_START, source.LEMMA_START + "\n" + source.LEMMA_START,
        ))


def test_prop58_before_lemma_is_refused() -> None:
    text = sample_source().replace(source.PROPOSITION_START, "")
    text = source.PROPOSITION_START + "\n" + text
    with pytest.raises(ValueError):
        source.source_clause_positions(text)


def test_text_is_not_registered_as_given_or_group_proof() -> None:
    assert "from proof import" not in Path(source.__file__).read_text(encoding="utf-8")
    assert source.SOURCE_PATH == "sources/toda/Toda_05_2.tex"
    assert len(source.SOURCE_BLOB) == 40


def test_reject_non_string_source() -> None:
    with pytest.raises(TypeError):
        source.source_clause_positions(b"not TeX")
```

## `tests/test_audit.py`

```python
"""R3R5 audit-only evidence gates and no-forged-proof contracts."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase175_r3r5_pi73_lemma57_frontier import audit


def prior_report() -> dict:
    return {
        "phase": "175-R3",
        "dry_run": False,
        "result": "PASS_R3_PI73_HOPF_FRONTIER_RECORDED",
        "tracked_unchanged": True,
        "new_given": 0,
        "worker": {"data": {
            "target_direct_given_excluded": True,
            "hopf_lift_candidate_count": 1,
            "subgoal_observations": [
                {"name": "hopf_injectivity", "status": "UNRESOLVED"},
                {"name": "cyclic_codomain", "status": "INFERRED"},
                {"name": "hopf_generator_image", "status": "INFERRED"},
                {"name": "source_bound_cyclic_codomain", "status": "INFERRED"},
            ],
        }},
    }


def write_report(root: Path, result: dict, stamp: str = "20261112T001000_123456Z") -> Path:
    location = root / "EHPProofTracerAudit" / "phase175_r3_pi73_hopf_lift" / stamp
    location.mkdir(parents=True, exist_ok=True)
    target = location / "report.json"
    target.write_text(json.dumps(result), encoding="utf-8")
    return target


def test_latest_real_r3r4_report_is_admitted(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    path = write_report(tmp_path, prior_report())
    assert audit.latest_verified_r3_report() == path


@pytest.mark.parametrize("changes", [
    {"dry_run": True},
    {"result": "PASS_R3_READ_ONLY_DRYRUN"},
    {"tracked_unchanged": False},
    {"new_given": 1},
])
def test_invalid_r3r4_evidence_refused(tmp_path: Path, monkeypatch, changes: dict) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    write_report(tmp_path, {**prior_report(), **changes})
    with pytest.raises(RuntimeError, match="NO_VERIFIED_R3R4"):
        audit.latest_verified_r3_report()


def test_unproved_hopf_injectivity_required(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    entry = prior_report()
    entry["worker"]["data"]["subgoal_observations"][0]["status"] = "INFERRED"
    write_report(tmp_path, entry)
    with pytest.raises(RuntimeError):
        audit.latest_verified_r3_report()


def test_direct_given_codomain_not_counted_as_success(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    entry = prior_report()
    entry["worker"]["data"]["subgoal_observations"][1]["status"] = "DIRECT_GIVEN_NOT_ACCEPTABLE"
    write_report(tmp_path, entry)
    with pytest.raises(RuntimeError):
        audit.latest_verified_r3_report()


def test_report_written_outside_source_tree(tmp_path: Path) -> None:
    folder = tmp_path / "evidence"
    folder.mkdir()
    payload = {
        "result": "PASS_R3R5_READ_ONLY_DRYRUN",
        "preflight": {"toda_lemma57_source": {"locator": "Lemma 5.7", "source_blob": "a" * 40}},
    }
    audit.write_report(folder, payload)
    assert json.loads((folder / "report.json").read_text()) == payload
    assert "Lemma 5.7" in (folder / "report.md").read_text()


def test_audit_package_never_writes_to_production_paths() -> None:
    source = Path(audit.__file__).read_text(encoding="utf-8")
    assert '"new_given": 0' in source
    assert '"production_changes": []' in source
    assert "--worker" in source
    assert "git reset" not in source
    assert "git add" not in source
```

## `tests/test_frontier.py`

```python
"""Verify the shape of the EHP-zero-image query in the real checkout."""
from __future__ import annotations

import pytest

pytest.importorskip("phase165_r52_r9_shared_math")

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaHopfInvariantMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase174_r3_r7_r5_zero_image_hopf_injective.rule import hopf_injectivity_from_zero_image_inputs
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import expand_zero_image_from_cyclic_generator


def test_pi73_hopf_injectivity_requires_precisely_pi62_suspension() -> None:
    hopf = TodaHopfInvariantMap(TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5))
    inputs = hopf_injectivity_from_zero_image_inputs(MapInjective(hopf))
    assert inputs is not None
    zero_image, exactness = inputs
    assert zero_image == ImageZeroStatement(TodaSuspensionMap(
        TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3),
    ))
    assert exactness.window.middle_term == TodaPrimaryGroup(7, 3)


def test_generic_zero_image_uses_unproved_pi62_presentation_and_image() -> None:
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    goals = expand_zero_image_from_cyclic_generator(ImageZeroStatement(e), prior)
    assert len(goals) == 1
    assert goals[0].subgoals == (
        prior, GeneratorImage(e, prior.rhs.generator, Zero()),
    )
    assert all(not hasattr(item, "premises") for item in goals[0].subgoals)
```
