"""Guarded R20R8 installer: propose typed nonzero-double proof subgoals only."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SOURCE = Path("phase171_r2j_r4_r7_nonzero_nu_order/source.py")
PROVIDER = Path("phase165_r52_r9_shared_math.py")
REVIEWED_R20R6_HEAD = "943b7f7af6f92c6987148e5d17c0f06c821434cb"
REVIEWED_BLOBS = {
    SOURCE: "340b66a90118a0760cd94eadaf192ad69f3c48b7",
    PROVIDER: "c3a25c075f1dfa4573ce3feb1c07f653b0aa649a",
}
R20R7_ADDITION = (PACKAGE / "r20r7_reviewed_addition.py.txt").read_text(encoding="utf-8")
SOURCE_ADDITION = (PACKAGE / "source_addition.py.txt").read_text(encoding="utf-8")
R20R7_ORDER_ANCHOR = "        options.extend(expand_public_order_four_from_nonzero_double(goal))\n"
R20R7_ORDER_PLUS_IMAGE = (
    R20R7_ORDER_ANCHOR
    + "        from phase171_r2j_r4_r7_nonzero_nu_order.source import (\n"
    + "            expand_public_injected_generator_nonzero,\n"
    + "        )\n"
    + "        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))\n"
)
R20R8_IMAGE_ANCHOR = "        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))\n"
R20R8_IMAGE_PLUS_DOUBLE = (
    R20R8_IMAGE_ANCHOR
    + "        from phase171_r2j_r4_r7_nonzero_nu_order.source import (\n"
    + "            expand_public_nonzero_double_from_cited_source,\n"
    + "        )\n"
    + "        options.extend(expand_public_nonzero_double_from_cited_source(goal, tuple(available)))\n"
)
SOURCE_FLAG = "def expand_public_nonzero_double_from_cited_source("
PROVIDER_FLAG = "        options.extend(expand_public_nonzero_double_from_cited_source(goal, tuple(available)))"


def normalize(data: bytes) -> str:
    """Normalize line endings for comparison, not for final output."""
    return data.decode("utf-8").replace("\r\n", "\n")


def adapt(text: str, original: bytes) -> bytes:
    """Write complete replacement using the original newline convention."""
    return text.replace("\n", "\r\n").encode("utf-8") if b"\r\n" in original else text.encode("utf-8")


def git(*args: str) -> bytes:
    """Allow only read-only Git commands required by this guarded installer."""
    if args in {("branch", "--show-current"), ("rev-parse", "HEAD")}:
        pass
    elif len(args) == 2 and args[0] in {"rev-parse", "show"}:
        if args[1] not in {
            REVIEWED_R20R6_HEAD + ":" + path.as_posix()
            for path in (SOURCE, PROVIDER)
        }:
            raise ValueError("unreviewed file or Git revision")
    else:
        raise ValueError("unapproved Git command")
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return result.stdout if args[0] == "show" else result.stdout.strip()


def expected_r20r7(source: str, provider: str) -> tuple[str, str]:
    """Reconstruct exact earlier source from the reviewed R20R6 Git objects."""
    if source.count("def expand_public_order_four_from_nonzero_double(") != 1:
        raise RuntimeError("reviewed R20R6 source anchor absent")
    if source.count("def expand_public_injected_generator_nonzero(") != 0:
        raise RuntimeError("reviewed R20R6 source unexpectedly contains R20R7")
    if provider.count(R20R7_ORDER_ANCHOR) != 1:
        raise RuntimeError("reviewed R20R6 provider anchor absent")
    return (
        source.rstrip("\n") + "\n\n" + R20R7_ADDITION.lstrip("\n"),
        provider.replace(R20R7_ORDER_ANCHOR, R20R7_ORDER_PLUS_IMAGE, 1),
    )


def patched_text(source: str, provider: str) -> tuple[str, str]:
    """Add only the R20R8 nonzero-double route; reject partial states."""
    if source.count("def expand_public_injected_generator_nonzero(") != 1:
        raise RuntimeError("R20R7 source prerequisite absent")
    if provider.count(R20R8_IMAGE_ANCHOR) != 1:
        raise RuntimeError("R20R7 shared-provider anchor absent")
    source_done = source.count(SOURCE_FLAG)
    provider_done = provider.count(PROVIDER_FLAG)
    if source_done not in (0, 1) or provider_done not in (0, 1) or source_done != provider_done:
        raise RuntimeError("partial or duplicated R20R8 installation")
    if source_done:
        return source, provider
    return (
        source.rstrip("\n") + "\n\n" + SOURCE_ADDITION.lstrip("\n"),
        provider.replace(R20R8_IMAGE_ANCHOR, R20R8_IMAGE_PLUS_DOUBLE, 1),
    )


def checked_worktree() -> tuple[str, dict[Path, bytes], dict[Path, str], dict[Path, str]]:
    """Require exact R20R7 working content, regardless of its commit state."""
    if git("branch", "--show-current").decode("utf-8") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD").decode("ascii")
    reviewed: dict[Path, str] = {}
    original: dict[Path, bytes] = {}
    for path, reviewed_sha in REVIEWED_BLOBS.items():
        ref = REVIEWED_R20R6_HEAD + ":" + path.as_posix()
        blob = git("rev-parse", ref).decode("ascii")
        if blob != reviewed_sha:
            raise RuntimeError("reviewed R20R6 baseline drift: " + path.as_posix())
        reviewed[path] = normalize(git("show", ref))
        original[path] = (ROOT / path).read_bytes()
    old_source, old_provider = expected_r20r7(reviewed[SOURCE], reviewed[PROVIDER])
    new_source, new_provider = patched_text(old_source, old_provider)
    before = {SOURCE: old_source, PROVIDER: old_provider}
    after = {SOURCE: new_source, PROVIDER: new_provider}
    source_installed = normalize(original[SOURCE]) == new_source
    provider_installed = normalize(original[PROVIDER]) == new_provider
    if source_installed != provider_installed:
        raise RuntimeError("partial R20R8 working state")
    for path in (SOURCE, PROVIDER):
        if normalize(original[path]) not in (before[path], after[path]):
            raise RuntimeError("unexpected local edit: " + path.as_posix())
    return head, original, before, after


def run_install(*, dry_run: bool) -> None:
    """Back up full files and apply R20R8 with tracked-state fail closed."""
    head, original, before, after = checked_worktree()
    already = all(normalize(original[path]) == after[path] for path in (SOURCE, PROVIDER))
    print("PHASE171_R20R8_HEAD=" + head, flush=True)
    print("PHASE171_R20R8_SOURCE_CONTENT_GUARD=PASS", flush=True)
    if dry_run:
        print("PHASE171_R20R8_DRY_RUN=PASS", flush=True)
        print("PHASE171_R20R8_ALREADY_INSTALLED=" + str(already), flush=True)
        return
    if not already:
        backup = PACKAGE / "output" / ("backup_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        backup.mkdir(parents=True, exist_ok=False)
        for path in (SOURCE, PROVIDER):
            (backup / path.name).write_bytes(original[path])
        try:
            for path in (SOURCE, PROVIDER):
                (ROOT / path).write_bytes(adapt(after[path], original[path]))
        except BaseException:
            for path in (SOURCE, PROVIDER):
                (ROOT / path).write_bytes(original[path])
            raise
        print("PHASE171_R20R8_BACKUP=" + str(backup), flush=True)
    checked_worktree()
    complete_source = normalize((ROOT / SOURCE).read_bytes())
    complete_provider = normalize((ROOT / PROVIDER).read_bytes())
    start = complete_provider.index("def shared_expansion_provider(")
    end = complete_provider.index("\ndef search_shared_group_goal(", start)
    out = PACKAGE / "output"
    out.mkdir(exist_ok=True)
    (out / "SOURCE_FULL_AFTER.py").write_text(complete_source, encoding="utf-8")
    (out / "SHARED_PROVIDER_FUNCTION_FULL_AFTER.py").write_text(
        complete_provider[start:end].rstrip("\n") + "\n", encoding="utf-8",
    )
    print("PHASE171_R20R8_SOURCE_CHANGES=" + ("0" if already else "2"), flush=True)
    print("PHASE171_R20R8_RESULT=PASS_INSTALLED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
