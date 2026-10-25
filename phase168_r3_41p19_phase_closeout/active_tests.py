"""Phase 168 closeout: reconcile active tests with previously retired Phase 144 copies.

Only three Phase 167 tests are updated to the current public Web projection.
Two Phase 144 files are taken out of active tests/ ONLY if identical bytes
already exist in the archived Phase 165 retirement record.
All five original files are backed up and can be restored exactly.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
FILES = PACKAGE / "active_test_full_files"
MANIFEST = OUTPUT / "active_tests_manifest.json"
REPLACEMENTS = (
    "test_phase167_r2_range_dedup.py",
    "test_phase167_r2_shared_reference.py",
    "test_phase167_r2_unified_reference.py",
)
RETIRED = (
    "test_phase144_6_pi6_generic_production_route.py",
    "test_phase144_6_public_route_cutover.py",
)
ARCHIVE = ROOT / "phase165_r6_audit_results" / "retired_phase144_tests" / "20261019T070710Z"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _module_ast(source: str) -> str:
    return ast.dump(ast.parse(source), include_attributes=False)


def _decode(data: bytes) -> str:
    return data.decode("utf-8-sig")


def _write_same_line_endings(original: bytes, replacement: str) -> bytes:
    eol = "\r\n" if b"\r\n" in original else "\n"
    converted = replacement.replace("\r\n", "\n").replace("\n", eol).encode("utf-8")
    return (b"\xef\xbb\xbf" + converted) if original.startswith(b"\xef\xbb\xbf") else converted


def install() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists():
        raise RuntimeError("an active test migration manifest already exists")
    backup_dir = OUTPUT / "active_test_backups"
    plan: list[dict[str, str]] = []
    contents: dict[str, bytes] = {}
    originals: dict[str, bytes] = {}

    for name in REPLACEMENTS + RETIRED:
        path = ROOT / "tests" / name
        if not path.is_file():
            raise RuntimeError("active test missing: " + name)
        original = path.read_bytes()
        originals[name] = original
        if name in REPLACEMENTS:
            expected = (FILES / (name + ".BEFORE.py")).read_text(encoding="utf-8")
            after = (FILES / (name + ".FULL.py")).read_text(encoding="utf-8")
            if _module_ast(_decode(original)) != _module_ast(expected):
                raise RuntimeError("active test differs from reviewed baseline: " + name)
            contents[name] = _write_same_line_endings(original, after)
            action = "replace"
        else:
            historic = ARCHIVE / name
            if not historic.is_file():
                raise RuntimeError("retired test has no preserved Phase 165 copy: " + name)
            if historic.read_bytes() != original:
                raise RuntimeError("retired test differs from archived byte-exact copy: " + name)
            action = "retire_duplicate"
        backup = backup_dir / (name + ".before")
        if backup.exists() and backup.read_bytes() != original:
            raise RuntimeError("existing test backup differs: " + name)
        plan.append({
            "name": name, "action": action,
            "path": "tests/" + name,
            "backup": "active_test_backups/" + name + ".before",
            "before_sha256": digest(original),
            "after_sha256": digest(contents[name]) if action == "replace" else None,
            "archived_path": str((ARCHIVE / name).relative_to(ROOT)).replace("\\", "/")
            if action == "retire_duplicate" else None,
        })

    backup_dir.mkdir(parents=True, exist_ok=True)
    for entry in plan:
        backup = OUTPUT / entry["backup"]
        if not backup.exists():
            backup.write_bytes(originals[entry["name"]])
        if digest(backup.read_bytes()) != entry["before_sha256"]:
            raise RuntimeError("test backup content changed: " + entry["name"])

    MANIFEST.write_text(json.dumps({"version": 1, "files": plan}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        for entry in plan:
            path = ROOT / entry["path"]
            if digest(path.read_bytes()) != entry["before_sha256"]:
                raise RuntimeError("active test changed during migration: " + entry["name"])
            if entry["action"] == "replace":
                path.write_bytes(contents[entry["name"]])
                print("UPDATED_REFERENCE_TEST", path, flush=True)
            else:
                path.unlink()
                print("RETIRED_DUPLICATE", path, "PRESERVED_IN", entry["archived_path"], flush=True)
    except BaseException:
        restore()
        raise
    print("ACTIVE_TEST_CONTRACT_MIGRATED", len(REPLACEMENTS), "RETIRED_DUPLICATES", len(RETIRED), flush=True)


def restore() -> None:
    if not MANIFEST.is_file():
        raise RuntimeError("no active test migration manifest to restore")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != 1:
        raise RuntimeError("incompatible test manifest")
    # Preflight every path, BEFORE restoring even one file.
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        backup = OUTPUT / entry["backup"]
        if not backup.is_file() or digest(backup.read_bytes()) != entry["before_sha256"]:
            raise RuntimeError("test backup checksum mismatch: " + entry["name"])
        if entry["action"] == "retire_duplicate":
            if path.exists() and digest(path.read_bytes()) != entry["before_sha256"]:
                raise RuntimeError("retired test was changed after migration: " + entry["name"])
        elif entry["action"] == "replace":
            if not path.is_file() or digest(path.read_bytes()) not in (
                entry["before_sha256"], entry["after_sha256"],
            ):
                raise RuntimeError("updated test was changed after migration: " + entry["name"])
        else:
            raise RuntimeError("invalid test action")
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        data = (OUTPUT / entry["backup"]).read_bytes()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        if path.read_bytes() != data:
            raise RuntimeError("test restoration verification failed: " + entry["name"])
        print("RESTORED_TEST", path, flush=True)
    MANIFEST.replace(OUTPUT / "active_tests_manifest.restored.json")
    print("ACTIVE_TESTS_RESTORED", flush=True)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("install", "restore"))
    arguments = parser.parse_args()
    if arguments.action == "install":
        install()
    else:
        restore()


if __name__ == "__main__":
    main()
