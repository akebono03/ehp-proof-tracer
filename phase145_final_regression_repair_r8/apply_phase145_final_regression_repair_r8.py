from __future__ import annotations

from pathlib import Path


PACKAGE_MARKER = Path("tests/__init__.py")
CONFTEST = Path("tests/conftest.py")

CONFTEST_CONTENT = """from __future__ import annotations

import sys
from pathlib import Path


TESTS_DIR = Path(__file__).resolve().parent

if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))
"""


def main() -> int:
    if not Path("tests").is_dir():
        raise RuntimeError("tests directory not found")

    if not PACKAGE_MARKER.exists():
        PACKAGE_MARKER.write_text("", encoding="utf-8")
        print("Created empty package marker: tests/__init__.py")
    else:
        marker_content = PACKAGE_MARKER.read_text(encoding="utf-8-sig")
        if marker_content.strip():
            raise RuntimeError(
                "tests/__init__.py is not empty; refusing to overwrite it"
            )
        print("Kept existing empty package marker: tests/__init__.py")

    if CONFTEST.exists():
        current = CONFTEST.read_text(encoding="utf-8-sig")
        if current != CONFTEST_CONTENT:
            raise RuntimeError(
                "tests/conftest.py already exists with different content; "
                "refusing to overwrite it"
            )
        print("tests/conftest.py already contains the R8 compatibility layer.")
    else:
        CONFTEST.write_text(CONFTEST_CONTENT, encoding="utf-8")
        print("Created import compatibility layer: tests/conftest.py")

    print("Phase 145 Final Regression Repair R8 apply: PASS")
    print("Production code changes: none")
    print("Existing test file changes: none")
    print("New canonical test infrastructure: tests/conftest.py")
    print("Retained package marker: tests/__init__.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
