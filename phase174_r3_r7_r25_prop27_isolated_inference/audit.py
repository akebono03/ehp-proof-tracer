"""R25 source-first guard with reviewed-ancestor lineage and explicit diagnostics.

R24 commits may follow the reviewed R23 merge; unrelated commits are rejected.
The single tracked pytest nodeids cache file may occur in reviewed commits.
No mathematics, production rule, GIVEN or search registration is changed.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_HEAD = "5349f850428085a162f5b286deebfaa0bdcfb9d0"
ALLOWED_TRACKED = {".pytest_cache/v/cache/nodeids"}
ALLOWED_COMMIT_PREFIXES = (
    "phase174_r3_r7_r24_prop27_general_typed_design/",
    "phase174_r3_r7_r25_prop27_isolated_inference/",
)
CHECKED = (
    "sources/toda/Toda_02_2.tex",
    "sources/toda/Toda_05_2.tex",
    "proof.py",
    "homotopy_groups.py",
    "tests/test_phase50_prop27_theorem_semantics.py",
)


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, capture_output=True,
        text=True, check=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def is_ancestor(ancestor: str, descendant: str) -> bool:
    process = subprocess.run(
        ("git", "merge-base", "--is-ancestor", ancestor, descendant),
        cwd=ROOT, capture_output=True,
    )
    if process.returncode not in (0, 1):
        raise RuntimeError("Could not inspect Git ancestry")
    return process.returncode == 0


def classify_lineage(local: str, remote: str, has_reviewed_ancestor: bool,
                     changed_committed: tuple[str, ...]) -> str:
    if not has_reviewed_ancestor:
        raise RuntimeError("Local HEAD does not descend from reviewed HEAD")
    if remote not in (REVIEWED_HEAD, local):
        raise RuntimeError(
            "Remote develop is neither reviewed HEAD nor local HEAD; "
            "fetch and independently review its history"
        )
    bad = tuple(path for path in changed_committed
                if path not in ALLOWED_TRACKED and not path.startswith(ALLOWED_COMMIT_PREFIXES))
    if bad:
        raise RuntimeError("Unreviewed committed paths: " + repr(bad))
    return "REVIEWED_HEAD" if local == REVIEWED_HEAD else "R24_R25_ONLY_DESCENDANT"


def audit() -> tuple[str, str, str]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R25 at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD")
    remote_output = git("ls-remote", "origin", "refs/heads/develop")
    if not remote_output:
        raise RuntimeError("Cannot read remote develop HEAD")
    remote = remote_output.split()[0]
    print("PHASE174_R3R7R25_LOCAL_HEAD=" + local)
    print("PHASE174_R3R7R25_REMOTE_HEAD=" + remote)
    changed_committed = tuple(git("diff", "--name-only", REVIEWED_HEAD, "HEAD").splitlines())
    lineage = classify_lineage(
        local, remote, is_ancestor(REVIEWED_HEAD, local), changed_committed,
    )
    modified = set(git("diff", "--name-only").splitlines()) | set(
        git("diff", "--cached", "--name-only").splitlines()
    )
    unexpected = modified - ALLOWED_TRACKED
    if unexpected:
        raise RuntimeError("Unreviewed tracked changes: " + repr(sorted(unexpected)))
    for path in CHECKED:
        stored = subprocess.run(
            ("git", "show", REVIEWED_HEAD + ":" + path), cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        actual = (ROOT / path).read_bytes()
        lf = stored.replace(b"\r\n", b"\n")
        if actual not in (stored, lf, lf.replace(b"\n", b"\r\n")):
            raise RuntimeError("Reviewed source changed: " + path)
    source = (ROOT / CHECKED[0]).read_text(encoding="utf-8-sig")
    if (r"\begin{proposition}\label{prop:2.7}" not in source
            or r"H\!\bigl(\Delta(\iota_{2n+1})\bigr)\ =\ \pm\,2\,\iota_{2n-1}" not in source
            or "$n$ が偶数のとき" not in source):
        raise RuntimeError("Proposition 2.7 source contract changed")
    value = typed_specialization(6)
    if value.delta.target_group != value.hopf.source_group:
        raise RuntimeError("Delta/Hopf domain mismatch")
    return local, remote, lineage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    local, remote, lineage = audit()
    prefix = "PHASE174_R3R7R25_"
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "HEAD=" + local)
    print(prefix + "LINEAGE=" + lineage)
    print(prefix + "N6_TYPED_DELTA_HOPF=True")
    print(prefix + "SIGNED_RELATION_UNDETERMINED=True")
    print(prefix + "NEW_GIVEN=0")
    print(prefix + "PUBLIC_REGISTRATION=False")
    print(prefix + "PUBLIC_VERIFIED_STEPS=NOT_CHECKED")
    print(prefix + "ROOT_COMPLETE=False")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "MODE=" + ("DRYRUN" if args.dry_run else "AUDIT"))
    print(prefix + "GATE=PASS_R25_ISOLATED_TYPED_INFERENCE_PUBLIC_PREMISE_PENDING")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
