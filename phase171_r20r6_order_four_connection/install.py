"""Install one source-checked, reversible public order-four expansion."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
SOURCE = Path("phase171_r2j_r4_r7_nonzero_nu_order/source.py")
PROVIDER = Path("phase165_r52_r9_shared_math.py")
REVIEWED_BLOBS = {
    SOURCE: "5b95010681f6257dc46a4236c099445281635e53",
    PROVIDER: "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac",
}
APPEND = (PACKAGE / "source_addition.py.txt").read_text(encoding="utf-8")
PROVIDER_ANCHOR = (
    "        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))\n"
)
PROVIDER_REPLACEMENT = (
    PROVIDER_ANCHOR
    + "        from phase171_r2j_r4_r7_nonzero_nu_order.source import (\n"
    + "            expand_public_order_four_from_nonzero_double,\n"
    + "        )\n"
    + "        options.extend(expand_public_order_four_from_nonzero_double(goal))\n"
)
SOURCE_FLAG = "def expand_public_order_four_from_nonzero_double("
PROVIDER_FLAG = "        options.extend(expand_public_order_four_from_nonzero_double(goal))"


def git_read(*args: str) -> str:
    """Read only Git branch, HEAD, and working tree file hashes."""
    if args not in {("branch", "--show-current"), ("rev-parse", "HEAD")} and not (
        len(args) == 2 and args[0] == "hash-object" and args[1] in {str(SOURCE), str(PROVIDER)}
    ):
        raise ValueError("unapproved Git command")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def patched_text(source: str, provider: str) -> tuple[str, str]:
    """Construct full replacement contents, rejecting drift and half-installs."""
    source_exists = SOURCE_FLAG in source
    provider_exists = PROVIDER_FLAG in provider
    if source_exists != provider_exists:
        raise RuntimeError("partial R20R6 installation; no files changed")
    if source_exists:
        if source.count(SOURCE_FLAG) != 1 or provider.count(PROVIDER_FLAG) != 1:
            raise RuntimeError("unexpected duplicate R20R6 anchors")
        return source, provider
    if source.count("def inferred_order_four_rule(") != 1:
        raise RuntimeError("missing original inference rule")
    # Git stores this reviewed provider with CRLF line endings.  Match the
    # original line ending convention instead of silently ignoring the anchor.
    newline = "\r\n" if "\r\n" in provider else "\n"
    anchor = PROVIDER_ANCHOR.replace("\n", newline)
    replacement = PROVIDER_REPLACEMENT.replace("\n", newline)
    if provider.count(anchor) != 1:
        raise RuntimeError("provider anchor absent or duplicated")
    return (
        source.rstrip("\r\n") + "\n\n" + APPEND.lstrip("\r\n"),
        provider.replace(anchor, replacement, 1),
    )


def run_install(*, dry_run: bool) -> None:
    """Preflight approved blobs and install exactly the intended two changes."""
    if git_read("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git_read("rev-parse", "HEAD")
    texts = {}
    for relative in (SOURCE, PROVIDER):
        if not (ROOT / relative).is_file():
            raise RuntimeError("missing source: " + str(relative))
        texts[relative] = (ROOT / relative).read_bytes()
    source_bytes = texts[SOURCE]
    provider_bytes = texts[PROVIDER]
    source_text = source_bytes.decode("utf-8")
    provider_text = provider_bytes.decode("utf-8")
    already = SOURCE_FLAG in source_text and PROVIDER_FLAG in provider_text
    for relative in (SOURCE, PROVIDER):
        blob = git_read("hash-object", str(relative))
        if already:
            # Full post-install contents are checked below; never trust flags alone.
            continue
        if blob != REVIEWED_BLOBS[relative]:
            raise RuntimeError(
                "reviewed source drift: " + str(relative)
                + " expected=" + REVIEWED_BLOBS[relative] + " actual=" + blob
            )
    result_source, result_provider = patched_text(source_text, provider_text)
    if already and (source_text != result_source or provider_text != result_provider):
        raise RuntimeError("postinstall content conflict")
    if already:
        # Ensure the entire installed files are the deterministic transformation
        # of the reviewed Git HEAD versions; use stored hashes on repeat runs.
        expected_file = PACKAGE / "output" / "installed_hashes.txt"
        if expected_file.exists():
            expected = dict(line.split(" ", 1) for line in expected_file.read_text(encoding="utf-8").splitlines())
            for relative in (SOURCE, PROVIDER):
                if git_read("hash-object", str(relative)) != expected.get(str(relative)):
                    raise RuntimeError("previously installed file changed: " + str(relative))
        else:
            raise RuntimeError("installed patch has no verified R20R6 provenance file")
    print("PHASE171_R20R6_HEAD=" + head, flush=True)
    print("PHASE171_R20R6_SOURCE_CONTENT_GUARD=PASS", flush=True)
    if dry_run:
        print("PHASE171_R20R6_DRY_RUN=PASS", flush=True)
        return
    if not already:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        backup = PACKAGE / "output" / ("backup_" + stamp)
        backup.mkdir(parents=True, exist_ok=False)
        (backup / SOURCE.name).write_bytes(source_bytes)
        (backup / PROVIDER.name).write_bytes(provider_bytes)
        # Production files retain their original newline convention.
        def adapt(new_text: str, old_bytes: bytes) -> bytes:
            if b"\r\n" in old_bytes:
                new_text = new_text.replace("\r\n", "\n").replace("\n", "\r\n")
            return new_text.encode("utf-8")
        (ROOT / SOURCE).write_bytes(adapt(result_source, source_bytes))
        (ROOT / PROVIDER).write_bytes(adapt(result_provider, provider_bytes))
        expected = "".join(
            str(relative) + " " + git_read("hash-object", str(relative)) + "\n"
            for relative in (SOURCE, PROVIDER)
        )
        (PACKAGE / "output" / "installed_hashes.txt").write_text(expected, encoding="utf-8")
        print("PHASE171_R20R6_BACKUP=" + str(backup), flush=True)
    # Produce complete, fully replaceable source and provider-function texts.
    source_final = (ROOT / SOURCE).read_text(encoding="utf-8")
    provider_final = (ROOT / PROVIDER).read_text(encoding="utf-8")
    heading = "def shared_expansion_provider("
    begin = provider_final.index(heading)
    end = provider_final.index("\ndef search_shared_group_goal(", begin)
    out = PACKAGE / "output"
    out.mkdir(exist_ok=True)
    (out / "SOURCE_FULL_AFTER.py").write_text(source_final, encoding="utf-8")
    (out / "SHARED_PROVIDER_FUNCTION_FULL_AFTER.py").write_text(
        provider_final[begin:end].rstrip("\r\n") + "\n", encoding="utf-8",
    )
    print("PHASE171_R20R6_SOURCE_CHANGES=2", flush=True)
    print("PHASE171_R20R6_RESULT=PASS_INSTALLED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
