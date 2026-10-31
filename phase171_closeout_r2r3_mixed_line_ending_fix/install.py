"""Phase 171 R2R3: guarded historical-byte-preserving document writer fix."""
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
REVIEWED_OLD_SHA256 = {
    "update_docs.py": "b8e11ea6f762ca7fc6699cc45a7878f448ab966fc1eee316ad1e63f7f8e65dae",
    "tests/test_document_writer.py": "5ce255360fcdafd1498bbec6f4fefb8fa862e2c5f792b686f266aa98aadadf65",
}
REVIEWED_R2_BASE_SHA256 = {
    # R2R1 and R2R3 restore these exact originals after a failed write.
    "update_docs.py": "19a65bc5b3e4c2ea38ec8216cc320bade803e5daa247e58f3075a4e79a59f247",
    "tests/test_document_writer.py": "ce7a2065ea346c879e29fe1258f919c375aba5bfe2877721b2e3af75759fb062",
}
EXPECTED_NEW_SHA256 = {
    "update_docs.py": "8b39e61e57d171b2bf451137fd28730fca283364f726740a0cb543b808fd05d1",
    "tests/test_document_writer.py": "d0da01d85904e496ac9297275b2108cbd00be1fb0bdf887ae5badb00114a0b1e",
}
BASE = "3e74849bf90bc115c16503ddd46d49996baa0856"
DOCUMENT_BLOBS = {
    "README.md": "cc65eea3ae9e4bf1e7d67d74550eda4f4f8b4024",
    "docs/design.md": "6f4a65431cf0e4ba2c517b521654e732568f45db",
    "docs/development_log.md": "64484312f89636c00e6d7dac670d719e81016eca",
    "docs/roadmap.md": "f6b48da7a853200c8b9323baff77731002d43026",
    "docs/proof_records.md": "0f4289bccca3558632f621596e04199e44360576",
}
SECTIONS = {
    "readme.md": "3950d718c0961c792526639e77112577b4bfdd1c9e672bbd5928d4edf256f058",
    "design.md": "a2f795706a43a0095a28ad4b65d1b1c4396750d14d0f26f6fdde08cc060ac507",
    "development_log.md": "3deb7d2dad9971664dbed6a37187abc8245b5c3eb537d5e5f2080df29e404616",
    "roadmap.md": "df6bfdef02530da7389f3ba09b39cecc4b733528d1711834e599be8fefee0ccc",
    "proof_records.md": "44bc5b3d430e8b3f602ecee16760e154385249cc879b8a2d4dca1f54ac4a06d6",
}
TEST_BLOB = "f98557eef6f2dd720c4b74ff28b8469e668df2f4"
R1R1_TEST = "phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py"


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".phase171_r2r3_", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def preflight() -> tuple[dict[Path, bytes], dict[Path, bytes], bool]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    if git("rev-parse", "origin/develop") != head:
        raise RuntimeError("local HEAD and origin/develop differ")
    try:
        git("merge-base", "--is-ancestor", BASE, "HEAD")
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("local HEAD not descended from reviewed base") from exc
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes refused")
    if head != BASE:
        delta = set(filter(None, git("diff", "--name-only", BASE, "HEAD", "--").splitlines()))
        if any(not (p.startswith("phase171_closeout_r2_documentation_full_output/")
                    or p.startswith("phase171_closeout_r2r")) for p in delta):
            raise RuntimeError("unreviewed committed changes after base")
    if git("rev-parse", "HEAD:" + R1R1_TEST) != TEST_BLOB:
        raise RuntimeError("semantic R1R1 test blob changed")
    for relative, blob in DOCUMENT_BLOBS.items():
        if git("rev-parse", "HEAD:" + relative) != blob:
            raise RuntimeError("reviewed document blob changed: " + relative)
    for name, expected in SECTIONS.items():
        if sha((R2 / "sections" / name).read_bytes()) != expected:
            raise RuntimeError("reviewed document section changed: " + name)
    if not (R2 / "run.ps1").is_file():
        raise RuntimeError("original R2 runner missing")
    if not (ROOT / "phase171_closeout_r2r1_committed_head_guard" / "run.ps1").is_file():
        raise RuntimeError("R2R1 runner missing")
    before = {}
    corrected = {}
    states = []
    for relative, asset in REPLACEMENTS.items():
        path = R2 / relative
        original = path.read_bytes()
        patch = (HERE / asset).read_bytes()
        if sha(patch) != EXPECTED_NEW_SHA256[relative]:
            raise RuntimeError("replacement source checksum mismatch: " + relative)
        actual = sha(original)
        if actual == REVIEWED_R2_BASE_SHA256[relative]:
            states.append("R2_BASE")
        elif actual == REVIEWED_OLD_SHA256[relative]:
            states.append("R2R1")
        elif actual == EXPECTED_NEW_SHA256[relative]:
            states.append("NEW")
        else:
            raise RuntimeError("unreviewed R2 source: " + relative)
        before[path] = original
        corrected[path] = patch
    if len(set(states)) != 1:
        raise RuntimeError("mixed state of R2 source and tests")
    unexpected = set(filter(None, git("diff", "--name-only", "HEAD", "--").splitlines())) - set(DOCUMENT_BLOBS)
    if unexpected:
        raise RuntimeError("unexpected tracked changes: " + ", ".join(sorted(unexpected)))
    print("PHASE171_CLOSEOUT_R2R3_HEAD=" + head, flush=True)
    print("PHASE171_CLOSEOUT_R2R3_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_CLOSEOUT_R2R3_ALREADY_CORRECTED=" + str(states[0] == "NEW"), flush=True)
    return before, corrected, states[0] == "NEW"


def report_dir() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    output = base / ("phase171_closeout_r2r3_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    return output


def invoke(command: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
    )
    print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n", flush=True)
    if proc.stderr:
        print(proc.stderr, flush=True)
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    before, corrected, already = preflight()
    if args.dry_run:
        print("PHASE171_CLOSEOUT_R2R3_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    output = report_dir()
    doc_before = {ROOT / doc: (ROOT / doc).read_bytes() for doc in DOCUMENT_BLOBS}
    for path, data in {**before, **doc_before}.items():
        atomic_write(output / "BEFORE" / path.relative_to(ROOT), data)
    changed = []
    report = {"phase": "171_CLOSEOUT_R2R3", "head": git("rev-parse", "HEAD"),
              "full_pytest": False, "already_corrected": already}
    try:
        for path, data in corrected.items():
            if path.read_bytes() != data:
                atomic_write(path, data)
                changed.append(path)
        code, result = invoke([
            sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
            "--disable-warnings", "-p", "no:cacheprovider",
            str(HERE / "tests" / "test_install.py"),
            "phase171_closeout_r2_documentation_full_output/tests/test_document_writer.py",
        ])
        report["repair_pytest_exit"] = code
        if code:
            raise RuntimeError("R2R3 safety and regression pytest failed")
        code, result = invoke([sys.executable, "-B", str(R2 / "update_docs.py"), "--dry-run"])
        report["r2_dry_run_exit"] = code
        if code:
            raise RuntimeError("R2 document preflight failed")
        code, result = invoke([sys.executable, "-B", str(R2 / "update_docs.py")])
        report["r2_exit"] = code
        if code:
            raise RuntimeError("R2 full-document write or focused pytest failed")
        if any(path.read_bytes() != value for path, value in corrected.items()):
            raise RuntimeError("source changed during R2 focused tests")
        report["result"] = "PASS_FIVE_DOCUMENTS_PENDING_PHASE_END"
        print("PHASE171_CLOSEOUT_R2R3_RESULT=PASS_FIVE_DOCUMENTS_PENDING_PHASE_END", flush=True)
        return 0
    except Exception as exc:
        for path in reversed(changed):
            atomic_write(path, before[path])
        for path, data in doc_before.items():
            if path.read_bytes() != data:
                atomic_write(path, data)
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["result"] = "FAIL_RESTORED"
        print("PHASE171_CLOSEOUT_R2R3_RESULT=FAIL_RESTORED", flush=True)
        return 1
    finally:
        report["tracked_after"] = git("diff", "--name-only", "HEAD", "--").splitlines()
        (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE171_CLOSEOUT_R2R3_REPORT=" + str(output / "audit.json"), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
