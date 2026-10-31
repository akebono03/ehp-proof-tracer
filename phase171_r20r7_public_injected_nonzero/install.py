"""Guarded R20R7 installer: connect only the prior-cyclic/E-injective nonzero rule."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
SOURCE = Path("phase171_r2j_r4_r7_nonzero_nu_order/source.py")
PROVIDER = Path("phase165_r52_r9_shared_math.py")
REVIEWED_HEAD_BLOBS = {
    SOURCE: "5b95010681f6257dc46a4236c099445281635e53",
    PROVIDER: "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac",
}
# The exact R20R6 worktree was subsequently committed to develop.
# Both pairs are reviewed. Never accept a mixed pair of these versions.
REVIEWED_R20R6_COMMITTED_BLOBS = {
    SOURCE: "340b66a90118a0760cd94eadaf192ad69f3c48b7",
    PROVIDER: "c3a25c075f1dfa4573ce3feb1c07f653b0aa649a",
}
R20R6_SOURCE_ADDITION = (PACKAGE / "r20r6_reviewed_source_addition.py.txt").read_text(encoding="utf-8")
SOURCE_ADDITION = (PACKAGE / "source_addition.py.txt").read_text(encoding="utf-8")
R20R6_ANCHOR = "        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))\n"
R20R6_REPLACEMENT = (
    R20R6_ANCHOR
    + "        from phase171_r2j_r4_r7_nonzero_nu_order.source import (\n"
    + "            expand_public_order_four_from_nonzero_double,\n"
    + "        )\n"
    + "        options.extend(expand_public_order_four_from_nonzero_double(goal))\n"
)
R20R7_ANCHOR = "        options.extend(expand_public_order_four_from_nonzero_double(goal))\n"
R20R7_REPLACEMENT = (
    R20R7_ANCHOR
    + "        from phase171_r2j_r4_r7_nonzero_nu_order.source import (\n"
    + "            expand_public_injected_generator_nonzero,\n"
    + "        )\n"
    + "        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))\n"
)
SOURCE_FLAG = "def expand_public_injected_generator_nonzero("
PROVIDER_FLAG = "        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))"


def git_read(*arguments: str) -> bytes:
    """Allow only branch, HEAD, and reviewed committed-file reads."""
    if arguments in {("branch", "--show-current"), ("rev-parse", "HEAD")}:
        pass
    elif len(arguments) == 2 and arguments[0] == "rev-parse" and arguments[1].startswith("HEAD:"):
        if arguments[1][5:] not in {SOURCE.as_posix(), PROVIDER.as_posix()}:
            raise ValueError("unreviewed committed file")
    elif len(arguments) == 2 and arguments[0] == "show" and arguments[1].startswith("HEAD:"):
        if arguments[1][5:] not in {SOURCE.as_posix(), PROVIDER.as_posix()}:
            raise ValueError("unreviewed committed file")
    else:
        raise ValueError("unapproved Git command")
    result = subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True, capture_output=True,
    )
    return result.stdout if arguments[0] == "show" else result.stdout.strip()


def normalize(data: bytes) -> str:
    """Use LF in memory while retaining each working file's line endings."""
    return data.decode("utf-8").replace("\r\n", "\n")


def adapt(text: str, original: bytes) -> bytes:
    """Restore the original newline convention when writing full files."""
    return text.replace("\n", "\r\n").encode("utf-8") if b"\r\n" in original else text.encode("utf-8")


def expected_r20r6(source: str, provider: str) -> tuple[str, str]:
    """Reconstruct the reviewed R20R6-only working state from Git HEAD."""
    if source.count("def inferred_order_four_rule(") != 1:
        raise RuntimeError("reviewed mathematical order-four rule was changed")
    if provider.count(R20R6_ANCHOR) != 1:
        raise RuntimeError("reviewed R20R6 provider insertion anchor absent")
    return (
        source.rstrip("\n") + "\n\n" + R20R6_SOURCE_ADDITION.lstrip("\n"),
        provider.replace(R20R6_ANCHOR, R20R6_REPLACEMENT, 1),
    )


def patched_text(source: str, provider: str) -> tuple[str, str]:
    """Append only R20R7, with no modification to existing inference rules."""
    if source.count("def expand_public_order_four_from_nonzero_double(") != 1:
        raise RuntimeError("R20R6 order-four source function is absent or duplicated")
    if provider.count(R20R7_ANCHOR) != 1:
        raise RuntimeError("R20R6 order-four provider call is absent or duplicated")
    source_exists = SOURCE_FLAG in source
    provider_exists = PROVIDER_FLAG in provider
    if source_exists != provider_exists:
        raise RuntimeError("partial R20R7 installation; no files changed")
    if source_exists:
        if source.count(SOURCE_FLAG) != 1 or provider.count(PROVIDER_FLAG) != 1:
            raise RuntimeError("duplicate R20R7 definitions")
        return source, provider
    return (
        source.rstrip("\n") + "\n\n" + SOURCE_ADDITION.lstrip("\n"),
        provider.replace(R20R7_ANCHOR, R20R7_REPLACEMENT, 1),
    )


def checked_worktree() -> tuple[str, dict[Path, bytes], dict[Path, str], dict[Path, str]]:
    """Accept either reviewed R20R6 baseline, rejecting mixed versions or edits.

    The earlier R20R6 patch was originally uncommitted, then committed as
    exactly the Git blobs listed in REVIEWED_R20R6_COMMITTED_BLOBS. The
    mathematical source is identical; only the HEAD file identities differ.
    """
    branch = git_read("branch", "--show-current").decode("utf-8")
    if branch != "develop":
        raise RuntimeError("develop branch required")
    head = git_read("rev-parse", "HEAD").decode("utf-8")
    committed: dict[Path, str] = {}
    original: dict[Path, bytes] = {}
    blobs: dict[Path, str] = {}
    for path, earlier_blob in REVIEWED_HEAD_BLOBS.items():
        blob = git_read("rev-parse", "HEAD:" + path.as_posix()).decode("ascii")
        if blob not in (earlier_blob, REVIEWED_R20R6_COMMITTED_BLOBS[path]):
            raise RuntimeError("reviewed committed source drift: " + str(path) + " actual=" + blob)
        blobs[path] = blob
        committed[path] = normalize(git_read("show", "HEAD:" + path.as_posix()))
        original[path] = (ROOT / path).read_bytes()
    if all(blobs[path] == REVIEWED_HEAD_BLOBS[path] for path in (SOURCE, PROVIDER)):
        r20r6_source, r20r6_provider = expected_r20r6(
            committed[SOURCE], committed[PROVIDER],
        )
    elif all(
        blobs[path] == REVIEWED_R20R6_COMMITTED_BLOBS[path]
        for path in (SOURCE, PROVIDER)
    ):
        r20r6_source, r20r6_provider = committed[SOURCE], committed[PROVIDER]
    else:
        raise RuntimeError("mixed R20R6 committed versions; no files changed")
    r20r7_source, r20r7_provider = patched_text(r20r6_source, r20r6_provider)
    valid_states = {
        SOURCE: {r20r6_source, r20r7_source},
        PROVIDER: {r20r6_provider, r20r7_provider},
    }
    for path in (SOURCE, PROVIDER):
        if normalize(original[path]) not in valid_states[path]:
            raise RuntimeError("unexpected local edits in " + str(path))
    source_done = normalize(original[SOURCE]) == r20r7_source
    provider_done = normalize(original[PROVIDER]) == r20r7_provider
    if source_done != provider_done:
        raise RuntimeError("partial R20R7 installation")
    return head, original, {SOURCE: r20r6_source, PROVIDER: r20r6_provider}, {SOURCE: r20r7_source, PROVIDER: r20r7_provider}


def run_install(*, dry_run: bool) -> None:
    """Install safely, back up full originals and emit full modified functions."""
    head, original, before, after = checked_worktree()
    print("PHASE171_R20R7_HEAD=" + head, flush=True)
    print("PHASE171_R20R7_SOURCE_CONTENT_GUARD=PASS", flush=True)
    already = all(normalize(original[path]) == after[path] for path in (SOURCE, PROVIDER))
    if dry_run:
        print("PHASE171_R20R7_DRY_RUN=PASS", flush=True)
        print("PHASE171_R20R7_ALREADY_INSTALLED=" + str(already), flush=True)
        return
    if not already:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        backup = PACKAGE / "output" / ("backup_" + stamp)
        backup.mkdir(parents=True, exist_ok=False)
        for path in (SOURCE, PROVIDER):
            (backup / path.name).write_bytes(original[path])
        try:
            for path in (SOURCE, PROVIDER):
                (ROOT / path).write_bytes(adapt(after[path], original[path]))
        except Exception:
            for path in (SOURCE, PROVIDER):
                (ROOT / path).write_bytes(original[path])
            raise
        print("PHASE171_R20R7_BACKUP=" + str(backup), flush=True)
    checked_worktree()
    out = PACKAGE / "output"
    out.mkdir(exist_ok=True)
    complete_source = normalize((ROOT / SOURCE).read_bytes())
    complete_provider = normalize((ROOT / PROVIDER).read_bytes())
    begin = complete_provider.index("def shared_expansion_provider(")
    end = complete_provider.index("\ndef search_shared_group_goal(", begin)
    (out / "SOURCE_FULL_AFTER.py").write_text(complete_source, encoding="utf-8")
    (out / "SHARED_PROVIDER_FUNCTION_FULL_AFTER.py").write_text(
        complete_provider[begin:end].rstrip("\n") + "\n", encoding="utf-8",
    )
    print("PHASE171_R20R7_SOURCE_CHANGES=" + ("0" if already else "2"), flush=True)
    print("PHASE171_R20R7_RESULT=PASS_INSTALLED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
