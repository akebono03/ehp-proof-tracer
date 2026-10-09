import pytest

from phase162_r4_b3_renderer_audit import audit_one, write_audit


@pytest.mark.parametrize('n', [4, 5])
def test_phase162_r4_b3_derived_replay_and_reference_audit(n):
    record = audit_one(n)
    assert record['old_root_is_derived_root'] is False
    assert record['derived_root_rule'] is not None
    assert record['derived_root_premises'] == 3
    assert any(entry['locator'] == '(4.5)' for entry in record['derived_references_before_filtering'])
    assert all(not entry['contains_root'] for entry in record['derived_references_before_filtering'])


def test_phase162_r4_b3_audit_writes_complete_comparison(tmp_path):
    records = write_audit(tmp_path)
    assert [record['target'] for record in records] == ['pi_5^4', 'pi_6^5']
    text = (tmp_path / 'comparison.md').read_text(encoding='utf-8')
    assert '旧root' in text
    assert '新しい導出root' in text
    assert (tmp_path / 'audit.json').is_file()
