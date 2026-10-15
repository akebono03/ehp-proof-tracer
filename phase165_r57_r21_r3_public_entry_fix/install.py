"""Phase165 R57-R21-R3: repair and verify the public partial renderer entry."""
from __future__ import annotations

import ast
import inspect
from pathlib import Path
import shutil
import sys

NAME = "render_partial_proof_markdown"


def function_definitions(source: str, name: str = NAME) -> tuple[ast.FunctionDef, ...]:
    return tuple(
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )


def effective_definition(source: str, name: str = NAME) -> str:
    nodes = function_definitions(source, name)
    if not nodes:
        raise ValueError("public partial renderer entry not found: " + name)
    node = nodes[-1]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def install(project: Path, package: Path) -> str:
    target = project / "phase165_r52_partial_proof.py"
    renderer = project / "toda_group_proof_generic_narrative_renderer.py"
    if not target.is_file() or not renderer.is_file():
        raise FileNotFoundError("required public and shared renderer files missing")
    original = target.read_text(encoding="utf8")
    replacement = (package / "render_partial_proof_markdown.py.txt").read_text(encoding="utf8")
    required = effective_definition(replacement)
    existing = effective_definition(original)
    if existing.rstrip() == required.rstrip():
        return "ALREADY_INSTALLED"
    if not any(isinstance(node, ast.Call) for node in ast.walk(function_definitions(original)[-1])):
        raise RuntimeError("unrecognized public partial renderer implementation")
    nodes = function_definitions(original)
    node = nodes[-1]
    lines = original.splitlines(keepends=True)
    updated = "".join(lines[:node.lineno - 1]) + required.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    backup = target.with_name(target.name + ".phase165_r57_r21_r3_backup")
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_text(updated, encoding="utf8")
    if effective_definition(target.read_text(encoding="utf8")).rstrip() != required.rstrip():
        raise RuntimeError("public renderer entry update verification failed")
    return "INSTALLED"


def verify_real_entry(project: Path) -> None:
    from phase165_r52_partial_proof import render_partial_proof_markdown
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    import toda_group_proof_generic_narrative_renderer as renderer
    import phase165_r52_partial_proof as partial

    print("Public partial module:", Path(partial.__file__).resolve())
    print("Shared Renderer module:", Path(renderer.__file__).resolve())
    print("Public function source:", inspect.getsourcefile(render_partial_proof_markdown))
    print("Shared function source:", inspect.getsourcefile(renderer.render_toda_partial_proof_narrative_markdown))
    if Path(partial.__file__).resolve() != (project / "phase165_r52_partial_proof.py").resolve():
        raise RuntimeError("public partial module resolved outside project root")
    if Path(renderer.__file__).resolve() != (project / "toda_group_proof_generic_narrative_renderer.py").resolve():
        raise RuntimeError("shared renderer module resolved outside project root")
    result = search_group_from_registered_goal(n=3, k=1)
    rendered = render_partial_proof_markdown(result)
    expected = renderer.render_toda_partial_proof_narrative_markdown(result)
    if rendered != expected:
        raise RuntimeError("public wrapper and shared renderer outputs differ")
    if "## 証明対象" not in rendered or "## 使用する結果" not in rendered or "## 証明\n" not in rendered:
        raise RuntimeError("public renderer output is not the common narrative layout")
    heading = rendered.split("## 証明対象", 1)[1].split("## 使用する結果", 1)[0]
    if "\\pi_{5}^{5}" in heading:
        raise RuntimeError("auxiliary pi55 goal is rendered as the main target")
    if not any(token in heading for token in ("\\pi_{4}^{3}", "π43", "π_4^3")):
        raise RuntimeError("requested pi43 target missing from narrative heading")
    print("Verified public entry output: target and shared sections")


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    project = package.parent
    sys.path.insert(0, str(project))
    print("R57-R21-R3:", install(project, package))
    verify_real_entry(project)
    print("No mathematical rules or search functions modified; full pytest NOT run")
