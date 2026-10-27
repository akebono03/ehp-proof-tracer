"""Fail-closed verification of the committed R4B/R4C production wiring.

This program never patches, checks out, stages, or writes repository source.
It tolerates future unrelated Git commits when the audited file blobs remain
unchanged, but rejects modifications to the audited source files.
"""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEWED_FILES = {
    "phase165_r52_r9_shared_math.py": "2dff86c7414bf2f3bada6c27ecc3c5e601228e33",
    "phase169_r4b_prop44_injectivity/rule.py": "aba4c769f2e6bc9a3359c2f8e4b4fa7d869aac4b",
    "phase169_r4c_pi64_suspension_iso/rule.py": "c5cc2190d243997fccb11751f5d530bf8fc12085",
    "phase169_r4c_pi64_suspension_iso/audit.py": "6c125c34473467d2cb70c6e9146f8d772758b724",
    "phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py": "165bd5dee76978dd5d3f0cca40b4890f14b9257b",
}
R4B_INSERT = (
    "        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity\n"
    "        options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))\n"
)
R4C_INSERT = (
    "        from phase169_r4c_pi64_suspension_iso.rule import expand_pi64_suspension_isomorphism\n"
    "        options.extend(expand_pi64_suspension_isomorphism(goal))\n"
)


def normalized_text(data: bytes) -> str:
    """Normalize Windows line endings without relaxing any source content."""
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def verify_provider_source(source: str) -> None:
    """Accept only one adjacent R4B/R4C pair inside the shared provider."""
    if source.count(R4B_INSERT) != 1 or source.count(R4C_INSERT) != 1:
        raise RuntimeError("missing or duplicated R4B/R4C expansion connection")
    if source.count(R4B_INSERT + R4C_INSERT) != 1:
        raise RuntimeError("R4C insertion is not immediately after reviewed R4B insertion")
    tree = ast.parse(source, filename="phase165_r52_r9_shared_math.py")
    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise RuntimeError("shared_expansion_provider is not unique")
    function = functions[0]
    function_text = "".join(source.splitlines(keepends=True)[function.lineno - 1:function.end_lineno])
    if function_text.count(R4B_INSERT + R4C_INSERT) != 1:
        raise RuntimeError("R4C is not wired inside shared_expansion_provider")


def git(*arguments: str, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True, capture_output=True,
    )
    return completed.stdout if binary else completed.stdout.decode("utf-8").strip()


def verify_committed_state() -> str:
    """Verify tracked blobs and the worktree; never assume a HEAD commit hash."""
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Phase 169 R4C2 must run on develop")
    head = git("rev-parse", "HEAD")
    for path, expected_blob in REVIEWED_FILES.items():
        actual_blob = git("rev-parse", "HEAD:" + path)
        if actual_blob != expected_blob:
            raise RuntimeError(
                f"reviewed source changed at HEAD: {path}; expected {expected_blob}, got {actual_blob}"
            )
        source_at_head = git("show", "HEAD:" + path, binary=True)
        current = ROOT / path
        if not current.is_file():
            raise RuntimeError(f"required tracked file is missing: {path}")
        if normalized_text(current.read_bytes()) != normalized_text(source_at_head):
            raise RuntimeError(f"reviewed source differs from HEAD: {path}")
        if path == "phase165_r52_r9_shared_math.py":
            verify_provider_source(normalized_text(source_at_head))
    return head


def main() -> None:
    head = verify_committed_state()
    print("R4C2_GIT_BRANCH=develop")
    print("R4C2_GIT_HEAD=" + head)
    print("R4C2_BASELINE=R4C_COMMITTED")
    print("R4C2_PATCH_SKIPPED=True")
    print("R4C2_REVIEWED_FILES_VERIFIED=" + str(len(REVIEWED_FILES)))


if __name__ == "__main__":
    main()
