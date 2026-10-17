"""Guarded installer. Patch only the known shared provider wiring."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
MARK = "from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import build_unified_backward_rule_registry"


def transform(source: str) -> str:
    ast.parse(source)
    if MARK in source:
        return source
    if "from phase165_r52_r23_existing_rule_adapter import" in source:
        raise ValueError("pi43 adapter still connected: remove it first")
    import_anchor = "from phase165_r3_recursive_search import GoalExpansion"
    if source.count(import_anchor) != 1:
        raise ValueError("expected one GoalExpansion import")
    source = source.replace(import_anchor, import_anchor + "\n" + MARK, 1)
    old = "    generic_provider = build_generic_backward_expansion_provider()"
    if source.count(old) != 1:
        raise ValueError("expected one generic provider assignment")
    source = source.replace(old, "    unified_registry, _unified_report = build_unified_backward_rule_registry()\n    unified_rules = unified_registry.rules()\n    generic_provider = build_generic_backward_expansion_provider(unified_rules)", 1)
    old = "    seeded_rules, _seeded_report = _discover_seeded_rules()"
    if source.count(old) != 1:
        raise ValueError("expected one seeded discovery assignment")
    source = source.replace(old, "    seeded_rules = unified_rules", 1)
    old = "    witness_rules, _witness_report = discover_inference_rules()"
    if source.count(old) != 1:
        raise ValueError("expected one witness discovery assignment")
    source = source.replace(old, "    witness_rules = unified_rules", 1)
    # Remove unused local discovery imports; keep all existing behavior otherwise.
    for line in ("    from phase165_r8_rule_provider import discover_inference_rules as _discover_seeded_rules\n",
                 "    from phase165_r8_rule_provider import discover_inference_rules\n"):
        if source.count(line) != 1:
            raise ValueError("expected local discover import: " + repr(line))
        source = source.replace(line, "", 1)
    ast.parse(source)
    return source


def main() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    source = TARGET.read_text(encoding="utf-8")
    changed = transform(source)
    if changed == source:
        print("Unified registry wiring already installed")
        return
    backup = TARGET.with_name(TARGET.name + ".unified_registry_r1_before.bak")
    if backup.exists():
        raise FileExistsError("backup already exists; refusing overwrite")
    shutil.copy2(TARGET, backup)
    TARGET.write_text(changed, encoding="utf-8")
    print("Unified registry wired; backup:", backup)


if __name__ == "__main__":
    main()
