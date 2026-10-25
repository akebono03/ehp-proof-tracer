"""Install only the reviewed factory function and observational source module."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
FACTORY = ROOT / "phase164_r8_proofstep_factory.py"
ADAPTER = ROOT / "phase165_r52_r2_search_adapter.py"
CAPTURE = ROOT / "proof_origin_capture.py"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def locate(source: str, name: str) -> ast.FunctionDef:
    matches = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    if len(matches) != 1:
        raise RuntimeError("expected exactly one " + name)
    return matches[0]


def preserve_newlines(original: bytes, text: str) -> bytes:
    ending = "\r\n" if b"\r\n" in original else "\n"
    raw = text.replace("\r\n", "\n").replace("\n", ending).encode("utf-8")
    if original.startswith(b"\xef\xbb\xbf"):
        raw = b"\xef\xbb\xbf" + raw
    return raw


def install() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUTPUT / "manifest.json"
    if manifest_path.exists():
        raise RuntimeError("existing installation manifest; refusing to overwrite backups")
    if CAPTURE.exists():
        raise RuntimeError("proof_origin_capture.py already exists; refusing overwrite")
    specs = (
        (FACTORY, "derive_inference_proof_step"),
        (ADAPTER, "search_registered_partial_proof"),
    )
    replacements = []
    for target, name in specs:
        old_bytes = target.read_bytes()
        source = old_bytes.decode("utf-8-sig")
        current = locate(source, name)
        before = (PACKAGE / "full_functions" / (name + "_BEFORE.py")).read_text(encoding="utf-8")
        after = (PACKAGE / "full_functions" / (name + "_FULL.py")).read_text(encoding="utf-8")
        if ast.dump(current, include_attributes=False) != ast.dump(
            locate(before, name), include_attributes=False
        ):
            raise RuntimeError("existing function differs from reviewed develop version: " + name)
        lines = source.splitlines(keepends=True)
        start = min((d.lineno for d in current.decorator_list), default=current.lineno)
        updated = "".join(lines[:start - 1]) + after.rstrip("\n") + "\n" + "".join(lines[current.end_lineno:])
        ast.parse(updated)
        rewritten = preserve_newlines(old_bytes, updated)
        replacements.append((target, old_bytes, rewritten))
    new_capture = (PACKAGE / "proof_origin_capture.py").read_bytes()
    manifest = {
        "phase": "168 R3-41P17",
        "changed": {},
        "new_file": str(CAPTURE.relative_to(ROOT)),
        "new_sha256": sha(new_capture),
        "full_pytest_run": False,
    }
    for target, original, rewritten in replacements:
        backup = OUTPUT / (target.name + ".before")
        if backup.exists():
            if backup.read_bytes() != original:
                raise RuntimeError(
                    "existing backup differs from current reviewed source: "
                    + backup.name
                )
            # A previous failed run may have restored the original modules.
            # Reuse only their byte-identical backups; never silently replace one.
        else:
            backup.write_bytes(original)
        manifest["changed"][str(target.relative_to(ROOT))] = {
            "backup": backup.name,
            "before_sha256": sha(original),
            "after_sha256": sha(rewritten),
        }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        CAPTURE.write_bytes(new_capture)
        for target, original, rewritten in replacements:
            if target.read_bytes() != original:
                raise RuntimeError("source changed between review and patch: " + target.name)
            target.write_bytes(rewritten)
            (OUTPUT / (target.name + ".FULL.py")).write_bytes(rewritten)
    except BaseException:
        for target, original, rewritten in replacements:
            if target.read_bytes() == rewritten:
                target.write_bytes(original)
        if CAPTURE.exists() and CAPTURE.read_bytes() == new_capture:
            CAPTURE.unlink()
        raise
    for target, original, rewritten in replacements:
        print("PATCHED", target)
        print("BACKUP", OUTPUT / (target.name + ".before"))
        print("FULL_FILE", OUTPUT / (target.name + ".FULL.py"))
    (OUTPUT / "proof_origin_capture.py.FULL.py").write_bytes(new_capture)
    print("ADDED", CAPTURE)
    print("FULL_FILE", OUTPUT / "proof_origin_capture.py.FULL.py")

if __name__ == "__main__":
    install()
