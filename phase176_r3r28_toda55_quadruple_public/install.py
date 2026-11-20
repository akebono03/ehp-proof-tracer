"""Install only the Phase 176 R3R28 shared Toda (5.5) connection.

The source of the two existing functions is preserved byte for byte except
for two bounded insertions.  Dry-run makes no repository code modifications.
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

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r28_toda55_quadruple_public"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
SOURCE = ROOT / "phase176_r3r27r1_toda55_quadruple_isolated" / "source.py"
SOURCE_ANCHOR = "    registry = UnifiedStatementRegistry()\n    links = []\n    records = []\n"
SOURCE_PATCH = (
    "    # Phase 176 R3R28: append a separate source-checked (5.5) quadruple clause.\n"
    "    # Existing source indices remain unchanged; no target group is GIVEN.\n"
    "    if default_sources:\n"
    "        from phase176_r3r27r1_toda55_quadruple_isolated.source import (\n"
    "            build_cited_toda55_quadruple_source,\n"
    "        )\n"
    "        sources = sources + (build_cited_toda55_quadruple_source(),)\n"
)
PROVIDER_ANCHOR = "    from phase165_r12_r15_toda51 import expand_cited_toda51_zero\n"
PROVIDER_PATCH = (
    "    # Phase 176 R3R28: conditional general right-hand side of Toda (5.5).\n"
    "    # The source and both definitions must survive source-first screening.\n"
    "    from phase176_r3r27r1_toda55_quadruple_isolated.source import (\n"
    "        expand_cited_quadruple,\n"
    "    )\n"
    "    def expand_public_toda55_quadruple(goal: object):\n"
    "        return expand_cited_quadruple(goal, tuple(available))\n"
    "    extra_providers = (expand_public_toda55_quadruple,) + tuple(extra_providers)\n"
)


def git(*args: str) -> str:
    result = subprocess.run(("git", *args), cwd=ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + ": " + result.stderr.strip())
    return result.stdout.strip()


def checked_root() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    if not SOURCE.is_file():
        raise RuntimeError("PREVIOUS_ISOLATED_SOURCE_MISSING")
    return git("rev-parse", "HEAD")


def functions_in(source: str) -> dict[str, str]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    return {node.name: "".join(lines[node.lineno - 1:node.end_lineno])
            for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def proposed(current: str) -> str:
    funcs = functions_in(current)
    for name in ("build_shared_typed_bridge", "shared_expansion_provider"):
        if name not in funcs:
            raise RuntimeError("FUNCTION_MISSING: " + name)
    if SOURCE_PATCH.strip() in current and PROVIDER_PATCH.strip() in current:
        return current
    if SOURCE_PATCH.strip() in current or PROVIDER_PATCH.strip() in current:
        raise RuntimeError("PARTIAL_PATCH_DETECTED")
    if funcs["build_shared_typed_bridge"].count(SOURCE_ANCHOR) != 1:
        raise RuntimeError("SOURCE_INSERTION_ANCHOR_CHANGED")
    if funcs["shared_expansion_provider"].count(PROVIDER_ANCHOR) != 1:
        raise RuntimeError("PROVIDER_INSERTION_ANCHOR_CHANGED")
    replacement = funcs["build_shared_typed_bridge"].replace(SOURCE_ANCHOR, SOURCE_PATCH + SOURCE_ANCHOR, 1)
    current = current.replace(funcs["build_shared_typed_bridge"], replacement, 1)
    funcs = functions_in(current)
    replacement = funcs["shared_expansion_provider"].replace(PROVIDER_ANCHOR, PROVIDER_PATCH + PROVIDER_ANCHOR, 1)
    current = current.replace(funcs["shared_expansion_provider"], replacement, 1)
    ast.parse(current)
    return current


def full_code_md(source: str) -> str:
    funcs = functions_in(source)
    return ("# R3R28 変更後の関数全文\n\n"
            "対象: `phase165_r52_r9_shared_math.py`。module-level import は変更しません。\n\n"
            "## build_shared_typed_bridge()\n\n```python\n"
            + funcs["build_shared_typed_bridge"] + "\n```\n\n"
            "## shared_expansion_provider()\n\n```python\n"
            + funcs["shared_expansion_provider"] + "\n```\n")


def output_dir() -> Path:
    path = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    path.mkdir(parents=True, exist_ok=True)
    return path


def execute(dry_run: bool) -> int:
    report = {"phase": "176_R3R28", "gate": "FAIL_R3R28", "full_pytest": "NOT_RUN",
              "new_direct_group_given": 0, "production_target": "phase165_r52_r9_shared_math.py"}
    try:
        report["head"] = checked_root()
        original = TARGET.read_bytes()
        if b"\r\n" in original:
            newline = "\r\n"
        else:
            newline = "\n"
        normalized = original.decode("utf-8-sig").replace("\r\n", "\n")
        output = proposed(normalized)
        report["changed"] = normalized != output
        report["new_source_assertions"] = 1
        report["new_mathematical_rules"] = 0
        if not dry_run:
            if output != normalized:
                # Atomic write without touching unrelated source content.
                data = output.replace("\n", newline).encode("utf-8")
                temporary = TARGET.with_suffix(".r3r28.tmp")
                temporary.write_bytes(data)
                temporary.replace(TARGET)
            (output_dir() / "CHANGED_FUNCTIONS_FULL_JA.md").write_text(full_code_md(output), encoding="utf-8")
            report["gate"] = "PASS_R3R28_PATCH_INSTALLED_TESTS_PENDING"
        else:
            report["gate"] = "PASS_R3R28_DRYRUN"
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
    path = output_dir() / "report.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key in ("gate", "head", "changed", "new_source_assertions", "new_mathematical_rules"):
        if key in report:
            print("PHASE176_R3R28_" + key.upper() + "=" + str(report[key]))
    if "error" in report:
        print("PHASE176_R3R28_ERROR=" + report["error"])
    print("PHASE176_R3R28_REPORT=" + str(path))
    print("PHASE176_R3R28_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())
