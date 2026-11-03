"""Exact source and reviewed commit-lineage guard for R15R3 read-only work."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess


REVIEWED_HEAD = "c44519a123fdbf2c5ec57fe9c89e2fb1027f41a5"
REVIEWED_BLOBS = {
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase169_r10eq_r1_universal_stable_definition/definition.py": "0c74d121419b6755e947a367d7de465d81193174",
    "phase173_r4_r15r1_unbounded_abstract_frontier/frontier.py": "efba543568e46e5b8303ee3ee794508213e2ee27",
}
AUDIT_PATH = "phase173_r4_r15r2_generator_obligation_audit/audit.py"
AUDIT_SHA256 = "9fbf9af9c4218a8ba019ce8fd131890e83a1392e6f0b9cd5f93d383d68305884"
ALLOWED_COMMITTED_PREFIX = "phase173_r4_r15r2_generator_obligation_audit/"
ALLOWED_DIRTY_FILES = {".pytest_cache/v/cache/nodeids"}


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ("git", *arguments), cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "git " + " ".join(arguments) + ": " + result.stderr[:500]
        )
    return result.stdout.strip()


def normalized(value: bytes) -> bytes:
    """Permit Windows CRLF without loosening substantive source guards."""
    return value.replace(b"\r\n", b"\n")


def git_bytes(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ("git", *arguments), cwd=root, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("Cannot read reviewed Git bytes: " + " ".join(arguments))
    return result.stdout


def guarded_descendant_paths(paths: tuple[str, ...]) -> bool:
    """Permit only the prior audit package and harmless test-cache history."""
    return all(
        item == ".pytest_cache/v/cache/nodeids"
        or item.startswith(ALLOWED_COMMITTED_PREFIX)
        for item in paths
    )


def preflight(root: Path) -> None:
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Not the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local/remote develop differs")
    # A later audit-only commit must not invalidate a source-reviewed phase.
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("Unreviewed HEAD lineage")
    committed_paths = tuple(filter(
        None, git(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()
    ))
    if not guarded_descendant_paths(committed_paths):
        raise RuntimeError("Unreviewed committed changes: " + str(committed_paths))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = set(filter(None, git(root, "diff", "--name-only").splitlines()))
    if dirty - ALLOWED_DIRTY_FILES:
        raise RuntimeError("Tracked source modifications require review")
    for name, blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("Committed dependency changed: " + name)
        if not (root / name).is_file():
            raise RuntimeError("Missing dependency: " + name)
        if normalized((root / name).read_bytes()) != normalized(
            git_bytes(root, "show", "HEAD:" + name)
        ):
            raise RuntimeError("Local dependency modified: " + name)
    previous_audit = root / AUDIT_PATH
    if not previous_audit.is_file():
        raise RuntimeError("R15R2 audit is required")
    digest = hashlib.sha256(normalized(previous_audit.read_bytes())).hexdigest()
    if digest != AUDIT_SHA256:
        raise RuntimeError("R15R2 audit changed: " + digest)
    print("PHASE173_R4_R15R3_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R3_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R3_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R3_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    preflight(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
