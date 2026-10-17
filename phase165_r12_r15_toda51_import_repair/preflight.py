"""Restore the missing R12-R14 module required by the R12-R15 audit."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def main() -> None:
    project = Path.cwd()
    package = Path(__file__).resolve().parent
    supplied = package / "prerequisite" / "phase165_r12_r14_kernel_closure.py"
    destination = project / supplied.name
    source = supplied.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(supplied))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    if not {"summarize_proof_ancestry", "prove_kernel_in_screened_context"} <= functions:
        raise RuntimeError("Bundled R12-R14 prerequisite is incomplete")
    if destination.is_file():
        current = destination.read_text(encoding="utf-8")
        existing_tree = ast.parse(current, filename=str(destination))
        existing_functions = {node.name for node in existing_tree.body if isinstance(node, ast.FunctionDef)}
        if "summarize_proof_ancestry" not in existing_functions:
            raise RuntimeError("Existing R12-R14 module lacks summarize_proof_ancestry; no overwrite performed")
        print("Existing R12-R14 module preserved:", destination)
    else:
        shutil.copy2(supplied, destination)
        print("Restored missing R12-R14 module:", destination)


if __name__ == "__main__":
    main()
