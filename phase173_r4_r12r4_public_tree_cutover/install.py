"""Phase 173 R4-R12R4: guarded Web narrative cutover to ProofNarrativeModel.

Only three reviewed files are changed. Never edits proof search, proof steps,
references, or the actual model renderer. Historical projector APIs stay intact.
"""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess


REVIEWED_HEAD = "188f707e1fcd8fde7b22af02a6b4005986fb3c1e"
ADAPTER = "phase165_r52_r3_web_adapter.py"
AUDIT = "phase173_r4_r13_narrative_audit/audit.py"
AUDIT_TEST = "phase173_r4_r13_narrative_audit/tests/test_audit.py"
BASELINE_BLOBS = {
    ADAPTER: "57b079d51d6d5810ab0be6884feae1ed117a386c",
    AUDIT: "6cb7fcd18e3bb7af2a376e656b2bef44b22d3e6e",
    AUDIT_TEST: "ccc746376f900c49c46751f6fa7cd1c89e6fa37b",
}
FIXTURES = {
    ADAPTER: "web_adapter_FULL.py",
    AUDIT: "inspect_dimension_FULL.py",
    AUDIT_TEST: "test_audit_FULL.py",
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return completed.stdout.strip()


def git_bytes(root: Path, *args: str) -> bytes:
    return subprocess.run(
        ("git", *args), cwd=root, capture_output=True, check=True,
    ).stdout


def replace_function(source: str, func_name: str, complete_function: str) -> str:
    """Replace one complete top-level function; never edit a partial body."""
    tree = ast.parse(source)
    expected = tuple(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == func_name
    )
    fixture = ast.parse(complete_function)
    if (len(expected) != 1 or len(fixture.body) != 1
            or not isinstance(fixture.body[0], ast.FunctionDef)
            or fixture.body[0].name != func_name):
        raise RuntimeError("Full function replacement does not match reviewed code")
    old = expected[0]
    lines = source.splitlines(keepends=True)
    newline = "\r\n" if "\r\n" in source else "\n"
    replacement = complete_function.replace("\n", newline)
    updated = "".join(lines[:old.lineno - 1]) + replacement + "".join(lines[old.end_lineno:])
    ast.parse(updated)
    return updated


def replacement_bytes(root: Path, path: str, fixture_dir: Path) -> bytes:
    original = git_bytes(root, "show", "HEAD:" + path)
    fixture = (fixture_dir / FIXTURES[path]).read_text(encoding="utf-8")
    ast.parse(fixture, filename=FIXTURES[path])
    if path == AUDIT:
        return replace_function(
            original.decode("utf-8-sig"), "inspect_dimension", fixture,
        ).encode("utf-8")
    return fixture.encode("utf-8")


def reviewed_head_lineage_allowed(root: Path, head: str) -> bool:
    """Allow only verified audit-only descendants of the reviewed production tree.

    Changing HEAD alone never authorizes a patch. The three target blobs are
    separately verified by preflight. Any other intervening repository change
    (including a renderer, proof rule, or test outside the audit directory)
    requires a new review and this function intentionally fails closed.
    """
    if head == REVIEWED_HEAD:
        return True
    ancestry = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestry.returncode != 0:
        return False
    committed_paths = git(
        root, "diff", "--name-only", REVIEWED_HEAD + ".." + head,
    ).splitlines()
    return all(
        path == ".pytest_cache/v/cache/nodeids"
        or path.startswith("phase173_r4_r12r3_architecture_audit/")
        for path in committed_paths
    )


def preflight(root: Path, fixture_dir: Path) -> dict[str, tuple[bytes, bytes]]:
    """Require reviewed Git ancestry and unchanged target blobs."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Run from the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("develop branch is required")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError(f"GitHub/local HEAD mismatch: local={head} remote={remote}")
    if not reviewed_head_lineage_allowed(root, head):
        raise RuntimeError(
            "HEAD is not a reviewed audit-only descendant: " + head
        )
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes must be reviewed first")
    dirty = set(git(root, "diff", "--name-only").splitlines())
    allowed = set(BASELINE_BLOBS) | {".pytest_cache/v/cache/nodeids"}
    if not dirty.issubset(allowed):
        raise RuntimeError("Unexpected tracked worktree changes: " + ", ".join(sorted(dirty - allowed)))
    content = {}
    for path, blob in BASELINE_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("Reviewed blob differs: " + path)
        original = git_bytes(root, "show", "HEAD:" + path)
        replacement = replacement_bytes(root, path, fixture_dir)
        compile(replacement, path, "exec")
        current = (root / path).read_bytes()
        if current not in (original, replacement):
            raise RuntimeError("Unreviewed local target content: " + path)
        content[path] = original, replacement
    adapter_source = content[ADAPTER][1].decode("utf-8")
    if "project_verified_toda56_narrative" in adapter_source:
        raise RuntimeError("Post-render projector is still reachable from Web adapter")
    print("PHASE173_R4_R12R4_HEAD=" + head)
    print("PHASE173_R4_R12R4_REVIEWED_BASE_HEAD=" + REVIEWED_HEAD)
    print("PHASE173_R4_R12R4_HEAD_LINEAGE=PASS")
    print("PHASE173_R4_R12R4_PREFLIGHT=PASS")
    return content


def update_files(root: Path, content: dict[str, tuple[bytes, bytes]], *, rollback: bool) -> None:
    """Apply the checked replacements; undo partial writes on any exception."""
    changed: list[tuple[Path, bytes, bytes]] = []
    try:
        for path, (original, replacement) in content.items():
            target = root / path
            present = target.read_bytes()
            expected = replacement if rollback else original
            desired = original if rollback else replacement
            if present == desired:
                print("PHASE173_R4_R12R4_ALREADY_DESIRED=" + path)
                continue
            if present != expected:
                raise RuntimeError("Refusing to overwrite an unexpected file: " + path)
            staged_file = target.with_name(target.name + ".r4r12r4_tmp")
            staged_file.write_bytes(desired)
            staged_file.replace(target)
            changed.append((target, present, desired))
            print(("PHASE173_R4_R12R4_ROLLED_BACK=" if rollback else "PHASE173_R4_R12R4_PATCHED=") + path)
    except Exception:
        for target, before, after in reversed(changed):
            if target.read_bytes() == after:
                target.write_bytes(before)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--apply", action="store_true")
    action.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    fixture_dir = Path(__file__).resolve().parent / "fixtures"
    content = preflight(root, fixture_dir)
    if args.dry_run:
        print("PHASE173_R4_R12R4_DRY_RUN=PASS")
        print("PHASE173_R4_R12R4_PRODUCTION_EDIT=NONE")
        return 0
    update_files(root, content, rollback=args.rollback)
    print("PHASE173_R4_R12R4_RESULT=" + ("ROLLED_BACK" if args.rollback else "PATCHED"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
