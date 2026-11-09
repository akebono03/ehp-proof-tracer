"""R34 guarded installer for two cited prior-source leaves only.

Refuses unreviewed production edits. Does not reset, stage, or commit the
checkout, and leaves every earlier phase package intact.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
    ROOT,
    checked_prior_statements,
    git_blob_sha,
    reviewed_source_positions,
)

BASE_HEAD = "8a1fa3c52264ba8544ad24cd68e24316963e090f"
SINGLE_REVIEWED_SUCCESSOR_PREFIX = "phase174_r3_r7_r33_three_premise_source_frontier/"
PRODUCTION = "phase165_r52_r9_shared_math.py"
BASE_BLOB = "742451ea67ede314f99246afbb470a5e8a7f008f"
ANCHOR = (
    "        sources = sources + "
    "(register_positioned_prop27(Path(__file__).resolve().parent),)"
)
ADDITION = (
    "        from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (\n"
    "            build_cited_lower_delta_sources,\n"
    "        )\n"
    "        sources = sources + (\n"
    "            build_cited_lower_delta_sources(Path(__file__).resolve().parent),\n"
    "        )"
)


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, capture_output=True, check=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def reviewed_remote_head() -> str:
    """Allow only an exact HEAD or a successor adding only unchanged R33 files."""
    response = git("ls-remote", "origin", "refs/heads/develop")
    remote = response.split()[0] if response else ""
    if not remote:
        raise RuntimeError("Cannot verify GitHub origin/develop")
    if remote == BASE_HEAD:
        return remote
    git("fetch", "-q", "origin", "develop")
    if git("rev-parse", "FETCH_HEAD") != remote:
        raise RuntimeError("Remote HEAD advanced during source review")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
        cwd=ROOT, capture_output=True,
    )
    if ancestor.returncode:
        raise RuntimeError("GitHub lineage differs from reviewed R33 base")
    additions = git("diff", "--name-status", BASE_HEAD, remote).splitlines()
    if not additions or any(
        not item.startswith("A\t" + SINGLE_REVIEWED_SUCCESSOR_PREFIX)
        for item in additions
    ):
        raise RuntimeError("GitHub advanced outside reviewed R33 package; re-review")
    return remote


def patch_source(original: str) -> str:
    """Insert the exact R34 source builder once into the existing source tuple."""
    if type(original) is not str:
        raise TypeError("R34 installer accepts str source only")
    if original.count(ANCHOR) != 1:
        raise RuntimeError("Shared provider R30 anchor changed or is ambiguous")
    if original.count(ADDITION) == 1:
        return original
    if "build_cited_lower_delta_sources" in original:
        raise RuntimeError("Partial or unreviewed R34 source wiring found")
    return original.replace(ANCHOR, ANCHOR + "\n" + ADDITION, 1)


def expected_source_bytes(original: bytes) -> bytes:
    """Preserve source-file LF/CRLF faithfully rather than rewriting a tree."""
    if git_blob_sha(original) != BASE_BLOB:
        raise RuntimeError("Reviewed original production Git blob differs")
    text = original.decode("utf-8")
    if "\r\n" in text:
        patch = patch_source(text.replace("\r\n", "\n"))
        return patch.replace("\n", "\r\n").encode("utf-8")
    return patch_source(text).encode("utf-8")


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R34 must be extracted in the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R34 requires develop branch")
    remote = reviewed_remote_head()
    local = git("rev-parse", "HEAD")
    if local not in (BASE_HEAD, remote):
        raise RuntimeError("Local HEAD differs from reviewed R33 lineage")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged edits require review")
    changed = git("diff", "--name-only").splitlines()
    if any(filename != PRODUCTION for filename in changed):
        raise RuntimeError("Unexpected tracked edits; no reset performed")
    for directory in (
        "phase174_r3_r7_r30_prop27_public_provider_wiring",
        "phase174_r3_r7_r31_delta_surjectivity_general_audit",
        "phase174_r3_r7_r32_lower_delta_kernel_audit",
        "phase174_r3_r7_r33_three_premise_source_frontier",
    ):
        if not (ROOT / directory).is_dir():
            raise RuntimeError("Earlier phase missing: " + directory)
    base = subprocess.run(
        ("git", "show", local + ":" + PRODUCTION),
        cwd=ROOT, check=True, capture_output=True,
    ).stdout
    expected = expected_source_bytes(base)
    actual = (ROOT / PRODUCTION).read_bytes()
    if actual == base:
        mode = "BASELINE"
    elif actual.replace(b"\r\n", b"\n") == base.replace(b"\r\n", b"\n"):
        mode = "BASELINE_EOL_NORMALIZED"
    elif actual == expected:
        mode = "INSTALLED"
    elif actual.replace(b"\r\n", b"\n") == expected.replace(b"\r\n", b"\n"):
        mode = "INSTALLED_EOL_NORMALIZED"
    else:
        raise RuntimeError("Tracked production changes are not the exact R34 patch")
    reviewed_source_positions()
    checked_prior_statements()
    return {
        "local_head": local, "remote_head": remote,
        "source_guard": "PASS", "mode": mode,
        "earlier_phases_preserved": True,
    }


def install() -> dict[str, object]:
    state = preflight()
    if state["mode"].startswith("BASELINE"):
        path = ROOT / PRODUCTION
        data = path.read_bytes()
        text = data.decode("utf-8")
        if "\r\n" in text:
            installed = patch_source(text.replace("\r\n", "\n")).replace("\n", "\r\n")
        else:
            installed = patch_source(text)
        path.write_bytes(installed.encode("utf-8"))
    final = preflight()
    if final["mode"] == "BASELINE":
        raise RuntimeError("R34 installer did not apply the intended patch")
    return final


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = preflight() if args.dry_run else install()
    p = "PHASE174_R3R7R34_"
    for key, value in state.items():
        print(p + key.upper() + "=" + str(value))
    print(p + "RUN=" + ("DRYRUN_PASS" if args.dry_run else "INSTALL_PASS"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
