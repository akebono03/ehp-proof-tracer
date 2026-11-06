"""Guarded, minimal Phase 174 R3-R7-R14 public source-first wiring.

Only two existing functions change; existing names, APIs, and order stay intact.
This tool never creates a concrete group GIVEN or a dedicated narrative.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase165_r52_r9_shared_math.py")
EXPECTED_BLOB = "0a06dcb0a721e5a79e866cd96909eeeec69303d6"

SOURCE_ANCHOR = (
    "        from phase174_r3_r6_r2_prop44_lemma54.source import (\n"
    "            build_cited_preprop44_splitting,\n"
    "        )\n"
    "        sources = sources + (build_cited_preprop44_splitting(),)\n"
    "    registry = UnifiedStatementRegistry()"
)
SOURCE_REPLACEMENT = (
    "        from phase174_r3_r6_r2_prop44_lemma54.source import (\n"
    "            build_cited_preprop44_splitting,\n"
    "        )\n"
    "        sources = sources + (build_cited_preprop44_splitting(),)\n"
    "        from phase174_r3_r7_r13_cited_annihilator_bridge.registry import (\n"
    "            build_isolated_toda59_annihilator_bridge,\n"
    "        )\n"
    "        sources = sources + (build_isolated_toda59_annihilator_bridge(),)\n"
    "    registry = UnifiedStatementRegistry()"
)
PROVIDER_ANCHOR = (
    "        options.extend(cited_stable_options)\n"
    "        composite_image_options = ()"
)
PROVIDER_REPLACEMENT = (
    "        options.extend(cited_stable_options)\n"
    "        from phase174_r3_r7_r12_toda59_annihilator_source.rule import (\n"
    "            expand_cited_annihilator_specialization,\n"
    "        )\n"
    "        options.extend(expand_cited_annihilator_specialization(goal, tuple(available)))\n"
    "        composite_image_options = ()"
)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def normalized_source(data: bytes) -> tuple[str, bytes, bool]:
    """Reject mixed newline, bare CR and BOM; preserve file-wide CRLF/LF."""
    bom = data.startswith(b"\xef\xbb\xbf")
    raw = data[3:] if bom else data
    if bom:
        raise RuntimeError("Unexpected BOM in shared math source")
    if b"\r\n" in raw:
        if b"\r" in raw.replace(b"\r\n", b"") or b"\n" in raw.replace(b"\r\n", b""):
            raise RuntimeError("Mixed or bare-CR line endings")
        newline = b"\r\n"
    else:
        if b"\r" in raw:
            raise RuntimeError("Bare-CR line endings")
        newline = b"\n"
    normalized = raw.replace(b"\r\n", b"\n")
    if git_blob_sha(normalized) != EXPECTED_BLOB:
        raise RuntimeError("Pinned shared math source differs")
    return normalized.decode("utf-8"), newline, bom


def transform_source(source: str) -> str:
    """Patch two exact, singular anchors; never silently accept a second match."""
    for anchor, replacement in (
        (SOURCE_ANCHOR, SOURCE_REPLACEMENT),
        (PROVIDER_ANCHOR, PROVIDER_REPLACEMENT),
    ):
        if source.count(anchor) != 1 or replacement in source:
            raise RuntimeError("Expected exactly one unpatched source anchor")
        source = source.replace(anchor, replacement, 1)
    compile(source, str(TARGET), "exec")
    return source


def expected_patched_bytes(source_bytes: bytes) -> bytes:
    original, newline, _ = normalized_source(source_bytes)
    patched = transform_source(original).encode("utf-8")
    return patched.replace(b"\n", newline)


def read_target(root: Path = ROOT) -> tuple[bytes, bytes]:
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("Missing shared math source")
    original = path.read_bytes()
    return original, expected_patched_bytes(original)


def apply_guarded_patch(root: Path = ROOT, *, dry_run: bool = False) -> dict[str, str]:
    """Only after caller verifies HEAD and other source files."""
    original, new_bytes = read_target(root)
    result = {
        "target": str(TARGET),
        "original_sha": git_blob_sha(original.replace(b"\r\n", b"\n")),
        "patched_sha": git_blob_sha(new_bytes.replace(b"\r\n", b"\n")),
    }
    if dry_run:
        return result
    audit_root = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    backup_dir = audit_root / "EHPProofTracerAudit" / "phase174_r3_r7_r14"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / "phase165_r52_r9_shared_math.original.py"
    if backup.exists() and backup.read_bytes() != original:
        raise RuntimeError("Existing guarded backup does not match source")
    backup.write_bytes(original)
    (root / TARGET).write_bytes(new_bytes)
    if (root / TARGET).read_bytes() != new_bytes:
        (root / TARGET).write_bytes(original)
        raise RuntimeError("Post-write verification failed")
    result["backup"] = str(backup)
    return result


def export_modified_functions(
    root: Path = ROOT, *, dry_run: bool = False,
) -> Path:
    """Output complete replacement bodies, including during non-writing DryRun."""
    import ast

    path = root / TARGET
    src = (
        transform_source(normalized_source(path.read_bytes())[0])
        if dry_run else path.read_text(encoding="utf-8-sig")
    )
    tree = ast.parse(src)
    lines = src.splitlines()
    functions = {
        node.name: node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    names = ("build_shared_typed_bridge", "shared_expansion_provider")
    if any(name not in functions for name in names):
        raise RuntimeError("Expected complete function definitions missing")
    out = root / "phase174_r3_r7_r14_public_annihilator_connection" / "MODIFIED_FUNCTIONS_FULL_JA.md"
    sections = ["# R14 置換後の既存関数全文", "", "次の2関数は現在のソースから全文抽出したものです。", ""]
    for name in names:
        node = functions[name]
        sections += [f"## `{name}`", "", "```python", "\n".join(lines[node.lineno-1:node.end_lineno]), "```", ""]
    out.write_text("\n".join(sections), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = apply_guarded_patch(dry_run=args.dry_run)
    print("PHASE174_R3R7R14_PATCH_TARGET=" + result["target"])
    print("PHASE174_R3R7R14_PATCHED_SHA=" + result["patched_sha"])
    if not args.dry_run:
        print("PHASE174_R3R7R14_SOURCE_BACKUP=" + result["backup"])
    print("PHASE174_R3R7R14_FULL_REPLACEMENT_FUNCTIONS=" + str(
        export_modified_functions(dry_run=args.dry_run)
    ))
    print("PHASE174_R3R7R14_PATCH_GATE=" + ("PASS_DRYRUN" if args.dry_run else "PASS_APPLIED"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
