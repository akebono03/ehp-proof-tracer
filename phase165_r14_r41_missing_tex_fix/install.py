"""Modify only the existing R40 dispatch branch, preserving other branches."""
from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase164_r5_r2_common_replay.py"

def main():
    code = TARGET.read_text(encoding="utf-8")
    tree = ast.parse(code)
    matches = [n for n in tree.body if isinstance(n, ast.FunctionDef)
               and n.name == "build_phase164_r5_r2_common_replay"]
    if len(matches) != 1:
        raise RuntimeError("shared replay dispatch not found")
    f = matches[0]
    branches = [n for n in f.body if isinstance(n, ast.If)
                and "build_phase165_r40_pi32_common_replay" in ast.unparse(n)]
    if len(branches) != 1:
        raise RuntimeError("expected exactly one R40 replay branch")
    n = branches[0]
    if "n == 2" not in ast.unparse(n.test) or "k == 1" not in ast.unparse(n.test):
        raise RuntimeError("R40 dispatch branch target changed")
    replacement = (
        "    if n == 2 and k == 1:\n"
        "        from phase165_r14_r41_proof_transfer import build_phase165_r41_pi32_common_replay\n"
        "        return build_phase165_r41_pi32_common_replay(group_result, max_depth, mode)\n"
    )
    lines = code.splitlines(keepends=True)
    updated = "".join(lines[:n.lineno-1] + [replacement] + lines[n.end_lineno:])
    compile(updated, str(TARGET), "exec")
    backup = TARGET.with_name("phase164_r5_r2_common_replay.phase165_r41_backup.py")
    if not backup.exists():
        backup.write_text(code, encoding="utf-8")
    TARGET.write_text(updated, encoding="utf-8")
    print("R41 full-depth narrative dispatch installed; shared renderer unchanged")

if __name__ == "__main__":
    main()
