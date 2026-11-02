"""Install only the reviewed full zero-branch function; preserve source EOLs."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import subprocess
import tempfile

BASE_HEAD = "924888b257f9fed1e2d34790127b4ff108a7badb"
TARGET = "phase165_r55_nk_only_goal.py"
EXPECTED_BLOB = "b207b8169590e634229d412324d857ffb3857939"
SOURCE_BLOBS = {
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "phase165_r52_r3_web_adapter.py": "cfe2c244567535ffaf1e1c2e3ac27dc539ed3c21",
    "phase173_r4_r7_source_first_rule/source.py": "abdc05c731e5ede1258962705bc577b5307b6f38",
    "phase173_r4_r7_source_first_rule/rule.py": "5113c88e263c28b748c1543ec57bbcedb3eff5bf",
    "phase173_r4_r1_narrative_source_fix/projection.py": "ef81a01df157075bc2a21b91bc4ad5fcd56d2cd1",
    "phase173_r4_r8_public_connection/route.py": "06a402083a23595861f2856255947e4d26a2cc88",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
}


def git(root: Path, *arguments: str) -> str:
    proc = subprocess.run(
        ["git", *arguments], cwd=root, text=True, encoding="utf-8",
        errors="replace", capture_output=True, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("git " + " ".join(arguments) + ": " + proc.stderr[:500])
    return proc.stdout.strip()


def _full_function(old: str, name: str) -> tuple[str, str, str]:
    """Identify the only top-level function, including its complete body."""
    tree = ast.parse(old)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == name]
    if len(matches) != 1:
        raise RuntimeError("Expected one exact function: " + name)
    node = matches[0]
    lines = old.splitlines(keepends=True)
    start = node.lineno - 1
    end = node.end_lineno
    return "".join(lines[:start]), "".join(lines[start:end]), "".join(lines[end:])


def patched_source(original: bytes, replacement_function: str) -> bytes:
    """Replace the whole function, rejecting all unreviewed variants."""
    if not isinstance(replacement_function, str):
        raise TypeError("replacement_function must be source text")
    newline = "\r\n" if b"\r\n" in original else "\n"
    decoded = original.decode("utf-8-sig").replace("\r\n", "\n")
    prefix, old_function, suffix = _full_function(decoded, "search_group_from_registered_goal")
    if original.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected BOM in reviewed source")
    if "prepare_zero_toda56_public_connection" in old_function:
        raise RuntimeError("R4-R11 hook already installed")
    required = (
        "screen_independent_sources_for_derived_goal(",
        "provider = shared_expansion_provider(",
        "if isinstance(candidate, TodaPrimaryGroupZeroStatement):",
    )
    if any(old_function.count(item) != 1 for item in required):
        raise RuntimeError("Reviewed function anchors differ")
    fresh = ast.parse(replacement_function)
    if len(fresh.body) != 1 or not isinstance(fresh.body[0], ast.FunctionDef):
        raise RuntimeError("Replacement must contain exactly one full function")
    if fresh.body[0].name != "search_group_from_registered_goal":
        raise RuntimeError("Replacement function has the wrong name")
    # Compare the unchanged pre-zero and post-zero behavior as AST, and make
    # the single new branch explicit in the full replacement file.
    old_tree = ast.parse(old_function).body[0]
    new_tree = fresh.body[0]
    old_sections = [ast.dump(node, include_attributes=False)
                    for node in old_tree.body]
    new_sections = [ast.dump(node, include_attributes=False)
                    for node in new_tree.body]
    if len(old_sections) != len(new_sections):
        raise RuntimeError("Top-level function body structure differs")
    different = [index for index, (a, b) in enumerate(zip(old_sections, new_sections))
                 if a != b]
    if len(different) != 1 or not isinstance(old_tree.body[different[0]], ast.If):
        raise RuntimeError("R4-R11 must change only the zero branch")
    if "isinstance(candidate, TodaPrimaryGroupZeroStatement)" not in old_function:
        raise RuntimeError("Zero branch anchor missing")
    combined = prefix + replacement_function.rstrip("\n") + "\n" + suffix
    transformed = combined.replace("\n", newline).encode("utf-8")
    compile(transformed.decode("utf-8"), TARGET, "exec")
    return transformed


def preflight(root: Path, *, dry_run: bool) -> tuple[Path, bytes, bytes, bool]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("Run at the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only develop is supported")
    head = git(root, "rev-parse", "HEAD")
    if head != BASE_HEAD:
        lineage = subprocess.run(["git", "merge-base", "--is-ancestor", BASE_HEAD, head],
                                 cwd=root, check=False)
        if lineage.returncode != 0:
            raise RuntimeError("Current HEAD is not a descendant of reviewed baseline")
    remote = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop").split()[0]
    if remote != head:
        raise RuntimeError("Local and GitHub develop must match")
    staged = git(root, "diff", "--cached", "--name-only")
    if staged:
        raise RuntimeError("Staged changes require review")
    for relative, expected in SOURCE_BLOBS.items():
        if not (root / relative).is_file() or git(root, "hash-object", "--", relative) != expected:
            raise RuntimeError("Reviewed source mismatch: " + relative)
    from hashlib import sha256
    reviewed_core = root / "phase173_r4_r10_general_toda56_core" / "core.py"
    if (not reviewed_core.is_file() or sha256(reviewed_core.read_bytes()).hexdigest()
            != "453b13c25a1b92e54ce574469734f547c6a52577b817c7bcd1d5ba2df7718f68"):
        raise RuntimeError("Reviewed R4-R10 core unavailable")
    target = root / TARGET
    if not target.is_file():
        raise RuntimeError("Target missing")
    source = target.read_bytes()
    replacement = (Path(__file__).with_name(
        "search_group_from_registered_goal_FULL.py.txt").read_text(encoding="utf-8"))
    if git(root, "hash-object", "--", TARGET) == EXPECTED_BLOB:
        if git(root, "status", "--porcelain", "--untracked-files=no"):
            raise RuntimeError("Tracked changes require review")
        return target, source, patched_source(source, replacement), False
    if b"prepare_zero_toda56_public_connection" in source:
        # Idempotent only if the committed source is exactly the patch calculated
        # from the reviewed Git blob. A foreign implementation is rejected.
        original = subprocess.run(["git", "show", BASE_HEAD + ":" + TARGET],
                                  cwd=root, capture_output=True, check=True).stdout
        expected = patched_source(original, replacement)
        if source != expected:
            raise RuntimeError("Unreviewed R4-R11 installed source")
        if git(root, "status", "--porcelain", "--untracked-files=no") not in ("", "M " + TARGET):
            raise RuntimeError("Unexpected tracked changes")
        return target, source, expected, True
    raise RuntimeError("Unreviewed target file changed; refusing overwrite")


def install(root: Path, *, dry_run: bool) -> str:
    target, old, changed, already = preflight(root, dry_run=dry_run)
    print("PHASE173_R4_R11_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R11_HEAD=" + git(root, "rev-parse", "HEAD"), flush=True)
    if already:
        print("PHASE173_R4_R11_ALREADY_INSTALLED=True", flush=True)
        return "ALREADY_INSTALLED"
    if dry_run:
        print("PHASE173_R4_R11_DRY_RUN=PASS", flush=True)
        return "DRY_RUN_PASS"
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent, prefix=".r4r11_",
                                         suffix=".tmp", delete=False) as stream:
            temp_name = stream.name
            stream.write(changed)
            stream.flush()
            os.fsync(stream.fileno())
        if target.read_bytes() != old:
            raise RuntimeError("Target changed during write")
        os.replace(temp_name, target)
        temp_name = None
    finally:
        if temp_name is not None:
            Path(temp_name).unlink(missing_ok=True)
    print("PHASE173_R4_R11_PATCHED=" + TARGET, flush=True)
    return "PATCHED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(Path(args.root).resolve(), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
