"""Conservative full-function replacement installer for the shared provider."""
from __future__ import annotations

import ast
from pathlib import Path

TARGET = Path("phase165_r52_r9_shared_math.py")
START = 'def shared_expansion_provider('
ANCHOR = '    # Phase 175 R4R10: screened literature claims produce only open subgoals.\n'
INSERT = '''    # Phase 175 R4R12R9: infer a generator image from a proved typed
    # Delta equality; the equality itself remains an independent proof goal.
    from phase175_r4r12r9_delta_generator_image_bridge.rule import (
        expand_proved_delta_equality_image,
    )
    extra_providers = (expand_proved_delta_equality_image,) + tuple(extra_providers)
'''


def replacement(original: str) -> tuple[str, str]:
    """Return (new module, entire updated function), or reject drift."""
    normalized = original.replace("\r\n", "\n")
    tree = ast.parse(normalized)
    matches = [node for node in tree.body
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
               and node.name == "shared_expansion_provider"]
    if len(matches) != 1:
        raise RuntimeError("R9_SHARED_PROVIDER_FUNCTION_MISSING")
    node = matches[0]
    lines = normalized.splitlines(keepends=True)
    start = node.lineno - 1
    end = node.end_lineno
    before = "".join(lines[:start])
    function = "".join(lines[start:end])
    after = "".join(lines[end:])
    if function.count(ANCHOR) != 1 or not function.startswith(START):
        raise RuntimeError("R9_UNREVIEWED_PROVIDER_ANCHOR")
    if INSERT in function:
        return normalized, function
    modified_function = function.replace(ANCHOR, INSERT + ANCHOR, 1)
    modified = before + modified_function + after
    ast.parse(modified)
    return modified, modified_function


def install(root: Path, dry_run: bool, output: Path) -> dict[str, object]:
    path = root / TARGET
    raw = path.read_bytes()
    if b"\r\n" in raw and b"\n" in raw.replace(b"\r\n", b""):
        raise RuntimeError("R9_MIXED_EOL_REQUIRES_REVIEW")
    old = raw.decode("utf-8")
    new, whole_function = replacement(old)
    output.mkdir(parents=True, exist_ok=True)
    (output / "SHARED_PROVIDER_FULL_AFTER.py").write_text(whole_function, encoding="utf-8")
    changed = old.replace("\r\n", "\n") != new
    if changed and not dry_run:
        eol = "\r\n" if b"\r\n" in raw else "\n"
        path.write_bytes(new.replace("\n", eol).encode("utf-8"))
    return {"target": str(TARGET), "patch_required": changed,
            "patch_applied": bool(changed and not dry_run),
            "full_function_output": str(output / "SHARED_PROVIDER_FULL_AFTER.py")}
