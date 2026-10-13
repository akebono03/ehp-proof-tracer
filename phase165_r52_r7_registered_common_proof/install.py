"""Conservative R52-R7 installer: never overwrite unexpected local state."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
TARGET = ROOT / "phase164_r5_r2_common_replay.py"


def main():
    for path in ("web_group_proof.py", "phase165_r14_r38_direct_registry.py",
                 "phase165_r14_r39_toda51.tex", "phase165_r52_r5_auto_search.py"):
        if not (ROOT / path).is_file():
            raise FileNotFoundError("Required dependency missing: " + path)
    old = TARGET.read_text(encoding="utf-8-sig")
    expected = 'if n == 2 and k == 1:'
    updated = (BUNDLE / TARGET.name).read_text(encoding="utf-8")
    if expected not in old and old != updated:
        raise RuntimeError("Unexpected common replay source; refusing to overwrite")
    for name in ("phase165_r52_r7_registered_common_proof.py", TARGET.name,
                 "test_phase165_r52_r7_registered_common_proof.py"):
        content = (BUNDLE / name).read_text(encoding="utf-8")
        ast.parse(content)
    if old != updated:
        backup = TARGET.with_suffix(".py.phase165_r52_r7_backup")
        if not backup.exists():
            shutil.copy2(TARGET, backup)
    for name in ("phase165_r52_r7_registered_common_proof.py", TARGET.name,
                 "test_phase165_r52_r7_registered_common_proof.py"):
        dst = ROOT / name
        src = (BUNDLE / name).read_text(encoding="utf-8")
        dst.write_text(src, encoding="utf-8")
        print("Installed:", name)


if __name__ == "__main__":
    main()
