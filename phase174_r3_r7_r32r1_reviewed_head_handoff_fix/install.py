"""R32R1 guarded repair: two full-file replacements, no production edit.

Old and repaired bytes are individually checked, with CRLF/LF normalization.
No checkout/reset/pull/fetch, and no R31 file is written.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
BASE_HEAD = "25118e281445ca17b30c60c8fd02d00acaa25ea5"
REVIEWED_R31_MERGE_HEAD = "02f694b27a4239052bfa9d27a116fca6bbbff6b5"
TARGETS = {
    "phase174_r3_r7_r32_lower_delta_kernel_audit/audit.py": (
        "bd2327bf8bf49d6a25cf099f915aa15afc2dc3815b1457d0eb03e95aef7ec5f7", "c191d8a9c25007e1d42b4a7faa6898b1d118a3b60f021f2dbb5ec713f0aa7656",
        PACKAGE / "replacement" / "audit.py",
    ),
    "phase174_r3_r7_r32_lower_delta_kernel_audit/run.ps1": (
        "d4fa72731ae50770c402b2ea0dfe0fd459c6152ce91de2a4f0507bdc9a8e87eb", "6e070729ce6c5ae809be0f564a87372df179ab49ce971f7a3af41efdd0044103",
        PACKAGE / "replacement" / "run.ps1",
    ),
}
R31_FILE = "phase174_r3_r7_r31_delta_surjectivity_general_audit/audit.py"
R31_SHA256 = "ab6f81dbbb32c6fd46dfb85c639534f7eff15062e2cc42c58b32f44efc0bc191"


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          check=True).stdout.strip()


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().removeprefix(b"\xef\xbb\xbf").replace(b"\r\n", b"\n")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R32R1 must be extracted directly under repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R32R1 requires develop")
    local = git("rev-parse", "HEAD")
    remote_line = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_line.split()[0] if remote_line else ""
    if remote != REVIEWED_R31_MERGE_HEAD or local not in (BASE_HEAD, REVIEWED_R31_MERGE_HEAD):
        raise RuntimeError("Unreviewed R31 GitHub/local transition; no changes made")
    if git("diff", "--cached", "--name-only") or git("diff", "--name-only"):
        raise RuntimeError("Tracked modifications require independent review")
    prior = ROOT / R31_FILE
    if not prior.is_file() or sha256(normalized_bytes(prior)) != R31_SHA256:
        raise RuntimeError("R31 audit source changed or unavailable; do not overwrite")
    states: dict[str, str] = {}
    for path, (before, after, replacement) in TARGETS.items():
        target = ROOT / path
        if not target.is_file() or not replacement.is_file():
            raise RuntimeError("Reviewed R32 target or replacement missing: " + path)
        if sha256(normalized_bytes(replacement)) != after:
            raise RuntimeError("R32R1 replacement contents mutated: " + path)
        current = sha256(normalized_bytes(target))
        if current not in (before, after):
            raise RuntimeError("Local R32 changes require review: " + path)
        states[path] = "PATCHED" if current == after else "BASELINE"
    return {"local_head": local, "remote_head": remote,
            "source_guard": "PASS", "target_states": states,
            "r31_preserved": True}


def install() -> dict[str, object]:
    state = preflight()
    for rel, (_before, after, replacement) in TARGETS.items():
        if state["target_states"][rel] == "PATCHED":
            continue
        target = ROOT / rel
        raw = target.read_bytes()
        eol = b"\r\n" if b"\r\n" in raw else b"\n"
        output = normalized_bytes(replacement).replace(b"\n", eol)
        if sha256(output.replace(b"\r\n", b"\n")) != after:
            raise RuntimeError("R32R1 output hash verification failed before write")
        target.write_bytes(output)
    result = preflight()
    if any(x != "PATCHED" for x in result["target_states"].values()):
        raise RuntimeError("R32R1 installation incomplete")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = preflight() if args.dry_run else install()
    prefix = "PHASE174_R3R7R32R1_"
    print(prefix + "LOCAL_HEAD=" + state["local_head"])
    print(prefix + "REMOTE_HEAD=" + state["remote_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "R31_PRESERVED=True")
    for path, status in state["target_states"].items():
        print(prefix + ("AUDIT_STATUS=" if path.endswith("audit.py") else "RUNNER_STATUS=") + status)
    print(prefix + "MODE=" + ("DRYRUN" if args.dry_run else "INSTALLED"))
    print(prefix + "GATE=" + ("PASS_R32R1_GUARDED_PREFLIGHT" if args.dry_run
                              else "PASS_R32R1_REVIEWED_HANDOFF_REPAIRED"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
