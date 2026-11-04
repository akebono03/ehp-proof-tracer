"""R15R11 guarded, reversible integration of abstract certificates into Narrative Model."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from .patch import EXPECTED_BLOBS, EXPECTED_HEAD, apply_to_source, changed_units


def _git(root: Path, *args: str) -> str:
    p = subprocess.run(("git", *args), cwd=root, check=True,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout.strip()


def _hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        tmp.write(raw)
        temp = Path(tmp.name)
    os.replace(temp, path)


def preflight(root: Path) -> dict[str, tuple[bytes, bytes]]:
    root = root.resolve()
    if _git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R15R11 requires develop")
    if _git(root, "rev-parse", "origin/develop") != EXPECTED_HEAD:
        raise RuntimeError("GitHub develop HEAD changed; rereview before applying")
    if _git(root, "rev-parse", "HEAD") != EXPECTED_HEAD:
        raise RuntimeError("Local HEAD does not match reviewed GitHub HEAD")
    if _git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Review staged changes before applying")
    proposal: dict[str, tuple[bytes, bytes]] = {}
    for rel, sha in EXPECTED_BLOBS.items():
        path = root / rel
        if not path.is_file():
            raise RuntimeError(f"Missing reviewed file: {rel}")
        actual = _git(root, "hash-object", f"--path={rel}", rel)
        if actual != sha:
            raise RuntimeError(f"Unreviewed {rel}: expected {sha}; got {actual}")
        original = path.read_bytes()
        new = apply_to_source(rel, original)
        proposal[rel] = (original, new)
    return proposal


def emit_review(package: Path, proposal: dict[str, tuple[bytes, bytes]]) -> None:
    sections = ["# Phase 173 R4-R15R11 — Full changed units (reviewed proposed code)",
                "", "Every changed class/function is shown in full. No omitted code.", ""]
    for rel, (_, patched) in proposal.items():
        sections.append(changed_units(rel, patched))
    _atomic_write(package / "FULL_CHANGED_UNITS.md", "\n".join(sections).encode("utf-8"))


def apply(root: Path, package: Path) -> None:
    proposal = preflight(root)
    state = package / "installed_state.json"
    backup_dir = package / "backups"
    if state.exists() or backup_dir.exists():
        raise RuntimeError("Existing R15R11 installation state requires review")
    emit_review(package, proposal)
    backups: dict[str, dict[str, str]] = {}
    for rel, (original, proposed) in proposal.items():
        backups[rel] = {"original_sha256": _hash(original), "patched_sha256": _hash(proposed)}
    written = []
    try:
        for rel, (original, proposed) in proposal.items():
            backup = backup_dir / rel
            _atomic_write(backup, original)
            _atomic_write(root / rel, proposed)
            written.append(rel)
        _atomic_write(state, json.dumps(backups, indent=2, ensure_ascii=False).encode("utf-8"))
    except Exception:
        for rel in reversed(written):
            _atomic_write(root / rel, proposal[rel][0])
        raise
    print("PHASE173_R4_R15R11_PATCHED_FILES=" + str(len(proposal)), flush=True)


def restore(root: Path, package: Path) -> None:
    state = package / "installed_state.json"
    if not state.is_file():
        raise RuntimeError("No prior R15R11 installation state")
    data = json.loads(state.read_text(encoding="utf-8"))
    if set(data) != set(EXPECTED_BLOBS):
        raise RuntimeError("Installation state does not match reviewed target files")
    for rel, checks in data.items():
        original = (package / "backups" / rel).read_bytes()
        current = (root / rel).read_bytes()
        if _hash(original) != checks["original_sha256"]:
            raise RuntimeError("Backup mismatch, refusing restore")
        if _hash(current) != checks["patched_sha256"]:
            raise RuntimeError(f"User has modified {rel}; refusing to overwrite")
    for rel in data:
        _atomic_write(root / rel, (package / "backups" / rel).read_bytes())
    state.unlink()
    print("PHASE173_R4_R15R11_RESTORED=PASS", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--restore", action="store_true")
    opts = p.parse_args()
    if sum((opts.dry_run, opts.apply, opts.restore)) != 1:
        p.error("Choose one operation")
    package = Path(__file__).resolve().parent
    if opts.restore:
        restore(opts.root, package)
        return
    proposal = preflight(opts.root)
    emit_review(package, proposal)
    print("PHASE173_R4_R15R11_SOURCE_GUARD=PASS", flush=True)
    if opts.dry_run:
        print("PHASE173_R4_R15R11_DRY_RUN=PASS", flush=True)
        print("PHASE173_R4_R15R11_PRODUCTION_EDIT=NONE", flush=True)
        return
    apply(opts.root, package)


if __name__ == "__main__":
    main()
