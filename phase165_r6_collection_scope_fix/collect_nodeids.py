"""Collect current candidate tests without walking historical package directories.

The scope is explicit and auditable; collection failures never count as PASS.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


class Collector:
    def __init__(self) -> None:
        self.nodeids: list[str] = []
        self.errors: list[str] = []

    def pytest_collection_finish(self, session: pytest.Session) -> None:
        self.nodeids = [item.nodeid for item in session.items]

    def pytest_collectreport(self, report: pytest.CollectReport) -> None:
        if report.failed:
            self.errors.append(str(report.nodeid))


def selection(root: Path) -> list[str]:
    paths = []
    tests = root / "tests"
    if tests.is_dir():
        paths.append(str(tests))
    paths.extend(str(p) for p in sorted(root.glob("test_*.py")) if p.is_file())
    if not paths:
        raise RuntimeError("No current test roots found")
    return paths


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    diagnostics = Path(sys.argv[3]).resolve()
    plugin = Collector()
    paths = selection(root)
    # -o overrides repository-wide testpaths/norecursedirs that could change scope.
    code = pytest.main(["--collect-only", "-q", "--continue-on-collection-errors", *paths], plugins=[plugin])
    report = {
        "scope": [str(Path(p).relative_to(root)) for p in paths],
        "explicit_exclusions": ["archive/", "phase*/ (except root test_*.py)", "backup/", "payload/", "files/"],
        "item_count": len(plugin.nodeids),
        "collection_errors": plugin.errors,
        "collection_exit_code": int(code),
        "status": "COLLECTION_OK" if code == pytest.ExitCode.OK and not plugin.errors and plugin.nodeids else "COLLECTION_FAILED",
    }
    diagnostics.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Scoped collection: {len(plugin.nodeids)} tests, {len(plugin.errors)} errors", flush=True)
    if report["status"] != "COLLECTION_OK":
        return 1
    output.write_text(json.dumps(plugin.nodeids, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
