"""Apply R4C only over a verified R4B baseline, committed or uncommitted.

No source edit happens unless the exact known Git blob and the exact expected
working-tree contents are verified. The published R4B content is the only
permitted predecessor of R4C.
"""
from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
EXPECTED_PRE_R4B_GIT_BLOB = "8a9d534f87cb04b807dca4b3b2ef09e2d3eaa1c5"
EXPECTED_COMMITTED_R4B_GIT_BLOB = "c94dc82fc28214fff63020773c2e9c5c126414ae"
R4B_ANCHOR = "        options.extend(expand_cited_eta_generator(goal))\n"
R4B_INSERT = (
    "        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity\n"
    "        options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))\n"
)
R4C_INSERT = (
    "        from phase169_r4c_pi64_suspension_iso.rule import expand_pi64_suspension_isomorphism\n"
    "        options.extend(expand_pi64_suspension_isomorphism(goal))\n"
)


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return completed.stdout.strip()


def git_blob_hash(data: bytes) -> str:
    """Compute Git's file-object SHA-1 without requiring a Git worktree."""
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def expected_r4b_source(base: str) -> str:
    if base.count(R4B_ANCHOR) != 1:
        raise RuntimeError("verified GitHub baseline does not have the R4B anchor once")
    if R4B_INSERT in base or R4C_INSERT in base:
        raise RuntimeError("pre-R4B baseline already contains later-phase rules")
    return base.replace(R4B_ANCHOR, R4B_ANCHOR + R4B_INSERT, 1)


def verified_r4b_worktree(head_blob: str, base_bytes: bytes, worktree_bytes: bytes) -> tuple[str, str]:
    """Return normalized R4B worktree and provenance, or fail closed.

    Accept exactly two audited layouts:
      pre-R4B commit + the local R4B edit, or R4B already in Git HEAD.
    Do not tolerate any additional tracked edit in the target file.
    """
    if git_blob_hash(base_bytes) != head_blob:
        raise RuntimeError("Git HEAD blob and retrieved bytes do not match")
    git_newline = "\r\n" if b"\r\n" in base_bytes else "\n"
    base = base_bytes.decode("utf-8").replace("\r\n", "\n")
    current = worktree_bytes.decode("utf-8").replace("\r\n", "\n")
    if head_blob == EXPECTED_PRE_R4B_GIT_BLOB:
        expected = expected_r4b_source(base)
        kind = "R4B_UNCOMMITTED"
    elif head_blob == EXPECTED_COMMITTED_R4B_GIT_BLOB:
        if base.count(R4B_INSERT) != 1 or R4C_INSERT in base:
            raise RuntimeError("committed R4B source has missing or duplicate insertion")
        old = base.replace(R4B_INSERT, "", 1)
        old_bytes = old.replace("\n", git_newline).encode("utf-8")
        if git_blob_hash(old_bytes) != EXPECTED_PRE_R4B_GIT_BLOB:
            raise RuntimeError("committed R4B differs from the audited single-rule edit")
        if expected_r4b_source(old) != base:
            raise RuntimeError("R4B insertion point is inconsistent")
        expected = base
        kind = "R4B_COMMITTED"
    else:
        raise RuntimeError("unrecognized Git HEAD shared provider blob; stop before patching")
    if current != expected:
        raise RuntimeError("working shared provider is not exactly the audited R4B state; no edits made")
    if current.count(R4B_INSERT) != 1 or R4C_INSERT in current:
        raise RuntimeError("R4C insertion is missing its unique R4B predecessor")
    return current, kind


def main() -> None:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R4C requires develop branch")
    if not TARGET.is_file():
        raise RuntimeError("shared provider missing")
    if not (ROOT / "phase169_r4b_prop44_injectivity" / "rule.py").is_file():
        raise RuntimeError("R4B proof rule is missing; apply R4B first")

    head_blob = git("rev-parse", "HEAD:" + TARGET.name)
    base_bytes = subprocess.run(
        ["git", "show", "HEAD:" + TARGET.name], cwd=ROOT,
        check=True, capture_output=True,
    ).stdout
    original = TARGET.read_bytes()
    current, baseline_kind = verified_r4b_worktree(head_blob, base_bytes, original)
    newline = "\r\n" if b"\r\n" in original else "\n"
    updated = current.replace(R4B_INSERT, R4B_INSERT + R4C_INSERT, 1)
    parsed = ast.parse(updated, filename=str(TARGET))
    functions = [
        item for item in parsed.body
        if isinstance(item, ast.FunctionDef) and item.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise RuntimeError("shared_expansion_provider must be defined exactly once")
    fn = functions[0]
    full_function = "".join(updated.splitlines(keepends=True)[fn.lineno - 1:fn.end_lineno])

    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    backup = output / "phase165_r52_r9_shared_math.py.before"
    backup.write_bytes(original)
    (output / "phase165_r52_r9_shared_math.py.FULL").write_text(updated, encoding="utf-8")
    (output / "shared_expansion_provider_FULL.py").write_text(full_function, encoding="utf-8")
    TARGET.write_bytes(updated.replace("\n", newline).encode("utf-8"))
    print("R4C_BASELINE_KIND=" + baseline_kind)
    print("R4C_PATCHED=" + str(TARGET))
    print("R4C_BACKUP=" + str(backup))
    print("R4C_FULL_FUNCTION=" + str(output / "shared_expansion_provider_FULL.py"))
    print("R4C_FULL_FILE=" + str(output / "phase165_r52_r9_shared_math.py.FULL"))


if __name__ == "__main__":
    main()
