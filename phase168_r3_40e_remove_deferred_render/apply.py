"""R3-40E: Remove only the dead deferred-render loop from the common Renderer."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase168_r3_5_model_renderer.py"
EXPECTED = PACKAGE / "full_functions" / "render_model_backed_narrative_markdown_FULL.py"
PRIOR = ROOT / "phase168_r3_40d_runner_module_fix" / "full_functions" / "render_model_backed_narrative_markdown_FULL.py"
FUNCTION_NAME = "render_model_backed_narrative_markdown"


def extract_function(source: str, name: str) -> str:
    nodes = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError(f"Expected exactly one function named {name}")
    node = nodes[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno]).rstrip() + "\n"


def patch_source(source: str, old_function: str, new_function: str) -> str:
    current = extract_function(source, FUNCTION_NAME)
    if current == new_function:
        return source
    if current != old_function:
        raise RuntimeError("Unexpected common Renderer version; refusing R3-40E patch")
    nodes = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef) and node.name == FUNCTION_NAME]
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    lines[node.lineno - 1:node.end_lineno] = [new_function.rstrip() + "\n"]
    result = "".join(lines)
    ast.parse(result)
    return result


def main() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    if not PRIOR.is_file():
        raise FileNotFoundError("R3-40D package with original function is missing")
    old_function = PRIOR.read_text(encoding="utf-8").rstrip() + "\n"
    new_function = EXPECTED.read_text(encoding="utf-8").rstrip() + "\n"
    if old_function == new_function:
        raise RuntimeError("No renderer simplification supplied")
    if "for postponed in entry.after_indices:" not in old_function:
        raise RuntimeError("Prior R3-40D function does not contain deferred rendering")
    if "after_indices" in new_function:
        raise RuntimeError("R3-40E function still uses deferred rendering")

    data = TARGET.read_bytes()
    original = data.decode("utf-8-sig").replace("\r\n", "\n")
    revised = patch_source(original, old_function, new_function)
    full_output = PACKAGE / "full_files"
    full_output.mkdir(parents=True, exist_ok=True)
    (full_output / TARGET.name).write_text(revised, encoding="utf-8")
    if revised == original:
        print("ALREADY_PATCHED", TARGET.name)
        return
    print("PRIOR_SHA256", hashlib.sha256(data).hexdigest())
    TARGET.write_text(revised, encoding="utf-8", newline="")
    print("PATCHED", TARGET.name)
    print("FULL_FUNCTION", EXPECTED)
    print("FULL_FILE", full_output / TARGET.name)


if __name__ == "__main__":
    main()
