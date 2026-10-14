from pathlib import Path

import pytest

from apply import TARGETS, active_imports, apply, replace_legacy_candidate_helper


SAMPLE = '''from __future__ import annotations
from dataclasses import dataclass

@dataclass
class LiteratureComponentInput:
    locator: str

def register_prop51_prop53_literature_statements(base, inputs):
    return base

def existing_prop51_prop53_candidates() -> tuple[LiteratureComponentInput, ...]:
    from toda_prop56_zero_bootstrap import _build_prop51_step
    return (LiteratureComponentInput(str(_build_prop51_step())),)
'''


def make_fixture(root: Path):
    (root / 'phase163_r4_r12_literature_registration.py').write_text(SAMPLE, encoding='utf-8')
    for filename in TARGETS:
        (root / filename).write_text('VALUE = 1\n', encoding='utf-8')


def test_r29_candidate_retirement_preserves_registration_api():
    updated, changed = replace_legacy_candidate_helper(SAMPLE)
    assert changed
    assert 'def register_prop51_prop53_literature_statements' in updated
    assert '_build_prop51_step' not in updated
    assert 'RuntimeError' in updated
    assert replace_legacy_candidate_helper(updated) == (updated, False)


def test_r29_removal_and_backup(tmp_path):
    make_fixture(tmp_path)
    result = apply(tmp_path)
    assert result['status'] == 'REMOVED'
    assert set(result['deleted']) == set(TARGETS)
    for file in TARGETS:
        assert not (tmp_path / file).exists()
        assert (tmp_path / 'phase165_r27_r29_removed_backup' / file).exists()
    assert 'register_prop51_prop53_literature_statements' in (tmp_path / 'phase163_r4_r12_literature_registration.py').read_text()


def test_r29_reentrant(tmp_path):
    make_fixture(tmp_path)
    apply(tmp_path)
    assert apply(tmp_path)['status'] == 'ALREADY_REMOVED'


def test_r29_blocked_import_atomic(tmp_path):
    make_fixture(tmp_path)
    (tmp_path / 'caller.py').write_text('from toda_midstream_bootstrap import foo\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='Active imports found'):
        apply(tmp_path)
    assert (tmp_path / TARGETS[0]).exists()
    assert '_build_prop51_step' in (tmp_path / 'phase163_r4_r12_literature_registration.py').read_text()


def test_r29_local_import_audit(tmp_path):
    make_fixture(tmp_path)
    (tmp_path / 'another.py').write_text('def f():\n    import toda_phase65_bootstrap\n', encoding='utf-8')
    assert active_imports(tmp_path, replacement=replace_legacy_candidate_helper(SAMPLE)[0]) == [{'file':'another.py','line':2,'module':'toda_phase65_bootstrap'}]


def test_r29_preserve_unrelated_modules(tmp_path):
    make_fixture(tmp_path)
    (tmp_path / 'unified_statement_registry.py').write_text('KEEP = True\n', encoding='utf-8')
    apply(tmp_path)
    assert (tmp_path / 'unified_statement_registry.py').read_text() == 'KEEP = True\n'
