"""Guarded migration of a superseded R10E2 byte-for-byte test assertion."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "phase169_r10e2_unpositioned_citation" / "tests" / "test_r10e2_unpositioned_citation.py"
OUTPUT = HERE / "output"
OLD = "    assert updated == (root / target).read_bytes()"
NEW = """    # Later phases may append new transport policy to the same function.
    # Verify the R10E2 source-first guard survives without requiring the
    # entire production file to equal the old R10E2 snapshot.
    current = (root / target).read_bytes()
    assert b\"uniquely_screened_prior_sources\" in updated
    assert b\"uniquely_screened_prior_sources\" in current
    assert b\"exact_prior_database_result\" in current""".replace('\\"', '"')


def _full_function(text: str, name: str) -> str:
    rows = text.splitlines(keepends=True)
    tree = ast.parse(text)
    fns = [node for node in tree.body
           if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(fns) != 1:
        raise RuntimeError("R10E4R1 expected one historical test function")
    node = fns[0]
    return "".join(rows[node.lineno - 1:node.end_lineno])


def transform(raw: bytes) -> bytes:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R10E4R1 refuses BOM rewrite")
    crlf = b"\r\n" in raw
    original = raw.decode("utf-8").replace("\r\n", "\n")
    if original.count(OLD) != 1 or NEW in original:
        raise RuntimeError("R10E4R1 migration anchor missing or already applied")
    if "def test_r10e2_guarded_patch_refuses_double_application():" not in original:
        raise RuntimeError("R10E4R1 expected historical test missing")
    updated = original.replace(OLD, NEW, 1)
    _full_function(updated, "test_r10e2_guarded_patch_refuses_double_application")
    ast.parse(updated)
    output = updated.encode("utf-8")
    return output.replace(b"\n", b"\r\n") if crlf else output


def main() -> None:
    original = TARGET.read_bytes()
    updated = transform(original)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "test_r10e2_unpositioned_citation.py.before").write_bytes(original)
    (OUTPUT / "test_r10e2_unpositioned_citation.py.FULL").write_bytes(updated)
    full_fn = _full_function(updated.decode("utf-8").replace("\r\n", "\n"),
                             "test_r10e2_guarded_patch_refuses_double_application")
    path = OUTPUT / "test_r10e2_guarded_patch_refuses_double_application_FULL.py"
    path.write_text(full_fn, encoding="utf-8")
    TARGET.write_bytes(updated)
    print("R10E4R1_TEST_PATCHED=" + str(TARGET))
    print("R10E4R1_FULL_TEST_FUNCTION=" + str(path))
    print("R10E4R1_FULL_TEST_FILE=" + str(OUTPUT / "test_r10e2_unpositioned_citation.py.FULL"))


if __name__ == "__main__":
    main()
