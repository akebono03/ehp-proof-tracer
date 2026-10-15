"""R57-R21-R1: replace the EFFECTIVE (last) shared renderer definition.

This is a narrow regression fix; do not modify mathematics, renderer interfaces,
or the presentation adapter. Confirm the loaded module is the project file.
"""
from __future__ import annotations

import ast
import inspect
from pathlib import Path
import shutil
import sys


FUNCTION_NAME = "render_toda_partial_proof_narrative_markdown"


def function_nodes(source: str) -> tuple[ast.FunctionDef, ...]:
    tree = ast.parse(source)
    return tuple(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == FUNCTION_NAME
    )


def effective_function_source(source: str) -> str:
    nodes = function_nodes(source)
    if not nodes:
        raise RuntimeError("shared narrative renderer function not found")
    lines = source.splitlines(keepends=True)
    node = nodes[-1]
    return "".join(lines[node.lineno - 1:node.end_lineno])


def install(project: Path, package: Path) -> str:
    target = project / "toda_group_proof_generic_narrative_renderer.py"
    if not target.is_file():
        raise FileNotFoundError(str(target))
    original = target.read_text(encoding="utf8")
    replacement = (package / "render_toda_partial_proof_narrative_markdown.py.txt").read_text(encoding="utf8")
    if len(function_nodes(replacement)) != 1:
        raise RuntimeError("replacement must define the renderer exactly once")
    nodes = function_nodes(original)
    if not nodes:
        raise RuntimeError("no existing shared renderer function")
    effective = effective_function_source(original)
    new_code = effective_function_source(replacement)
    if effective.rstrip() == new_code.rstrip():
        return "ALREADY_INSTALLED"
    # Only touch the known old renderer, not an unfamiliar local rewrite.
    old_markers = (
        "target = statement_math(result.open_goals[0])",
        "## 証明（Proof（導出済み））",
        "ProofStep",
    )
    if not any(marker in effective for marker in old_markers):
        raise RuntimeError("unrecognized effective renderer: refusing to overwrite")
    node = nodes[-1]
    lines = original.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno - 1]) + new_code.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    backup = target.with_name(target.name + ".phase165_r57_r21_r1_backup")
    if not backup.exists():
        shutil.copy2(target,backup)
    target.write_text(updated, encoding="utf8")
    if effective_function_source(target.read_text(encoding="utf8")).rstrip() != new_code.rstrip():
        raise RuntimeError("effective renderer verification failed")
    return "INSTALLED"


def verify_loaded(project: Path) -> None:
    import importlib
    import toda_group_proof_generic_narrative_renderer as module
    expected = (project / "toda_group_proof_generic_narrative_renderer.py").resolve()
    actual = Path(module.__file__).resolve()
    print("Loaded renderer:", actual)
    if actual != expected:
        raise RuntimeError("imported a different shared renderer module")
    func = getattr(module, FUNCTION_NAME)
    source = inspect.getsource(func)
    if ("## 使用する結果" not in source or "## 証明" not in source
            or "candidate_goals" not in source):
        raise RuntimeError("effective renderer is not the R57-R21 unified implementation")
    print("Verified effective shared Renderer implementation")


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    project = package.parent
    sys.path.insert(0, str(project))
    print("R57-R21-R1:", install(project, package))
    verify_loaded(project)
    print("R57-R21-R1 renderer only; full pytest NOT run")
