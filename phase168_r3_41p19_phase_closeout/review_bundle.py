"""Archive the final verification evidence from this package."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".zip"):
        raise SystemExit("Usage: python -m phase168_r3_41p19_phase_closeout.review_bundle <name.zip>")
    selected = [OUTPUT / "manifest.json", OUTPUT / "verification.py.FULL.py",
                OUTPUT / "pytest_focused_stdout.log", OUTPUT / "pytest_focused_stderr.log",
                OUTPUT / "pytest_full_stdout.log", OUTPUT / "pytest_full_stderr.log",
                OUTPUT / "active_suite_diagnostics.json", OUTPUT / "active_suite_diagnostics.md",
                OUTPUT / "active_tests_manifest.json"]
    selected.extend(sorted((OUTPUT / "active_test_backups").glob("*")))
    selected.extend(sorted((PACKAGE / "active_test_full_files").glob("*")))
    selected.extend(sorted((OUTPUT / "before").glob("*")))
    selected.extend(sorted((OUTPUT / "after").glob("*")))
    pub = ROOT / "phase168_r3_41p12_publication_boundary_audit" / "output"
    selected.extend([pub / "audit.md", pub / "audit.json"])
    with zipfile.ZipFile(OUTPUT / sys.argv[1], "w", zipfile.ZIP_DEFLATED) as z:
        for path in selected:
            if path.is_file():
                arc = ("publication_audit/" + path.name if path.parent == pub else
                       ("active_test_full_files/" + path.name) if path.parent == PACKAGE / "active_test_full_files"
                       else path.relative_to(OUTPUT).as_posix())
                z.write(path, arc)
    with zipfile.ZipFile(OUTPUT / sys.argv[1]) as z:
        if z.testzip() is not None:
            raise RuntimeError("review bundle corruption")
    print("REVIEW_BUNDLE", OUTPUT / sys.argv[1])


if __name__ == "__main__":
    main()
