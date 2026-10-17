"""R12-R34-R1: guarded display-only fixes to existing shared entrypoints."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

def replace_function(source: str, name: str, replacement: str) -> str:
    matches = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(matches) != 1:
        raise RuntimeError("expected one existing function: " + name)
    node = matches[0]
    lines = source.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno - 1]) + replacement.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated

def install(project: Path, package: Path) -> None:
    renderer = project / "toda_group_proof_narrative_renderer.py"
    adapter = project / "phase165_r56_presentation_adapter.py"
    if not renderer.exists() or not adapter.exists():
        raise FileNotFoundError("shared renderer / completed adapter missing")
    before_renderer = renderer.read_text(encoding="utf8")
    before_adapter = adapter.read_text(encoding="utf8")
    if "phase165_r12_r34_narrative" not in before_renderer:
        raise RuntimeError("R12-R34 must be installed before R12-R34-R1")
    renderer_replacement = (package / "render_function.py.txt").read_text(encoding="utf8")
    adapter_replacement = (package / "adapter_function.py.txt").read_text(encoding="utf8")
    updated_renderer = replace_function(before_renderer, "render_toda_partial_proof_narrative_markdown", renderer_replacement)
    updated_adapter = replace_function(before_adapter, "render_completed_shared_narrative", adapter_replacement)
    # Older adapter module already imports both required names, but protect against drift.
    if "from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus" not in before_adapter:
        raise RuntimeError("unknown adapter imports; refusing unsafe replacement")
    for target, before, after in ((renderer,before_renderer,updated_renderer),(adapter,before_adapter,updated_adapter)):
        if before != after:
            shutil.copy2(target, target.with_name(target.name + ".r12_r34_r1_backup"))
            target.write_text(after,encoding="utf8")
    print("R12-R34-R1 common completed renderer: CONNECTED")

if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    install(package.parent,package)
