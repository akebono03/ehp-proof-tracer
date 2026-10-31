"""Phase 172 R2R1: correct typed generator identity and replay R2 focused tests.

Only the two untracked Phase 172 R2 files are replaced. The original R2
installer alone applies the already reviewed one-function Renderer modification.
Every candidate source is content-guarded; all corrections are backed up.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
R2_PACKAGE = "phase172_r2_suspension_relation_display"
RENDERER = Path("phase168_r3_5_model_renderer.py")
REVIEWED_RENDERER_BLOB = "94996b403f1c01f81319824565db422463714f02"
FILES = {
    Path(R2_PACKAGE) / "projection.py": (
        "7795a363f315d3161d7bf4575cdadd9229cd90b8c765817ab16481f94ea01657",
        "a7d7072d2adfcdbc17e27200241b5240b0ab17148c60811388e2543df9c09818",
        PACKAGE / "payload/projection.py",
    ),
    Path(R2_PACKAGE) / "tests/test_projection.py": (
        "e9cca325dbc3e2f8eda67bf165f2c26ca83defeb3b32a59e581ae3a2804fa42d",
        "c021fae71c00e64589685e12061dbb6022ca22189c9ae7599f0a19a7a0ed4036",
        PACKAGE / "payload/test_projection.py",
    ),
}


def command(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if check and result.returncode:
        raise RuntimeError("command failed: " + repr(args) + "\n" + result.stderr[-1200:])
    return result


def git(*args: str) -> str:
    return command(["git", *args]).stdout.strip()


def normalized(source: bytes) -> bytes:
    text = source.decode("utf-8-sig")
    if "\r" in text.replace("\r\n", ""):
        raise RuntimeError("mixed or unreviewed newline convention")
    return text.replace("\r\n", "\n").encode("utf-8")


def digest(source: bytes) -> str:
    return hashlib.sha256(normalized(source)).hexdigest()


def output_directory() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    path = base / "EHPProofTracerRecovery" / ("phase172_r2r1_" + stamp)
    path.mkdir(parents=True, exist_ok=False)
    return path


def preflight() -> tuple[dict[str, object], str]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Phase 172 R2R1 requires develop")
    head = git("rev-parse", "HEAD")
    blob = git("rev-parse", "HEAD:" + RENDERER.as_posix())
    if blob != REVIEWED_RENDERER_BLOB:
        raise RuntimeError("Renderer HEAD content differs from reviewed baseline")
    from phase172_r2_suspension_relation_display.install import transformed
    committed = subprocess.run(
        ["git", "show", "HEAD:" + RENDERER.as_posix()],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    current = (ROOT / RENDERER).read_bytes()
    if normalized(current) == normalized(committed):
        renderer_state = "RESTORED_BASELINE"
    elif normalized(current) == normalized(transformed(committed)):
        renderer_state = "R2_ALREADY_INSTALLED"
    else:
        raise RuntimeError("Renderer has unrelated changes; no modification made")
    # Do not require the whole worktree to be clean; inspect only the target.
    tracked = command(["git", "status", "--porcelain", "--", RENDERER.as_posix()]).stdout
    if renderer_state == "RESTORED_BASELINE" and tracked.strip():
        raise RuntimeError("Renderer tracked status differs from baseline")
    rows: dict[str, object] = {}
    for relative, (old_hash, new_hash, payload) in FILES.items():
        path = ROOT / relative
        if not path.is_file() or not payload.is_file():
            raise RuntimeError("required R2 file/payload absent: " + str(relative))
        if digest(payload.read_bytes()) != new_hash:
            raise RuntimeError("correction payload hash mismatch: " + str(relative))
        current_hash = digest(path.read_bytes())
        if current_hash not in (old_hash, new_hash):
            raise RuntimeError("R2 file modified outside reviewed variants: " + str(relative))
        rows[str(relative)] = "ORIGINAL" if current_hash == old_hash else "CORRECTED"
    for extra in ("install.py", "run.ps1"):
        if not (ROOT / R2_PACKAGE / extra).is_file():
            raise RuntimeError("original R2 installer absent: " + extra)
    return {
        "branch": "develop", "head": head, "reviewed_renderer_blob": blob,
        "renderer_state": renderer_state, "files": rows,
    }, renderer_state


def run_r2_focused(output: Path, renderer_state: str) -> None:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    if renderer_state == "RESTORED_BASELINE":
        args = [sys.executable, "-B", "-m", R2_PACKAGE + ".install", "--run-focused-tests"]
    else:
        args = [sys.executable, "-B", "-c", (
            "from pathlib import Path; "
            "from phase172_r2_suspension_relation_display.install import run_focused; "
            "run_focused(Path(" + repr(str(output)) + "))"
        )]
    result = subprocess.run(
        args, cwd=ROOT, env=env, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    log = result.stdout + "\n" + result.stderr
    (output / "r2_focused_runner.log").write_text(log, encoding="utf-8")
    print(log[-8000:], flush=True)
    if result.returncode:
        raise RuntimeError("corrected R2 focused test run failed; see log")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-focused-tests", action="store_true")
    args = parser.parse_args()
    state, renderer_state = preflight()
    print("PHASE172_R2R1_BRANCH=" + str(state["branch"]), flush=True)
    print("PHASE172_R2R1_HEAD=" + str(state["head"]), flush=True)
    print("PHASE172_R2R1_REVIEWED_RENDERER=PASS", flush=True)
    print("PHASE172_R2R1_RENDERER_STATE=" + renderer_state, flush=True)
    print("PHASE172_R2R1_PAYLOAD_GUARD=PASS", flush=True)
    if args.dry_run:
        print("PHASE172_R2R1_DRY_RUN=PASS", flush=True)
        print("PHASE172_R2R1_SOURCE_CHANGES=0", flush=True)
        return 0
    output = output_directory()
    original = {rel: (ROOT / rel).read_bytes() for rel in FILES}
    report: dict[str, object] = {
        "phase": "172-R2R1", "mode": "TYPED_IDENTITY_CORRECTION",
        "preflight": state, "full_pytest_executed": False,
        "math_inference_changed": False, "proof_tree_changed": False,
    }
    try:
        for relative, (_, _, payload) in FILES.items():
            destination = ROOT / relative
            (output / (destination.name + "." + destination.parent.name + ".before")).write_bytes(original[relative])
            destination.write_bytes(payload.read_bytes())
        print("PHASE172_R2R1_TWO_FILES_CORRECTED=PASS", flush=True)
        if args.run_focused_tests:
            run_r2_focused(output, renderer_state)
        report["result"] = "PASS_R2R1_CORRECTION"
    except BaseException:
        for relative, content in original.items():
            (ROOT / relative).write_bytes(content)
        report["result"] = "FAILED_CORRECTION_FILES_RESTORED"
        (output / "result.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
        )
        print("PHASE172_R2R1_CORRECTION_RESTORED=PASS", flush=True)
        raise
    (output / "result.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    print("PHASE172_R2R1_REPORT=" + str(output), flush=True)
    print("PHASE172_R2R1_RESULT=PASS_R2R1_CORRECTION", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
