"""R57-R10 fail-closed, idempotent installer."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
TARGET = PROJECT / "phase165_r56_presentation_adapter.py"
HELPER = PROJECT / "phase165_r57_r10_step_narrative.py"


def replace_function(source: str, replacement: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == "render_completed_shared_narrative"]
    if len(matches) != 1:
        raise RuntimeError("expected one completed adapter function")
    node = matches[0]
    lines = source.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno - 1]) + replacement + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated


def install() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    current = TARGET.read_text(encoding="utf-8")
    replacement = (PACKAGE / "phase165_r56_presentation_adapter.py").read_text(encoding="utf-8")
    function = next(node for node in ast.parse(replacement).body
                    if isinstance(node, ast.FunctionDef) and node.name == "render_completed_shared_narrative")
    replacement_lines = replacement.splitlines(keepends=True)
    block = "".join(replacement_lines[function.lineno - 1:function.end_lineno])
    if "render_completed_from_proofsteps(result, root)" in current:
        if HELPER.read_text(encoding="utf-8") != (PACKAGE / HELPER.name).read_text(encoding="utf-8"):
            raise RuntimeError("existing helper differs; refusing overwrite")
        print("R57-R10 already installed")
        return
    if "build_complete_toda_group_result_proof_replay(group_result)" not in current:
        raise RuntimeError("unexpected completed adapter; no modification")
    updated = replace_function(current, block)
    helper = (PACKAGE / HELPER.name).read_text(encoding="utf-8")
    ast.parse(helper)
    if HELPER.exists() and HELPER.read_text(encoding="utf-8") != helper:
        raise RuntimeError("different helper already exists; no modification")
    shutil.copy2(TARGET, PROJECT / "phase165_r56_presentation_adapter.py.phase165_r57_r10_backup")
    if not HELPER.exists():
        HELPER.write_text(helper, encoding="utf-8")
    TARGET.write_text(updated, encoding="utf-8")
    print("R57-R10: installed evidence-aligned completed Narrative fallback")
    print("No old renderer deleted; full pytest NOT run")


if __name__ == "__main__":
    install()
