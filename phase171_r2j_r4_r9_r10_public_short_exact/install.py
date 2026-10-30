"""Guarded minimal provider patch for the already implemented EHP short-exact rule.

The installer recognizes only the reviewed baseline and the exact R7/R8/R9/R10
hooks. It neither resets Git nor overwrites an unknown tracked modification.
"""
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
GIT_TARGET = "phase165_r52_r9_shared_math.py"
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
R10_HOOK = (
    "        from phase171_r2j_r4_r5_short_exact_sequence.source import expand_ehp_short_exact\n"
    "        options.extend(expand_ehp_short_exact(goal))\n"
)
HOOKS = (R7_HOOK, R8_HOOK, R9_HOOK, R10_HOOK)


def _git(*arguments: str) -> bytes:
    """Allow only read operations and an explicit tracked HEAD file."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("show", f"HEAD:{GIT_TARGET}"),
    }
    if arguments not in allowed:
        raise ValueError("only read-only reviewed Git commands are allowed")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, check=True,
    ).stdout


def _normal(blob: bytes) -> str:
    """Normalize CRLF and optional UTF-8 BOM for exact source inspection."""
    return blob.decode("utf-8-sig").replace("\r\n", "\n")


def _git_blob_sha(blob: bytes) -> str:
    """Compute the exact Git blob identity of an untouched reviewed file."""
    return hashlib.sha1(f"blob {len(blob)}\0".encode("ascii") + blob).hexdigest()


def _complete_function(source: str) -> str:
    """Extract the full original function with no code abbreviation."""
    candidates = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(candidates) != 1:
        raise RuntimeError("expected a unique shared_expansion_provider function")
    node = candidates[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def _verified_source_and_state(head_bytes: bytes, current_bytes: bytes) -> tuple[str, str]:
    """Accept only the reviewed R7/R8/R9 chain, optionally with R10 already in it."""
    head_text = _normal(head_bytes)
    current = _normal(current_bytes)
    head_newline = "\r\n" if b"\r\n" in head_bytes else "\n"
    raw_reviewed = head_bytes
    for hook in HOOKS:
        if head_text.count(hook) > 1:
            raise RuntimeError("duplicate provider hook in HEAD")
        raw_reviewed = raw_reviewed.replace(
            hook.replace("\n", head_newline).encode("utf-8"), b"",
        )
    if _git_blob_sha(raw_reviewed) != REVIEWED_ORIGINAL_BLOB_SHA:
        raise RuntimeError("HEAD provider differs from reviewed GitHub baseline")
    expected = head_text
    anchor = "        options.extend(expand_finite_cyclic_relation(goal))\n"
    for index, hook in enumerate((R7_HOOK, R8_HOOK, R9_HOOK)):
        preceding = anchor if index == 0 else HOOKS[index - 1]
        if hook not in expected:
            if expected.count(preceding) != 1:
                raise RuntimeError("reviewed predecessor hook is absent or ambiguous")
            expected = expected.replace(preceding, preceding + hook, 1)
    if any(expected.count(hook) != 1 for hook in (R7_HOOK, R8_HOOK, R9_HOOK)):
        raise RuntimeError("R7/R8/R9 prerequisites are absent")
    final = expected if R10_HOOK in expected else expected.replace(
        R9_HOOK, R9_HOOK + R10_HOOK, 1,
    )
    if current == expected and R10_HOOK not in expected:
        state = "READY_TO_PATCH"
    elif current == final:
        state = "ALREADY_INSTALLED"
    else:
        raise RuntimeError("unknown tracked provider changes; no files overwritten")
    if any(final.count(hook) != 1 for hook in HOOKS):
        raise RuntimeError("missing or duplicated provider hook")
    function = _complete_function(final)
    if any(hook not in function for hook in HOOKS):
        raise RuntimeError("patch left the existing provider function")
    ast.parse(final)
    return state, final


def install(*, dry_run: bool) -> bool:
    """Guard R7–R9 and insert exactly the existing short-exact expander."""
    if _git("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("shared provider file is absent")
    current_bytes = TARGET.read_bytes()
    state, final = _verified_source_and_state(
        _git("show", f"HEAD:{GIT_TARGET}"), current_bytes,
    )
    print("PHASE171_R2J_R4_R9_R10_HEAD=" + _git("rev-parse", "HEAD").decode().strip(), flush=True)
    print("PHASE171_R2J_R4_R9_R10_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R10_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if state == "READY_TO_PATCH":
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(current_bytes)
        newline = "\r\n" if b"\r\n" in current_bytes else "\n"
        bom = b"\xef\xbb\xbf" if current_bytes.startswith(b"\xef\xbb\xbf") else b""
        TARGET.write_bytes(bom + final.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R10_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(
        _complete_function(final) + "\n", encoding="utf-8",
    )
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R10_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R10_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return state == "READY_TO_PATCH"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    install(dry_run=arguments.dry_run)


if __name__ == "__main__":
    main()
