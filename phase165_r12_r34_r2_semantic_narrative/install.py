"""Install the R34-R2 presentation-only function with guardrails."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def install(project: Path, package: Path):
    target = project / "toda_group_proof_narrative_renderer.py"
    if not target.is_file() or not (project/"phase165_r12_r34_narrative.py").exists():
        raise FileNotFoundError("R12-R34-R1 must be installed")
    before = target.read_text(encoding="utf8")
    nodes = [n for n in ast.parse(before).body if isinstance(n, ast.FunctionDef) and n.name == "render_toda_partial_proof_narrative_markdown"]
    if len(nodes)!=1 or "completed_step_text" not in before:
        raise RuntimeError("unknown common Renderer version")
    node = nodes[0]
    replacement = (package/"render_function.py.txt").read_text(encoding="utf8")
    lines = before.splitlines(keepends=True)
    after = "".join(lines[:node.lineno-1])+replacement.rstrip()+"\n"+"".join(lines[node.end_lineno:])
    ast.parse(after)
    helper = package/"phase165_r12_r34_r2_semantic_narrative.py"
    destination = project/helper.name
    if before != after:
        shutil.copy2(target,target.with_name(target.name+".r12_r34_r2_backup"))
        target.write_text(after,encoding="utf8")
    if not destination.exists() or destination.read_bytes()!=helper.read_bytes():
        shutil.copy2(helper,destination)
    print("R12-R34-R2 typed semantic Narrative: CONNECTED")

if __name__=="__main__":
    package=Path(__file__).resolve().parent
    install(package.parent,package)
