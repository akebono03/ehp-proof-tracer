"""Install R3-AS narrowly, preserving existing unrelated local modifications."""
import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGETS = (
    ("phase166_r3aj_structured_generator.py", "_base_element", "base_element.txt"),
    ("toda_human_readable_renderer.py", "_render_generator_symbol_latex", "render_generator.txt"),
)

def replace_function(source, function_name, replacement):
    tree = ast.parse(source)
    candidates = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name]
    if len(candidates) != 1:
        raise RuntimeError(f"Expected exactly one top-level function {function_name}; found {len(candidates)}")
    node = candidates[0]
    lines = source.splitlines(keepends=True)
    replacement_text = replacement.rstrip("\n") + "\n"
    return "".join(lines[:node.lineno - 1] + [replacement_text] + lines[node.end_lineno:])

def main():
    replacements = []
    for name, function_name, new_file in TARGETS:
        target = ROOT / name
        old = target.read_text(encoding="utf-8")
        replacement = (PACKAGE / new_file).read_text(encoding="utf-8")
        ast.parse(replacement)
        new = replace_function(old, function_name, replacement)
        compile(new, str(target), "exec")
        replacements.append((target, old, new))
    backup = ROOT / "phase166_r3as_registered_generator_latex_backup"
    backup.mkdir(exist_ok=True)
    for target, old, new in replacements:
        shutil.copy2(target, backup / target.name)
        target.write_text(new, encoding="utf-8")
        print("PATCHED:", target)
    print("BACKUP:", backup)
    print("Full replacement functions: base_element.txt, render_generator.txt")

if __name__ == "__main__":
    main()
