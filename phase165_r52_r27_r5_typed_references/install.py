"""Install the R27-R5 optional production-bridge integration and module."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
MODULE = "phase165_r52_r27_r5_literature.py"
INSERT_FROM = "        sources = (production, build_adopted_typed_reference_registry(adopted_tex))"
INSERT_TO = """        from phase165_r52_r27_r5_literature import build_typed_literature_bridge
        literature = build_typed_literature_bridge(production)
        sources = (production, build_adopted_typed_reference_registry(adopted_tex), literature)"""


def install() -> dict:
    package = Path(__file__).resolve().parent
    module_path = ROOT / MODULE
    source = (package / MODULE).read_text(encoding="utf-8")
    ast.parse(source)
    destination = TARGET.read_text(encoding="utf-8")
    if INSERT_TO in destination and INSERT_FROM not in destination:
        state = "ALREADY_INSTALLED"
    else:
        if destination.count(INSERT_FROM) != 1:
            raise RuntimeError("Shared bridge source shape mismatch; no files changed")
        destination = destination.replace(INSERT_FROM, INSERT_TO, 1)
        ast.parse(destination)
        state = "INSTALLED"
    if module_path.exists() and module_path.read_text(encoding="utf-8") != source:
        raise RuntimeError("Existing literature module differs; no files changed")
    if state == "INSTALLED":
        backup = TARGET.with_name(TARGET.name + ".phase165_r52_r27_r5_backup")
        if backup.exists():
            raise RuntimeError("Existing backup detected; no files changed")
        shutil.copy2(TARGET, backup)
        if not module_path.exists():
            module_path.write_text(source, encoding="utf-8")
        TARGET.write_text(destination, encoding="utf-8", newline="")
    ast_tree = ast.parse(destination)
    nodes = [node for node in ast_tree.body if isinstance(node, ast.FunctionDef)
             and node.name == "build_shared_typed_bridge"]
    if len(nodes) != 1:
        raise RuntimeError("Shared bridge function not unique")
    node = nodes[0]
    lines = destination.splitlines(keepends=True)
    full_function = "".join(lines[node.lineno - 1:node.end_lineno])
    output = package / "audit_output"
    output.mkdir(exist_ok=True)
    (output / "MODIFIED_FUNCTION.md").write_text(
        "# 変更後の関数全文\n\n```python\n" + full_function + "\n```\n",
        encoding="utf-8",
    )
    result = {
        "phase": "165 R52-R27-R5", "status": state,
        "new_module": MODULE, "modified_file": TARGET.name,
        "specialization_verified": False, "new_specialized_inference_rules": 0,
        "full_pytest_run": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    install()
