"""Guarded single-function patch; preserve reviewed R7 and R8 hooks."""
from __future__ import annotations

import argparse
import ast
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
PATH_IN_GIT = "phase165_r52_r9_shared_math.py"
REVIEWED_ORIGINAL_BLOB_SHA = "68846671215c38e3e0a572932b8ed955a7880edc"
R7_HOOK = (
    "        from phase171_r2j_r4_r9_r7_public_cyclic_root.source import (\n"
    "            expand_cited_double_cyclic_root,\n"
    "        )\n"
    "        options.extend(expand_cited_double_cyclic_root(goal, tuple(available)))\n"
)
R8_HOOK = (
    "        from phase171_r2j_r4_r9_r8_public_cardinality.source import (\n"
    "            expand_cited_ehp_middle_cardinality,\n"
    "        )\n"
    "        options.extend(expand_cited_ehp_middle_cardinality(goal, tuple(available)))\n"
)
R9_HOOK = (
    "        from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import (\n"
    "            expand_cited_full_order_cyclic_structure,\n"
    "        )\n"
    "        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))\n"
)


def _git(*args: str) -> bytes:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("show", f"HEAD:{PATH_IN_GIT}"),
    }
    if args not in permitted:
        raise ValueError("read-only reviewed Git operations only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=True,
    ).stdout


def _clean_text(blob: bytes) -> str:
    return blob.decode("utf-8-sig").replace("\r\n", "\n")


def _git_blob_sha(blob: bytes) -> str:
    return hashlib.sha1(f"blob {len(blob)}\0".encode() + blob).hexdigest()


def _function_text(source: str) -> str:
    tree = ast.parse(source)
    selected = [
        item for item in tree.body
        if isinstance(item, ast.FunctionDef)
        and item.name == "shared_expansion_provider"
    ]
    if len(selected) != 1:
        raise RuntimeError("expected exactly one existing shared provider function")
    node = selected[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def install(*, dry_run: bool) -> bool:
    """Check exact reviewed baseline and in-worktree R7/R8 before insertion."""
    if _git("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("shared provider is missing")
    head_bytes = _git("show", f"HEAD:{PATH_IN_GIT}")
    head_text = _clean_text(head_bytes)
    # HEAD may contain R7 and R8 if committed; do not accept unrelated edits.
    if any(head_text.count(hook) > 1 for hook in (R7_HOOK, R8_HOOK, R9_HOOK)):
        raise RuntimeError("duplicate previously committed provider hook")
    head_newline = "\r\n" if b"\r\n" in head_bytes else "\n"
    baseline_bytes = head_bytes
    for hook in (R7_HOOK, R8_HOOK, R9_HOOK):
        baseline_bytes = baseline_bytes.replace(
            hook.replace("\n", head_newline).encode("utf-8"), b"",
        )
    if _git_blob_sha(baseline_bytes) != REVIEWED_ORIGINAL_BLOB_SHA:
        raise RuntimeError("HEAD provider differs from reviewed GitHub source")
    original_bytes = TARGET.read_bytes()
    current = _clean_text(original_bytes)
    expected = head_text
    anchor = "        options.extend(expand_finite_cyclic_relation(goal))\n"
    if R7_HOOK not in expected:
        if expected.count(anchor) != 1:
            raise RuntimeError("R7 insertion anchor is not unique")
        expected = expected.replace(anchor, anchor + R7_HOOK, 1)
    if R8_HOOK not in expected:
        if expected.count(R7_HOOK) != 1:
            raise RuntimeError("R7 prerequisite is ambiguous")
        expected = expected.replace(R7_HOOK, R7_HOOK + R8_HOOK, 1)
    if any(expected.count(hook) != 1 for hook in (R7_HOOK, R8_HOOK)):
        raise RuntimeError("R7/R8 prerequisite is absent")
    if R9_HOOK not in expected:
        expected_with_r9 = expected.replace(R8_HOOK, R8_HOOK + R9_HOOK, 1)
    else:
        expected_with_r9 = expected
    if current == expected and R9_HOOK not in expected:
        state = "READY_TO_PATCH"
    elif current == expected_with_r9:
        state = "ALREADY_INSTALLED"
    else:
        raise RuntimeError("unknown tracked provider changes; refusing overwrite")
    next_text = expected_with_r9
    if any(next_text.count(hook) != 1 for hook in (R7_HOOK, R8_HOOK, R9_HOOK)):
        raise RuntimeError("required hook is missing or duplicated")
    function = _function_text(next_text)
    if any(hook not in function for hook in (R7_HOOK, R8_HOOK, R9_HOOK)):
        raise RuntimeError("patch escaped the shared provider function")
    ast.parse(next_text)
    print("PHASE171_R2J_R4_R9_R9_HEAD=" + _git("rev-parse", "HEAD").decode().strip(), flush=True)
    print("PHASE171_R2J_R4_R9_R9_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R9_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if state == "READY_TO_PATCH":
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(original_bytes)
        newline = "\r\n" if b"\r\n" in original_bytes else "\n"
        bom = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
        TARGET.write_bytes(bom + next_text.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R9_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(function + "\n", encoding="utf-8")
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R9_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R9_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return state == "READY_TO_PATCH"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
