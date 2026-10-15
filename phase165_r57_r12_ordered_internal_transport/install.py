"""Fail-closed installer preserving the current R57-R11 source baseline."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def _replace(source: str, name: str, desired: str) -> str:
    matches = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError("expected one " + name)
    node = matches[0]
    lines = source.splitlines(keepends=True)
    current = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    desired = desired.strip()
    if current == desired:
        return source
    if name == "shared_expansion_provider":
        if "retain_ordered_root_expansions" not in current or "expand_registered_toda45_finite_cyclic_goal" not in current:
            raise RuntimeError("R57-R11 provider prerequisite missing")
        if "prior_conclusions" in current:
            raise RuntimeError("unknown prior proof integration; abort")
    if name == "search_shared_group_goal":
        if "shared_expansion_provider(proof_context, proof_target=goal)" not in current:
            raise RuntimeError("R57-R11 search prerequisite missing")
        if "ordered_completed_proofs" in current:
            raise RuntimeError("unknown ordered search integration; abort")
    output = "".join(lines[:node.lineno - 1]) + desired + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(output)
    return output


def install(root: Path, package: Path) -> str:
    destination = root / "phase165_r52_r9_shared_math.py"
    helper = root / "phase165_r57_r12_ordered_proofs.py"
    helper_bytes = (package / helper.name).read_bytes()
    if helper.exists() and helper.read_bytes() != helper_bytes:
        raise RuntimeError("R57-R12 helper differs; abort")
    before = destination.read_text(encoding="utf-8")
    after = before
    for name in ("shared_expansion_provider", "search_shared_group_goal"):
        after = _replace(after, name, (package / (name + ".py.txt")).read_text(encoding="utf-8"))
    ast.parse(after)
    if after == before and helper.exists():
        return "ALREADY_INSTALLED"
    if after != before:
        backup = destination.with_suffix(".r57_r12_before.py.bak")
        if not backup.exists():
            shutil.copy2(destination, backup)
    if not helper.exists():
        shutil.copy2(package / helper.name, helper)
    if after != before:
        destination.write_text(after, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R12:", install(package.parent, package))
    print("Earlier internal proof order checked; no GIVEN constructed; full pytest NOT run")
