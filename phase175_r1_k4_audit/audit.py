"""Phase 175 R1: read-only audit of all six registered k=4 group proofs.

The project proof engine, references and Web renderer are observed, not edited.
Each actual proof search runs in its own subprocess and can time out independently.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback


PACKAGE = "phase175_r1_k4_audit"
REVIEWED_MAIN_MERGE = "4f87fc5722e85f7365250c07e684e959b71ae8bb"
STEM = 4
EXPECTED_GROUPS = tuple((n, STEM) for n in range(2, 8))
WORKER_MARKER = "__PHASE175_R1_K4_WORKER__="
SOURCE_BLOBS = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "phase165_r55_nk_only_goal.py": "e436879f578148fe5c30f5a34974bea3425108b2",
    "phase165_r52_partial_proof.py": "0af6b459ed5a136a8e30a9e349ccf9fa601d448b",
    "phase165_r52_r9_shared_math.py": "9fa11b383812570fae1a26868c98992a5934a327",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase168_r3_4_link_bridge.py": "c3a6233a57c41e61e6649ee33c7a336d7aa1c664",
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_41p13_trust_boundary/verification.py": "547464846ce574d227092a4aacb895d2e2dfefca",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "web_group_proof_common.py": "cb52a4dc2b4c24594f2acf2d76dc6c68ec0947ab",
}
FAILURE_RESULTS = frozenset({
    "WORKER_EXCEPTION", "WORKER_FAILED", "WORKER_TIMEOUT", "WORKER_JSON_INVALID",
    "WORKER_GOAL_MISMATCH", "MISSING_TYPED_DB_GOAL", "UNVERIFIED_COMPLETION",
    "INCOMPLETE_WITH_DISCREPANCY", "UNRECOGNIZED_SEARCH_STATUS",
})


def git(root: Path, *args: str, allow_failure: bool = False) -> tuple[int, str]:
    """Read Git state without fetching, checking out, staging, or committing."""
    process = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode and not allow_failure:
        raise RuntimeError(
            f"R1_GIT_ERROR {args}: {process.stderr.strip()}"
        )
    return process.returncode, process.stdout.strip()


def registered_k4_rows(csv_file: Path) -> dict[tuple[int, int], list[dict[str, str]]]:
    """Read only explicit rows: duplicate CSV summands count as one group."""
    output: dict[tuple[int, int], list[dict[str, str]]] = {}
    with csv_file.open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.DictReader(stream)
        if rows.fieldnames is None or not {"n", "k", "id", "generator", "orders"}.issubset(rows.fieldnames):
            raise ValueError("R1_CSV_HEADERS_CHANGED")
        for line_number, row in enumerate(rows, start=2):
            k_value = (row.get("k") or "").strip()
            if k_value != str(STEM):
                continue
            n_value = (row.get("n") or "").strip()
            if not n_value:  # section separator, not a registered group
                continue
            identifier = (row.get("id") or "").strip()
            if not n_value.isdecimal() or not identifier.isdecimal():
                raise ValueError(f"R1_CSV_INVALID_COORDINATE: line={line_number}")
            n = int(n_value)
            if n < 2:
                raise ValueError(f"R1_CSV_INVALID_SPHERE_DIMENSION: line={line_number}")
            pair = (n, STEM)
            data = {
                "id": identifier, "orders": (row.get("orders") or "").strip(),
                "generator": (row.get("generator") or "").strip(),
            }
            if identifier in {item["id"] for item in output.get(pair, [])}:
                raise ValueError(f"R1_CSV_DUPLICATE_SUMMAND_ID: {pair}")
            output.setdefault(pair, []).append(data)
    if tuple(sorted(output)) != EXPECTED_GROUPS:
        raise RuntimeError(
            f"R1_REGISTERED_SCOPE_CHANGED: actual={tuple(sorted(output))} "
            f"expected={EXPECTED_GROUPS}"
        )
    return output


def preflight(root: Path) -> dict[str, object]:
    """Fail closed on source drift; allow CRLF checkout and newer audit-only HEADs."""
    _, repo_root = git(root, "rev-parse", "--show-toplevel")
    if Path(repo_root).resolve() != root.resolve():
        raise RuntimeError("R1_NOT_GIT_REPOSITORY_ROOT")
    _, branch = git(root, "branch", "--show-current")
    _, head = git(root, "rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("R1_WRONG_BRANCH: expected develop, got " + branch)
    _, tracked = git(root, "status", "--porcelain", "--untracked-files=no")
    if tracked:
        raise RuntimeError("R1_TRACKED_OR_INDEX_CHANGES: " + tracked[:800])
    ancestor_code, _ = git(
        root, "merge-base", "--is-ancestor", REVIEWED_MAIN_MERGE, "HEAD",
        allow_failure=True,
    )
    if ancestor_code:
        raise RuntimeError("R1_REVIEWED_PHASE174_BASE_NOT_ANCESTOR")
    for path, expected in SOURCE_BLOBS.items():
        _, actual = git(root, "rev-parse", "HEAD:" + path)
        if actual != expected or not (root / path).is_file():
            raise RuntimeError(f"R1_SOURCE_PIN_MISMATCH: {path} {actual} != {expected}")
    registrations = registered_k4_rows(root / "data/sphere.csv")
    _, remote = git(root, "rev-parse", "--verify", "origin/develop", allow_failure=True)
    return {
        "branch": branch, "head": head,
        "reviewed_phase174_main_merge": REVIEWED_MAIN_MERGE,
        "origin_develop_observed": remote or None,
        "origin_develop_matches_head": bool(remote and remote == head),
        "source_blobs": dict(SOURCE_BLOBS),
        "registered_groups": len(registrations),
        "registered_summand_rows": sum(map(len, registrations.values())),
        "tracked_clean": True,
    }


def short(value: object, limit: int = 1500) -> str:
    """Safely capture diagnostics and typed goals without serializing live objects."""
    try:
        return str(value)[:limit]
    except Exception as exc:
        return f"<unprintable {type(value).__name__}: {type(exc).__name__}>"


def classify(row: dict[str, object]) -> str:
    """Never promote an unfinished or unverified result to a completed proof."""
    if row.get("exception"):
        return "WORKER_EXCEPTION"
    if row.get("db_goal_typed") is not True:
        return "MISSING_TYPED_DB_GOAL"
    status = row.get("search_status")
    if status == "complete":
        if (
            row.get("search_conclusion_matches_db") is True
            and row.get("search_open_count") == 0
            and isinstance(row.get("search_proven_count"), int)
            and row["search_proven_count"] > 0
            and row.get("trust_verified") is True
            and row.get("model_root_verified") is True
            and row.get("web_key") == "generic-complete-proof"
            and row.get("web_partial") is False
            and isinstance(row.get("web_line_count"), int)
            and row["web_line_count"] > 0
            and not row.get("web_error")
        ):
            return "COMPLETE_AND_WEB_VERIFIED"
        return "UNVERIFIED_COMPLETION"
    if status in ("partial", "search_failed"):
        if (
            row.get("search_conclusion_is_none") is True
            and row.get("search_open_count", 0) > 0
            and row.get("web_key") == "generic-partial-proof"
            and row.get("web_partial") is True
            and not row.get("web_error")
        ):
            return "INCOMPLETE_AND_WEB_CONFIRMED"
        return "INCOMPLETE_WITH_DISCREPANCY"
    return "UNRECOGNIZED_SEARCH_STATUS"


def inspect_one_group(n: int, k: int) -> dict[str, object]:
    """Run real typed search and canonical Web route, recording source-backed steps."""
    row: dict[str, object] = {"n": n, "k": k, "group": f"pi_{n+k}^{n}"}
    try:
        from phase165_r52_partial_proof import ProofSearchStatus
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
        from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
        from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
        from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
        from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
        from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
        from web_group_proof import build_standard_web_group_proof_view

        db = exact_prior_database_result(n, k)
        row["db_goal_typed"] = db is not None
        row["db_goal_type"] = type(db).__name__ if db is not None else None
        row["db_goal_text"] = short(db, 1600) if db is not None else None
        if db is None:
            row["audit_result"] = classify(row)
            return row
        bridge = build_shared_typed_bridge()
        contexts: list[object] = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        row["search_status"] = getattr(result.status, "value", str(result.status))
        row["search_open_count"] = len(result.open_goals)
        row["search_open_goals"] = [short(item) for item in result.open_goals]
        row["search_diagnostics"] = [short(item) for item in result.diagnostics]
        row["search_proven_count"] = len(result.proven_steps)
        row["search_conclusion_is_none"] = result.conclusion is None
        row["search_conclusion_matches_db"] = bool(result.conclusion == db)
        row["search_context_count"] = len(contexts)
        row["search_reference_text"] = [short(item) for item in result.references]
        row["abstract_certificate_present"] = result.abstract_structure is not None
        row["proof_steps"] = [
            {
                "index": index, "rule": getattr(getattr(step, "rule", None), "name", None),
                "conclusion": short(step.conclusion, 2000),
                "inference_rule": short(getattr(getattr(step, "inference_rule", None), "name", None)),
                "premise_count": len(step.premises),
                "source_label": getattr(
                    getattr(getattr(step, "inference_rule", None), "literature_reference", None),
                    "label", None,
                ),
                "source_locator": getattr(
                    getattr(getattr(step, "inference_rule", None), "literature_reference", None),
                    "locator", None,
                ),
            }
            for index, step in enumerate(result.proven_steps)
        ]
        row["trust_verified"] = False
        row["model_root_verified"] = False
        row["model_error"] = None
        row["reference_count"] = 0
        row["references"] = []
        row["markdown"] = None
        try:
            if result.status is ProofSearchStatus.COMPLETE:
                if len(contexts) != 1:
                    raise RuntimeError("completed search lacks exactly one screened context")
                cited_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
                if cited_id is None:
                    verify_proof_tree_for_narrative(
                        result, contexts[0], citing_assertion_id=None,
                        derived_target_without_citing_id=True,
                    )
                else:
                    verify_proof_tree_for_narrative(
                        result, contexts[0], citing_assertion_id=cited_id,
                    )
                row["trust_verified"] = True
                model = build_linked_proof_narrative_model(result, contexts[0])
                row["model_root_verified"] = bool(
                    model.root_index is not None
                    and 0 <= model.root_index < len(model.steps)
                    and model.steps[model.root_index].conclusion == db
                )
            else:
                model = build_proof_narrative_model(result)
                row["model_root_verified"] = model.root_index is None
            row["reference_count"] = len(model.citations)
            row["references"] = [
                {"number": cite.number,
                 "label": cite.reference.label,
                 "locator": cite.reference.locator}
                for cite in model.citations
            ]
            text = render_model_backed_narrative_markdown(result, model)
            row["markdown"] = text
            row["markdown_sha256"] = sha256(text.encode("utf-8")).hexdigest()
        except Exception as exc:
            row["model_error"] = f"{type(exc).__name__}: {exc}"
        row["web_key"] = None
        row["web_partial"] = None
        row["web_error"] = None
        row["web_line_count"] = 0
        row["web_lines"] = []
        try:
            # Do not supply a target override: observe the real Group query route.
            web = build_standard_web_group_proof_view(
                n=n, k=k, max_depth=2, mode="narrative", citation_source="model",
            )
            row["web_key"] = web.key
            row["web_partial"] = web.partial_result
            row["web_line_count"] = len(web.rendered_lines)
            row["web_conclusion_latex"] = web.conclusion_latex
            row["web_abstract_structure_certified"] = web.abstract_structure_certified
            row["web_lines"] = [
                {
                    "kind": line.kind, "indent": line.indent_level,
                    "prefix": line.prefix, "math": line.statement_latex,
                    "suffix": line.suffix,
                }
                for line in web.rendered_lines
            ]
        except Exception as exc:
            row["web_error"] = f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        row["exception"] = f"{type(exc).__name__}: {exc}"
        row["traceback"] = traceback.format_exc()[-4000:]
    row["audit_result"] = classify(row)
    return row


def parse_worker_output(output: str, exit_code: int, n: int, k: int) -> dict[str, object]:
    """Reject missing/duplicated/malformed markers and spoofed group coordinates."""
    markers = [line[len(WORKER_MARKER):] for line in output.splitlines()
               if line.startswith(WORKER_MARKER)]
    if exit_code or len(markers) != 1:
        return {"n": n, "k": k, "audit_result": "WORKER_FAILED",
                "exit_code": exit_code, "marker_count": len(markers)}
    try:
        row = json.loads(markers[0])
    except (json.JSONDecodeError, TypeError):
        return {"n": n, "k": k, "audit_result": "WORKER_JSON_INVALID"}
    if not isinstance(row, dict) or row.get("n") != n or row.get("k") != k:
        return {"n": n, "k": k, "audit_result": "WORKER_GOAL_MISMATCH"}
    row["audit_result"] = classify(row)
    return row


def launch_worker(root: Path, n: int, k: int, seconds: int, output_dir: Path) -> dict[str, object]:
    """Isolate each group so a hang/error does not erase other observations."""
    env = dict(os.environ)
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    log_file = output_dir / f"pi_{n+k}_{n}.log"
    try:
        completed = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker",
             "--n", str(n), "--k", str(k)],
            cwd=root, env=env, capture_output=True,
            text=True, encoding="utf-8", errors="replace", check=False,
            timeout=seconds,
        )
        log_file.write_text(completed.stdout + "\nSTDERR:\n" + completed.stderr,
                            encoding="utf-8")
        return parse_worker_output(completed.stdout, completed.returncode, n, k)
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        log_file.write_bytes(raw if isinstance(raw, bytes) else str(raw).encode("utf-8"))
        return {"n": n, "k": k, "audit_result": "WORKER_TIMEOUT",
                "timeout_seconds": seconds}


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Keep missing/unfinished proofs distinct from operational failures."""
    pairs = [(row["n"], row["k"]) for row in rows]
    if len(pairs) != len(set(pairs)):
        raise ValueError("R1_DUPLICATE_WORKER_RESULT")
    counts: dict[str, int] = {}
    for row in rows:
        label = str(row["audit_result"])
        counts[label] = counts.get(label, 0) + 1
    return {
        "checked": len(rows), "target_count": len(EXPECTED_GROUPS),
        "complete": counts.get("COMPLETE_AND_WEB_VERIFIED", 0),
        "unfinished": counts.get("INCOMPLETE_AND_WEB_CONFIRMED", 0),
        "execution_or_trust_failures": sum(counts.get(label, 0) for label in FAILURE_RESULTS),
        "not_yet_checked": len(EXPECTED_GROUPS) - len(rows),
        "classification_counts": counts,
    }


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Persist every observed group and the exact audit state atomically."""
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    os.replace(temporary, path)


def write_markdown(path: Path, payload: dict[str, object]) -> None:
    """Write Japanese proof-gap summary alongside the full machine-readable data."""
    stats = payload["summary"]
    lines = [
        "# Phase 175 R1 — 4-stem ($k=4$) の登録済み6群の監査", "",
        "Source-first／First Successful Proof Search。これは監査であり新規証明ではない。", "",
        f"- Git HEAD: `{payload['preflight']['head']}`",
        f"- 検査済み: {stats['checked']}/6",
        f"- 完成・Web検証済み: {stats['complete']}",
        f"- 未完成・Web確認済み: {stats['unfinished']}",
        f"- 実行・認証上の問題: {stats['execution_or_trust_failures']}", "",
        "| 対象 | CSV 成分 | Search | Step | Open | Reference | Web | 判定 |",
        "|---|---:|---|---:|---:|---:|---|---|",
    ]
    for row in payload["rows"]:
        n, k = row["n"], row["k"]
        lines.append(
            f"| $\\pi_{{{n+k}}}^{{{n}}}$ | {len(row['registered_summands'])} | "
            f"{row.get('search_status', '—')} | {row.get('search_proven_count', '—')} | "
            f"{row.get('search_open_count', '—')} | {row.get('reference_count', '—')} | "
            f"{row.get('web_key', '—')} | {row['audit_result']} |"
        )
    lines.extend([
        "", "詳細な型付き Goal、ProofStep、引用、Web の各行は report.json と各 worker log に保存。",
        "DB の群構造が登録されていることと、記名生成元の証明完成は区別する。",
        "全体 pytest は Phase 175 終了時にのみ実施する。", "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    """Perform preflight, then optionally run six isolated real proof searches."""
    parent = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    target = parent / "EHPProofTracerAudit" / PACKAGE / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    )
    target.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R1", "mode": "READ_ONLY_AUDIT",
        "dry_run": dry_run, "full_pytest_executed": False,
        "production_changes": [], "new_given": 0, "new_mathematical_rules": 0,
        "rows": [], "result": "NOT_STARTED", "report_folder": str(target),
    }
    return_code = 2
    before: dict[str, object] | None = None
    print("PHASE175_R1_REPORT_DIR=" + str(target), flush=True)
    try:
        before = preflight(root)
        report["preflight"] = before
        registrations = registered_k4_rows(root / "data/sphere.csv")
        report["registered_groups"] = [
            {"n": n, "k": k, "summands": registrations[n, k]}
            for n, k in EXPECTED_GROUPS
        ]
        print("PHASE175_R1_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R1_SOURCE_PINS=" + str(len(SOURCE_BLOBS)), flush=True)
        print("PHASE175_R1_REGISTERED_GROUPS=6", flush=True)
        print("PHASE175_R1_REGISTERED_SUMMAND_ROWS=" +
              str(before["registered_summand_rows"]), flush=True)
        if dry_run:
            report["summary"] = summary([])
            report["result"] = "PASS_R1_READ_ONLY_DRYRUN"
            return_code = 0
        else:
            for n, k in EXPECTED_GROUPS:
                row = launch_worker(root, n, k, timeout_seconds, target)
                row["registered_summands"] = registrations[n, k]
                report["rows"].append(row)
                report["summary"] = summary(report["rows"])
                write_json(target / "report.json", report)
                print(f"PHASE175_R1_GROUP=pi_{n+k}^{n}:{row['audit_result']}", flush=True)
            stats = report["summary"]
            return_code = 2 if stats["execution_or_trust_failures"] else 0
            report["result"] = (
                "AUDIT_REQUIRES_INVESTIGATION" if return_code else
                "PASS_R1_AUDIT_ALL_COMPLETE" if stats["complete"] == 6 else
                "PASS_R1_AUDIT_WITH_PROOF_GAPS"
            )
            write_markdown(target / "report.md", report)
            print("PHASE175_R1_COMPLETE=" + str(stats["complete"]), flush=True)
            print("PHASE175_R1_INCOMPLETE=" + str(stats["unfinished"]), flush=True)
            print("PHASE175_R1_FAILURES=" + str(stats["execution_or_trust_failures"]), flush=True)
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-4000:]
        return_code = 2
        print("PHASE175_R1_REFUSED=" + report["error"], flush=True)
    finally:
        if before is not None:
            try:
                report["tracked_unchanged"] = (before == preflight(root))
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = f"{type(exc).__name__}: {exc}"
            if not report["tracked_unchanged"]:
                report["result"] = "TRACKED_SOURCE_CHANGED"
                return_code = 2
        else:
            report["tracked_unchanged"] = None
        write_json(target / "report.json", report)
        print("PHASE175_R1_REPORT=" + str(target / "report.json"), flush=True)
        print("PHASE175_R1_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE175_R1_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return return_code


def main() -> int:
    """CLI entrypoint for the audit runner and isolated workers."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--n", type=int)
    parser.add_argument("--k", type=int)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    if args.worker:
        if (args.n, args.k) not in EXPECTED_GROUPS:
            parser.error("--worker requires one registered k=4 pair with 2<=n<=7")
        row = inspect_one_group(args.n, args.k)
        print(WORKER_MARKER + json.dumps(row, ensure_ascii=False, sort_keys=True), flush=True)
        return 0
    if args.root is None:
        parser.error("--root is required unless --worker")
    if args.timeout_seconds < 1:
        parser.error("--timeout-seconds must be positive")
    return run(args.root.resolve(), args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
