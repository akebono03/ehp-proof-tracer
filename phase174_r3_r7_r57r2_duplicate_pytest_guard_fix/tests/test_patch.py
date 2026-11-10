"""R57R2 narrow guard tests: duplicate pytest decorator and R57 pin consistency."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r57r2_duplicate_pytest_guard_fix import install


@pytest.fixture
def reviewed_sources() -> tuple[str, str]:
    path = Path(install.__file__).resolve().parent / 'fixtures'
    return (
        (path / 'R56_TEST_ORIGINAL.py.txt').read_text(encoding='utf-8'),
        (path / 'R57_INSTALL_FULL_BEFORE.py.txt').read_text(encoding='utf-8'),
    )


def test_original_patch_duplicates_parametrization(reviewed_sources) -> None:
    original_test, old_installer = reviewed_sources
    namespace = {'__name__': '_r57r2_old_inst', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(old_installer, str(install.TARGET_INSTALL), 'exec'), namespace)
    defective = namespace['patch_test'](original_test)
    assert install.sha256_text(defective) == install.BEFORE_TEST_SHA
    assert defective.count(install.DOUBLE_PARAM) == 1


def test_corrected_test_has_exactly_one_n_parameterization(reviewed_sources) -> None:
    original_test, old_installer = reviewed_sources
    scope = {'__name__': '_r57r2_old_inst', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(old_installer, str(install.TARGET_INSTALL), 'exec'), scope)
    patched = install.corrected_test(scope['patch_test'](original_test))
    tree = ast.parse(patched)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == 'test_generator_relation_alone_proves_delta_surjectivity')
    assert len(function.decorator_list) == 1
    assert install.sha256_text(patched) == install.AFTER_TEST_SHA


def test_corrected_installer_regenerates_single_marker(reviewed_sources) -> None:
    original_test, old_installer = reviewed_sources
    fixed = install.corrected_installer(old_installer)
    scope = {'__name__': '_r57r2_fixed_inst', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(fixed, str(install.TARGET_INSTALL), 'exec'), scope)
    assert install.sha256_text(fixed) == install.AFTER_INSTALL_SHA
    assert scope['AFTER_SHA256'][scope['R56_TEST']] == install.AFTER_TEST_SHA
    assert scope['patch_test'](original_test).count(install.DOUBLE_PARAM) == 0
    generated = scope['patch_test'](original_test)
    assert install.sha256_text(generated) == install.AFTER_TEST_SHA


def test_source_guard_refuses_modified_or_ambiguous_tests() -> None:
    with pytest.raises(RuntimeError):
        install.corrected_test('def test_something_else(): pass\n')
    with pytest.raises(RuntimeError):
        install.corrected_test(install.DOUBLE_PARAM + '\n' + install.DOUBLE_PARAM)
    with pytest.raises(RuntimeError):
        install.corrected_installer('AFTER_SHA256 = {}')


def test_current_test_and_installer_match_reviewed_final_state() -> None:
    raw_test, test_source, _, _ = install._read_target(install.TARGET_TEST)
    raw_inst, installer_source, _, _ = install._read_target(install.TARGET_INSTALL)
    assert raw_test and raw_inst
    assert install.sha256_text(test_source) == install.AFTER_TEST_SHA
    assert install.sha256_text(installer_source) == install.AFTER_INSTALL_SHA
    assert len(tuple(ast.walk(ast.parse(test_source)))) > 0


def test_no_math_or_renderer_file_is_edited_by_r57r2() -> None:
    changes = install.review()
    assert {target.relative_to(install.ROOT).as_posix() for target, _, _ in changes} == {
        install.TEST_NAME, install.INSTALL_NAME,
    }
    assert all(before == after for _, before, after in changes)


def test_local_dryrun_install_and_idempotency(tmp_path, monkeypatch, reviewed_sources) -> None:
    original_test, old_installer = reviewed_sources
    namespace = {'__name__': '_r57r2_test_setup', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(old_installer, str(install.TARGET_INSTALL), 'exec'), namespace)
    original_installed_test = namespace['patch_test'](original_test)
    test_path = tmp_path / install.TEST_NAME
    installer_path = tmp_path / install.INSTALL_NAME
    test_path.parent.mkdir(parents=True)
    installer_path.parent.mkdir(parents=True)
    test_path.write_text(original_installed_test, encoding='utf-8')
    installer_path.write_text(old_installer, encoding='utf-8')
    monkeypatch.setattr(install, 'ROOT', tmp_path)
    monkeypatch.setattr(install, 'TARGET_TEST', test_path)
    monkeypatch.setattr(install, 'TARGET_INSTALL', installer_path)
    monkeypatch.setattr(install, '_check_repo', lambda: None)
    monkeypatch.setattr(install, '_check_r57_review', lambda _: None)
    install.run(True)
    assert install.sha256_text(test_path.read_text(encoding='utf-8')) == install.BEFORE_TEST_SHA
    install.run(False)
    assert install.sha256_text(test_path.read_text(encoding='utf-8')) == install.AFTER_TEST_SHA
    assert install.sha256_text(installer_path.read_text(encoding='utf-8')) == install.AFTER_INSTALL_SHA
    install.run(False)
    assert all(before == after for _, before, after in install.review())
