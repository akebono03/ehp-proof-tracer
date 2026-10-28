"""Minimal guarded full-function replacements; backup and rollback are caller-owned."""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FILE_CITATION = "phase169_r10d2_general_family_definition/family_citation.py"
FILE_SHARED = "phase165_r52_r9_shared_math.py"
EXPECTED_BLOBS = {
    FILE_CITATION: "91587dcd19c96a7bd069a2e009b70c2e5aa9b378",
    FILE_SHARED: "d015e11030a15a62fbe75099bda10ddacdfdcbc5",
}
_INSERT_ANCHOR = (
    "        sources = sources + (\n"
    "            build_cited_stable_family_definitions(),\n"
    "            build_cited_chapter_vi_family_definitions(),\n"
    "        )\n"
)
_INSERT_NEW = (
    "        from phase169_r10eo_r3_reviewed_definition_bridge.reviewed_definitions import (\n"
    "            build_cited_reviewed_definitions,\n"
    "        )\n"
    "        sources = sources + (build_cited_reviewed_definitions(),)\n"
)


def current_blob(path: str) -> str:
    """Inspect the tracked Git blob; avoid CRLF-dependent working-file hashes."""
    clean = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", path], cwd=ROOT,
        check=False,
    )
    if clean.returncode != 0:
        raise RuntimeError(f"R10EO R3 refuses edited source: {path}")
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True,
    ).strip()


def verify_baseline() -> None:
    for path, blob in EXPECTED_BLOBS.items():
        if current_blob(path) != blob:
            raise RuntimeError(f"R10EO R3 source changed: {path}")


def function_span(source: str, name: str) -> tuple[int, int]:
    module = ast.parse(source)
    found = [item for item in module.body
             if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
             and item.name == name]
    if len(found) != 1:
        raise RuntimeError(f"expected exactly one function: {name}")
    node = found[0]
    lines = source.splitlines(keepends=True)
    return (sum(len(item) for item in lines[:node.lineno - 1]),
            sum(len(item) for item in lines[:node.end_lineno]))


def replace_complete_function(source: str, name: str, replacement: str) -> str:
    start, end = function_span(source, name)
    if not replacement.endswith("\n"):
        raise RuntimeError("replacement must have a final newline")
    return source[:start] + replacement + source[end:]


def build_replacements() -> tuple[dict[str, bytes], dict[str, str]]:
    verify_baseline()
    before_citation = (ROOT / FILE_CITATION).read_bytes()
    before_shared = (ROOT / FILE_SHARED).read_bytes()
    newline_citation = "\r\n" if b"\r\n" in before_citation else "\n"
    newline_shared = "\r\n" if b"\r\n" in before_shared else "\n"
    citation = before_citation.decode("utf-8-sig").replace("\r\n", "\n")
    shared = before_shared.decode("utf-8-sig").replace("\r\n", "\n")
    canonical = (HERE / "full_functions" / "canonical_member.py").read_text(encoding="utf-8")
    reference = (HERE / "full_functions" / "cited_family_reference_sentence.py").read_text(encoding="utf-8")
    citation = replace_complete_function(citation, "canonical_member", canonical)
    citation = replace_complete_function(citation, "cited_family_reference_sentence", reference)
    if shared.count(_INSERT_ANCHOR) != 1 or _INSERT_NEW in shared:
        raise RuntimeError("R10EO R3 shared bridge anchor changed")
    bridge_start, bridge_end = function_span(shared, "build_shared_typed_bridge")
    full_bridge = shared[bridge_start:bridge_end]
    if full_bridge.count(_INSERT_ANCHOR) != 1:
        raise RuntimeError("R10EO R3 bridge anchor out of function")
    expected_bridge = full_bridge.replace(_INSERT_ANCHOR, _INSERT_ANCHOR + _INSERT_NEW)
    full_bridge = (HERE / "full_functions" / "build_shared_typed_bridge.py").read_text(encoding="utf-8")
    if expected_bridge.strip() != full_bridge.strip():
        raise RuntimeError("reviewed full bridge function and upstream source disagree")
    shared = replace_complete_function(shared, "build_shared_typed_bridge", full_bridge)
    ast.parse(citation)
    ast.parse(shared)
    files = {
        FILE_CITATION: citation.replace("\n", newline_citation).encode("utf-8"),
        FILE_SHARED: shared.replace("\n", newline_shared).encode("utf-8"),
    }
    full_functions = {
        "canonical_member.py": canonical,
        "cited_family_reference_sentence.py": reference,
        "build_shared_typed_bridge.py": full_bridge,
    }
    return files, full_functions


def main() -> None:
    files, functions = build_replacements()
    backups = {}
    try:
        for path, replacement in files.items():
            target = ROOT / path
            backups[path] = target.read_bytes()
            target.write_bytes(replacement)
            print("R10EO_R3_PATCHED=" + path)
        output = HERE / "output" / "full_functions"
        output.mkdir(parents=True, exist_ok=True)
        for name, content in functions.items():
            (output / name).write_text(content, encoding="utf-8")
        for path in files:
            if (ROOT / path).read_bytes() != files[path]:
                raise RuntimeError("post-write integrity failure")
    except Exception:
        for path, original in backups.items():
            (ROOT / path).write_bytes(original)
        raise


if __name__ == "__main__":
    main()
