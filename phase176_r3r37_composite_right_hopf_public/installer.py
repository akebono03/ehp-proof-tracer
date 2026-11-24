"""Phase 176 R3R37: fail-closed additive hookup for composite right-Hopf candidates.

No mathematics, citation, or root proof is installed by this script.  It
patches exactly one existing nested provider and preserves prior hooks.
"""
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
PACKAGE = "phase176_r3r37_composite_right_hopf_public"
MARKER = "        options.extend(expand_composite_suspension_equality(goal))"
R3R31_MARKER = "        options.extend(expand_generic_hopf_substitution(goal, tuple(available)))"
PATCH = (
    "        # Phase 176 R3R37: source-screened composite-right Hopf candidates.\n"
    "        from phase176_r3r36_composite_right_hopf_isolated.source import (\n"
    "            expand_cited_composite_right_hopf,\n"
    "        )\n"
    "        options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))\n"
)
PATCH_CALL = "options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))"


def _nested_expand_location(source: str) -> tuple[int, int]:
    """Return one-based line bounds for the exact public nested expand()."""
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
    """Insert exactly once after R3R35 or accept identical prior insertion."""
    if not isinstance(source, str):
        raise TypeError("source must be str")
    lines = source.splitlines(keepends=True)
    marker_indexes = [
        index for index, line in enumerate(lines)
        if line.rstrip("\r\n") == MARKER
    ]
    if len(marker_indexes) != 1:
        raise ValueError("R3R35_ANCHOR_NOT_UNIQUE")
    if sum(line.rstrip("\r\n") == R3R31_MARKER for line in lines) != 1:
        raise ValueError("R3R31_ANCHOR_NOT_UNIQUE")
    start, end = _nested_expand_location(source)
    index = marker_indexes[0]
    if not start <= index + 1 <= end:
        raise ValueError("R3R35_ANCHOR_OUTSIDE_NESTED_EXPAND")
    eol = "\r\n" if "\r\n" in source else "\n"
    patch = PATCH.replace("\n", eol)
    patch_lines = patch.splitlines(keepends=True)
    already = PATCH_CALL in source
    if already:
        if source.count(PATCH_CALL) != 1:
            raise ValueError("DUPLICATE_R3R37_PROVIDER")
        if "".join(lines[index + 1:index + 1 + len(patch_lines)]) != patch:
            raise ValueError("CONFLICTING_R3R37_PATCH")
        return source
    if "expand_cited_composite_right_hopf" in source:
        raise ValueError("PARTIAL_R3R37_PATCH")
    lines.insert(index + 1, patch)
    result = "".join(lines)
    ast.parse(result)
    if result.count(PATCH_CALL) != 1:
        raise ValueError("R3R37_PROVIDER_NOT_UNIQUE")
    return result


def changed_function_text(source: str) -> str:
    """Extract the entire enclosing public function, including nested expand."""
    module = ast.parse(source)
    outer = [
        node for node in module.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(outer) != 1:
        raise ValueError("SHARED_FUNCTION_NOT_UNIQUE")
    node = outer[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def git(*args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True,
    )
    if completed.returncode:
        raise RuntimeError("GIT_FAILED: " + completed.stderr.strip())
    return completed.stdout.strip()


def preflight() -> str:
    """Require develop, current proof-source files, and a matching repository root."""
    checkout = Path(git("rev-parse", "--show-toplevel")).resolve()
    if str(checkout).casefold() != str(ROOT.resolve()).casefold():
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    for relative, signatures in {
        "phase176_r3r36_composite_right_hopf_isolated/source.py": (
            "def expand_cited_composite_right_hopf(",
            "def composite_hopf_substitution_inputs(",
        ),
        "phase176_r3r34_composite_suspension_isolated/source.py": (
            "def expand_composite_suspension_equality(",
        ),
        "phase171_r2h_prop22_cited_hopf/source.py": (
            "class TodaProp22RightFormula:",
        ),
        "phase176_r3r30_generic_hopf_substitution_isolated/source.py": (
            "def expand_generic_hopf_substitution(",
        ),
    }.items():
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError("DEPENDENCY_MISSING: " + relative)
        content = path.read_text(encoding="utf-8-sig")
        if not all(signature in content for signature in signatures):
            raise RuntimeError("DEPENDENCY_SIGNATURE_CHANGED: " + relative)
    if not TARGET.is_file():
        raise RuntimeError("SHARED_PROVIDER_MISSING")
    return git("rev-parse", "HEAD")


def report_folder() -> Path:
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def install(dry_run: bool) -> dict:
    head = preflight()
    original_bytes = TARGET.read_bytes()
    bom = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
    original = original_bytes[len(bom):].decode("utf-8")
    updated = proposed_code(original)
    unchanged = updated == original
    if not unchanged and (
        git("diff", "--", "phase165_r52_r9_shared_math.py")
        or git("diff", "--cached", "--", "phase165_r52_r9_shared_math.py")
    ):
        raise RuntimeError("EXISTING_SHARED_SOURCE_EDITS_REFUSED")
    output = report_folder()
    full = changed_function_text(updated)
    artifact = output / "CHANGED_FUNCTION_FULL_JA.md"
    artifact.write_text(
        "# Phase 176 R3R37 — 変更後の関数全文\n\n"
        "対象：`phase165_r52_r9_shared_math.py` の "
        "`shared_expansion_provider()`（内部の `expand()` を含む全文）。\n\n"
        "```python\n" + full + ("" if full.endswith("\n") else "\n") + "```\n",
        encoding="utf-8",
    )
    if not dry_run and not unchanged:
        (output / "phase165_r52_r9_shared_math.py.before_R3R37").write_bytes(original_bytes)
        TARGET.write_bytes(bom + updated.encode("utf-8"))
    return {
        "gate": "PASS_R3R37_DRYRUN" if dry_run else "PASS_R3R37_PATCH_INSTALLED_TESTS_PENDING",
        "head": head,
        "changed_on_this_run": not dry_run and not unchanged,
        "already_connected": unchanged,
        "target": str(TARGET),
        "full_function": str(artifact),
        "new_given": 0,
        "new_source_assertions": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    try:
        result = install(arguments.dry_run)
    except Exception as error:
        result = {
            "gate": "FAIL_R3R37_INSTALL",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    destination = report_folder() / "install_report.json"
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for key, value in result.items():
        print("PHASE176_R3R37_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
