"""R3-36F corrective patch; change only recursion context sink forwarding."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "output"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OLD = "                context_sink=context_sink,"
NEW = "                context_sink=context_sink if statement == goal else None,"


def main() -> None:
    raw = TARGET.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    source = raw.decode("utf-8").replace("\r\n", "\n")
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "search_shared_group_goal"]
    if len(functions) != 1:
        raise RuntimeError("search_shared_group_goal must occur exactly once")
    fn = functions[0]
    lines = source.splitlines(keepends=True)
    before = "".join(lines[fn.lineno - 1:fn.end_lineno])
    if before.count(OLD) != 1:
        if NEW in before:
            print("ALREADY_PATCHED: recursive sink already scoped to target")
            return
        raise RuntimeError("Expected exactly one recursive context_sink anchor; repository version differs")
    after = before.replace(OLD, NEW, 1)
    updated = "".join(lines[:fn.lineno - 1]) + after + "".join(lines[fn.end_lineno:])
    ast.parse(updated)
    OUT.mkdir(exist_ok=True)
    (OUT / "search_shared_group_goal_BEFORE.py").write_text(before, encoding="utf-8")
    (OUT / "search_shared_group_goal_FULL.py").write_text(after, encoding="utf-8")
    TARGET.write_bytes(updated.replace("\n", newline).encode("utf-8"))
    print("PATCHED:", TARGET)
    print("FULL_FUNCTION:", OUT / "search_shared_group_goal_FULL.py")


if __name__ == "__main__":
    main()
