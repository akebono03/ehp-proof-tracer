"""Guarded, idempotent installer for pi_7^4 narrative sentence layout."""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import os
from pathlib import Path
import shutil
import subprocess

PACKAGE = Path("phase173_r4_r1_prose_layout_fix")
TARGETS = {
    'phase173_r4_r1_alpha_literal_fix/tests/test_install.py': (
        'c3b73840e88c403271305061a251440287316a5fadee053e643dbd6ae3fe3e9d',
        '68d0041f2108bd28caf69e04285a6ac34e98184347e6a5983fe2bd03fb02d98c',
        ('c3c27d0f48106afbdc49f1c53411c3016cf23102', '6f10e7fea6d17564137908e93c5fe57638a545d3'),
    ),
    'phase173_r4_r1_narrative_source_fix/projection.py': (
        '1d99e8b135fb49868a185e5edac4b294478ca4c2c6794e36e61242cc544e15a3',
        'fedaa7f4522a86bcc577e11cd84aa83682264053d8570b97d486cec6f328e68f',
        ('4e2e921af6049e1557ac9d53949d4840f4ac0df2', 'ef81a01df157075bc2a21b91bc4ad5fcd56d2cd1'),
    ),
    'phase173_r4_r1_narrative_source_fix/verify.py': (
        '91e542172a766c80532f1f0f51267f5d7987c015618596620452924d35099b64',
        'e17b6224b537cbfd593c9629ca3eefc8bd4cdca5d2161d9e9f205f428bd774a4',
        ('89a5693844877db04d3efad79bcc354c51e908f1', '2672828bd7ac613a5077b8ba797b8a57154ad00d'),
    ),
    'phase173_r4_r1_narrative_source_fix/tests/test_live.py': (
        'a0794ec3587b897465639244f8f3772f9475405f1c9c4f7f8f38380b03a09bfe',
        '7feaa4846a6dca5d67e09fcbe0b31b724cd5f33319b78682c3a33562dd94eab5',
        ('0fe23aeba792101f9a73095e348a5dd13b9b3b0d', '32ff56cd5cd169083a50a5bb6433aab62af2c3ce'),
    ),
}
EXPECTED_DEPENDENCIES = {
    "phase165_r52_r3_web_adapter.py": "cfe2c244567535ffaf1e1c2e3ac27dc539ed3c21",
    "phase165_r52_r9_shared_math.py": "3e4c5f9c62b04d618f845b0f82d1cb1cacccdf2e",
    "phase173_r4_r1_source_bound_56/rule.py": "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def blob_hash(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ("git", *arguments), cwd=root, capture_output=True,
        check=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def state_for(path: str, data: bytes) -> str:
    if path not in TARGETS:
        raise ValueError("Unexpected patch target")
    original, revised, _ = TARGETS[path]
    digest = sha256(normalize(data)).hexdigest()
    if digest == original:
        return "NEW"
    if digest == revised:
        return "ALREADY_INSTALLED"
    raise RuntimeError("Unreviewed source content: " + path)


def preflight(root: Path) -> dict[str, tuple[str, bytes]]:
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    if git(root, "rev-parse", "HEAD") != git(root, "rev-parse", "origin/develop"):
        raise RuntimeError("HEAD is not at origin/develop")
    for path, expected in EXPECTED_DEPENDENCIES.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Reviewed dependency blob changed: " + path)
        if normalize((root / path).read_bytes()) != normalize(
                subprocess.run(("git", "show", "HEAD:" + path), cwd=root,
                               capture_output=True, check=True).stdout):
            raise RuntimeError("Reviewed dependency worktree changed: " + path)
    outputs: dict[str, tuple[str, bytes]] = {}
    for path, (original_hash, revised_hash, committed_blobs) in TARGETS.items():
        try:
            recorded = git(root, "rev-parse", "HEAD:" + path)
        except subprocess.CalledProcessError:
            if (path != "phase173_r4_r1_alpha_literal_fix/tests/test_install.py"
                    or git(root, "ls-files", "--", path)):
                raise RuntimeError("Unexpected missing reviewed target: " + path)
            recorded = None
        if recorded is not None and recorded not in committed_blobs:
            raise RuntimeError("Reviewed Git blob changed: " + path)
        if git(root, "diff", "--cached", "--name-only", "--", path):
            raise RuntimeError("Staged patch target: " + path)
        data = (root / path).read_bytes()
        state = state_for(path, data)
        reviewed_file = root / PACKAGE / "full_replacements" / path
        if sha256(normalize(reviewed_file.read_bytes())).hexdigest() != revised_hash:
            raise RuntimeError("Bundled full replacement has changed: " + path)
        outputs[path] = (state, data)
    return outputs


def install(root: Path) -> dict[str, str]:
    states = preflight(root)
    recovery = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_prose_layout_fix"
    )
    pending = {}
    for path, (state, data) in states.items():
        if state == "NEW":
            proposed = normalize(
                (root / PACKAGE / "full_replacements" / path).read_bytes()
            )
            output = proposed.replace(b"\n", b"\r\n") if b"\r\n" in data else proposed
            backup = recovery / (path.replace("/", "__") + "_" + sha256(data).hexdigest() + ".bak")
            if backup.exists() and backup.read_bytes() != data:
                raise RuntimeError("Unexpected recovery backup: " + str(backup))
            pending[path] = (data, output, backup)
    for path, (data, output, backup) in pending.items():
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            backup.write_bytes(data)
        (root / path).write_bytes(output)
    return {path: ("INSTALLED" if state == "NEW" else state)
            for path, (state, data) in states.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    states = preflight(root)
    for path, (state, _) in states.items():
        print("PHASE173_R4_R1_PROSE_GUARD=" + path + ":" + state)
    if args.dry_run:
        print("PHASE173_R4_R1_PROSE_DRY_RUN=PASS")
        return 0
    installed = install(root)
    for path, state in installed.items():
        print("PHASE173_R4_R1_PROSE_INSTALL=" + path + ":" + state)
    print("PHASE173_R4_R1_PROSE_INSTALLATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
