"""Patch only the complete shared Renderer function over the installed R10A."""
from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "phase168_r3_5_model_renderer.py"
R10A_INSTALLED = ROOT / "phase169_r10a_verified_stable_chain_projection" / "output" / "phase168_r3_5_model_renderer.py.FULL"
OUTPUT = HERE / "output"
BACKUP = OUTPUT / "phase168_r3_5_model_renderer.py.r10a-before"

OLD_IMPORT = """    from phase169_r10a_verified_stable_chain_projection.projection import (
        project_verified_stable_image_chain,
    )
    stable_chain_display = (
        project_verified_stable_image_chain(model, order)
        if not incomplete else None
    )
"""
NEW_IMPORT = """    from phase169_r10a_verified_stable_chain_projection.projection import (
        project_verified_stable_image_chain,
    )
    from phase169_r10a2_unified_one_stem.one_stem_projection import (
        project_verified_one_stem_notation_chain,
    )
    stable_chain_display = (
        (project_verified_stable_image_chain(model, order)
         or project_verified_one_stem_notation_chain(model, order))
        if not incomplete else None
    )
"""
OLD_TRANSITION = "    transition = project_stable_eta_notation_transition(model, index)\n"
NEW_TRANSITION = """    transition = (
        None
        if stable_chain_display is not None and index == stable_chain_display.root_index
        else project_stable_eta_notation_transition(model, index)
    )
"""


def full_renderer_function(code: str) -> str:
    """Export the complete replacement function, without truncation."""
    tree = ast.parse(code)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "render_model_backed_narrative_markdown"]
    if len(matches) != 1:
        raise RuntimeError("expected exactly one Renderer function")
    node = matches[0]
    return "\n".join(code.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def replacement_content(original: bytes, expected: bytes) -> tuple[bytes, str]:
    """Reject any local Renderer different from the successful R10A output."""
    if original != expected:
        raise RuntimeError("Renderer differs from installed and audited R10A output")
    windows = b"\r\n" in original
    code = original.decode("utf-8").replace("\r\n", "\n")
    if code.count(OLD_IMPORT) != 1 or code.count(OLD_TRANSITION) != 1:
        raise RuntimeError("R10A insertion points missing or duplicated")
    updated = code.replace(OLD_IMPORT, NEW_IMPORT).replace(OLD_TRANSITION, NEW_TRANSITION)
    ast.parse(updated)
    full = full_renderer_function(updated)
    new_content = updated.replace("\n", "\r\n") if windows else updated
    return new_content.encode("utf-8"), full


def main() -> None:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R10A2 requires develop")
    if not R10A_INSTALLED.is_file():
        raise RuntimeError("R10A output/FULL missing: run successful R10A1 first")
    original = TARGET.read_bytes()
    expected = R10A_INSTALLED.read_bytes()
    changed, full = replacement_content(original, expected)
    OUTPUT.mkdir(exist_ok=True)
    if BACKUP.exists():
        if BACKUP.read_bytes() != original:
            raise RuntimeError("an earlier R10A2 backup differs from current Renderer")
    else:
        BACKUP.write_bytes(original)
    (OUTPUT / "render_model_backed_narrative_markdown_FULL.py").write_text(
        full, encoding="utf-8")
    (OUTPUT / "phase168_r3_5_model_renderer.py.FULL").write_bytes(changed)
    tmp = TARGET.with_suffix(".py.r10a2-tmp")
    try:
        tmp.write_bytes(changed)
        tmp.replace(TARGET)
    finally:
        if tmp.exists():
            tmp.unlink()
    print("R10A2_PATCHED=" + str(TARGET))
    print("R10A2_RESTORE_POINT=" + str(BACKUP))
    print("R10A2_FULL_FUNCTION=" + str(OUTPUT / "render_model_backed_narrative_markdown_FULL.py"))
    print("R10A2_FULL_FILE=" + str(OUTPUT / "phase168_r3_5_model_renderer.py.FULL"))


if __name__ == "__main__":
    main()
