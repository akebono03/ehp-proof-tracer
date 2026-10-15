"""Fail-closed installer: replace exactly one complete shared function."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def install(root: Path, package: Path) -> str:
    target = root / "phase165_r52_r9_shared_math.py"
    helper_target = root / "phase165_r57_r7_stable_expansion.py"
    src = target.read_text(encoding="utf-8")
    replacement = (package / "shared_expansion_provider.py.txt").read_text(encoding="utf-8").rstrip("\n")
    tree = ast.parse(src)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "shared_expansion_provider"]
    if len(matches) != 1:
        raise RuntimeError("expected exactly one shared_expansion_provider; no change")
    node = matches[0]
    lines = src.splitlines(keepends=True)
    old = "".join(lines[node.lineno-1:node.end_lineno])
    if "expand_registered_toda45_finite_cyclic_goal" in old:
        if old.rstrip("\n") != replacement:
            raise RuntimeError("already changed provider differs from R57-R7; no change")
        if not helper_target.exists() or helper_target.read_bytes() != (package / helper_target.name).read_bytes():
            raise RuntimeError("installed helper mismatch; no change")
        return "ALREADY_INSTALLED"
    for required in (
        "expand_existing_pi43_rules", "reverse_free_cyclic_transport_rule",
        "def expand(goal: object)", "*extra_providers",
    ):
        if required not in old:
            raise RuntimeError("unrecognized provider layout: " + required)
    ast.parse(replacement)
    new_src = "".join(lines[:node.lineno-1]) + replacement + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(new_src)
    if helper_target.exists() and helper_target.read_bytes() != (package / helper_target.name).read_bytes():
        raise RuntimeError("existing helper differs; no change")
    backup = root / "phase165_r52_r9_shared_math.r57_r7_before.py.bak"
    if not backup.exists():
        shutil.copy2(target, backup)
    if not helper_target.exists():
        shutil.copy2(package / helper_target.name, helper_target)
    target.write_text(new_src, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R7:", install(package.parent, package))
    print("Existing Toda (4.5) rule exposed to typed shared backward search")
    print("No GIVEN added; no eta normalization assumed; full pytest NOT run")
