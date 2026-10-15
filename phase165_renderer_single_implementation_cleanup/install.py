"""Retire the duplicate generic Narrative implementation while retaining imports.

The completed Narrative renderer remains the only implementation module.
Existing helper functions move unchanged to a non-renderer component module.
The old module name becomes a lazy compatibility package, not a renderer.
"""
from __future__ import annotations

import ast
from pathlib import Path
import shutil
import sys

DUPLICATE = "toda_group_proof_generic_narrative_renderer"
PRIMARY = "toda_group_proof_narrative_renderer"
HELPERS = "toda_group_proof_narrative_shared_components"
PARTIAL_FUNCTION = "render_toda_partial_proof_narrative_markdown"
GENERIC_FUNCTION = "render_toda_group_proof_generic_narrative_markdown"


def _definitions(source: str, name: str) -> tuple[ast.FunctionDef, ...]:
    tree = ast.parse(source)
    return tuple(item for item in tree.body if isinstance(item, ast.FunctionDef) and item.name == name)


def _whole_function(source: str, name: str) -> str:
    nodes = _definitions(source, name)
    if len(nodes) != 1:
        raise RuntimeError(f"expected exactly one {name}, found {len(nodes)}")
    node = nodes[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def _without_functions(source: str, names: tuple[str, ...]) -> str:
    nodes = []
    for name in names:
        found = _definitions(source, name)
        if len(found) != 1:
            raise RuntimeError(f"expected exactly one {name}, found {len(found)}")
        nodes.append(found[0])
    lines = source.splitlines(keepends=True)
    for node in sorted(nodes, key=lambda item: item.lineno, reverse=True):
        del lines[node.lineno - 1:node.end_lineno]
    updated = "".join(lines)
    ast.parse(updated)
    return updated


def _public_delegate() -> str:
    return '''"""Compatibility imports only. This package contains no Narrative renderer."""
from __future__ import annotations
from importlib import import_module

_PUBLIC = {
    "render_toda_partial_proof_narrative_markdown": "render_toda_partial_proof_narrative_markdown",
    "render_toda_group_proof_generic_narrative_markdown": "render_toda_group_proof_narrative_markdown",
}


def __getattr__(name: str):
    if name in _PUBLIC:
        return getattr(import_module("toda_group_proof_narrative_renderer"), _PUBLIC[name])
    return getattr(import_module("toda_group_proof_narrative_shared_components"), name)


def __dir__():
    helpers = import_module("toda_group_proof_narrative_shared_components")
    return sorted(set(globals()) | set(dir(helpers)) | set(_PUBLIC))
'''


def install(project: Path) -> str:
    project = project.resolve()
    old = project / f"{DUPLICATE}.py"
    primary = project / f"{PRIMARY}.py"
    partial = project / "phase165_r52_partial_proof.py"
    helper = project / f"{HELPERS}.py"
    alias = project / DUPLICATE / "__init__.py"
    if not old.is_file():
        if alias.is_file() and helper.is_file() and primary.is_file():
            return "ALREADY_INSTALLED"
        raise FileNotFoundError("the original generic renderer is missing; no changes made")
    if any(not item.is_file() for item in (primary, partial)):
        raise FileNotFoundError("primary renderer or partial entry missing")
    if helper.exists() or alias.exists():
        raise RuntimeError("conflicting helper or compatibility alias already exists")
    generic_text = old.read_text(encoding="utf8")
    primary_text = primary.read_text(encoding="utf8")
    partial_text = partial.read_text(encoding="utf8")
    if _definitions(primary_text, PARTIAL_FUNCTION):
        raise RuntimeError("primary already defines partial rendering; refuse duplicate")
    if not _definitions(primary_text, "render_toda_group_proof_narrative_markdown"):
        raise RuntimeError("primary Narrative entry is missing")
    partial_source = _whole_function(generic_text, PARTIAL_FUNCTION)
    helpers_text = _without_functions(generic_text, (PARTIAL_FUNCTION, GENERIC_FUNCTION))
    # The old primary renderer already imports low-level helper names from the
    # retired generic module; the compatibility package keeps those imports valid.
    # The partial function uses internal helpers that the primary imports.
    for symbol in ("_render_generic_narrative_step",):
        if symbol not in primary_text:
            raise RuntimeError("missing primary renderer helper: " + symbol)
    before_import = "from toda_group_proof_generic_narrative_renderer import ("
    if before_import not in partial_text:
        raise RuntimeError("unexpected partial renderer import; no changes made")
    changed_partial = partial_text.replace(
        before_import, "from toda_group_proof_narrative_renderer import (", 1
    )
    if changed_partial == partial_text:
        raise RuntimeError("partial import was not updated")
    changed_primary = primary_text.rstrip() + "\n\n\n" + partial_source.rstrip() + "\n"
    ast.parse(changed_primary)
    ast.parse(changed_partial)
    ast.parse(_public_delegate())
    # Fail closed if a *module-level* statement in the helper source still
    # references either removed public renderer by name.
    body = ast.parse(helpers_text).body
    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if any(isinstance(child, ast.Name) and child.id in (PARTIAL_FUNCTION, GENERIC_FUNCTION)
               for child in ast.walk(node)):
            raise RuntimeError("removed renderer referenced during helper module initialization")
    # Retain full originals outside the importable source tree for rollback.
    backup = project / ".renderer_single_implementation_backup"
    if backup.exists():
        raise RuntimeError("existing backup directory; refuse overwrite")
    backup.mkdir()
    try:
        for src in (old, primary, partial):
            shutil.copy2(src, backup / src.name)
        helper.write_text(helpers_text, encoding="utf8")
        primary.write_text(changed_primary, encoding="utf8")
        partial.write_text(changed_partial, encoding="utf8")
        alias.parent.mkdir(exist_ok=False)
        alias.write_text(_public_delegate(), encoding="utf8")
        old.unlink()
    except BaseException:
        shutil.copy2(backup / old.name, old)
        shutil.copy2(backup / primary.name, primary)
        shutil.copy2(backup / partial.name, partial)
        if alias.exists():
            alias.unlink()
        if alias.parent.is_dir():
            alias.parent.rmdir()
        if helper.exists():
            helper.unlink()
        raise
    return "INSTALLED"


if __name__ == "__main__":
    project = Path(__file__).resolve().parent.parent
    result = install(project)
    print("Single Narrative implementation cleanup:", result)
    print("Duplicate renderer .py removed; lazy import-compatibility package retained")
    print("Search and proof mathematics unchanged; full pytest NOT run")
