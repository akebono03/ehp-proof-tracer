"""Guarded R11 insertion after the exact reviewed R10 public provider hook.

Preserves already installed R7–R10 patches. Rejects all unknown tracked edits.
"""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

from phase171_r2j_r4_r9_r10_public_short_exact.install import (
    GIT_TARGET,
    R10_HOOK,
    _complete_function,
    _git,
    _verified_source_and_state,
)

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / GIT_TARGET
OUTPUT = PACKAGE / "output"
R11_HOOK = (
    "        from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (\n"
    "            expand_reverse_cited_eta_hopf_equalities,\n"
    "        )\n"
    "        directed = expand_reverse_cited_eta_hopf_equalities(goal, tuple(available))\n"
    "        if directed:\n"
    "            return directed\n"
)


def _normal(blob: bytes) -> str:
    return blob.decode("utf-8-sig").replace("\r\n", "\n")


def _verified_r11_state(head_bytes: bytes, current_bytes: bytes) -> tuple[str, str]:
    """Derive the exact R10 baseline and allow one source-anchored R11 hook."""
    current = _normal(current_bytes)
    if current.count(R11_HOOK) > 1:
        raise RuntimeError("duplicate R11 provider hook")
    without = current.replace(R11_HOOK, "", 1)
    baseline_bytes = without.encode("utf-8")
    state, canonical_r10 = _verified_source_and_state(head_bytes, baseline_bytes)
    if state != "ALREADY_INSTALLED" or without != canonical_r10:
        raise RuntimeError("R10 base is not exactly the reviewed complete provider")
    if canonical_r10.count(R10_HOOK) != 1:
        raise RuntimeError("R10 hook is not unique")
    patched = canonical_r10.replace(R10_HOOK, R10_HOOK + R11_HOOK, 1)
    if current == canonical_r10:
        mode = "READY_TO_PATCH"
    elif current == patched:
        mode = "ALREADY_INSTALLED"
    else:
        raise RuntimeError("unexpected provider modification; refuse overwrite")
    if patched.count(R11_HOOK) != 1 or R11_HOOK not in _complete_function(patched):
        raise RuntimeError("R11 hook escaped shared_expansion_provider")
    ast.parse(patched)
    return mode, patched


def install(*, dry_run: bool) -> bool:
    if _git("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("shared provider file is absent")
    original = TARGET.read_bytes()
    state, final = _verified_r11_state(_git("show", f"HEAD:{GIT_TARGET}"), original)
    print("PHASE171_R2J_R4_R9_R11_HEAD=" + _git("rev-parse", "HEAD").decode().strip(), flush=True)
    print("PHASE171_R2J_R4_R9_R11_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R11_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if state == "READY_TO_PATCH":
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(original)
        newline = "\r\n" if b"\r\n" in original else "\n"
        bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
        TARGET.write_bytes(bom + final.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R11_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(
        _complete_function(final) + "\n", encoding="utf-8",
    )
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R11_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R11_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return state == "READY_TO_PATCH"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
