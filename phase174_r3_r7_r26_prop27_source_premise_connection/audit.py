"""Fail-closed R26 source and Git audit; no public proof registration."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from phase174_r3_r7_r26_prop27_source_premise_connection.bridge import (
    audited_prop27_source,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = "5349f850428085a162f5b286deebfaa0bdcfb9d0"
ALLOWED_PREFIXES = (
    "phase174_r3_r7_r24_prop27_general_typed_design/",
    "phase174_r3_r7_r25_prop27_isolated_inference/",
    "phase174_r3_r7_r26_prop27_source_premise_connection/",
)
ALLOWED_CACHE = ".pytest_cache/v/cache/nodeids"
PROTECTED = (
    "sources/toda/Toda_02_2.tex",
    "proof.py", "homotopy_groups.py",
    "tests/test_phase50_prop27_theorem_semantics.py",
)


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          text=True, capture_output=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def classify_changes(changed: tuple[str, ...]) -> tuple[str, ...]:
    unexpected = tuple(p for p in changed if p != ALLOWED_CACHE and not p.startswith(ALLOWED_PREFIXES))
    if unexpected:
        raise RuntimeError("Unreviewed committed or tracked changes: " + repr(unexpected))
    return changed


def audit() -> tuple[str, str, str]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract directly under repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop")
    head = git("rev-parse", "HEAD")
    line = git("ls-remote", "origin", "refs/heads/develop")
    remote = line.split()[0] if line else ""
    if remote != head:
        raise RuntimeError("Local/remote develop HEAD differ: review required")
    lineage = subprocess.run(("git", "merge-base", "--is-ancestor", BASE, head),
                             cwd=ROOT, capture_output=True)
    if lineage.returncode != 0:
        raise RuntimeError("Reviewed base is not an ancestor")
    classify_changes(tuple(git("diff", "--name-only", BASE, "HEAD").splitlines()))
    tracked = tuple(sorted(set(git("diff", "--name-only").splitlines()) |
                           set(git("diff", "--cached", "--name-only").splitlines())))
    classify_changes(tracked)
    for p in PROTECTED:
        before = subprocess.run(("git", "show", BASE + ":" + p),
                                cwd=ROOT, capture_output=True, check=True).stdout
        actual = (ROOT / p).read_bytes()
        lf = before.replace(b"\r\n", b"\n")
        if actual not in (before, lf, lf.replace(b"\n", b"\r\n")):
            raise RuntimeError("Protected source changed: " + p)
    evidence = audited_prop27_source(ROOT)
    if evidence.only_even_n is not True or evidence.sign_undetermined is not True:
        raise RuntimeError("Proposition 2.7 source contract changed")
    return head, remote, evidence.theorem_sha256


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head, remote, sha = audit()
    p = "PHASE174_R3R7R26_"
    print(p + "LOCAL_HEAD=" + head)
    print(p + "REMOTE_HEAD=" + remote)
    print(p + "SOURCE_GUARD=PASS")
    print(p + "PROP27_SOURCE_SHA256=" + sha)
    print(p + "SOURCE_TEXT_MATCH=True")
    print(p + "CONDITIONAL_INFERENCE_BRIDGE=True")
    print(p + "CERTIFIED_INPUT_STEP=NOT_PROVIDED")
    print(p + "NEW_GIVEN=0")
    print(p + "PUBLIC_REGISTRATION=False")
    print(p + "PUBLIC_VERIFIED_STEPS=NOT_CHECKED")
    print(p + "ROOT_COMPLETE=False")
    print(p + "FULL_PYTEST=False")
    print(p + "MODE=" + ("DRYRUN" if args.dry_run else "AUDIT"))
    print(p + "GATE=PASS_R26_SOURCE_MATCHED_CONDITIONAL_BRIDGE_CERTIFIED_PREMISE_PENDING")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
