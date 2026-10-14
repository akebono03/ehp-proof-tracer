from pathlib import Path

from phase165_r52_r21_rule_inventory import audit_rule_inventory, write_audit


def test_r21_categorizes_rule_factories_without_importing_production(tmp_path: Path):
    (tmp_path / 'example.py').write_text('''from proof import InferenceRule\ndef first_rule():\n    return InferenceRule(name="first")\ndef unused_rule():\n    return InferenceRule(name="unused")\ndef another():\n    return first_rule()\n''', encoding='utf-8')
    (tmp_path / 'phase165_r52_r9_shared_math.py').write_text('''def shared_expansion_provider():\n    first_rule()\n''', encoding='utf-8')
    result = audit_rule_inventory(tmp_path)
    keyed = {r['function']: r for r in result['rules']}
    assert keyed['first_rule']['status'] == 'DIRECT_SHARED_PROVIDER_REFERENCE'
    assert keyed['unused_rule']['status'] == 'NO_STATIC_CALLERS'


def test_r21_does_not_label_indirect_rules_as_proven_unconnected(tmp_path: Path):
    (tmp_path / 'example.py').write_text('''def old_rule():\n    return InferenceRule(name="old")\ndef wrapper():\n    return old_rule()\n''', encoding='utf-8')
    result = audit_rule_inventory(tmp_path)
    assert result['rules'][0]['status'] == 'OTHER_CALLERS_NO_DIRECT_SHARED_LINK'
    assert 'NOT proof of disconnection' in result['limitations'][1]


def test_r21_emits_json_csv_and_review(tmp_path: Path):
    (tmp_path / 'a.py').write_text('''def r():\n    return InferenceRule(name="quotient")\n''', encoding='utf-8')
    output = tmp_path / 'audit'
    result = write_audit(tmp_path, output)
    assert result['rule_factory_calls'] == 1
    assert all((output / name).exists() for name in ('inventory.json', 'rules.csv', 'review.md'))
    assert result['full_pytest_run'] is False


def test_r21_skips_tests_and_backup_paths(tmp_path: Path):
    (tmp_path / 'test_x.py').write_text('''def t():\n    InferenceRule(name="test")\n''', encoding='utf-8')
    folder = tmp_path / 'phase159_backup'
    folder.mkdir()
    (folder / 'old.py').write_text('''def t():\n    InferenceRule(name="backup")\n''', encoding='utf-8')
    assert audit_rule_inventory(tmp_path)['rule_factory_calls'] == 0
