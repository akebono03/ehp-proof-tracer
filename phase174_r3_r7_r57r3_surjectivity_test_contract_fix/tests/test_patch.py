"""R57R3: strict regression of one-premise matcher test and installer pin."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r57r3_surjectivity_test_contract_fix import install


@pytest.fixture
def sources() -> tuple[str, str, str, str, str]:
    root = Path(install.__file__).resolve().parent / 'fixtures'
    return tuple((root / filename).read_text(encoding='utf-8') for filename in (
        'R56_TEST_FULL_BEFORE.py.txt',
        'R56_TEST_FULL_AFTER.py.txt',
        'R57_INSTALL_FULL_BEFORE.py.txt',
        'R57_INSTALL_FULL_AFTER.py.txt',
        'R56_TEST_ORIGINAL.py.txt',
    ))


def test_reviewed_inputs_match_independent_pins(sources) -> None:
    old_test, new_test, old_inst, new_inst, original = sources
    assert install.sha256_text(old_test) == install.BEFORE_TEST_SHA
    assert install.sha256_text(new_test) == install.AFTER_TEST_SHA
    assert install.sha256_text(old_inst) == install.BEFORE_INSTALL_SHA
    assert install.sha256_text(new_inst) == install.AFTER_INSTALL_SHA
    assert ast.parse(original)


def test_test_function_replacement_is_only_functional_change(sources) -> None:
    old_test, new_test, _, _, _ = sources
    assert install.corrected_test(old_test) == new_test
    old_tree, new_tree = ast.parse(old_test), ast.parse(new_test)
    old_names = [node.name for node in old_tree.body if isinstance(node, ast.FunctionDef)]
    new_names = [node.name for node in new_tree.body if isinstance(node, ast.FunctionDef)]
    assert old_names == new_names
    assert new_test.count('assert matches[0].premises == (valid_relation,)') == 1
    assert new_test.count('assert derived.premises == (valid_relation,)') == 1
    assert 'rule, (_test_step(relation), _test_step(theorem))' not in new_test


def test_new_expected_behavior_requires_valid_group_not_unrelated_fact(sources) -> None:
    _, new_test, _, _, _ = sources
    fn = next(node for node in ast.parse(new_test).body
              if isinstance(node, ast.FunctionDef)
              and node.name == install.TEST_FUNCTION)
    body = ast.get_source_segment(new_test, fn)
    assert 'find_inference_matches_for_rule(rule, ()) == ()' in body
    assert 'find_inference_matches_for_rule(rule, (_test_step(wrong),)) == ()' in body
    assert 'find_inference_matches_for_rule(rule, (_test_step(theorem),)) == ()' in body
    assert 'assert len(matches) == 1' in body
    assert 'assert derived.conclusion == goal' in body


def test_installer_template_and_sha_are_consistent(sources) -> None:
    _, new_test, old_inst, new_inst, original = sources
    assert install.corrected_installer(old_inst) == new_inst
    scope = {'__name__': '_r57r3_test_installer', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(new_inst, str(install.TARGET_INSTALL), 'exec'), scope)
    assert scope['patch_test'](original) == new_test
    assert scope['AFTER_SHA256'][scope['R56_TEST']] == install.AFTER_TEST_SHA


def test_guard_rejects_unreviewed_or_ambiguous_source() -> None:
    with pytest.raises((RuntimeError, SyntaxError, AssertionError)):
        install.corrected_test('def unrelated():\n    return True\n')
    with pytest.raises(RuntimeError):
        install.corrected_installer('NEW_TEST3 = "missing reviewed anchors"\n')


def test_mocked_dryrun_install_and_idempotency(tmp_path, monkeypatch, sources) -> None:
    old_test, new_test, old_inst, new_inst, _ = sources
    test = tmp_path / install.TEST_NAME
    installer = tmp_path / install.INSTALL_NAME
    test.parent.mkdir(parents=True)
    installer.parent.mkdir(parents=True)
    test.write_text(old_test, encoding='utf-8')
    installer.write_text(old_inst, encoding='utf-8')
    monkeypatch.setattr(install, 'ROOT', tmp_path)
    monkeypatch.setattr(install, 'TARGET_TEST', test)
    monkeypatch.setattr(install, 'TARGET_INSTALL', installer)
    monkeypatch.setattr(install, '_check_repo', lambda: None)
    monkeypatch.setattr(install, '_check_r57_review', lambda source: None)
    install.run(True)
    assert test.read_text(encoding='utf-8') == old_test
    assert installer.read_text(encoding='utf-8') == old_inst
    install.run(False)
    assert test.read_text(encoding='utf-8') == new_test
    assert installer.read_text(encoding='utf-8') == new_inst
    install.run(False)
    assert all(before == after for _, before, after in install.review())


def test_no_mathematical_or_renderer_files_appear_as_patch_targets(sources, monkeypatch, tmp_path) -> None:
    old_test, _, old_inst, _, _ = sources
    test = tmp_path / install.TEST_NAME
    installer = tmp_path / install.INSTALL_NAME
    test.parent.mkdir(parents=True)
    installer.parent.mkdir(parents=True)
    test.write_text(old_test, encoding='utf-8')
    installer.write_text(old_inst, encoding='utf-8')
    monkeypatch.setattr(install, 'ROOT', tmp_path)
    monkeypatch.setattr(install, 'TARGET_TEST', test)
    monkeypatch.setattr(install, 'TARGET_INSTALL', installer)
    monkeypatch.setattr(install, '_check_repo', lambda: None)
    monkeypatch.setattr(install, '_check_r57_review', lambda source: None)
    targets = {path.relative_to(tmp_path).as_posix() for path, _, _ in install.review()}
    assert targets == {install.TEST_NAME, install.INSTALL_NAME}


def test_actual_installed_state_matches_pins_if_repo_available() -> None:
    if not (install.ROOT / '.git').exists():
        pytest.skip('runtime project repository is required')
    test, source, _, _ = install._read(install.TARGET_TEST)
    installer, source_installer, _, _ = install._read(install.TARGET_INSTALL)
    assert test and installer
    assert install.sha256_text(source) == install.AFTER_TEST_SHA
    assert install.sha256_text(source_installer) == install.AFTER_INSTALL_SHA
    assert all(before == after for _, before, after in install.review())
