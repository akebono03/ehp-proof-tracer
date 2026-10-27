"""R10E8-R2 guarded CRLF adapter around the UNCHANGED R10E8 transform.

No family rule, source record, search logic or citation semantics change here.
The existing transform still requires exact source anchors and parses both
fully transformed Python modules before any working-tree file is written.
"""
from __future__ import annotations

from pathlib import Path

from phase169_r10e8_hyoujigen_generic_suspension import patch as original
from phase169_r10e8r2_crlf_safe_patch.newline_support import (
    decode_working_source,
    encode_working_source,
)


def apply_guarded_crlf_patch() -> None:
    """Transform both reviewed source files while preserving each newline style."""
    paths = (original.FAMILY, original.SHARED)
    original_bytes = tuple(path.read_bytes() for path in paths)
    family_text, family_style = decode_working_source(paths[0], original_bytes[0])
    shared_text, shared_style = decode_working_source(paths[1], original_bytes[1])
    family_updated, shared_updated = original.transformed_sources(
        family_text, shared_text,
    )
    updated_bytes = (
        encode_working_source(family_updated, family_style),
        encode_working_source(shared_updated, shared_style),
    )
    original.OUTPUT.mkdir(parents=True, exist_ok=True)
    first_import = family_updated.index("from __future__ import annotations")
    last_import = family_updated.index("\n\nROOT =")
    output_files = (
        ("phase169_r10d2_general_family_definition__family_citation.py.FULL", family_updated),
        ("phase165_r52_r9_shared_math.py.FULL", shared_updated),
        ("family_citation_IMPORTS_FULL.py", family_updated[first_import:last_import] + "\n"),
        ("canonical_member_FULL.py", original._extract_function(family_updated, "canonical_member")),
        ("cited_family_reference_sentence_FULL.py", original._extract_function(
            family_updated, "cited_family_reference_sentence",
        )),
        ("build_shared_typed_bridge_FULL.py", original._extract_function(
            shared_updated, "build_shared_typed_bridge",
        )),
    )
    try:
        for path, content in zip(paths, updated_bytes):
            path.write_bytes(content)
        for name, text in output_files:
            (original.OUTPUT / name).write_bytes(text.encode("utf-8"))
    except Exception:
        for path, content in zip(paths, original_bytes):
            path.write_bytes(content)
        raise
    for path, style in zip(paths, (family_style, shared_style)):
        print("R10E8R2_PATCHED=" + str(path))
        print("R10E8R2_NEWLINE=" + path.name + "=" + (
            "CRLF" if style == "\r\n" else "LF"
        ))
    print("R10E8R2_FULL_FUNCTIONS=" + str(original.OUTPUT))


def main() -> None:
    apply_guarded_crlf_patch()


if __name__ == "__main__":
    main()
