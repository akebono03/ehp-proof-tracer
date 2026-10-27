"""Fix R10E8's two distinct member guards, preserving source newline bytes.

Only the guard in the R10E8 patcher was incorrect. This adapter leaves the
original patch.py, mathematical rule engine, and existing tests unchanged.
"""
from __future__ import annotations

import ast
from pathlib import Path

from phase169_r10e8_hyoujigen_generic_suspension import patch as original
from phase169_r10e8r2_crlf_safe_patch.newline_support import (
    decode_working_source,
    encode_working_source,
)


OLD_REFERENCE = (
    "statement.family_id not in {record.family_id for record in SOURCE_RECORDS}"
)
NEW_REFERENCE = (
    "statement.family_id not in {record.family_id for record in "
    "SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS}"
)


def _function_body(source: str, function_name: str) -> str:
    """Retrieve one entire module-level function for exact guard validation."""
    module = ast.parse(source)
    functions = tuple(node for node in module.body
                      if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                      and node.name == function_name)
    if len(functions) != 1:
        raise RuntimeError("R10E8R3 expected exactly one " + function_name)
    return ast.get_source_segment(source, functions[0]) or ""


def transformed_sources_r3(family_source: str, shared_source: str) -> tuple[str, str]:
    """Apply exact two-function R10D2 guards and the original R10E8 wiring.

    This transform is textual only within three already-reviewed functions.
    Reject source drift, duplicate anchors, or already-applied changes.
    """
    if (family_source.count(original.OLD_MEMBER) != 1
            or family_source.count(OLD_REFERENCE) != 1
            or _function_body(family_source, "canonical_member").count(
                original.OLD_MEMBER) != 1
            or _function_body(family_source, "cited_family_reference_sentence").count(
                OLD_REFERENCE) != 1):
        raise RuntimeError("R10E8R3 distinct family guards changed")
    family_updated = original._replace_once(
        family_source, original.IMPORT_INSERT_AT,
        original.NEW_IMPORT + original.IMPORT_INSERT_AT,
    )
    family_updated = original._replace_once(
        family_updated, original.OLD_MEMBER, original.NEW_MEMBER,
    )
    family_updated = original._replace_once(
        family_updated, OLD_REFERENCE, NEW_REFERENCE,
    )
    shared_updated = original._replace_once(
        shared_source, original.OLD_SHARED, original.NEW_SHARED,
    )
    # Parse both entire outputs and demand the expected three public functions.
    ast.parse(family_updated, filename=str(original.FAMILY))
    ast.parse(shared_updated, filename=str(original.SHARED))
    _function_body(family_updated, "canonical_member")
    _function_body(family_updated, "cited_family_reference_sentence")
    _function_body(shared_updated, "build_shared_typed_bridge")
    return family_updated, shared_updated


def apply_guarded_r3_patch() -> None:
    """Patch reviewed production files, preserving their individual LF/CRLF style.

    Both transformed contents and the full-function output artifacts are
    prepared before any production write. Any error restores original bytes.
    """
    paths = (original.FAMILY, original.SHARED)
    before = tuple(path.read_bytes() for path in paths)
    family, family_style = decode_working_source(paths[0], before[0])
    shared, shared_style = decode_working_source(paths[1], before[1])
    transformed_family, transformed_shared = transformed_sources_r3(
        family, shared,
    )
    changed_bytes = (
        encode_working_source(transformed_family, family_style),
        encode_working_source(transformed_shared, shared_style),
    )
    first_import = transformed_family.index("from __future__ import annotations")
    last_import = transformed_family.index("\n\nROOT =")
    output_files = (
        ("phase169_r10d2_general_family_definition__family_citation.py.FULL",
         transformed_family),
        ("phase165_r52_r9_shared_math.py.FULL", transformed_shared),
        ("family_citation_IMPORTS_FULL.py",
         transformed_family[first_import:last_import] + "\n"),
        ("canonical_member_FULL.py", original._extract_function(
            transformed_family, "canonical_member")),
        ("cited_family_reference_sentence_FULL.py", original._extract_function(
            transformed_family, "cited_family_reference_sentence")),
        ("build_shared_typed_bridge_FULL.py", original._extract_function(
            transformed_shared, "build_shared_typed_bridge")),
    )
    original.OUTPUT.mkdir(parents=True, exist_ok=True)
    try:
        for path, content in zip(paths, changed_bytes):
            path.write_bytes(content)
        for name, source in output_files:
            (original.OUTPUT / name).write_bytes(source.encode("utf-8"))
    except Exception:
        for path, content in zip(paths, before):
            path.write_bytes(content)
        raise
    for path, style in zip(paths, (family_style, shared_style)):
        print("R10E8R3_PATCHED=" + str(path))
        print("R10E8R3_NEWLINE=" + path.name + "=" + (
            "CRLF" if style == "\r\n" else "LF"
        ))
    print("R10E8R3_FULL_FUNCTIONS=" + str(original.OUTPUT))


def main() -> None:
    apply_guarded_r3_patch()


if __name__ == "__main__":
    main()
