from __future__ import annotations
import ast
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "phase165_r57_r7_stable_expansion.py"
REPLACEMENT = Path(__file__).with_name("replacement_function.py.txt")

def main():
    text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(text)
    definitions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "expand_registered_toda45_finite_cyclic_goal"
    ]
    if len(definitions) != 1:
        raise RuntimeError("Expected one existing Toda45 expansion function")
    node = definitions[0]
    if "for iso in available:" not in ast.get_source_segment(text, node):
        raise RuntimeError("Unrecognized existing implementation; no patch applied")
    new_function = REPLACEMENT.read_text(encoding="utf-8")
    ast.parse(new_function)
    lines = text.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno - 1]) + new_function + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    backup = Path(__file__).parent / "backups" / datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup.mkdir(parents=True,exist_ok=False)
    (backup / SOURCE.name).write_text(text,encoding="utf-8")
    SOURCE.write_text(updated,encoding="utf-8")
    (Path(__file__).parent / "modified_function.txt").write_text(new_function, encoding="utf-8")
    print("PATCHED:",SOURCE)
    print("BACKUP:",backup)
    print("FULL FUNCTION:",Path(__file__).parent / "modified_function.txt")

if __name__ == "__main__":
    main()
