"""Guarded single-function provider hook, preserving all unrelated bytes."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
REVIEWED_BLOB = "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"
ORIGINAL = "        return retain_ordered_root_expansions(proof_target, goal, merged)"
REPLACEMENT = """        from phase171_r2j_r4_r9_r20_eta_route_precedence.source import (
            prefer_specific_cited_eta_specialization,
        )
        preferred = prefer_specific_cited_eta_specialization(
            goal, tuple(available), merged,
        )
        return retain_ordered_root_expansions(proof_target, goal, preferred)"""


def git_read(*args: str) -> bytes:
    """Read-only Git access, never checkout, reset, pull, or stage."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("show", "HEAD:phase165_r52_r9_shared_math.py"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if args not in allowed:
        raise ValueError("mutating Git commands are not allowed")
    return subprocess.run(["git", *args], cwd=ROOT,
                          check=True, capture_output=True).stdout


def blob_sha(data: bytes) -> str:
    """Calculate the SHA-1 of a committed Git blob without writing files."""
    return hashlib.sha1(("blob %d\0" % len(data)).encode("ascii") + data).hexdigest()


def source_function(source: str, name: str = "shared_expansion_provider") -> str:
    """Extract the *complete* function via AST, without truncation."""
    tree = ast.parse(source)
    selected = [item for item in tree.body
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                and item.name == name]
    if len(selected) != 1:
        raise RuntimeError("expected one complete shared provider definition")
    node = selected[0]
    return "\n".join(source.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def patch_text(original: str) -> str:
    """Only change the reviewed final return of the common provider."""
    if original.count(REPLACEMENT) == 1:
        source_function(original)
        return original
    if original.count(ORIGINAL) != 1:
        raise RuntimeError("reviewed provider return anchor is not unique")
    altered = original.replace(ORIGINAL, REPLACEMENT, 1)
    ast.parse(altered)
    before = source_function(original)
    after = source_function(altered)
    if before == after:
        raise RuntimeError("provider function was not updated")
    if altered.replace(REPLACEMENT, ORIGINAL, 1) != original:
        raise RuntimeError("nonlocal source modification detected")
    return altered


def preflight() -> dict[str, str]:
    branch = git_read("branch", "--show-current").decode("utf-8").strip()
    head = git_read("rev-parse", "HEAD").decode("utf-8").strip()
    committed = git_read("show", "HEAD:phase165_r52_r9_shared_math.py")
    if branch != "develop":
        raise RuntimeError("R20 requires develop")
    if blob_sha(committed) != REVIEWED_BLOB:
        raise RuntimeError("HEAD provider differs from the reviewed R19/R11 baseline")
    local = TARGET.read_bytes()
    newline = "\r\n" if b"\r\n" in local else "\n"
    current = local.decode("utf-8-sig").replace("\r\n", "\n")
    expected = committed.decode("utf-8-sig").replace("\r\n", "\n")
    if current != expected and current != patch_text(expected):
        raise RuntimeError("working provider differs from HEAD and the R20 patch")
    return {"branch": branch, "head": head, "newline": newline}


def install(*, dry_run: bool = False) -> bool:
    """Apply one guarded patch; always write full-function evidence on success."""
    ready = preflight()
    before = TARGET.read_bytes()
    original = before.decode("utf-8-sig").replace("\r\n", "\n")
    after = patch_text(original)
    output = PACKAGE / "output"
    print("PHASE171_R20_BRANCH=" + ready["branch"], flush=True)
    print("PHASE171_R20_HEAD=" + ready["head"], flush=True)
    print("PHASE171_R20_REVIEWED_PROVIDER=PASS", flush=True)
    if dry_run:
        print("PHASE171_R20_RESULT=PASS_DRY_RUN", flush=True)
        return False
    output.mkdir(exist_ok=True)
    (output / "FULL_SHARED_PROVIDER_BEFORE.py").write_text(
        source_function(original), encoding="utf-8")
    (output / "FULL_SHARED_PROVIDER_AFTER.py").write_text(
        source_function(after), encoding="utf-8")
    (output / "BACKUP_phase165_r52_r9_shared_math.py").write_bytes(before)
    changed = after != original
    if changed:
        target_bytes = after.replace("\n", ready["newline"]).encode("utf-8")
        if before.startswith(b"\xef\xbb\xbf"):
            target_bytes = b"\xef\xbb\xbf" + target_bytes
        TARGET.write_bytes(target_bytes)
    print("PHASE171_R20_PATCHED=" + str(changed), flush=True)
    print("PHASE171_R20_FULL_FUNCTION=" + str(output / "FULL_SHARED_PROVIDER_AFTER.py"), flush=True)
    print("PHASE171_R20_BACKUP=" + str(output / "BACKUP_phase165_r52_r9_shared_math.py"), flush=True)
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
