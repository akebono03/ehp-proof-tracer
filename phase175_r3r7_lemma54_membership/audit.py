"""Phase 175 R3R7: read-only isolated source-to-EHP proof-search audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r6_lemma57_general import audit as r3r6
from phase175_r3r7_lemma54_membership.source import verify_lemma54_before_lemma57

PACKAGE = "phase175_r3r7_lemma54_membership"
MARKER = "__PHASE175_R3R7_WORKER__="
ALLOWED_NEW_FILES = frozenset({
    PACKAGE + "/__init__.py",
    PACKAGE + "/source.py",
    PACKAGE + "/rule.py",
    PACKAGE + "/audit.py",
    PACKAGE + "/run.ps1",
    PACKAGE + "/README.md",
    PACKAGE + "/AUDIT_PLAN_JA.md",
    PACKAGE + "/CODE_FULL_JA.md",
    PACKAGE + "/TEST_RESULTS_JA.md",
    PACKAGE + "/tests/__init__.py",
    PACKAGE + "/tests/test_source.py",
    PACKAGE + "/tests/test_rule.py",
    PACKAGE + "/tests/test_audit.py",
})


def verify_lineage(root: Path, previous: dict, checked: dict) -> dict[str, object]:
    """Permit only explicitly named added audit files since the verified R2 run."""
    old = previous.get("preflight", {}).get("head")
    new = checked.get("head")
    if (not isinstance(old, str) or not isinstance(new, str)
            or re.fullmatch(r"[a-f0-9]{40}", old) is None
            or re.fullmatch(r"[a-f0-9]{40}", new) is None
            or r3r6._lineage_git(root, "rev-parse", "HEAD") != new):
        raise RuntimeError("R3R7_INVALID_VERIFIED_HEAD")
    if old == new:
        return {"mode": "SAME_HEAD", "audit_only_paths": [], "r3r7_added_paths": []}
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", old, new],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("R3R7_R2_HEAD_NOT_ANCESTOR")
    changes = r3r6._lineage_git(root, "diff", "--name-status", "--no-renames", old, new)
    paths: list[str] = []
    additions: list[str] = []
    for line in changes.splitlines():
        status, tab, path = line.partition("\t")
        if tab != "\t" or status != "A":
            raise RuntimeError("R3R7_NON_AUDIT_CHANGE_IN_LINEAGE")
        if (path.startswith(r3r6.R2_PACKAGE + "/")
                or path in r3r6.R3_LINEAGE_ALLOWED_ADDITIONS
                or path in r3r6.R3R5_ALLOWED_ADDITIONS
                or path in r3r6.R3R6_ALLOWED_ADDITIONS):
            paths.append(path)
        elif path in ALLOWED_NEW_FILES:
            paths.append(path)
            additions.append(path)
        else:
            raise RuntimeError("R3R7_UNKNOWN_LINEAGE_ADDITION: " + path)
    if not paths:
        raise RuntimeError("R3R7_EMPTY_DESCENDANT_DIFF")
    return {
        "mode": "AUDIT_ONLY_DESCENDANT",
        "audit_only_paths": paths,
        "r3r7_added_paths": additions,
    }


def scoped_preflight(root: Path) -> dict[str, object]:
    """Reuse the R3 Source Guard and R2 evidence; extend lineage for this ZIP."""
    from phase175_r3_pi73_hopf_lift import audit as r3

    if r3.R3_LINEAGE_ALLOWED_ADDITIONS != r3r6.R3_LINEAGE_ALLOWED_ADDITIONS:
        raise RuntimeError("R3R7_R3_SOURCE_GUARD_POLICY_CHANGED")
    checked = r3.preflight(root)
    report_file = r3.select_r2_report(None)
    previous = json.loads(report_file.read_text(encoding="utf-8"))
    r3.validate_r2(previous)
    lineage = verify_lineage(root, previous, checked)
    source = verify_lemma54_before_lemma57(root)
    return {
        "r3_source_guard": checked,
        "r2_lineage": lineage,
        "r2_report_path": str(report_file),
        "lemma54_lemma57_source": source,
    }


def latest_successful_r3r6() -> Path:
    """Require the actual preceding normal audit, never its DryRun or notes."""
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    directory = base / "EHPProofTracerAudit" / "phase175_r3r6_lemma57_general"
    for path in sorted(directory.glob("*/report.json"), reverse=True):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
            data = report.get("worker", {}).get("data", {})
            statuses = {item["name"]: item["status"] for item in data.get("observations", ())}
            if (report.get("phase") == "175-R3R6"
                    and report.get("dry_run") is False
                    and report.get("result") == "PASS_R3R6_GENERAL_LEMMA57_FRONTIER_RECORDED"
                    and report.get("tracked_unchanged") is True
                    and report.get("new_production_given") == 0
                    and data.get("source_general_given_count") == 1
                    and data.get("particular_nu_prime_given_count") == 0
                    and statuses == {
                        "double_suspension_membership": "UNRESOLVED",
                        "lemma57_zero_generator_image": "UNRESOLVED",
                    }):
                return path
        except (OSError, UnicodeError, KeyError, ValueError, TypeError):
            continue
    raise RuntimeError("R3R7_NO_VERIFIED_R3R6_NORMAL_AUDIT_REPORT")


def inspect_actual_search() -> dict[str, object]:
    """Reconstruct real ProofSteps without a saved result or direct target GIVEN."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase166_r3c_publication_order import precedes_citing_assertion
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase173_r4_r1_lemma54_source_bridge.source import (
        ADOPTED_ASSERTION_ID,
        TodaLemma54TypedSource,
    )
    from phase174_r3_r6_r2_prop44_lemma54.source import attach_earlier_verified_lemma54
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        expand_hopf_injective_from_zero_image,
        hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        expand_zero_image_from_cyclic_generator,
    )
    from phase175_r3_pi73_hopf_lift.frontier import inspect_independent_obligation
    from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
    from phase175_r3r6_lemma57_general.rule import (
        expand_cited_lemma57_zero_generator,
        lemma57_criterion_inputs,
    )
    from phase175_r3r6_lemma57_general.source import (
        GENERAL_ASSERTION_ID,
        TodaLemma57GeneralCriterion,
        build_isolated_lemma57_source,
        merge_isolated_cited_source,
    )
    from phase175_r3r7_lemma54_membership.rule import (
        cited_lemma54_double_relation,
        expand_cited_lemma54_double,
        expand_even_factor_membership,
    )
    from proof import ProofRule, Relation
    from unified_statement_registry import AssertionOrigin

    root = Path(__file__).resolve().parents[1]
    original = build_shared_typed_bridge()
    target = exact_prior_database_result(3, 4)
    prior = exact_prior_database_result(2, 4)
    if (not isinstance(target, Relation)
            or target.lhs != TodaPrimaryGroup(7, 3)
            or not isinstance(prior, Relation)
            or prior.lhs != TodaPrimaryGroup(6, 2)):
        raise RuntimeError("R3R7_GROUP_GOAL_OR_PI62_PRIOR_INVALID")
    citing = resolve_specialized_goal_citing_id(original, target)
    if not isinstance(citing, str) or not citing:
        raise RuntimeError("R3R7_CITING_ASSERTION_NOT_REGISTERED")
    source_bound = attach_earlier_verified_lemma54(original, citing)
    screened = screen_shared_proof_context(
        source_bound, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    supplement = build_isolated_lemma57_source(root)
    merged = merge_isolated_cited_source(screened, supplement)
    for assertion_id in (ADOPTED_ASSERTION_ID, GENERAL_ASSERTION_ID):
        if assertion_id not in merged.registry._assertions:
            raise RuntimeError("R3R7_REQUIRED_EARLIER_SOURCE_NOT_ADOPTED: " + assertion_id)
        if not precedes_citing_assertion(merged, assertion_id, citing):
            raise RuntimeError("R3R7_CITED_SOURCE_AFTER_GOAL: " + assertion_id)
    available = tuple(
        link.step.conclusion for link in merged.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and merged.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    if (available.count(TodaLemma54TypedSource()) != 1
            or available.count(TodaLemma57GeneralCriterion()) != 1
            or target in available):
        raise RuntimeError("R3R7_INVALID_SOURCE_LEAVES_OR_TARGET_GIVEN")
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    zero_generator = GeneratorImage(e, prior.rhs.generator, Zero())
    lemma57_inputs = lemma57_criterion_inputs(zero_generator)
    if lemma57_inputs is None:
        raise RuntimeError("R3R7_TYPED_LEMMA57_TARGET_NOT_MATCHED")
    general, membership = lemma57_inputs
    equation = cited_lemma54_double_relation()
    extracted = expand_cited_lemma54_double(equation, available)
    factors = expand_even_factor_membership(membership, (equation,))
    zero_offers = expand_cited_lemma57_zero_generator(zero_generator, available)
    if (len(extracted) != 1 or len(factors) != 1 or len(zero_offers) != 1
            or extracted[0].subgoals != (TodaLemma54TypedSource(),)
            or factors[0].subgoals != (equation,)
            or zero_offers[0].subgoals != (general, membership)):
        raise RuntimeError("R3R7_TYPED_SOURCE_CHAIN_NOT_OFFERED")
    zero_image = ImageZeroStatement(e)
    bridge_options = expand_zero_image_from_cyclic_generator(zero_image, prior)
    if len(bridge_options) != 1 or bridge_options[0].subgoals != (prior, zero_generator):
        raise RuntimeError("R3R7_CYCLIC_ZERO_IMAGE_BRIDGE_MISSING")
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    lift_offers = expand_cited_hopf_lift(cyclic, available)
    if len(lift_offers) != 1:
        raise RuntimeError("R3R7_CITED_HOPF_LIFT_NOT_UNIQUE")
    hopf_injective = lift_offers[0].subgoals[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf_injective)
    if (hopf_inputs is None or hopf_inputs[0] != zero_image
            or len(expand_hopf_injective_from_zero_image(hopf_injective)) != 1):
        raise RuntimeError("R3R7_EHP_EXACTNESS_RULE_UNAVAILABLE")
    ordinary = shared_expansion_provider(merged, proof_target=target)

    def provider(goal: object):
        if goal == equation:
            return extracted + ordinary(goal)
        if goal == membership:
            return factors + ordinary(goal)
        if goal == zero_generator:
            return zero_offers + ordinary(goal)
        if goal == zero_image:
            return bridge_options + ordinary(goal)
        if goal == hopf_injective:
            return expand_hopf_injective_from_zero_image(goal) + ordinary(goal)
        if goal == cyclic:
            return lift_offers + ordinary(goal)
        return ordinary(goal)

    goals = (
        ("lemma54_double_relation", equation),
        ("double_suspension_membership", membership),
        ("lemma57_zero_generator_image", zero_generator),
        ("zero_suspension_image", zero_image),
        ("hopf_injectivity", hopf_injective),
        ("pi73_cyclic_lift", cyclic),
    )
    inspected = [
        inspect_independent_obligation(name, goal, merged, citing, provider)
        for name, goal in goals
    ]
    return {
        "target": repr(target),
        "verified_lemma54_source": True,
        "verified_lemma57_source": True,
        "lemma54_precedes_lemma57": True,
        "new_specific_given": 0,
        "new_production_rules": 0,
        "public_provider_modified": False,
        "literal_equation": repr(equation),
        "membership_goal": repr(membership),
        "offered_source_extraction": len(extracted),
        "offered_generic_factor_rule": len(factors),
        "offered_lemma57_rule": len(zero_offers),
        "observations": inspected,
    }


def worker() -> int:
    """Run isolated canonical search; errors are reported as failed audits."""
    try:
        payload = {"status": "INSPECTED", "data": inspect_actual_search()}
    except Exception as exc:
        payload = {
            "status": "ERROR",
            "error": type(exc).__name__ + ": " + str(exc),
            "traceback": traceback.format_exc()[-8000:],
        }
    print(MARKER + json.dumps(payload, ensure_ascii=False), flush=True)
    return 0


def launch_worker(root: Path, seconds: int, folder: Path) -> dict[str, object]:
    """Constrain the expensive proof search in a separate Python process."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        completed = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--root", str(root), "--worker"],
            cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=seconds, check=False, env=env,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "seconds": seconds}
    (folder / "worker.log").write_text(
        completed.stdout + "\nSTDERR:\n" + completed.stderr, encoding="utf-8",
    )
    rows = [line[len(MARKER):] for line in completed.stdout.splitlines() if line.startswith(MARKER)]
    if completed.returncode or len(rows) != 1:
        return {"status": "INVALID_WORKER", "code": completed.returncode, "markers": len(rows)}
    try:
        result = json.loads(rows[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_JSON"}
    return result if isinstance(result, dict) else {"status": "INVALID_WORKER_PAYLOAD"}


def write_report(folder: Path, report: dict) -> None:
    """All outputs are outside the repository and UTF-8 encoded."""
    (folder / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    md = [
        "# Phase 175 R3R7 — Lemma 5.4 double suspension membership", "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- No direct theorem GIVEN and no production or Web changes",
        "- Whole-repository pytest not executed", "",
        "## Verified proof-search obligations", "",
    ]
    data = report.get("worker", {}).get("data", {})
    if isinstance(data, dict):
        for item in data.get("observations", ()):
            md.append("- **" + item["name"] + "**: " + item["status"])
            md.append("  - offered routes: " + str(item["offered_routes"]))
            for unresolved in item.get("observed_unresolved", ())[:5]:
                md.append("  - Open Goal: `" + str(unresolved).replace("`", "'") + "`")
    if report.get("error"):
        md.extend(["", "## Failure", "", "`" + str(report["error"]) + "`"])
    (folder / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    """Preflight, fixed-source checks, isolated audit, and postflight guard."""
    root = Path(root).resolve()
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3R7", "dry_run": dry_run, "result": "NOT_STARTED",
        "new_specific_given": 0, "production_changes": [], "full_pytest": False,
    }
    preflight = None
    code = 2
    print("PHASE175_R3R7_OUTPUT=" + str(folder), flush=True)
    try:
        preflight = scoped_preflight(root)
        report["preflight"] = preflight
        report["r3r6_report"] = str(latest_successful_r3r6())
        print("PHASE175_R3R7_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R7_LEMMA54_BEFORE_LEMMA57=PASS", flush=True)
        print("PHASE175_R3R7_R3R6_EVIDENCE=PASS", flush=True)
        if dry_run:
            report["result"] = "PASS_R3R7_READ_ONLY_DRYRUN"
            code = 0
        else:
            inspected = launch_worker(root, timeout_seconds, folder)
            report["worker"] = inspected
            if inspected.get("status") != "INSPECTED":
                raise RuntimeError("R3R7_WORKER_FAILED: " + str(inspected))
            data = inspected.get("data")
            if (not isinstance(data, dict)
                    or data.get("verified_lemma54_source") is not True
                    or data.get("verified_lemma57_source") is not True
                    or data.get("new_specific_given") != 0
                    or data.get("new_production_rules") != 0
                    or data.get("public_provider_modified") is not False):
                raise RuntimeError("R3R7_TYPED_SOURCE_POLICY_FAILURE")
            statuses = {item["name"]: item["status"] for item in data["observations"]}
            expected = {
                "lemma54_double_relation", "double_suspension_membership",
                "lemma57_zero_generator_image", "zero_suspension_image",
                "hopf_injectivity", "pi73_cyclic_lift",
            }
            if set(statuses) != expected:
                raise RuntimeError("R3R7_TYPED_PROOF_OBLIGATIONS_MISSING")
            for name, status in statuses.items():
                print("PHASE175_R3R7_" + name.upper() + "=" + status, flush=True)
            if statuses["double_suspension_membership"] != "INFERRED":
                report["result"] = "R3R7_MEMBERSHIP_UNRESOLVED"
                code = 3
            elif statuses["pi73_cyclic_lift"] == "INFERRED":
                report["result"] = "PASS_R3R7_ISOLATED_PI73_CYCLIC_INFERRED"
                code = 0
            else:
                report["result"] = "PASS_R3R7_MEMBERSHIP_INFERRED_PI73_PENDING"
                code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-8000:]
        report["result"] = "R3R7_REFUSED_OR_WORKER_ERROR"
        print("PHASE175_R3R7_ERROR=" + str(report["error"]), flush=True)
    finally:
        if preflight is not None:
            try:
                report["tracked_unchanged"] = scoped_preflight(root) == preflight
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)
            if report["tracked_unchanged"] is not True:
                report["result"] = "R3R7_TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(folder, report)
        print("PHASE175_R3R7_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R7_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE175_R3R7_GATE=" + str(report["result"]), flush=True)
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
    return run(args.root, args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
