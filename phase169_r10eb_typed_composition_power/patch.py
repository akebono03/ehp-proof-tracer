"""Guarded R10EB two-function display-only wiring with LF/CRLF preservation."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
TARGETS = {
    "phase168_r3_27_typed_statement_projection.py": "acc1ba15d78872553921dc30fd7487e4a48e89d2",
    "toda_human_readable_renderer.py": "2eb51eac89684310ecebd41ac09afc8f8ae0eb61",
}

NARRATIVE_ANCHOR = "    from expression import Composition\n\n    if isinstance(value, Multiple)"
NARRATIVE_REPLACEMENT = '''    from expression import Composition

    if isinstance(value, Composition):
        from phase169_r10eb_typed_composition_power.display import (
            typed_stable_composition_power_latex,
        )
        power = typed_stable_composition_power_latex(value)
        if power is not None:
            return power

    if isinstance(value, Multiple)'''
PUBLIC_ANCHOR = '''  if isinstance(
    expression,
    Composition,
  ):
    # Compress only a well-typed consecutive sigma family composition.'''
PUBLIC_REPLACEMENT = '''  if isinstance(
    expression,
    Composition,
  ):
    from phase169_r10eb_typed_composition_power.display import (
      typed_stable_composition_power_latex,
    )
    power = typed_stable_composition_power_latex(expression)
    if power is not None:
      return power
    # Keep the legacy sigma fallback for historical non-canonical display names.
    # Compress only a well-typed consecutive sigma family composition.'''


def _style_and_source(raw: bytes) -> tuple[str, str]:
    if not raw:
        raise RuntimeError("R10EB empty source")
    if b"\r\n" in raw:
        other = raw.replace(b"\r\n", b"")
        if b"\n" in other or b"\r" in other:
            raise RuntimeError("R10EB mixed newlines refused")
        return raw.replace(b"\r\n", b"\n").decode("utf-8"), "CRLF"
    if b"\r" in raw:
        raise RuntimeError("R10EB CR-only source refused")
    return raw.decode("utf-8"), "LF"


def _git_blob(source: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(source)).encode("ascii") + b"\0" + source).hexdigest()


def _function(source: str, name: str) -> str:
    module = ast.parse(source)
    selected = [node for node in module.body if isinstance(node, ast.FunctionDef)
                and node.name == name]
    if len(selected) != 1:
        raise RuntimeError("R10EB expected one function " + name)
    return ast.get_source_segment(source, selected[0]) or ""


def transform(path: str, source: str) -> tuple[str, str]:
    """Add an early generic display path to precisely one existing function."""
    if path == "phase168_r3_27_typed_statement_projection.py":
        function_name = "element_tex"
        old, new = NARRATIVE_ANCHOR, NARRATIVE_REPLACEMENT
    elif path == "toda_human_readable_renderer.py":
        function_name = "render_toda_expression_latex"
        old, new = PUBLIC_ANCHOR, PUBLIC_REPLACEMENT
    else:
        raise RuntimeError("R10EB unreviewed patch destination")
    original_function = _function(source, function_name)
    if original_function.count(old) != 1 or source.count(old) != 1:
        raise RuntimeError("R10EB reviewed function anchor changed: " + function_name)
    updated = source.replace(old, new, 1)
    updated_function = _function(updated, function_name)
    if updated_function.count(new) != 1 or updated_function.count(old) != 0:
        raise RuntimeError("R10EB function postcondition failed: " + function_name)
    if _function(source, function_name).replace(old, new, 1) != updated_function:
        raise RuntimeError("R10EB unexpected mutation within " + function_name)
    return updated, updated_function


def prepare_patch(source_files: dict[str, bytes]) -> dict[str, tuple[bytes, str, str]]:
    """Prepare BOTH replacements without touching production files."""
    if set(source_files) != set(TARGETS):
        raise RuntimeError("R10EB required both reviewed source files")
    prepared = {}
    for path, expected in TARGETS.items():
        source, style = _style_and_source(source_files[path])
        if _git_blob(source.encode("utf-8")) != expected:
            raise RuntimeError("R10EB source Git blob not reviewed: " + path)
        updated, function = transform(path, source)
        payload = updated.encode("utf-8")
        if style == "CRLF":
            payload = payload.replace(b"\n", b"\r\n")
        prepared[path] = payload, function, style
    return prepared


def main() -> None:
    source_files = {path: (ROOT / path).read_bytes() for path in TARGETS}
    updated = prepare_patch(source_files)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path, (payload, function, style) in updated.items():
        target = ROOT / path
        target.write_bytes(payload)
        clean_name = path.replace("/", "__")
        (OUTPUT / (clean_name + ".FULL")).write_bytes(payload)
        (OUTPUT / (clean_name + ".FUNCTION_FULL.py")).write_text(
            function + "\n", encoding="utf-8",
        )
        print("R10EB_PATCHED=" + str(target))
        print("R10EB_NEWLINE=" + path + "=" + style)
        print("R10EB_FULL_FUNCTION=" + str(OUTPUT / (clean_name + ".FUNCTION_FULL.py")))
    print("R10EB_SOURCE_OR_RULE_CHANGED=False")


if __name__ == "__main__":
    main()
