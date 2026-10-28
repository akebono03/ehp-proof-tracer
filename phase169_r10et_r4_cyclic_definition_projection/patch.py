"""Fail-closed two-function patch; export complete functions and full files."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
PROJECTOR = "phase169_r10a_verified_stable_chain_projection/projection.py"
RENDERER = "phase168_r3_5_model_renderer.py"
EXPECTED_GIT_BLOBS = {
    PROJECTOR: "2a230bbab4a7c670ed4bc297ab9683e9faaa0451",
    RENDERER: "2685ef3ef6bf7bc1673dededef1e3487d9941362",
}

PROJECTOR_OLD = '''    from phase169_r10en_shared_citation_provenance.core import (
        verified_generator_image_citation_numbers,
    )
    citation_numbers = verified_generator_image_citation_numbers(
        model, order, images, require_each=False,
    )'''
PROJECTOR_NEW = '''    from phase169_r10et_r4_cyclic_definition_projection.policy import (
        verified_cyclic_generator_image_citation_numbers,
    )
    citation_numbers = verified_cyclic_generator_image_citation_numbers(
        model, order, images,
    )'''
RENDER_IMPORT_OLD = '''    from phase169_r10a_verified_stable_chain_projection.projection import (
        project_verified_stable_image_chain,
    )'''
RENDER_IMPORT_NEW = '''    from phase169_r10a_verified_stable_chain_projection.projection import (
        VerifiedStableImageChainDisplay,
        project_verified_stable_image_chain,
    )'''
RENDER_LINE_OLD = '''            lines.extend((f"{source_tags}より, {compressed_statement}.", ""))'''
RENDER_LINE_NEW = '''            if source_tags:
                prefix = f"{source_tags}より, "
            elif isinstance(stable_chain_display, VerifiedStableImageChainDisplay):
                prefix = "Definition より, "
            else:
                prefix = ""
            lines.extend((f"{prefix}{compressed_statement}.", ""))'''


def git_blob_sha1(blob: bytes) -> str:
    return hashlib.sha1(f"blob {len(blob)}\0".encode("ascii") + blob).hexdigest()


def function_source(source: str, name: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one top-level function: {name}")
    node = matches[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def transformed(source: bytes, target: str) -> tuple[bytes, str]:
    if target not in EXPECTED_GIT_BLOBS:
        raise RuntimeError(f"unreviewed patch target: {target}")
    if git_blob_sha1(source) != EXPECTED_GIT_BLOBS[target]:
        raise RuntimeError(f"{target}: source Git blob differs from reviewed version")
    newline = "\r\n" if b"\r\n" in source else "\n"
    normalized = source.decode("utf-8").replace("\r\n", "\n")
    function = ("project_verified_stable_image_chain" if target == PROJECTOR
                else "render_model_backed_narrative_markdown")
    before_function = function_source(normalized, function)
    replacements = ((PROJECTOR_OLD, PROJECTOR_NEW),) if target == PROJECTOR else (
        (RENDER_IMPORT_OLD, RENDER_IMPORT_NEW),
        (RENDER_LINE_OLD, RENDER_LINE_NEW),
    )
    after_function = before_function
    for old, new in replacements:
        if after_function.count(old) != 1 or new in after_function:
            raise RuntimeError(f"{target}: expected unique patch anchor absent")
        after_function = after_function.replace(old, new)
    if normalized.count(before_function) != 1:
        raise RuntimeError(f"{target}: full function not unique")
    updated = normalized.replace(before_function, after_function)
    ast.parse(updated)
    if function_source(updated, function) != after_function:
        raise RuntimeError(f"{target}: full function export mismatch")
    return updated.replace("\n", newline).encode("utf-8"), after_function


def prepare(root: Path, output: Path) -> dict[str, tuple[bytes, bytes]]:
    """Validate *both* files before writing either one; output complete source."""
    prepared: dict[str, tuple[bytes, bytes]] = {}
    output.mkdir(parents=True, exist_ok=False)
    for path in (PROJECTOR, RENDERER):
        original = (root / path).read_bytes()
        revised, complete_function = transformed(original, path)
        prepared[path] = original, revised
        name = Path(path).stem
        (output / f"{name}.before").write_bytes(original)
        (output / f"{name}.FULL").write_bytes(revised)
        (output / f"{name}.changed_function.FULL.py").write_text(
            complete_function, encoding="utf-8",
        )
    return prepared


def apply(root: Path, prepared: dict[str, tuple[bytes, bytes]]) -> None:
    written = []
    try:
        for path, (old, new) in prepared.items():
            if (root / path).read_bytes() != old:
                raise RuntimeError(f"{path}: file changed during preparation")
            (root / path).write_bytes(new)
            written.append(path)
    except Exception:
        for path in written:
            (root / path).write_bytes(prepared[path][0])
        raise


def restore(root: Path, prepared: dict[str, tuple[bytes, bytes]]) -> None:
    for path, (old, _) in prepared.items():
        (root / path).write_bytes(old)
