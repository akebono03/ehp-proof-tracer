"""R15R16R3R1: install one reviewed CRLF-sensitive test correction only."""
from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
RELATIVE = Path("phase173_r4_r15r16r3_staged_guard_fix/tests/test_staged_guard.py")
TARGET = ROOT / RELATIVE
BASELINE = PACKAGE / "baseline_test_staged_guard.py.txt"
CORRECTED = PACKAGE / "test_staged_guard.py"
REVIEWED_HEAD = "92f967c079f4a66e19a598e0acc54b742f11df9c"
BASELINE_HASH = "31274cba1a86f3a695cb9f510c2c0de5bc647393a3bdc203911ac74be2438bb5"
CORRECTED_HASH = "8878fd8fd8990e902a8289eeaebabc5077df79cc8110ce44ea08f47fb0e5eebd"


def normalized(contents: bytes) -> bytes:
    return contents.replace(b"\r\n", b"\n")


def git(*arguments: str, binary: bool = False):
    response = subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True,
        check=False, **({} if binary else {"text": True, "encoding": "utf-8", "errors": "replace"}),
    )
    if response.returncode != 0:
        raise RuntimeError("git command failed: " + " ".join(arguments))
    return response.stdout if binary else response.stdout.strip()


def guard() -> str:
    if not TARGET.is_file():
        raise RuntimeError("existing R15R16R3 regression test is missing")
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if branch != "develop" or head != remote:
        raise RuntimeError("develop local/remote HEAD mismatch")
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if ancestry.returncode != 0:
        raise RuntimeError("HEAD is not descended from reviewed R15R16")
    before = BASELINE.read_bytes()
    after = CORRECTED.read_bytes()
    if sha256(before).hexdigest() != BASELINE_HASH:
        raise RuntimeError("packaged baseline test content changed")
    if sha256(after).hexdigest() != CORRECTED_HASH:
        raise RuntimeError("packaged corrected test content changed")
    present = normalized(TARGET.read_bytes())
    present_hash = sha256(present).hexdigest()
    if present_hash not in (BASELINE_HASH, CORRECTED_HASH):
        raise RuntimeError("local regression test was edited; refusing to overwrite")
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    if RELATIVE.as_posix() in staged:
        indexed = normalized(git("show", ":" + RELATIVE.as_posix(), binary=True))
        indexed_hash = sha256(indexed).hexdigest()
        if indexed_hash not in (BASELINE_HASH, CORRECTED_HASH):
            raise RuntimeError("staged test content differs from reviewed test")
        if present_hash == BASELINE_HASH and indexed_hash != BASELINE_HASH:
            raise RuntimeError("staged test differs from pre-install working tree")
    print("R15R16R3R1_LOCAL_HEAD=" + head, flush=True)
    print("R15R16R3R1_INDEX_MODIFIED=False", flush=True)
    print("R15R16R3R1_SOURCE_GUARD=PASS", flush=True)
    return "corrected" if present_hash == CORRECTED_HASH else "baseline"


def project(template: bytes, original: bytes) -> bytes:
    if b"\r\n" in original:
        return normalized(template).replace(b"\n", b"\r\n")
    return normalized(template)


def install() -> None:
    state = guard()
    if state == "corrected":
        print("R15R16R3R1_ALREADY_INSTALLED=True", flush=True)
        return
    source = TARGET.read_bytes()
    TARGET.write_bytes(project(CORRECTED.read_bytes(), source))
    print("R15R16R3R1_TEST_CORRECTED=True", flush=True)
    print("R15R16R3R1_PRODUCTION_EDIT=NONE", flush=True)


def restore() -> None:
    state = guard()
    if state == "baseline":
        print("R15R16R3R1_ALREADY_RESTORED=True", flush=True)
        return
    source = TARGET.read_bytes()
    TARGET.write_bytes(project(BASELINE.read_bytes(), source))
    print("R15R16R3R1_TEST_RESTORED=True", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    choices = parser.add_mutually_exclusive_group(required=True)
    choices.add_argument("--dry-run", action="store_true")
    choices.add_argument("--install", action="store_true")
    choices.add_argument("--restore", action="store_true")
    options = parser.parse_args()
    try:
        if options.dry_run:
            state = guard()
            print("R15R16R3R1_EXISTING_TEST_STATE=" + state, flush=True)
            print("R15R16R3R1_DRY_RUN=PASS", flush=True)
        elif options.install:
            install()
        else:
            restore()
        return 0
    except (RuntimeError, OSError, UnicodeError) as exc:
        print("R15R16R3R1_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
