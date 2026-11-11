"""Phase 175 R2: read-only, source-first frontier audit for three k=4 gaps.

R1's actual six-group observations are retained; previously registered Toda
sources are re-checked. No new inference, GIVEN, or successful proof is claimed.
"""
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


PACKAGE = "phase175_r2_k4_frontier_audit"
R1_PACKAGE = "phase175_r1_k4_audit"
MARKER = "__PHASE175_R2_SOURCE_WORKER__="
UNFINISHED = ((3, 4), (5, 4), (6, 4))
EXPECTED_STATUSES = {
    (2, 4): "COMPLETE_AND_WEB_VERIFIED",
    (3, 4): "INCOMPLETE_AND_WEB_CONFIRMED",
    (4, 4): "COMPLETE_AND_WEB_VERIFIED",
    (5, 4): "INCOMPLETE_AND_WEB_CONFIRMED",
    (6, 4): "INCOMPLETE_AND_WEB_CONFIRMED",
    (7, 4): "COMPLETE_AND_WEB_VERIFIED",
}
OPEN_COUNTS = {(3, 4): 3, (5, 4): 3, (6, 4): 2}
EXTRA_PINS = {
    "phase170_r3_r6_prop58_source.py": "f0223668e60bb9d18f10b0e8721dece79d7e705a",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py": "b90fe1fee5db04228ed986083b5214709045a7ea",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_source.py": "01d200cd7fd8698cb34ac02fdffe1b01c6879d10",
    "phase174_r3_r7_r18_delta_image_surjectivity/rule.py": "f8da1f6fb7d5fb66feae33b4a4847fbad6891342",
    "phase174_r3_r7_r56_cyclic_generator_bridge/rule.py": "e6bbeb8efa47a46f7326b8711b6de9e79ff60319",
    "phase165_r12_r5_structure_bridge.py": "4067bf1b2cc4114359c2d1a104d17ba874122060",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(root: Path, *args: str) -> str:
    """Read Git metadata without writing to the checkout."""
    run = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if run.returncode:
        raise RuntimeError("R2_GIT_ERROR: " + " ".join(args) + ": " + run.stderr.strip())
    return run.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    """Reuse R1's reviewed source/head guard and verify new audit dependencies."""
    from phase175_r1_k4_audit.audit import preflight as r1_preflight

    initial = r1_preflight(root)
    for relative, expected in EXTRA_PINS.items():
        if not (root / relative).is_file():
            raise RuntimeError("R2_SOURCE_MISSING: " + relative)
        observed = git(root, "rev-parse", "HEAD:" + relative)
        if observed != expected:
            raise RuntimeError("R2_SOURCE_PIN_MISMATCH: " + relative)
    return {
        "head": initial["head"], "branch": initial["branch"],
        "r1_pins": initial["source_blobs"],
        "r2_extra_pins": dict(EXTRA_PINS),
        "tracked_clean": initial["tracked_clean"],
        "origin_develop_matches_head": initial["origin_develop_matches_head"],
    }


def validate_r1(report: dict[str, object]) -> list[dict[str, object]]:
    """Reject synthetic, stale-shaped, incomplete or promoted R1 evidence."""
    if not isinstance(report, dict):
        raise RuntimeError("R2_R1_NOT_AN_OBJECT")
    if (report.get("phase") != "175-R1"
            or report.get("mode") != "READ_ONLY_AUDIT"
            or report.get("dry_run") is not False
            or report.get("result") != "PASS_R1_AUDIT_WITH_PROOF_GAPS"
            or report.get("tracked_unchanged") is not True
            or report.get("production_changes") != []
            or report.get("new_given") != 0
            or report.get("new_mathematical_rules") != 0
            or report.get("full_pytest_executed") is not False):
        raise RuntimeError("R2_R1_EVIDENCE_CONTRACT_MISMATCH")
    before = report.get("preflight")
    if not isinstance(before, dict) or before.get("tracked_clean") is not True:
        raise RuntimeError("R2_R1_PREFLIGHT_MISSING")
    rows = report.get("rows")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED_STATUSES):
        raise RuntimeError("R2_R1_SIX_ROWS_REQUIRED")
    by_pair: dict[tuple[int, int], dict[str, object]] = {}
    for row in rows:
        if not isinstance(row, dict) or type(row.get("n")) is not int or type(row.get("k")) is not int:
            raise RuntimeError("R2_R1_INVALID_COORDINATES")
        pair = (row["n"], row["k"])
        if pair not in EXPECTED_STATUSES or pair in by_pair:
            raise RuntimeError("R2_R1_DUPLICATE_OR_UNKNOWN_GROUP")
        if (row.get("audit_result") != EXPECTED_STATUSES[pair]
                or row.get("db_goal_typed") is not True
                or row.get("group") != f"pi_{pair[0]+pair[1]}^{pair[0]}"):
            raise RuntimeError("R2_R1_GROUP_STATUS_CHANGED: " + str(pair))
        if pair in OPEN_COUNTS:
            goals = row.get("search_open_goals")
            if (row.get("search_status") != "search_failed"
                    or row.get("search_proven_count") != 0
                    or row.get("search_open_count") != OPEN_COUNTS[pair]
                    or not isinstance(goals, list)
                    or len(goals) != OPEN_COUNTS[pair]
                    or not all(isinstance(g, str) and g for g in goals)
                    or row.get("web_key") != "generic-partial-proof"
                    or row.get("web_partial") is not True
                    or row.get("search_conclusion_is_none") is not True
                    or row.get("references") != []):
                raise RuntimeError("R2_R1_UNFINISHED_EVIDENCE_CHANGED: " + str(pair))
            if pair in ((3, 4), (5, 4)):
                if not goals[0].startswith("CyclicStructureStatement("):
                    raise RuntimeError("R2_R1_CYCLIC_GOAL_MISSING: " + str(pair))
                if not goals[1].startswith("Relation(") or not goals[2].startswith("Relation("):
                    raise RuntimeError("R2_R1_GROUP_RELATION_GOALS_MISSING: " + str(pair))
            else:
                if (not goals[0].startswith("MapSurjective(")
                        or not goals[1].startswith("TodaPrimaryGroupZeroStatement(")):
                    raise RuntimeError("R2_R1_DELTA_GOAL_MISSING")
        by_pair[pair] = row
    if set(by_pair) != set(EXPECTED_STATUSES):
        raise RuntimeError("R2_R1_SIX_ROWS_REQUIRED")
    counts = report.get("summary")
    if (not isinstance(counts, dict) or counts.get("checked") != 6
            or counts.get("complete") != 3 or counts.get("unfinished") != 3
            or counts.get("execution_or_trust_failures") != 0):
        raise RuntimeError("R2_R1_COUNTS_CHANGED")
    return [by_pair[pair] for pair in UNFINISHED]


def select_r1_report(root: Path, explicit: Path | None) -> Path:
    """Find real, complete R1 evidence; never use a DryRun or invent a result."""
    if explicit is not None:
        if not explicit.is_file():
            raise RuntimeError("R2_R1_REPORT_NOT_FOUND: " + str(explicit))
        return explicit.resolve()
    parent = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    base = parent / "EHPProofTracerAudit" / R1_PACKAGE
    candidates = sorted(base.glob("*/report.json"), reverse=True)
    for candidate in candidates:
        try:
            validate_r1(json.loads(candidate.read_text(encoding="utf-8")))
            return candidate
        except (RuntimeError, ValueError, OSError, UnicodeError, json.JSONDecodeError):
            continue
    raise RuntimeError("R2_NO_VALID_R1_REPORT: run Phase 175 R1 normally first")


def verify_provenance(
    report: dict[str, object], checked: dict[str, object],
    *, root: Path | None = None,
) -> dict[str, object]:
    """Accept identical HEADs or a strictly audit-only R1 descendant merge.

    Never accept a changed production source, changed R1 pin, unrelated commit,
    rewritten history, or modification/deletion of a historical file.
    """
    from phase175_r1_k4_audit.audit import SOURCE_BLOBS, REVIEWED_MAIN_MERGE

    before = report["preflight"]
    if (before.get("source_blobs") != SOURCE_BLOBS
            or checked.get("r1_pins") != SOURCE_BLOBS
            or before.get("reviewed_phase174_main_merge") != REVIEWED_MAIN_MERGE
            or before.get("branch") != "develop"
            or checked.get("branch") != "develop"):
        raise RuntimeError("R2_R1_SOURCE_LINEAGE_CHANGED: source pins or reviewed baseline")

    old_head = before.get("head")
    new_head = checked.get("head")
    if old_head == new_head:
        return {
            "mode": "SAME_HEAD", "r1_head": old_head,
            "r2_head": new_head, "audit_only_added_paths": [],
        }

    # A legitimate post-R1 merge can add the R1 audit package, which was
    # untracked during the real R1 run. Check the actual Git DAG, not a guessed
    # successor SHA. Do not permit changes to any pre-existing tracked file.
    if (root is None
            or not isinstance(old_head, str)
            or not isinstance(new_head, str)
            or re.fullmatch(r"[0-9a-f]{40}", old_head) is None
            or re.fullmatch(r"[0-9a-f]{40}", new_head) is None):
        raise RuntimeError("R2_R1_SOURCE_LINEAGE_CHANGED: unverified different HEADs")

    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", old_head, new_head],
        cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("R2_R1_SOURCE_LINEAGE_CHANGED: R1 HEAD not an ancestor")

    changes = git(
        root, "diff", "--name-status", "--no-renames", old_head, new_head,
    )
    entries = tuple(line.split("\t", 1) for line in changes.splitlines())
    if (not entries
            or any(len(entry) != 2
                   or entry[0] != "A"
                   or not entry[1].startswith("phase175_r1_k4_audit/")
                   or entry[1].endswith("/")
                   for entry in entries)):
        raise RuntimeError(
            "R2_R1_SOURCE_LINEAGE_CHANGED: post-R1 changes are not audit-only additions"
        )
    return {
        "mode": "AUDIT_ONLY_DESCENDANT", "r1_head": old_head,
        "r2_head": new_head,
        "audit_only_added_paths": [entry[1] for entry in entries],
    }


def source_frontier(root: Path) -> dict[str, object]:
    """Read real positioned source leaves and screen them for the zero root.

    This function neither runs inference nor treats a cited target as its own
    proved root. It reports absence of a screened source honestly.
    """
    from homotopy_groups import (
        FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
    )
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase170_r3_r6_prop58_source import _source_checked_pi73_relation
    from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
        build_cited_lower_delta_sources, checked_prior_statements,
        reviewed_source_positions,
    )
    from phase174_r3_r7_r18_delta_image_surjectivity.rule import delta_surjectivity_image_inputs
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import cyclic_generator_inputs
    from proof import ProofRule, Relation
    from toda_rules import TodaDeltaImageUpToSignStatement
    from unified_statement_registry import AssertionOrigin

    bridge = build_shared_typed_bridge()
    goal73 = exact_prior_database_result(3, 4)
    goal95 = exact_prior_database_result(5, 4)
    goal106 = exact_prior_database_result(6, 4)
    if (goal73 is None or goal95 is None
            or goal106 != TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))):
        raise RuntimeError("R2_REGISTERED_GOAL_CHANGED")
    p73 = _source_checked_pi73_relation(bridge)
    if p73 != goal73:
        raise RuntimeError("R2_PROP58_PI73_TYPED_MISMATCH")
    p95, image = checked_prior_statements(root)
    if p95 != goal95:
        raise RuntimeError("R2_PROP58_PI95_TYPED_MISMATCH")
    if (not isinstance(p95, Relation)
            or not isinstance(p95.rhs, FiniteCyclicGroup)
            or p95.rhs.order != 2
            or not isinstance(image, TodaDeltaImageUpToSignStatement)):
        raise RuntimeError("R2_FINITE_CYCLIC_IMAGE_UNTYPED")
    lower_delta = TodaDeltaMap(TodaPrimaryGroup(11, 11), TodaPrimaryGroup(9, 5))
    if image.map != lower_delta or image.positive_value != p95.rhs.generator:
        raise RuntimeError("R2_DELTA_IMAGE_GENERATOR_MISMATCH")
    cited = build_cited_lower_delta_sources(root)
    if (len(cited.proof_links) != 2
            or tuple(link.step.conclusion for link in cited.proof_links) != (p95, image)
            or any(link.step.rule is not ProofRule.GIVEN for link in cited.proof_links)):
        raise RuntimeError("R2_TWO_CITED_PRIOR_FACTS_CHANGED")
    screen = screen_independent_sources_for_derived_goal(bridge, goal=goal106)
    screened = []
    for expected, locator in ((p95, "Proposition 5.8"), (image, "(5.10)")):
        match = []
        for link in screen.proof_links:
            if link.step is None or link.step.rule is not ProofRule.GIVEN:
                continue
            if link.step.conclusion != expected:
                continue
            assertion = screen.registry.assertion(link.assertion_id)
            reference = screen.registry.reference(assertion.reference_id)
            if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                    and reference.locator == locator):
                match.append({
                    "assertion_id": link.assertion_id,
                    "locator": reference.locator,
                    "source_id": reference.source_id,
                    "publication_position": reference.publication_position,
                })
        screened.append({"locator": locator, "matches": match, "screened_count": len(match)})
    # R18's free-cyclic implication cannot be reused as a finite-cyclic rule.
    # A failure here would mean the old rule was silently broadened.
    old_free_delta_inputs = delta_surjectivity_image_inputs(MapSurjective(lower_delta), p95)
    old_free_generator_inputs = cyclic_generator_inputs(p95)
    if old_free_delta_inputs is not None or old_free_generator_inputs is not None:
        raise RuntimeError("R2_FREE_CYCLIC_RULE_SCOPE_DRIFT")
    return {
        "pi_7_3": {
            "printed_prop58_checked": True, "typed_relation_matches_db": True,
            "source_is_independent_complete_proof": False,
            "note": "Existing Proposition 5.8 clause is not a completed R1 root proof",
        },
        "pi_9_5": {
            "printed_prop58_checked": True, "typed_relation_matches_db": True,
            "finite_cyclic_order": p95.rhs.order,
            "source_is_independent_complete_proof": False,
        },
        "pi_10_6": {
            "checked_delta_domain": repr(lower_delta.source_group),
            "checked_delta_codomain": repr(lower_delta.target_group),
            "printed_equation_510_checked": True,
            "typed_image_generator_matches_pi_9_5": True,
            "verified_cited_prior_source_leaves": 2,
            "source_publication_positions": list(reviewed_source_positions()),
            "screened_prior_sources_for_zero_goal": screened,
            "finite_cyclic_surjectivity_inferred": False,
            "zero_group_proved": False,
        },
        "existing_rules": {
            "R18_free_cyclic_delta_rule_applicable": False,
            "R56_free_cyclic_generator_rule_applicable": False,
            "finite_cyclic_inference_path_audit_required": True,
        },
    }


def source_worker(root: Path) -> int:
    """Run typed source inventory in isolation from report writing."""
    try:
        result = {"status": "PASS_SOURCE_INVENTORY", "data": source_frontier(root)}
    except Exception as exc:
        result = {"status": "SOURCE_WORKER_ERROR", "error": str(exc),
                  "traceback": traceback.format_exc()[-6000:]}
    print(MARKER + json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


def launch_source_worker(root: Path, timeout_seconds: int, target: Path) -> dict[str, object]:
    """Isolate live registry/manifest screening and retain diagnostics."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        completed = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker", "--root", str(root)],
            cwd=root, env=env, capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        text = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        (target / "source_worker.log").write_text(text, encoding="utf-8")
        return {"status": "SOURCE_WORKER_TIMEOUT", "timeout_seconds": timeout_seconds}
    (target / "source_worker.log").write_text(
        completed.stdout + "\nSTDERR:\n" + completed.stderr, encoding="utf-8",
    )
    markers = [line[len(MARKER):] for line in completed.stdout.splitlines()
               if line.startswith(MARKER)]
    if completed.returncode or len(markers) != 1:
        return {"status": "SOURCE_WORKER_INVALID", "exit_code": completed.returncode,
                "marker_count": len(markers)}
    try:
        data = json.loads(markers[0])
    except json.JSONDecodeError:
        return {"status": "SOURCE_WORKER_INVALID_JSON"}
    if not isinstance(data, dict) or data.get("status") not in (
        "PASS_SOURCE_INVENTORY", "SOURCE_WORKER_ERROR",
    ):
        return {"status": "SOURCE_WORKER_INVALID_PAYLOAD"}
    return data


def write_json(path: Path, report: dict[str, object]) -> None:
    """Atomic report write outside the Git checkout."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def write_markdown(path: Path, report: dict[str, object]) -> None:
    """Summarize actual R1 obligations and live source-screening evidence."""
    frontier = report["source_worker"]["data"]
    lower = frontier["pi_10_6"]
    lines = [
        "# Phase 175 R2 — $k=4$ 未完成3群の Source-first Frontier Audit", "",
        "監査のみ。数学規則・GIVEN・既存 Proof Tree・Web Renderer の変更なし。", "",
        f"- Git HEAD: `{report['preflight']['head']}`",
        f"- R1 証拠: `{report['r1_report']}`",
        "- R1 の未完成: $\\pi_7^3$, $\\pi_9^5$, $\\pi_{10}^6$（いずれも ProofStep 0）", "",
        "## 検証済み文献前提（完成証明ではない）", "",
        "- Toda Proposition 5.8: $\\pi_7^3=\\mathbb Z/2\\{\\nu'\\eta_6\\}$ を型付き照合", 
        "- Toda Proposition 5.8: $\\pi_9^5=\\mathbb Z/2\\{\\nu_5\\eta_8\\}$ を型付き照合", 
        "- Toda (5.10): $\\Delta(\\iota_{11})=\\nu_5\\eta_8$ を型付き照合", "",
        "## $\\pi_{10}^6$ の先行文献ソース Screen", "",
    ]
    for item in lower["screened_prior_sources_for_zero_goal"]:
        lines.append(f"- `{item['locator']}`: {item['screened_count']} 件（型付き・位置付き FIXED_STATEMENT）")
    lines += [
        "", "## 未解決の境界", "",
        "1. $\\pi_7^3$：記名生成元に関する巡回構造の独立した推論鎖が未完成", 
        "2. $\\pi_9^5$：記名生成元に関する巡回構造の独立した推論鎖が未完成", 
        "3. $\\pi_{10}^6$：位数2の生成元が $\\Delta(\\iota_{11})$ の像である事実から全射性を示す接続を監査。EHP 完全性との接続も未証明", "",
        "R18/R56 の自由巡回群向け規則を有限巡回群へそのまま流用しない。", 
        "次工程では数学的に一般的な有限巡回群の全射性推論の既存実装と Source-first provider 接続を調べる。", 
        "この監査は新規 ProofStep を作成せず、未完成を Complete に昇格しない。", 
        "全体 pytest は Phase 175 終了時のみ実施する。", "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def run(root: Path, dry_run: bool, r1_path: Path | None, timeout_seconds: int) -> int:
    """Pin R1 evidence, check code, optionally inspect live cited source leaves."""
    parent = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    target = parent / "EHPProofTracerAudit" / PACKAGE / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    )
    target.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R2", "mode": "READ_ONLY_FRONTIER_AUDIT",
        "dry_run": dry_run, "full_pytest_executed": False,
        "production_changes": [], "new_given": 0, "new_mathematical_rules": 0,
        "result": "NOT_STARTED", "report_dir": str(target),
    }
    checked = None
    code = 2
    print("PHASE175_R2_OUTPUT=" + str(target), flush=True)
    try:
        checked = preflight(root)
        report["preflight"] = checked
        path = select_r1_report(root, r1_path)
        r1_report = json.loads(path.read_text(encoding="utf-8"))
        rows = validate_r1(r1_report)
        lineage = verify_provenance(r1_report, checked, root=root)
        report["r1_lineage"] = lineage
        report["r1_report"] = str(path)
        report["r1_root_status"] = [
            {"group": row["group"], "status": row["search_status"],
             "proven_steps": row["search_proven_count"],
             "open_goals": row["search_open_goals"],
             "diagnostics": row.get("search_diagnostics", []),
             "source_references": row.get("references", [])}
            for row in rows
        ]
        print("PHASE175_R2_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R2_SOURCE_PINS=" + str(len(checked["r1_pins"]) + len(EXTRA_PINS)), flush=True)
        print("PHASE175_R2_R1_EVIDENCE=PASS", flush=True)
        print("PHASE175_R2_R1_LINEAGE=" + str(lineage["mode"]), flush=True)
        print("PHASE175_R2_R1_AUDIT_ONLY_ADDITIONS=" +
              str(len(lineage["audit_only_added_paths"])), flush=True)
        print("PHASE175_R2_INCOMPLETE_GROUPS=3", flush=True)
        if dry_run:
            report["result"] = "PASS_R2_READ_ONLY_DRYRUN"
            code = 0
        else:
            result = launch_source_worker(root, timeout_seconds, target)
            report["source_worker"] = result
            if result["status"] != "PASS_SOURCE_INVENTORY":
                raise RuntimeError("R2_SOURCE_FRONTIER_NOT_CERTIFIED: " + str(result))
            source = result["data"]
            for item in source["pi_10_6"]["screened_prior_sources_for_zero_goal"]:
                print("PHASE175_R2_SCREENED=" + item["locator"] + ":" + str(item["screened_count"]), flush=True)
            report["result"] = "PASS_R2_SOURCE_FRONTIER_RECORDED"
            write_markdown(target / "report.md", report)
            code = 0
    except Exception as exc:
        report["result"] = "R2_REFUSED_OR_SOURCE_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-6000:]
        print("PHASE175_R2_ERROR=" + report["error"], flush=True)
        code = 2
    finally:
        if checked is not None:
            try:
                after = preflight(root)
                report["tracked_unchanged"] = after == checked
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)
            if report["tracked_unchanged"] is not True:
                report["result"] = "R2_TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_json(target / "report.json", report)
        print("PHASE175_R2_REPORT=" + str(target / "report.json"), flush=True)
        print("PHASE175_R2_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE175_R2_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return code


def main() -> int:
    """Command-line entrypoint; worker is reserved for source inventory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--r1-report", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("--timeout-seconds must be positive")
    root = args.root.resolve()
    if args.worker:
        return source_worker(root)
    return run(root, args.dry_run, args.r1_report, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
