"""Guarded one-function edit to the canonical shared Web adapter."""
from __future__ import annotations

import ast
from pathlib import Path


ANCHOR = '''        rendered_lines = _build_group_proof_rendered_lines(markdown)
'''
REPLACEMENT = '''        from phase173_r4_r15r9_shared_abstract_renderer.projection import (
            render_certified_abstract_section,
        )
        abstract_markdown = render_certified_abstract_section(result)
        if abstract_markdown:
            markdown = markdown.rstrip() + "\\n\\n" + abstract_markdown + "\\n"
        rendered_lines = _build_group_proof_rendered_lines(markdown)
'''
BASELINE_BLOB = "b427ca5a1c1d0eb213f9a4c76fa559b849f8987c"


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def transform(source: bytes) -> bytes:
    """Replace one reviewed adapter statement, retaining all other functions."""
    eol = "\r\n" if b"\r\n" in source else "\n"
    if b"\r\n" in source and source.count(b"\r\n") != source.count(b"\n"):
        raise RuntimeError("Mixed line endings require review")
    original = source.decode("utf-8-sig").replace("\r\n", "\n")
    if original.count(ANCHOR) != 1 or "render_certified_abstract_section" in original:
        raise RuntimeError("Unreviewed or already patched shared Web adapter")
    tree = ast.parse(original)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1 or functions[0].name != "build_partial_web_group_proof_view":
        raise RuntimeError("Unexpected shared Web adapter module structure")
    updated = original.replace(ANCHOR, REPLACEMENT)
    ast.parse(updated)
    return updated.replace("\n", eol).encode("utf-8")


def complete_changed_units(baseline: bytes) -> str:
    """Output the entire revised function and full import section for review."""
    content = transform(baseline).decode("utf-8").replace("\r\n", "\n")
    tree = ast.parse(content)
    imports = []
    function = None
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append("".join(content.splitlines(keepends=True)[node.lineno-1:node.end_lineno]))
        elif isinstance(node, ast.FunctionDef) and node.name == "build_partial_web_group_proof_view":
            function = "".join(content.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
    if function is None:
        raise RuntimeError("Expected one full modified function")
    return (
        "# R4-R15R9 — 変更後の全 import・変更関数全文\n\n"
        "変更ファイル：`phase165_r52_r3_web_adapter.py`。"
        "トップレベル import は変更なし。\n\n"
        "## 完全な import 部分\n\n```python\n"
        + "\n".join(imports)
        + "```\n\n## `build_partial_web_group_proof_view` 関数全体\n\n```python\n"
        + function + "```\n"
    )


def write_complete_sources(baseline: bytes, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "phase165_r52_r3_web_adapter_FULL.py.txt").write_bytes(transform(baseline))
    (directory / "FULL_CHANGED_UNITS.md").write_text(
        complete_changed_units(baseline), encoding="utf-8",
    )
