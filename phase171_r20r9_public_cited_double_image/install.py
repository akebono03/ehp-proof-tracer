"""Guarded R20R9 installer; only public typed double-image proposal wiring."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
REVIEWED_HEAD = "9c4e903c512941b9c2003105d1867cf7b694b363"
R7_SOURCE = Path("phase171_r2j_r4_r7_nonzero_nu_order/source.py")
DOUBLE_SOURCE = Path("phase171_r2j_r4_r3_double_image_bridge/source.py")
PROVIDER = Path("phase165_r52_r9_shared_math.py")
REVIEWED_BLOBS = {
    R7_SOURCE: "d395784df802a279ac03fd8a6beb443c961d5538",
    DOUBLE_SOURCE: "52d5aced7e698e508d87a35d3237ec496cc9c262",
    PROVIDER: "8d4197f5939bb344321d98d5df06373e9acbf86d",
}
R8_ADDITION = (PACKAGE / "r20r8_source_addition.py.txt").read_text(encoding="utf-8")
R9_ADDITION = (PACKAGE / "source_addition.py.txt").read_text(encoding="utf-8")
# Keep the first R20R9 source in the guard as an upgradeable, exact baseline.
LEGACY_SOURCE_DIMENSION_GUARD = "if qn is None or _endpoints(goal.rhs.expression) != qn:"
CORRECT_SOURCE_DIMENSION_GUARD = (
    "if qn is None or _endpoints(goal.rhs.expression) != (qn[0] - 1, qn[1] - 1):"
)
# R20R9R2 incorrectly compared an E-image target with the E-image input.
# The cited (5.3) equality is 2*x=y, while the goal is 2*x=E(z).
R20R9R2_CITED_TARGET_GUARD = "and claim.rhs == goal.rhs.expression"
R20R9R4_CITED_TARGET_GUARD = "and _endpoints(claim.rhs) == qn"
if R9_ADDITION.count(CORRECT_SOURCE_DIMENSION_GUARD) != 1:
    raise RuntimeError("R20R9R2 corrected source dimension guard absent or duplicated")
if R9_ADDITION.count(R20R9R4_CITED_TARGET_GUARD) != 1:
    raise RuntimeError("R20R9R4 corrected citation target guard absent or duplicated")
# The earlier R20R9R2 also set image.target_generator to the E input.
# Recover its exact pre-fix function text for full-content guard matching.
R20R9R2_GENERATOR_IMAGE_BLOCK = (
    "        image = GeneratorImage(\n"
    "            map=TodaSuspensionMap(earlier_group, middle_group),\n"
    "            source_generator=typed.rhs.generator,\n"
    "            target_generator=goal.rhs.expression,\n"
    "        )\n"
    "        for cited_double in cited_doubles:\n"
)
R20R9R4_GENERATOR_IMAGE_BLOCK = (
    "        for cited_double in cited_doubles:\n"
    "            image = GeneratorImage(\n"
    "                map=TodaSuspensionMap(earlier_group, middle_group),\n"
    "                source_generator=typed.rhs.generator,\n"
    "                target_generator=cited_double.rhs,\n"
    "            )\n"
)
if R9_ADDITION.count(R20R9R4_GENERATOR_IMAGE_BLOCK) != 1:
    raise RuntimeError("R20R9R4 corrected E-target generator block absent or duplicated")
R20R9R2_ADDITION = R9_ADDITION.replace(
    R20R9R4_GENERATOR_IMAGE_BLOCK, R20R9R2_GENERATOR_IMAGE_BLOCK, 1,
).replace(
    R20R9R4_CITED_TARGET_GUARD, R20R9R2_CITED_TARGET_GUARD, 1,
)
LEGACY_R9_ADDITION = R20R9R2_ADDITION.replace(
    CORRECT_SOURCE_DIMENSION_GUARD, LEGACY_SOURCE_DIMENSION_GUARD, 1,
)
R8_ANCHOR = "        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))\n"
R8_LINE = "        options.extend(expand_public_nonzero_double_from_cited_source(goal, tuple(available)))\n"
R8_INSERTION = (
    R8_ANCHOR
    + "        from phase171_r2j_r4_r7_nonzero_nu_order.source import (\n"
    + "            expand_public_nonzero_double_from_cited_source,\n"
    + "        )\n"
    + R8_LINE
)
R9_INSERTION = (
    R8_LINE
    + "        from phase171_r2j_r4_r3_double_image_bridge.source import (\n"
    + "            expand_public_cited_double_image_equality,\n"
    + "        )\n"
    + "        options.extend(expand_public_cited_double_image_equality(goal, tuple(available)))\n"
)
R9_SOURCE_FLAG = "def expand_public_cited_double_image_equality("
R9_PROVIDER_FLAG = "        options.extend(expand_public_cited_double_image_equality(goal, tuple(available)))"


def normalize(data: bytes) -> str:
    """Compare complete text without changing the original newline format."""
    return data.decode("utf-8").replace("\r\n", "\n")


def adapt(text: str, original: bytes) -> bytes:
    """Preserve the original file's newline convention on replacement."""
    return (text.replace("\n", "\r\n") if b"\r\n" in original else text).encode("utf-8")


def git(*args: str) -> bytes:
    """Allow only the fixed, read-only Git queries required for preflight."""
    if args in {("branch", "--show-current"), ("rev-parse", "HEAD")}:
        pass
    elif len(args) == 2 and args[0] in {"show", "rev-parse"}:
        if args[1] not in {REVIEWED_HEAD + ":" + path.as_posix() for path in REVIEWED_BLOBS}:
            raise ValueError("unreviewed Git reference")
    else:
        raise ValueError("unapproved Git command")
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return result.stdout if args[0] == "show" else result.stdout.strip()


def expected_r20r8(reviewed: dict[Path, str]) -> dict[Path, str]:
    """Reconstruct exact R20R8 content from the verified R20R7 commit."""
    source = reviewed[R7_SOURCE]
    provider = reviewed[PROVIDER]
    if source.count("def expand_public_injected_generator_nonzero(") != 1:
        raise RuntimeError("R20R7 source is absent in reviewed commit")
    if source.count("def expand_public_nonzero_double_from_cited_source(") != 0:
        raise RuntimeError("R20R8 source already present in reviewed commit")
    if provider.count(R8_ANCHOR) != 1:
        raise RuntimeError("R20R7 provider anchor is missing or duplicated")
    return {
        R7_SOURCE: source.rstrip("\n") + "\n\n" + R8_ADDITION.lstrip("\n"),
        PROVIDER: provider.replace(R8_ANCHOR, R8_INSERTION, 1),
        DOUBLE_SOURCE: reviewed[DOUBLE_SOURCE],
    }


def patched_text(before: dict[Path, str]) -> dict[Path, str]:
    """Generate full replacements for the two R20R9 target source files."""
    source, provider = before[DOUBLE_SOURCE], before[PROVIDER]
    if source.count(R9_SOURCE_FLAG) != 0:
        raise RuntimeError("R20R9 already appears in reviewed R20R8 source")
    if provider.count(R8_LINE) != 1 or provider.count(R9_PROVIDER_FLAG) != 0:
        raise RuntimeError("R20R8 provider anchor absent or duplicated")
    return {
        R7_SOURCE: before[R7_SOURCE],
        DOUBLE_SOURCE: source.rstrip("\n") + "\n\n" + R9_ADDITION.lstrip("\n"),
        PROVIDER: provider.replace(R8_LINE, R9_INSERTION, 1),
    }


def legacy_r20r9_text(before: dict[Path, str]) -> dict[Path, str]:
    """Reconstruct the already-installed R20R9 source with its wrong E-input guard.

    The provider is unchanged. Only this exact, reviewed previous source may
    be migrated; arbitrary local edits must still fail closed.
    """
    after = patched_text(before)
    legacy = dict(after)
    old_source = before[DOUBLE_SOURCE].rstrip("\n") + "\n\n" + LEGACY_R9_ADDITION.lstrip("\n")
    if old_source.count(LEGACY_SOURCE_DIMENSION_GUARD) != 1:
        raise RuntimeError("R20R9R1 old guard absent or duplicated")
    legacy[DOUBLE_SOURCE] = old_source
    return legacy


def r20r9r2_text(before: dict[Path, str]) -> dict[Path, str]:
    """Reconstruct the complete, exact R20R9R2 source installed previously."""
    after = patched_text(before)
    previous = dict(after)
    previous[DOUBLE_SOURCE] = (
        before[DOUBLE_SOURCE].rstrip("\n") + "\n\n" + R20R9R2_ADDITION.lstrip("\n")
    )
    if previous[DOUBLE_SOURCE].count(R20R9R2_CITED_TARGET_GUARD) != 1:
        raise RuntimeError("R20R9R2 previous citation guard absent or duplicated")
    return previous


def checked_worktree() -> tuple[str, dict[Path, bytes], dict[Path, str], dict[Path, str]]:
    """Accept exact R20R8, R20R9R1, R20R9R2, or R20R9R4 content.

    The full reviewed R20R7 snapshot and deterministic transformations
    are used. Do not permit unrelated local edits or partial source states.
    """
    if git("branch", "--show-current").decode("utf-8") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD").decode("ascii")
    reviewed: dict[Path, str] = {}
    original: dict[Path, bytes] = {}
    for path, reviewed_sha in REVIEWED_BLOBS.items():
        ref = REVIEWED_HEAD + ":" + path.as_posix()
        if git("rev-parse", ref).decode("ascii") != reviewed_sha:
            raise RuntimeError("reviewed commit baseline drift: " + path.as_posix())
        reviewed[path] = normalize(git("show", ref))
        original[path] = (ROOT / path).read_bytes()
    before = expected_r20r8(reviewed)
    after = patched_text(before)
    legacy = legacy_r20r9_text(before)
    previous = r20r9r2_text(before)
    edited = (DOUBLE_SOURCE, PROVIDER)
    if normalize(original[R7_SOURCE]) != before[R7_SOURCE]:
        raise RuntimeError("unexpected R20R8 dependency edit: " + R7_SOURCE.as_posix())
    if all(normalize(original[path]) == before[path] for path in edited):
        return head, original, before, after
    if all(normalize(original[path]) == legacy[path] for path in edited):
        return head, original, before, after
    if all(normalize(original[path]) == previous[path] for path in edited):
        return head, original, before, after
    if all(normalize(original[path]) == after[path] for path in edited):
        return head, original, before, after
    raise RuntimeError("partial R20R9 state or unexpected local edits")


def run_install(*, dry_run: bool) -> None:
    """Back up and replace only files that differ from corrected R20R9R2."""
    head, original, before, after = checked_worktree()
    edited = (DOUBLE_SOURCE, PROVIDER)
    changed = tuple(path for path in edited if normalize(original[path]) != after[path])
    already = not changed
    print("PHASE171_R20R9_HEAD=" + head, flush=True)
    print("PHASE171_R20R9_SOURCE_CONTENT_GUARD=PASS", flush=True)
    if dry_run:
        print("PHASE171_R20R9_DRY_RUN=PASS", flush=True)
        print("PHASE171_R20R9_ALREADY_INSTALLED=" + str(already), flush=True)
        print("PHASE171_R20R9R2_CORRECTION_NEEDED=" + str(bool(changed)), flush=True)
        return
    if changed:
        backup = PACKAGE / "output" / ("backup_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        backup.mkdir(parents=True, exist_ok=False)
        for path in changed:
            (backup / path.name).write_bytes(original[path])
        try:
            for path in changed:
                (ROOT / path).write_bytes(adapt(after[path], original[path]))
        except BaseException:
            for path in changed:
                (ROOT / path).write_bytes(original[path])
            raise
        print("PHASE171_R20R9_BACKUP=" + str(backup), flush=True)
    checked_worktree()
    out = PACKAGE / "output"
    out.mkdir(parents=True, exist_ok=True)
    for path in edited:
        full_text = normalize((ROOT / path).read_bytes())
        (out / (path.stem.upper() + "_" + path.parent.name.upper() + "_FULL_AFTER.py")).write_text(full_text, encoding="utf-8")
    shared = normalize((ROOT / PROVIDER).read_bytes())
    start = shared.index("def shared_expansion_provider(")
    end = shared.index("\ndef search_shared_group_goal(", start)
    (out / "SHARED_EXPANSION_PROVIDER_FUNCTION_FULL_AFTER.py").write_text(
        shared[start:end].rstrip("\n") + "\n", encoding="utf-8",
    )
    print("PHASE171_R20R9_SOURCE_CHANGES=" + str(len(changed)), flush=True)
    print("PHASE171_R20R9R2_SOURCE_DIMENSION_GUARD=CORRECTED", flush=True)
    print("PHASE171_R20R9R4_CITED_IMAGE_TARGET_GUARD=CORRECTED", flush=True)
    print("PHASE171_R20R9_RESULT=PASS_INSTALLED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
