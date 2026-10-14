"""Phase 165 R52-R27-R2: correct Phase 50 result shape (minimal patch)."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil

TARGET = "toda_upstream_bootstrap.py"
FUNCTION = "build_toda_52_composition_isomorphism_step"
OLD = 'for step in phase50["premise_steps"]'
NEW = 'for step in phase50["result"].steps'


def function_node(source: str) -> ast.FunctionDef:
    matches = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == FUNCTION
    ]
    if len(matches) != 1:
        raise RuntimeError("Expected one target function")
    return matches[0]


def install(root: Path) -> dict:
    target = root.resolve() / TARGET
    original = target.read_text(encoding="utf-8")
    node = function_node(original)
    lines = original.splitlines(keepends=True)
    function_source = "".join(lines[node.lineno - 1:node.end_lineno])
    if function_source.count(NEW) == 1 and OLD not in function_source:
        state = "ALREADY_INSTALLED"
        updated = original
    else:
        if function_source.count(OLD) != 1 or NEW in function_source:
            raise RuntimeError("Unexpected Phase 50 consumer shape: no changes made")
        updated_function = function_source.replace(OLD, NEW, 1)
        updated = (
            "".join(lines[:node.lineno - 1]) +
            updated_function +
            "".join(lines[node.end_lineno:])
        )
        ast.parse(updated)
        if "toda_pi3_2_define_eta2_inference_rule" in updated or "toda_pi3_2_eta2_hopf_relation_inference_rule" in updated:
            raise RuntimeError("Obsolete pi3^2 inference factory reference remains")
        backup = target.with_name(target.name + ".phase165_r52_r27_r2_backup")
        if backup.exists():
            raise RuntimeError("Backup exists, refusing overwrite: " + str(backup))
        shutil.copy2(target, backup)
        target.write_text(updated, encoding="utf-8", newline="")
        state = "INSTALLED"
    new_node = function_node(updated)
    new_lines = updated.splitlines(keepends=True)
    full_function = "".join(new_lines[new_node.lineno - 1:new_node.end_lineno])
    output = Path(__file__).resolve().parent / "audit_output"
    output.mkdir(exist_ok=True)
    (output / "MODIFIED_FUNCTION.md").write_text(
        "# 変更後の関数全文\n\n```python\n" + full_function + "\n```\n",
        encoding="utf-8",
    )
    result = {
        "phase": "165 R52-R27-R2",
        "status": state,
        "changed_file": TARGET,
        "changed_function": FUNCTION,
        "old_rule_restored": False,
        "new_given_created": False,
        "full_pytest_run": False,
    }
    (output / "result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return result


if __name__ == "__main__":
    print(json.dumps(install(Path(__file__).resolve().parent.parent), indent=2, ensure_ascii=False))
