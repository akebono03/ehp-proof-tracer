"""Patch only reviewed functions; keep checked backups and full-file copies."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
WEB = Path("web_group_proof.py")
P14_TEST = Path(
    "phase168_r3_41p14_trust_boundary_audit/tests/"
    "test_phase168_r3_41p14_trust_boundary_audit.py"
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def locate(source: str, name: str) -> ast.FunctionDef:
    matches = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one function: {name}")
    return matches[0]


def patch_function(source: str, name: str, old: str, new: str) -> str:
    current = locate(source, name)
    expected = locate(old, name)
    replacement = locate(new, name)
    if ast.dump(current, include_attributes=False) != ast.dump(expected, include_attributes=False):
        raise RuntimeError(f"unreviewed existing function: {name}")
    lines = source.splitlines(keepends=True)
    start = min((dec.lineno for dec in current.decorator_list), default=current.lineno)
    replacement_lines = new.splitlines(keepends=True)
    new_start = min((dec.lineno for dec in replacement.decorator_list), default=replacement.lineno)
    new_text = "".join(replacement_lines[new_start - 1:replacement.end_lineno])
    result = "".join(lines[:start - 1]) + new_text + "".join(lines[current.end_lineno:])
    ast.parse(result)
    return result


def encode_like(original: bytes, rewritten: str) -> bytes:
    newline = "\r\n" if b"\r\n" in original else "\n"
    data = rewritten.replace("\r\n", "\n").replace("\n", newline).encode("utf-8")
    return (b"\xef\xbb\xbf" + data) if original.startswith(b"\xef\xbb\xbf") else data


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if (OUTPUT / "manifest.json").exists():
        raise RuntimeError("R3-41P15 is already installed or has backups; refusing to overwrite")
    specs = (
        (
            WEB, "build_standard_web_group_proof_view",
            PACKAGE / "full_functions" / "before_P13_FULL.py",
            PACKAGE / "full_functions" / "build_standard_web_group_proof_view_FULL.py",
        ),
        (
            P14_TEST, "test_complete_unverified_routes_reach_model_without_invoking_boundary",
            PACKAGE / "expected_before" / "test_phase168_r3_41p14_trust_boundary_audit.py",
            PACKAGE / "tests" / "test_phase168_r3_41p14_trust_boundary_audit_FULL.py",
        ),
    )
    replacements: list[tuple[Path, bytes, bytes]] = []
    for relative, name, before_file, after_file in specs:
        target = ROOT / relative
        if not target.is_file():
            raise FileNotFoundError(f"required reviewed file is absent: {relative}")
        original = target.read_bytes()
        content = original.decode("utf-8-sig")
        old = before_file.read_text(encoding="utf-8-sig")
        new = after_file.read_text(encoding="utf-8-sig")
        # For the P14 audit test, the name changes as part of the replacement.
        if relative == P14_TEST:
            old_node = locate(old, name)
            replacement_name = "test_complete_web_boundary_is_always_required"
            new_node = locate(new, replacement_name)
            replacement_source = "".join(new.splitlines(keepends=True)[
                min((d.lineno for d in new_node.decorator_list), default=new_node.lineno) - 1:
                new_node.end_lineno
            ])
            old_current = locate(content, name)
            if ast.dump(old_current, include_attributes=False) != ast.dump(old_node, include_attributes=False):
                raise RuntimeError("reviewed P14 audit test changed unexpectedly")
            lines = content.splitlines(keepends=True)
            start = min((d.lineno for d in old_current.decorator_list), default=old_current.lineno)
            rewritten = "".join(lines[:start - 1]) + replacement_source + "".join(lines[old_current.end_lineno:])
            ast.parse(rewritten)
        else:
            rewritten = patch_function(content, name, old, new)
        replacements.append((relative, original, encode_like(original, rewritten)))
    manifest = {
        "phase": "168 R3-41P15",
        "changed": {},
        "full_pytest_run": False,
        "notes": "P14 old behavior regression expectation updated for the repaired boundary",
    }
    for relative, before, after in replacements:
        key = relative.as_posix()
        backup = OUTPUT / (relative.name + ".before")
        if backup.exists():
            raise RuntimeError(f"backup already exists: {backup}")
        backup.write_bytes(before)
        manifest["changed"][key] = {
            "backup": backup.name,
            "before_sha256": digest(before),
            "after_sha256": digest(after),
        }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    try:
        for relative, before, after in replacements:
            target = ROOT / relative
            if target.read_bytes() != before:
                raise RuntimeError(f"source changed during install: {relative}")
            target.write_bytes(after)
            (OUTPUT / (relative.name + ".FULL.py")).write_bytes(after)
            print("PATCHED", target)
            print("BACKUP", OUTPUT / (relative.name + ".before"))
            print("FULL_FILE", OUTPUT / (relative.name + ".FULL.py"))
    except BaseException:
        for relative, before, after in replacements:
            target = ROOT / relative
            if target.read_bytes() in (before, after):
                target.write_bytes(before)
        raise


if __name__ == "__main__":
    main()
