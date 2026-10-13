"""Install or restore a group-proof-only presentation without changing routes."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil

ROOT = Path.cwd()
TEMPLATE = ROOT / "templates" / "index.html"
BACKUP = TEMPLATE.with_name("index.html.phase165_r52_r6_before_layout")
START = "    <!-- R52-R6: group proof only; presentation-layer switch -->"
END = "    <!-- /R52-R6: group proof only -->"
BLOCK = """    <!-- R52-R6: group proof only; presentation-layer switch -->
    <style id="phase165-group-proof-only-layout">
      /* Keep group input, its result, and the existing group proof visible. */
      main > nav,
      main > section:not(#group-query):not([aria-labelledby="result-heading"]):not([aria-labelledby="group-proof-heading"]) {
        display: none !important;
      }
    </style>
    <!-- /R52-R6: group proof only -->
"""


def install() -> None:
    if not TEMPLATE.is_file():
        raise FileNotFoundError("Run from the EHP Proof Tracer repository root")
    source = TEMPLATE.read_text(encoding="utf-8-sig")
    if START in source:
        if source.count(START) != 1 or source.count(END) != 1 or BLOCK not in source:
            raise RuntimeError("An unknown R52-R6 layout edit is present; refusing to overwrite")
        install_test()
        print("Already installed: templates/index.html")
        return
    if not all(token in source for token in (
        'id="group-query"',
        'aria-labelledby="result-heading"',
        'aria-labelledby="group-proof-heading"',
        'id="group-proof-progress-query"',
    )):
        raise RuntimeError("Unexpected template version: group/proof/progress sections not found")
    if source.count("</head>") != 1:
        raise RuntimeError("Unexpected template: </head> missing or duplicated")
    if BACKUP.exists():
        raise RuntimeError("Existing R52-R6 backup found without patch; refuse to overwrite")
    updated = source.replace("</head>", BLOCK + "</head>", 1)
    if not (updated.count(START) == 1 and updated.count(END) == 1):
        raise RuntimeError("Layout insertion failed")
    shutil.copy2(TEMPLATE, BACKUP)
    TEMPLATE.write_text(updated, encoding="utf-8")
    print("Installed: templates/index.html (other UI hidden, not deleted)")
    print("Backup:", BACKUP)
    install_test()


def install_test() -> None:
    bundled = Path(__file__).resolve().with_name("test_phase165_r52_r6_group_proof_only.py")
    target = ROOT / bundled.name
    content = bundled.read_text(encoding="utf-8")
    if target.exists() and target.read_text(encoding="utf-8-sig") != content:
        raise RuntimeError("Existing layout test differs; refusing to overwrite")
    if not target.exists():
        target.write_text(content, encoding="utf-8")
    print("Installed: " + bundled.name)


def restore() -> None:
    if not TEMPLATE.is_file():
        raise FileNotFoundError(str(TEMPLATE))
    source = TEMPLATE.read_text(encoding="utf-8-sig")
    if BLOCK not in source or source.count(BLOCK) != 1:
        raise RuntimeError("Installed R52-R6 block not found exactly; refusing to alter template")
    TEMPLATE.write_text(source.replace(BLOCK, "", 1), encoding="utf-8")
    print("Restored: templates/index.html (all UI displayed again)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    if args.restore:
        restore()
    else:
        install()


if __name__ == "__main__":
    main()
