"""Fail-closed source guard with allowance for committed prior R15R3 package."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess


REVIEWED_BASE_HEAD = "3901da80ac4af7226b41246353b700708a33c085"
REVIEWED_BLOBS = {
    "phase169_r10d2_general_family_definition/family_citation.py": "b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8",
    "phase169_r10e8_hyoujigen_generic_suspension/source_records.py": "bb54cc49092c6b16c4b83b113b325e028a42f50c",
    "phase169_r10b_registered_stable_family_binding/family_registry.py": "4e461795954cc3e7a34fe9e3b47f77d00e5faeda",
    "phase169_r10e8_hyoujigen_generic_suspension/chapter_vi_reference.py": "e3b2f167428ba6b230acd8505b976eea189d39ff",
    "phase169_r10eq_r1_universal_stable_definition/definition.py": "0c74d121419b6755e947a367d7de465d81193174",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
}
LOCAL_PINNED = {
    "phase173_r4_r15r2_generator_obligation_audit/audit.py": "9fbf9af9c4218a8ba019ce8fd131890e83a1392e6f0b9cd5f93d383d68305884",
    "phase173_r4_r15r3_formal_suspension_bridge/bridge.py": "0e2a44e97ae8d87aca02559cda5d0b8e14c1c2a161a966b5f34bb36140459adf",
}
ALLOWED_COMMITTED = "phase173_r4_r15r3_formal_suspension_bridge/"
ALLOWED_DIRTY = frozenset({".pytest_cache/v/cache/nodeids"})


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + result.stderr[:500])
    return result.stdout.strip()


def verify_source_head(root: Path) -> None:
    """Accept only the inspected HEAD lineage with intact pinned dependencies."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Not the EHP Proof Tracer repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local develop and origin/develop differ")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_BASE_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed HEAD lineage")
    changed = tuple(filter(None, git(
        root, "diff", "--name-only", REVIEWED_BASE_HEAD, head,
    ).splitlines()))
    if any(
        path != ".pytest_cache/v/cache/nodeids"
        and not path.startswith(ALLOWED_COMMITTED)
        for path in changed
    ):
        raise RuntimeError("Unreviewed committed dependencies: " + repr(changed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = set(filter(None, git(root, "diff", "--name-only").splitlines()))
    if dirty - ALLOWED_DIRTY:
        raise RuntimeError("Unreviewed tracked local source modifications")
    for path, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Unexpected Git blob for " + path)
        if git(root, "hash-object", "--", path) != expected:
            raise RuntimeError("Modified working tree dependency: " + path)
    for path, expected in LOCAL_PINNED.items():
        target = root / path
        if not target.is_file():
            raise RuntimeError("Required previous phase source missing: " + path)
        actual = hashlib.sha256(
            target.read_bytes().replace(b"\r\n", b"\n")
        ).hexdigest()
        if actual != expected:
            raise RuntimeError("Previous phase source changed: " + path)
    print("PHASE173_R4_R15R4_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R4_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R4_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R4_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    verify_source_head(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
