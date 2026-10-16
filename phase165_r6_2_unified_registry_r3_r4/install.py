"""Install the R3-4 context registry without touching unrelated code."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

TARGET = Path.cwd() / "phase165_r52_r9_shared_math.py"
IMPORT = "from phase165_r6_2_unified_registry_r3_r4.context_provider_registry import build_context_expansion_provider_registry"
OLD = '''        options.extend(expand_registered_toda45_finite_cyclic_goal(goal, tuple(available) + prior_conclusions))
        options.extend(expand_registered_eta_specialization(goal, tuple(available)))
        options.extend(expand_registered_delta_image_goal(goal, tuple(available)))
        options.extend(expand_cited_general_specialization(goal, tuple(available)))'''
NEW = '''        for provider in context_provider_registry.providers():
            new = provider(goal)
            if not isinstance(new, tuple) or not all(isinstance(x, GoalExpansion) for x in new):
                raise TypeError("expansion provider contract violated")
            options.extend(new)'''
SETUP = '''    context_provider_registry = build_context_expansion_provider_registry(
        available=tuple(available),
        prior_conclusions=prior_conclusions,
        expand_registered_toda45_finite_cyclic_goal=expand_registered_toda45_finite_cyclic_goal,
        expand_registered_eta_specialization=expand_registered_eta_specialization,
        expand_registered_delta_image_goal=expand_registered_delta_image_goal,
        expand_cited_general_specialization=expand_cited_general_specialization,
    )

'''


def transform(source: str) -> str:
    ast.parse(source)
    if IMPORT in source:
        if NEW not in source or OLD in source:
            raise ValueError("partial R3-4 installation")
        return source
    if "expand_existing_pi43_rules" in source:
        raise ValueError("dedicated pi4^3 adapter still referenced")
    if "shared_provider_registry.providers()" not in source:
        raise ValueError("R3-3 provider registry is required")
    if "unified_rules = unified_registry.rules()" not in source:
        raise ValueError("R1 unified rules are required")
    if source.count(OLD) != 1:
        raise ValueError("expected four context provider calls exactly once")
    marker = "from phase165_r3_recursive_search import GoalExpansion"
    if source.count(marker) != 1:
        raise ValueError("shared import anchor missing")
    source = source.replace(marker, marker + "\n" + IMPORT, 1)
    anchor = "    def expand(goal: object) -> tuple[GoalExpansion, ...]:"
    if source.count(anchor) != 1:
        raise ValueError("expansion closure not unique")
    source = source.replace(anchor, SETUP + anchor, 1)
    source = source.replace(OLD, NEW, 1)
    ast.parse(source)
    return source


def main() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    before = TARGET.read_text(encoding="utf-8")
    after = transform(before)
    if before == after:
        print("R3-4 already installed")
        return
    backup = TARGET.with_name(TARGET.name + ".unified_registry_r3_r4_before.bak")
    if backup.exists():
        raise FileExistsError(backup)
    shutil.copy2(TARGET, backup)
    TARGET.write_text(after, encoding="utf-8")
    print("R3-4 context providers connected; backup:", backup)


if __name__ == "__main__":
    main()
