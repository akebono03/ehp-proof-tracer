"""R52-R11: install shared proof-forest narrative renderer with checked AST edits."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
COMMON = ROOT / "toda_group_proof_generic_narrative_renderer.py"
PARTIAL = ROOT / "phase165_r52_partial_proof.py"
TEST = ROOT / "test_phase165_r52_r11_common_renderer.py"
FUNCTION_NAME = "render_toda_partial_proof_narrative_markdown"


def replace_function(source: str, name: str, replacement: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one {name}, found {len(matches)}")
    lines = source.splitlines(keepends=True)
    node = matches[0]
    return "".join(lines[:node.lineno - 1]) + replacement.rstrip() + "\n" + "".join(lines[node.end_lineno:])


def main() -> None:
    if not COMMON.is_file() or not PARTIAL.is_file():
        raise FileNotFoundError("Current shared renderer and R52 model are required")
    shared_old = COMMON.read_text(encoding="utf-8-sig")
    partial_old = PARTIAL.read_text(encoding="utf-8-sig")
    function = (BUNDLE / "common_renderer_function.py.txt").read_text(encoding="utf-8")
    wrapper = (BUNDLE / "partial_wrapper_function.py.txt").read_text(encoding="utf-8")
    for code in (function, wrapper):
        tree = ast.parse(code)
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
            raise RuntimeError("Expected complete one-function replacement")
    shared_tree = ast.parse(shared_old)
    existing = [node for node in shared_tree.body
                if isinstance(node, ast.FunctionDef) and node.name == FUNCTION_NAME]
    if existing:
        shared_new = replace_function(shared_old, FUNCTION_NAME, function)
    else:
        shared_new = shared_old.rstrip() + "\n\n\n" + function.rstrip() + "\n"
    partial_new = replace_function(partial_old, "render_partial_proof_markdown", wrapper)
    ast.parse(shared_new)
    ast.parse(partial_new)
    test_src = (BUNDLE / TEST.name).read_text(encoding="utf-8")
    ast.parse(test_src)
    staged = [(COMMON, shared_old, shared_new), (PARTIAL, partial_old, partial_new)]
    # Validate everything before changing production files.
    for path, old, new in staged:
        if old != new:
            backup = path.with_name(path.name + ".phase165_r52_r11_backup")
            if not backup.exists():
                shutil.copy2(path, backup)
            path.write_text(new, encoding="utf-8")
            print("Installed:", path.name)
        else:
            print("Unchanged:", path.name)
    TEST.write_text(test_src, encoding="utf-8")
    print("Installed:", TEST.name)
    # Full replaceable units for review; extract from the actual edited source.
    common_ast = ast.parse(shared_new)
    target = next(node for node in common_ast.body
                  if isinstance(node, ast.FunctionDef) and node.name == FUNCTION_NAME)
    (BUNDLE / "INSTALLED_COMMON_FUNCTION_FULL.txt").write_text(
        "".join(shared_new.splitlines(keepends=True)[target.lineno - 1:target.end_lineno]),
        encoding="utf-8",
    )
    partial_ast = ast.parse(partial_new)
    target = next(node for node in partial_ast.body
                  if isinstance(node, ast.FunctionDef) and node.name == "render_partial_proof_markdown")
    (BUNDLE / "INSTALLED_WRAPPER_FULL.txt").write_text(
        "".join(partial_new.splitlines(keepends=True)[target.lineno - 1:target.end_lineno]),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
