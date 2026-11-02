"""Review-bound, single-function public search connection installer.

The existing R4-R7R2 working-tree modification is preserved and verified.
No Git operation modifies HEAD, index, or any file beyond the one target.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
from pathlib import Path
import subprocess

REVIEWED_HEAD = "72c66346b07cfc5517543627e010fd0db9842274"
TARGET = "phase165_r52_r9_shared_math.py"
PREVIOUS_PATCH = "phase173_r4_r7_source_first_rule/source.py"
TARGET_GIT_BLOB = "3e4c5f9c62b04d618f845b0f82d1cb1cacccdf2e"
PREVIOUS_GIT_BLOB = "abdc05c731e5ede1258962705bc577b5307b6f38"
PREVIOUS_WORKTREE_BLOB = "abdc05c731e5ede1258962705bc577b5307b6f38"
REVIEWED_FILES = {
    TARGET: TARGET_GIT_BLOB,
    PREVIOUS_PATCH: PREVIOUS_GIT_BLOB,
    "phase173_r4_r7r2_pi84_prior_selection/tests/test_context.py": "e4583931efae67cb96efa683b5be31e93fc4fbdd",
    "phase173_r4_r7r2_pi84_prior_selection/verify.py": "e7b349db5902c9821fb1d17159ce8c0733c9de89",
    "phase173_r4_r7_source_first_rule/rule.py": "5113c88e263c28b748c1543ec57bbcedb3eff5bf",
    "phase173_r4_r7_source_first_rule/tests/test_rule.py": "24f8be3c1407ba653547b2b987efa904fdb58347",
    "phase173_r4_r7r1_pi84_premise_diagnostic/audit.py": "bcaf8feb008113eba0e8cdc1661f9ed931728c92",
    "phase173_r4_r1_public_connection/route.py": "fa79655aa24a88d5e7dd46d8c7a00ae04aeb15d4",
    "phase173_r4_r1_public_connection/verify.py": "9bf5bb6eee4d6d3428da68f40c9cda9370ee20cf",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
}
ANCHOR = (
    "    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation\n"
    "    proof_context = prefer_universal_prop42_derivation(proof_context)\n"
    "    if context_sink is not None:\n"
)
INSERTION = (
    "    # Phase 173 R4-R8: reuse only the three isolated, source-verified Toda (5.6) roots.\n"
    "    if n == 4 and k in (4, 5, 6) and expansion_provider is None and citing_assertion_id is None:\n"
    "        from phase173_r4_r8_public_connection.route import (\n"
    "            prepare_pi4_higher_public_connection,\n"
    "        )\n"
    "        pi4_higher_connection = prepare_pi4_higher_public_connection(\n"
    "            bridge=bridge, goal=goal,\n"
    "            prior_conclusions=tuple(item.root.conclusion for item in prior),\n"
    "        )\n"
    "        if pi4_higher_connection is not None:\n"
    "            proof_context, expansion_provider = pi4_higher_connection\n"
)
HOOK = INSERTION


def git(root: Path, *arguments: str) -> str:
    run = subprocess.run(
        ("git", *arguments), cwd=root, check=False, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
    )
    if run.returncode:
        raise RuntimeError("git " + " ".join(arguments) + ": " + run.stderr[:500])
    return run.stdout.strip()


def blob_hash(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def _function(source: str) -> str:
    parsed = ast.parse(source)
    matches = [node for node in parsed.body if isinstance(node, ast.FunctionDef)
               and node.name == "search_shared_group_goal"]
    if len(matches) != 1:
        raise RuntimeError("expected one canonical search function")
    selected = matches[0]
    return "".join(source.splitlines(keepends=True)[selected.lineno - 1:selected.end_lineno])


def transform(source: bytes) -> bytes:
    """Insert the only hook after existing screening, preserving original EOL."""
    normalized = normalize(source).decode("utf-8")
    if normalized.count(HOOK) == 1:
        raise RuntimeError("R4-R8 connector already installed")
    if normalized.count(ANCHOR) != 1:
        raise RuntimeError("canonical screen anchor is not unique")
    proposed = normalized.replace(ANCHOR, ANCHOR.replace(
        "    if context_sink is not None:\n", INSERTION + "    if context_sink is not None:\n",
    ))
    ast.parse(proposed)
    full = Path(__file__).with_name("search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    if ast.dump(ast.parse(_function(proposed)), include_attributes=False) != ast.dump(
        ast.parse(full), include_attributes=False,
    ):
        raise RuntimeError("full replacement function is not the verified patch")
    result = proposed.encode("utf-8")
    if b"\r\n" in source:
        result = result.replace(b"\n", b"\r\n")
    return result


def committed_bytes(root: Path, name: str) -> bytes:
    result = subprocess.run(
        ("git", "show", "HEAD:" + name), cwd=root, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("committed source unavailable: " + name)
    return result.stdout


def preflight(root: Path, *, remote: bool) -> str:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("not repository root")
    if (git(root, "branch", "--show-current") != "develop"
            or git(root, "rev-parse", "HEAD") != REVIEWED_HEAD):
        raise RuntimeError("unreviewed develop HEAD")
    for name, blob in REVIEWED_FILES.items():
        if not (root / name).is_file() or git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("unreviewed committed source: " + name)
    if remote:
        found = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not found or found.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("GitHub develop has changed")
    if blob_hash(normalize((root / PREVIOUS_PATCH).read_bytes())) != PREVIOUS_WORKTREE_BLOB:
        raise RuntimeError("R4-R7R2 source correction is absent or changed")
    differences = set(git(root, "diff", "--name-only").splitlines())
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes must be reviewed separately")
    source = (root / TARGET).read_bytes()
    committed = committed_bytes(root, TARGET)
    if blob_hash(committed) != TARGET_GIT_BLOB:
        raise RuntimeError("committed target blob failed content check")
    expected = transform(committed)
    if HOOK.encode("utf-8") in normalize(source):
        if differences != {TARGET}:
            raise RuntimeError("unexpected tracked changes after R4-R8 install")
        if normalize(source) != normalize(expected):
            raise RuntimeError("installed R4-R8 source is not the reviewed replacement")
        return "ALREADY_INSTALLED"
    if differences:
        raise RuntimeError("unexpected tracked changes before R4-R8 install")
    if normalize(source) != normalize(committed):
        raise RuntimeError("target source has unreviewed working-tree content")
    return "NEEDS_INSTALL"


def install(root: Path, *, dry_run: bool, remote: bool) -> str:
    state = preflight(root, remote=remote)
    print("PHASE173_R4_R8_REVIEWED_HEAD=" + REVIEWED_HEAD, flush=True)
    print("PHASE173_R4_R8_INSTALL_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE173_R4_R8_RESULT=DRY_RUN_PASS", flush=True)
        return state
    if state == "NEEDS_INSTALL":
        path = root / TARGET
        prior = path.read_bytes()
        try:
            path.write_bytes(transform(prior))
            if preflight(root, remote=False) != "ALREADY_INSTALLED":
                raise RuntimeError("post-install guard refused the patch")
        except BaseException:
            path.write_bytes(prior)
            raise
    print("PHASE173_R4_R8_RESULT=INSTALLED", flush=True)
    return state


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", required=True, type=Path)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-remote-check", action="store_true")
    args = p.parse_args()
    try:
        install(args.root.resolve(), dry_run=args.dry_run,
                remote=not args.skip_remote_check)
    except Exception as exc:
        print("PHASE173_R4_R8_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
