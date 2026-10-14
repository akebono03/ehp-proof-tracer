"""Install R27-R5 using scoped AST replacement, preserving earlier changes."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
MODULE = "phase165_r52_r27_r5_literature.py"
IMPORT = "from phase165_r52_r27_r5_literature import build_typed_literature_bridge"


def _target_function(text: str) -> ast.FunctionDef:
    matches = [node for node in ast.parse(text).body
               if isinstance(node, ast.FunctionDef)
               and node.name == "build_shared_typed_bridge"]
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one shared bridge function")
    return matches[0]


def _patched_source(original: str) -> tuple[str, str]:
    node = _target_function(original)
    lines = original.splitlines(keepends=True)
    body_text = "".join(lines[node.lineno-1:node.end_lineno])
    if "build_typed_literature_bridge(production)" in body_text:
        if "literature" not in body_text:
            raise RuntimeError("Incomplete existing integration")
        return original, "ALREADY_INSTALLED"
    candidates = []
    for entry in ast.walk(node):
        if isinstance(entry, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "sources" for target in entry.targets
        ):
            candidates.append(entry)
    if len(candidates) != 1:
        raise RuntimeError("Expected exactly one source tuple assignment")
    assignment = candidates[0]
    if not any(isinstance(item, ast.Name) and item.id == "production"
               for item in ast.walk(assignment.value)):
        raise RuntimeError("Source tuple must retain production registry")
    if not isinstance(assignment.value, ast.Tuple):
        raise RuntimeError("Source expression is not a tuple; refusing to guess")
    if assignment.lineno != assignment.end_lineno:
        start=assignment.lineno-1
        end=assignment.end_lineno
        original_line="".join(lines[start:end])
        indent=original_line[:len(original_line)-len(original_line.lstrip())]
    else:
        start=assignment.lineno-1
        end=assignment.end_lineno
        original_line=lines[start]
        indent=original_line[:len(original_line)-len(original_line.lstrip())]
    rhs=ast.get_source_segment(original,assignment.value)
    if not rhs:
        raise RuntimeError("Cannot extract original sources tuple")
    replacement=(indent+IMPORT+"\n"+indent+"literature = build_typed_literature_bridge(production)\n"
                 +indent+"sources = "+rhs+" + (literature,)\n")
    updated="".join(lines[:start])+replacement+"".join(lines[end:])
    ast.parse(updated)
    return updated, "INSTALLED"


def install() -> dict:
    package = Path(__file__).resolve().parent
    source = (package / MODULE).read_text(encoding="utf-8")
    ast.parse(source)
    original = TARGET.read_text(encoding="utf-8")
    patched, status = _patched_source(original)
    dest_module = ROOT / MODULE
    if dest_module.exists() and dest_module.read_text(encoding="utf-8") != source:
        raise RuntimeError("Literature module exists with different content")
    backup = TARGET.with_name(TARGET.name+".phase165_r52_r27_r5_r1_backup")
    if status == "INSTALLED" and backup.exists():
        raise RuntimeError("Backup already exists; no files changed")
    if status == "INSTALLED":
        shutil.copy2(TARGET,backup)
        if not dest_module.exists():
            dest_module.write_text(source,encoding="utf-8")
        TARGET.write_text(patched,encoding="utf-8",newline="")
    node=_target_function(patched)
    lines=patched.splitlines(keepends=True)
    full="".join(lines[node.lineno-1:node.end_lineno])
    out=package/"audit_output";out.mkdir(exist_ok=True)
    (out/"MODIFIED_FUNCTION.md").write_text("# 変更後の関数全文\n\n```python\n"+full+"\n```\n",encoding="utf-8")
    result={"phase":"165 R52-R27-R5-R1","status":status,"modified_file":TARGET.name,
            "new_module":MODULE,"specialization_verified":False,"full_pytest_run":False}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result


if __name__ == "__main__":
    install()
