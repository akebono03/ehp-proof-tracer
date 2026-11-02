"""Install a reviewed complete Web-adapter function, protecting the R4-R11 patch."""
from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import os
from pathlib import Path
import subprocess
import tempfile

TARGET = "phase165_r52_r3_web_adapter.py"
EXISTING_PROOF_TARGET = "phase165_r55_nk_only_goal.py"
EXPECTED_WEB_ADAPTER_BLOB = "cfe2c244567535ffaf1e1c2e3ac27dc539ed3c21"
EXPECTED_PROJECTOR_SHA256 = "7c553d5f9651e3e8754b661f25907c544fd78857859335c695842f4cac8bcc08"
REVIEWED_BASE_HEAD = "de390132fcdcb52d2d5c16d2259f2b1073f09ad9"


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + ": " + proc.stderr[:500])
    return proc.stdout.strip()


def git_bytes(root: Path, *args: str) -> bytes:
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + " failed")
    return proc.stdout


def _function_span(source: str, name: str) -> tuple[int, int, ast.FunctionDef]:
    tree = ast.parse(source)
    selected = [node for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(selected) != 1:
        raise RuntimeError("A single complete function is required")
    node = selected[0]
    return node.lineno - 1, node.end_lineno, node


def patched_source(original: bytes, fixture: str) -> bytes:
    """Replace only the reviewed entire function, preserving other source bytes."""
    if not isinstance(fixture, str):
        raise TypeError("Full Web adapter fixture must be str")
    if original.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected UTF-8 BOM")
    newline = "\r\n" if b"\r\n" in original else "\n"
    old = original.decode("utf-8").replace("\r\n", "\n")
    new = fixture.replace("\r\n", "\n")
    old_tree = ast.parse(old)
    new_tree = ast.parse(new)
    old_others = [ast.dump(node, include_attributes=False)
                  for node in old_tree.body if not (
                      isinstance(node, ast.FunctionDef)
                      and node.name == "build_partial_web_group_proof_view")]
    new_others = [ast.dump(node, include_attributes=False)
                  for node in new_tree.body if not (
                      isinstance(node, ast.FunctionDef)
                      and node.name == "build_partial_web_group_proof_view")]
    if old_others != new_others:
        raise RuntimeError("Adapter imports or other definitions changed")
    start, end, old_fn = _function_span(old, "build_partial_web_group_proof_view")
    _, _, new_fn = _function_span(new, "build_partial_web_group_proof_view")
    old_nodes = [ast.dump(node, include_attributes=False) for node in old_fn.body]
    new_nodes = [ast.dump(node, include_attributes=False) for node in new_fn.body]
    if len(old_nodes) != len(new_nodes):
        raise RuntimeError("Unexpected Web adapter function structure")
    differences = [i for i, (left, right) in enumerate(zip(old_nodes, new_nodes))
                   if left != right]
    if len(differences) != 1 or not isinstance(old_fn.body[differences[0]], ast.If):
        raise RuntimeError("Only the narrative branch may change")
    if old.count("project_verified_pi74_narrative(") != 1:
        raise RuntimeError("Legacy narrative anchor changed")
    if new.count("project_verified_toda56_narrative(") != 1:
        raise RuntimeError("Common narrative anchor changed")
    lines = old.splitlines(keepends=True)
    fresh_lines = new.splitlines(keepends=True)
    fresh_start, fresh_end, _ = _function_span(new, "build_partial_web_group_proof_view")
    updated = "".join(lines[:start]) + "".join(fresh_lines[fresh_start:fresh_end]) + "".join(lines[end:])
    output = updated.replace("\n", newline).encode("utf-8")
    compile(output.decode("utf-8"), TARGET, "exec")
    return output


def preflight(root: Path) -> tuple[Path, bytes, bytes, bool]:
    """Fail closed for a foreign diff, source or R4-R11 production patch."""
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("Run at the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only develop branch is supported")
    head = git(root, "rev-parse", "HEAD")
    if head != REVIEWED_BASE_HEAD and subprocess.run(
        ["git", "merge-base", "--is-ancestor", REVIEWED_BASE_HEAD, head],
        cwd=root, check=False,
    ).returncode != 0:
        raise RuntimeError("Unexpected develop lineage")
    if git(root, "ls-remote", "origin", "refs/heads/develop").split()[0] != head:
        raise RuntimeError("Local and remote develop HEAD differ")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    changed = set(git(root, "diff", "--name-only").splitlines()) - {""}
    if not changed.issubset({EXISTING_PROOF_TARGET, TARGET}):
        raise RuntimeError("Unrelated tracked changes require review")
    if git(root, "rev-parse", "HEAD:" + TARGET) != EXPECTED_WEB_ADAPTER_BLOB:
        raise RuntimeError("Web adapter committed source differs from reviewed blob")
    from phase173_r4_r11_zero_public_connection import install as earlier
    proof_baseline = git_bytes(root, "show", earlier.BASE_HEAD + ":" + EXISTING_PROOF_TARGET)
    proof_function = (
        root / "phase173_r4_r11_zero_public_connection"
        / "search_group_from_registered_goal_FULL.py.txt"
    ).read_text(encoding="utf-8")
    expected_proof = earlier.patched_source(proof_baseline, proof_function)
    if (root / EXISTING_PROOF_TARGET).read_bytes() != expected_proof:
        raise RuntimeError("Existing R4-R11 proof-search modification is not the reviewed patch")
    projector = root / "phase173_r4_r12_common_narrative" / "projection.py"
    if sha256(projector.read_bytes()).hexdigest() != EXPECTED_PROJECTOR_SHA256:
        raise RuntimeError("Narrative projector changed after review")
    target = root / TARGET
    original = git_bytes(root, "show", "HEAD:" + TARGET)
    fixture = (root / "phase173_r4_r12_common_narrative" / "web_adapter_FULL.py.txt").read_text(encoding="utf-8")
    replacement = patched_source(original, fixture)
    actual = target.read_bytes()
    if actual not in (original, replacement):
        raise RuntimeError("Unreviewed Web adapter modification")
    return target, actual, replacement, actual == replacement


def apply(root: Path, *, dry_run: bool) -> str:
    target, current, replacement, installed = preflight(root)
    print("PHASE173_R4_R12_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R12_HEAD=" + git(root, "rev-parse", "HEAD"), flush=True)
    if dry_run:
        print("PHASE173_R4_R12_DRY_RUN=PASS", flush=True)
        return "DRY_RUN_PASS"
    if installed:
        print("PHASE173_R4_R12_ALREADY_INSTALLED=True", flush=True)
        return "ALREADY_INSTALLED"
    filename = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=target.parent, prefix=".r4r12_", suffix=".tmp", delete=False,
        ) as stream:
            filename = stream.name
            stream.write(replacement)
            stream.flush()
            os.fsync(stream.fileno())
        if target.read_bytes() != current:
            raise RuntimeError("Web adapter changed during installation")
        os.replace(filename, target)
        filename = None
    finally:
        if filename is not None:
            Path(filename).unlink(missing_ok=True)
    print("PHASE173_R4_R12_PATCHED=" + TARGET, flush=True)
    return "PATCHED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    apply(Path(args.root).resolve(), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
