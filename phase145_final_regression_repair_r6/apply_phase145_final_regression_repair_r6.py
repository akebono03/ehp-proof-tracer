from __future__ import annotations

from pathlib import Path


PACKAGE_MARKER = Path("tests/__init__.py")


def main() -> int:
    if not Path("tests").is_dir():
        raise RuntimeError("tests directory not found")

    if PACKAGE_MARKER.exists():
        content = PACKAGE_MARKER.read_text(encoding="utf-8-sig")
        if content.strip():
            raise RuntimeError(
                "tests/__init__.py already exists and is not empty; "
                "refusing to overwrite it"
            )
        print("tests/__init__.py already exists as an empty package marker.")
    else:
        PACKAGE_MARKER.write_text("", encoding="utf-8")
        print("Created empty package marker: tests/__init__.py")

    print("Phase 145 Final Regression Repair R6 apply: PASS")
    print("Production code changes: none")
    print("Existing test file changes: none")
    print("New file only: tests/__init__.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
