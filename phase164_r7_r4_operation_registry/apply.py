"""Install only R7-R4 scoped operation entry and shared internal root resolver."""
import hashlib
import shutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OPERATION = ROOT / "repository_operation_query_facade.py"
GENERATOR_ADAPTER = ROOT / "phase164_r7_r3_generator_registry.py"
EXPECTED_OPERATION_SHA = "5dcf16588e4a958af84de8c6de2b3e600e0a75c8"
EXPECTED_GENERATOR_ADAPTER = '''"""Phase 164 R7-R3: resolve generator repository roots through the R7 registry API.

The bridge records existing internal proof roots, not verified literature.
This module neither constructs nor authorizes mathematical ProofSteps.
"""
from types import SimpleNamespace

from phase163_r4_registry_bridge import build_registry_bridge
from phase164_r7_statement_resolution import resolve_registered_statement
from proof_repository import ProofRepository
from unified_statement_registry import AssertionOrigin


def validate_generator_repository_registry_links(
    repository: ProofRepository,
) -> ProofRepository:
    """Fail closed on inconsistent registered root steps, preserving identity."""
    if not isinstance(repository, ProofRepository):
        raise TypeError("repository must be a ProofRepository")

    bridge = build_registry_bridge(
        components_by_reference={},
        theorem_facts=SimpleNamespace(entries=()),
        proof_repository=repository,
    )
    for entry in repository.entries():
        resolved = resolve_registered_statement(
            bridge,
            f"repository:{entry.key}:conclusion",
            proof_repository=repository,
            expected_conclusion=entry.step.conclusion,
        )
        if resolved.assertion.origin is not AssertionOrigin.PROOF_INTERNAL:
            raise ValueError("generator root must remain proof-internal")
        if resolved.proof_link is None or resolved.proof_link.step is not entry.step:
            raise ValueError("generator root ProofStep identity mismatch")
    return repository
'''
OP_IMPORT_ANCHOR = "from proof_repository import ProofRepository\n"
OP_NEW_IMPORT = "from phase164_r7_repository_root_resolution import (\n  validate_repository_internal_proof_roots,\n)\n"
OP_ORIGINAL_SECTION = (
    "  repository = (\n"
    "    build_standard_production_proof_repository()\n"
    "  )\n\n"
    "  return query_repository_operation_input(\n"
)
OP_NEW_SECTION = (
    "  repository = (\n"
    "    build_standard_production_proof_repository()\n"
    "  )\n\n"
    "  validate_repository_internal_proof_roots(\n"
    "    repository\n"
    "  )\n\n"
    "  return query_repository_operation_input(\n"
)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def normalize(data: bytes) -> str:
    return data.decode("utf-8").replace("\r\n", "\n")


def encoded(text: str, original: bytes) -> bytes:
    return text.replace("\n", "\r\n" if b"\r\n" in original else "\n").encode("utf-8")


def main() -> None:
    if not OPERATION.is_file() or not GENERATOR_ADAPTER.is_file():
        raise RuntimeError("R7-R3 prerequisite or Operation facade not found")
    if not (ROOT / "phase164_r7_statement_resolution.py").is_file():
        raise RuntimeError("R7 common resolver missing")
    operation_before = OPERATION.read_bytes()
    generator_before = GENERATOR_ADAPTER.read_bytes()
    op_text = normalize(operation_before)
    gen_text = normalize(generator_before)

    if blob_sha(operation_before) == EXPECTED_OPERATION_SHA:
        if op_text.count(OP_IMPORT_ANCHOR) != 1 or op_text.count(OP_ORIGINAL_SECTION) != 1:
            raise RuntimeError("Operation insertion anchors not unique")
        op_next = encoded(
            op_text.replace(OP_IMPORT_ANCHOR, OP_IMPORT_ANCHOR + OP_NEW_IMPORT, 1)
            .replace(OP_ORIGINAL_SECTION, OP_NEW_SECTION, 1), operation_before
        )
    elif OP_NEW_IMPORT in op_text and OP_NEW_SECTION in op_text:
        op_next = operation_before
    else:
        raise RuntimeError("Operation facade differs from inspected GitHub baseline")

    expected_gen = EXPECTED_GENERATOR_ADAPTER.replace("\r\n", "\n")
    new_gen = (PACKAGE / "files/phase164_r7_r3_generator_registry.py").read_text(encoding="utf-8")
    if gen_text == expected_gen:
        gen_next = encoded(new_gen, generator_before)
    elif gen_text == new_gen:
        gen_next = generator_before
    else:
        raise RuntimeError("Generator R7-R3 adapter differs from known implementation")

    for path, data in ((OPERATION, op_next), (GENERATOR_ADAPTER, gen_next)):
        compile(data, str(path), "exec")
    additions = (
        (PACKAGE / "files/phase164_r7_repository_root_resolution.py", ROOT / "phase164_r7_repository_root_resolution.py"),
        (PACKAGE / "files/tests/test_phase164_r7_r4_operation_registry.py", ROOT / "tests/test_phase164_r7_r4_operation_registry.py"),
    )
    for src, dst in additions:
        content = src.read_bytes()
        compile(content, str(src), "exec")
        if dst.exists() and dst.read_bytes() != content:
            raise RuntimeError(f"Existing file conflicts: {dst}")

    backups = (
        (OPERATION.with_name("repository_operation_query_facade.phase164_r7_r4_backup.py"), operation_before, op_next),
        (GENERATOR_ADAPTER.with_name("phase164_r7_r3_generator_registry.phase164_r7_r4_backup.py"), generator_before, gen_next),
    )
    for backup, previous, next_data in backups:
        if previous != next_data and backup.exists() and backup.read_bytes() != previous:
            raise RuntimeError(f"Backup conflicts: {backup}")

    for backup, previous, next_data in backups:
        if previous != next_data:
            backup.write_bytes(previous)
    for path, data in ((OPERATION, op_next), (GENERATOR_ADAPTER, gen_next)):
        if path.read_bytes() != data:
            path.write_bytes(data)
            print("Updated:", path.name)
    for src, dst in additions:
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print("Added:", dst.name)
    print("R7-R4 installed: shared internal proof-root guard; no ProofStep or query result changes")


if __name__ == "__main__":
    main()
