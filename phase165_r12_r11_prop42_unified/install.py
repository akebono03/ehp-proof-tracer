"""Install the shared Proposition 4.2 path without replacing local Phase 165 edits."""
from __future__ import annotations

from pathlib import Path
import ast
import shutil


def insert_once(text: str, anchor: str, replacement: str, marker: str) -> str:
    if marker in text:
        return text
    if text.count(anchor) != 1:
        raise RuntimeError("Expected exactly one anchor: " + anchor)
    return text.replace(anchor, replacement, 1)


def main() -> None:
    project = Path.cwd()
    source = Path(__file__).resolve().parent / "payload" / "phase165_r12_r11_prop42_unified.py"
    target = project / source.name
    if target.exists() and target.read_bytes() != source.read_bytes():
        raise RuntimeError("Existing unified module differs; will not overwrite")
    shared_path = project / "phase165_r52_r9_shared_math.py"
    citation_path = project / "phase165_r52_r16_web_citation_gate.py"
    shared = shared_path.read_text(encoding="utf8")
    citation = citation_path.read_text(encoding="utf8")
    shared = insert_once(
        shared,
        'sources = (production, build_adopted_typed_reference_registry(adopted_tex),',
        'from phase165_r12_r11_prop42_unified import build_adopted_prop42_general_reference\n'
        '        sources = (production, build_adopted_typed_reference_registry(adopted_tex),',
        'build_adopted_prop42_general_reference',
    )
    shared = insert_once(
        shared,
        'build_adopted_toda51_diagonal_reference(adopted_tex)) + (literature,)',
        'build_adopted_toda51_diagonal_reference(adopted_tex)) + (literature, build_adopted_prop42_general_reference())',
        'literature, build_adopted_prop42_general_reference()',
    )
    shared = insert_once(
        shared,
        'extra_providers = (build_exactness_binding_provider(bridge),) + tuple(extra_providers)',
        'from phase165_r12_r11_prop42_unified import build_prop42_specialization_provider\n'
        '    extra_providers = (build_exactness_binding_provider(bridge), '
        'build_prop42_specialization_provider(bridge)) + tuple(extra_providers)',
        'build_prop42_specialization_provider(bridge)',
    )
    citation = insert_once(
        citation,
        'or ":toda:adopted:prop5.1:finite_dimensional" in assertion.assertion_id',
        'or ":toda:adopted:prop5.1:finite_dimensional" in assertion.assertion_id\n'
        '                or assertion.assertion_id.endswith(":adopted:assertion:prop42:general")',
        'endswith(":adopted:assertion:prop42:general")',
    )
    ast.parse(shared, filename=str(shared_path))
    ast.parse(citation, filename=str(citation_path))
    ast.parse(source.read_text(encoding="utf8"), filename=str(target))
    updates = ((shared_path, shared), (citation_path, citation))
    for path, updated in updates:
        backup = path.with_name(path.name + ".r12_r11.bak")
        if not backup.exists():
            shutil.copy2(path, backup)
        if path.read_text(encoding="utf8") != updated:
            path.write_text(updated, encoding="utf8")
            print("Updated:", path.name)
        else:
            print("Already installed:", path.name)
    shutil.copy2(source, target)
    print("Installed common Proposition 4.2 reference and backward specialization")


if __name__ == "__main__":
    main()
