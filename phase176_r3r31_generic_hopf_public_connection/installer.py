"""Minimal, fail-closed public hookup for the audited R3R30 rule."""
from __future__ import annotations

import ast
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
MARKER = "        options.extend(expand_cited_prop22_right_formula(goal, tuple(available)))"
NEW_LINES = (
    "        # Phase 176 R3R31: general Hopf substitution with two open proof obligations.\n"
    "        from phase176_r3r30_generic_hopf_substitution_isolated.source import (\n"
    "            expand_generic_hopf_substitution,\n"
    "        )\n"
    "        options.extend(expand_generic_hopf_substitution(goal, tuple(available)))\n"
)


def proposed_code(source: str) -> str:
    """Insert one additive provider call, preserving all existing source text."""
    if not isinstance(source, str):
        raise TypeError("source must be str")
    if source.count(MARKER) != 1:
        raise ValueError("EXPECTED_SINGLE_PROP22_PROVIDER_ANCHOR")
    if "options.extend(expand_generic_hopf_substitution(goal, tuple(available)))" in source:
        raise ValueError("R3R31_ALREADY_APPLIED")
    tree = ast.parse(source)
    funcs = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "shared_expansion_provider"
    ]
    if len(funcs) != 1:
        raise ValueError("SHARED_PROVIDER_FUNCTION_NOT_UNIQUE")
    original_lines = source.splitlines(keepends=True)
    position = next(
        i for i, line in enumerate(original_lines)
        if MARKER in line
    )
    if not funcs[0].lineno - 1 <= position < funcs[0].end_lineno:
        raise ValueError("ANCHOR_OUTSIDE_SHARED_PROVIDER")
    eol = "\r\n" if "\r\n" in source else "\n"
    inserted = NEW_LINES.replace("\n", eol)
    original_lines.insert(position + 1, inserted)
    candidate = "".join(original_lines)
    ast.parse(candidate)
    if candidate.count("expand_generic_hopf_substitution(goal, tuple(available))") != 1:
        raise ValueError("NEW_PROVIDER_NOT_UNIQUE")
    return candidate


def git(*args: str) -> str:
    p = subprocess.run(("git", *args), cwd=ROOT, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if p.returncode:
        raise RuntimeError("GIT_COMMAND_FAILED: " + p.stderr.strip())
    return p.stdout.strip()


def verify_checkout() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if not (ROOT / "phase176_r3r30_generic_hopf_substitution_isolated" / "source.py").is_file():
        raise RuntimeError("R3R30_DEPENDENCY_MISSING")
    if not (ROOT / "phase176_r3r28_toda55_quadruple_public" / "tests" / "test_public.py").is_file():
        raise RuntimeError("R3R28_DEPENDENCY_MISSING")
    if git("diff", "--", "phase165_r52_r9_shared_math.py"):
        raise RuntimeError("TARGET_ALREADY_HAS_UNSTAGED_EDITS")
    if git("diff", "--cached", "--", "phase165_r52_r9_shared_math.py"):
        raise RuntimeError("TARGET_ALREADY_HAS_STAGED_EDITS")
    return git("rev-parse", "HEAD")


def changed_function_text(source: str) -> str:
    tree = ast.parse(source)
    node = next(
        item for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == "shared_expansion_provider"
    )
    return "".join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])


def install(dry_run: bool) -> dict:
    head = verify_checkout()
    current = TARGET.read_bytes()
    encoding = "utf-8-sig" if current.startswith(b"\xef\xbb\xbf") else "utf-8"
    original = current.decode(encoding)
    proposed = proposed_code(original)
    report_dir = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                  / "EHPProofTracerAudit" / "phase176_r3r31_generic_hopf_public_connection")
    report_dir.mkdir(parents=True, exist_ok=True)
    # Full function output for direct replacement review.
    if not dry_run:
        artifact = report_dir / "CHANGED_FUNCTION_FULL_JA.md"
        artifact.write_text(
            "# R3R31 変更後の関数全文\n\n対象: `phase165_r52_r9_shared_math.py` "
            "の `shared_expansion_provider()`\n\n```python\n"
            + changed_function_text(proposed) + "\n```\n",
            encoding="utf-8",
        )
        TARGET.write_bytes(proposed.encode(encoding))
    return {"gate": "PASS_R3R31_DRYRUN" if dry_run
            else "PASS_R3R31_PUBLIC_PATCH_INSTALLED_TESTS_PENDING",
            "head": head,
            "production_target": str(TARGET),
            "production_changed": not dry_run,
            "new_given": 0,
            "new_source_statements": 0,
            "new_math_rules": 0,
            "full_pytest": "NOT_RUN"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        report = install(args.dry_run)
    except Exception as err:
        report = {"gate": "FAIL_R3R31", "error": type(err).__name__ + ": " + str(err),
                  "full_pytest": "NOT_RUN"}
    report_dir = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                  / "EHPProofTracerAudit" / "phase176_r3r31_generic_hopf_public_connection")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "report.json"
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    for k, v in report.items():
        print("PHASE176_R3R31_" + k.upper() + "=" + str(v))
    print("PHASE176_R3R31_REPORT=" + str(report_file))
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
