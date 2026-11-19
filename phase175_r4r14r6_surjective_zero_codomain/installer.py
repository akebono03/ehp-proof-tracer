"""Guarded and idempotent addition of one generic root expansion provider."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess
import sys

TARGET = "phase165_r52_r9_shared_math.py"
R5_PIN = "f103bd9ca787542bf41a8b9ab1d1d96668ba63b7"
ANCHOR = "        options.extend(expand_ehp_zero_from_delta_surjectivity(goal))"
INSERT = (
    "        # Phase 175 R4R14R6: generic surjective-zero-image root branch.\n"
    "        # All subgoals remain ordinary source-first proof obligations.\n"
    "        from phase175_r4r14r6_surjective_zero_codomain.rule import (\n"
    "            expand_surjective_zero_codomain,\n"
    "        )\n"
    "        options.extend(expand_surjective_zero_codomain(goal))\n"
)


def git(root: Path, *args: str, data: bytes | None = None) -> str:
    proc = subprocess.run(
        ("git",) + args, cwd=root, input=data, capture_output=True, check=False,
    )
    if proc.returncode:
        raise RuntimeError("GIT_FAILURE: " + " ".join(args) + " " + proc.stderr.decode(errors="replace")[:300])
    return proc.stdout.decode("ascii", errors="replace").strip()


def source_hash(root: Path, contents: str) -> str:
    return git(root, "hash-object", "--stdin", data=contents.encode("utf-8"))


def next_source(source: str) -> str:
    if source.count(ANCHOR) != 1:
        raise RuntimeError("EXPECTED_EHP_ROOT_ANCHOR_MISSING")
    if source.count("build_public_composite_zero_transport_provider(bridge)") != 1:
        raise RuntimeError("R4R14R5_SOURCE_WIRING_MISSING")
    if INSERT in source:
        return source
    updated = source.replace(ANCHOR, INSERT + ANCHOR, 1)
    tree = ast.parse(updated)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "shared_expansion_provider"]
    if len(matches) != 1:
        raise RuntimeError("SHARED_PROVIDER_DEFINITION_CHANGED")
    return updated


def verify_and_apply(root: Path, dry_run: bool) -> str:
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_FILES_PRESENT")
    f = root / TARGET
    raw = f.read_bytes()
    if b"\r" in raw.replace(b"\r\n", b""):
        raise RuntimeError("MIXED_OR_INVALID_EOL")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    source = raw.decode("utf-8").replace("\r\n", "\n")
    updated = next_source(source)
    if INSERT in source:
        before = source.replace(INSERT, "", 1)
        if source_hash(root, before) != R5_PIN:
            raise RuntimeError("UNREVIEWED_MODIFIED_SHARED_SOURCE")
        status = "ALREADY_APPLIED"
    else:
        if source_hash(root, source) != R5_PIN:
            raise RuntimeError("R5_SOURCE_BLOB_MISMATCH")
        status = "PATCH_REQUIRED"
        if not dry_run:
            f.write_bytes(updated.replace("\n", newline).encode("utf-8"))
    if not dry_run:
        tree = ast.parse(updated)
        fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                  and node.name == "shared_expansion_provider")
        complete = "\n".join(updated.splitlines()[fn.lineno - 1:fn.end_lineno])
        report = root / "phase175_r4r14r6_surjective_zero_codomain" / "SHARED_FUNCTION_FULL_JA.md"
        report.write_text(
            "# 更新後の共有関数全文\n\n"
            "`phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 全文。\n\n"
            "```python\n" + complete + "\n```\n", encoding="utf-8",
        )
    return status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    status = verify_and_apply(args.root, dry_run=args.dry_run)
    print("PHASE175_R4R14R6_PATCH_STATUS=" + status)
    print("PHASE175_R4R14R6_GATE=" + (
        "PASS_R4R14R6_DRYRUN_SOURCE_GUARD" if args.dry_run
        else "PASS_R4R14R6_SHARED_ROOT_PROVIDER_CONNECTED"
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
