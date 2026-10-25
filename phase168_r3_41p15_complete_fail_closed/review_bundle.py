"""Pack P15 focused evidence with disjoint before/after artifact names."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".zip"):
        raise SystemExit("Usage: python -m phase168_r3_41p15_complete_fail_closed.review_bundle <name.zip>")
    bundle = OUTPUT / sys.argv[1]
    selected = [
        OUTPUT / "manifest.json",
        OUTPUT / "web_group_proof.py.FULL.py",
        OUTPUT / "test_phase168_r3_41p14_trust_boundary_audit.py.FULL.py",
        OUTPUT / "pytest_focused_stdout.log",
        OUTPUT / "pytest_focused_stderr.log",
    ]
    selected.extend(sorted((OUTPUT / "before").glob("*")))
    selected.extend(sorted((OUTPUT / "after").glob("*")))
    publication = ROOT / "phase168_r3_41p12_publication_boundary_audit" / "output"
    for name in ("audit.md", "audit.json"):
        selected.append(publication / name)
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in selected:
            if not path.is_file():
                continue
            if publication in path.parents:
                arcname = "publication_audit/" + path.name
            else:
                arcname = path.relative_to(OUTPUT).as_posix()
            archive.write(path, arcname)
    with zipfile.ZipFile(bundle) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Review archive CRC failure")
        members = archive.namelist()
        if len(set(members)) != len(members):
            raise RuntimeError("Review archive includes duplicate names")
    print("REVIEW_BUNDLE", bundle)


if __name__ == "__main__":
    main()
