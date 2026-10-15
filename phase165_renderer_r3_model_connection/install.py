"""Guarded R3 connector installation; no search or established prose modification."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def function_nodes(source: str, name: str) -> tuple[ast.FunctionDef, ...]:
    return tuple(
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )


def function_text(source: str, node: ast.FunctionDef) -> str:
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def replace_function(source: str, node: ast.FunctionDef, new: str) -> str:
    lines = source.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno - 1]) + new.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated


def install(project: Path, package: Path) -> str:
    primary = project / "toda_group_proof_narrative_renderer.py"
    partial = project / "phase165_r52_partial_proof.py"
    model = project / "phase165_renderer_narrative_model.py"
    if not all(path.is_file() for path in (primary, partial, model)):
        raise FileNotFoundError("R2 model or established Narrative sources missing")
    old_primary = primary.read_text(encoding="utf8")
    old_partial = partial.read_text(encoding="utf8")
    dispatcher = (package / "render_narrative_proof_model.py.txt").read_text(encoding="utf8")
    public = (package / "render_partial_proof_markdown.py.txt").read_text(encoding="utf8")
    assert len(function_nodes(dispatcher, "render_narrative_proof_model")) == 1
    assert len(function_nodes(public, "render_partial_proof_markdown")) == 1
    nodes = function_nodes(old_partial, "render_partial_proof_markdown")
    if len(nodes) != 1:
        raise RuntimeError("unexpected public renderer wrapper definitions")
    old_wrapper = function_text(old_partial, nodes[0])
    if old_wrapper.rstrip() != public.rstrip() and not all(
        token in old_wrapper for token in (
            "render_completed_shared_narrative",
            "render_toda_partial_proof_narrative_markdown",
        )
    ):
        raise RuntimeError("unrecognized public wrapper; refusing overwrite")
    if len(function_nodes(old_primary, "render_toda_group_proof_narrative_markdown")) < 1:
        raise RuntimeError("established complete renderer missing")
    if len(function_nodes(old_primary, "render_toda_partial_proof_narrative_markdown")) != 1:
        raise RuntimeError("established partial renderer missing")
    current = function_nodes(old_primary, "render_narrative_proof_model")
    if len(current) > 1:
        raise RuntimeError("duplicate dispatcher definitions")
    if current and function_text(old_primary, current[0]).rstrip() != dispatcher.rstrip():
        raise RuntimeError("conflicting existing dispatcher")
    new_primary = old_primary if current else old_primary.rstrip() + "\n\n\n" + dispatcher.rstrip() + "\n"
    new_partial = replace_function(old_partial, nodes[0], public)
    if new_primary == old_primary and new_partial == old_partial:
        return "ALREADY_INSTALLED"
    ast.parse(new_primary)
    ast.parse(new_partial)
    backup = project / ".phase165_renderer_r3_backup"
    if backup.exists():
        raise RuntimeError("R3 backup already exists: refusing overwrite")
    backup.mkdir()
    try:
        shutil.copy2(primary, backup / primary.name)
        shutil.copy2(partial, backup / partial.name)
        primary.write_text(new_primary, encoding="utf8")
        partial.write_text(new_partial, encoding="utf8")
    except BaseException:
        shutil.copy2(backup / primary.name, primary)
        shutil.copy2(backup / partial.name, partial)
        raise
    return "INSTALLED"


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    print("Phase165 Renderer R3:", install(folder.parent, folder))
    print("Only public entry and canonical dispatcher changed; full pytest NOT run")
