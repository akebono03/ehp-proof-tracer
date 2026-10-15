"""Install R57-R11 with an all-or-nothing AST-verified patch."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def _replace_function(source: str, name: str, desired: str) -> str:
    matches = [x for x in ast.parse(source).body
               if isinstance(x, ast.FunctionDef) and x.name == name]
    if len(matches) != 1:
        raise RuntimeError("expected one function: " + name)
    node = matches[0]
    lines = source.splitlines(keepends=True)
    current = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    desired = desired.strip()
    if current == desired:
        return source
    if name == "shared_expansion_provider":
        if "expand_registered_eta_specialization" not in current or "expand_registered_toda45_finite_cyclic_goal" not in current:
            raise RuntimeError("R57-R7/R8 shared provider prerequisite missing")
        if "retain_ordered_root_expansions" in current:
            raise RuntimeError("different order gate already installed")
    elif name == "search_shared_group_goal":
        if "shared_expansion_provider(proof_context)" not in current:
            raise RuntimeError("unexpected shared search function; abort")
    result = "".join(lines[:node.lineno - 1]) + desired + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(result)
    return result


def install(root: Path, package: Path) -> str:
    destination = root / "phase165_r52_r9_shared_math.py"
    helper_target = root / "phase165_r57_r11_proof_order_gate.py"
    helper_source = package / helper_target.name
    if helper_target.exists() and helper_target.read_bytes() != helper_source.read_bytes():
        raise RuntimeError("R57-R11 helper differs; abort")
    original = destination.read_text(encoding="utf-8")
    result = original
    for name, unit in (
        ("shared_expansion_provider", "shared_expansion_provider.py.txt"),
        ("search_shared_group_goal", "search_shared_group_goal.py.txt"),
    ):
        desired = (package / unit).read_text(encoding="utf-8")
        result = _replace_function(result, name, desired)
    ast.parse(result)
    if result == original and helper_target.exists():
        return "ALREADY_INSTALLED"
    if result != original:
        backup = destination.with_suffix(".r57_r11_before.py.bak")
        if not backup.exists():
            shutil.copy2(destination, backup)
    if not helper_target.exists():
        shutil.copy2(helper_source, helper_target)
    if result != original:
        destination.write_text(result, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    print("R57-R11:", install(folder.parent, folder))
    print("Strict root-source proof order gate installed; no GIVEN created")
    print("Full pytest NOT run")
