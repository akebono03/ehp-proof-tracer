"""Safely repair the PowerShell splat variable, without changing R2 math or docs."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "phase171_closeout_r2r1_committed_head_guard" / "run.ps1"
REPLACEMENT = HERE / "replacements" / "run.ps1"
INSTALLER = ROOT / "phase171_closeout_r2r1_committed_head_guard" / "install.py"
R2_RUNNER = ROOT / "phase171_closeout_r2_documentation_full_output" / "run.ps1"
R2_WRITER = ROOT / "phase171_closeout_r2_documentation_full_output" / "update_docs.py"
OLD_SHA = "d55e4c6e88ec56de2fcdaeafef3a1c87a5c282735e31734bb26b3f866da27bc9"
CORRECTED_SHA = "b640331897babaa5e73db70738a604aca0467511e99865b2b91e6cdf01ca3a9d"
INSTALLER_SHA = "6dcac944bfef7bd76b69a8a0a7ea4730edb5614cfecadd49dc8ab566d26e136d"
R2_RUNNER_SHA = "0fd5136297f2cb8c84173cd5d7b0dcdd26f74bf487cfe047c538ec2ced457bd1"
R2_WRITER_ALLOWED = frozenset({
    "19a65bc5b3e4c2ea38ec8216cc320bade803e5daa247e58f3075a4e79a59f247",
    "b8e11ea6f762ca7fc6699cc45a7878f448ab966fc1eee316ad1e63f7f8e65dae",
})


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def preflight() -> tuple[bytes, bytes, bool]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("HEAD must match origin/develop")
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes refused")
    existing = TARGET.read_bytes()
    revised = REPLACEMENT.read_bytes()
    if sha(revised) != CORRECTED_SHA:
        raise RuntimeError("replacement PowerShell code differs from reviewed source")
    if sha(existing) not in {OLD_SHA, CORRECTED_SHA}:
        raise RuntimeError("unreviewed existing PowerShell runner")
    if sha(INSTALLER.read_bytes()) != INSTALLER_SHA:
        raise RuntimeError("R2R1 installer differs from reviewed source")
    if sha(R2_RUNNER.read_bytes()) != R2_RUNNER_SHA:
        raise RuntimeError("R2 runner differs from reviewed source")
    if sha(R2_WRITER.read_bytes()) not in R2_WRITER_ALLOWED:
        raise RuntimeError("R2 document writer differs from reviewed source")
    if revised.replace(b"& python @PythonArguments", b"& python @Args") != existing and existing != revised:
        raise RuntimeError("replacement contains unrelated changes")
    print("PHASE171_CLOSEOUT_R2R2_BRANCH=develop", flush=True)
    print("PHASE171_CLOSEOUT_R2R2_HEAD=" + head, flush=True)
    print("PHASE171_CLOSEOUT_R2R2_RUNNER_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_CLOSEOUT_R2R2_ALREADY_CORRECTED=" + str(existing == revised), flush=True)
    return existing, revised, existing == revised


def atomic_write(path: Path, value: bytes) -> None:
    fd, tmp = tempfile.mkstemp(prefix=".phase171_r2r2_", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(value)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    original, revised, already = preflight()
    if opts.dry_run:
        print("PHASE171_CLOSEOUT_R2R2_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    report_dir = base / ("phase171_closeout_r2r2_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    report_dir.mkdir(parents=True, exist_ok=False)
    (report_dir / "run_before.ps1").write_bytes(original)
    if not already:
        atomic_write(TARGET, revised)
    if sha(TARGET.read_bytes()) != CORRECTED_SHA:
        raise RuntimeError("corrected PowerShell runner verification failed")
    report = {
        "phase": "171_CLOSEOUT_R2R2",
        "result": "PASS_RUNNER_CORRECTED",
        "already_corrected": already,
        "runner": str(TARGET),
        "before_sha256": sha(original),
        "after_sha256": sha(revised),
        "full_pytest": False,
        "documents_updated_by_this_step": False,
    }
    (report_dir / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_CLOSEOUT_R2R2_RESULT=PASS_RUNNER_CORRECTED", flush=True)
    print("PHASE171_CLOSEOUT_R2R2_REPORT=" + str(report_dir / "audit.json"), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
