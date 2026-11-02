"""Guarded installer for the scoped and read-only pi_7^4 Web narrative fix."""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1, sha256
import os
from pathlib import Path
import shutil
import subprocess

TARGET = Path("phase165_r52_r3_web_adapter.py")
EXPECTED_TARGET_BLOB = "aefdc5527aeec7bcb7ffe77f69b754a39f3a242b"
EXPECTED_PUBLIC_BASE = "2718c55789af7f442ac2c086d016d3d6f7ca3133"
EXPECTED_PUBLIC_COMMITTED = "3e4c5f9c62b04d618f845b0f82d1cb1cacccdf2e"
EXPECTED_PUBLIC_INSTALLER = "9aa2e08a60cdd63a9033277327320f016f7104fc"
EXPECTED_PUBLIC_ROUTE = "fa79655aa24a88d5e7dd46d8c7a00ae04aeb15d4"
PUBLIC_TARGET = "phase165_r52_r9_shared_math.py"
PUBLIC_INSTALLER = "phase173_r4_r1_public_connection/install.py"
PUBLIC_ROUTE = "phase173_r4_r1_public_connection/route.py"
ANCHOR = "            markdown = render_model_backed_narrative_markdown(result, narrative_model)\n"
HOOK = (
    "            if (n == 4 and k == 3 and mode == \"narrative\"\n"
    "                    and result.status is ProofSearchStatus.COMPLETE):\n"
    "                from phase173_r4_r1_narrative_source_fix.projection import (\n"
    "                    project_verified_pi74_narrative,\n"
    "                )\n"
    "                markdown = project_verified_pi74_narrative(\n"
    "                    result, narrative_model, markdown,\n"
    "                )\n"
)


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ("git", *arguments), cwd=root, capture_output=True,
        check=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(root: Path, filename: str) -> bytes:
    return subprocess.run(
        ("git", "show", "HEAD:" + filename),
        cwd=root, capture_output=True, check=True,
    ).stdout


def normalize(content: bytes) -> bytes:
    return content.replace(b"\r\n", b"\n")


def transform(source: str) -> str:
    if source.count(HOOK) != 0:
        raise RuntimeError("R4-R1 narrative hook already exists")
    if source.count(ANCHOR) != 1:
        raise RuntimeError("Reviewed narrative rendering anchor is absent or duplicated")
    functions = tuple(
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef)
        and node.name == "build_partial_web_group_proof_view"
    )
    if len(functions) != 1:
        raise RuntimeError("Canonical Web adapter function is not unique")
    lines = source.splitlines(keepends=True)
    function = "".join(lines[functions[0].lineno - 1:functions[0].end_lineno])
    if function.count(ANCHOR) != 1:
        raise RuntimeError("The reviewed anchor is outside the Web adapter")
    patched = source.replace(ANCHOR, ANCHOR + HOOK, 1)
    ast.parse(patched)
    return patched


def reviewed_public_state(root: Path) -> str:
    """Accept only the reviewed installed worktree hook or its committed form."""
    source_blob = git(root, "rev-parse", "HEAD:" + PUBLIC_TARGET)
    if source_blob == EXPECTED_PUBLIC_BASE:
        from phase173_r4_r1_public_connection.install import preflight as public_preflight
        state, _ = public_preflight(root)
        if state != "ALREADY_INSTALLED":
            raise RuntimeError("Install the reviewed R4-R1 public proof connection first")
        return "WORKTREE_INSTALLED"
    if source_blob != EXPECTED_PUBLIC_COMMITTED:
        raise RuntimeError("Reviewed search function Git blob changed")

    # After the public connection is committed, its old installer is no
    # longer a suitable preflight: it requires the pre-connection Git blob.
    # Check the complete reviewed committed source and each dependency instead.
    if git(root, "rev-parse", "HEAD:" + PUBLIC_INSTALLER) != EXPECTED_PUBLIC_INSTALLER:
        raise RuntimeError("Reviewed public installer Git blob changed")
    from phase173_r4_r1_public_connection.install import (
        EXPECTED_DEPENDENCIES,
        HOOK as PUBLIC_HOOK,
        REVIEWED_DIAGONAL_HEADS,
        REVIEWED_DIAGONAL_PATCH_SHA256,
    )
    dependencies = dict(EXPECTED_DEPENDENCIES)
    dependencies[PUBLIC_INSTALLER] = EXPECTED_PUBLIC_INSTALLER
    dependencies[PUBLIC_ROUTE] = EXPECTED_PUBLIC_ROUTE
    for path, expected in dependencies.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Reviewed public dependency Git blob changed: " + path)
        if normalize((root / path).read_bytes()) != normalize(git_bytes(root, path)):
            raise RuntimeError("Reviewed public dependency worktree changed: " + path)

    diagonal = "phase173_r4_r1_source_bound_56/rule.py"
    diagonal_blob = git(root, "rev-parse", "HEAD:" + diagonal)
    if diagonal_blob not in REVIEWED_DIAGONAL_HEADS:
        raise RuntimeError("Reviewed diagonal rule Git blob changed")
    diagonal_content = normalize((root / diagonal).read_bytes())
    diagonal_ok = (
        (diagonal_blob == REVIEWED_DIAGONAL_HEADS[0]
         and diagonal_content == normalize(git_bytes(root, diagonal)))
        or sha256(diagonal_content).hexdigest() == REVIEWED_DIAGONAL_PATCH_SHA256
    )
    if (not diagonal_ok
            or b"SourceBoundGoal(diagonal, diagonal_source)" not in diagonal_content):
        raise RuntimeError("Reviewed inferred diagonal rule is not installed")

    source = normalize(git_bytes(root, PUBLIC_TARGET)).decode("utf-8")
    worktree = normalize((root / PUBLIC_TARGET).read_bytes()).decode("utf-8")
    if source != worktree or source.count(PUBLIC_HOOK) != 1:
        raise RuntimeError("Reviewed committed public hook is missing or modified")
    # The committed file must differ from the original reviewed search file
    # by the single exact hook, and nothing else.
    original = source.replace(PUBLIC_HOOK, "", 1).encode("utf-8")
    git_source = git_bytes(root, PUBLIC_TARGET)
    if b"\r\n" in git_source:
        original = original.replace(b"\n", b"\r\n")
    original_blob = sha1(
        b"blob " + str(len(original)).encode("ascii") + b"\x00" + original
    ).hexdigest()
    if original_blob != EXPECTED_PUBLIC_BASE:
        raise RuntimeError("Committed public hook differs from reviewed search source")
    return "COMMITTED_INSTALLED"


def preflight(root: Path) -> tuple[str, bytes]:
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only develop is eligible")
    if git(root, "rev-parse", "HEAD") != git(root, "rev-parse", "origin/develop"):
        raise RuntimeError("HEAD differs from origin/develop")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != EXPECTED_TARGET_BLOB:
        raise RuntimeError("Reviewed Web adapter Git blob changed")
    public_state = reviewed_public_state(root)
    print("PHASE173_R4_R1_NARRATIVE_PUBLIC_STATE=" + public_state)
    if git(root, "diff", "--cached", "--name-only", "--", TARGET.as_posix()):
        raise RuntimeError("Refusing to overwrite staged Web adapter changes")
    content = (root / TARGET).read_bytes()
    text = normalize(content).decode("utf-8")
    original = normalize(git_bytes(root, TARGET.as_posix()))
    if text.encode("utf-8") == original:
        transform(text)
        return "NEW", content
    if text.count(HOOK) != 1 or text.replace(HOOK, "", 1).encode("utf-8") != original:
        raise RuntimeError("Unreviewed Web adapter worktree change; no overwrite")
    return "ALREADY_INSTALLED", content


def install(root: Path) -> str:
    state, content = preflight(root)
    if state == "ALREADY_INSTALLED":
        return state
    proposed = transform(normalize(content).decode("utf-8"))
    new_content = (
        proposed.replace("\n", "\r\n").encode("utf-8")
        if b"\r\n" in content else proposed.encode("utf-8")
    )
    backup = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_narrative_source_fix/"
        + sha256(content).hexdigest() + ".py"
    )
    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists() and backup.read_bytes() != content:
        raise RuntimeError("A different recovery backup already exists")
    if not backup.exists():
        shutil.copy2(root / TARGET, backup)
    (root / TARGET).write_bytes(new_content)
    return "INSTALLED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    state, _ = preflight(root)
    print("PHASE173_R4_R1_NARRATIVE_SOURCE_GUARD=PASS")
    print("PHASE173_R4_R1_NARRATIVE_PATCH_STATE=" + state)
    if args.dry_run:
        print("PHASE173_R4_R1_NARRATIVE_DRY_RUN=PASS")
        return 0
    print("PHASE173_R4_R1_NARRATIVE_INSTALL=" + install(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
