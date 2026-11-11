"""R70R1: replace only the reviewed existing complete composite-display function.

The source guard accepts full-file LF or CRLF, not mixed or CR-only data.
No mathematical rule, existing text formatter or reference mapping is changed.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
from pathlib import Path
import subprocess


PACKAGE = "phase174_r3_r7_r70r1_assoc_chain_display_fix"
TARGET = "phase174_r3_r7_r70_verified_narrative_projection/projection.py"
OLD_SOURCE_BLOB = "e77875a3d03bcb189c4053aa178f3c59375fbfce"
REVIEWED_DEPENDENCIES = {
    "phase174_r3_r7_r9_composition_associativity/rule.py": "2c44c68be90cb761d7bdd35e29f23977b5f93a2e",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py": "6aa48096b41714fbdf588c3ba423d264a4a13bb9",
}


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def normalize(data: bytes) -> tuple[str, bytes, str]:
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    body = data[len(bom):]
    if b"\r" in body.replace(b"\r\n", b""):
        raise RuntimeError("R70R1_UNEXPECTED_CR_ONLY")
    if b"\r\n" in body and b"\n" in body.replace(b"\r\n", b""):
        raise RuntimeError("R70R1_MIXED_LINE_ENDINGS")
    eol = "\r\n" if b"\r\n" in body else "\n"
    return body.decode("utf-8").replace("\r\n", "\n"), bom, eol


def acceptable_blob(data: bytes, expected_sha: str) -> bool:
    text, bom, _ = normalize(data)
    lf = bom + text.encode("utf-8")
    crlf = bom + text.replace("\n", "\r\n").encode("utf-8")
    return expected_sha in {
        git_blob_sha(data), git_blob_sha(lf), git_blob_sha(crlf)
    }


def function_text(source: str, name: str) -> str:
    tree = ast.parse(source)
    named = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(named) != 1:
        raise RuntimeError("R70R1_TARGET_FUNCTION_MISSING_OR_AMBIGUOUS")
    fragment = ast.get_source_segment(source, named[0])
    if fragment is None:
        raise RuntimeError("R70R1_NO_FUNCTION_SEGMENT")
    return fragment.rstrip("\n") + "\n"


def replacement(root: Path, original: bytes) -> tuple[str, bytes]:
    text, bom, eol = normalize(original)
    revised = (root / PACKAGE / "output/_project_composite_images_FULL_AFTER.py").read_text(encoding="utf-8")
    old_function = function_text(text, "_project_composite_images")
    if not revised.startswith("def _project_composite_images("):
        raise RuntimeError("R70R1_INVALID_REVIEWED_REPLACEMENT")
    ast.parse(revised)
    if old_function == revised:
        # Recover the prior fully reviewed function from the package's exact R70 source.
        prior = (root / PACKAGE / "output/_project_composite_images_FULL_BEFORE.py").read_text(encoding="utf-8")
        restored = text.replace(old_function, prior, 1)
        baseline = bom + restored.replace("\n", eol).encode("utf-8")
        if not acceptable_blob(baseline, OLD_SOURCE_BLOB):
            raise RuntimeError("R70R1_PATCHED_SOURCE_NOT_REVIEWED")
        return "ALREADY_APPLIED", original
    if not acceptable_blob(original, OLD_SOURCE_BLOB):
        raise RuntimeError("R70R1_SOURCE_GUARD_FAILED")
    changed = text.replace(old_function, revised, 1)
    if changed == text or changed.count(revised) != 1:
        raise RuntimeError("R70R1_PATCH_IS_NOT_SINGLE_FUNCTION")
    ast.parse(changed)
    return "PATCH_REQUIRED", bom + changed.replace("\n", eol).encode("utf-8")


def source_guard(root: Path) -> tuple[str, ...]:
    checked = []
    for name, expected in REVIEWED_DEPENDENCIES.items():
        if not acceptable_blob((root / name).read_bytes(), expected):
            raise RuntimeError("R70R1_DEPENDENCY_MISMATCH: " + name)
        checked.append(name)
    return tuple(checked)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=root,
                            capture_output=True, text=True, check=False)
    if branch.returncode or branch.stdout.strip() != "develop":
        raise RuntimeError("R70R1_DEVELOP_REQUIRED")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          capture_output=True, text=True, check=True).stdout.strip()
    pins = source_guard(root)
    # R70 must already have installed its one-function shared formatter.
    # Do not proceed on an unrelated or unpatched narrative path.
    from phase174_r3_r7_r70_verified_narrative_projection.install import (
        TARGET as FORMATTER_TARGET,
        replace_formatter,
    )
    formatter_state, _ = replace_formatter((root / FORMATTER_TARGET).read_bytes())
    if formatter_state != "ALREADY_APPLIED":
        raise RuntimeError("R70R1_PRECEDING_R70_FORMATTER_MISSING")
    target = root / TARGET
    status, patched = replacement(root, target.read_bytes())
    print("PHASE174_R70R1_SOURCE_GUARD=PASS")
    print("PHASE174_R70R1_SOURCE_PINS=" + str(len(pins) + 1))
    print("PHASE174_R70R1_LOCAL_HEAD=" + head)
    print("PHASE174_R70R1_PATCH_STATUS=" + status)
    print("PHASE174_R70R1_NEW_GIVEN=0")
    print("PHASE174_R70R1_NEW_MATHEMATICAL_RULES=0")
    if options.dry_run:
        print("PHASE174_R70R1_GATE=PASS_R70R1_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    if status == "PATCH_REQUIRED":
        target.write_bytes(patched)
    print("PHASE174_R70R1_GATE=PASS_R70R1_ASSOCIATIVITY_PATCH_APPLIED_OR_PRESENT")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
