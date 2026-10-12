"""Phase 164 R7-R8 guarded atomic installer."""
import hashlib
import shutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SPECIAL = ROOT / "phase164_r4_r8_registry_reconstruction.py"
RESOLVER = ROOT / "phase164_r7_statement_resolution.py"
TEST = ROOT / "tests/test_phase164_r7_r8_fixed_literature_resolution.py"
ORIGINAL_SPECIAL_BLOB = "7155229657d510699b5d62f013c723951eaafaa8"
ORIGINAL_RESOLVER_SHA256 = "262399d5c02ffa304f78770cf7fe462df2f53e002da058179df0435de72b7a25"
OLD_BLOCK = '        assertion = registration.bridge.registry.assertion(expected_id)\n        reference = registration.bridge.registry.reference(assertion.reference_id)\n        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT\n                or assertion.content is not binding.step.conclusion\n                or assertion.dependencies\n                or reference.locator != binding.locator\n                or reference.publication_position is not None\n                or assertion.available_after_position is not None):\n            raise ValueError("typed reference content or boundary changed")\n        selected.append(link.step)'
NEW_BLOCK = '        resolved = resolve_registered_statement(\n            registration.bridge,\n            expected_id,\n            expected_conclusion=binding.step.conclusion,\n            confirmed_fixed_step=binding.step,\n            confirmed_source_locator=binding.locator,\n            source_confirmation_recorded=registration.user_source_confirmation_recorded,\n        )\n        if (resolved.assertion.origin is not AssertionOrigin.FIXED_STATEMENT\n                or resolved.proof_link is not link\n                or resolved.reference.locator != binding.locator):\n            raise ValueError("typed reference content or boundary changed")\n        selected.append(resolved.proof_link.step)'
IMPORT_ANCHOR = "from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings\n"
NEW_IMPORT = "from phase164_r7_statement_resolution import resolve_registered_statement\n"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def normalize(data):
    return data.decode("utf-8").replace("\r\n", "\n")


def encode(text, original):
    return text.replace("\n", "\r\n" if b"\r\n" in original else "\n").encode("utf-8")


def main():
    if not SPECIAL.is_file() or not RESOLVER.is_file():
        raise RuntimeError("R7-R8 prerequisites missing")
    old_special = SPECIAL.read_bytes()
    old_resolver = RESOLVER.read_bytes()
    special_text = normalize(old_special)
    if git_blob(old_special) == ORIGINAL_SPECIAL_BLOB:
        if special_text.count(OLD_BLOCK) != 1 or special_text.count(IMPORT_ANCHOR) != 1:
            raise RuntimeError("special literature insertion anchors changed")
        updated_special = encode(special_text.replace(IMPORT_ANCHOR, IMPORT_ANCHOR+NEW_IMPORT, 1).replace(OLD_BLOCK, NEW_BLOCK, 1), old_special)
    elif NEW_BLOCK in special_text and NEW_IMPORT in special_text:
        updated_special = old_special
    else:
        raise RuntimeError("special literature code differs from GitHub baseline")
    updated_resolver = (PACKAGE / "files/phase164_r7_statement_resolution.py").read_bytes()
    if sha256(old_resolver) not in (ORIGINAL_RESOLVER_SHA256, sha256(updated_resolver)):
        raise RuntimeError("local shared resolver differs from R7 baseline")
    test_bytes = (PACKAGE / "files/tests/test_phase164_r7_r8_fixed_literature_resolution.py").read_bytes()
    if TEST.exists() and TEST.read_bytes() != test_bytes:
        raise RuntimeError("existing R7-R8 test differs")
    for file, original in ((SPECIAL, old_special), (RESOLVER, old_resolver)):
        backup = file.with_name(file.stem + ".phase164_r7_r8_backup.py")
        if backup.exists() and backup.read_bytes() != original and file.read_bytes() != (updated_special if file == SPECIAL else updated_resolver):
            raise RuntimeError("conflicting backup: " + str(backup))
    # All validation completed before any mutation.
    for file, original in ((SPECIAL, old_special), (RESOLVER, old_resolver)):
        target = updated_special if file == SPECIAL else updated_resolver
        if original != target:
            backup = file.with_name(file.stem + ".phase164_r7_r8_backup.py")
            if not backup.exists():
                backup.write_bytes(original)
            file.write_bytes(target)
            print("Updated:", file.name)
    TEST.parent.mkdir(parents=True, exist_ok=True)
    TEST.write_bytes(test_bytes)
    print("Added:", TEST.name)
    print("R7-R8 confirmed fixed-literature statement resolution installed; R2 policy unchanged")

if __name__ == "__main__":
    main()
