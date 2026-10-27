"""Guarded one-function edit of the common backward expansion provider."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OLD = (
    "        options.extend(expand_cited_eta_generator(goal))\n"
    "        options.extend(expand_cited_stable_family(goal, tuple(available)))"
)
NEW = (
    "        eta_generator_options = expand_cited_eta_generator(goal)\n"
    "        options.extend(eta_generator_options)\n"
    "        options.extend(expand_cited_stable_family(goal, tuple(available)))\n"
    "        if not eta_generator_options:\n"
    "            from phase169_r10e5_composite_generator_image.rule import (\n"
    "                expand_composite_generator_image,\n"
    "            )\n"
    "            options.extend(expand_composite_generator_image(goal))"
)


def full_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    found = tuple(n for n in tree.body
                  if isinstance(n, ast.FunctionDef) and n.name == name)
    if len(found) != 1:
        raise RuntimeError("expected exactly one full function: " + name)
    node = found[0]
    return "".join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])


def transform(raw: bytes) -> tuple[bytes, str]:
    crlf = b"\r\n" in raw
    source = raw.decode("utf-8-sig").replace("\r\n", "\n")
    if source.count(OLD) != 1 or NEW in source:
        raise RuntimeError("R10E5 source anchor missing or already applied")
    updated = source.replace(OLD, NEW, 1)
    ast.parse(updated)
    full = full_function(updated, "shared_expansion_provider")
    encoded = updated.encode("utf-8")
    if crlf:
        encoded = encoded.replace(b"\n", b"\r\n")
    return encoded, full


def main() -> None:
    raw = TARGET.read_bytes()
    updated, fn = transform(raw)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "phase165_r52_r9_shared_math.py.before").write_bytes(raw)
    (OUTPUT / "phase165_r52_r9_shared_math.py.FULL").write_bytes(updated)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(fn, encoding="utf-8")
    TARGET.write_bytes(updated)
    print("R10E5_PATCHED=" + str(TARGET))
    print("R10E5_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"))
    print("R10E5_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.py.FULL"))


if __name__ == "__main__":
    main()
