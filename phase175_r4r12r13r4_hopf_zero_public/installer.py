"""Fail-closed, single-hook installer; exports complete changed shared function."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("phase165_r52_r9_shared_math.py")
ANCHOR = "    # Phase 175 R4R12R13R3: conditional Delta injectivity and E surjectivity.\n"
INSERT = '''    # Phase 175 R4R12R13R4: retain H=0 as a verified intermediate ProofStep.
    # All subgoals are resolved by the ordinary source-first recursive search.
    from phase175_r4r12r13r4_hopf_zero_public.provider import (
        expand_public_hopf_zero_ehp,
    )
    extra_providers = (expand_public_hopf_zero_ehp,) + tuple(extra_providers)
'''


def render(text: str) -> tuple[str, bool]:
    if text.count(INSERT) == 1:
        return text, False
    if "expand_public_hopf_zero_ehp" in text:
        raise RuntimeError("R13R4_PARTIAL_OR_UNREVIEWED_INSTALLATION")
    if text.count(ANCHOR) != 1:
        raise RuntimeError("R13R4_MISSING_R13R3_ANCHOR")
    return text.replace(ANCHOR, INSERT + ANCHOR, 1), True


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    target = root / TARGET
    raw = target.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    after, required = render(text)
    output.mkdir(parents=True, exist_ok=True)
    start = after.index("def shared_expansion_provider(")
    next_def = after.find("\ndef ", start + 5)
    function = after[start:] if next_def == -1 else after[start:next_def]
    (output / "shared_expansion_provider_FULL.py").write_text(function, encoding="utf-8")
    if required and not dry_run:
        data = after.replace("\n", "\r\n").encode("utf-8") if b"\r\n" in raw else after.encode("utf-8")
        target.write_bytes(data)
    return {"target": str(TARGET), "required": required,
            "installed": required and not dry_run,
            "complete_changed_function": str(output / "shared_expansion_provider_FULL.py")}
