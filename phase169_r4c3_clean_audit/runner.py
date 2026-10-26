"""Repeat the proved R4C audit while preserving tracked report files exactly.

No application source changes. Generated reports are retained under this new
package's (normally untracked) output directory. Any other tracked status
change is reported as an error instead of being silently ignored.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
SOURCE_OUTPUT = ROOT / "phase169_r4c_pi64_suspension_iso" / "output"
REPORT_NAMES = ("audit.md", "audit.json")


def tracked_status(root: Path = ROOT) -> bytes:
    """Snapshot the exact porcelain bytes, including previously dirty paths."""
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-uno"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return result.stdout


def snapshot_files(paths: tuple[Path, ...]) -> dict[Path, bytes | None]:
    """Preserve the exact pre-audit contents (also supports absent files)."""
    return {path: path.read_bytes() if path.is_file() else None for path in paths}


def restore_files(snapshot: dict[Path, bytes | None]) -> None:
    """Undo only audit report writes, without using git checkout or reset."""
    for path, original in snapshot.items():
        if original is None:
            if path.exists():
                if not path.is_file():
                    raise RuntimeError("audit report path was replaced with a nonfile: " + str(path))
                path.unlink()
            continue
        if not path.is_file():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(original)
        elif path.read_bytes() != original:
            path.write_bytes(original)


def validated_report(report_path: Path) -> dict:
    """Fail closed unless the completed root and cited isomorphism are present."""
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise RuntimeError("R4C result must be a JSON object")
    expected_sources = {
        "TodaProp44UniversalStatement": True,
        "TodaProp42GeneralExactnessStatement": True,
        "Toda51BelowDiagonalZeroStatement": True,
    }
    if not (
        report.get("iso_derived") is True
        and report.get("pi6_4_status") == "complete"
        and report.get("pi6_4_open_goals") == []
        and isinstance(report.get("pi6_4_steps"), int)
        and report["pi6_4_steps"] > 0
        and report.get("cited_source_ancestors") == expected_sources
        and report.get("toda45_stable_range_relaxed") is False
    ):
        raise RuntimeError("R4C verified completed proof criteria were not satisfied")
    return report


def execute(args: list[str], env: dict[str, str]) -> None:
    subprocess.run(args, cwd=ROOT, check=True, env=env)


def main() -> None:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTEST_ADDOPTS"] = "-p no:cacheprovider"
    report_paths = tuple(SOURCE_OUTPUT / name for name in REPORT_NAMES)
    before = tracked_status()
    snapshots = snapshot_files(report_paths)
    failure: BaseException | None = None
    report: dict | None = None
    try:
        execute([sys.executable, "-m", "phase169_r4c3_clean_audit.verify"], env)
        tests = [
            "phase169_r4c3_clean_audit/tests/test_r4c3_guard.py",
            "phase169_r4c2_committed_audit/tests/test_r4c2_verifier.py",
            "phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py",
            "phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py",
            "phase169_r3o_toda45_composite_transport/tests/test_r3o_toda45_composite_transport.py",
        ]
        for test in tests:
            if not (ROOT / test).is_file():
                raise FileNotFoundError("required focused pytest missing: " + test)
        execute([sys.executable, "-m", "pytest", "-q", *tests], env)
        execute([sys.executable, "-m", "phase169_r4c_pi64_suspension_iso.audit"], env)
        report = validated_report(SOURCE_OUTPUT / "audit.json")
        output = PACKAGE / "output"
        output.mkdir(exist_ok=True)
        for name in REPORT_NAMES:
            source = SOURCE_OUTPUT / name
            if not source.is_file():
                raise FileNotFoundError("R4C report was not created: " + str(source))
            shutil.copyfile(source, output / name)
        execute([sys.executable, "-m", "phase169_r4c3_clean_audit.verify"], env)
    except BaseException as exc:
        failure = exc
    finally:
        try:
            restore_files(snapshots)
        except BaseException as exc:
            print("R4C3_REPORT_RESTORE_FAILED=" + str(exc), file=sys.stderr)
            if failure is None:
                failure = exc
        try:
            after = tracked_status()
            if after != before:
                print("R4C3_TRACKED_STATUS_BEFORE=" + repr(before.decode("utf-8", "replace")), file=sys.stderr)
                print("R4C3_TRACKED_STATUS_AFTER=" + repr(after.decode("utf-8", "replace")), file=sys.stderr)
                print("R4C3_TRACKED_CHANGE_DETAILS:", file=sys.stderr)
                subprocess.run(["git", "diff", "--name-status"], cwd=ROOT, check=False)
                if failure is None:
                    failure = RuntimeError("tracked Git status changed outside restored audit reports")
        except BaseException as exc:
            if failure is None:
                failure = exc
    if failure is not None:
        raise failure
    if report is None:
        raise RuntimeError("missing successfully validated report")
    print("R4C3_TRACKED_STATUS_UNCHANGED=True")
    print("R4C3_ORIGINAL_AUDIT_REPORTS_RESTORED=True")
    print("R4C3_E_ISOMORPHISM_PROVED=True")
    print("R4C3_PI64_STATUS=" + report["pi6_4_status"])
    print("R4C3_PI64_STEPS=" + str(report["pi6_4_steps"]))
    print("R4C3_PI64_OPEN_GOALS=" + str(len(report["pi6_4_open_goals"])))
    print("R4C3_PRODUCTION_MODIFIED=False")
    print("R4C3_FULL_PYTEST_RUN=False")
    print("R4C3_REPORT=" + str(PACKAGE / "output" / "audit.md"))
    print("R4C3_JSON=" + str(PACKAGE / "output" / "audit.json"))


if __name__ == "__main__":
    main()
