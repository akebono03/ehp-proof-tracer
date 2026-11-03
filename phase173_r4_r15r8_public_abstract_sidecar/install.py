"""Guarded, reversible two-file installation for the public abstract sidecar."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from phase173_r4_r15r8_public_abstract_sidecar.patch_source import (
    transform_model,
    transform_selector,
    full_replacement_units,
)

REVIEWED_HEAD = "9d5b57205ebf001c7eb6981de71a626fb5aeafa2"
REVIEWED_BLOBS = {
    "phase165_r52_partial_proof.py": "669fb947f1f9b4670d10723f8a562e60c015b249",
    "phase165_r55_nk_only_goal.py": "8afedad058c040a4d618af04485b83e93aacf5a4",
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase173_r4_r10_general_toda56_core/tests/test_core.py": "68205bf2840688a7b5d7277875c513323be7a5fc",
}
REVIEWED_PREVIOUS_FILES = {
    "phase173_r4_r15r7_source_first_abstract_certificate/search.py": "e7026a26302816a4d06eb5d99b35d46f9e16ceeb4f9477c6fa2435e0f3776fe1",
    "phase173_r4_r15r7_source_first_abstract_certificate/source.py": "4d4f64fe2470dcf32da38463edc21dc4e4f05a406b36e34d0f15810d4821aadd",
    "phase173_r4_r15r6_abstract_toda44_rule/abstract_rule.py": "fceab3505977b741e0756221b8c7c7abb70339ca75527e55f1924f23f7b54444",
}
TARGETS = {
    "phase165_r52_partial_proof.py": transform_model,
    "phase165_r55_nk_only_goal.py": transform_selector,
}
PACKAGE = "phase173_r4_r15r8_public_abstract_sidecar"
REPORT_FILE = "installed_state.json"


def git(root: Path, *args: str, binary: bool = False):
    result = subprocess.run(("git", *args), cwd=root, capture_output=True,
                            text=not binary, encoding=None if binary else "utf-8",
                            errors=None if binary else "replace", check=False)
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + " failed: " + str(result.stderr)[:500])
    return result.stdout if binary else result.stdout.strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(normalized(data)).hexdigest()


def reviewed_patch(root: Path) -> tuple[dict[str, bytes], dict[str, bytes], dict[str, str]]:
    originals: dict[str, bytes] = {}
    patched: dict[str, bytes] = {}
    states: dict[str, str] = {}
    for name, transform in TARGETS.items():
        if git(root, "rev-parse", "HEAD:" + name) != REVIEWED_BLOBS[name]:
            raise RuntimeError("Unreviewed Git blob: " + name)
        baseline = git(root, "show", "HEAD:" + name, binary=True)
        existing = (root / name).read_bytes()
        next_bytes = transform(baseline)
        originals[name] = baseline
        patched[name] = next_bytes
        if normalized(existing) == normalized(baseline):
            states[name] = "BASELINE"
        elif normalized(existing) == normalized(next_bytes):
            states[name] = "PATCHED"
        else:
            raise RuntimeError("Unreviewed worktree content: " + name)
    return originals, patched, states


def preflight(root: Path):
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Wrong repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    if git(root, "rev-parse", "origin/develop") != head:
        raise RuntimeError("Local and remote develop do not agree")
    ancestor = subprocess.run(("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
                              cwd=root, check=False)
    if ancestor.returncode != 0:
        raise RuntimeError("Unreviewed HEAD lineage")
    changed = tuple(filter(None, git(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()))
    if any(not (path == ".pytest_cache/v/cache/nodeids"
                or path.startswith("phase173_r4_r15r7_source_first_abstract_certificate/"))
           for path in changed):
        raise RuntimeError("Unreviewed committed change: " + repr(changed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = tuple(filter(None, git(root, "diff", "--name-only").splitlines()))
    if any(name not in TARGETS and name != ".pytest_cache/v/cache/nodeids" for name in dirty):
        raise RuntimeError("Other tracked modifications require review: " + repr(dirty))
    for name, blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("Dependency source blob mismatch: " + name)
        if name not in TARGETS and git(root, "hash-object", "--", name) != blob:
            raise RuntimeError("Dependency worktree changed: " + name)
    for name, expected in REVIEWED_PREVIOUS_FILES.items():
        file = root / name
        if not file.is_file() or sha(file.read_bytes()) != expected:
            raise RuntimeError("Unreviewed preceding phase file: " + name)
    originals, patched, states = reviewed_patch(root)
    if len(set(states.values())) > 1:
        raise RuntimeError("Mixed baseline/installed state requires review")
    print("PHASE173_R4_R15R8_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R8_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R8_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R8_INSTALL_STATE=" + next(iter(states.values())), flush=True)
    return originals, patched, states


def install(root: Path, package: Path, *, dry_run: bool) -> None:
    originals, patched, states = preflight(root)
    preview = full_replacement_units(originals["phase165_r52_partial_proof.py"],
                                     originals["phase165_r55_nk_only_goal.py"])
    (package / "FULL_CHANGED_UNITS.md").write_text(
        "# Complete revised production classes and function\n\n" + preview,
        encoding="utf-8",
    )
    if dry_run:
        print("PHASE173_R4_R15R8_DRY_RUN=PASS", flush=True)
        print("PHASE173_R4_R15R8_PRODUCTION_EDIT=NONE", flush=True)
        return
    if next(iter(states.values())) == "PATCHED":
        print("PHASE173_R4_R15R8_ALREADY_INSTALLED=True", flush=True)
        return
    backup = package / "reviewed_originals"
    backup.mkdir(parents=True, exist_ok=True)
    for name, content in originals.items():
        (backup / (Path(name).name + ".bak")).write_bytes(content)
    try:
        for name, content in patched.items():
            destination = root / name
            tmp = destination.with_suffix(destination.suffix + ".r15r8_tmp")
            tmp.write_bytes(content)
            tmp.replace(destination)
    except Exception:
        for name, content in originals.items():
            (root / name).write_bytes(content)
        raise
    (package / REPORT_FILE).write_text(json.dumps({
        "phase": "173-R4-R15R8", "before": {k: sha(v) for k,v in originals.items()},
        "after": {k: sha(v) for k,v in patched.items()},
        "completed_named_proof_promoted": False,
    }, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R15R8_PATCHED=" + ",".join(TARGETS), flush=True)


def restore(root: Path, package: Path):
    originals, patched, states = preflight(root)
    backup = package / "reviewed_originals"
    if next(iter(states.values())) != "PATCHED":
        print("PHASE173_R4_R15R8_RESTORE=SKIPPED_BASELINE", flush=True)
        return
    for name, original in originals.items():
        saved = backup / (Path(name).name + ".bak")
        if not saved.is_file() or sha(saved.read_bytes()) != sha(original):
            raise RuntimeError("Reviewed rollback backup missing: " + name)
    for name in TARGETS:
        (root / name).write_bytes((backup / (Path(name).name + ".bak")).read_bytes())
    print("PHASE173_R4_R15R8_ROLLBACK=PASS", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    package = Path(__file__).resolve().parent
    if args.restore:
        restore(root, package)
    else:
        install(root, package, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
