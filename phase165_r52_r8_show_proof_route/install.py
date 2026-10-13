"""R52-R8: align Show proof fallback with the actual partial-search route.

Only the explicit Group proof button path is changed. A registered proof is
always attempted first, and only a missing registered Goal/rule configuration
causes a fallback to the actual partial-search result.
"""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
APP = ROOT / "web_app.py"

OLD = """          group_proof_view = (
            build_standard_web_group_proof_view(
              n,
              k,
              max_depth=group_proof_depth,
              mode=group_proof_mode_value,
            )
          )"""

NEW = """          try:
            group_proof_view = (
              build_standard_web_group_proof_view(
                n,
                k,
                max_depth=group_proof_depth,
                mode=group_proof_mode_value,
              )
            )
          except GoalSearchIncompleteError:
            group_proof_view = build_group_proof_progress_view(
              n=n,
              k=k,
              max_depth=group_proof_depth,
            )"""

IMPORT = """from phase165_goal_only_search import GoalSearchIncompleteError
"""


def main() -> None:
    for name in (
        "web_app.py",
        "phase165_goal_only_search.py",
        "phase165_r52_r4_flask_bridge.py",
        "phase165_r52_r5_auto_search.py",
        "phase165_r52_r7_registered_common_proof.py",
    ):
        if not (ROOT / name).is_file():
            raise FileNotFoundError("Required file missing: " + name)
    old = APP.read_text(encoding="utf-8-sig")
    if OLD in old and NEW not in old:
        if old.count(OLD) != 1:
            raise RuntimeError("Unexpected multiple group proof routes")
        out = old.replace(OLD, NEW, 1)
    elif NEW in old and OLD not in old:
        out = old
    else:
        raise RuntimeError(
            "Current web_app.py Group proof route differs; no files changed"
        )
    if IMPORT not in out:
        import_anchor = "from web_group_proof import ("
        if out.count(import_anchor) != 1:
            raise RuntimeError("Unknown imports layout; no files changed")
        out = out.replace(import_anchor, IMPORT + "\n" + import_anchor, 1)
    if out.count(IMPORT) != 1:
        raise RuntimeError("Unexpected duplicate import")
    tree = ast.parse(out)
    funcs = [x for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)
             and x.name == "index"]
    if len(funcs) != 1:
        raise RuntimeError("Expected exactly one Flask index method")
    source_lines = out.splitlines(keepends=True)
    index_fn = funcs[0]
    full_index = "".join(
        source_lines[index_fn.lineno - 1:index_fn.end_lineno]
    )
    (BUNDLE / "web_app_index_FULL.txt").write_text(
        full_index, encoding="utf-8"
    )
    (BUNDLE / "web_app_IMPORTS_FULL.txt").write_text(
        "".join(source_lines[:index_fn.lineno - 1]), encoding="utf-8"
    )
    test_src = (BUNDLE / "test_phase165_r52_r8_show_proof_route.py").read_text(
        encoding="utf-8"
    )
    ast.parse(test_src)
    test_dest = ROOT / "test_phase165_r52_r8_show_proof_route.py"
    if out != old:
        backup = ROOT / "web_app.py.phase165_r52_r8_backup"
        if not backup.exists():
            shutil.copy2(APP, backup)
        APP.write_text(out, encoding="utf-8")
        print("Installed: web_app.py")
    else:
        print("Unchanged: web_app.py")
    if not test_dest.exists() or test_dest.read_text(encoding="utf-8") != test_src:
        test_dest.write_text(test_src, encoding="utf-8")
        print("Installed: test_phase165_r52_r8_show_proof_route.py")


if __name__ == "__main__":
    main()
