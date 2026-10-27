"""Fail-closed, single-function renderer patch; exports full replacement source."""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase168_r3_5_model_renderer.py"
OUTPUT = PACKAGE / "output"
BACKUP = OUTPUT / "phase168_r3_5_model_renderer.py.before"
EXPECTED_SHA256 = "983e72461f33dee20b4e22f31db2625b662e7a62e049962b490b093089ae4fb8"

OLD = """    for index in order:
        if index in suppressed_body_indices:
"""
NEW = """    # R10A: presentation-only projection of the already-verified E^r image chain.
    # The Proof Tree, its citations, and all original ProofSteps remain intact.
    from phase169_r10a_verified_stable_chain_projection.projection import (
        project_verified_stable_image_chain,
    )
    stable_chain_display = (
        project_verified_stable_image_chain(model, order)
        if not incomplete else None
    )
    if stable_chain_display is not None:
        suppressed_body_indices.update(stable_chain_display.hidden_indices)
    for index in order:
        if stable_chain_display is not None and index == stable_chain_display.root_index:
            source_tags = ", ".join(
                f"[R{number}]" for number in stable_chain_display.citation_numbers
            )
            compressed_statement = (
                rf"$E^{{{stable_chain_display.exponent}}}"
                rf"({stable_chain_display.source_tex})="
                rf"{stable_chain_display.target_tex}$"
            )
            lines.extend((f"{source_tags}より, {compressed_statement}.", ""))
        if index in suppressed_body_indices:
"""


def _function_source(code: str) -> str:
    tree = ast.parse(code)
    matches = [node for node in tree.body
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
               and node.name == "render_model_backed_narrative_markdown"]
    if len(matches) != 1:
        raise RuntimeError("expected one full renderer function")
    node = matches[0]
    return "\n".join(code.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def replacement_content(original: bytes, *, expected_sha256: str = EXPECTED_SHA256
                        ) -> tuple[bytes, str]:
    if hashlib.sha256(original).hexdigest() != expected_sha256:
        raise RuntimeError("renderer SHA256 differs from the reviewed R9 baseline")
    text = original.decode("utf-8")
    normal = text.replace("\r\n", "\n")
    if normal.count(OLD) != 1:
        raise RuntimeError("reviewed renderer insertion anchor is missing or duplicated")
    updated = normal.replace(OLD, NEW)
    ast.parse(updated)
    result = updated.replace("\n", "\r\n") if b"\r\n" in original else updated
    return result.encode("utf-8"), _function_source(updated)


def main() -> None:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            text=True, capture_output=True, check=True).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R10A requires the develop branch")
    tracked = subprocess.run(["git", "status", "--porcelain", "--", TARGET.name],
                             cwd=ROOT, text=True, capture_output=True,
                             check=True).stdout.strip()
    if tracked:
        raise RuntimeError("renderer has local changes; refusing to overwrite")
    original = TARGET.read_bytes()
    patched, full = replacement_content(original)
    OUTPUT.mkdir(exist_ok=True)
    if BACKUP.exists():
        # A failed R10A run restores the original renderer but keeps the backup.
        # Reuse it only when the bytes are identical; never overwrite a backup.
        if BACKUP.read_bytes() != original:
            raise RuntimeError("previous backup differs from the pristine renderer")
        print("R10A_BACKUP_REUSED=True")
    else:
        BACKUP.write_bytes(original)
        print("R10A_BACKUP_REUSED=False")
    (OUTPUT / "render_model_backed_narrative_markdown_FULL.py").write_text(
        full, encoding="utf-8",
    )
    (OUTPUT / "phase168_r3_5_model_renderer.py.FULL").write_bytes(patched)
    temp = TARGET.with_suffix(".py.r10a-tmp")
    try:
        temp.write_bytes(patched)
        temp.replace(TARGET)
    finally:
        if temp.exists():
            temp.unlink()
    print("R10A_PATCHED=" + str(TARGET))
    print("R10A_BACKUP=" + str(BACKUP))
    print("R10A_FULL_FUNCTION=" + str(OUTPUT / "render_model_backed_narrative_markdown_FULL.py"))
    print("R10A_FULL_FILE=" + str(OUTPUT / "phase168_r3_5_model_renderer.py.FULL"))


if __name__ == "__main__":
    main()
