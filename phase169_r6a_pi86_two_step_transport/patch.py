"""R6A one-function patch, pinned to GitHub-reviewed source blobs."""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OUTPUT = PACKAGE / "output"
EXPECTED_BLOB = "9a8a6fdf0f54e7639fe798665e7f7869dfbd8156"
OLD = (
    "        options.extend(expand_prior_cited_toda45_composite_transport(\n"
    "            goal, tuple(available), bridge, proof_target=proof_target,\n"
    "        ))\n"
)
NEW = OLD + (
    "        from phase169_r6a_pi86_two_step_transport.rule import (\n"
    "            expand_prior_two_step_eta_square_transport,\n"
    "        )\n"
    "        options.extend(expand_prior_two_step_eta_square_transport(\n"
    "            goal, tuple(available), bridge, proof_target=proof_target,\n"
    "        ))\n"
)


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
    ).stdout


def normalized(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n")


def patched_content(current: bytes, committed: bytes) -> bytes:
    """Require an unchanged committed provider, then patch one audited anchor."""
    if normalized(current) != normalized(committed):
        raise RuntimeError("provider working content differs from its Git baseline")
    original = normalized(current).decode("utf-8")
    if original.count(OLD) != 1 or NEW in original:
        raise RuntimeError("R5B anchor missing, duplicated, or already patched")
    changed = original.replace(OLD, NEW, 1)
    ast.parse(changed)
    newline = "\r\n" if b"\r\n" in current else "\n"
    return changed.replace("\n", newline).encode("utf-8")


def full_function(data: bytes) -> str:
    """Return the entire amended public provider function."""
    source = normalized(data).decode("utf-8")
    tree = ast.parse(source)
    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise RuntimeError("shared_expansion_provider function not uniquely located")
    node = functions[0]
    return "\n".join(source.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def main() -> None:
    branch = git("branch", "--show-current").decode().strip()
    if branch != "develop":
        raise RuntimeError("R6A patch requires develop branch")
    blob = git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py").decode().strip()
    if blob != EXPECTED_BLOB:
        raise RuntimeError("provider Git blob changed; review current source before patch")
    original = TARGET.read_bytes()
    result = patched_content(original, git("show", "HEAD:phase165_r52_r9_shared_math.py"))
    OUTPUT.mkdir(exist_ok=True)
    before = OUTPUT / "phase165_r52_r9_shared_math.py.before"
    after = OUTPUT / "phase165_r52_r9_shared_math.py.FULL"
    full = OUTPUT / "shared_expansion_provider_FULL.py"
    before.write_bytes(original)
    after.write_bytes(result)
    full.write_text(full_function(result), encoding="utf-8")
    TARGET.write_bytes(result)
    print("R6A_PATCHED=phase165_r52_r9_shared_math.py")
    print("R6A_BACKUP=" + str(before))
    print("R6A_FULL_FUNCTION=" + str(full))
    print("R6A_FULL_FILE=" + str(after))


if __name__ == "__main__":
    main()
