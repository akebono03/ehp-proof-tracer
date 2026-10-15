"""Fail-closed Phase 165 R57-R20 installer for two existing functions."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def _replace(source: str, name: str, old: str, new: str) -> tuple[str, bool]:
    matches = [node for node in ast.parse(source).body
               if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError("missing or duplicated function: " + name)
    node = matches[0]
    lines = source.splitlines(keepends=True)
    actual = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    if actual == new.strip():
        return source, False
    if actual != old.strip():
        raise RuntimeError("Unexpected existing function: " + name + "; project unchanged")
    output = "".join(lines[:node.lineno - 1]) + new.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(output)
    return output, True


def install(root: Path, package: Path) -> str:
    shared = root / "phase165_r52_r9_shared_math.py"
    helper = root / "phase165_r57_r20_general_specialization.py"
    if not shared.is_file() or not (root / "phase165_r57_r19_delta_image_backward.py").is_file():
        raise RuntimeError("R57-R19 must already be installed")
    gate = root / "phase165_r57_r11_proof_order_gate.py"
    if not gate.is_file():
        raise RuntimeError("R57-R18 updated proof-order gate is required")
    original = shared.read_text(encoding="utf8")
    gate_original = gate.read_text(encoding="utf8")
    gate_updated, gate_changed = _replace(
        gate_original, "is_unordered_root_structure_specialization",
        (package / "previous_is_unordered_root_structure_specialization.py.txt").read_text(encoding="utf8"),
        (package / "is_unordered_root_structure_specialization.py.txt").read_text(encoding="utf8"),
    )
    steps = (
        ("build_shared_typed_bridge", "previous_build_shared_typed_bridge.py.txt", "build_shared_typed_bridge.py.txt"),
        ("shared_expansion_provider", "previous_shared_expansion_provider.py.txt", "shared_expansion_provider.py.txt"),
    )
    result = original
    for name, old, new in steps:
        result, _ = _replace(result, name,
                             (package / old).read_text(encoding="utf8"),
                             (package / new).read_text(encoding="utf8"))
    module = (package / helper.name).read_text(encoding="utf8")
    ast.parse(module)
    if helper.exists() and helper.read_text(encoding="utf8") != module:
        raise RuntimeError("Conflicting R57-R20 module; project unchanged")
    if result != original:
        backup = shared.with_name(shared.name + ".r57_r20_before.bak")
        if not backup.exists():
            shutil.copy2(shared, backup)
        shared.write_text(result, encoding="utf8")
    if gate_changed:
        backup = gate.with_name(gate.name + ".r57_r20_before.bak")
        if not backup.exists():
            shutil.copy2(gate, backup)
        gate.write_text(gate_updated, encoding="utf8")
    if not helper.exists():
        helper.write_text(module, encoding="utf8")
    return "INSTALLED" if result != original or gate_changed else "ALREADY_INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R20:", install(package.parent, package))
    print("Cited (5.1) symbolic source + generic scalar substitution; no uncited proof facts added")
    print("Full pytest NOT run")
