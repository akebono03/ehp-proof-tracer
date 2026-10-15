"""Regression: R55 selector uses keyword-only n and k."""
from pathlib import Path
import tempfile
import sys
import ast

PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE))
from installer import _replace_selector

SOURCE = 'from __future__ import annotations\n\ndef registered_group_goal_candidates(bridge, *, n: int, k: int) -> tuple:\n    return ()\n'

def main():
    with tempfile.TemporaryDirectory() as work:
        root = Path(work)
        target = root / "phase165_r55_nk_only_goal.py"
        target.write_text(SOURCE, encoding="utf-8")
        result = _replace_selector(root)
        assert result is not None
        content = result[1]
        ast.parse(content)
        assert "def registered_group_goal_candidates(bridge, *, n: int, k: int):" in content
        assert "bridge=bridge, n=n, k=k" in content
        assert "typed_bridge = bridge" in content
        print("R57-R8 keyword-only selector contract: PASS")

if __name__ == "__main__":
    main()
