"""Guarded R1R1 replacement of one brittle Phase 169 assertion.

The only target edit is a complete test function. No production mathematical
files are modified. Existing working-tree bytes are preserved on failures.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = Path("phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py")
REVIEWED_BLOB = "b2b21c4fa35181fc0df45c3ef5af8433e147f891"
REVIEWED_HEAD = "e814ec939652807d464fd76051d34a9da40328f8"
REVIEWED = HERE / "reviewed_test.py"
OLD = "    assert len(model.steps) == 28\n"
NEW = (
    "    assert model.steps is proof.proven_steps\n"
    "    assert model.root_index is not None\n"
    "    assert model.steps[model.root_index].rule is ProofRule.INFERENCE\n"
    "    assert model.steps[model.root_index].conclusion == proof.conclusion\n"
    "    assert model.status is ProofSearchStatus.COMPLETE\n"
    "    assert model.open_goals == proof.open_goals == ()\n"
)
FOCUSED_TESTS = (
    "tests/test_phase167_r2_shared_reference.py",
    "tests/test_phase167_r2_unified_reference.py",
    "tests/test_phase167_r3_generic_resolver.py",
    "tests/test_phase168_r3_4_link_bridge.py",
    "phase169_r10a2_unified_one_stem/tests/test_r10a2_one_stem_projection.py",
    "phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py",
    "phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py",
    "phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py",
    "phase170_r3_r7_toda52_ordered_db_transport/tests/test_ordered_db_toda52.py",
    "phase171_r20r2_first_successful_search/tests/test_first_successful_search.py",
    "phase171_r20r11_verified_prior_hopf_surjectivity/tests/test_r20r11_verified_prior.py",
    "phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py",
    "phase171_r20r12r2_unindexed_nu_projection_fix/tests/test_correction.py",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py",
    "phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py",
    "phase171_r20r13r3_content_guard_fix/tests/test_head_content_guard.py",
    "phase171_r20r13r4_test_count_fix/tests/test_install.py",
)


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True, check=True,
    )
    return completed.stdout.rstrip("\r\n")


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def normalized(data: bytes) -> bytes:
    text = data.decode("utf-8-sig")
    text = text.replace("\r\n", "\n")
    if "\r" in text:
        raise ValueError("unrecognized line ending")
    return text.encode("utf-8")


def transform(source: bytes) -> bytes:
    """Replace one assertion in the one reviewed function, with all others intact."""
    reviewed = REVIEWED.read_bytes()
    if git_blob(reviewed) != REVIEWED_BLOB:
        raise RuntimeError("bundled reviewed baseline does not match GitHub blob")
    original = normalized(source)
    if original != reviewed:
        raise RuntimeError("test content differs from reviewed baseline")
    body = reviewed.decode("utf-8")
    function_head = "def test_r3z_general_higher_eta_is_reference_only(rendered_pi53):\n"
    if body.count(function_head) != 1 or body.count(OLD) != 1:
        raise RuntimeError("test function or assertion anchor is not unique")
    patched = body.replace(OLD, NEW, 1)
    ast.parse(patched)
    return patched.encode("utf-8")


def preserve_format(original: bytes, replacement: bytes) -> bytes:
    """Keep the original CRLF/LF and BOM form when replacing whole test module."""
    if b"\r\n" in original:
        replacement = replacement.replace(b"\n", b"\r\n")
    if original.startswith(b"\xef\xbb\xbf"):
        replacement = b"\xef\xbb\xbf" + replacement
    return replacement


def atomic_write(destination: Path, data: bytes) -> None:
    handle, name = tempfile.mkstemp(prefix=".phase171_r1r1_", dir=destination.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
        os.replace(name, destination)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def report_dir() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home())))
    name = "phase171_closeout_r1r1_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    result = base / "EHPProofTracerRecovery" / name
    result.mkdir(parents=True, exist_ok=False)
    return result


def preflight() -> tuple[bytes, bytes, bool, dict[str, object]]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch is required")
    head = git("rev-parse", "HEAD")
    git_head_blob = git("rev-parse", f"HEAD:{TARGET.as_posix()}")
    if git_head_blob != REVIEWED_BLOB:
        raise RuntimeError("tracked baseline changed since reviewed GitHub commit")
    target = ROOT / TARGET
    if not target.is_file():
        raise RuntimeError("test target is absent")
    before = target.read_bytes()
    reviewed = REVIEWED.read_bytes()
    if git_blob(reviewed) != REVIEWED_BLOB:
        raise RuntimeError("reviewed source export has changed")
    expected = preserve_format(before, transform(reviewed))
    if normalized(before) == normalized(expected):
        already = True
        after = before
    else:
        after = transform(before)
        after = preserve_format(before, after)
        already = False
    tracked = git("status", "--porcelain=v1", "--untracked-files=no")
    entries = [line[3:] for line in tracked.splitlines()]
    if any(path != TARGET.as_posix() for path in entries):
        raise RuntimeError("unrelated tracked changes present; refusing to patch")
    if entries and not already:
        raise RuntimeError("target has unreviewed tracked edits")
    missing = [path for path in FOCUSED_TESTS if not (ROOT / path).is_file()]
    if missing:
        raise RuntimeError("missing focused tests: " + ", ".join(missing))
    status = {
        "head": head,
        "reviewed_head": REVIEWED_HEAD,
        "branch": "develop",
        "target": TARGET.as_posix(),
        "reviewed_blob": REVIEWED_BLOB,
        "baseline_step_count": "not assumed",
        "already_installed": already,
        "tracked_before": tracked,
        "tests": list(FOCUSED_TESTS),
        "full_pytest_executed": False,
    }
    return before, after, already, status


def run_tests() -> list[dict[str, object]]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONUTF8"] = "1"
    suites = (
        ("installer", ("phase171_closeout_r1r1_r3z_semantic_guard/tests/test_install.py",)),
        ("focused", FOCUSED_TESTS),
    )
    reports: list[dict[str, object]] = []
    for name, files in suites:
        cmd = [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
               "--disable-warnings", "-p", "no:cacheprovider", *files]
        completed = subprocess.run(cmd, cwd=ROOT, env=env,
                                   text=True, encoding="utf-8", errors="replace",
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   check=False)
        print(completed.stdout, flush=True)
        reports.append({"name": name, "command": cmd,
                        "exit_code": completed.returncode,
                        "output": completed.stdout})
        if completed.returncode != 0:
            raise TestFailure(reports)
    return reports


class TestFailure(RuntimeError):
    def __init__(self, reports: list[dict[str, object]]) -> None:
        super().__init__("focused test failed")
        self.reports = reports


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    before, after, already, report = preflight()
    print("PHASE171_CLOSEOUT_R1R1_HEAD=" + str(report["head"]), flush=True)
    print("PHASE171_CLOSEOUT_R1R1_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_CLOSEOUT_R1R1_ALREADY_INSTALLED=" + str(already), flush=True)
    print("PHASE171_CLOSEOUT_R1R1_FOCUSED_MANIFEST=" + str(len(FOCUSED_TESTS)), flush=True)
    if options.dry_run:
        print("PHASE171_CLOSEOUT_R1R1_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    destination = report_dir()
    (destination / "test_before.py").write_bytes(before)
    target = ROOT / TARGET
    applied = False
    try:
        if not already:
            atomic_write(target, after)
            applied = True
        report["focused_results"] = run_tests()
        report["test_modified"] = applied
        report["production_code_modified"] = False
        report["proof_tree_modified"] = False
        report["reference_modified"] = False
        report["test_after_matches_expected"] = target.read_bytes() == after
        if not report["test_after_matches_expected"]:
            raise RuntimeError("target changed unexpectedly during verification")
        report["result"] = "PASS_TEST_ONLY_SEMANTIC_GUARD"
        print("PHASE171_CLOSEOUT_R1R1_RESULT=PASS_TEST_ONLY_SEMANTIC_GUARD", flush=True)
        return 0
    except Exception as exc:
        if isinstance(exc, TestFailure):
            report["focused_results"] = exc.reports
        if applied:
            atomic_write(target, before)
        report["restored_on_failure"] = applied
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["result"] = "FAILED_RESTORED" if applied else "FAILED_UNCHANGED"
        print("PHASE171_CLOSEOUT_R1R1_RESULT=" + str(report["result"]), flush=True)
        return 1
    finally:
        report["tracked_after"] = git("status", "--porcelain=v1", "--untracked-files=no")
        (destination / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("PHASE171_CLOSEOUT_R1R1_REPORT=" + str(destination / "audit.json"), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
