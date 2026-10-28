"""R10ET-R6D: precise certification change for R6 after reviewed R6C.

This module changes exactly one audit function; no proof or production edits.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

TARGET = "phase169_r10et_r6_residual_definition_dependency_audit/audit.py"
ORIGINAL_SHA256 = "07f9c289e5646eb5013ffd356c87bd21702fa64b0fa5b9591cfc3eb5ccee97ba"
R6C_PATCH = "phase169_r10et_r6c_root_reachable_citations/patch.py"
R6C_PATCH_SHA256 = "dc2c79ad779119f553ebbfeb39a424d8ea816d971e638d09f2df143d4daefdd0"
EXPECTED_HEAD = "232a92883b0cb009762b437cbb3cc550f00ab6bd"

FUNCTION = '''def certify_reviewed_production(root: Path) -> dict[str, str]:
    """Certify exact R5D and R6C production against reviewed Git R4 bytes.

    R6C is a source-verified root-reachability change. Verify its *exact*
    transformation of the reviewed R4 Model and Renderer; do not loosen
    acceptance to arbitrary modified renderers or arbitrary citations.
    """
    from hashlib import sha256
    from phase169_r10et_r5d_staged_audit_guard.patch import (
        EXPECTED_BLOBS, git_blob, transform,
    )
    from phase169_r10et_r6c_root_reachable_citations.patch import (
        EXPECTED_GIT_BLOBS, MODEL, RENDERER, transform as transform_r6c,
    )

    branch = git_text(root, "branch", "--show-current")
    head = git_text(root, "rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError(f"R6 refuses branch {branch!r}; develop required")
    ancestor = subprocess.run(
        ("git", "-C", str(root), "merge-base", "--is-ancestor", R4_COMMITTED, head),
        capture_output=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("R6 refuses HEAD outside the reviewed R4 ancestry")

    r6c_path = root / "phase169_r10et_r6c_root_reachable_citations/patch.py"
    r6c_expected_sha256 = "dc2c79ad779119f553ebbfeb39a424d8ea816d971e638d09f2df143d4daefdd0"
    if sha256(r6c_path.read_bytes()).hexdigest() != r6c_expected_sha256:
        raise RuntimeError("R6 refuses changed or unknown R6C transform source")

    checked: dict[str, str] = {}
    for path, original_blob in EXPECTED_BLOBS.items():
        before = git_bytes(root, "show", f"{R4_COMMITTED}:{path}")
        if git_blob(before) != original_blob:
            raise RuntimeError(f"reviewed R4 source changed: {path}")
        after, _functions = transform(path, before)
        if (root / path).read_bytes() != after:
            raise RuntimeError(f"R6 requires exact completed R5 production: {path}")
        checked[path] = git_blob(after)

    r4_blobs = {
        "phase168_r3_3_proof_narrative_model.py":
            "1080843a2a90bf60f0b8096d3c5542a24a9abb7c",
        "phase168_r3_5_model_renderer.py":
            "6694fa68205628d5bd870a08f38b1d4df2d45681",
        "phase169_r10a_verified_stable_chain_projection/projection.py":
            "a166ffbbb64d3cc60bc964cb4c42f854d1207953",
    }
    if set(EXPECTED_GIT_BLOBS) != {MODEL, RENDERER}:
        raise RuntimeError("R6C certified Model/Renderer scope is unexpected")
    if (EXPECTED_GIT_BLOBS.get(MODEL) != r4_blobs[MODEL]
            or EXPECTED_GIT_BLOBS.get(RENDERER) != r4_blobs[RENDERER]):
        raise RuntimeError("R6C source baselines differ from reviewed R4")
    for path, expected_blob in r4_blobs.items():
        before = git_bytes(root, "show", f"{R4_COMMITTED}:{path}")
        if git_blob(before) != expected_blob:
            raise RuntimeError(f"reviewed R4 Projection/Model/Renderer differs: {path}")
        after = transform_r6c(path, before) if path in (MODEL, RENDERER) else before
        if (root / path).read_bytes() != after:
            raise RuntimeError(f"reviewed R6C Projection/Model/Renderer differs: {path}")
        checked[path] = git_blob(after)
    return checked
'''


def sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def transform_r6_audit(raw: bytes) -> bytes:
    """One exact complete-function replacement; refuses any altered input."""
    if sha256_hex(raw) != ORIGINAL_SHA256:
        raise RuntimeError("R6 audit source is not the reviewed original; refuse overwrite")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").replace("\r\n", "\n")
    start = text.find("def certify_reviewed_production(root: Path) -> dict[str, str]:\n")
    stop = text.find("\ndef summarize_dependency(", start)
    if start < 0 or stop < 0 or text.count("def certify_reviewed_production(") != 1:
        raise RuntimeError("R6 certification function boundary changed")
    changed = text[:start] + FUNCTION + text[stop:]
    if changed == text:
        raise RuntimeError("R6D would have no effect")
    compile(changed, TARGET, "exec")
    return changed.replace("\n", newline).encode("utf-8")


def whole_function(raw: bytes) -> str:
    text = raw.decode("utf-8").replace("\r\n", "\n")
    start = text.find("def certify_reviewed_production(root: Path) -> dict[str, str]:\n")
    stop = text.find("\ndef summarize_dependency(", start)
    if start < 0 or stop < 0:
        raise RuntimeError("R6D function export failed")
    return text[start:stop].rstrip() + "\n"
