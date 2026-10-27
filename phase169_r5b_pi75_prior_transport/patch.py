"""Fail-closed one-function integration for Phase 169 R5B."""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OUTPUT = PACKAGE / "output"
EXPECTED_GIT_BLOB = "2dff86c7414bf2f3bada6c27ecc3c5e601228e33"
OLD = (
    "        options.extend(expand_cited_toda45_composite_transport(\n"
    "            goal, tuple(available),\n"
    "        ))\n"
)
NEW = OLD + (
    "        from phase169_r5b_pi75_prior_transport.rule import (\n"
    "            expand_prior_cited_toda45_composite_transport,\n"
    "        )\n"
    "        options.extend(expand_prior_cited_toda45_composite_transport(\n"
    "            goal, tuple(available), bridge, proof_target=proof_target,\n"
    "        ))\n"
)


def git(*arguments: str) -> bytes:
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True,
    ).stdout


def normalized(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n")


def build_patched_provider(current: bytes, committed: bytes) -> bytes:
    """Replace exactly one expansion anchor; reject unreviewed code changes."""
    if normalized(current) != normalized(committed):
        raise RuntimeError("working provider differs from its committed baseline")
    newline = b"\r\n" if b"\r\n" in current else b"\n"
    content = normalized(current).decode("utf-8")
    if content.count(OLD) != 1 or NEW in content:
        raise RuntimeError("R3O provider anchor changed or was already patched")
    result = content.replace(OLD, NEW, 1)
    ast.parse(result)
    return result.replace("\n", newline.decode("ascii")).encode("utf-8")


def full_function(source: bytes) -> str:
    """Export the complete changed function for replaceable review."""
    content = normalized(source).decode("utf-8")
    tree = ast.parse(content)
    matches = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "shared_expansion_provider"
    ]
    if len(matches) != 1:
        raise RuntimeError("cannot locate full shared_expansion_provider function")
    node = matches[0]
    return "\n".join(content.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def main() -> None:
    branch = git("branch", "--show-current").decode().strip()
    if branch != "develop":
        raise RuntimeError("R5B requires the develop branch")
    blob = git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py").decode().strip()
    if blob != EXPECTED_GIT_BLOB:
        raise RuntimeError("provider Git blob changed; re-audit before patching")
    committed = git("show", "HEAD:phase165_r52_r9_shared_math.py")
    current = TARGET.read_bytes()
    patched = build_patched_provider(current, committed)
    OUTPUT.mkdir(exist_ok=True)
    backup = OUTPUT / "phase165_r52_r9_shared_math.py.before"
    backup.write_bytes(current)
    (OUTPUT / "phase165_r52_r9_shared_math.py.FULL").write_bytes(patched)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(
        full_function(patched), encoding="utf-8",
    )
    TARGET.write_bytes(patched)
    print("R5B_PATCHED=phase165_r52_r9_shared_math.py")
    print("R5B_BACKUP=" + str(backup))
    print("R5B_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"))
    print("R5B_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.py.FULL"))


if __name__ == "__main__":
    main()
