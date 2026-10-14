"""R57-R3: retire two obsolete renderer implementations, fail closed."""
from __future__ import annotations

import ast
import shutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
GENERIC = ROOT / "toda_group_proof_generic_narrative_renderer.py"
R39 = ROOT / "phase165_r14_r39_web_connection.py"
LEGACY_FUNCTION = "render_toda_group_proof_generic_proof_markdown"
COMPAT_SOURCE = (PACKAGE / "phase165_r14_r39_web_connection.py").read_text(encoding="utf-8")


def _remove_unused_generic_entry(source: str) -> str:
    module = ast.parse(source)
    matches = [
        node for node in module.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == LEGACY_FUNCTION
    ]
    if not matches:
        return source
    if len(matches) != 1:
        raise RuntimeError("Multiple obsolete generic renderer definitions")
    node = matches[0]
    lines = source.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno - 1] + lines[node.end_lineno:])
    ast.parse(updated)
    return updated


def _check_production_references() -> None:
    for path in ROOT.glob("*.py"):
        if path in (GENERIC, R39):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if any(alias.name == LEGACY_FUNCTION for alias in node.names):
                    raise RuntimeError(f"Obsolete renderer still imported: {path.name}")
            if isinstance(node, ast.Attribute) and node.attr == LEGACY_FUNCTION:
                raise RuntimeError(f"Obsolete renderer still accessed: {path.name}")
            if isinstance(node, ast.Name) and node.id == LEGACY_FUNCTION:
                raise RuntimeError(f"Obsolete renderer still referenced: {path.name}")
    # Static scanning cannot certify dynamic getattr/importlib or code in subfolders.


def install() -> None:
    if not GENERIC.is_file() or not R39.is_file():
        raise FileNotFoundError("Required production renderer file missing")
    generic_original = GENERIC.read_text(encoding="utf-8")
    r39_original = R39.read_text(encoding="utf-8")
    if "def render_toda_group_proof_generic_proof_markdown(" not in generic_original and r39_original == COMPAT_SOURCE:
        print("R57-R3 already installed")
        return
    _check_production_references()
    generic_updated = _remove_unused_generic_entry(generic_original)
    if generic_updated == generic_original and r39_original != COMPAT_SOURCE:
        raise RuntimeError("Missing expected obsolete generic entry; check local baseline")
    if "def build_phase165_pi32_web_view(" not in r39_original:
        raise RuntimeError("Unexpected R39 legacy API shape")
    if r39_original != COMPAT_SOURCE and "# Render the registered backward proof" not in r39_original:
        raise RuntimeError("Unexpected R39 source; refusing destructive replacement")
    ast.parse(COMPAT_SOURCE)
    if generic_updated != generic_original:
        shutil.copy2(GENERIC, GENERIC.with_suffix(".py.phase165_r57_r3_backup"))
    if r39_original != COMPAT_SOURCE:
        shutil.copy2(R39, R39.with_suffix(".py.phase165_r57_r3_backup"))
    if generic_updated != generic_original:
        GENERIC.write_text(generic_updated, encoding="utf-8")
    if r39_original != COMPAT_SOURCE:
        R39.write_text(COMPAT_SOURCE, encoding="utf-8")
    print("R57-R3: unused generic proof renderer removed; R39 fixed prose retired")
    print("R39 API now delegates to shared Web entry; internal math helpers preserved")
    print("Full pytest NOT run")


if __name__ == "__main__":
    install()
