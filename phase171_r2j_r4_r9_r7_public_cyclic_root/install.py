"""One-function guarded shared-provider patch and full-code export."""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
ANCHOR = "        options.extend(expand_finite_cyclic_relation(goal))\n"
ADDITION = (
    "        from phase171_r2j_r4_r9_r7_public_cyclic_root.source import (\n"
    "            expand_cited_double_cyclic_root,\n"
    "        )\n"
    "        options.extend(expand_cited_double_cyclic_root(goal, tuple(available)))\n"
)


def _git(*args: str) -> str:
    if args not in {
        ("branch", "--show-current"),
        ("status", "--porcelain", "--untracked-files=no"),
        ("rev-parse", "HEAD"),
    }:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout.strip()


def _function_text(source: str) -> str:
    tree = ast.parse(source)
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise RuntimeError("expected one shared_expansion_provider function")
    node = functions[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def install(*, dry_run: bool) -> bool:
    if _git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("shared math provider missing")
    original_bytes = TARGET.read_bytes()
    prefix = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
    raw = original_bytes[len(prefix):]
    if b"\r\n" in raw:
        newline = "\r\n"
    else:
        newline = "\n"
    content = raw.decode("utf-8").replace("\r\n", "\n")
    if content.count(ANCHOR) != 1:
        raise RuntimeError("shared provider hook anchor missing or ambiguous")
    already = ADDITION in content
    if already:
        proposed = content
        state = "ALREADY_INSTALLED"
    else:
        if "phase171_r2j_r4_r9_r7_public_cyclic_root.source" in content:
            raise RuntimeError("partial/unknown prior hook detected")
        # Refuse to overlay pre-existing tracked changes.
        if _git("status", "--porcelain", "--untracked-files=no"):
            raise RuntimeError("tracked worktree must be clean before patch")
        proposed = content.replace(ANCHOR, ANCHOR + ADDITION, 1)
        state = "READY_TO_PATCH"
    # Confirm the generated hook is INSIDE the intended function.
    function = _function_text(proposed)
    if ADDITION not in function:
        raise RuntimeError("insertion escaped shared_expansion_provider")
    if proposed.count(ADDITION) != 1:
        raise RuntimeError("duplicate provider hook")
    ast.parse(proposed)
    print("PHASE171_R2J_R4_R9_R7_HEAD=" + _git("rev-parse", "HEAD"), flush=True)
    print("PHASE171_R2J_R4_R9_R7_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R7_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if not already:
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(original_bytes)
        TARGET.write_bytes(prefix + proposed.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R7_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    # Full replacement units as requested by the project development rules.
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(
        function + "\n", encoding="utf-8",
    )
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R7_FULL_FUNCTION=" + str(
        OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R7_FULL_FILE=" + str(
        OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return not already


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
