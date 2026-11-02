"""Guarded and idempotent installer for one public search function addition."""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1, sha256
import os
from pathlib import Path
import shutil
import subprocess

TARGET = Path("phase165_r52_r9_shared_math.py")
EXPECTED_TARGET_BLOB = "2718c55789af7f442ac2c086d016d3d6f7ca3133"
REVIEWED_DIAGONAL_HEADS = (
    "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
    "e05ada41cbcf53e8b755428afd245ba2da619fa8",
)
REVIEWED_DIAGONAL_PATCH_SHA256 = (
    "1d63582af0e1632ac733e9dcb764a2afd6a1c3583f00acb88b56ce8b0d8964ce"
)
EXPECTED_DEPENDENCIES = {
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
ANCHOR = (
    "    if bridge is None:\n"
    "        bridge = build_shared_typed_bridge()\n"
    "    assertions = tuple(bridge.registry._assertions.values())\n"
)
HOOK = (
    "    if n == 4 and k == 3 and expansion_provider is None:\n"
    "        from phase173_r4_r1_public_connection.route import (\n"
    "            prepare_pi74_public_connection,\n"
    "        )\n"
    "        pi74_connection = prepare_pi74_public_connection(\n"
    "            bridge=bridge, goal=goal, citing_assertion_id=citing_assertion_id,\n"
    "            prior_conclusions=tuple(item.root.conclusion for item in prior),\n"
    "        )\n"
    "        if pi74_connection is not None:\n"
    "            bridge, citing_assertion_id, expansion_provider = pi74_connection\n"
)


def run_git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ("git", *arguments), cwd=root, capture_output=True, check=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def committed_bytes(root: Path, path: str) -> bytes:
    return subprocess.run(
        ("git", "show", "HEAD:" + path), cwd=root, capture_output=True,
        check=True,
    ).stdout


def blob_hash(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def transform(source: str) -> str:
    if HOOK in source:
        raise RuntimeError("Public hook already exists")
    if source.count(ANCHOR) != 1:
        raise RuntimeError("Reviewed function anchor does not occur exactly once")
    function = [
        node for node in ast.parse(source).body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "search_shared_group_goal"
    ]
    if len(function) != 1:
        raise RuntimeError("Exactly one canonical search function is required")
    lines = source.splitlines(keepends=True)
    start, end = function[0].lineno, function[0].end_lineno
    section = "".join(lines[start - 1:end])
    if section.count(ANCHOR) != 1:
        raise RuntimeError("Anchor is outside the reviewed canonical function")
    patched = source.replace(ANCHOR, ANCHOR.replace(
        "    assertions = tuple(bridge.registry._assertions.values())\n",
        HOOK + "    assertions = tuple(bridge.registry._assertions.values())\n",
    ), 1)
    ast.parse(patched)
    return patched


def restored_source(source: str, committed: bytes | None = None) -> str:
    if source.count(HOOK) != 1:
        raise RuntimeError("An installed hook is absent or duplicated")
    restored = source.replace(HOOK, "", 1)
    if committed is None or restored.encode("utf-8") != normalize(committed):
        raise RuntimeError("Installed public search has unreviewed other changes")
    return restored


def preflight(root: Path) -> tuple[str, bytes]:
    if run_git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only develop is eligible")
    if run_git(root, "rev-parse", "HEAD") != run_git(root, "rev-parse", "origin/develop"):
        raise RuntimeError("Local HEAD and origin/develop differ; stop without modifying")
    for path, expected in {TARGET.as_posix(): EXPECTED_TARGET_BLOB,
                           **EXPECTED_DEPENDENCIES}.items():
        if run_git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Git reviewed dependency changed: " + path)
        if path != TARGET.as_posix() and normalize((root / path).read_bytes()) != normalize(committed_bytes(root, path)):
            raise RuntimeError("Reviewed dependency worktree changed: " + path)
    diagonal = "phase173_r4_r1_source_bound_56/rule.py"
    if run_git(root, "rev-parse", "HEAD:" + diagonal) not in REVIEWED_DIAGONAL_HEADS:
        raise RuntimeError("Unreviewed committed Toda (5.6) rule")
    diagonal_source = normalize((root / diagonal).read_bytes())
    diagonal_verified = (
        (run_git(root, "rev-parse", "HEAD:" + diagonal) == REVIEWED_DIAGONAL_HEADS[0]
         and diagonal_source == normalize(committed_bytes(root, diagonal)))
        or sha256(diagonal_source).hexdigest() == REVIEWED_DIAGONAL_PATCH_SHA256
    )
    if not diagonal_verified or b"SourceBoundGoal(diagonal, diagonal_source)" not in diagonal_source:
        raise RuntimeError("Reviewed inferred diagonal rule is not installed")
    if run_git(root, "diff", "--cached", "--name-only", "--", TARGET.as_posix()):
        raise RuntimeError("Refusing to overwrite staged search function")
    current = (root / TARGET).read_bytes()
    content = normalize(current).decode("utf-8")
    committed = normalize(committed_bytes(root, TARGET.as_posix()))
    if content.encode("utf-8") == committed:
        _ = transform(content)
        return "NEW", current
    restored_source(content, committed)
    return "ALREADY_INSTALLED", current


def install(root: Path) -> str:
    state, current = preflight(root)
    if state == "ALREADY_INSTALLED":
        return state
    edited = transform(normalize(current).decode("utf-8"))
    updated = edited.replace("\n", "\r\n").encode("utf-8") if b"\r\n" in current else edited.encode("utf-8")
    backup = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_public_connection/"
        + sha256(current).hexdigest() + ".py"
    )
    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists() and backup.read_bytes() != current:
        raise RuntimeError("Existing backup differs; refusing to overwrite")
    if not backup.exists():
        shutil.copy2(root / TARGET, backup)
    (root / TARGET).write_bytes(updated)
    return "INSTALLED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    state, _ = preflight(root)
    print("PHASE173_R4_R1_PUBLIC_SOURCE_GUARD=PASS")
    print("PHASE173_R4_R1_PUBLIC_PATCH_STATE=" + state)
    if args.dry_run:
        print("PHASE173_R4_R1_PUBLIC_DRY_RUN=PASS")
        return 0
    print("PHASE173_R4_R1_PUBLIC_INSTALL=" + install(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
