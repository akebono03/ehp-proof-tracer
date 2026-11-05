"""Guarded R3-R6 patch: exact reviewed R3-R5 code and focused test contracts.

Only whole-function or unique guarded insertions are installed.  Source bytes
are pinned to the actual 174-3-5 Git commit, including an older local HEAD
with the identical R3-R5 worktree implementation.  No reset or merge occurs.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess
import tempfile

REVIEWED_HEAD = "7bd64d36e17246195525ecb0ec27a170abb73206"
PREVIOUS_HEAD = "45d97b2adc73c2347866de28b344fce1e6d2c095"
SHARED = "phase165_r52_r9_shared_math.py"
R3R4_TEST = "phase174_r3_r4_public_delta_connection/tests/test_connection.py"
R3R5_TEST = "phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py"
PREFLIGHT = "phase174_r3_r5_preflight/audit.py"
REVIEWED_BLOBS = {
    SHARED: "419e6fd2f5848777fec05f2048169bc2dc044f9d",
    R3R4_TEST: "e34c6c24a6a1de1a330c8a36d135e3bb87a8f633",
    R3R5_TEST: "f7351a47ce328603236f2dad71c8c8d886d79cd1",
    PREFLIGHT: "b309cdd38475e1c8643f757f93f0830903983b52",
}


def git(*args: str) -> bytes:
    return subprocess.run(("git",) + args, check=True, capture_output=True).stdout


def blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def reviewed_originals() -> dict[str, bytes]:
    """Check the reviewed production/test blobs, even before the local merge."""
    head = git("rev-parse", "HEAD").decode("ascii").strip()
    branch = git("branch", "--show-current").decode("utf-8").strip()
    remote = git("ls-remote", "origin", "refs/heads/develop").decode("ascii").split()
    if len(remote) != 2 or remote[1] != "refs/heads/develop":
        raise ValueError("Cannot confirm remote develop HEAD")
    if branch != "develop" or head not in (PREVIOUS_HEAD, REVIEWED_HEAD) or remote[0] != REVIEWED_HEAD:
        raise ValueError(
            "Reviewed R3-R6 HEAD mismatch: " + f"local={head} remote={remote[0]} expected={REVIEWED_HEAD}"
        )
    if git("diff", "--cached", "--name-only").strip():
        raise ValueError("Staged changes require review")
    changed = set(git("diff", "--name-only", "HEAD").decode("utf-8").splitlines())
    known_prior_worktree = set(REVIEWED_BLOBS)
    if changed - known_prior_worktree:
        raise ValueError("Unrelated user worktree changes: " + repr(sorted(changed - known_prior_worktree)))
    reviewed = {}
    for path, expected in REVIEWED_BLOBS.items():
        if head == REVIEWED_HEAD:
            data = git("show", "HEAD:" + path)
        elif path == SHARED:
            from phase174_r3_r5_finite_cyclic_extension.patch import insert_shared
            data = insert_shared(git("show", "HEAD:" + path))
        elif path == R3R4_TEST:
            from phase174_r3_r5_finite_cyclic_extension.patch import replace_r3r4_test
            data = replace_r3r4_test(git("show", "HEAD:" + path))
        elif path == PREFLIGHT:
            from phase174_r3_r5_finite_cyclic_extension.patch import replace_preflight_provider_guard
            data = replace_preflight_provider_guard(git("show", "HEAD:" + path))
        else:
            data = Path(path).read_bytes()
        if blob_sha(data) != expected:
            raise ValueError("Pinned reviewed Git blob differs: " + path)
        reviewed[path] = data
    return reviewed


def reviewed_shared_bytes() -> bytes:
    """Return the pinned full R3-R5 production file, not a guessed patch."""
    return reviewed_originals()[SHARED]


def _insert(original: bytes, old_text: str, new_text: str, description: str) -> bytes:
    ending = b"\r\n" if b"\r\n" in original else b"\n"
    old = old_text.encode("utf-8").replace(b"\n", ending)
    new = new_text.encode("utf-8").replace(b"\n", ending)
    if original.count(new) == 1 and original.count(old) == 0:
        return original
    if original.count(old) != 1 or original.count(new) != 0:
        raise ValueError("Reviewed insertion context changed: " + description)
    result = original.replace(old, new, 1)
    ast.parse(result.decode("utf-8-sig"))
    return result


def connect_shared(original: bytes) -> bytes:
    """Change just the two reviewed functions, never the root goal or renderer."""
    old_sources = (
        "        sources = sources + (build_cited_prop22_right_reference(production),)\n"
        "    registry = UnifiedStatementRegistry()\n"
    )
    new_sources = (
        "        sources = sources + (build_cited_prop22_right_reference(production),)\n"
        "        from phase174_r3_r6_source_extension.source import build_cited_extension_sources\n"
        "        sources = sources + (build_cited_extension_sources(),)\n"
        "    registry = UnifiedStatementRegistry()\n"
    )
    first = _insert(original, old_sources, new_sources, "source registration")
    old_expand = (
        "        options.extend(expand_toda48_index_two(goal))\n"
        "        options.extend(expand_finite_index_two_cyclic_structure(goal))\n"
        "        options.extend(expand_finite_cyclic_relation(goal))\n"
    )
    new_expand = (
        "        options.extend(expand_toda48_index_two(goal))\n"
        "        options.extend(expand_finite_index_two_cyclic_structure(goal))\n"
        "        from phase174_r3_r6_source_extension.source import expand_cited_toda55_double\n"
        "        options.extend(expand_cited_toda55_double(goal, tuple(available)))\n"
        "        options.extend(expand_finite_cyclic_relation(goal))\n"
    )
    return _insert(first, old_expand, new_expand, "universal doubled relation expansion")


def replace_r3r4_test(original: bytes) -> bytes:
    old = (
        "    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared\n"
        "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = replace_provider_call(old)\n"
        "    assert current in (r3r4, insert_shared(r3r4))\n"
    )
    new = (
        "    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared\n"
        "    from phase174_r3_r6_source_extension.patch import connect_shared\n"
        "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = replace_provider_call(old)\n"
        "    r3r5 = insert_shared(r3r4)\n"
        "    assert current in (r3r4, r3r5, connect_shared(r3r5))\n"
    )
    return _insert(original, old, new, "R3-R4 source-guard test")


def replace_r3r5_test(original: bytes) -> bytes:
    old = (
        "    # The source theorem is deliberately NOT created as a verified GIVEN.\n"
        "    assert not any(link.step is not None and link.step.conclusion == index_options[0].subgoals[1]\n"
        "                   for link in screened.proof_links)\n"
    )
    new = (
        "    # In R3-R6 only the general source formulae are GIVEN; concrete\n"
        "    # index-two and doubled relations still require independent inference.\n"
        "    from phase174_r3_r6_source_extension.source import Toda55UniversalDoubleStatement\n"
        "    assert any(link.step is not None and link.step.rule is ProofRule.GIVEN\n"
        "               and link.step.conclusion == index_options[0].subgoals[1]\n"
        "               for link in screened.proof_links)\n"
        "    assert any(link.step is not None and link.step.rule is ProofRule.GIVEN\n"
        "               and link.step.conclusion == Toda55UniversalDoubleStatement()\n"
        "               for link in screened.proof_links)\n"
        "    assert not any(link.step is not None and link.step.rule is ProofRule.GIVEN\n"
        "                   and link.step.conclusion in (goal, cyclic, index, double)\n"
        "                   for link in screened.proof_links)\n"
    )
    return _insert(original, old, new, "R3-R5 published source theorem test")


def _replace_function(original: bytes, function_name: str, replacement: str) -> bytes:
    normalized = original.decode("utf-8-sig").replace("\r\n", "\n")
    tree = ast.parse(normalized)
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == function_name]
    if len(found) != 1:
        raise ValueError("Expected exactly one function: " + function_name)
    node = found[0]
    lines = normalized.splitlines(keepends=True)
    expected_name = "def " + function_name + "("
    if not lines[node.lineno - 1].startswith(expected_name):
        raise ValueError("Unexpected function header")
    output = "".join(lines[:node.lineno - 1]) + replacement.rstrip("\n") + "\n" + "".join(lines[node.end_lineno:])
    ending = "\r\n" if b"\r\n" in original else "\n"
    data = output.replace("\n", ending).encode("utf-8")
    if original.startswith(b"\xef\xbb\xbf"):
        data = b"\xef\xbb\xbf" + data
    ast.parse(data.decode("utf-8-sig"))
    return data


PREFLIGHT_FUNCTION = '''def inspect_source_provider(root: Path) -> dict[str, Any]:
    """Check the exact reviewed R3-R5 or R3-R6 provider, not a loose substring."""
    file = root / SOURCE_FILE
    source = file.read_bytes()
    parsed = ast.parse(source.decode("utf-8-sig"))
    functions = [
        node for node in parsed.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise ValueError("shared_expansion_provider must have one definition")
    if source.count(DELTA_HOOK.encode("utf-8")) != 1:
        raise ValueError("R3-R4 general Delta-zero hook is absent or duplicated")
    from phase174_r3_r6_source_extension.patch import reviewed_shared_bytes, connect_shared
    reviewed = reviewed_shared_bytes()
    if source not in (reviewed, connect_shared(reviewed)):
        raise ValueError("Unreviewed production source modifications")
    head = run_git("rev-parse", "HEAD")
    state = "COMMITTED" if head == "7bd64d36e17246195525ecb0ec27a170abb73206" and source == reviewed else "WORKTREE_PATCHED"
    return {
        "state": state,
        "delta_provider_hook_present": True,
        "full_function_line_count": functions[0].end_lineno - functions[0].lineno + 1,
        "production_source_changed_by_this_audit": False,
    }
'''


def replace_preflight_audit(original: bytes) -> bytes:
    return _replace_function(original, "inspect_source_provider", PREFLIGHT_FUNCTION)


def full_function(data: bytes, function_name: str) -> str:
    text = data.decode("utf-8-sig").replace("\r\n", "\n")
    lines = text.splitlines()
    hits = [n for n in ast.parse(text).body
            if isinstance(n, ast.FunctionDef) and n.name == function_name]
    if len(hits) != 1:
        raise ValueError("Cannot export complete replacement function: " + function_name)
    return "\n".join(lines[hits[0].lineno - 1:hits[0].end_lineno]) + "\n"


def install(*, dry_run: bool) -> dict[str, object]:
    reviewed = reviewed_originals()
    modified = {
        SHARED: connect_shared(reviewed[SHARED]),
        R3R4_TEST: replace_r3r4_test(reviewed[R3R4_TEST]),
        R3R5_TEST: replace_r3r5_test(reviewed[R3R5_TEST]),
        PREFLIGHT: replace_preflight_audit(reviewed[PREFLIGHT]),
    }
    states = {}
    for path, before in reviewed.items():
        current = Path(path).read_bytes()
        if current == before:
            states[path] = "REVIEWED_R3R5"
        elif current == modified[path]:
            states[path] = "ALREADY_R3R6"
        else:
            raise ValueError("Refusing unrelated user changes to " + path)
    if not dry_run:
        for path, after in modified.items():
            if states[path] == "REVIEWED_R3R5":
                Path(path).write_bytes(after)
        for path, after in modified.items():
            if Path(path).read_bytes() != after:
                raise ValueError("Installed file differs from reviewed replacement: " + path)
        folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
        folder = folder / "EHPProofTracerAudit" / "phase174_r3_r6"
        folder.mkdir(parents=True, exist_ok=True)
        functions = (
            (SHARED, "build_shared_typed_bridge"),
            (SHARED, "shared_expansion_provider"),
            (R3R4_TEST, "test_r3r4_real_production_file_has_only_reviewed_wiring"),
            (R3R5_TEST, "test_public_pi85_cyclic_root_and_delta_proposals_reached"),
            (PREFLIGHT, "inspect_source_provider"),
        )
        for path, name in functions:
            output = folder / (name + "_FULL.py")
            output.write_text(full_function(modified[path], name), encoding="utf-8")
    return {
        "changed": tuple(modified),
        "states": states,
        "blobs": {path: blob_sha(data) for path, data in modified.items()},
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = install(dry_run=args.dry_run)
    print("PHASE174_R3R6_REVIEWED_HEAD=" + REVIEWED_HEAD)
    print("PHASE174_R3R6_EXISTING_FILES=" + str(len(result["changed"])))
    for path, sha in result["blobs"].items():
        print("PHASE174_R3R6_PATCH_BLOB " + path + " " + sha)
    print("PHASE174_R3R6_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6_DRY_RUN=PASS" if args.dry_run else "PHASE174_R3R6_PATCH=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
