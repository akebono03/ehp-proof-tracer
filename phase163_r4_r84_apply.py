"""Phase 163 R4-R84: guarded source archive origin migration."""
from __future__ import annotations

import argparse
from pathlib import Path

OLD_ENUM = '''class AssertionOrigin(str, Enum):
    FIXED_STATEMENT = "fixed_statement"
    PROOF_INTERNAL = "proof_internal"
'''
NEW_ENUM = '''class AssertionOrigin(str, Enum):
    FIXED_STATEMENT = "fixed_statement"
    PROOF_INTERNAL = "proof_internal"
    SOURCE_ARCHIVE = "source_archive"
'''
OLD_ENTRY = 'origin=AssertionOrigin.FIXED_STATEMENT,'
NEW_ENTRY = 'origin=AssertionOrigin.SOURCE_ARCHIVE,'


def transformed_registry(source: str) -> str:
    if source.count(OLD_ENUM) != 1 or "SOURCE_ARCHIVE" in source:
        raise ValueError("registry origin block mismatch; refusing change")
    return source.replace(OLD_ENUM, NEW_ENUM, 1)


def transformed_archive(source: str) -> str:
    if source.count(OLD_ENTRY) != 1 or NEW_ENTRY in source:
        raise ValueError("archive origin block mismatch; refusing change")
    return source.replace(OLD_ENTRY, NEW_ENTRY, 1)


def apply(project: Path, payload: Path) -> tuple[str, str]:
    registry_file = project / "unified_statement_registry.py"
    archive_file = project / "phase163_source_archive_registry.py"
    catalog_file = project / "phase163_source_archive_catalog.json"
    if not all(path.is_file() for path in (registry_file, archive_file, catalog_file)):
        raise FileNotFoundError("R83 installation or registry missing")
    reg_raw = registry_file.read_bytes()
    arc_raw = archive_file.read_bytes()
    registry_text = reg_raw.decode("utf-8")
    archive_text = arc_raw.decode("utf-8")
    updated_registry = transformed_registry(registry_text)
    updated_archive = transformed_archive(archive_text)
    expected_archive = (payload / "phase163_source_archive_registry.py").read_text(encoding="utf-8")
    if updated_archive.replace("\r\n", "\n") != expected_archive.replace("\r\n", "\n"):
        raise ValueError("R83 archive diverged from expected version")
    backups = [registry_file.with_suffix(".phase163_r84_before.py.bak"),
               archive_file.with_suffix(".phase163_r84_before.py.bak")]
    if any(path.exists() for path in backups):
        raise FileExistsError("R84 backup already exists; refusing overwrite")
    for path, raw in zip(backups, (reg_raw, arc_raw)):
        path.write_bytes(raw)
    registry_file.write_text(updated_registry, encoding="utf-8", newline="")
    archive_file.write_text(updated_archive, encoding="utf-8", newline="")
    return str(registry_file), str(archive_file)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--package", type=Path, required=True)
    args = parser.parse_args()
    print("Changed:", *apply(args.project, args.package), sep="\n")


if __name__ == "__main__":
    main()
