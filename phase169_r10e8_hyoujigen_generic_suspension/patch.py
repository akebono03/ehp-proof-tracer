"""Guarded, minimal replacement of complete functions and one import section.

Run from the project root. The historical R10D2 API remains Chapter V-only;
R10E8's new Chapter VI source bridge is an independent append-only source.
"""
from __future__ import annotations

import ast
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FAMILY = ROOT / "phase169_r10d2_general_family_definition" / "family_citation.py"
SHARED = ROOT / "phase165_r52_r9_shared_math.py"
OUTPUT = HERE / "output"

IMPORT_INSERT_AT = "from proof import (\n"
NEW_IMPORT = (
    "from phase169_r10e8_hyoujigen_generic_suspension.source_records import (\n"
    "    CHAPTER_VI_SOURCE_RECORDS,\n"
    ")\n"
)
OLD_MEMBER = "source.family_id not in {record.family_id for record in SOURCE_RECORDS}"
NEW_MEMBER = (
    "source.family_id not in {record.family_id for record in "
    "SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS}"
)
OLD_SHARED = "        sources = sources + (build_cited_stable_family_definitions(),)"
NEW_SHARED = "\n".join((
    "        from phase169_r10e8_hyoujigen_generic_suspension.chapter_vi_reference import (",
    "            build_cited_chapter_vi_family_definitions,",
    "        )",
    "        sources = sources + (",
    "            build_cited_stable_family_definitions(),",
    "            build_cited_chapter_vi_family_definitions(),",
    "        )",
))


def _replace_once(source: str, before: str, after: str, count: int = 1) -> str:
    if source.count(before) != count or after in source:
        raise RuntimeError(f"source guard failed: {before[:64]}")
    return source.replace(before, after)


def transformed_sources(family_source: str, shared_source: str) -> tuple[str, str]:
    """Fail closed on source drift and return full replacement file contents."""
    if family_source.count(OLD_MEMBER) != 2:
        raise RuntimeError("R10D2 family guard changed")
    family_updated = _replace_once(family_source, IMPORT_INSERT_AT,
                                   NEW_IMPORT + IMPORT_INSERT_AT)
    family_updated = _replace_once(family_updated, OLD_MEMBER, NEW_MEMBER, 2)
    shared_updated = _replace_once(shared_source, OLD_SHARED, NEW_SHARED)
    ast.parse(family_updated, filename=str(FAMILY))
    ast.parse(shared_updated, filename=str(SHARED))
    return family_updated, shared_updated


def _extract_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    matches = tuple(node for node in tree.body
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and node.name == name)
    if len(matches) != 1:
        raise RuntimeError(f"function not uniquely found: {name}")
    lines = source.splitlines(keepends=True)
    node = matches[0]
    return "".join(lines[node.lineno - 1:node.end_lineno]) + "\n"


def main() -> None:
    """Apply entire-file replacements and save all changed functions/imports."""
    before_family = FAMILY.read_bytes()
    before_shared = SHARED.read_bytes()
    for path, data in ((FAMILY, before_family), (SHARED, before_shared)):
        if b"\r\n" in data:
            raise RuntimeError(f"expected LF working source: {path}")
    family_updated, shared_updated = transformed_sources(
        before_family.decode("utf-8"), before_shared.decode("utf-8"),
    )
    if not OUTPUT.exists():
        OUTPUT.mkdir(parents=True)
    import_section = family_updated.split("\n\n", 2)
    first_import = family_updated.index("from __future__ import annotations")
    last_import = family_updated.index("\n\nROOT =")
    changed = (
        (FAMILY, family_updated, "phase169_r10d2_general_family_definition__family_citation.py"),
        (SHARED, shared_updated, "phase165_r52_r9_shared_math.py"),
    )
    try:
        for path, value, output_name in changed:
            path.write_bytes(value.encode("utf-8"))
            (OUTPUT / (output_name + ".FULL")).write_text(value, encoding="utf-8")
        (OUTPUT / "family_citation_IMPORTS_FULL.py").write_text(
            family_updated[first_import:last_import] + "\n", encoding="utf-8",
        )
        for function in ("canonical_member", "cited_family_reference_sentence"):
            (OUTPUT / (function + "_FULL.py")).write_text(
                _extract_function(family_updated, function), encoding="utf-8",
            )
        (OUTPUT / "build_shared_typed_bridge_FULL.py").write_text(
            _extract_function(shared_updated, "build_shared_typed_bridge"),
            encoding="utf-8",
        )
    except Exception:
        FAMILY.write_bytes(before_family)
        SHARED.write_bytes(before_shared)
        raise
    print("R10E8_PATCHED=" + str(FAMILY))
    print("R10E8_PATCHED=" + str(SHARED))
    print("R10E8_FULL_FUNCTIONS=" + str(OUTPUT))


if __name__ == "__main__":
    main()
