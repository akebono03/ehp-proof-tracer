"""Collect the repository pytest items using pytest's actual collection process."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


class Collector:
    def __init__(self) -> None:
        self.nodeids: list[str] = []

    def pytest_collection_finish(self, session: pytest.Session) -> None:
        self.nodeids = [item.nodeid for item in session.items]


def main() -> int:
    output = Path(sys.argv[1])
    plugin = Collector()
    code = pytest.main(["--collect-only", "-q"], plugins=[plugin])
    if code not in (pytest.ExitCode.OK, pytest.ExitCode.NO_TESTS_COLLECTED):
        return int(code)
    if not plugin.nodeids:
        print("ERROR: no tests collected", flush=True)
        return 5
    output.write_text(json.dumps(plugin.nodeids, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Collected {len(plugin.nodeids)} pytest items", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
