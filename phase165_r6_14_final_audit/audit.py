"""Phase 165 R6-14: read-only active dependency and pytest collection audit."""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

LEGACY_MODULES = {"probes.probe_phase49_capabilities", "probes.probe_phase56_capabilities"}
LEGACY_BUILDERS = {"build_phase49_representative_result", "build_phase56_representative_result"}
REQUIRED_ABSENT = ("probes/probe_phase49_capabilities.py", "probes/probe_phase56_capabilities.py")
REQUIRED_PRESENT = ("phase165_r55_nk_only_goal.py", "phase165_r52_r9_shared_math.py", "probes/probe_phase58_capabilities.py")


def active_sources(root: Path) -> list[Path]:
    sources = sorted(root.glob("*.py"))
    for directory in ("tests", "probes"):
        folder = root / directory
        if folder.is_dir():
            sources.extend(sorted(folder.rglob("*.py")))
    return sources


def scan(root: Path) -> dict:
    findings = []
    errors = []
    inspected = 0
    for path in active_sources(root):
        relative = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=relative)
        except (SyntaxError, UnicodeError) as exc:
            errors.append({"path": relative, "error": str(exc)})
            continue
        inspected += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in LEGACY_MODULES:
                findings.append({"path": relative, "line": node.lineno, "kind": "import_from", "module": node.module})
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in LEGACY_MODULES:
                        findings.append({"path": relative, "line": node.lineno, "kind": "import", "module": alias.name})
            elif isinstance(node, ast.Call):
                target = node.func
                if isinstance(target, ast.Name) and target.id in LEGACY_BUILDERS:
                    findings.append({"path": relative, "line": node.lineno, "kind": "legacy_builder_call", "name": target.id})
                if isinstance(target, ast.Attribute) and target.attr in LEGACY_BUILDERS:
                    findings.append({"path": relative, "line": node.lineno, "kind": "legacy_builder_attribute_call", "name": target.attr})
    missing = [p for p in REQUIRED_PRESENT if not (root / p).is_file()]
    remaining = [p for p in REQUIRED_ABSENT if (root / p).exists()]
    entry = root / "phase165_r55_nk_only_goal.py"
    entry_verified = False
    if entry.exists():
        try:
            t = ast.parse(entry.read_text(encoding="utf-8-sig"))
            entry_verified = any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "search_group_from_registered_goal" for n in t.body)
        except (SyntaxError, UnicodeError):
            pass
    return {"active_python_files_parsed": inspected, "legacy_references": findings, "parse_errors": errors, "missing_required_modules": missing, "retired_probes_still_present": remaining, "shared_entry_function_present": entry_verified}


def run_collection(root: Path, output: Path) -> dict:
    command = [sys.executable, "-m", "pytest", "--collect-only", "-q", "tests"]
    try:
        with (output / "collection_stdout.txt").open("w", encoding="utf-8") as stdout, (output / "collection_stderr.txt").open("w", encoding="utf-8") as stderr:
            result = subprocess.run(command, cwd=root, stdout=stdout, stderr=stderr, timeout=900, check=False)
        return {"command": command, "returncode": result.returncode, "stdout_file": "collection_stdout.txt", "stderr_file": "collection_stderr.txt", "timeout": False}
    except subprocess.TimeoutExpired:
        return {"command": command, "returncode": None, "stdout_file": "collection_stdout.txt", "stderr_file": "collection_stderr.txt", "timeout": True}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    output = root / "phase165_r6_audit_results" / "r6_14_final_audit"
    output.mkdir(parents=True, exist_ok=True)
    static = scan(root)
    collection = run_collection(root, output)
    ready = (not static["legacy_references"] and not static["parse_errors"] and not static["missing_required_modules"] and not static["retired_probes_still_present"] and static["shared_entry_function_present"] and collection["returncode"] == 0)
    report = {"phase": "165 R6-14", "mode": "read_only", "generated_utc": datetime.now(timezone.utc).isoformat(), "status": "READY_FOR_FINAL_PYTEST" if ready else "BLOCKED_FOR_REVIEW", "static_audit": static, "collection": collection, "full_pytest_run": False}
    (output / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("Collection-only completed; full pytest NOT run.")
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
