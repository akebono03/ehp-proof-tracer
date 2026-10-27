"""Minimal single-function patch, pinned to an audited GitHub blob."""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
EXPECTED_GIT_BLOB = "8a9d534f87cb04b807dca4b3b2ef09e2d3eaa1c5"
ANCHOR = "        options.extend(expand_cited_eta_generator(goal))\n"
INSERT = (
    "        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity\n"
    "        options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))\n"
)


def _git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def main() -> None:
    if _git("branch", "--show-current") != "develop":
        raise RuntimeError("R4B requires branch develop")
    if not TARGET.is_file():
        raise RuntimeError("expected shared provider file missing")
    if _git("rev-parse", "HEAD:" + TARGET.name) != EXPECTED_GIT_BLOB:
        raise RuntimeError("HEAD shared provider differs from the verified GitHub blob; stop")
    if _git("diff", "--", TARGET.name) or _git("diff", "--cached", "--", TARGET.name):
        raise RuntimeError("shared provider has local tracked changes; stop")
    original = TARGET.read_bytes()
    newline = "\r\n" if b"\r\n" in original else "\n"
    source = original.decode("utf-8").replace("\r\n", "\n")
    if source.count(ANCHOR) != 1 or INSERT.strip() in source:
        raise RuntimeError("shared expansion insertion point is not unique or already installed")
    new_source = source.replace(ANCHOR, ANCHOR + INSERT, 1)
    tree = ast.parse(new_source, filename=str(TARGET))
    funcs = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))
             and x.name == "shared_expansion_provider"]
    if len(funcs) != 1:
        raise RuntimeError("expected a single shared_expansion_provider definition")
    function = funcs[0]
    lines = new_source.splitlines(keepends=True)
    full_function = "".join(lines[function.lineno - 1:function.end_lineno])
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    (output / "phase165_r52_r9_shared_math.py.before").write_bytes(original)
    (output / "phase165_r52_r9_shared_math.py.FULL").write_text(new_source, encoding="utf-8")
    (output / "shared_expansion_provider_FULL.py").write_text(full_function, encoding="utf-8")
    TARGET.write_bytes(new_source.replace("\n", newline).encode("utf-8"))
    print("R4B_PATCHED=" + str(TARGET))
    print("R4B_BACKUP=" + str(output / "phase165_r52_r9_shared_math.py.before"))
    print("R4B_FULL_FUNCTION=" + str(output / "shared_expansion_provider_FULL.py"))
    print("R4B_FULL_FILE=" + str(output / "phase165_r52_r9_shared_math.py.FULL"))


if __name__ == "__main__":
    main()
