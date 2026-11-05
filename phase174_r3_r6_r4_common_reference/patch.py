"""Guarded, scope-limited installation of Phase 174 R3-R6-R4 Reference prose.

Only the existing project_reference_bodies function is extended by two
source-checked presentation lines. All other paths and functions are retained.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase168_r3_37c_reference_projection.py")
REVIEWED_REMOTE_HEAD = "f2e148afefb11eb0b0ca31da67c65ec1ffe9e1e9"
REVIEWED_LOCAL_HEADS = (
    "ecbb2fea225c5b88000629d9c025934fcc2d7075",
    REVIEWED_REMOTE_HEAD,
)
REVIEWED_BLOB = "754e63cf4beee3c882c601dbe4b97cb8ecbdc4d2"
MODULE = "phase174_r3_r6_r4_common_reference.projection"

IMPORT_OLD = """    from proof import Relation

    result = []
"""
IMPORT_NEW = """    from proof import Relation
    from phase174_r3_r6_r4_common_reference.projection import (
        project_cited_universal_toda_reference_body,
    )

    result = []
"""
BODY_OLD = """            if sentence is None:
                sentence = typed_sentence(statement, None)
"""
BODY_NEW = """            if sentence is None:
                sentence = project_cited_universal_toda_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = typed_sentence(statement, None)
"""


def _git(*args: str) -> bytes:
    completed = subprocess.run(
        ("git",) + args,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        message = completed.stderr.decode("utf-8", errors="replace")
        raise ValueError(f"Git preflight rejected {args}: {message.strip()}")
    return completed.stdout


def _git_blob(content: bytes) -> str:
    return sha1(b"blob " + str(len(content)).encode("ascii") + b"\x00" + content).hexdigest()


def _normalized(source: str) -> str:
    return source.replace("\r\n", "\n")


def _replace_one_preserving_ends(source: str, before: str, after: str) -> str:
    """Add one reviewed block, preserving every untouched byte/EOL sequence."""
    candidates = tuple(
        (before.replace("\n", ending), after.replace("\n", ending))
        for ending in ("\r\n", "\n")
    )
    matches = tuple((old, new) for old, new in candidates if source.count(old) == 1)
    if len(matches) != 1:
        raise ValueError("Reviewed insertion anchor is missing or ambiguous")
    old, new = matches[0]
    return source.replace(old, new, 1)


def candidate_source(source: str) -> str:
    """Return an entire replacement module from exactly two reviewed inserts."""
    result = _replace_one_preserving_ends(source, IMPORT_OLD, IMPORT_NEW)
    result = _replace_one_preserving_ends(result, BODY_OLD, BODY_NEW)
    original = ast.parse(source)
    changed = ast.parse(result)
    original_functions = [node.name for node in original.body if isinstance(node, ast.FunctionDef)]
    changed_functions = [node.name for node in changed.body if isinstance(node, ast.FunctionDef)]
    if original_functions != changed_functions:
        raise ValueError("Function API changed during Reference projection patch")
    return result


def _function_source(module: str, name: str) -> str:
    tree = ast.parse(_normalized(module))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(found) != 1:
        raise ValueError("Expected exactly one existing Reference projection function")
    node = found[0]
    lines = _normalized(module).splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def reviewed_changes() -> tuple[bytes, bool]:
    """Validate the pinned remote and exact target content before any write."""
    branch = _git("branch", "--show-current").decode("ascii").strip()
    local_head = _git("rev-parse", "HEAD").decode("ascii").strip()
    remote_head = _git("rev-parse", "origin/develop").decode("ascii").strip()
    print("PHASE174_R3R6R4_BRANCH=" + branch)
    print("PHASE174_R3R6R4_LOCAL_HEAD=" + local_head)
    print("PHASE174_R3R6R4_REMOTE_HEAD=" + remote_head)
    if branch != "develop" or remote_head != REVIEWED_REMOTE_HEAD:
        raise ValueError("Unreviewed branch or remote HEAD; do not apply")
    if local_head not in REVIEWED_LOCAL_HEADS:
        raise ValueError("Unreviewed local HEAD; do not apply")
    if _git("diff", "--cached", "--name-only", "--", TARGET.as_posix()).strip():
        raise ValueError("Target contains staged changes; do not overwrite")

    baseline = _git("show", f"{REVIEWED_REMOTE_HEAD}:{TARGET.as_posix()}")
    if _git_blob(baseline) != REVIEWED_BLOB:
        raise ValueError("Reviewed reference file blob was replaced")
    target = ROOT / TARGET
    raw = target.read_bytes()
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    local = raw[len(bom):].decode("utf-8")
    canonical = baseline.decode("utf-8")
    expected = candidate_source(canonical)
    if _normalized(local) == _normalized(expected):
        print("PHASE174_R3R6R4_ALREADY_INSTALLED=True")
        return raw, True
    if _normalized(local) != _normalized(canonical):
        raise ValueError("Unreviewed local Reference changes; refusing overwrite")
    revised = candidate_source(local)
    if (len(ast.parse(revised).body) != len(ast.parse(local).body)
            or _normalized(revised) != _normalized(expected)):
        raise ValueError("Unexpected module-level changes after patch")
    return bom + revised.encode("utf-8"), False


def _write_output(candidate: bytes, installed: bool) -> None:
    folder = ROOT / "phase174_r3_r6_r4_common_reference" / "output"
    folder.mkdir(parents=True, exist_ok=True)
    source = candidate.decode("utf-8-sig")
    full = _normalized(source)
    (folder / "phase168_r3_37c_reference_projection.py.FULL.py").write_text(
        full, encoding="utf-8", newline="\n",
    )
    (folder / "project_reference_bodies_FULL.py").write_text(
        _function_source(full, "project_reference_bodies"), encoding="utf-8", newline="\n",
    )
    (folder / "README.txt").write_text(
        "Reviewed HEAD: " + REVIEWED_REMOTE_HEAD + "\n"
        "Production target: " + TARGET.as_posix() + "\n"
        "Entire modified function and entire module are in this directory.\n"
        "Already installed: " + str(installed) + "\n"
        "No other production file is modified.\n",
        encoding="utf-8", newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    candidate, installed = reviewed_changes()
    _write_output(candidate, installed)
    print("PHASE174_R3R6R4_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6R4_PRODUCTION_TARGETS=1")
    print("PHASE174_R3R6R4_NEW_GIVEN=0")
    if args.dry_run:
        print("PHASE174_R3R6R4_DRY_RUN=PASS")
        return 0
    if not installed:
        (ROOT / TARGET).write_bytes(candidate)
    print("PHASE174_R3R6R4_APPLIED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
