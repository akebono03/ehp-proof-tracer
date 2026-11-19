"""Strict, reversible installation of a single shared-provider registration."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("phase165_r52_r9_shared_math.py")
ANCHOR = '    # Phase 175 R4R12R9: infer a generator image from a proved typed\n'
INSERT = '''    # Phase 175 R4R12R13R3: conditional Delta injectivity and E surjectivity.
    # Every parent is independently verified by recursive proof search.
    from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
        build_public_delta_e_provider,
    )
    extra_providers = (build_public_delta_e_provider(bridge),) + tuple(extra_providers)
'''


def render(text: str) -> tuple[str, bool]:
    """Fail closed for unknown source, duplicate hooks, or partial installation."""
    if text.count(INSERT) == 1:
        return text, False
    if "build_public_delta_e_provider" in text:
        raise RuntimeError("R13R3_PARTIAL_OR_UNREVIEWED_PROVIDER")
    if text.count(ANCHOR) != 1:
        raise RuntimeError("R13R3_UNREVIEWED_SHARED_PROVIDER_ANCHOR")
    return text.replace(ANCHOR, INSERT + ANCHOR, 1), True


def plan(root: Path) -> tuple[Path, str, str, bool]:
    target = root / TARGET
    before = target.read_text(encoding="utf-8")
    after, change = render(before)
    return target, before, after, change


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    target, before, after, required = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    # Full replacement function is automatically exported from actual local code.
    start = after.index("def shared_expansion_provider(")
    next_def = after.find("\ndef ", start + 5)
    body = after[start:] if next_def == -1 else after[start:next_def]
    (output / "shared_expansion_provider_FULL.py").write_text(body, encoding="utf-8")
    if not dry_run and required:
        # Only the exact anchored insertion is permitted; retain original EOL.
        raw = target.read_bytes()
        if b"\r\n" in raw:
            after_bytes = after.replace("\n", "\r\n").encode("utf-8")
        else:
            after_bytes = after.encode("utf-8")
        target.write_bytes(after_bytes)
    return {
        "target": str(TARGET), "change_required": required,
        "installed": not dry_run and required,
        "full_function_export": str(output / "shared_expansion_provider_FULL.py"),
    }
