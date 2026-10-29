"""Source-independent R2E-R2 patch integrity and rollback-contract tests."""
from __future__ import annotations

import ast

import pytest

from phase171_r2e_toda53_double_source import install


def fixture_original() -> str:
    updated_function = install.FULL_FUNCTION.read_text(encoding="utf-8")
    with_added = install.ANCHOR + "\n" + install.ADDITION
    assert updated_function.count(with_added) == 1
    assert updated_function.count(install.POSITION_NEW) == 1
    original = updated_function.replace(with_added, install.ANCHOR)
    original = original.replace(install.POSITION_NEW, install.POSITION_OLD)
    return original + "\n\ndef shared_expansion_provider(*args):\n    return ()\n"


def fixture_test_original() -> str:
    updated = install.FULL_TEST.read_text(encoding="utf-8")
    assert updated.count(install.TEST_NEW) == 1
    assert updated.count(install.TEST_PROOF_NEW) == 1
    return updated.replace(install.TEST_NEW, install.TEST_OLD).replace(
        install.TEST_PROOF_NEW, install.TEST_PROOF_OLD
    )


def test_proposed_source_has_exact_full_replacement_and_preserves_other_function():
    original = fixture_original()
    updated = install.proposed_source(original.encode("utf-8")).decode("utf-8")
    assert install.ADDITION in updated
    assert updated.count(install.ADDITION) == 1
    assert install.POSITION_NEW in updated
    assert install.POSITION_OLD not in updated
    assert updated.endswith("def shared_expansion_provider(*args):\n    return ()\n")
    assert updated.replace(install.ANCHOR + "\n" + install.ADDITION, install.ANCHOR).replace(
        install.POSITION_NEW, install.POSITION_OLD
    ) == original
    ast.parse(updated)


def test_proposed_source_preserves_crlf():
    original = fixture_original().replace("\n", "\r\n")
    updated = install.proposed_source(original.encode("utf-8")).decode("utf-8")
    assert "\r\n" in updated
    assert "\n" not in updated.replace("\r\n", "")
    assert install.ADDITION.replace("\n", "\r\n") in updated
    assert install.POSITION_NEW.replace("\n", "\r\n") in updated


def test_proposed_source_rejects_missing_anchor():
    with pytest.raises(RuntimeError, match="source anchor not unique"):
        install.proposed_source(b'def build_shared_typed_bridge():\n    pass\n')


def test_proposed_source_rejects_duplicated_anchor():
    source = fixture_original().replace(
        install.ANCHOR, install.ANCHOR + "\n" + install.ANCHOR
    )
    with pytest.raises(RuntimeError, match="source anchor not unique"):
        install.proposed_source(source.encode("utf-8"))


def test_proposed_source_rejects_unreviewed_function_changes():
    source = fixture_original().replace(
        "if not isinstance(source, RegistryBridgeResult):", "if source is None:"
    )
    with pytest.raises(RuntimeError, match="differs from reviewed"):
        install.proposed_source(source.encode("utf-8"))


def test_proposed_source_rejects_missing_position_anchor():
    source = fixture_original().replace(install.POSITION_OLD, "    return ordered")
    with pytest.raises(RuntimeError, match="position anchor not unique"):
        install.proposed_source(source.encode("utf-8"))


def test_proposed_test_changes_only_legacy_heading_assertion():
    original = fixture_test_original()
    updated = install.proposed_test(original.encode("utf-8")).decode("utf-8")
    assert install.TEST_NEW in updated
    assert install.TEST_OLD not in updated
    assert install.TEST_PROOF_NEW in updated
    assert install.TEST_PROOF_OLD not in updated
    assert updated.replace(install.TEST_NEW, install.TEST_OLD).replace(
        install.TEST_PROOF_NEW, install.TEST_PROOF_OLD
    ) == original
    ast.parse(updated)


def test_proposed_test_preserves_crlf():
    original = fixture_test_original().replace("\n", "\r\n")
    updated = install.proposed_test(original.encode("utf-8")).decode("utf-8")
    assert "\n" not in updated.replace("\r\n", "")
    assert install.TEST_NEW.replace("\n", "\r\n") in updated
    assert install.TEST_PROOF_NEW.replace("\n", "\r\n") in updated


def test_proposed_test_rejects_missing_anchor():
    with pytest.raises(RuntimeError, match="test anchor not unique"):
        install.proposed_test(b'def test_old():\n    pass\n')


def test_proposed_test_rejects_duplicate_anchor():
    source = fixture_test_original().replace(
        install.TEST_OLD, install.TEST_OLD + "\n" + install.TEST_OLD
    )
    with pytest.raises(RuntimeError, match="test anchor not unique"):
        install.proposed_test(source.encode("utf-8"))


def test_reviewed_pi32_function_has_no_blank_line_after_import():
    old = install.TEST_PROOF_OLD
    new = install.TEST_PROOF_NEW
    original_layout = (
        'def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n'
        '    from hopf_facts import ETA_2\n'
        '    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))\n'
    )
    revised_layout = (
        'def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n'
        '    from hopf_facts import ETA_2\n'
        '    bridge = build_shared_typed_bridge()\n'
    )
    assert old.startswith(original_layout)
    assert new.startswith(revised_layout)
    assert old.count('    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))') == 1
    assert new.count('    bridge = build_shared_typed_bridge()') == 1
    assert '\n\n    bridge = build_shared_typed_bridge' not in old
    assert '\n\n    bridge = build_shared_typed_bridge' not in new


def test_reviewed_pi32_full_function_is_the_expected_replacement():
    test = install.FULL_TEST.read_text(encoding='utf-8')
    assert test.count(install.TEST_PROOF_NEW) == 1
    original = fixture_test_original()
    assert original.count(install.TEST_PROOF_OLD) == 1
    updated = install.proposed_test(original.encode('utf-8')).decode('utf-8')
    start = updated.index('def test_r9_pi32_regenerated_by_shared_mathematical_expansion():')
    end = updated.index('def test_r9_pi43_is_a_real_typed_goal_even_if_not_proved():', start)
    assert updated[start:end].strip() == install.TEST_PROOF_NEW.strip()
    assert original[:start] == updated[:start]


def test_reviewed_original_test_matches_exact_git_blob():
    from hashlib import sha1

    normalized_original = fixture_test_original()
    original_bytes = normalized_original.replace('\n', '\r\n').encode('utf-8')
    blob_header = b'blob ' + str(len(original_bytes)).encode('ascii') + b'\0'
    assert sha1(blob_header + original_bytes).hexdigest() == install.EXPECTED_TEST_BLOB
    assert install.EXPECTED_TEST_BLOB == 'c6dcfb3cda9c9115fb802f4a1b2141e0502506bd'


def test_pi32_complete_requires_full_production_sources():
    full = install.FULL_TEST.read_text(encoding="utf-8")
    assert full.count(install.TEST_PROOF_NEW) == 1
    assert "bridge = build_shared_typed_bridge()" in install.TEST_PROOF_NEW
    assert "sources=(_adopted_source(),)" in install.TEST_PROOF_OLD
    assert "assert result.status is ProofSearchStatus.COMPLETE" in install.TEST_PROOF_NEW
    assert "assert any(step.rule is ProofRule.INFERENCE" in install.TEST_PROOF_NEW


def test_proposed_test_rejects_outdated_pi32_proof_anchor():
    source = fixture_test_original().replace(
        install.TEST_PROOF_OLD,
        install.TEST_PROOF_OLD.replace("COMPLETE", "PARTIAL"),
    )
    with pytest.raises(RuntimeError, match="pi32 proof test anchor not unique"):
        install.proposed_test(source.encode("utf-8"))


def test_proposed_test_changes_no_other_mathematical_assertions():
    source = fixture_test_original()
    patched = install.proposed_test(source.encode("utf-8")).decode("utf-8")
    assert "assert result.status is ProofSearchStatus.COMPLETE" in patched
    assert "assert result.conclusion == Relation(TodaPrimaryGroup(3, 2)" in patched
    assert "assert any(step.rule is ProofRule.INFERENCE" in patched
    assert "assert result.status in (ProofSearchStatus.SEARCH_FAILED" in patched


def test_source_and_functions_are_syntactically_valid():
    contents = (
        install.PAYLOAD.read_text(encoding="utf-8"),
        install.FULL_FUNCTION.read_text(encoding="utf-8"),
        install.FULL_TEST.read_text(encoding="utf-8"),
    )
    for content in contents:
        ast.parse(content)


def test_patch_does_not_change_existing_imports():
    original = fixture_original()
    updated = install.proposed_source(original.encode("utf-8")).decode("utf-8")
    before = ast.parse(original).body[0]
    after = ast.parse(updated).body[0]
    assert isinstance(before, ast.FunctionDef)
    assert isinstance(after, ast.FunctionDef)
    assert before.name == after.name == "build_shared_typed_bridge"
    assert ast.dump(after.args) == ast.dump(before.args)


def test_position_binding_changes_only_explicit_source_mode():
    updated = install.FULL_FUNCTION.read_text(encoding="utf-8")
    assert updated.count("    if default_sources:\n        from phase166_r3p_position_binding") == 1
    assert updated.count("    return ordered") == 1
    assert updated.index("    if default_sources:\n        from phase166_r3p_position_binding") < updated.index("    return ordered")


def test_apply_and_restore_are_byte_exact_in_temporary_checkout(tmp_path, monkeypatch):
    from pathlib import Path

    source = tmp_path / "phase165_r52_r9_shared_math.py"
    focused = tmp_path / "test_phase165_r52_r9_shared_math.py"
    module = tmp_path / "phase171_r2e_toda53_double_reference.py"
    backup = tmp_path / "backup"
    original_source = fixture_original().replace("\n", "\r\n").encode("utf-8")
    original_test = fixture_test_original().replace("\n", "\r\n").encode("utf-8")
    source.write_bytes(original_source)
    focused.write_bytes(original_test)
    monkeypatch.setattr(install, "TARGET", source)
    monkeypatch.setattr(install, "EXISTING_TEST", focused)
    monkeypatch.setattr(install, "NEW_MODULE", module)
    monkeypatch.setattr(install, "BACKUP", backup)
    monkeypatch.setattr(install, "verify_checkout", lambda: None)

    install.apply(dry_run=True)
    assert source.read_bytes() == original_source
    assert focused.read_bytes() == original_test
    assert not module.exists()
    install.apply()
    assert source.read_bytes() != original_source
    assert focused.read_bytes() != original_test
    assert module.read_bytes() == install.PAYLOAD.read_bytes()
    assert (backup / "state.json").is_file()
    install.restore()
    assert source.read_bytes() == original_source
    assert focused.read_bytes() == original_test
    assert not module.exists()
    assert not (backup / "state.json").exists()


def test_restore_refuses_modified_patched_test(tmp_path, monkeypatch):
    source = tmp_path / "phase165_r52_r9_shared_math.py"
    focused = tmp_path / "test_phase165_r52_r9_shared_math.py"
    module = tmp_path / "phase171_r2e_toda53_double_reference.py"
    backup = tmp_path / "backup"
    source.write_bytes(fixture_original().encode("utf-8"))
    focused.write_bytes(fixture_test_original().encode("utf-8"))
    monkeypatch.setattr(install, "TARGET", source)
    monkeypatch.setattr(install, "EXISTING_TEST", focused)
    monkeypatch.setattr(install, "NEW_MODULE", module)
    monkeypatch.setattr(install, "BACKUP", backup)
    monkeypatch.setattr(install, "verify_checkout", lambda: None)
    install.apply()
    focused.write_bytes(focused.read_bytes() + b"# modified\n")
    with pytest.raises(RuntimeError, match="refusing to overwrite"):
        install.restore()
