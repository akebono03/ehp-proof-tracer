"""Restore R57-R21 pre-switch completed Narrative route, fail closed."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def effective(source: str, name: str) -> tuple[ast.FunctionDef, str]:
    nodes = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef) and node.name == name]
    if not nodes:
        raise RuntimeError(f"missing function: {name}")
    node = nodes[-1]
    lines = source.splitlines(keepends=True)
    return node, "".join(lines[node.lineno - 1:node.end_lineno])


def install(project: Path, package: Path) -> str:
    adapter = project / "phase165_r56_presentation_adapter.py"
    partial = project / "phase165_r52_partial_proof.py"
    old_renderer = project / "toda_group_proof_narrative_renderer.py"
    if not all(item.is_file() for item in (adapter, partial, old_renderer)):
        raise FileNotFoundError("required existing Narrative files missing")

    before_adapter = adapter.read_text(encoding="utf8")
    desired_adapter = (package / adapter.name).read_text(encoding="utf8")
    before_partial = partial.read_text(encoding="utf8")
    desired_function = (package / "render_partial_proof_markdown.py.txt").read_text(encoding="utf8")
    _, current_adapter_fn = effective(before_adapter, "render_completed_shared_narrative")
    _, desired_adapter_fn = effective(desired_adapter, "render_completed_shared_narrative")
    if current_adapter_fn != desired_adapter_fn and (
        "render_toda_partial_proof_narrative_markdown" not in current_adapter_fn
        or "render_toda_group_proof_narrative_markdown" in current_adapter_fn
    ):
        raise RuntimeError("unexpected completed adapter: refusing to overwrite")
    node, existing_entry = effective(before_partial, "render_partial_proof_markdown")
    _, desired_entry = effective(desired_function, "render_partial_proof_markdown")
    if existing_entry != desired_entry and (
        "render_toda_partial_proof_narrative_markdown" not in existing_entry
        or "render_completed_shared_narrative" in existing_entry
    ):
        raise RuntimeError("unexpected public partial entry: refusing to overwrite")
    if before_adapter == desired_adapter and existing_entry == desired_entry:
        return "ALREADY_INSTALLED"
    lines = before_partial.splitlines(keepends=True)
    new_partial = ("".join(lines[:node.lineno - 1]) + desired_entry.rstrip() + "\n"
                   + "".join(lines[node.end_lineno:]))
    ast.parse(desired_adapter)
    ast.parse(new_partial)
    updates = [(adapter, desired_adapter), (partial, new_partial)]
    for target, replacement in updates:
        if target.read_text(encoding="utf8") == replacement:
            continue
        backup = target.with_name(target.name + ".before_original_narrative_restore.bak")
        if not backup.exists():
            shutil.copy2(target, backup)
        target.write_text(replacement, encoding="utf8")
    return "INSTALLED"


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    print("R57-R21 original Narrative restore:", install(folder.parent, folder))
    print("Proof search unchanged. Full pytest NOT run.")
