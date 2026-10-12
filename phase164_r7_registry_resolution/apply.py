"""Phase 164 R7 guarded installer. Only R3 resolution caller is migrated."""
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase164_r3_registry_search_connection.py"
EXPECTED = "ce9352c426515c31bade8dfd46475969d8eed254"
IMPORT_OLD = 'from phase164_r2_citation_eligibility import assess_phase164_r2_citation\n'
IMPORT_NEW = 'from phase164_r7_statement_resolution import resolve_registered_statement\n'
OLD = '''        entry = bridge.registry.assertion(item.assertion_id)
        # Identity of the mathematical statement is checked structurally; the
        # Assertion ID by itself cannot authorize an unrelated ProofStep.
        if type(entry.content) is not type(item.step.conclusion):
            raise ValueError("registered conclusion type mismatch")
        equality = entry.content == item.step.conclusion
        if type(equality) is not bool or not equality:
            raise ValueError("registered conclusion mismatch")
        decision = assess_phase164_r2_citation(
            bridge, item.assertion_id, citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
        if not decision.usable:
            raise ValueError(
                f"citation not eligible: {item.assertion_id}: "
                f"{decision.status.value}/{decision.reason}"
            )
'''
NEW = '''        resolve_registered_statement(
            bridge,
            item.assertion_id,
            expected_conclusion=item.step.conclusion,
            citing_assertion_id=citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
'''


def git_hash(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> None:
    original = TARGET.read_bytes()
    source = original.decode("utf-8")
    if git_hash(original) != EXPECTED:
        if IMPORT_NEW in source and NEW in source and IMPORT_OLD not in source:
            print("R3 already connected; verifying files")
        else:
            raise RuntimeError("Local R3 differs from checked GitHub baseline; no files changed")
    else:
        if source.count(IMPORT_OLD) != 1 or source.count(OLD) != 1:
            raise RuntimeError("R3 expected import/function section mismatch; no files changed")
        patched = source.replace(IMPORT_OLD, IMPORT_NEW).replace(OLD, NEW)
        compile(patched, str(TARGET), "exec")
    files = (
        (PACKAGE / "files/phase164_r7_statement_resolution.py", ROOT / "phase164_r7_statement_resolution.py"),
        (PACKAGE / "files/tests/test_phase164_r7_statement_resolution.py", ROOT / "tests/test_phase164_r7_statement_resolution.py"),
    )
    for src, _ in files:
        compile(src.read_text(encoding="utf-8"), str(src), "exec")
    if git_hash(original) == EXPECTED:
        backup = ROOT / "phase164_r3_registry_search_connection.phase164_r7_backup.py"
        if backup.exists() and backup.read_bytes() != original:
            raise RuntimeError("Existing R7 backup differs; refusing overwrite")
        backup.write_bytes(original)
        TARGET.write_text(patched, encoding="utf-8", newline="")
        print("Migrated R3 registered literature lookup to common R7 resolver")
    for src, dst in files:
        if dst.exists() and dst.read_bytes() != src.read_bytes():
            raise RuntimeError(f"Existing R7 path differs: {dst}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    print("Installed read-only statement resolution API and focused tests")


if __name__ == "__main__":
    main()
