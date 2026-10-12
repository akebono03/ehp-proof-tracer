"""Guarded, repeatable Phase 164 R7-R3 installer."""
import hashlib
import shutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "repository_generator_known_group_identity_lookup.py"
EXPECTED_SHA = "68215f1f022ec9ab4a48c65da1bc377fe806db22"
INSERT_IMPORT_AFTER = (
    "from proof_repository import (\n"
    "  ProofRepository,\n"
    ")\n"
)
ADDED_IMPORT = (
    "from phase164_r7_r3_generator_registry import (\n"
    "  validate_generator_repository_registry_links,\n"
    ")\n"
)
OLD_FUNCTION_SECTION = (
    "  repository = (\n"
    "    build_standard_production_proof_repository()\n"
    "  )\n\n"
    "  return (\n"
)
NEW_FUNCTION_SECTION = (
    "  repository = (\n"
    "    build_standard_production_proof_repository()\n"
    "  )\n\n"
    "  validate_generator_repository_registry_links(\n"
    "    repository\n"
    "  )\n\n"
    "  return (\n"
)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> None:
    original = TARGET.read_bytes()
    normalized = original.decode("utf-8").replace("\r\n", "\n")
    if blob_sha(original) == EXPECTED_SHA:
        if normalized.count(INSERT_IMPORT_AFTER) != 1:
            raise RuntimeError("Expected original import block not found; no changes")
        if normalized.count(OLD_FUNCTION_SECTION) != 1:
            raise RuntimeError("Expected Generator function section not unique; no changes")
        new_source = normalized.replace(
            INSERT_IMPORT_AFTER, INSERT_IMPORT_AFTER + ADDED_IMPORT, 1
        ).replace(OLD_FUNCTION_SECTION, NEW_FUNCTION_SECTION, 1)
        compile(new_source, str(TARGET), "exec")
        # Preserve CRLF if the original file uses it.
        ending = "\r\n" if b"\r\n" in original else "\n"
        new_bytes = new_source.replace("\n", ending).encode("utf-8")
        patched = True
    elif ADDED_IMPORT in normalized and NEW_FUNCTION_SECTION in normalized:
        new_bytes = original
        patched = False
    else:
        raise RuntimeError("Local Generator source differs from inspected GitHub baseline")

    destinations = [
        (PACKAGE / "files/phase164_r7_r3_generator_registry.py", ROOT / "phase164_r7_r3_generator_registry.py"),
        (PACKAGE / "files/tests/test_phase164_r7_r3_generator_registry.py", ROOT / "tests/test_phase164_r7_r3_generator_registry.py"),
    ]
    for source, dest in destinations:
        compile(source.read_text(encoding="utf-8"), str(source), "exec")
        if dest.exists() and dest.read_bytes() != source.read_bytes():
            raise RuntimeError(f"Existing R7-R3 file differs, refusing overwrite: {dest}")
    dependency = ROOT / "phase164_r7_statement_resolution.py"
    if not dependency.exists():
        raise RuntimeError("R7-R1 resolver missing; run R7-R1 first")
    if "def resolve_registered_statement(" not in dependency.read_text(encoding="utf-8"):
        raise RuntimeError("R7 resolver contract not recognized")
    backup = ROOT / "repository_generator_known_group_identity_lookup.phase164_r7_r3_backup.py"
    if patched and backup.exists() and backup.read_bytes() != original:
        raise RuntimeError("Pre-existing R7-R3 backup differs; refusing overwrite")

    if patched:
        backup.write_bytes(original)
        TARGET.write_bytes(new_bytes)
        print("Guarded Generator standard entry with registered internal proof-root resolution")
    else:
        print("Generator entry already patched; verifying package files")
    for source, dest in destinations:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            shutil.copyfile(source, dest)
    print("R7-R3 installation complete; existing ProofStep and public APIs preserved")


if __name__ == "__main__":
    main()
