"""Repair only the tab mistakenly emitted instead of LaTeX \to."""
from __future__ import annotations

import ast
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase168_r3_27_typed_statement_projection.py"
OUT = Path(__file__).resolve().parent / "output"


def main():
    raw = TARGET.read_bytes()
    old = raw.decode("utf-8")
    lf = old.replace("\r\n", "\n")
    tree = ast.parse(lf)
    matches = [item for item in tree.body if isinstance(item, ast.FunctionDef)
               and item.name == "typed_sentence"]
    if len(matches) != 1:
        raise RuntimeError("typed_sentence must occur exactly once")
    node = matches[0]
    lines = lf.splitlines(keepends=True)
    function = "".join(lines[node.lineno - 1:node.end_lineno])
    # This is a literal tab following a brace; the original patch interpreted \t.
    broken = "{source}" + "\t" + "o {target}"
    fixed = r"{source}\to {target}"
    if function.count(broken) != 1:
        raise RuntimeError("Expected exactly one broken Toda45 LaTeX arrow; "
                           "inspect source before changing: " + str(function.count(broken)))
    updated = function.replace(broken, fixed)
    rewritten = lf.replace(function, updated, 1)
    ast.parse(rewritten)
    OUT.mkdir(exist_ok=True)
    (OUT / "typed_sentence_BEFORE.py").write_text(function, encoding="utf-8")
    (OUT / "typed_sentence_FULL.py").write_text(updated, encoding="utf-8")
    (OUT / "typed_sentence.diff").write_text("".join(difflib.unified_diff(
        function.splitlines(True), updated.splitlines(True),
        fromfile="typed_sentence:before", tofile="typed_sentence:after")), encoding="utf-8")
    TARGET.write_bytes(rewritten.replace("\n", "\r\n").encode("utf-8")
                       if b"\r\n" in raw else rewritten.encode("utf-8"))
    print("PATCHED:", TARGET)
    print("FULL_FUNCTION:", OUT / "typed_sentence_FULL.py")


if __name__ == "__main__":
    main()
