"""Print complete modified functions for review, never shorten source with ellipses."""
from __future__ import annotations

import ast
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    path = root / "phase165_r52_r9_shared_math.py"
    content = path.read_text(encoding="utf-8")
    tree = ast.parse(content)
    lines = content.splitlines(keepends=True)
    for name in ("build_shared_typed_bridge", "shared_expansion_provider"):
        node = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name), None)
        if node is None:
            raise RuntimeError("MISSING_FUNCTION_" + name)
        print("## " + name)
        print("```python")
        print("".join(lines[node.lineno - 1:node.end_lineno]), end="\n")
        print("```")


if __name__ == "__main__":
    main()
