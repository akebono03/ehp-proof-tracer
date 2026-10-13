"""Install R52-R5 on top of the tested R52-R4 code, fail closed on drift."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
APP = ROOT / "web_app.py"
BRIDGE = ROOT / "phase165_r52_r4_flask_bridge.py"


def main() -> None:
    for name in (
        "web_app.py",
        "phase165_r52_partial_proof.py",
        "phase165_r52_r2_search_adapter.py",
        "phase165_r52_r3_web_adapter.py",
        "phase165_r52_r4_flask_bridge.py",
    ):
        if not (ROOT / name).is_file():
            raise FileNotFoundError(f"Required existing file missing: {name}")

    app = APP.read_text(encoding="utf-8-sig")
    old_import = "from web_group_proof import ("
    new_import = (
        "from phase165_r52_r4_flask_bridge import (\n"
        "  build_group_proof_progress_view,\n"
        ")\n"
        "from web_group_proof import ("
    )
    if new_import not in app:
        if app.count(old_import) != 1:
            raise RuntimeError("R52-R4 Flask import state unexpected")
        app = app.replace(old_import, new_import, 1)

    # The old group lookup remains an independent calculation query. The NEW
    # proof output is generated via the registered prover; no proof replay.
    old_block = '''          view = (
            build_standard_web_group_query_view(
              n=n,
              k=k,
            )
          )'''
    new_block = old_block + '''
          if n >= 2 and k >= 0:
            group_proof_view = build_group_proof_progress_view(
              n=n, k=k,
            )'''
    if new_block not in app:
        if app.count(old_block) != 2:
            raise RuntimeError("unexpected Group query route; refusing to patch")
        # Only patch the final default Group query route, not the
        # explicit legacy group_proof route.
        position = app.rfind(old_block)
        app = app[:position] + new_block + app[position + len(old_block):]

    ast.parse(app)
    if app.count('elif form_kind == "group_proof_progress"') != 1:
        raise RuntimeError("R52-R4 progress route missing")
    if app.count("group_proof_view = build_group_proof_progress_view(") != 2:
        raise RuntimeError("expected both group and progress proof entry points")

    source_names = (
        "phase165_r52_r5_auto_search.py",
        "phase165_r52_r4_flask_bridge.py",
        "test_phase165_r52_r5_auto_search.py",
        "test_phase165_r52_r4_flask_connection.py",
    )
    staged = {APP: app}
    for name in source_names:
        code = (BUNDLE / name).read_text(encoding="utf-8")
        ast.parse(code)
        staged[ROOT / name] = code

    existing_r4_test = ROOT / "test_phase165_r52_r4_flask_connection.py"
    if existing_r4_test.is_file():
        current_test = existing_r4_test.read_text(encoding="utf-8-sig")
        if not ("def test_unconfigured_search_is_explicitly_not_searched_outside_112" in current_test
                or "def test_group_progress_runs_automatic_search_outside_112" in current_test):
            raise RuntimeError("Unexpected R52-R4 test version")

    current_bridge = BRIDGE.read_text(encoding="utf-8-sig")
    original_intro = '"""R52-R4: Flask-independent bridge'
    r5_intro = '"""R52-R5: Flask bridge'
    if not (current_bridge.startswith(original_intro) or current_bridge.startswith(r5_intro)):
        raise RuntimeError("unexpected R52-R4 bridge; refusing to overwrite")

    # Preserve copies of complete replacement units (including imports).
    tree = ast.parse(app)
    create = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "create_app")
    index = next(n for n in create.body if isinstance(n, ast.FunctionDef) and n.name == "index")
    lines = app.splitlines(keepends=True)
    (BUNDLE / "web_app_IMPORTS_FULL.py.txt").write_text(
        "".join(lines[:create.lineno-1]), encoding="utf-8"
    )
    (BUNDLE / "web_app_index_FULL.py.txt").write_text(
        "".join(lines[index.lineno-1:index.end_lineno]), encoding="utf-8"
    )
    for path in (APP, BRIDGE):
        backup = path.with_suffix(path.suffix + ".phase165_r52_r5_backup")
        if not backup.exists():
            shutil.copy2(path, backup)
    for path, content in staged.items():
        if path.exists() and path.read_text(encoding="utf-8-sig") == content:
            print("Unchanged:", path.relative_to(ROOT))
        else:
            path.write_text(content, encoding="utf-8")
            print("Installed:", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
