"""Install exactly one rule after validating previous stage dependencies."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "map_property_rules.py"
SOURCE = PACKAGE / "new_rule.py"
FUNCTION = "injective_and_surjective_imply_isomorphism_inference_rule"


def install(target: Path = TARGET, source: Path = SOURCE) -> str:
    original = target.read_text(encoding="utf-8")
    existing = ast.parse(original)
    names = {node.name for node in existing.body if isinstance(node, (ast.ClassDef, ast.FunctionDef))}
    prerequisites = {"InjectiveMapStatement", "SurjectiveMapStatement", "IsomorphismStatement"}
    missing = sorted(prerequisites - names)
    if missing:
        raise RuntimeError("R4-4 stage2/earlier prerequisite classes missing: " + ", ".join(missing))
    if FUNCTION in names:
        return "ALREADY_INSTALLED"
    addition = source.read_text(encoding="utf-8")
    # Add only the full factory function, not the auxiliary module docstring.
    parsed = ast.parse(addition)
    definition = next(n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name == FUNCTION)
    lines = addition.splitlines(keepends=True)
    full_function = "".join(lines[definition.lineno - 1:definition.end_lineno])
    modified = original.rstrip() + "\n\n\n" + full_function.rstrip() + "\n"
    ast.parse(modified)
    backup = target.with_name(target.name + ".phase165_r4_r4_stage5_before.bak")
    if not backup.exists():
        backup.write_text(original, encoding="utf-8")
    target.write_text(modified, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    print(install())
