"""Fail-closed public registration of the independently tested R3R34 bridge."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
PACKAGE = "phase176_r3r35_composite_suspension_public"
MARKER = "        options.extend(expand_generic_hopf_substitution(goal, tuple(available)))"
PATCH = (
    "        # Phase 176 R3R35: composite suspension equality; image stays an open goal.\n"
    "        from phase176_r3r34_composite_suspension_isolated.source import (\n"
    "            expand_composite_suspension_equality,\n"
    "        )\n"
    "        options.extend(expand_composite_suspension_equality(goal))\n"
)


def _shared_expand_location(source: str) -> tuple[int, int]:
    """Find the exact nested public provider; reject ambiguous refactors."""
    module = ast.parse(source)
    outer = [
        node for node in module.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(outer) != 1:
        raise ValueError("EXPECTED_ONE_SHARED_EXPANSION_PROVIDER")
    nested = [
        node for node in ast.walk(outer[0])
        if isinstance(node, ast.FunctionDef) and node.name == "expand"
    ]
    if len(nested) != 1:
        raise ValueError("EXPECTED_ONE_NESTED_EXPAND")
    return nested[0].lineno, nested[0].end_lineno


def proposed_code(source: str) -> str:
    """Insert one hook, or accept an exact prior installation unchanged."""
    if not isinstance(source, str):
        raise TypeError("source must be str")
    lines = source.splitlines(keepends=True)
    anchors = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == MARKER]
    if len(anchors) != 1:
        raise ValueError("EXPECTED_ONE_R3R31_ANCHOR")
    low, high = _shared_expand_location(source)
    index = anchors[0]
    if not low <= index + 1 <= high:
        raise ValueError("R3R31_ANCHOR_OUTSIDE_NESTED_EXPAND")
    eol = "\r\n" if "\r\n" in source else "\n"
    patch = PATCH.replace("\n", eol)
    if "expand_composite_suspension_equality(goal)" in source:
        if source.count(patch) != 1 or index + 1 >= len(lines):
            raise ValueError("CONFLICTING_R3R35_PATCH")
        if "".join(lines[index + 1:index + 1 + len(PATCH.splitlines())]) != patch:
            raise ValueError("R3R35_PATCH_AT_UNEXPECTED_POSITION")
        return source
    lines.insert(index + 1, patch)
    candidate = "".join(lines)
    ast.parse(candidate)
    if candidate.count("options.extend(expand_composite_suspension_equality(goal))") != 1:
        raise ValueError("NEW_R3R35_PROVIDER_NOT_UNIQUE")
    return candidate


def changed_function_text(source: str) -> str:
    """Return the ENTIRE changed enclosing function for review."""
    module = ast.parse(source)
    nodes = [
        item for item in module.body
        if isinstance(item, ast.FunctionDef)
        and item.name == "shared_expansion_provider"
    ]
    if len(nodes) != 1:
        raise ValueError("SHARED_FUNCTION_MISSING")
    node = nodes[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def git(*args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=ROOT, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + result.stderr.strip())
    return result.stdout.strip()


def preflight() -> str:
    """Guard the target source and the required isolated rule."""
    actual = Path(git("rev-parse", "--show-toplevel")).resolve()
    if str(actual).casefold() != str(ROOT.resolve()).casefold():
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    for path in (
        "phase176_r3r34_composite_suspension_isolated/source.py",
        "phase176_r3r30_generic_hopf_substitution_isolated/source.py",
        "phase171_r2h_prop22_cited_hopf/source.py",
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError("MISSING_DEPENDENCY: " + path)
    if not TARGET.is_file():
        raise RuntimeError("SHARED_PROVIDER_MISSING")
    return git("rev-parse", "HEAD")


def install(dry_run: bool) -> dict:
    head = preflight()
    original_bytes = TARGET.read_bytes()
    bom = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
    original = original_bytes[len(bom):].decode("utf-8")
    revised = proposed_code(original)
    unchanged = revised == original
    if not unchanged and (
        git("diff", "--", TARGET.name)
        or git("diff", "--cached", "--", TARGET.name)
    ):
        raise RuntimeError("UNCOMMITTED_TARGET_EDITS_REFUSED")
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE)
    folder.mkdir(parents=True, exist_ok=True)
    full = changed_function_text(revised)
    (folder / "CHANGED_FUNCTION_FULL_JA.md").write_text(
        "# R3R35 変更後の関数全文\n\n"
        "対象: `phase165_r52_r9_shared_math.py` の "
        "`shared_expansion_provider()`（全文）。\n\n```python\n"
        + full + ("" if full.endswith("\n") else "\n") + "```\n",
        encoding="utf-8",
    )
    if not dry_run and not unchanged:
        backup = folder / "phase165_r52_r9_shared_math.py.before_R3R35"
        backup.write_bytes(original_bytes)
        TARGET.write_bytes(bom + revised.encode("utf-8"))
    return {
        "gate": ("PASS_R3R35_DRYRUN" if dry_run
                 else "PASS_R3R35_PATCH_INSTALLED_TESTS_PENDING"),
        "head": head,
        "changed_on_this_run": not dry_run and not unchanged,
        "already_connected": unchanged,
        "target": str(TARGET),
        "full_function": str(folder / "CHANGED_FUNCTION_FULL_JA.md"),
        "new_given": 0,
        "new_source_assertions": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        report = install(args.dry_run)
    except Exception as error:
        report = {
            "gate": "FAIL_R3R35_INSTALL",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE)
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / "install_report.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for key, value in report.items():
        print("PHASE176_R3R35_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    return 0 if report["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
