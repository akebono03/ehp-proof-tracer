# Phase 175 R2R1 — 置換用コード全文

既存の本番ファイル・クラス・関数は変更しない。R2 監査専用の以下のファイルのみを上書きする。`audit.py` の `verify_provenance()` と `run()` はそれぞれ関数全文であり、import 部分も省略していない。`tests/test_audit.py` の変更・追加された全テスト関数を含むファイル全文を提示する。コードに省略記号は使用していない。

- 変更 `phase175_r2_k4_frontier_audit/audit.py`：`re` を import、`verify_provenance()` と `run()` の全関数を置換。
- 変更 `phase175_r2_k4_frontier_audit/tests/test_audit.py`：`subprocess` を import、既存の `test_provenance_must_match_reviewed_source_pins()` 全体を置換。新テスト関数は同一ファイル内の `test_preflight_pins_extra_dependencies_and_r1_preflight()` の**直前**に挿入。
- `run.ps1` は変更なし。既存 API と Source-first の信頼境界を維持。
- `README.md` は英語、`AUDIT_PLAN_JA.md` は日本語。プロジェクト主要5文書は変更なし。

## `phase175_r2_k4_frontier_audit/audit.py` 全文

```python
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
```

## `phase175_r2_k4_frontier_audit/tests/test_audit.py` 全文

```python
"""Focused fail-closed R2 contracts using synthetic evidence only in tests."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest

from phase175_r2_k4_frontier_audit import audit


def fixture_r1() -> dict[str, object]:
    """Test-only shape; never a fabricated production report."""
    rows = []
    for (n, k), status in audit.EXPECTED_STATUSES.items():
        incomplete = (n, k) in audit.OPEN_COUNTS
        if (n, k) in ((3, 4), (5, 4)):
            goals = [
                "CyclicStructureStatement(group=sample, generator=sample, order=2)",
                "Relation(lhs=sample, rhs=sample)",
                "Relation(lhs=sample, rhs=sample)",
            ]
        elif (n, k) == (6, 4):
            goals = [
                "MapSurjective(map=TodaDeltaMap(source_group=sample, target_group=sample))",
                "TodaPrimaryGroupZeroStatement(group=sample)",
            ]
        else:
            goals = []
        rows.append({
            "n": n, "k": k, "group": f"pi_{n+k}^{n}",
            "audit_result": status, "db_goal_typed": True,
            "search_status": "search_failed" if incomplete else "complete",
            "search_open_count": len(goals), "search_open_goals": goals,
            "search_proven_count": 0 if incomplete else 8,
            "search_conclusion_is_none": incomplete,
            "web_key": "generic-partial-proof" if incomplete else "generic-complete-proof",
            "web_partial": incomplete,
            "references": [],
            "search_diagnostics": ["no verified derivation"] if incomplete else [],
        })
    return {
        "phase": "175-R1", "mode": "READ_ONLY_AUDIT",
        "dry_run": False, "result": "PASS_R1_AUDIT_WITH_PROOF_GAPS",
        "tracked_unchanged": True,
        "production_changes": [], "new_given": 0,
        "new_mathematical_rules": 0, "full_pytest_executed": False,
        "preflight": {"tracked_clean": True, "branch": "develop", "head": "sample-head"},
        "summary": {"checked": 6, "complete": 3, "unfinished": 3,
                    "execution_or_trust_failures": 0},
        "rows": rows,
    }


def test_R1_six_group_contract_accepts_only_three_observed_gaps() -> None:
    found = audit.validate_r1(fixture_r1())
    assert [(row["n"], row["k"]) for row in found] == list(audit.UNFINISHED)
    assert [row["search_open_count"] for row in found] == [3, 3, 2]
    assert all(row["search_proven_count"] == 0 for row in found)


@pytest.mark.parametrize("field,value", [
    ("phase", "174-R74"),
    ("mode", "PROOF_PATCH"),
    ("dry_run", True),
    ("result", "PASS_R1_READ_ONLY_DRYRUN"),
    ("tracked_unchanged", False),
    ("production_changes", ["production.py"]),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("full_pytest_executed", True),
])
def test_reject_unreviewed_or_mutating_r1_report(field: str, value: object) -> None:
    report = fixture_r1()
    report[field] = value
    with pytest.raises(RuntimeError, match="EVIDENCE_CONTRACT_MISMATCH"):
        audit.validate_r1(report)


def test_r1_requires_full_exact_six_group_coverage() -> None:
    report = fixture_r1()
    report["rows"].pop()
    with pytest.raises(RuntimeError, match="SIX_ROWS_REQUIRED"):
        audit.validate_r1(report)
    report = fixture_r1()
    report["rows"].append(deepcopy(report["rows"][0]))
    with pytest.raises(RuntimeError, match="SIX_ROWS_REQUIRED"):
        audit.validate_r1(report)
    report = fixture_r1()
    report["rows"][0] = deepcopy(report["rows"][1])
    with pytest.raises(RuntimeError, match="DUPLICATE_OR_UNKNOWN_GROUP"):
        audit.validate_r1(report)


@pytest.mark.parametrize("pair,bad_status", [
    ((3, 4), "COMPLETE_AND_WEB_VERIFIED"),
    ((5, 4), "COMPLETE_AND_WEB_VERIFIED"),
    ((6, 4), "COMPLETE_AND_WEB_VERIFIED"),
    ((2, 4), "INCOMPLETE_AND_WEB_CONFIRMED"),
])
def test_never_promote_unknown_gap_to_complete(pair: tuple[int, int], bad_status: str) -> None:
    report = fixture_r1()
    target = next(row for row in report["rows"] if (row["n"], row["k"]) == pair)
    target["audit_result"] = bad_status
    with pytest.raises(RuntimeError, match="GROUP_STATUS_CHANGED"):
        audit.validate_r1(report)


def test_requires_type_checked_cyclic_root_obligations() -> None:
    report = fixture_r1()
    row = next(row for row in report["rows"] if row["n"] == 3)
    row["search_open_goals"][0] = "A claim typed only as prose"
    with pytest.raises(RuntimeError, match="CYCLIC_GOAL_MISSING"):
        audit.validate_r1(report)
    report = fixture_r1()
    row = next(row for row in report["rows"] if row["n"] == 5)
    row["search_open_goals"].pop()
    with pytest.raises(RuntimeError, match="UNFINISHED_EVIDENCE_CHANGED"):
        audit.validate_r1(report)


def test_requires_true_delta_surjectivity_obligation() -> None:
    report = fixture_r1()
    row = next(row for row in report["rows"] if row["n"] == 6)
    row["search_open_goals"][0] = "TodaDeltaMap(no surjectivity proof)"
    with pytest.raises(RuntimeError, match="DELTA_GOAL_MISSING"):
        audit.validate_r1(report)


def test_r1_summary_discrepancy_is_failure() -> None:
    report = fixture_r1()
    report["summary"]["complete"] = 6
    with pytest.raises(RuntimeError, match="COUNTS_CHANGED"):
        audit.validate_r1(report)


def test_choose_latest_valid_r1_without_selecting_dryrun(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    base = tmp_path / "EHPProofTracerAudit" / audit.R1_PACKAGE
    older = base / "20261111T074852_297718Z"
    newer = base / "20261111T075000_000000Z"
    older.mkdir(parents=True)
    newer.mkdir(parents=True)
    good = fixture_r1()
    (older / "report.json").write_text(json.dumps(good), encoding="utf-8")
    bad = deepcopy(good)
    bad["dry_run"] = True
    (newer / "report.json").write_text(json.dumps(bad), encoding="utf-8")
    assert audit.select_r1_report(tmp_path, None) == older / "report.json"
    assert audit.select_r1_report(tmp_path, older / "report.json") == (older / "report.json").resolve()
    with pytest.raises(RuntimeError, match="REPORT_NOT_FOUND"):
        audit.select_r1_report(tmp_path, tmp_path / "unknown.json")


def test_provenance_must_match_reviewed_source_pins() -> None:
    from phase175_r1_k4_audit.audit import SOURCE_BLOBS, REVIEWED_MAIN_MERGE

    report = fixture_r1()
    report["preflight"].update({
        "source_blobs": dict(SOURCE_BLOBS),
        "reviewed_phase174_main_merge": REVIEWED_MAIN_MERGE,
    })
    checked = {"head": "sample-head", "branch": "develop", "r1_pins": dict(SOURCE_BLOBS)}
    audit.verify_provenance(report, checked)
    report["preflight"]["head"] = "unreviewed-head"
    with pytest.raises(RuntimeError, match="SOURCE_LINEAGE_CHANGED"):
        audit.verify_provenance(report, checked)


def reviewed_provenance_fixture() -> tuple[dict[str, object], dict[str, object]]:
    """Use the actual R1 source pins, not invented mathematical source claims."""
    from phase175_r1_k4_audit.audit import SOURCE_BLOBS, REVIEWED_MAIN_MERGE

    report = fixture_r1()
    report["preflight"].update({
        "source_blobs": dict(SOURCE_BLOBS),
        "reviewed_phase174_main_merge": REVIEWED_MAIN_MERGE,
        "head": "4f87fc5722e85f7365250c07e684e959b71ae8bb",
    })
    checked = {
        "head": "b" * 40, "branch": "develop",
        "r1_pins": dict(SOURCE_BLOBS),
    }
    return report, checked


def test_post_r1_merge_accepts_only_added_r1_audit_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    report, checked = reviewed_provenance_fixture()
    paths = (
        "phase175_r1_k4_audit/audit.py",
        "phase175_r1_k4_audit/tests/test_audit.py",
    )
    changes = "\n".join("A\t" + path for path in paths)
    calls: list[tuple[str, ...]] = []

    def fake_git(root: Path, *args: str) -> str:
        assert root == tmp_path
        calls.append(args)
        return changes

    def fake_run(argv: list[str], **kwargs: object) -> SimpleNamespace:
        assert argv[:3] == ["git", "merge-base", "--is-ancestor"]
        assert argv[3:] == [report["preflight"]["head"], checked["head"]]
        assert kwargs["cwd"] == tmp_path
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(audit, "git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", fake_run)
    result = audit.verify_provenance(report, checked, root=tmp_path)
    assert result["mode"] == "AUDIT_ONLY_DESCENDANT"
    assert result["audit_only_added_paths"] == list(paths)
    assert len(calls) == 1
    assert calls[0][:3] == ("diff", "--name-status", "--no-renames")


@pytest.mark.parametrize("changed", [
    "M\tphase165_r52_r9_shared_math.py",
    "A\tphase175_r1_k4_audit/audit.py\nM\tweb_group_proof.py",
    "M\tphase175_r1_k4_audit/audit.py",
    "D\tphase175_r1_k4_audit/audit.py",
    "A\tphase175_r2_k4_frontier_audit/audit.py",
    "A\tREADME.md",
    "",
])
def test_post_r1_merge_rejects_other_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, changed: str,
) -> None:
    report, checked = reviewed_provenance_fixture()
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0))
    monkeypatch.setattr(audit, "git", lambda *a: changed)
    with pytest.raises(RuntimeError, match="SOURCE_LINEAGE_CHANGED"):
        audit.verify_provenance(report, checked, root=tmp_path)


def test_post_r1_merge_rejects_unrelated_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    report, checked = reviewed_provenance_fixture()
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=1))
    monkeypatch.setattr(audit, "git", lambda *a: "A\tphase175_r1_k4_audit/audit.py")
    with pytest.raises(RuntimeError, match="not an ancestor"):
        audit.verify_provenance(report, checked, root=tmp_path)


def test_post_r1_merge_requires_real_sha_and_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    report, checked = reviewed_provenance_fixture()
    report["preflight"]["head"] = "not-a-git-sha"
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: pytest.fail("must not run git"))
    with pytest.raises(RuntimeError, match="unverified different HEADs"):
        audit.verify_provenance(report, checked, root=tmp_path)
    report, checked = reviewed_provenance_fixture()
    with pytest.raises(RuntimeError, match="unverified different HEADs"):
        audit.verify_provenance(report, checked)


def test_same_head_needs_no_git_ancestry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report, checked = reviewed_provenance_fixture()
    checked["head"] = report["preflight"]["head"]
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: pytest.fail("must not run git"))
    result = audit.verify_provenance(report, checked)
    assert result["mode"] == "SAME_HEAD"
    assert result["audit_only_added_paths"] == []


def test_post_r1_merge_rejects_source_pin_or_base_drift() -> None:
    report, checked = reviewed_provenance_fixture()
    report["preflight"]["source_blobs"]["data/sphere.csv"] = "unreviewed"
    with pytest.raises(RuntimeError, match="source pins or reviewed baseline"):
        audit.verify_provenance(report, checked)
    report, checked = reviewed_provenance_fixture()
    report["preflight"]["reviewed_phase174_main_merge"] = "unreviewed"
    with pytest.raises(RuntimeError, match="source pins or reviewed baseline"):
        audit.verify_provenance(report, checked)


def test_real_git_history_accepts_only_r1_audit_commit(tmp_path: Path) -> None:
    """Exercise actual merge-base and diff commands in a temporary repository."""
    def git_command(*args: str) -> str:
        cmd = subprocess.run(
            ["git", *args], cwd=tmp_path, text=True,
            capture_output=True, encoding="utf-8", check=True,
        )
        return cmd.stdout.strip()

    git_command("init", "-q")
    (tmp_path / "tracked_source.txt").write_text("unchanged source\n", encoding="utf-8")
    git_command("add", "tracked_source.txt")
    git_command("-c", "user.name=Audit Test", "-c", "user.email=audit@example.invalid",
                "commit", "-qm", "baseline")
    old_head = git_command("rev-parse", "HEAD")

    audit_dir = tmp_path / "phase175_r1_k4_audit"
    audit_dir.mkdir()
    (audit_dir / "audit.py").write_text("# read only audit\n", encoding="utf-8")
    git_command("add", "phase175_r1_k4_audit/audit.py")
    git_command("-c", "user.name=Audit Test", "-c", "user.email=audit@example.invalid",
                "commit", "-qm", "R1 audit added")
    merged_head = git_command("rev-parse", "HEAD")

    report, checked = reviewed_provenance_fixture()
    report["preflight"]["head"] = old_head
    checked["head"] = merged_head
    result = audit.verify_provenance(report, checked, root=tmp_path)
    assert result["mode"] == "AUDIT_ONLY_DESCENDANT"
    assert result["audit_only_added_paths"] == ["phase175_r1_k4_audit/audit.py"]

    (tmp_path / "tracked_source.txt").write_text("changed source\n", encoding="utf-8")
    git_command("add", "tracked_source.txt")
    git_command("-c", "user.name=Audit Test", "-c", "user.email=audit@example.invalid",
                "commit", "-qm", "unreviewed production edit")
    checked["head"] = git_command("rev-parse", "HEAD")
    with pytest.raises(RuntimeError, match="SOURCE_LINEAGE_CHANGED"):
        audit.verify_provenance(report, checked, root=tmp_path)


def test_preflight_pins_extra_dependencies_and_r1_preflight(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import phase175_r1_k4_audit.audit as r1_audit

    def fake_r1(_root: Path) -> dict[str, object]:
        return {"head": "reviewed", "branch": "develop", "tracked_clean": True,
                "source_blobs": {"a.py": "old"}, "origin_develop_matches_head": True}

    monkeypatch.setattr(r1_audit, "preflight", fake_r1)
    monkeypatch.setattr(audit, "git", lambda _root, *args: audit.EXTRA_PINS[args[1][5:]])
    for path in audit.EXTRA_PINS:
        f = tmp_path / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("source", encoding="utf-8")
    assert len(audit.preflight(tmp_path)["r2_extra_pins"]) == len(audit.EXTRA_PINS)
    next(iter(audit.EXTRA_PINS))
    changed = next(iter(audit.EXTRA_PINS))
    monkeypatch.setattr(audit, "git", lambda _root, *args: "unreviewed")
    with pytest.raises(RuntimeError, match="PIN_MISMATCH"):
        audit.preflight(tmp_path)
    monkeypatch.setattr(audit, "git", lambda _root, *args: audit.EXTRA_PINS[args[1][5:]])
    (tmp_path / changed).unlink()
    with pytest.raises(RuntimeError, match="SOURCE_MISSING"):
        audit.preflight(tmp_path)


def test_worker_fail_closed_on_missing_or_forged_marker(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(*args: object, **kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(returncode=0, stdout="no trusted marker", stderr="")

    monkeypatch.setattr(audit.subprocess, "run", fake_run)
    result = audit.launch_source_worker(tmp_path, 30, tmp_path)
    assert result["status"] == "SOURCE_WORKER_INVALID"
    assert (tmp_path / "source_worker.log").is_file()


def test_markdown_never_promotes_unproved_root(tmp_path: Path) -> None:
    record = {
        "preflight": {"head": "reviewed"}, "r1_report": "R1 report",
        "source_worker": {
            "data": {
                "pi_10_6": {
                    "screened_prior_sources_for_zero_goal": [
                        {"locator": "Proposition 5.8", "screened_count": 1},
                        {"locator": "(5.10)", "screened_count": 1},
                    ]
                }
            }
        },
    }
    path = tmp_path / "report.md"
    audit.write_markdown(path, record)
    text = path.read_text(encoding="utf-8")
    assert "EHP" in text
    assert "未解決" in text
    assert "ProofStep" in text
    assert "完成証明ではない" in text


def test_r2_only_writes_to_explicit_report_path(tmp_path: Path) -> None:
    report_path = tmp_path / "report.json"
    report = {"phase": "175-R2", "new_given": 0,
              "new_mathematical_rules": 0, "production_changes": []}
    audit.write_json(report_path, report)
    assert json.loads(report_path.read_text(encoding="utf-8")) == report
    assert list(tmp_path.iterdir()) == [report_path]
```

## `phase175_r2_k4_frontier_audit/run.ps1` 全文

```powershell
param(
    [switch]$DryRun,
    [string]$R1Report = '',
    [ValidateRange(1, 7200)][int]$TimeoutSeconds = 240
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
        if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python is required' }
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is required' }
        Write-Output 'PHASE175_R2_GIT_STATUS_BEFORE'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R2 Git status before failed' }

        & python -B -m pytest -q --disable-warnings -p no:cacheprovider -o addopts= `
            --import-mode=importlib '.\phase175_r2_k4_frontier_audit\tests\test_audit.py' `
            '.\phase175_r1_k4_audit\tests\test_audit.py' `
            '.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_source.py'
        if ($LASTEXITCODE -ne 0) { throw 'R2 focused pytest failed' }
        Write-Output 'PHASE175_R2_FOCUSED_PYTEST=PASS'

        $Arguments = @(
            '-B', '-m', 'phase175_r2_k4_frontier_audit.audit',
            '--root', $RepoRoot, '--timeout-seconds', [string]$TimeoutSeconds
        )
        if ($DryRun) { $Arguments += '--dry-run' }
        if ($R1Report.Trim()) { $Arguments += @('--r1-report', $R1Report) }
        & python @Arguments
        $AuditExitCode = $LASTEXITCODE

        Write-Output 'PHASE175_R2_GIT_STATUS_AFTER'
        & git status -sb
        if ($LASTEXITCODE -ne 0) { throw 'R2 Git status after failed' }
        if ($AuditExitCode -ne 0) { throw "R2 audit failed or requires investigation: $AuditExitCode" }
        Write-Output 'PHASE175_R2=PASS'
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

## `phase175_r2_k4_frontier_audit/__init__.py` 全文

```python
"""Phase 175 R2 source-first, read-only frontier audit."""
```

