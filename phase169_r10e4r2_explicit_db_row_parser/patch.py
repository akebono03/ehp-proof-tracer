"""Guarded replacement of one full function; no other production edits."""
from __future__ import annotations

import ast
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "output"
TARGET = ROOT / "phase169_r10e4_ordered_db_prior" / "db_prior.py"
FUNCTION_NAME = "_has_explicit_row"


def _bounds(source: str, name: str) -> tuple[int, int]:
    tree = ast.parse(source)
    functions = tuple(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)
    if len(functions) != 1:
        raise RuntimeError("R10E4R2 cannot find one complete function " + name)
    node = functions[0]
    rows = source.splitlines(keepends=True)
    return sum(map(len, rows[:node.lineno - 1])), sum(map(len, rows[:node.end_lineno]))


def transform(raw: bytes) -> tuple[bytes, str]:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R10E4R2 refuses unexpected BOM")
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8").replace("\r\n", "\n")
    start, end = _bounds(text, FUNCTION_NAME)
    old = text[start:end]
    if "return any(int(row[\"n\"]) == n and int(row[\"k\"]) == k for row in rows)" not in old:
        raise RuntimeError("R10E4R2 source anchor changed; patch refused")
    changed = (HERE / "_has_explicit_row_FULL.py").read_text(encoding="utf-8")
    if changed == old:
        raise RuntimeError("R10E4R2 was already applied")
    new = text[:start] + changed + text[end:]
    ast.parse(new)
    raw_changed = new.encode("utf-8")
    if crlf:
        raw_changed = raw_changed.replace(b"\n", b"\r\n")
    return raw_changed, changed


def main() -> None:
    if not TARGET.is_file():
        raise RuntimeError("R10E4R2 source file missing")
    old = TARGET.read_bytes()
    new, full = transform(old)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "db_prior.py.before").write_bytes(old)
    (OUTPUT / "db_prior.py.FULL").write_bytes(new)
    (OUTPUT / "_has_explicit_row_FULL.py").write_text(full, encoding="utf-8")
    TARGET.write_bytes(new)
    print("R10E4R2_PATCHED=" + str(TARGET))
    print("R10E4R2_FULL_FUNCTION=" + str(OUTPUT / "_has_explicit_row_FULL.py"))
    print("R10E4R2_FULL_FILE=" + str(OUTPUT / "db_prior.py.FULL"))


if __name__ == "__main__":
    main()
