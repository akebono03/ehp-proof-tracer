"""Guarded additive installer for the R3-3 shared provider loop."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
IMPORT_LINE = "from phase165_r6_2_unified_registry_r3_r3.provider_registry import build_shared_expansion_provider_registry"


def transform(source: str) -> str:
    ast.parse(source)
    if IMPORT_LINE in source:
        if "shared_provider_registry.providers()" not in source:
            raise ValueError("R3-3 import exists without provider wiring")
        return source
    if "expand_existing_pi43_rules" in source:
        raise ValueError("pi4^3 dedicated adapter still referenced: refusing installation")
    if "unified_rules = unified_registry.rules()" not in source:
        raise ValueError("R1 unified rule registry is required")
    anchor = "from phase165_r3_recursive_search import GoalExpansion"
    if source.count(anchor) != 1:
        raise ValueError("unexpected import location")
    source = source.replace(anchor, anchor + "\n" + IMPORT_LINE, 1)
    old = """        for provider in (
            expand_generic_iso_goal,
            expand_generic_ehp_hopf_goal,
            expand_delta_zero_from_suspension_iso,
            expand_diagonal_suspension,
            *extra_providers,
        ):"""
    new = """        for provider in shared_provider_registry.providers():"""
    if source.count(old) != 1:
        raise ValueError("expected exactly one provider loop; no changes made")
    source = source.replace(old, new, 1)
    anchor = "    def expand(goal: object) -> tuple[GoalExpansion, ...]:"
    if source.count(anchor) != 1:
        raise ValueError("expected one expansion closure")
    setup = """    shared_provider_registry = build_shared_expansion_provider_registry(
        expand_generic_iso_goal=expand_generic_iso_goal,
        expand_generic_ehp_hopf_goal=expand_generic_ehp_hopf_goal,
        expand_delta_zero_from_suspension_iso=expand_delta_zero_from_suspension_iso,
        expand_diagonal_suspension=expand_diagonal_suspension,
        extra_providers=extra_providers,
    )

"""
    source = source.replace(anchor, setup + anchor, 1)
    ast.parse(source)
    return source


def main() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    before = TARGET.read_text(encoding="utf-8")
    after = transform(before)
    if before == after:
        print("R3-3 already installed")
        return
    backup = TARGET.with_name(TARGET.name + ".unified_registry_r3_r3_before.bak")
    if backup.exists():
        raise FileExistsError("backup exists; no changes made")
    shutil.copy2(TARGET, backup)
    TARGET.write_text(after, encoding="utf-8")
    print("R3-3 provider connection installed; backup:", backup)


if __name__ == "__main__":
    main()
