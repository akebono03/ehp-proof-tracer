"""Safely close out R10ET documentation against the reviewed GitHub develop tree.

The five updated documents are constructed from the FULL local originals.
No historical development/proof-record content is rewritten or truncated.
This tool never stages, commits, pulls, resets, or runs the full test suite.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
import zipfile

sys.dont_write_bytecode = True

REVIEWED_HEAD = "a759c12fbcc0a7fc64c578fcd8a4dd86ac94b3c5"
DOCUMENT_BLOBS = {
    "README.md": "06eb0dde339dabfe25e34c066f35a4edbce66713",
    "docs/design.md": "dc2495137242eb9f69b65df108c98d323f1e6294",
    "docs/development_log.md": "067d3a3b285e6e489cb1c2e8a1583e29f29598cb",
    "docs/roadmap.md": "47185fb87571eed1ff57a65d4a890dab0260d90c",
    "docs/proof_records.md": "2e9a1c24e638dba408c46b9a1a6d10c706d5255b",
}
REVIEWED_SOURCE_BLOBS = {
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_5_model_renderer.py": "4b4478ccbc20a4264be86e61b7a2c72f69b1e5b0",
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py": "daad1b7b246c4b005bd529637f82e64ce85a9cfe",
    "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py": "f0664c1e28793f5a3ab341b17eb5e7ded0724436",
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py": "9038d656aac21311a5272e4d62551cce435037c3",
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py": "65f65b5bacdbec9cc4257b2c96140720568097a3",
    "phase169_r10et_r6_residual_definition_dependency_audit/audit.py": "ae883ad6ec24382dfc4bac26790a4a2b7e8fa54e",
}
APPENDIX_PATHS = {
    "README.md": "readme_current.md",
    "docs/design.md": "design_append.md",
    "docs/development_log.md": "development_append.md",
    "docs/roadmap.md": "roadmap_append.md",
    "docs/proof_records.md": "proof_append.md",
}
MARKER = "<!-- PHASE169_R10ET_DOCUMENT_CLOSEOUT_20261028 -->"
README_ANCHOR = "## Current status — Phase 168 closed (2026-10-25)"


def updated_document(path: str, original: bytes, appendix: str) -> bytes:
    """Compose full final bytes while preserving every historical byte."""
    if path not in DOCUMENT_BLOBS:
        raise ValueError(f"Unexpected document path: {path}")
    if not original or not appendix or not appendix.endswith("\n"):
        raise ValueError("Expected nonempty original and complete appendix")
    source = original.decode("utf-8")
    if MARKER in source or "Phase 169 R10ET complete; Phase 169 remains open" in source:
        raise ValueError(f"Document appears already updated: {path}")
    if path == "README.md":
        if source.count(README_ANCHOR) != 1:
            raise ValueError("README Phase 168 heading missing or ambiguous")
        return source.replace(README_ANCHOR, appendix + README_ANCHOR, 1).encode("utf-8")
    if not appendix.startswith(MARKER):
        raise ValueError(f"Missing append-only historical marker: {path}")
    if not source.lstrip().startswith("#"):
        raise ValueError(f"Expected Markdown source: {path}")
    separator = b"\n" if original.endswith(b"\n") else b"\n\n"
    return original + separator + appendix.encode("utf-8")


def git(root: Path, *arguments: str, timeout: int = 30) -> str:
    env = os.environ.copy()
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0",
                "GCM_INTERACTIVE": "Never"})
    call = subprocess.run(
        ["git", "-c", "core.longpaths=true", "-C", str(root), *arguments],
        text=True, encoding="utf-8", errors="replace", capture_output=True,
        timeout=timeout, env=env, check=False,
    )
    if call.returncode:
        raise RuntimeError(
            f"Git {arguments} failed ({call.returncode}): {call.stderr.strip()}"
        )
    return call.stdout.strip()


def verify_git_state(root: Path) -> None:
    """Require the exact currently reviewed, clean tracked input tree."""
    if not (root / ".git").exists():
        raise RuntimeError("Missing .git at repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    if git(root, "rev-parse", "HEAD") != REVIEWED_HEAD:
        raise RuntimeError("Unexpected HEAD: refusing to update documentation")
    if git(root, "rev-parse", "refs/remotes/origin/develop") != REVIEWED_HEAD:
        raise RuntimeError("Unexpected origin/develop: refusing update")
    raw = git(root, "ls-remote", "origin", "refs/heads/develop", timeout=25)
    expected = f"{REVIEWED_HEAD}\trefs/heads/develop"
    if raw != expected:
        raise RuntimeError("GitHub develop moved or cannot be verified")
    if git(root, "diff", "--name-only") or git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Tracked worktree/index is not clean: no update")
    for path, expected_blob in {**REVIEWED_SOURCE_BLOBS, **DOCUMENT_BLOBS}.items():
        actual = git(root, "hash-object", f"--path={path}", path, timeout=12)
        if actual != expected_blob:
            raise RuntimeError(f"Reviewed file differs from GitHub: {path}")


def outside_repository(root: Path) -> Path:
    raw = os.environ.get("LOCALAPPDATA", "")
    if not raw:
        raise RuntimeError("LOCALAPPDATA must be defined")
    folder = Path(raw).resolve() / "EHPProofTracerRecovery"
    if root == folder or root in folder.parents or folder in root.parents:
        raise RuntimeError("Output folder must be outside repository/Dropbox")
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output = folder / ("r10et_closeout_r2_" + stamp)
    output.mkdir(parents=False, exist_ok=False)
    return output


def atomic_file_write(path: Path, content: bytes) -> None:
    """Replace a single complete document, never a partial write."""
    descriptor, temp = tempfile.mkstemp(prefix="._r10et_doc_", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def create_full_archive(output: Path) -> Path:
    archive = output / "updated_five_documents_FULL.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in DOCUMENT_BLOBS:
            bundle.write(output / "AFTER_FULL" / path, path)
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None or set(bundle.namelist()) != set(DOCUMENT_BLOBS):
            raise RuntimeError("Updated documents archive failed validation")
    return archive


def execute(root: Path, package: Path) -> int:
    print("R10ET_CLOSEOUT_R2_MODE=DOCUMENT_ONLY", flush=True)
    verify_git_state(root)
    before: dict[str, bytes] = {}
    after: dict[str, bytes] = {}
    for path in DOCUMENT_BLOBS:
        source = (root / path).read_bytes()
        appendix = (package / "appendices" / APPENDIX_PATHS[path]).read_text(encoding="utf-8")
        original_sha = hashlib.sha256(source).hexdigest()
        expected = git(root, "hash-object", f"--path={path}", path)
        if expected != DOCUMENT_BLOBS[path]:
            raise RuntimeError(f"Late document drift: {path}")
        updated = updated_document(path, source, appendix)
        if hashlib.sha256(source).hexdigest() != original_sha:
            raise RuntimeError(f"Original bytes changed during preparation: {path}")
        before[path], after[path] = source, updated
    backup_root = outside_repository(root)
    for path in DOCUMENT_BLOBS:
        old = backup_root / "BEFORE_FULL" / path
        new = backup_root / "AFTER_FULL" / path
        old.parent.mkdir(parents=True, exist_ok=True)
        new.parent.mkdir(parents=True, exist_ok=True)
        old.write_bytes(before[path])
        new.write_bytes(after[path])
    archive = create_full_archive(backup_root)
    patch_lines: list[str] = ["# Phase 169 R10ET Closeout R2 — 文書変更レビュー", "",
                              "変更対象は下記の5ファイルのみ。原本・更新後の全文は各フォルダに保存。", ""]
    for path in DOCUMENT_BLOBS:
        patch_lines.extend([f"## `{path}`", "", "```diff"])
        patch_lines.extend(difflib.unified_diff(
            before[path].decode("utf-8").splitlines(),
            after[path].decode("utf-8").splitlines(),
            fromfile="BEFORE_FULL/" + path, tofile="AFTER_FULL/" + path,
            lineterm="",
        ))
        patch_lines.extend(["```", ""])
    (backup_root / "CHANGE_REVIEW.md").write_text("\n".join(patch_lines), encoding="utf-8")
    print("R10ET_CLOSEOUT_R2_BACKUP=" + str(backup_root), flush=True)
    written: list[str] = []
    try:
        # Last check before any write: no concurrent Git change.
        verify_git_state(root)
        for path in DOCUMENT_BLOBS:
            if (root / path).read_bytes() != before[path]:
                raise RuntimeError(f"Concurrent document update: {path}")
            atomic_file_write(root / path, after[path])
            written.append(path)
            print("R10ET_CLOSEOUT_R2_UPDATED=" + path, flush=True)
        for path in DOCUMENT_BLOBS:
            if (root / path).read_bytes() != after[path]:
                raise RuntimeError(f"Postwrite content mismatch: {path}")
        staged = git(root, "diff", "--cached", "--name-only")
        unstaged = git(root, "diff", "--name-only").splitlines()
        if staged or set(unstaged) != set(DOCUMENT_BLOBS):
            raise RuntimeError(f"Unexpected tracked changes after document update: {unstaged}")
        if git(root, "rev-parse", "HEAD") != REVIEWED_HEAD:
            raise RuntimeError("HEAD moved during document update")
        record = {"head": REVIEWED_HEAD, "phase_169_closed": False,
                  "full_pytest_executed": False, "index_modified": False,
                  "documents": [
                      {"path": path, "before_git_blob": DOCUMENT_BLOBS[path],
                       "before_sha256": hashlib.sha256(before[path]).hexdigest(),
                       "after_sha256": hashlib.sha256(after[path]).hexdigest(),
                       "after_bytes": len(after[path])}
                      for path in DOCUMENT_BLOBS
                  ]}
        (backup_root / "manifest.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
    except BaseException:
        for path in written:
            atomic_file_write(root / path, before[path])
        print("R10ET_CLOSEOUT_R2_ROLLBACK=RESTORED_ALL_UPDATED_DOCUMENTS", flush=True)
        raise
    print("R10ET_CLOSEOUT_R2_FULL_DOCS=" + str(archive), flush=True)
    print("R10ET_CLOSEOUT_R2_CHANGE_REVIEW=" + str(backup_root / "CHANGE_REVIEW.md"), flush=True)
    print("R10ET_CLOSEOUT_R2_DOC_COUNT=5", flush=True)
    print("R10ET_CLOSEOUT_R2_STAGED_INDEX_UNCHANGED=True", flush=True)
    print("R10ET_CLOSEOUT_R2_FULL_PYTEST_NOT_RUN=True", flush=True)
    print("R10ET_CLOSEOUT_R2_COMPLETE=PASS", flush=True)
    print("R10ET_CLOSEOUT_R2_EXIT=0", flush=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parsed = parser.parse_args(argv)
    try:
        return execute(parsed.repo.resolve(), Path(__file__).resolve().parent)
    except BaseException:
        print("R10ET_CLOSEOUT_R2_ERROR=" + traceback.format_exc(), flush=True)
        print("R10ET_CLOSEOUT_R2_EXIT=1", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
