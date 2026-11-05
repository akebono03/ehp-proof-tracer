"""Guarded R3-R5 patch; adapt only directly affected previous tests.

All three modified functions are exported in their entirety after application.
Original bytes and line endings are preserved around the reviewed insertions.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

SHARED = "phase165_r52_r9_shared_math.py"
TEST = "phase174_r3_r4_public_delta_connection/tests/test_connection.py"
PREFLIGHT = "phase174_r3_r5_preflight/audit.py"
PREFLIGHT_COMMITTED_BLOB = "989d14731e88053554b491324475f319b8be2660"
REVIEWED_HEAD = "45d97b2adc73c2347866de28b344fce1e6d2c095"
BASE_COMMIT = "7ad6ae86714251a88f7002981c0aa20fb51e7069"
SHARED_BLOB = "b8e8bf820e470a9cad9bad2092cd4ed1a7fc55ac"
TEST_FUNCTION = "test_r3r4_real_production_file_has_only_reviewed_wiring"
OLD_SHARED = (
    "        options.extend(expand_delta_zero_from_injection(goal))\n"
    "        options.extend(expand_finite_cyclic_relation(goal))\n"
)
NEW_SHARED = (
    "        options.extend(expand_delta_zero_from_injection(goal))\n"
    "        from phase174_r3_r5_finite_cyclic_extension.rule import (\n"
    "            expand_finite_index_two_cyclic_structure, expand_toda48_index_two,\n"
    "        )\n"
    "        options.extend(expand_toda48_index_two(goal))\n"
    "        options.extend(expand_finite_index_two_cyclic_structure(goal))\n"
    "        options.extend(expand_finite_cyclic_relation(goal))\n"
)


def git(*args: str) -> bytes:
    return subprocess.run(
        ("git",) + args, check=True, capture_output=True,
    ).stdout


def blob_sha(contents: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(contents)).encode("ascii") + b"\x00" + contents
    ).hexdigest()


def insert_shared(original: bytes) -> bytes:
    ending = b"\r\n" if b"\r\n" in original else b"\n"
    old = OLD_SHARED.encode("utf-8").replace(b"\n", ending)
    new = NEW_SHARED.encode("utf-8").replace(b"\n", ending)
    if original.count(new) == 1 and original.count(old) == 0:
        return original
    if original.count(old) != 1 or original.count(new) != 0:
        raise ValueError("R3-R4 provider insertion context is not unique")
    changed = original.replace(old, new)
    ast.parse(changed.decode("utf-8-sig"))
    return changed


def extract_function(contents: bytes, name: str) -> str:
    string = contents.decode("utf-8-sig").replace("\r\n", "\n")
    tree = ast.parse(string)
    definitions = [
        item for item in tree.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        and item.name == name
    ]
    if len(definitions) != 1:
        raise ValueError("Expected exactly one complete function: " + name)
    node = definitions[0]
    return "\n".join(string.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def replace_r3r4_test(original: bytes) -> bytes:
    """Keep the earlier R3-R4 invariant, allowing only the reviewed R3-R5 tail."""
    ending = b"\r\n" if b"\r\n" in original else b"\n"
    string = original.decode("utf-8-sig").replace("\r\n", "\n")
    tree = ast.parse(string)
    definitions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == TEST_FUNCTION
    ]
    if len(definitions) != 1:
        raise ValueError("R3-R4 guarded test function not found exactly once")
    node = definitions[0]
    old = "\n".join(string.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"
    expected = (
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r4_public_delta_connection.patch import reviewed_head_bytes\n"
        "    old = reviewed_head_bytes()\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    assert current == replace_provider_call(old)\n"
        "    assert git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'\n"
        "    assert current.count(b'options.extend(expand_delta_zero_from_injection(goal))') == 1\n"
    )
    replacement = (
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared\n"
        "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = replace_provider_call(old)\n"
        "    assert current in (r3r4, insert_shared(r3r4))\n"
        "    assert git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'\n"
        "    assert current.count(b'options.extend(expand_delta_zero_from_injection(goal))') == 1\n"
    )
    if old == replacement:
        return original
    if old != expected:
        raise ValueError("R3-R4 original regression test diverged from reviewed body")
    changed = string.replace(old, replacement, 1).replace("\n", ending.decode("ascii"))
    result = changed.encode("utf-8")
    if original.startswith(b"\xef\xbb\xbf"):
        result = b"\xef\xbb\xbf" + result
    ast.parse(result.decode("utf-8-sig"))
    return result



def replace_preflight_provider_guard(original: bytes) -> bytes:
    """Accept only the reviewed committed preflight file or its exact patch.

    The preflight package was committed after the previous implementation ZIP
    had been prepared. It is now a tracked file, guarded by its Git blob.
    """
    committed = git("show", "HEAD:" + PREFLIGHT)
    if blob_sha(committed) != PREFLIGHT_COMMITTED_BLOB:
        raise ValueError("Reviewed preflight Git blob changed")
    old = (
        '        from phase174_r3_r4_public_delta_connection.patch import replace_provider_call\n'
        '        if source.encode("utf-8") != replace_provider_call(committed.encode("utf-8")):\n'
        '            raise ValueError("Unreviewed production source modifications")'
    )
    new = (
        '        from phase174_r3_r4_public_delta_connection.patch import replace_provider_call\n'
        '        from phase174_r3_r5_finite_cyclic_extension.patch import insert_shared\n'
        '        reviewed_r3r4 = replace_provider_call(committed.encode("utf-8"))\n'
        '        if source.encode("utf-8") not in (reviewed_r3r4, insert_shared(reviewed_r3r4)):\n'
        '            raise ValueError("Unreviewed production source modifications")'
    )
    old_bytes = old.encode("utf-8")
    if committed.count(old_bytes) != 1:
        raise ValueError("Reviewed preflight insertion context changed")
    modified = committed.replace(old_bytes, new.encode("utf-8"), 1)
    ast.parse(modified.decode("utf-8-sig"))
    if original == committed or original == modified:
        return modified
    raise ValueError("Refusing unrelated edit to committed preflight audit")


def verify_originals() -> tuple[bytes, bytes]:
    head = git("rev-parse", "HEAD").decode().strip()
    branch = git("branch", "--show-current").decode().strip()
    remote_result = git("ls-remote", "origin", "refs/heads/develop").decode().split()
    if len(remote_result) != 2:
        raise ValueError("Cannot uniquely read remote develop HEAD")
    remote = remote_result[0]
    if branch != "develop" or head != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise ValueError(
            "Reviewed develop HEAD mismatch: local=" + head
            + " remote=" + remote + " expected=" + REVIEWED_HEAD
        )
    git("merge-base", "--is-ancestor", BASE_COMMIT, head)
    # Keep the entire reviewed-path check, but request literal UTF-8 paths.
    # By default Git quotes non-ASCII filenames as C-style octal escapes,
    # e.g. the reviewed Japanese .md pathname would never equal its literal.
    changed = set(git(
        "-c", "core.quotePath=false", "diff", "--name-only",
        BASE_COMMIT + ".." + head,
    ).decode("utf-8").splitlines())
    reviewed_changes = {
        "phase174_r3_r5_preflight/README.md",
        "phase174_r3_r5_preflight/__init__.py",
        "phase174_r3_r5_preflight/audit.py",
        "phase174_r3_r5_preflight/run.ps1",
        "phase174_r3_r5_preflight/tests/__init__.py",
        "phase174_r3_r5_preflight/tests/test_audit.py",
        "phase174_r3_r5_preflight/実装前監査.md",
    }
    if changed != reviewed_changes:
        unexpected = sorted(changed - reviewed_changes)
        missing = sorted(reviewed_changes - changed)
        raise ValueError(
            "Unexpected files changed since the reviewed R3-R4 base: "
            + f"unexpected={unexpected!r} missing={missing!r}"
        )
    original_shared = git("show", "HEAD:" + SHARED)
    original_test = git("show", "HEAD:" + TEST)
    original_preflight = git("show", "HEAD:" + PREFLIGHT)
    if blob_sha(original_shared) != SHARED_BLOB:
        raise ValueError("Shared provider no longer has the reviewed Git blob")
    if blob_sha(original_preflight) != PREFLIGHT_COMMITTED_BLOB:
        raise ValueError("Committed preflight audit differs from the reviewed Git blob")
    if git("diff", "--cached", "--name-only").strip():
        raise ValueError("Staged changes need manual review")
    return original_shared, original_test

def apply(*, dry_run: bool) -> dict[str, object]:
    original_shared, original_test = verify_originals()
    modified_shared = insert_shared(original_shared)
    modified_test = replace_r3r4_test(original_test)
    original_preflight = git("show", "HEAD:" + PREFLIGHT)
    modified_preflight = replace_preflight_provider_guard(original_preflight)
    targets = ((SHARED, original_shared, modified_shared),
               (TEST, original_test, modified_test),
               (PREFLIGHT, original_preflight, modified_preflight))
    states: dict[str, str] = {}
    for name, before, after in targets:
        current = Path(name).read_bytes()
        if current == before:
            states[name] = "REVIEWED_ORIGINAL"
        elif current == after:
            states[name] = "ALREADY_APPLIED"
        else:
            raise ValueError("Refusing to overwrite unrelated user edit: " + name)
    if not dry_run:
        for name, before, after in targets:
            if states[name] == "REVIEWED_ORIGINAL":
                Path(name).write_bytes(after)
        for name, before, after in targets:
            if Path(name).read_bytes() != after:
                raise ValueError("Production or test replacement differs: " + name)
        folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
        folder = folder / "EHPProofTracerAudit" / "phase174_r3_r5_impl"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "shared_expansion_provider_FULL.py").write_text(
            extract_function(modified_shared, "shared_expansion_provider"),
            encoding="utf-8",
        )
        (folder / "test_r3r4_source_guard_FULL.py").write_text(
            extract_function(modified_test, TEST_FUNCTION), encoding="utf-8",
        )
        (folder / "preflight_inspect_source_provider_FULL.py").write_text(
            extract_function(modified_preflight, "inspect_source_provider"),
            encoding="utf-8",
        )
    return {
        "states": states,
        "new_shared_blob": blob_sha(modified_shared),
        "new_test_blob": blob_sha(modified_test),
        "only_three_reviewed_existing_files": True,
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = apply(dry_run=args.dry_run)
    print("PHASE174_R3R5_IMPL_SOURCE_GUARD=PASS")
    print("PHASE174_R3R5_IMPL_SHARED_BLOB=" + result["new_shared_blob"])
    print("PHASE174_R3R5_IMPL_TEST_BLOB=" + result["new_test_blob"])
    print("PHASE174_R3R5_IMPL_REVIEWED_CHANGES=3")
    if args.dry_run:
        print("PHASE174_R3R5_IMPL_DRY_RUN=PASS")
    else:
        print("PHASE174_R3R5_IMPL_SOURCE_PATCH=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
