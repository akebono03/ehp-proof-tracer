"""Phase 175 R3R9: guarded direct Lemma 5.7 citation and public proof audit."""
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

from phase175_r3r9_lemma57_explicit_public import install, source

PACKAGE = "phase175_r3r9_lemma57_explicit_public"
MARKER = "__PHASE175_R3R9_WORKER__="
FOCUSED_TESTS = (
    PACKAGE + "/tests",
    "phase175_r3r8r1_verified_prior_public/tests/test_verified_prior.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_public_search.py",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py",
    "phase175_r3_pi73_hopf_lift/tests/test_rule.py",
    "phase173_r4_r1_public_connection/tests",
)
GATE = "PASS_R3R9_DIRECT_LEMMA57_PI73_PUBLIC_COMPLETE"


def git(root: Path, *args: str) -> str:
    """Run approved read-only Git queries; no mutating subcommands."""
    if not args or args[0] not in {"rev-parse", "branch", "merge-base"}:
        raise ValueError("R3R9_GIT_READ_ONLY_REQUIRED")
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if proc.returncode:
        raise RuntimeError("R3R9_GIT_QUERY_FAILED: " + " ".join(args))
    return proc.stdout.strip()


def source_guard(root: Path) -> dict[str, object]:
    """Pin all earlier reviewed sources, updating only the former public-route pin.

    The original Phase 175 R1 guard required the pre-R3R8 production blob.
    That blob is intentionally superseded by the successful R3R8R1R2 commit;
    all other R1/R2/R3 anchors retain their original expected SHAs.
    """
    from phase175_r1_k4_audit import audit as r1
    from phase175_r2_k4_frontier_audit import audit as r2
    from phase175_r3_pi73_hopf_lift import audit as r3

    if (
        git(root, "branch", "--show-current") != "develop"
        or Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root
    ):
        raise RuntimeError("R3R9_NOT_REVIEWED_DEVELOP_ROOT")
    head = git(root, "rev-parse", "HEAD")
    git(root, "merge-base", "--is-ancestor", install.PINNED_HEAD_ANCESTOR, head)
    checked = {}
    for relative, expected in (
        dict(r1.SOURCE_BLOBS)
        | r2.EXTRA_PINS
        | r3.EXTRA_PINS
    ).items():
        if relative == install.TARGET.as_posix():
            expected = install.PINNED_GIT_BLOB
        if not (root / relative).is_file():
            raise RuntimeError("R3R9_REQUIRED_SOURCE_MISSING: " + relative)
        observed = git(root, "rev-parse", "HEAD:" + relative)
        if observed != expected:
            raise RuntimeError("R3R9_PINNED_SOURCE_BLOB_CHANGED: " + relative)
        checked[relative] = expected
    if len(r1.registered_k4_rows(root / "data/sphere.csv")) != 6:
        raise RuntimeError("R3R9_REGISTERED_K4_TARGETS_CHANGED")
    citation = source.verify_explicit_lemma57_source(root)
    patch = install.preflight(root)
    return {
        "head": head, "pinned_blobs": checked,
        "explicit_source": citation,
        "patch": patch,
    }


def latest_successful_r3r8r1() -> Path:
    """Require the actual earlier user-run public PASS, not a claimed success."""
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / "phase175_r3r8r1_verified_prior_public"
    for file in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            row = json.loads(file.read_text(encoding="utf-8"))
            worker = row.get("worker")
            data = worker.get("data") if isinstance(worker, dict) else None
            if (
                row.get("phase") == "175-R3R8R1"
                and row.get("dry_run") is False
                and row.get("result") == "PASS_R3R8R1_PUBLIC_PI73_COMPLETE_AND_WEB_VERIFIED"
                and isinstance(data, dict)
                and data.get("audit_result") == "COMPLETE_AND_WEB_VERIFIED"
                and data.get("search_status") == "complete"
                and data.get("trust_verified") is True
                and data.get("web_key") == "generic-complete-proof"
            ):
                return file
        except (OSError, UnicodeError, TypeError, ValueError, KeyError):
            continue
    raise RuntimeError("R3R9_PRIOR_R3R8R1_PUBLIC_PASS_NOT_FOUND")


def worker() -> int:
    """Observe real registered backward search, trust boundary and Web view."""
    try:
        from phase175_r1_k4_audit.audit import inspect_one_group
        report = {"status": "INSPECTED", "data": inspect_one_group(3, 4)}
    except Exception as exc:
        report = {
            "status": "ERROR", "error": type(exc).__name__ + ": " + str(exc),
            "traceback": traceback.format_exc()[-6000:],
        }
    print(MARKER + json.dumps(report, ensure_ascii=False), flush=True)
    return 0


def run_worker(root: Path, folder: Path, seconds: int) -> dict:
    """Run public audit in an isolated subprocess with a bounded timeout."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        done = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"],
            cwd=root, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "seconds": seconds}
    (folder / "worker.log").write_text(
        done.stdout + "\nSTDERR:\n" + done.stderr, encoding="utf-8",
    )
    candidates = [line[len(MARKER):] for line in done.stdout.splitlines()
                  if line.startswith(MARKER)]
    if done.returncode or len(candidates) != 1:
        return {"status": "INVALID_WORKER", "exit_code": done.returncode,
                "marker_count": len(candidates)}
    try:
        decoded = json.loads(candidates[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_JSON"}
    return decoded if isinstance(decoded, dict) else {"status": "INVALID_PAYLOAD"}


def focused_pytest(root: Path, folder: Path, seconds: int) -> None:
    """Run only this Phase's relevant tests; full pytest is deferred."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        done = subprocess.run(
            [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
             *FOCUSED_TESTS],
            cwd=root, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=seconds, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("R3R9_FOCUSED_PYTEST_TIMEOUT") from exc
    output = done.stdout + "\nSTDERR:\n" + done.stderr
    (folder / "focused_pytest.log").write_text(output, encoding="utf-8")
    for line in done.stdout.strip().splitlines()[-3:]:
        print("PHASE175_R3R9_PYTEST_OUTPUT=" + line[:500], flush=True)
    if done.returncode:
        raise RuntimeError("R3R9_FOCUSED_PYTEST_FAILED: " + output[-2000:])
    print("PHASE175_R3R9_FOCUSED_PYTEST=PASS", flush=True)


def verify_public_result(data: dict[str, object]) -> dict[str, object]:
    """Trust completed tree and explicitly exclude the former Lemma 5.4 route."""
    if not isinstance(data, dict):
        raise RuntimeError("R3R9_PUBLIC_RESULT_NOT_TYPED_DATA")
    steps = data.get("proof_steps")
    refs = data.get("references")
    if not isinstance(steps, list) or not isinstance(refs, list):
        raise RuntimeError("R3R9_PROOF_ANCESTRY_NOT_PRESENT")
    from phase175_r3r9_lemma57_explicit_public.rule import RULE_NAME

    extracted = [step for step in steps if step.get("inference_rule") == RULE_NAME]
    rejected_names = (
        "Toda Lemma 5.4 verified double-suspension clause extraction",
        "even double-suspension factor implies Lemma 5.7 membership",
        "Toda Lemma 5.7 general double-suspension criterion",
    )
    old = [step for step in steps if step.get("inference_rule") in rejected_names]
    cited_54 = [ref for ref in refs if ref.get("locator") == "Lemma 5.4"]
    if not (
        data.get("audit_result") == "COMPLETE_AND_WEB_VERIFIED"
        and data.get("search_status") == "complete"
        and data.get("search_open_count") == 0
        and data.get("search_conclusion_matches_db") is True
        and data.get("trust_verified") is True
        and data.get("model_root_verified") is True
        and data.get("web_key") == "generic-complete-proof"
        and data.get("web_partial") is False
        and len(extracted) == 1
        and extracted[0].get("rule") == "INFERENCE"
        and extracted[0].get("premise_count") == 1
        and not old
        and not cited_54
        and any(ref.get("locator") == "Lemma 5.7" for ref in refs)
        and all(not (step.get("rule") == "GIVEN"
                     and "GeneratorImage(" in str(step.get("conclusion")))
                for step in steps)
    ):
        raise RuntimeError("R3R9_PUBLIC_DIRECT_LEMMA57_NOT_VERIFIED: " + str({
            key: data.get(key) for key in (
                "audit_result", "search_status", "search_open_count",
                "search_proven_count", "trust_verified", "model_error",
                "web_key", "web_error", "exception",
            )
        }) + f"; extract={len(extracted)}, old={len(old)}, lemma54_refs={len(cited_54)}")
    return {
        "search_status": "complete", "web": "generic-complete-proof",
        "source": "Lemma 5.7 explicit special clause", "lemma54_used": False,
        "reference_count": data.get("reference_count"),
        "proof_steps": len(steps),
    }


def write_report(folder: Path, report: dict[str, object]) -> None:
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 175 R3R9 — Lemma 5.7 特別結論の直接引用", "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- 対象: $\\pi_7^3=\\mathbb{Z}/2\\{\\nu'\\eta_6\\}$",
        "- Lemma 5.7 の明記された特別結論を出典付きで利用",
        "- Lemma 5.4 の依存を公開証明木に含めない",
        "- 最終群構造の直接 GIVEN: なし",
        "- 全体 pytest: 未実施", "",
        "## 実測", "",
    ]
    checked = report.get("public_evidence")
    if isinstance(checked, dict):
        for key, value in checked.items():
            lines.append("- " + key + ": `" + str(value) + "`")
    if report.get("error"):
        lines += ["", "## 失敗", "", "`" + str(report["error"]) + "`"]
    (folder / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, seconds: int) -> int:
    root = Path(root).resolve()
    local = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = local / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S_%fZ"
    )
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3R9", "dry_run": dry_run, "result": "NOT_STARTED",
        "new_group_given": 0, "new_specific_cited_clause": 1,
        "new_mathematical_inference_theorems": 0, "full_pytest": False,
        "modified_file": str(install.TARGET),
    }
    installed = False
    exit_code = 2
    print("PHASE175_R3R9_OUTPUT=" + str(folder), flush=True)
    try:
        report["source_guard"] = source_guard(root)
        report["previous_success"] = str(latest_successful_r3r8r1())
        print("PHASE175_R3R9_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R9_PRIOR_PUBLIC_PASS=PASS", flush=True)
        if dry_run:
            report["result"] = "PASS_R3R9_READ_ONLY_DRYRUN"
            exit_code = 0
        else:
            report["installation"] = install.apply(root, folder)
            installed = True
            print("PHASE175_R3R9_PUBLIC_ROUTE_PATCH=ONE_FUNCTION", flush=True)
            focused_pytest(root, folder, seconds)
            tested = run_worker(root, folder, seconds)
            report["worker"] = tested
            if tested.get("status") != "INSPECTED":
                raise RuntimeError("R3R9_PUBLIC_WORKER_FAILED: " + str(tested))
            observed = tested.get("data", {})
            print("PHASE175_R3R9_SEARCH=" + str(observed.get("search_status")), flush=True)
            print("PHASE175_R3R9_TRUST=" + str(observed.get("trust_verified")), flush=True)
            print("PHASE175_R3R9_WEB=" + str(observed.get("web_key")), flush=True)
            report["public_evidence"] = verify_public_result(observed)
            install.verify_postflight(root, report["installation"])
            report["result"] = GATE
            exit_code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
        report["result"] = "R3R9_REFUSED_OR_PUBLIC_VERIFICATION_FAILED"
        print("PHASE175_R3R9_ERROR=" + report["error"], flush=True)
    finally:
        if installed and exit_code != 0:
            try:
                install.rollback(root, folder)
                report["rolled_back"] = True
                print("PHASE175_R3R9_ROLLBACK=PASS", flush=True)
            except Exception as exc:
                report["rolled_back"] = False
                report["rollback_error"] = str(exc)
                report["result"] = "R3R9_ROLLBACK_FAILED"
        write_report(folder, report)
        print("PHASE175_R3R9_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R9_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=install.ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("timeout-seconds must be positive")
    if args.worker:
        return worker()
    return run(args.root, args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
