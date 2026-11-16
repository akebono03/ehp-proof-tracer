"""Phase 175 R3R6: source-first, isolated Lemma 5.7 general inference audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r5_pi73_lemma57_frontier.source import verify_reviewed_toda_source
from phase175_r3r6_lemma57_general.source import verify_lemma57_manifest

PACKAGE = "phase175_r3r6_lemma57_general"
MARKER = "__PHASE175_R3R6_WORKER__="


R3_PACKAGE = "phase175_r3_pi73_hopf_lift"
R2_PACKAGE = "phase175_r2_k4_frontier_audit"
R3_LINEAGE_ALLOWED_ADDITIONS = frozenset({
    R3_PACKAGE + "/__init__.py",
    R3_PACKAGE + "/rule.py",
    R3_PACKAGE + "/audit.py",
    R3_PACKAGE + "/run.ps1",
    R3_PACKAGE + "/frontier.py",
    R3_PACKAGE + "/tests/__init__.py",
    R3_PACKAGE + "/tests/test_rule.py",
    R3_PACKAGE + "/tests/test_audit.py",
    R3_PACKAGE + "/tests/test_frontier.py",
    R3_PACKAGE + "/README.md",
    R3_PACKAGE + "/AUDIT_PLAN_JA.md",
    R3_PACKAGE + "/CODE_FULL_JA.md",
})

R3R5_ALLOWED_ADDITIONS = frozenset({
    'phase175_r3r5_pi73_lemma57_frontier/AUDIT_PLAN_JA.md',
    'phase175_r3r5_pi73_lemma57_frontier/CODE_FULL_JA.md',
    'phase175_r3r5_pi73_lemma57_frontier/README.md',
    'phase175_r3r5_pi73_lemma57_frontier/TEST_RESULTS_JA.md',
    'phase175_r3r5_pi73_lemma57_frontier/__init__.py',
    'phase175_r3r5_pi73_lemma57_frontier/audit.py',
    'phase175_r3r5_pi73_lemma57_frontier/frontier.py',
    'phase175_r3r5_pi73_lemma57_frontier/run.ps1',
    'phase175_r3r5_pi73_lemma57_frontier/source.py',
    'phase175_r3r5_pi73_lemma57_frontier/tests/__init__.py',
    'phase175_r3r5_pi73_lemma57_frontier/tests/test_audit.py',
    'phase175_r3r5_pi73_lemma57_frontier/tests/test_frontier.py',
    'phase175_r3r5_pi73_lemma57_frontier/tests/test_source.py',
})

R3R6_ALLOWED_ADDITIONS = frozenset({
    'phase175_r3r6_lemma57_general/AUDIT_PLAN_JA.md',
    'phase175_r3r6_lemma57_general/CODE_FULL_JA.md',
    'phase175_r3r6_lemma57_general/README.md',
    'phase175_r3r6_lemma57_general/TEST_RESULTS_JA.md',
    'phase175_r3r6_lemma57_general/__init__.py',
    'phase175_r3r6_lemma57_general/audit.py',
    'phase175_r3r6_lemma57_general/rule.py',
    'phase175_r3r6_lemma57_general/run.ps1',
    'phase175_r3r6_lemma57_general/source.py',
    'phase175_r3r6_lemma57_general/tests/__init__.py',
    'phase175_r3r6_lemma57_general/tests/test_audit.py',
    'phase175_r3r6_lemma57_general/tests/test_lineage.py',
    'phase175_r3r6_lemma57_general/tests/test_powershell_utf8.py',
    'phase175_r3r6_lemma57_general/tests/test_rule.py',
    'phase175_r3r6_lemma57_general/tests/test_source.py',
})

def _lineage_git(root: Path, *args: str) -> str:
    """Read-only Git query; never stage, reset, or modify the worktree."""
    if not args or args[0] not in {"rev-parse", "diff"}:
        raise ValueError("R3R6 lineage accepts only Git read operations")
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R3R6_GIT_LINEAGE_READ_FAILED: " + " ".join(args))
    return result.stdout.strip()


def verify_r3r6_lineage(
    root: Path, previous: dict[str, object], checked: dict[str, object],
) -> dict[str, object]:
    """Allow only known added audit files since the verified R2 run.

    R3R4's rule predates the R3R5 commit and therefore rejected that
    later audit-only addition.  Do not relax it in the R3/R2 packages.
    R3R6 extends the exact allowlist locally; modifications, deletions,
    renames and unrecognized additions still fail closed.
    """
    before = previous.get("preflight")
    old = before.get("head") if isinstance(before, dict) else None
    new = checked.get("head")
    if (
        type(old) is not str or type(new) is not str
        or re.fullmatch(r"[0-9a-f]{40}", old) is None
        or re.fullmatch(r"[0-9a-f]{40}", new) is None
        or _lineage_git(root, "rev-parse", "HEAD") != new
    ):
        raise RuntimeError("R3R6_UNVERIFIED_GIT_HEAD")
    if old == new:
        return {
            "mode": "SAME_HEAD", "audit_only_paths": [],
            "r3_added_paths": [], "r3r5_added_paths": [],
            "r3r6_added_paths": [],
        }
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", old, new],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("R3R6_R2_HEAD_NOT_ANCESTOR")
    changed = _lineage_git(root, "diff", "--name-status", "--no-renames", old, new)
    if not changed:
        raise RuntimeError("R3R6_LINEAGE_NOT_AUDIT_ONLY")
    paths: list[str] = []
    r3_paths: list[str] = []
    r3r5_paths: list[str] = []
    r3r6_paths: list[str] = []
    for line in changed.splitlines():
        status, separator, relative = line.partition("\t")
        if separator != "\t" or status != "A":
            raise RuntimeError("R3R6_LINEAGE_NOT_AUDIT_ONLY")
        if relative.startswith(R2_PACKAGE + "/"):
            paths.append(relative)
        elif relative in R3_LINEAGE_ALLOWED_ADDITIONS:
            paths.append(relative)
            r3_paths.append(relative)
        elif relative in R3R5_ALLOWED_ADDITIONS:
            paths.append(relative)
            r3r5_paths.append(relative)
        elif relative in R3R6_ALLOWED_ADDITIONS:
            paths.append(relative)
            r3r6_paths.append(relative)
        else:
            raise RuntimeError("R3R6_LINEAGE_NOT_AUDIT_ONLY: " + relative)
    return {
        "mode": "AUDIT_ONLY_DESCENDANT", "audit_only_paths": paths,
        "r3_added_paths": r3_paths, "r3r5_added_paths": r3r5_paths,
        "r3r6_added_paths": r3r6_paths,
    }


def scoped_preflight(root: Path) -> dict[str, object]:
    """Preserve R3/R2 source guards with R3R5 committed-audit lineage support."""
    from phase175_r3_pi73_hopf_lift import audit as r3

    if r3.R3_LINEAGE_ALLOWED_ADDITIONS != R3_LINEAGE_ALLOWED_ADDITIONS:
        raise RuntimeError("R3R6_R3_LINEAGE_POLICY_DRIFT")
    checked = r3.preflight(root)
    report_file = r3.select_r2_report(None)
    previous = json.loads(report_file.read_text(encoding="utf-8"))
    r3.validate_r2(previous)
    lineage = verify_r3r6_lineage(root, previous, checked)
    source = verify_reviewed_toda_source(root)
    return {
        "r3_source_guard": checked,
        "r2_lineage": lineage,
        "r2_report_path": str(report_file),
        "toda_lemma57_source": source,
    }



def latest_r3r5_report() -> Path:
    """Require a real successful normal R3R5 audit with its observed frontier."""
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    directory = base / "EHPProofTracerAudit" / "phase175_r3r5_pi73_lemma57_frontier"
    for filename in sorted(directory.glob("*/report.json"), reverse=True):
        try:
            report = json.loads(filename.read_text(encoding="utf-8"))
            data = report.get("worker", {}).get("data", {})
            statuses = {row["name"]: row["status"] for row in data.get("obligations", ())}
            if (report.get("phase") == "175-R3R5"
                    and report.get("dry_run") is False
                    and report.get("result") == "PASS_R3R5_LEMMA57_FRONTIER_RECORDED"
                    and report.get("tracked_unchanged") is True
                    and report.get("new_given") == 0
                    and report.get("new_math_rules") == 0
                    and statuses == {
                        "ehp_exactness": "INFERRED",
                        "lower_pi62_group": "INFERRED",
                        "zero_generator_image": "UNRESOLVED",
                        "zero_suspension_image": "UNRESOLVED",
                        "hopf_injectivity": "UNRESOLVED",
                    }):
                return filename
        except (OSError, ValueError, KeyError, TypeError, UnicodeError):
            continue
    raise RuntimeError("R3R6_NO_VERIFIED_R3R5_FRONTIER_REPORT")


def inspected_general_criterion() -> dict[str, object]:
    """Build only a cited conditional and observe the still-unproved membership."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase166_r3c_publication_order import precedes_citing_assertion
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase175_r3_pi73_hopf_lift.frontier import inspect_independent_obligation
    from phase175_r3r6_lemma57_general.rule import (
        TodaLemma57DoubleSuspensionMembership,
        expand_cited_lemma57_zero_generator,
        lemma57_criterion_inputs,
    )
    from phase175_r3r6_lemma57_general.source import (
        GENERAL_ASSERTION_ID, TodaLemma57GeneralCriterion,
        build_isolated_lemma57_source, merge_isolated_cited_source,
    )
    from proof import ProofRule

    root = Path(__file__).resolve().parents[1]
    original = build_shared_typed_bridge()
    target = exact_prior_database_result(3, 4)
    citing = resolve_specialized_goal_citing_id(original, target)
    if not citing:
        raise RuntimeError("R3R6_PI73_CITING_SOURCE_UNAVAILABLE")
    screened = screen_shared_proof_context(
        original, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    prior = exact_prior_database_result(2, 4)
    if prior is None or prior.lhs != TodaPrimaryGroup(6, 2):
        raise RuntimeError("R3R6_PI62_TYPED_PRIOR_UNAVAILABLE")
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    zero = GeneratorImage(e, prior.rhs.generator, Zero())
    new_source = build_isolated_lemma57_source(root)
    merged = merge_isolated_cited_source(screened, new_source)
    if not precedes_citing_assertion(merged, GENERAL_ASSERTION_ID, citing):
        raise RuntimeError("R3R6_LEMMA57_MUST_PRECEDE_PI73_GOAL")
    available = tuple(
        link.step.conclusion for link in merged.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if target in available:
        raise RuntimeError("R3R6_PI73_TARGET_MUST_NOT_BE_GIVEN")
    if available.count(TodaLemma57GeneralCriterion()) != 1:
        raise RuntimeError("R3R6_SOURCE_MUST_BE_UNIQUE")
    required = lemma57_criterion_inputs(zero)
    offers = expand_cited_lemma57_zero_generator(zero, available)
    if (required is None or len(offers) != 1 or offers[0].subgoals != required
            or not isinstance(required[1], TodaLemma57DoubleSuspensionMembership)):
        raise RuntimeError("R3R6_TYPED_GENERAL_RULE_DID_NOT_MATCH")
    ordinary = shared_expansion_provider(merged, proof_target=target)

    def scoped(goal: object):
        if goal == zero:
            return offers + ordinary(goal)
        return ordinary(goal)

    observations = (
        inspect_independent_obligation(
            "double_suspension_membership", required[1], merged, citing, scoped,
        ),
        inspect_independent_obligation(
            "lemma57_zero_generator_image", zero, merged, citing, scoped,
        ),
    )
    return {
        "target": repr(target),
        "source_reference": "Lemma 5.7",
        "source_assertion": GENERAL_ASSERTION_ID,
        "source_before_target": True,
        "source_general_given_count": 1,
        "particular_nu_prime_given_count": 0,
        "new_production_given": 0,
        "new_general_rule_count": 1,
        "isolated_proposal_count": len(offers),
        "membership_goal": repr(required[1]),
        "public_provider_modified": False,
        "observations": observations,
    }


def launch_worker(root: Path, timeout_seconds: int, folder: Path) -> dict[str, object]:
    """Isolate recursive search with a bounded worker process."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        process = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--root", str(root), "--worker"],
            cwd=root, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout_seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "seconds": timeout_seconds}
    (folder / "worker.log").write_text(
        process.stdout + "\nSTDERR:\n" + process.stderr, encoding="utf-8",
    )
    lines = [line[len(MARKER):] for line in process.stdout.splitlines() if line.startswith(MARKER)]
    if process.returncode or len(lines) != 1:
        return {"status": "INVALID_WORKER", "code": process.returncode, "markers": len(lines)}
    try:
        result = json.loads(lines[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_JSON"}
    return result if isinstance(result, dict) else {"status": "INVALID_PAYLOAD"}


def worker() -> int:
    """Report genuine typed-goal reconstruction, never import a saved ProofStep."""
    try:
        payload = {"status": "INSPECTED", "data": inspected_general_criterion()}
    except Exception as exc:
        payload = {
            "status": "ERROR", "error": type(exc).__name__ + ": " + str(exc),
            "traceback": traceback.format_exc()[-6000:],
        }
    print(MARKER + json.dumps(payload, ensure_ascii=False), flush=True)
    return 0


def write_report(folder: Path, report: dict[str, object]) -> None:
    """Write the full audit evidence outside the repository."""
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    rows = [
        "# Phase 175 R3R6 — Toda Lemma 5.7 general criterion", "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- New cited general source only, no conclusion GIVEN",
        "- Production and Web unchanged; full pytest not executed", "",
    ]
    data = report.get("worker", {}).get("data", {})
    if isinstance(data, dict):
        rows.extend(["## Source-first proof obligations", ""])
        for observation in data.get("observations", ()):
            rows.append("- **" + observation["name"] + "**: " + observation["status"])
            rows.append("  - proposed routes: " + str(observation["offered_routes"]))
            for value in observation.get("observed_unresolved", ())[:8]:
                rows.append("  - Open Goal: `" + str(value).replace("`", "'") + "`")
    if report.get("error"):
        rows.extend(["", "## Error", "", "`" + str(report["error"]) + "`"])
    (folder / "report.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    """Preserve R3R5 Source Guard, source order and all tracked repository files."""
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3R6", "dry_run": dry_run, "result": "NOT_STARTED",
        "new_production_given": 0, "production_changes": [], "full_pytest": False,
    }
    checked = None
    code = 2
    print("PHASE175_R3R6_OUTPUT=" + str(folder), flush=True)
    try:
        checked = scoped_preflight(root)
        report["preflight"] = checked
        report["r3r5_report"] = str(latest_r3r5_report())
        report["lemma57_manifest"] = verify_lemma57_manifest(root)
        print("PHASE175_R3R6_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R6_R2_LINEAGE=" + str(checked["r2_lineage"]["mode"]), flush=True)
        print("PHASE175_R3R6_R3R5_COMMITTED_AUDIT_FILES=" + str(
            len(checked["r2_lineage"]["r3r5_added_paths"])
        ), flush=True)
        print("PHASE175_R3R6_R3R5_EVIDENCE=PASS", flush=True)
        print("PHASE175_R3R6_GENERAL_SOURCE=PASS", flush=True)
        if dry_run:
            report["result"] = "PASS_R3R6_READ_ONLY_DRYRUN"
            code = 0
        else:
            result = launch_worker(root, timeout_seconds, folder)
            report["worker"] = result
            if result.get("status") != "INSPECTED":
                raise RuntimeError("R3R6_WORKER_FAILED: " + str(result))
            data = result.get("data", {})
            if (data.get("source_before_target") is not True
                    or data.get("source_general_given_count") != 1
                    or data.get("particular_nu_prime_given_count") != 0
                    or data.get("new_production_given") != 0
                    or data.get("isolated_proposal_count") != 1
                    or data.get("public_provider_modified") is not False):
                raise RuntimeError("R3R6_TYPED_SOURCE_POLICY_VIOLATION")
            observations = {item["name"]: item["status"] for item in data["observations"]}
            if set(observations) != {"double_suspension_membership", "lemma57_zero_generator_image"}:
                raise RuntimeError("R3R6_MISSING_TYPED_OBLIGATIONS")
            for name, status in observations.items():
                print("PHASE175_R3R6_" + name.upper() + "=" + status, flush=True)
            report["result"] = "PASS_R3R6_GENERAL_LEMMA57_FRONTIER_RECORDED"
            code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
        report["result"] = "R3R6_REFUSED_OR_WORKER_ERROR"
        print("PHASE175_R3R6_ERROR=" + report["error"], flush=True)
    finally:
        if checked is not None:
            try:
                report["tracked_unchanged"] = scoped_preflight(root) == checked
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)
            if report["tracked_unchanged"] is not True:
                report["result"] = "R3R6_TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(folder, report)
        print("PHASE175_R3R6_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R6_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE175_R3R6_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("timeout must be positive")
    if args.worker:
        return worker()
    return run(args.root.resolve(), args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
