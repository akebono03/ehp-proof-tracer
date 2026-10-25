"""Apply a conservative Phase 168 documentation update to a real checkout.

Historical large documents are read from the checkout and preserved verbatim.
Complete updated copies of all five Markdown files are emitted in output/full_files.
No production module or test is modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
BACKUPS = OUTPUT / "backups"
FULL = OUTPUT / "full_files"
MANIFEST = OUTPUT / "manifest.json"

DOCS = (
    "README.md",
    "docs/design.md",
    "docs/development_log.md",
    "docs/roadmap.md",
    "docs/proof_records.md",
)
MARKER = "<!-- PHASE168_FINAL_CLOSURE_20261025 -->"
ROADMAP_OLD_HEADING = "## Phase 168 — 2-stem 証明生成（次工程・未着手）"
ROADMAP_LAST_LINE = "5. 全体 pytest は Phase 168 の終了時に実施する。"
HEADINGS = {
    "docs/design.md": "# EHP Proof Tracer 設計",
    "docs/development_log.md": "# EHP Proof Tracer 開発記録",
    "docs/roadmap.md": "# EHP Proof Tracer ロードマップ",
    "docs/proof_records.md": "# EHP Proof Tracer — 証明記録",
}
REQUIRED_HISTORICAL_ANCHORS = {
    "docs/design.md": ("<!-- PHASE165_FINAL_CLOSURE_20261019 -->", "<!-- PHASE166_HANDOFF_20261021 -->"),
    "docs/development_log.md": ("<!-- PHASE167_CLOSURE_20261022 -->", "<!-- PHASE166_HANDOFF_20261021 -->"),
    "docs/roadmap.md": ("<!-- PHASE167_CLOSURE_20261022 -->", ROADMAP_OLD_HEADING),
    "docs/proof_records.md": ("<!-- PHASE167_CLOSURE_20261022 -->", "<!-- PHASE166_HANDOFF_20261021 -->"),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def payload_path(name: str) -> Path:
    if name == "README.md":
        return PACKAGE / "payload" / "README.md"
    return PACKAGE / "payload" / "sections" / Path(name).name


def validate_original(name: str, original: bytes) -> str:
    if b"\x00" in original:
        raise RuntimeError(name + ": binary source refused")
    try:
        text = original.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise RuntimeError(name + ": source must be UTF-8") from exc
    if MARKER in text:
        raise RuntimeError(name + ": closure section already present; refusing duplicate")
    if name == "README.md":
        reviewed = (PACKAGE / "payload" / "README.before.md").read_text(encoding="utf-8")
        def significant_lines(value: str) -> tuple[str, ...]:
            return tuple(line.rstrip() for line in value.splitlines() if line.strip())
        if significant_lines(text) != significant_lines(reviewed):
            raise RuntimeError(name + ": README differs from reviewed pre-closure version")
    else:
        if not text.startswith(HEADINGS[name]):
            raise RuntimeError(name + ": unexpected Markdown title")
        for anchor in REQUIRED_HISTORICAL_ANCHORS[name]:
            if anchor not in text:
                raise RuntimeError(name + ": missing prerequisite historical anchor: " + anchor)
        if len(original) < 12000:
            raise RuntimeError(name + ": historical document unexpectedly short")
    if name == "docs/roadmap.md":
        if text.count(ROADMAP_OLD_HEADING) != 1 or not text.rstrip().endswith(ROADMAP_LAST_LINE):
            raise RuntimeError(name + ": final planned Phase 168 section has changed")
    return text


def build_updated(name: str, original: bytes) -> bytes:
    text = validate_original(name, original)
    section = payload_path(name).read_text(encoding="utf-8")
    if name == "README.md":
        updated = section
    elif name == "docs/roadmap.md":
        position = text.index(ROADMAP_OLD_HEADING)
        updated = text[:position].rstrip() + "\n\n" + section
    else:
        updated = text.rstrip("\r\n") + "\n\n" + section
    if updated.count(MARKER) != (0 if name == "README.md" else 1):
        raise RuntimeError(name + ": missing or repeated new closure marker")
    encoded = updated.encode("utf-8")
    if name != "README.md" and original.startswith(b"\xef\xbb\xbf"):
        encoded = b"\xef\xbb\xbf" + encoded
    if name != "README.md" and len(encoded) <= len(original) // 2:
        raise RuntimeError(name + ": historical content might have been discarded")
    return encoded


def atomic_write(target: Path, data: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=".ehp_doc_", dir=str(target.parent))
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, target)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def current_matches_existing_manifest() -> bool:
    if not MANIFEST.is_file():
        return False
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("status") != "APPLIED":
        raise RuntimeError("previous documentation manifest is not an applied version")
    for name in DOCS:
        entry = manifest["files"][name]
        if sha((ROOT / name).read_bytes()) != entry["after_sha256"]:
            raise RuntimeError("previously applied documentation changed: " + name)
    return True


def generate_review_bundle(manifest: dict) -> Path:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    result = OUTPUT / "phase168_documentation_full_files_review.zip"
    with zipfile.ZipFile(result, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name in DOCS:
            z.write(FULL / name, "updated_full_files/" + name)
            z.write(BACKUPS / name, "original_backups/" + name)
        z.write(MANIFEST, "manifest.json")
    with zipfile.ZipFile(result) as z:
        if z.testzip() is not None:
            raise RuntimeError("review ZIP integrity check failed")
    return result


def apply() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if current_matches_existing_manifest():
        print("DOCUMENTATION_ALREADY_APPLIED", flush=True)
        verify()
        return

    original: dict[str, bytes] = {}
    updated: dict[str, bytes] = {}
    for name in DOCS:
        target = ROOT / name
        if not target.is_file():
            raise RuntimeError("missing source document: " + name)
        original[name] = target.read_bytes()
        updated[name] = build_updated(name, original[name])
        backup = BACKUPS / name
        if backup.exists() and backup.read_bytes() != original[name]:
            raise RuntimeError("existing backup differs from original: " + name)

    # Every original is persisted before the first production document changes.
    for name in DOCS:
        backup = BACKUPS / name
        if not backup.exists():
            atomic_write(backup, original[name])

    files = {
        name: {"before_sha256": sha(original[name]), "after_sha256": sha(updated[name]), "bytes_after": len(updated[name])}
        for name in DOCS
    }
    manifest = {"phase": "168", "status": "APPLIED", "updated_at_utc": datetime.now(timezone.utc).isoformat(), "files": files}
    changed: list[str] = []
    try:
        for name in DOCS:
            atomic_write(ROOT / name, updated[name])
            changed.append(name)
            print("DOCUMENT_UPDATED", name, flush=True)
        for name in DOCS:
            atomic_write(FULL / name, updated[name])
            if sha((ROOT / name).read_bytes()) != files[name]["after_sha256"]:
                raise RuntimeError("post-write SHA256 mismatch: " + name)
        atomic_write(MANIFEST, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        bundle = generate_review_bundle(manifest)
    except Exception:
        for name in reversed(changed):
            target = ROOT / name
            if target.read_bytes() == updated[name]:
                atomic_write(target, original[name])
                print("AUTO_RESTORED", name, flush=True)
            else:
                print("MANUAL_INSPECTION_REQUIRED", name, flush=True)
        if MANIFEST.exists():
            MANIFEST.unlink()
        raise
    print("FULL_DOCUMENTS", FULL, flush=True)
    print("REVIEW_BUNDLE", bundle, flush=True)
    print("DOCUMENTATION_CLOSURE_APPLIED 5", flush=True)
    print("PYTEST_NOT_RERUN_DOCUMENTATION_ONLY", flush=True)


def verify() -> None:
    if not MANIFEST.is_file():
        raise RuntimeError("documentation manifest missing")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("phase") != "168" or manifest.get("status") != "APPLIED":
        raise RuntimeError("documentation manifest status invalid")
    if set(manifest["files"]) != set(DOCS):
        raise RuntimeError("documentation manifest incomplete")
    for name in DOCS:
        target = ROOT / name
        expected = manifest["files"][name]["after_sha256"]
        if sha(target.read_bytes()) != expected or sha((FULL / name).read_bytes()) != expected:
            raise RuntimeError("applied document does not match its FULL output: " + name)
        before = manifest["files"][name]["before_sha256"]
        if sha((BACKUPS / name).read_bytes()) != before:
            raise RuntimeError("backup mutated: " + name)
        if name != "README.md" and MARKER not in target.read_text(encoding="utf-8-sig"):
            raise RuntimeError("Phase 168 closure marker absent: " + name)
        print("VERIFIED_FULL_DOCUMENT", name, "BYTES", target.stat().st_size, flush=True)
    print("ALL_FIVE_FULL_DOCUMENTS_VERIFIED", flush=True)
    print("PYTEST_NOT_RERUN_DOCUMENTATION_ONLY", flush=True)


def restore() -> None:
    if not MANIFEST.is_file():
        raise RuntimeError("no applied manifest; restore requires a successful apply")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for name in DOCS:
        entry = manifest["files"][name]
        if sha((ROOT / name).read_bytes()) != entry["after_sha256"]:
            raise RuntimeError("document changed after apply; refusing restore: " + name)
        if sha((BACKUPS / name).read_bytes()) != entry["before_sha256"]:
            raise RuntimeError("backup changed; refusing restore: " + name)
    for name in DOCS:
        atomic_write(ROOT / name, (BACKUPS / name).read_bytes())
        print("RESTORED_DOCUMENT", name, flush=True)
    MANIFEST.rename(OUTPUT / "manifest.restored.json")
    print("DOCUMENTATION_RESTORED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("apply", "verify", "restore"))
    args = parser.parse_args()
    if args.mode == "apply":
        apply()
    elif args.mode == "verify":
        verify()
    else:
        restore()


if __name__ == "__main__":
    main()
