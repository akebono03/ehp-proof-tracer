from pathlib import Path

import pytest

from phase165_r52_r22_rule_compatibility import FACTORIES, audit, write_report


def _fixture(tmp_path: Path) -> Path:
    parts = []
    for name in FACTORIES:
        parts.append(f'''def {name}():
    return InferenceRule(name="existing", premise_patterns=(PremisePattern(statement_type=A),), match_guard=_guard, conclusion_builder=_result)
''')
    (tmp_path / 'toda_rules.py').write_text('def _guard(premises, bindings):\n    return True\n\ndef _result(premises):\n    return X()\n\n' + '\n'.join(parts), encoding='utf-8')
    (tmp_path / 'phase165_r52_r9_shared_math.py').write_text('def shared_expansion_provider(bridge):\n    def expand(goal):\n        return ()\n    return expand\n', encoding='utf-8')
    return tmp_path


def test_all_five_existing_factories_detected(tmp_path: Path):
    result = audit(_fixture(tmp_path))
    assert result['rule_count_present'] == 5
    assert all(row['premise_patterns'] == [{'statement_type': 'A'}] for row in result['rules'])
    assert all(row['conclusion_builder'] == '_result' for row in result['rules'])


def test_missing_factory_never_classified_as_connected(tmp_path: Path):
    root = _fixture(tmp_path)
    text = (root / 'toda_rules.py').read_text(encoding='utf-8')
    pos = text.index('def ' + FACTORIES[-1] + '(')
    (root / 'toda_rules.py').write_text(text[:pos], encoding='utf-8')
    result = audit(root)
    assert result['rules'][-1]['status'] == 'MISSING_IN_ROOT'
    assert result['rules'][-1]['direct_shared_reference'] is False


def test_audit_does_not_modify_sources(tmp_path: Path):
    root = _fixture(tmp_path)
    original = {p.name: p.read_bytes() for p in root.glob('*.py')}
    result = write_report(root, root / 'report')
    assert (root / 'report' / 'compatibility.json').is_file()
    assert (root / 'report' / 'review.md').is_file()
    assert original == {p.name: p.read_bytes() for p in root.glob('*.py')}
    assert result['full_pytest_run'] is False


def test_missing_production_inputs_fail_closed(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        audit(tmp_path)
