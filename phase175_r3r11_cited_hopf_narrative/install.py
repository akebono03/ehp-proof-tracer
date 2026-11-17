"""Replace one pinned, complete renderer function with EOL-aware rollback support."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

TARGET = Path("phase171_r20r13_eta_sentence_layout/projection.py")
REVIEWED_HEAD_BLOB = "5deaa8886f36ec967d52b9fcd603d135ae290b39"
PACKAGE = Path(__file__).resolve().parent
BASE = (PACKAGE / "full_functions" /
        "format_complete_proof_sentences_BASE.py").read_text(encoding="utf-8")
FULL = (PACKAGE / "full_functions" /
        "format_complete_proof_sentences_FULL.py").read_text(encoding="utf-8")


@dataclass(frozen=True)
class PatchPlan:
    status: str
    old_bytes: bytes
    new_bytes: bytes


def _canonical(data: bytes) -> tuple[bytes, bytes]:
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R11_UNEXPECTED_BOM")
    if b"\r\r\n" in data:
        raise RuntimeError("R3R11_DOUBLE_CRLF")
    rest = data.replace(b"\r\n", b"")
    if b"\r" in rest:
        raise RuntimeError("R3R11_UNEXPECTED_CR")
    if b"\r\n" in data and b"\n" in rest:
        raise RuntimeError("R3R11_MIXED_EOL")
    eol = b"\r\n" if b"\r\n" in data else b"\n"
    normalized = data.replace(b"\r\n", b"\n")
    return normalized, eol


def plan_patch(root: Path) -> PatchPlan:
    target = Path(root) / TARGET
    if not target.is_file():
        raise RuntimeError("R3R11_RENDERER_NOT_FOUND")
    original = target.read_bytes()
    normalized, eol = _canonical(original)
    before = BASE.encode("utf-8")
    after = FULL.encode("utf-8")
    if (normalized.count(b"def format_complete_proof_sentences(") != 1
            or not normalized.endswith(b"\n")
            or BASE == FULL):
        raise RuntimeError("R3R11_FUNCTION_BOUNDARY_NOT_UNIQUE")
    if normalized.endswith(after) and normalized.count(after) == 1:
        return PatchPlan("ALREADY_APPLIED", original, original)
    if not normalized.endswith(before) or normalized.count(before) != 1:
        raise RuntimeError("R3R11_REVIEWED_FORMATTER_MISMATCH")
    patched = normalized[:-len(before)] + after
    result = patched.replace(b"\n", eol)
    if eol == b"\r\n" and result.count(b"\n") != result.count(b"\r\n"):
        raise RuntimeError("R3R11_EOL_PRESERVATION_FAILED")
    return PatchPlan("PATCH_REQUIRED", original, result)


def apply_patch(root: Path, plan: PatchPlan) -> None:
    target = Path(root) / TARGET
    if plan.status not in ("PATCH_REQUIRED", "ALREADY_APPLIED"):
        raise RuntimeError("R3R11_UNKNOWN_PATCH_STATUS")
    if target.read_bytes() != plan.old_bytes:
        raise RuntimeError("R3R11_TARGET_CHANGED_SINCE_PREFLIGHT")
    if plan.status == "PATCH_REQUIRED":
        target.write_bytes(plan.new_bytes)
