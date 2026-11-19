"""Install only the full verified reference-body function; preserve file EOL."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

PACKAGE = "phase175_r4r12r13r8r3_verified_reference_body"
TARGET = "phase168_r3_37c_reference_projection.py"
EXPECTED_GIT_BLOB = "3800dc72a2e09808f15b8ee78ae76d4d39c2eede"
FUNCTION = "_verified_source_sentence"


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + result.stderr)
    return result.stdout.strip()


def updated_bytes(original: bytes, replacement: str) -> bytes:
    if not isinstance(original, bytes) or not isinstance(replacement, str):
        raise TypeError("expected bytes and replacement string")
    normalized = original.replace(b"\r\n", b"\n")
    text = normalized.decode("utf-8")
    tree = ast.parse(text)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == FUNCTION]
    if len(matches) != 1:
        raise RuntimeError("FUNCTION_NOT_UNIQUE")
    node = matches[0]
    lines = text.splitlines(keepends=True)
    replace_text = replacement.rstrip("\n") + "\n"
    updated = "".join(lines[:node.lineno-1]) + replace_text + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    if original.count(b"\r\n") and original.count(b"\n") == original.count(b"\r\n"):
        updated = updated.replace("\n", "\r\n")
    return updated.encode("utf-8")


def run(root: Path, dry_run: bool) -> None:
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("BRANCH_MISMATCH")
    file = root / TARGET
    if git(root, "hash-object", TARGET) != EXPECTED_GIT_BLOB:
        raise RuntimeError("SOURCE_BLOB_MISMATCH_NO_WRITE")
    if git(root, "diff", "--name-only", "--", TARGET):
        raise RuntimeError("TRACKED_TARGET_DIRTY_NO_WRITE")
    source = file.read_bytes()
    replacement = (root / PACKAGE / "verified_function_FULL.py").read_text(encoding="utf-8")
    candidate = updated_bytes(source, replacement)
    if candidate == source:
        print("PHASE175_R13R8R3_PATCH_STATUS=ALREADY_APPLIED")
        return
    if dry_run:
        print("PHASE175_R13R8R3_PATCH_STATUS=DRYRUN_VERIFIED")
        return
    file.write_bytes(candidate)
    print("PHASE175_R13R8R3_PATCH_STATUS=INSTALLED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    main()
