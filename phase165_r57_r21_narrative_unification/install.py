"""Install R57-R21 without modifying search mathematics or old renderer sources."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def _function(source: str, name: str) -> tuple[ast.FunctionDef, str]:
    tree = ast.parse(source)
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(found) != 1:
        raise RuntimeError("expected one function: " + name)
    node = found[0]
    return node, "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def install(project: Path, package: Path) -> str:
    renderer_path = project / "toda_group_proof_generic_narrative_renderer.py"
    adapter_path = project / "phase165_r56_presentation_adapter.py"
    if not all(p.is_file() for p in (renderer_path, adapter_path)):
        raise FileNotFoundError("required existing Narrative modules are missing")
    renderer_before = renderer_path.read_text(encoding="utf8")
    adapter_before = adapter_path.read_text(encoding="utf8")
    renderer_new = (package / "render_toda_partial_proof_narrative_markdown.py.txt").read_text(encoding="utf8")
    adapter_new = (package / "phase165_r56_presentation_adapter.py").read_text(encoding="utf8")
    _, old_function = _function(renderer_before, "render_toda_partial_proof_narrative_markdown")
    _, new_function = _function(renderer_new, "render_toda_partial_proof_narrative_markdown")
    if old_function != new_function:
        if ("target = statement_math(result.open_goals[0])" not in old_function
                or "_render_generic_narrative_step" not in old_function):
            raise RuntimeError("unexpected partial renderer version; no modification")
    _, old_adapter = _function(adapter_before, "render_completed_shared_narrative")
    if adapter_before != adapter_new and (
        "build_complete_toda_group_result_proof_replay" not in old_adapter
        or "render_toda_group_proof_narrative_markdown" not in old_adapter
    ):
        raise RuntimeError("unexpected completed renderer version; no modification")
    node, _ = _function(renderer_before, "render_toda_partial_proof_narrative_markdown")
    lines = renderer_before.splitlines(keepends=True)
    updated_renderer = "".join(lines[:node.lineno - 1]) + new_function.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated_renderer)
    ast.parse(adapter_new)
    if updated_renderer == renderer_before and adapter_new == adapter_before:
        return "ALREADY_INSTALLED"
    for target, content in ((renderer_path, updated_renderer), (adapter_path, adapter_new)):
        if target.read_text(encoding="utf8") != content:
            backup = target.with_name(target.name + ".phase165_r57_r21_backup")
            if not backup.exists():
                shutil.copy2(target, backup)
            target.write_text(content, encoding="utf8")
    return "INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R21:", install(package.parent, package))
    print("One common completed/partial Narrative path; full pytest NOT run")
