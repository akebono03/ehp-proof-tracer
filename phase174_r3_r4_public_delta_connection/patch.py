"""Minimal source-guarded, whole-function integration of the R3-R3 rule.

Only shared_expansion_provider() is modified. The top-level import block stays
unchanged, and the new import is local to the existing nested expand function.
No group-specific dispatch, citation alteration, narrative branch or GIVEN.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

EXPECTED_SOURCE_SHA = "f49b0b7699e29ec1b78d73578dc66a0e33d6e336"
SOURCE_PATH = "phase165_r52_r9_shared_math.py"
OLD_CONTEXT = (
    "        options.extend(expand_cited_ehp_surjectivity_consequences(goal))\n"
    "        options.extend(expand_finite_cyclic_relation(goal))\n"
)
NEW_CONTEXT = (
    "        options.extend(expand_cited_ehp_surjectivity_consequences(goal))\n"
    "        from phase174_r3_r3_injective_delta_zero.rule import expand_delta_zero_from_injection\n"
    "        options.extend(expand_delta_zero_from_injection(goal))\n"
    "        options.extend(expand_finite_cyclic_relation(goal))\n"
)


def git_blob_sha(content: bytes) -> str:
    """Compute git's blob identity, not a plain SHA1 of the file content."""
    framed = b"blob " + str(len(content)).encode("ascii") + b"\x00" + content
    return hashlib.sha1(framed).hexdigest()


def replace_provider_call(source: bytes) -> bytes:
    """Produce a whole-file replacement with exactly one reviewed modification."""
    newline = b"\r\n" if b"\r\n" in source else b"\n"
    old = OLD_CONTEXT.encode("utf-8").replace(b"\n", newline)
    new = NEW_CONTEXT.encode("utf-8").replace(b"\n", newline)
    if source.count(new) == 1 and source.count(old) == 0:
        return source
    if source.count(old) != 1 or source.count(new) != 0:
        raise ValueError("The reviewed shared-expansion insertion point is absent or ambiguous")
    updated = source.replace(old, new)
    if len(updated) - len(source) != len(new) - len(old):
        raise ValueError("Unexpected edit size")
    ast.parse(updated.decode("utf-8-sig"))
    return updated


def extract_full_function(source: bytes) -> str:
    """Return the entire changed function for direct copy/review."""
    parsed = ast.parse(source.decode("utf-8-sig"))
    matches = [
        node for node in parsed.body
        if isinstance(node, ast.FunctionDef) and node.name == "shared_expansion_provider"
    ]
    if len(matches) != 1:
        raise ValueError("No unique shared_expansion_provider function in the source")
    lines = source.decode("utf-8-sig").splitlines(keepends=True)
    node = matches[0]
    full = "".join(lines[node.lineno - 1:node.end_lineno])
    if "options.extend(expand_delta_zero_from_injection(goal))" not in full:
        raise ValueError("Full function extraction lacks the reviewed new rule")
    return full.replace("\r\n", "\n").rstrip("\n") + "\n"


def git(*args: str) -> bytes:
    result = subprocess.run(("git",) + args, check=True, capture_output=True)
    return result.stdout


def reviewed_head_bytes() -> bytes:
    """Read only the local commit's actual file, without changing Git state."""
    raw = git("show", "HEAD:" + SOURCE_PATH)
    if git_blob_sha(raw) != EXPECTED_SOURCE_SHA:
        raise ValueError("Reviewed committed source is not present at HEAD")
    return raw


def ensure_expected_input(current: bytes, expected: bytes, changed: bytes) -> str:
    if current == expected:
        return "ORIGINAL_REVIEWED"
    if current == changed:
        return "ALREADY_INSTALLED"
    raise ValueError("Refusing to overwrite user-modified shared source")


def apply(root: Path, *, dry_run: bool) -> dict[str, object]:
    source = root / SOURCE_PATH
    original = reviewed_head_bytes()
    modified = replace_provider_call(original)
    if modified == original:
        raise ValueError("No reviewed change was produced")
    status = ensure_expected_input(source.read_bytes(), original, modified)
    indexed = git("diff", "--cached", "--name-only", "--", SOURCE_PATH).strip()
    if indexed:
        raise ValueError("Refusing to change a staged source file")
    if not dry_run and status == "ORIGINAL_REVIEWED":
        source.write_bytes(modified)
    if not dry_run and source.read_bytes() != modified:
        raise ValueError("The installed file does not match the reviewed transformation")
    if not dry_run:
        folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
        folder = folder / "EHPProofTracerAudit" / "phase174_r3_r4"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "shared_expansion_provider_FULL.py").write_text(
            extract_full_function(modified), encoding="utf-8",
        )
    return {
        "state_before": status,
        "dry_run": dry_run,
        "old_git_blob": EXPECTED_SOURCE_SHA,
        "new_git_blob": git_blob_sha(modified),
        "whole_function_lines": len(extract_full_function(modified).splitlines()),
        "production_source_changed": not dry_run and status == "ORIGINAL_REVIEWED",
        "only_existing_function_modified": True,
        "top_level_import_section_unchanged": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = apply(Path.cwd(), dry_run=args.dry_run)
    print("PHASE174_R3R4_PATCH_STATE=" + str(result["state_before"]))
    print("PHASE174_R3R4_SOURCE_GUARD=PASS")
    print("PHASE174_R3R4_UPDATED_BLOB=" + str(result["new_git_blob"]))
    print("PHASE174_R3R4_FULL_FUNCTION_LINES=" + str(result["whole_function_lines"]))
    print("PHASE174_R3R4_TOP_IMPORTS_UNCHANGED=True")
    if args.dry_run:
        print("PHASE174_R3R4_DRY_RUN=PASS")
        print("PHASE174_R3R4_NO_FILES_CHANGED=True")
    else:
        print("PHASE174_R3R4_PUBLIC_PROVIDER_CONNECTED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
