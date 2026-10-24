"""Phase 168 R3-40C: guarded, dependency-preserving common narrative projection."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
FULL = PACKAGE / "full_functions"

BASELINE_SHA256 = {
    "phase168_r3_29_order_projection.py": "0a2b7f665030cb72670915b3c6b04edc8fc66ca7952612c4a6e105bb03764162",
    "phase168_r3_27_typed_statement_projection.py": "74e2f644ad92a0d0d41ffe52727d1f017f635151de245112fbc826dee5ce006c",
    "phase168_r3_5_model_renderer.py": "955d3a1d963898f4ddd89814400b23f50542d1a5bc326f2a3a9278a75edb0c97",
}


def extract_function(source: str, name: str) -> str:
    matches = [n for n in ast.parse(source).body
               if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one function {name}")
    node = matches[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno]).rstrip() + "\n"


def replace_function(source: str, name: str, replacement: str) -> str:
    nodes = [n for n in ast.parse(source).body
             if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(nodes) != 1:
        raise RuntimeError(f"Expected one function {name}")
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    lines[node.lineno - 1:node.end_lineno] = [replacement.rstrip() + "\n"]
    result = "".join(lines)
    ast.parse(result)
    return result


def patch_order(source: str) -> str:
    expected = (FULL / "project_narrative_order_FULL.py").read_text(encoding="utf-8")
    old = extract_function(source, "project_narrative_order")
    if old == expected:
        return source
    if "postponed.setdefault(max(source_index, iso_index), []).append(index)" not in old:
        raise RuntimeError("Expected pre-R3-40A narrative ordering; R3-40A may already be installed")
    return replace_function(source, "project_narrative_order", expected)


def patch_projection(source: str) -> str:
    helper = (FULL / "project_stable_eta_notation_transition_FULL.py").read_text(encoding="utf-8")
    if "def project_stable_eta_notation_transition(" in source:
        if extract_function(source, "project_stable_eta_notation_transition") != helper:
            raise RuntimeError("Conflicting existing stable-eta transition function")
        return source
    anchor = "def typed_sentence(statement, step):\n"
    if source.count(anchor) != 1:
        raise RuntimeError("Expected typed_sentence anchor not found")
    revised = source.replace(anchor, helper.rstrip() + "\n\n\n" + anchor)
    ast.parse(revised)
    return revised


def patch_renderer(source: str) -> str:
    expected = (FULL / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")
    old = extract_function(source, "render_model_backed_narrative_markdown")
    if old == expected:
        return source
    if "project_toda45_specialization_citation_numbers" not in old:
        raise RuntimeError("R3-39G-4 citation import is missing")
    if "project_stable_eta_notation_transition" in old:
        raise RuntimeError("Renderer already changed by another eta-projection patch")
    if "for postponed in entry.after_indices:" not in old:
        raise RuntimeError("R3-39G postponed entry contract is missing")
    return replace_function(source, "render_model_backed_narrative_markdown", expected)


def main() -> None:
    changes = (
        ("phase168_r3_29_order_projection.py", patch_order),
        ("phase168_r3_27_typed_statement_projection.py", patch_projection),
        ("phase168_r3_5_model_renderer.py", patch_renderer),
    )
    replacements = []
    for name, transform in changes:
        path = PROJECT / name
        raw = path.read_bytes()
        original = raw.decode("utf-8-sig").replace("\r\n", "\n")
        before_sha = hashlib.sha256(raw).hexdigest()
        revised = transform(original)
        if revised != original and before_sha != BASELINE_SHA256[name]:
            raise RuntimeError(f"Unexpected repository baseline for {name}: {before_sha}")
        ast.parse(revised)
        replacements.append((name, path, original, revised))

    full_files = PACKAGE / "full_files"
    full_files.mkdir(exist_ok=True)
    for name, path, original, revised in replacements:
        (full_files / name).write_text(revised, encoding="utf-8")
    for name, path, original, revised in replacements:
        if revised == original:
            print("ALREADY_PATCHED", name)
        else:
            path.write_text(revised, encoding="utf-8", newline="")
            print("PATCHED", name)
    print("FULL_FUNCTIONS", FULL)
    print("FULL_FILES", full_files)


if __name__ == "__main__":
    main()
