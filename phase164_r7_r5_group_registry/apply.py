"""R7-R5 guarded application: standard Group facade only."""
import hashlib
import shutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "toda_calculation_facade.py"
EXPECTED_BLOB_SHA = "d096b97f8def6a5f55a01dfa79e8ff73702be147"
OLD_IMPORT = 'from proof_repository import ProofRepository\n'
NEW_IMPORT = 'from phase164_r7_repository_root_resolution import (\n  validate_repository_internal_proof_roots,\n)\n'
OLD_FUNCTION = 'def build_standard_toda_report(\n  n: int,\n  k: int,\n) -> TodaCalculationReportResult:\n  repository = (\n    build_standard_production_proof_repository()\n  )\n\n  return build_toda_report(\n    repository,\n    n=n,\n    k=k,\n  )\n'
NEW_FUNCTION = 'def build_standard_toda_report(\n  n: int,\n  k: int,\n) -> TodaCalculationReportResult:\n  repository = (\n    build_standard_production_proof_repository()\n  )\n\n  validate_repository_internal_proof_roots(\n    repository\n  )\n\n  return build_toda_report(\n    repository,\n    n=n,\n    k=k,\n  )\n'


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main():
    if not TARGET.is_file():
        raise RuntimeError("Missing Group facade")
    for prerequisite in ("phase164_r7_repository_root_resolution.py", "phase164_r7_statement_resolution.py"):
        if not (ROOT / prerequisite).is_file():
            raise RuntimeError(f"Missing R7 prerequisite: {prerequisite}")
    original = TARGET.read_bytes()
    text = original.decode("utf-8").replace("\r\n", "\n")
    if git_blob_sha(original) == EXPECTED_BLOB_SHA:
        if text.count(OLD_IMPORT) != 1 or text.count(OLD_FUNCTION) != 1:
            raise RuntimeError("Group facade anchors not unique")
        updated = text.replace(OLD_IMPORT, OLD_IMPORT + NEW_IMPORT, 1).replace(OLD_FUNCTION, NEW_FUNCTION, 1)
    elif NEW_IMPORT in text and NEW_FUNCTION in text:
        updated = text
    else:
        raise RuntimeError("Group facade differs from inspected GitHub baseline; no changes applied")
    data = updated.replace("\n", "\r\n" if b"\r\n" in original else "\n").encode("utf-8")
    compile(data, str(TARGET), "exec")
    test_source = PACKAGE / "files/tests/test_phase164_r7_r5_group_registry.py"
    test_destination = ROOT / "tests/test_phase164_r7_r5_group_registry.py"
    test_data = test_source.read_bytes()
    compile(test_data, str(test_source), "exec")
    if test_destination.exists() and test_destination.read_bytes() != test_data:
        raise RuntimeError("Existing R7-R5 tests conflict; no changes applied")
    backup = ROOT / "toda_calculation_facade.phase164_r7_r5_backup.py"
    if original != data and backup.exists() and backup.read_bytes() != original:
        raise RuntimeError("Backup conflict; no changes applied")
    if original != data:
        backup.write_bytes(original)
        TARGET.write_bytes(data)
        print("Updated:", TARGET.name)
    if not test_destination.exists():
        test_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(test_source, test_destination)
        print("Added:", test_destination.name)
    print("R7-R5 Group facade uses shared internal proof-root resolver")


if __name__ == "__main__":
    main()
