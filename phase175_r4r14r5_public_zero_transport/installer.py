"""Guarded minimal insertion of the shared provider; no full-file rewrites."""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

TARGET = "phase165_r52_r9_shared_math.py"
EXPECTED_BLOB = "f5329594a8298af34cd05932bf4a7b6c59d6e4de"
ANCHOR = "    # R41: retain DB-prior provenance and the actual cited source boundary."
INSERTION = (
    "    # Phase 175 R4R14R5: source-screened composite-value zero transport.\n"
    "    # Each premise is still proved by the shared source-first DFS.\n"
    "    from phase175_r4r14r5_public_zero_transport.provider import (\n"
    "        build_public_composite_zero_transport_provider,\n"
    "    )\n"
    "    extra_providers = (\n"
    "        build_public_composite_zero_transport_provider(bridge),\n"
    "    ) + tuple(extra_providers)\n"
)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, text=True, encoding="utf-8",
        capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("GIT_FAILED " + " ".join(args) + " " + result.stderr.strip())
    return result.stdout.strip()


def expected_updated_source(data: str) -> str:
    if data.count(ANCHOR) != 1 or INSERTION in data:
        raise RuntimeError("SHARED_PROVIDER_ANCHOR_CHANGED")
    updated = data.replace(ANCHOR, INSERTION + ANCHOR)
    tree = ast.parse(updated)
    fun = [node for node in tree.body
           if isinstance(node, ast.FunctionDef)
           and node.name == "shared_expansion_provider"]
    if len(fun) != 1:
        raise RuntimeError("SHARED_PROVIDER_FUNCTION_CHANGED")
    return updated


def verify_and_apply(root: Path, *, dry_run: bool) -> str:
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("REPOSITORY_ROOT_REQUIRED")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_CHANGES_REQUIRE_REVIEW")
    if git(root, "rev-parse", "HEAD:" + TARGET) != EXPECTED_BLOB:
        raise RuntimeError("HEAD_SOURCE_BLOB_CHANGED")
    source = root / TARGET
    original = subprocess.run(
        ("git", "show", "HEAD:" + TARGET), cwd=root,
        capture_output=True, check=True,
    ).stdout.decode("utf-8")
    canonical = expected_updated_source(original)
    contents = source.read_bytes()
    if b"\r\n" in contents and b"\n" in contents.replace(b"\r\n", b""):
        raise RuntimeError("MIXED_EOL_REJECTED")
    newline = "\r\n" if b"\r\n" in contents else "\n"
    current = contents.decode("utf-8").replace("\r\n", "\n")
    if current not in (original.replace("\r\n", "\n"), canonical.replace("\r\n", "\n")):
        raise RuntimeError("UNEXPECTED_WORKTREE_SOURCE")
    baseline = original.replace("\r\n", "\n")
    modified = canonical.replace("\r\n", "\n")
    if current == baseline:
        status = "PATCH_REQUIRED"
        if not dry_run:
            source.write_bytes(modified.replace("\n", newline).encode("utf-8"))
    else:
        status = "ALREADY_APPLIED"
    # Provide the complete modified function for immediate inspection.
    tree = ast.parse(modified)
    fun = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == "shared_expansion_provider")
    body = "\n".join(modified.splitlines()[fun.lineno - 1:fun.end_lineno])
    out = root / "phase175_r4r14r5_public_zero_transport" / "SHARED_PROVIDER_FULL_JA.md"
    if not dry_run:
        out.write_text(
            "# 変更後の共有関数全文\n\n"
            "変更対象：`phase165_r52_r9_shared_math.py` / "
            "`shared_expansion_provider`。\n\n```python\n"
            + body + "\n```\n", encoding="utf-8",
        )
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_and_apply(args.root, dry_run=args.dry_run)
    print("PHASE175_R4R14R5_PATCH_STATUS=" + state)
    print("PHASE175_R4R14R5_GATE=" + (
        "PASS_DRYRUN_SOURCE_GUARD" if args.dry_run
        else "PASS_GUARDED_SHARED_PROVIDER_WIRING"
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
