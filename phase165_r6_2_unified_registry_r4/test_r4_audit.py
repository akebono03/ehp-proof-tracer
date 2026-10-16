from types import SimpleNamespace
from pathlib import Path
import pytest
from phase165_r6_2_unified_registry_r4.r4_audit import unique_goals, evaluate_provider, check_adapter_removed, markdown


def test_unique_goals_removes_duplicates():
    assert unique_goals([SimpleNamespace(content=1), SimpleNamespace(content=1), SimpleNamespace(content=2)], 5) == (1, 2)


def test_unique_goals_limit():
    assert unique_goals([SimpleNamespace(content=1), SimpleNamespace(content=2)], 1) == (1,)


def test_unique_goals_invalid_limit():
    with pytest.raises(ValueError):
        unique_goals([], 0)


def test_evaluate_provider_proposals():
    result = evaluate_provider(lambda x: (x,) if x == 1 else (), (1, 2))
    assert result['goals_proposed'] == 1
    assert result['expansions'] == 1


def test_evaluate_provider_catches_errors():
    def broken(goal):
        raise ValueError('bad goal')
    result = evaluate_provider(broken, (1,))
    assert result['errors'] == {'ValueError': 1}
    assert result['goals_proposed'] == 0


def test_evaluate_provider_rejects_wrong_return():
    result = evaluate_provider(lambda goal: [], (1,))
    assert result['errors'] == {'TypeError': 1}


def test_adapter_guard(tmp_path):
    file = tmp_path / 'phase165_r52_r9_shared_math.py'
    file.write_text('def generic_provider(): pass\n', encoding='utf-8')
    assert check_adapter_removed(tmp_path)
    file.write_text('expand_existing_pi43_rules()', encoding='utf-8')
    assert not check_adapter_removed(tmp_path)


def test_markdown_report():
    text = markdown({'status': 'APPLICABILITY_AUDITED', 'goals_examined': 2,
                     'r1_registered_rules': 1, 'registered_providers': 0,
                     'provider_results': [], 'limitations': []})
    assert 'APPLICABILITY_AUDITED' in text
    assert '証明成立の検証: 0' in text
