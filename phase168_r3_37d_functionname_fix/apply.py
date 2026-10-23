"""Guarded replacement of the actual R3-37C project_reference_bodies function."""
from __future__ import annotations
import ast
import difflib
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
TARGET = PACKAGE.parent / "phase168_r3_37c_reference_projection.py"
FULL = PACKAGE / "project_reference_bodies_FULL.py"


def main():
    raw = TARGET.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    source = raw.decode("utf-8").replace("\r\n", "\n")
    tree = ast.parse(source)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef)
                 and node.name == "project_reference_bodies"]
    if len(functions) != 1:
        raise RuntimeError("Expected one existing project_reference_bodies function")
    node = functions[0]
    lines = source.splitlines(keepends=True)
    before = "".join(lines[node.lineno-1:node.end_lineno])
    required = (
        "statement = registry.assertion(assertion_id).content",
        "typed_sentence(statement, None)",
        "_group_proof_statement_latex(statement)",
    )
    if any(item not in before for item in required):
        raise RuntimeError("Unexpected local R3-37C function; no files modified")
    if "TodaProp42GeneralExactnessStatement" in before:
        raise RuntimeError("General statement projection already installed; no files modified")
    replacement = FULL.read_text(encoding="utf-8")
    updated = source.replace(before, replacement, 1)
    ast.parse(updated)
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    (output / "project_reference_bodies_BEFORE.py").write_text(before, encoding="utf-8")
    (output / "project_reference_bodies_FULL.py").write_text(replacement, encoding="utf-8")
    (output / "reference_projection.diff").write_text(
        "".join(difflib.unified_diff(source.splitlines(True), updated.splitlines(True),
                                    fromfile="before", tofile="after")), encoding="utf-8")
    TARGET.write_bytes(updated.replace("\n", newline).encode("utf-8"))
    print("PATCHED:", TARGET)
    print("FULL_FUNCTION:", output / "project_reference_bodies_FULL.py")


if __name__ == "__main__":
    main()
