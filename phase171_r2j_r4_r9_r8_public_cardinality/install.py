"""Guarded single-function provider patch; preserve an uncommitted R9-R7 patch."""
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


def _git(*args: str) -> bytes:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
        ("show", f"HEAD:{PATH_IN_GIT}"),
    }
    if args not in permitted:
        raise ValueError("only reviewed read-only Git commands are permitted")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
    ).stdout


def _clean_text(blob: bytes) -> str:
    return blob.decode("utf-8-sig").replace("\r\n", "\n")


def _git_blob_sha(blob: bytes) -> str:
    header = f"blob {len(blob)}\0".encode("ascii")
    return hashlib.sha1(header + blob).hexdigest()


def _function_text(source: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == "shared_expansion_provider"]
    if len(matches) != 1:
        raise RuntimeError("expected exactly one shared_expansion_provider function")
    node = matches[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def install(*, dry_run: bool) -> bool:
    if _git("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("existing shared provider is missing")
    head_bytes = _git("show", f"HEAD:{PATH_IN_GIT}")
    head_text = _clean_text(head_bytes)
    # Ensure this is still the exact GitHub-reviewed module, whether the
    # previous four-line R7 patch was committed or remains uncommitted.
    if head_text.count(R7_HOOK) > 1 or R8_HOOK in head_text:
        raise RuntimeError("unknown previously committed provider hook")
    if R7_HOOK in head_text:
        newline = "\r\n" if b"\r\n" in head_bytes else "\n"
        reviewed_blob = head_bytes.replace(R7_HOOK.replace("\n", newline).encode(), b"")
    else:
        reviewed_blob = head_bytes
    if _git_blob_sha(reviewed_blob) != REVIEWED_ORIGINAL_BLOB_SHA:
        raise RuntimeError("Git HEAD provider differs from GitHub-reviewed baseline")
    original_bytes = TARGET.read_bytes()
    content = _clean_text(original_bytes)
    expected = head_text if R7_HOOK in head_text else head_text.replace(
        "        options.extend(expand_finite_cyclic_relation(goal))\n",
        "        options.extend(expand_finite_cyclic_relation(goal))\n" + R7_HOOK,
        1,
    )
    if R7_HOOK not in expected or expected.count(R7_HOOK) != 1:
        raise RuntimeError("reviewed R7 hook missing or ambiguous")
    if content == expected:
        state = "READY_TO_PATCH"
        next_text = content.replace(R7_HOOK, R7_HOOK + R8_HOOK, 1)
    elif content == expected.replace(R7_HOOK, R7_HOOK + R8_HOOK, 1):
        state = "ALREADY_INSTALLED"
        next_text = content
    else:
        raise RuntimeError("tracked provider has unknown changes; refusing overwrite")
    if next_text.count(R8_HOOK) != 1 or next_text.count(R7_HOOK) != 1:
        raise RuntimeError("R7/R8 hook duplicate or missing")
    function = _function_text(next_text)
    if R7_HOOK not in function or R8_HOOK not in function:
        raise RuntimeError("hook escaped the intended provider function")
    ast.parse(next_text)
    print("PHASE171_R2J_R4_R9_R8_HEAD=" + _git("rev-parse", "HEAD").decode().strip(), flush=True)
    print("PHASE171_R2J_R4_R9_R8_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R8_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if state == "READY_TO_PATCH":
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(original_bytes)
        newline = "\r\n" if b"\r\n" in original_bytes else "\n"
        prefix = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
        TARGET.write_bytes(prefix + next_text.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R8_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(function + "\n", encoding="utf-8")
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R8_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R8_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return state == "READY_TO_PATCH"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    install(dry_run=arguments.dry_run)


if __name__ == "__main__":
    main()
