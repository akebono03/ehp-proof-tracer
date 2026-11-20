"""R3R28R1: replace only the failed citation-context test function."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "phase176_r3r28_toda55_quadruple_public" / "tests" / "test_public.py"
BASE = Path(__file__).resolve().parent
EXPECTED_OLD = (BASE / "OLD_FUNCTION.txt").read_text(encoding="utf-8")
REPLACEMENT = (BASE / "NEW_FUNCTION.txt").read_text(encoding="utf-8")


def git(*args: str) -> str:
    result = subprocess.run(("git", *args), cwd=ROOT, text=True,
                            encoding="utf-8", errors="replace", capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("GIT_FAILED: " + result.stderr.strip())
    return result.stdout.strip()


def check_checkout() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    if not TARGET.is_file():
        raise RuntimeError("TARGET_TEST_NOT_FOUND")
    return git("rev-parse", "HEAD")


def function_body(source: str, name: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError("TEST_FUNCTION_MISSING_OR_DUPLICATED")
    node = matches[0]
    return "".join(lines[node.lineno - 1:node.end_lineno])


def proposed(source: str) -> str:
    name = "test_shared_provider_proposes_and_proves_nu5_quadruple"
    current = function_body(source, name)
    if current.rstrip("\n") == REPLACEMENT.rstrip("\n"):
        return source
    if current.rstrip("\n") != EXPECTED_OLD.rstrip("\n"):
        raise RuntimeError("TEST_BASELINE_CHANGED")
    result = source.replace(current, REPLACEMENT, 1)
    ast.parse(result)
    if function_body(result, name).rstrip("\n") != REPLACEMENT.rstrip("\n"):
        raise RuntimeError("FUNCTION_REPLACEMENT_FAILED")
    return result


def execute(dry_run: bool) -> int:
    row = {"phase": "176_R3R28R1", "gate": "FAIL_R3R28R1",
           "full_pytest": "NOT_RUN", "production_changes": 0,
           "new_given": 0, "new_mathematical_rules": 0}
    try:
        row["head"] = check_checkout()
        raw = TARGET.read_bytes()
        newline = "\r\n" if b"\r\n" in raw else "\n"
        original = raw.decode("utf-8-sig").replace("\r\n", "\n")
        replacement = proposed(original)
        row["changed"] = replacement != original
        if not dry_run and replacement != original:
            TARGET.write_bytes(replacement.replace("\n", newline).encode("utf-8"))
        row["gate"] = "PASS_R3R28R1_DRYRUN" if dry_run else "PASS_R3R28R1_TEST_FIXED_PENDING_PYTEST"
    except Exception as exc:
        row["error"] = type(exc).__name__ + ": " + str(exc)
    path = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / "phase176_r3r28r1_uncited_root_test_fix"
    path.mkdir(parents=True, exist_ok=True)
    report = path / "report.json"
    report.write_text(json.dumps(row, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for key in ("gate", "head", "changed", "production_changes"):
        if key in row:
            print("PHASE176_R3R28R1_" + key.upper() + "=" + str(row[key]))
    if "error" in row:
        print("PHASE176_R3R28R1_ERROR=" + row["error"])
    print("PHASE176_R3R28R1_REPORT=" + str(report))
    print("PHASE176_R3R28R1_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if row["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())
