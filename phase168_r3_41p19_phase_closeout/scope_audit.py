"""Read-only diagnosis of active-suite test dependency and pytest results.

No test is skipped, patched, or silently treated as passing. The current
historical archive is inspected only as evidence of a moved dependency.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"


def missing_test_dependencies(root: Path) -> list[dict[str, object]]:
    """Locate imports of root tests helpers that are no longer in tests/."""
    tests = root / "tests"
    if not tests.is_dir():
        raise FileNotFoundError("tests/ is missing")
    results: list[dict[str, object]] = []
    archive = root / "archive"
    archived_paths: dict[str, list[str]] = {}
    if archive.exists():
        for path in archive.rglob("test_*.py"):
            archived_paths.setdefault(path.name, []).append(
                path.relative_to(root).as_posix()
            )
    for file in sorted(tests.rglob("test_*.py")):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8-sig"), filename=str(file))
        except (UnicodeError, SyntaxError) as exc:
            results.append({
                "from": file.relative_to(root).as_posix(),
                "module": "(unparseable)",
                "archived": [],
                "note": str(exc),
            })
            continue
        requested: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                mod = node.module
                if mod.startswith("tests.test_"):
                    requested.add(mod)
                elif node.level == 1 and mod.startswith("test_"):
                    requested.add("tests." + mod)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("tests.test_"):
                        requested.add(alias.name)
        for module in sorted(requested):
            parts = module.split(".")
            expected = root.joinpath(*parts).with_suffix(".py")
            expected_package = root.joinpath(*parts) / "__init__.py"
            if expected.is_file() or expected_package.is_file():
                continue
            basename = parts[-1] + ".py"
            results.append({
                "from": file.relative_to(root).as_posix(),
                "module": module,
                "archived": archived_paths.get(basename, []),
                "note": "required tests helper is absent from active tests/",
            })
    return results


def diagnostic_lines(output: str) -> list[str]:
    """Keep short pytest error markers without assuming output language/style."""
    return [line.strip() for line in output.splitlines() if (
        "ERROR collecting" in line
        or line.startswith(("ERROR ", "FAILED ", "ImportError", "ModuleNotFoundError"))
        or "short test summary info" in line
        or re.search(r"[0-9]+ (?:failed|error|errors|passed|deselected)", line)
    )][-160:]


def generate_report(root: Path, output: Path, pytest_code: int | None) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    missing = missing_test_dependencies(root)
    stdout_path = output / "pytest_full_stdout.log"
    stderr_path = output / "pytest_full_stderr.log"
    body = ""
    if pytest_code is not None:
        if stdout_path.is_file():
            body += stdout_path.read_text(encoding="utf-8-sig", errors="replace")
        if stderr_path.is_file():
            body += "\n" + stderr_path.read_text(encoding="utf-8-sig", errors="replace")
    status = "PREFLIGHT_ONLY" if pytest_code is None else (
        "ACTIVE_SUITE_PASS" if pytest_code == 0 and not missing
        else "ACTIVE_SUITE_INCOMPLETE"
    )
    report = {
        "phase": "168 R3-41P19 R2",
        "scope": "tests/ (no automatic ignores or exclusion)",
        "status": status,
        "pytest_exit_code": pytest_code,
        "missing_active_test_dependencies": missing,
        "pytest_diagnostic_lines": diagnostic_lines(body),
        "full_suite_certified": status == "ACTIVE_SUITE_PASS",
        "application_files_changed_by_scope_audit": False,
    }
    (output / "active_suite_diagnostics.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 168 — Active pytest 収集範囲診断", "",
        f"- 実行対象: `{report['scope']}`", f"- 判定: `{status}`",
        f"- pytest exit code: `{pytest_code}`",
        f"- 欠落した test helper の静的参照数: `{len(missing)}`", "",
        "収集エラーや失敗は無視していない。PASS と記録するのは pytest exit code 0 で、",
        "既知の欠落した test helper がない場合に限る。", "",
        "## 欠落するテスト依存", "",
    ]
    for record in missing:
        lines.append(f"- `{record['from']}` -> `{record['module']}`")
        for historical in record["archived"]:
            lines.append(f"  - 退避先: `{historical}`")
    if not missing:
        lines.append("- 直接 import の欠落は静的検査では検出されなかった。")
    lines.extend(["", "## pytest の主な診断行", ""])
    if report["pytest_diagnostic_lines"]:
        lines.extend("- " + item.replace("`", "'") for item in report["pytest_diagnostic_lines"])
    else:
        lines.append("- 取得なし")
    lines.extend(["", "## 完了判定", "", "静的検査は動的 import 全体を保証しない。",
                  "pytest が失敗した場合は Phase 168 の全体テスト合格と判定しない。", ""])
    (output / "active_suite_diagnostics.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("preflight", "after"))
    parser.add_argument("--pytest-code", type=int)
    options = parser.parse_args()
    if options.stage == "after" and options.pytest_code is None:
        parser.error("after requires --pytest-code")
    report = generate_report(ROOT, OUTPUT, options.pytest_code if options.stage == "after" else None)
    print("ACTIVE_SUITE_DIAG_STATUS", report["status"], flush=True)
    print("MISSING_ACTIVE_TEST_DEPENDENCIES", len(report["missing_active_test_dependencies"]), flush=True)
    print("SCOPE_DIAGNOSTICS", OUTPUT / "active_suite_diagnostics.md", flush=True)
    print("FULL_SUITE_CERTIFIED", report["full_suite_certified"], flush=True)


if __name__ == "__main__":
    main()
