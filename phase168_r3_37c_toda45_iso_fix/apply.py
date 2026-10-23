"""Patch only typed_sentence; preserve prior R3-37C Reference work."""
from __future__ import annotations

import ast
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase168_r3_27_typed_statement_projection.py"
OUT = Path(__file__).resolve().parent / "output"

INSERT = '''
    from toda_rules import Toda45IsomorphismStatement
    from homotopy_groups import TodaIteratedSuspensionMap
    if isinstance(statement, Toda45IsomorphismStatement):
        mapping = statement.map
        if isinstance(mapping, TodaIteratedSuspensionMap):
            source = group_tex(mapping.source_group)
            target = group_tex(mapping.target_group)
            exponent = mapping.exponent
            if source is not None and target is not None and type(exponent) is int and exponent >= 1:
                symbol = "E" if exponent == 1 else rf"E^{{{exponent}}}"
                return rf"${symbol}: {source}\to {target}$ は同型である."
'''

def main():
    raw = TARGET.read_bytes()
    crlf = b"\r\n" in raw
    old = raw.decode("utf-8").replace("\r\n", "\n")
    tree = ast.parse(old)
    funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "typed_sentence"]
    if len(funcs) != 1:
        raise RuntimeError("Expected one typed_sentence")
    node = funcs[0]
    body = old.splitlines(keepends=True)
    function_source = "".join(body[node.lineno - 1:node.end_lineno])
    if "from toda_rules import Toda45IsomorphismStatement" in function_source:
        raise RuntimeError("Existing Toda45 block detected. Review before reapplying.")
    header = "def typed_sentence(statement, step):\n"
    if function_source.count(header) != 1:
        raise RuntimeError("Unexpected typed_sentence header")
    new_function = function_source.replace(header, header + INSERT, 1)
    new = old.replace(function_source, new_function, 1)
    ast.parse(new)
    OUT.mkdir(exist_ok=True)
    (OUT / "typed_sentence_BEFORE.py").write_text(function_source, encoding="utf-8")
    (OUT / "typed_sentence_FULL.py").write_text(new_function, encoding="utf-8")
    (OUT / "phase168_r3_27_typed_statement_projection.diff").write_text(
        "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                    fromfile="before", tofile="after")), encoding="utf-8")
    TARGET.write_bytes(new.replace("\n", "\r\n").encode("utf-8") if crlf else new.encode("utf-8"))
    print("PATCHED:", TARGET)
    print("FULL_FUNCTION:", OUT / "typed_sentence_FULL.py")


if __name__ == "__main__":
    main()
