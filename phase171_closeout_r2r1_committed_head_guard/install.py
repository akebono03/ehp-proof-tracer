"""Phase 171 Closeout R2R1: guarded replacement of an R2-only HEAD check."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
R2 = ROOT / "phase171_closeout_r2_documentation_full_output"
REPLACEMENTS = {
    "update_docs.py": "replacements/update_docs.py",
    "tests/test_document_writer.py": "replacements/tests/test_document_writer.py",
}
OLD_HASHES = {
    "update_docs.py": "19a65bc5b3e4c2ea38ec8216cc320bade803e5daa247e58f3075a4e79a59f247",
    "tests/test_document_writer.py": "ce7a2065ea346c879e29fe1258f919c375aba5bfe2877721b2e3af75759fb062",
}
SECTIONS = {
    "readme.md": "3950d718c0961c792526639e77112577b4bfdd1c9e672bbd5928d4edf256f058",
    "design.md": "a2f795706a43a0095a28ad4b65d1b1c4396750d14d0f26f6fdde08cc060ac507",
    "development_log.md": "3deb7d2dad9971664dbed6a37187abc8245b5c3eb537d5e5f2080df29e404616",
    "roadmap.md": "df6bfdef02530da7389f3ba09b39cecc4b733528d1711834e599be8fefee0ccc",
    "proof_records.md": "44bc5b3d430e8b3f602ecee16760e154385249cc879b8a2d4dca1f54ac4a06d6",
}
DOCUMENTS = (
    "README.md", "docs/design.md", "docs/development_log.md",
    "docs/roadmap.md", "docs/proof_records.md",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="._phase171_r2r1_", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def inspect() -> tuple[str, dict[Path, bytes], dict[Path, bytes], bool]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    if git("rev-parse", "origin/develop") != head:
        raise RuntimeError("HEAD must match local origin/develop")
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes refused")
    if not (R2 / "run.ps1").is_file():
        raise RuntimeError("original R2 runner missing")
    before: dict[Path, bytes] = {}
    replacement: dict[Path, bytes] = {}
    states: list[str] = []
    for relative, source in REPLACEMENTS.items():
        path = R2 / relative
        asset = HERE / source
        existing = path.read_bytes()
        corrected = asset.read_bytes()
        current_hash = sha(existing)
        if current_hash == OLD_HASHES[relative]:
            states.append("OLD")
        elif current_hash == sha(corrected):
            states.append("CORRECTED")
        else:
            raise RuntimeError("unreviewed R2 source content: " + relative)
        before[path] = existing
        replacement[path] = corrected
    if len(set(states)) != 1:
        raise RuntimeError("mixed R2 correction states refused")
    for name, expected in SECTIONS.items():
        value = (R2 / "sections" / name).read_bytes()
        if sha(value) != expected:
            raise RuntimeError("unreviewed Phase 171 document section: " + name)
    for document in DOCUMENTS:
        if not (ROOT / document).is_file():
            raise RuntimeError("missing document: " + document)
    print("PHASE171_CLOSEOUT_R2R1_BRANCH=develop", flush=True)
    print("PHASE171_CLOSEOUT_R2R1_HEAD=" + head, flush=True)
    print("PHASE171_CLOSEOUT_R2R1_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_CLOSEOUT_R2R1_ALREADY_CORRECTED=" + str(states[0] == "CORRECTED"), flush=True)
    return head, before, replacement, states[0] == "CORRECTED"


def record_root() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    folder = base / ("phase171_closeout_r2r1_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head, before, replacement, already = inspect()
    if args.dry_run:
        print("PHASE171_CLOSEOUT_R2R1_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    destination = record_root()
    doc_before = {ROOT / doc: (ROOT / doc).read_bytes() for doc in DOCUMENTS}
    for path, content in before.items():
        relative = path.relative_to(ROOT)
        atomic_write(destination / "BEFORE" / relative, content)
    changed: list[Path] = []
    report: dict[str, object] = {
        "phase": "171_CLOSEOUT_R2R1",
        "head": head,
        "full_pytest": False,
        "already_corrected": already,
        "patch_paths": [str(path.relative_to(ROOT)) for path in before],
    }
    result_code = 1
    try:
        for path, content in replacement.items():
            if before[path] != content:
                atomic_write(path, content)
                changed.append(path)
        proc = subprocess.run(
            [sys.executable, "-B", str(R2 / "update_docs.py")],
            cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
        )
        print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n", flush=True)
        report["r2_exit_code"] = proc.returncode
        if proc.returncode:
            raise RuntimeError("corrected R2 full-document writer failed")
        if any(path.read_bytes() != content for path, content in replacement.items()):
            raise RuntimeError("corrected R2 source changed unexpectedly")
        report["result"] = "PASS_R2_DOCUMENTS_PENDING_PHASE_END_FULL_SUITE"
        print("PHASE171_CLOSEOUT_R2R1_RESULT=" + str(report["result"]), flush=True)
        result_code = 0
    except Exception as exc:
        for path in reversed(changed):
            atomic_write(path, before[path])
        for path, original in doc_before.items():
            if path.read_bytes() != original:
                atomic_write(path, original)
        report["result"] = "FAIL_RESTORED"
        report["error"] = str(exc)
        print("PHASE171_CLOSEOUT_R2R1_RESULT=FAIL_RESTORED", flush=True)
    finally:
        report["tracked_after"] = git("diff", "--name-only", "HEAD", "--").splitlines()
        output = destination / "audit.json"
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE171_CLOSEOUT_R2R1_REPORT=" + str(output), flush=True)
    return result_code


if __name__ == "__main__":
    raise SystemExit(main())
