"""Fail-closed, EOL-preserving replacement of one existing complete function."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path

TARGET = Path("phase175_r3r11_cited_hopf_narrative/projection.py")
REVIEWED_GIT_BLOB = "258d22589f92fbebdb9c4516dbe72c1f94a98afd"
PACKAGE = Path(__file__).resolve().parent
REVIEWED = (PACKAGE / "full_functions" / "REVIEWED_PROJECTION.py").read_bytes()
BASE = (PACKAGE / "full_functions" /
        "project_verified_source_and_hopf_summary_BASE.py").read_bytes()
FULL = (PACKAGE / "full_functions" /
        "project_verified_source_and_hopf_summary_FULL.py").read_bytes()


@dataclass(frozen=True)
class PatchPlan:
    status: str
    old_bytes: bytes
    new_bytes: bytes


def _canonical(data: bytes) -> tuple[bytes, bytes]:
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R12_UNEXPECTED_BOM")
    if b"\r\r\n" in data:
        raise RuntimeError("R3R12_DOUBLE_CRLF")
    remainder = data.replace(b"\r\n", b"")
    if b"\r" in remainder:
        raise RuntimeError("R3R12_UNEXPECTED_CR")
    if b"\r\n" in data and b"\n" in remainder:
        raise RuntimeError("R3R12_MIXED_EOL")
    eol = b"\r\n" if b"\r\n" in data else b"\n"
    return data.replace(b"\r\n", b"\n"), eol


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def plan_patch(root: Path) -> PatchPlan:
    target = Path(root) / TARGET
    if not target.is_file():
        raise RuntimeError("R3R12_TARGET_MISSING")
    original = target.read_bytes()
    normalized, eol = _canonical(original)
    if (git_blob_sha(REVIEWED) != REVIEWED_GIT_BLOB
            or not REVIEWED.endswith(BASE)
            or not BASE.endswith(b"\n") or not FULL.endswith(b"\n")
            or BASE == FULL):
        raise RuntimeError("R3R12_PACKAGE_REVIEW_PIN_FAILED")
    replacement = REVIEWED[:-len(BASE)] + FULL
    if normalized == replacement:
        return PatchPlan("ALREADY_APPLIED", original, original)
    if normalized != REVIEWED:
        raise RuntimeError("R3R12_UNREVIEWED_TARGET_REFUSED")
    patched = replacement.replace(b"\n", eol)
    if eol == b"\r\n" and patched.count(b"\n") != patched.count(b"\r\n"):
        raise RuntimeError("R3R12_EOL_PRESERVATION_FAILED")
    return PatchPlan("PATCH_REQUIRED", original, patched)


def apply_patch(root: Path, plan: PatchPlan) -> None:
    target = Path(root) / TARGET
    if plan.status not in ("PATCH_REQUIRED", "ALREADY_APPLIED"):
        raise RuntimeError("R3R12_BAD_PATCH_STATUS")
    if target.read_bytes() != plan.old_bytes:
        raise RuntimeError("R3R12_TARGET_CHANGED_SINCE_PREFLIGHT")
    if plan.status == "PATCH_REQUIRED":
        target.write_bytes(plan.new_bytes)
