"""Safely install the R3-Q single-source Hopf equation conversion."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
POSITION = ROOT / "phase166_r3p_position_binding.py"
SHARED = ROOT / "phase165_r52_r9_shared_math.py"

POSITION_ANCHOR = "    result = UnifiedStatementRegistry()"
POSITION_INSERT = '''    # One cited Hopf-image source; use the established Proposition 5.1 position.
    from phase165_r14_r33_final_group import hopf_eta2_image_step
    image_id = "shared:1:adopted:assertion:5"
    image = bridge.registry.assertion(image_id)
    hopf_id = "shared:2:toda:adopted:prop5.1:eta2_hopf_relation"
    hopf = bridge.registry.assertion(hopf_id)
    if bridge.registry.reference(image.reference_id).locator != "Proposition 5.1":
        raise ValueError("unexpected Hopf image literature locator")
    if image.content != hopf_eta2_image_step().conclusion:
        raise ValueError("Hopf image content mismatch")
    if hopf.component_position not in (100,):
        raise ValueError("Hopf source position mismatch")
    if image.component_position not in (None, 100):
        raise ValueError("conflicting Hopf image position")
    assertion_updates[image_id] = 100
'''

SHARED_ANCHOR = '    ordered, _order_report = connect_all_reference_orders(joined)'
SHARED_INSERT = '''    # Preserve registered mathematical statements/IDs, but keep one direct
    # GIVEN for the Hopf-image fact; relation views are derived by a rule.
    hopf_relation_ids = {
        "shared:2:toda:adopted:prop5.1:eta2_hopf_relation",
        "shared:2:toda:adopted:prop5.1:finite_dimensional:component:eta2_hopf_relation",
    }
    joined = RegistryBridgeResult(
        joined.registry,
        joined.records,
        tuple(link for link in joined.proof_links
              if link.assertion_id not in hopf_relation_ids),
    )
'''
EXPAND_ANCHOR = '        options.extend(expand_finite_cyclic_relation(goal))'
EXPAND_INSERT = '''        from phase166_r3q_hopf_image_relation import expand_hopf_image_relation
        options.extend(expand_hopf_image_relation(goal, tuple(available)))
'''


def replace_function(source: str, name: str, replacements: tuple[tuple[str, str], ...]) -> tuple[str, str]:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise ValueError("unexpected function count: " + name)
    node = matches[0]
    lines = source.splitlines(keepends=True)
    block = "".join(lines[node.lineno - 1:node.end_lineno])
    for anchor, insertion in replacements:
        if block.count(anchor) != 1:
            raise ValueError("unexpected anchor in " + name + ": " + anchor)
        block = block.replace(anchor, insertion + anchor)
    output = "".join(lines[:node.lineno - 1]) + block + "".join(lines[node.end_lineno:])
    ast.parse(output)
    return output, block


def main() -> None:
    original_position = POSITION.read_text(encoding="utf-8")
    original_shared = SHARED.read_text(encoding="utf-8")
    if "assertion_updates[image_id] = 100" in original_position:
        raise ValueError("patch already applied; refusing duplicate installation")
    if "expand_hopf_image_relation(goal, tuple(available))" in original_shared:
        raise ValueError("shared search already patched")
    position, position_function = replace_function(original_position, "place_r3p_reference_positions", ((POSITION_ANCHOR, POSITION_INSERT),))
    shared, shared_function = replace_function(original_shared, "build_shared_typed_bridge", ((SHARED_ANCHOR, SHARED_INSERT),))
    shared, expansion_function = replace_function(shared, "shared_expansion_provider", ((EXPAND_ANCHOR, EXPAND_INSERT),))
    backup = ROOT / "phase166_r3q_generatorimage_canonical_backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup.mkdir(parents=True)
    shutil.copy2(POSITION, backup / POSITION.name)
    shutil.copy2(SHARED, backup / SHARED.name)
    (backup / "place_r3p_reference_positions.py.txt").write_text(position_function, encoding="utf-8")
    (backup / "build_shared_typed_bridge.py.txt").write_text(shared_function, encoding="utf-8")
    (backup / "shared_expansion_provider.py.txt").write_text(expansion_function, encoding="utf-8")
    POSITION.write_text(position, encoding="utf-8")
    SHARED.write_text(shared, encoding="utf-8")
    print("PATCHED:", POSITION)
    print("PATCHED:", SHARED)
    print("BACKUP:", backup)
    print("FULL FUNCTIONS SAVED: 3")


if __name__ == "__main__":
    main()
