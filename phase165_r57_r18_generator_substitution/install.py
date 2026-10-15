"""R57-R18 fail-closed installer with backups. No broad refactoring."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def replace_function(source: str, name: str, desired: str) -> tuple[str, bool]:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError("missing or duplicated function: " + name)
    node = matches[0]
    lines = source.splitlines(keepends=True)
    old = "".join(lines[node.lineno - 1:node.end_lineno])
    if old.strip() == desired.strip():
        return source, False
    if name == "expand_existing_pi43_rules":
        checks = (
            "toda_pi4_3_eta3_generator_inference_rule",
            "toda_pi4_3_finite_cyclic_inference_rule",
            "toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule",
            "toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule",
        )
        if any(value not in old for value in checks):
            raise RuntimeError("unexpected reverse adapter; no files modified")
    else:
        raise RuntimeError("unsupported function")
    result = "".join(lines[:node.lineno - 1]) + desired.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(result)
    return result, True


def install(root: Path, package: Path) -> str:
    adapter = root / "phase165_r52_r23_existing_rule_adapter.py"
    gate = root / "phase165_r57_r11_proof_order_gate.py"
    helper = root / "phase165_r57_r18_generator_substitution.py"
    if not adapter.is_file() or not gate.is_file():
        raise RuntimeError("existing R52-R23 adapter and R57-R11 gate are required")
    before = adapter.read_text(encoding="utf8")
    after, changed = replace_function(
        before, "expand_existing_pi43_rules",
        (package / "expand_existing_pi43_rules.py.txt").read_text(encoding="utf8"),
    )
    gate_before = gate.read_text(encoding="utf8")
    gate_new = (package / gate.name).read_text(encoding="utf8")
    if gate_before != gate_new:
        # Gate must be the R57-R11 original; never replace unrecognized extensions.
        required = (
            'def is_unordered_root_structure_specialization(',
            'def retain_ordered_root_expansions(',
            'source_group == root_goal.lhs',
        )
        if any(token not in gate_before for token in required):
            raise RuntimeError("unexpected R57-R11 gate; no files modified")
        if 'def _proved_generator_substitution_shape(' in gate_before:
            raise RuntimeError("conflicting gate extension; no files modified")
    helper_new = (package / helper.name).read_text(encoding="utf8")
    if helper.exists() and helper.read_text(encoding="utf8") != helper_new:
        raise RuntimeError("conflicting R57-R18 inference module; no files modified")
    ast.parse(after)
    ast.parse(gate_new)
    ast.parse(helper_new)
    changes = []
    if changed:
        changes.append((adapter, after))
    if gate_before != gate_new:
        changes.append((gate, gate_new))
    if not helper.exists():
        changes.append((helper, helper_new))
    for path, value in changes:
        if path.exists():
            backup = path.with_name(path.name + '.r57_r18_before.bak')
            if not backup.exists():
                shutil.copy2(path, backup)
        path.write_text(value, encoding="utf8")
    return "INSTALLED" if changes else "ALREADY_INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R18:", install(package.parent, package))
    print("Generic proved generator substitution; no GIVEN synthesized")
    print("Full pytest NOT run")
