"""Guarded installer for R12-R34, limited to Narrative and provenance label."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def replace_function(source, name, replacement):
    nodes = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError("cannot locate unique renderer function")
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno-1]) + replacement.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated


def install(project, package):
    renderer = project / "toda_group_proof_narrative_renderer.py"
    web = project / "phase165_r52_r3_web_adapter.py"
    target_helper = project / "phase165_r12_r34_narrative.py"
    replacement = (package / "render_function.py.txt").read_text(encoding="utf8")
    original = renderer.read_text(encoding="utf8")
    if "def render_toda_partial_proof_narrative_markdown" not in original:
        raise RuntimeError("unexpected renderer")
    if "from phase165_r12_r34_narrative import" not in original:
        updated = replace_function(original, "render_toda_partial_proof_narrative_markdown", replacement)
    else:
        updated = original
    original_web = web.read_text(encoding="utf8")
    old_key = 'key="generic-partial-proof",'
    new_key = 'key=("generic-complete-proof" if result.status is ProofSearchStatus.COMPLETE else "generic-partial-proof"),'
    if old_key in original_web:
        updated_web = original_web.replace(old_key,new_key)
    elif new_key in original_web:
        updated_web = original_web
    else:
        raise RuntimeError("unexpected Web provenance implementation")
    ast.parse(updated_web)
    for path, current, newer in ((renderer,original,updated),(web,original_web,updated_web)):
        if current != newer:
            shutil.copy2(path,path.with_name(path.name+".r12_r34_backup"))
            path.write_text(newer,encoding="utf8")
    source_helper = (package / "phase165_r12_r34_narrative.py").read_text(encoding="utf8")
    ast.parse(source_helper)
    target_helper.write_text(source_helper,encoding="utf8")
    print("R12-R34 public narrative: CONNECTED")


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    install(package.parent,package)
