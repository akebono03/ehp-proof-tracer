"""Idempotent, anchored R3R39 minimal shared-provider patch."""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
INSERT_AFTER_AVAILABLE = "    if not isinstance(prior_conclusions, tuple):\n"
INSERT_AFTER_HOPF = "        options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))\n"
NEW_SETUP = (
    "    # Phase 176 R3R39: source-screened, six existing equality inferences.\n"
    "    from phase176_r3r39_public_equality_transport.source import (\n"
    "        build_public_right_hopf_transport_provider,\n"
    "    )\n"
    "    public_right_hopf_transport = build_public_right_hopf_transport_provider(\n"
    "        tuple(available),\n"
    "    )\n"
)
NEW_DISPATCH = (
    "        # All six transport steps stay visible in the ordinary Proof Tree.\n"
    "        options.extend(public_right_hopf_transport(goal))\n"
)


def updated_source(source: str) -> str:
    """Produce one exact shared-function update; fail on missing/changed hooks."""
    setup_count = source.count(NEW_SETUP)
    dispatch_count = source.count(NEW_DISPATCH)
    if setup_count == 1 and dispatch_count == 1:
        return source
    if setup_count != 0 or dispatch_count != 0:
        raise ValueError("PARTIAL_R3R39_PATCH_REFUSED")
    if (source.count(INSERT_AFTER_AVAILABLE) != 1
            or source.count(INSERT_AFTER_HOPF) != 1
            or source.count("options.extend(expand_composite_suspension_equality(goal))") != 1):
        raise ValueError("SHARED_PROVIDER_ANCHORS_CHANGED")
    return source.replace(
        INSERT_AFTER_AVAILABLE, NEW_SETUP + INSERT_AFTER_AVAILABLE, 1,
    ).replace(
        INSERT_AFTER_HOPF, INSERT_AFTER_HOPF + NEW_DISPATCH, 1,
    )


def normalized_source(raw: bytes) -> str:
    """Decode UTF-8 without treating the byte representation as source code."""
    return raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def patched_bytes(baseline: bytes, current: bytes) -> bytes:
    """Only permit the exact R3R39 insertion; preserve baseline EOL and BOM."""
    original = normalized_source(baseline)
    proposed = updated_source(original)
    if normalized_source(current) not in (original, proposed):
        raise ValueError("UNRELATED_WORKTREE_CHANGE_REFUSED")
    without_crlf = baseline.replace(b"\r\n", b"")
    if b"\r" in without_crlf or (b"\r\n" in baseline and b"\n" in without_crlf):
        raise ValueError("MIXED_OR_UNSUPPORTED_BASELINE_EOL")
    eol = "\r\n" if b"\r\n" in baseline else "\n"
    encoding = "utf-8-sig" if baseline.startswith(b"\xef\xbb\xbf") else "utf-8"
    ast.parse(proposed, filename=str(TARGET))
    return proposed.replace("\n", eol).encode(encoding)


def tracked_baseline() -> bytes:
    """Reject staged changes; compare the index and HEAD as exact bytes."""
    relative = TARGET.relative_to(ROOT).as_posix()
    head = subprocess.check_output(["git", "show", "HEAD:" + relative], cwd=ROOT)
    index = subprocess.check_output(["git", "show", ":" + relative], cwd=ROOT)
    if head != index:
        raise ValueError("STAGED_TARGET_CHANGE_REFUSED")
    return index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    for required in (
        ROOT / "phase176_r3r38_equality_transport_isolated/source.py",
        ROOT / "phase176_r3r34_composite_suspension_isolated/source.py",
        ROOT / "phase176_r3r36_composite_right_hopf_isolated/source.py",
    ):
        if not required.is_file():
            raise ValueError("MISSING_BASELINE:" + str(required.relative_to(ROOT)))
    current = TARGET.read_bytes()
    proposed = patched_bytes(tracked_baseline(), current)
    if not args.dry_run:
        if current != proposed:
            TARGET.write_bytes(proposed)
        if TARGET.read_bytes() != proposed:
            raise ValueError("BYTE_VERIFICATION_FAILED")
        text = normalized_source(proposed)
        start = text.index("def shared_expansion_provider(")
        end = text.index("\ndef search_shared_group_goal(", start)
        documented = (
            "# Phase 176 R3R39 — shared_expansion_provider() 全文\n\n"
            "既存実装を維持し、R3R39 のセットアップと呼び出しのみを追加したものです。\n\n"
            "```python\n" + text[start:end].rstrip() + "\n```\n"
        )
        (Path(__file__).resolve().parent / "SHARED_FUNCTION_FULL_JA.md").write_bytes(
            documented.encode("utf-8"),
        )
    print("PHASE176_R3R39_PATCH=" + ("DRY_RUN_PASS" if args.dry_run else "APPLIED_OR_ALREADY_PRESENT"))
    print("PHASE176_R3R39R1_EOL=" + ("DRY_RUN_PASS" if args.dry_run else "BYTE_VERIFIED"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
