import ast
from pathlib import Path

import pytest

from phase165_r27_r56.apply import apply, transform


def test_removes_dead_legacy_import():
    src = 'from toda_calculation_facade import build_standard_toda_report\n\ndef view():\n    return 1\n'
    out, removed, kept = transform(src, frozenset({'toda_calculation_facade'}))
    assert 'toda_calculation_facade' not in out
    assert removed == ('toda_calculation_facade',)
    assert kept == ()
    ast.parse(out)


def test_preserves_live_legacy_import():
    src = 'from toda_calculation_facade import build_standard_toda_report\n\ndef view():\n    return build_standard_toda_report(2, 1)\n'
    out, removed, kept = transform(src, frozenset({'toda_calculation_facade'}))
    assert out == src
    assert removed == ()
    assert kept == ('toda_calculation_facade',)


def test_preserves_mixed_import():
    src = 'from toda_calculation_facade import build_standard_toda_report, other\n\ndef view():\n    return other()\n'
    out, _, kept = transform(src, frozenset({'toda_calculation_facade'}))
    assert out == src
    assert kept == ('toda_calculation_facade',)


def test_no_change_on_second_pass():
    src = 'from repository_element_presentation import unused\n\ndef view():\n    return 1\n'
    out, _, _ = transform(src, frozenset({'repository_element_presentation'}))
    again, removed, kept = transform(out, frozenset({'repository_element_presentation'}))
    assert out == again
    assert removed == kept == ()


def test_real_apply_deletes_unused_and_keeps_used(tmp_path):
    (tmp_path/'web_group_query.py').write_text('from toda_calculation_facade import legacy\n\ndef view():\n    return 3\n')
    (tmp_path/'web_group_proof.py').write_text('from toda_calculation_facade import legacy\n\ndef view():\n    return legacy()\n')
    result = apply(tmp_path)
    assert result['modified_files'] == ['web_group_query.py']
    assert 'legacy()' in (tmp_path/'web_group_proof.py').read_text()
    assert (tmp_path/'phase165_r27_r56_backup/web_group_query.py').exists()
    assert apply(tmp_path)['modified_files'] == []


def test_backup_conflict_is_fail_closed(tmp_path):
    (tmp_path/'web_group_query.py').write_text('from toda_calculation_facade import legacy\n')
    (tmp_path/'web_group_proof.py').write_text('def view():\n    return 1\n')
    folder = tmp_path/'phase165_r27_r56_backup'
    folder.mkdir()
    (folder/'web_group_query.py').write_text('wrong backup')
    with pytest.raises(RuntimeError, match='backup conflict'):
        apply(tmp_path)
    assert (tmp_path/'web_group_query.py').read_text().startswith('from toda_')


def test_preserves_function_body_and_signature():
    src = 'from repository_element_presentation import x\n\ndef view(a: int, *, b: str = "x"):\n    return a, b\n'
    out, _, _ = transform(src, frozenset({'repository_element_presentation'}))
    a, b = ast.parse(src), ast.parse(out)
    assert ast.dump(a.body[-1]) == ast.dump(b.body[-1])
