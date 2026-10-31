"""Phase 171 Closeout R2: guarded five-document full-file writer.

The reviewed repository files are read from the user's checked-out worktree.
All five complete revised files are exported. No full pytest is invoked.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_HEAD = "e814ec939652807d464fd76051d34a9da40328f8"
DOC_BLOBS = {
    "README.md": "cc65eea3ae9e4bf1e7d67d74550eda4f4f8b4024",
    "docs/design.md": "6f4a65431cf0e4ba2c517b521654e732568f45db",
    "docs/development_log.md": "64484312f89636c00e6d7dac670d719e81016eca",
    "docs/roadmap.md": "f6b48da7a853200c8b9323baff77731002d43026",
    "docs/proof_records.md": "0f4289bccca3558632f621596e04199e44360576",
}
SECTIONS = {
    "README.md": "readme.md",
    "docs/design.md": "design.md",
    "docs/development_log.md": "development_log.md",
    "docs/roadmap.md": "roadmap.md",
    "docs/proof_records.md": "proof_records.md",
}
SECTION_SHA256 = {
    # Filled at package build; these hashes protect reviewed document additions.
    "readme.md": "3950d718c0961c792526639e77112577b4bfdd1c9e672bbd5928d4edf256f058",
    "design.md": "a2f795706a43a0095a28ad4b65d1b1c4396750d14d0f26f6fdde08cc060ac507",
    "development_log.md": "3deb7d2dad9971664dbed6a37187abc8245b5c3eb537d5e5f2080df29e404616",
    "roadmap.md": "df6bfdef02530da7389f3ba09b39cecc4b733528d1711834e599be8fefee0ccc",
    "proof_records.md": "44bc5b3d430e8b3f602ecee16760e154385249cc879b8a2d4dca1f54ac4a06d6",
}
README_ANCHOR = "<!-- PHASE170_FINAL_DOCUMENT_CLOSEOUT_20261029 -->"
MARKER = "PHASE171_CLOSEOUT_R2_REVIEWED_20261031"
R1R1_TEST = "phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py"
R1R1_EXPECTED = "27ab6eb0a481eeb71ccf11603df4c7cbc8d2397380ca01f7d264d44f3fab2c84"
R1R1_SOURCE_BLOB = "b2b21c4fa35181fc0df45c3ef5af8433e147f891"
R1R1_COMMITTED_BLOB = "f98557eef6f2dd720c4b74ff28b8469e668df2f4"
FOCUSED = (
    "phase171_closeout_r2_documentation_full_output/tests/test_document_writer.py",
    "phase170_r3_r12_document_closeout/tests/test_document_contract.py",
    "phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py",
    "phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py",
)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    return result.stdout.rstrip("\r\n")


def lf_text(data: bytes) -> str:
    """Normalize one or more CR bytes followed by LF for comparison only.

    Historical documents may contain CRCRLF, CRLF, and LF together. A bare CR
    is not treated as a line ending, because silently changing it could alter
    a historical record.
    """
    value = data.decode("utf-8-sig")
    value = re.sub(r"\r+\n", "\n", value)
    if "\r" in value:
        raise ValueError("unknown line endings")
    return value


def document_newline(original: bytes) -> bytes:
    """Choose the final existing line separator, without changing old bytes."""
    index = original.rfind(b"\n")
    if index < 0:
        return b"\n"
    start = index
    while start > 0 and original[start - 1] == 13:
        start -= 1
    return original[start:index + 1]


def section_text(name: str) -> str:
    file = HERE / "sections" / name
    data = file.read_bytes()
    if hashlib.sha256(data).hexdigest() != SECTION_SHA256[name]:
        raise RuntimeError("reviewed section hash changed: " + name)
    return lf_text(data)


def updated_document(relative: str, original: bytes) -> bytes:
    """Generate a complete new file, preserving every historical source byte."""
    if relative not in DOC_BLOBS:
        raise ValueError("unreviewed document path")
    text = lf_text(original)
    section = section_text(SECTIONS[relative])
    if MARKER in text:
        raise ValueError("Phase 171 documentation marker already exists")
    if "Phase 171" not in section or "pytest" not in section:
        raise ValueError("reviewed Phase 171 section contract failed")
    newline = document_newline(original)
    section_bytes = section.encode("utf-8").replace(b"\n", newline)
    if relative == "README.md":
        anchor = README_ANCHOR + "\n"
        if text.count(anchor) != 1 or not section.startswith("<!-- " + MARKER + " -->"):
            raise ValueError("README insertion anchor missing or ambiguous")
        anchor_bytes = README_ANCHOR.encode("utf-8")
        if original.count(anchor_bytes) != 1:
            raise ValueError("README insertion anchor missing or ambiguous")
        position = original.index(anchor_bytes)
        changed = original[:position] + section_bytes + original[position:]
    else:
        if not (section.startswith("\n## ") or section.startswith("\n\n## ")):
            raise ValueError("append-only section marker missing")
        changed = original + section_bytes
    if lf_text(changed).count(MARKER) != (1 if relative == "README.md" else 0):
        raise ValueError("Phase 171 marker count invalid")
    if relative != "README.md" and not changed.startswith(original):
        raise ValueError("historical bytes not preserved")
    return changed


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp = tempfile.mkstemp(prefix=".phase171_r2_", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def current_files() -> tuple[dict[str, bytes], dict[str, bytes], set[str]]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    if head != EXPECTED_HEAD:
        try:
            git("merge-base", "--is-ancestor", EXPECTED_HEAD, "HEAD")
        except subprocess.CalledProcessError as exc:
            raise RuntimeError("local HEAD is not descended from reviewed base") from exc
        committed_delta = {
            path for path in git(
                "diff", "--name-only", EXPECTED_HEAD, "HEAD", "--"
            ).splitlines() if path
        }
        allowed_delta = {
            path for path in committed_delta
            if path == R1R1_TEST
            or path.startswith("phase171_closeout_r1_preflight_audit/")
            or path.startswith("phase171_closeout_r1r1_r3z_semantic_guard/")
        }
        if committed_delta != allowed_delta:
            raise RuntimeError(
                "unreviewed committed paths after reviewed base HEAD: "
                + ", ".join(sorted(committed_delta - allowed_delta))
            )
    if git("rev-parse", "origin/develop") != head:
        raise RuntimeError("local HEAD and origin/develop must match")
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes present")
    committed_test_blob = git("rev-parse", "HEAD:" + R1R1_TEST)
    if committed_test_blob not in {R1R1_SOURCE_BLOB, R1R1_COMMITTED_BLOB}:
        raise RuntimeError("historical R3Z test baseline is not reviewed")
    test_file = ROOT / R1R1_TEST
    if hashlib.sha256(lf_text(test_file.read_bytes()).encode("utf-8")).hexdigest() != R1R1_EXPECTED:
        raise RuntimeError("R1R1 semantic test fix has not been installed or differs")
    before: dict[str, bytes] = {}
    after: dict[str, bytes] = {}
    for relative, blob in DOC_BLOBS.items():
        if git("rev-parse", "HEAD:" + relative) != blob:
            raise RuntimeError("reviewed GitHub document blob changed: " + relative)
        source = (ROOT / relative).read_bytes()
        before[relative] = source
        committed = subprocess.run(["git", "show", "HEAD:" + relative],
                                   cwd=ROOT, capture_output=True, check=True).stdout
        if lf_text(source) == lf_text(committed):
            # A clean or platform-line-ending-only worktree preserves its
            # exact existing bytes; never normalize historical document text.
            after[relative] = updated_document(relative, source)
        else:
            expected = updated_document(relative, committed)
            if lf_text(source) != lf_text(expected):
                raise RuntimeError("unreviewed document worktree content: " + relative)
            # Already installed and fully reviewed: keep local historical
            # formatting rather than reconstituting the committed source.
            after[relative] = source
    tracked = {p for p in git("diff", "--name-only", "HEAD", "--").splitlines() if p}
    unexpected = tracked - {R1R1_TEST, *DOC_BLOBS}
    if unexpected:
        raise RuntimeError("unexpected tracked changes: " + ", ".join(sorted(unexpected)))
    if committed_test_blob == R1R1_SOURCE_BLOB and R1R1_TEST not in tracked:
        raise RuntimeError("R1R1 reviewed test change must remain in worktree")
    for relative in DOC_BLOBS:
        if relative in tracked and before[relative] != after[relative]:
            raise RuntimeError("pre-existing unreviewed document change: " + relative)
    missing = [p for p in FOCUSED if not (ROOT / p).is_file()]
    if missing:
        raise RuntimeError("missing focused test files: " + ", ".join(missing))
    return before, after, tracked


def output_directory() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home())))
    folder = base / "EHPProofTracerRecovery" / ("phase171_closeout_r2_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def run_focused() -> dict[str, object]:
    command = [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
               "--disable-warnings", "-p", "no:cacheprovider", *FOCUSED]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONUTF8"] = "1"
    proc = subprocess.run(command, cwd=ROOT, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, encoding="utf-8", errors="replace")
    print(proc.stdout, flush=True)
    return {"command": command, "exit_code": proc.returncode, "output": proc.stdout}


def export_full_documents(folder: Path, documents: dict[str, bytes]) -> Path:
    complete = folder / "FULL_DOCUMENTS"
    for relative, content in documents.items():
        atomic_write(complete / relative, content)
    archive = folder / "PHASE171_R2_FIVE_FULL_DOCUMENTS.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as stream:
        for relative, content in documents.items():
            stream.writestr(relative, content)
    return archive


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    before, after, tracked = current_files()
    head = git("rev-parse", "HEAD")
    print("PHASE171_CLOSEOUT_R2_HEAD=" + head, flush=True)
    print("PHASE171_CLOSEOUT_R2_REVIEWED_BASE=" + EXPECTED_HEAD, flush=True)
    print("PHASE171_CLOSEOUT_R2_DOCS=" + ",".join(DOC_BLOBS), flush=True)
    print("PHASE171_CLOSEOUT_R2_TRACKED_BEFORE=" + ",".join(sorted(tracked)), flush=True)
    print("PHASE171_CLOSEOUT_R2_FOCUSED_FILES=" + str(len(FOCUSED)), flush=True)
    if args.dry_run:
        print("PHASE171_CLOSEOUT_R2_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    destination = output_directory()
    for relative, value in before.items():
        atomic_write(destination / "BEFORE_FULL_DOCUMENTS" / relative, value)
    changed: list[str] = []
    report: dict[str, object] = {
        "phase": "171_CLOSEOUT_R2",
        "head": head,
        "reviewed_base": EXPECTED_HEAD,
        "full_pytest": False,
        "document_paths": list(DOC_BLOBS),
        "tracked_before": sorted(tracked),
    }
    try:
        for relative, content in after.items():
            target = ROOT / relative
            if target.read_bytes() != content:
                atomic_write(target, content)
                changed.append(relative)
        result = run_focused()
        report["focused"] = result
        if result["exit_code"]:
            raise RuntimeError("focused pytest failed")
        for relative, content in after.items():
            if (ROOT / relative).read_bytes() != content:
                raise RuntimeError("document unexpectedly changed after pytest: " + relative)
        expected_tracked = set(tracked) | set(DOC_BLOBS)
        current_tracked = set(git("diff", "--name-only", "HEAD", "--").splitlines())
        if current_tracked != expected_tracked:
            raise RuntimeError("unreviewed tracked change after tests")
        if git("diff", "--cached", "--name-only", "--"):
            raise RuntimeError("unexpected staged changes")
        archive = export_full_documents(destination, after)
        report["full_document_archive"] = str(archive)
        report["changed_documents"] = changed
        report["result"] = "PASS_FIVE_FULL_DOCUMENTS_PENDING_FULL_SUITE"
        print("PHASE171_CLOSEOUT_R2_FULL_DOCUMENTS=" + str(archive), flush=True)
        print("PHASE171_CLOSEOUT_R2_RESULT=" + str(report["result"]), flush=True)
        return 0
    except Exception as exc:
        for relative in reversed(changed):
            atomic_write(ROOT / relative, before[relative])
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["restored_documents"] = changed
        report["result"] = "FAILED_DOCUMENTS_RESTORED"
        print("PHASE171_CLOSEOUT_R2_RESULT=FAILED_DOCUMENTS_RESTORED", flush=True)
        return 1
    finally:
        report["tracked_after"] = git("diff", "--name-only", "HEAD", "--").splitlines()
        output = destination / "audit.json"
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE171_CLOSEOUT_R2_REPORT=" + str(output), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
