"""Targeted, non-destructive tests of the adapter-removal audit."""
from __future__ import annotations
from pathlib import Path
import ast

from audit import audit_repository


def test_pi43_adapter_no_longer_used_by_active_root_code():
    result = audit_repository(Path(__file__).resolve().parent.parent)
    assert result['status'] == 'REMOVED', result
    assert result['adapter_file_exists'] is False
    assert result['active_root_references'] == []


def test_generic_search_connectors_survive_adapter_removal():
    result = audit_repository(Path(__file__).resolve().parent.parent)
    assert all(result['generic_connectors'].values()), result


def test_removed_adapter_reference_is_detected(tmp_path):
    (tmp_path / 'phase165_r52_r9_shared_math.py').write_text(
        'def shared_expansion_provider():\n'
        '    build_generic_backward_expansion_provider()\n'
        '    reverse_rules_from_witnesses()\n'
        '    generate_seeded_backward_goals()\n', encoding='utf-8')
    (tmp_path / 'other.py').write_text(
        'from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules\n', encoding='utf-8')
    result = audit_repository(tmp_path)
    assert result['status'] == 'REVIEW_REQUIRED'
    assert result['active_root_references']


def test_existing_adapter_file_is_detected(tmp_path):
    (tmp_path / 'phase165_r52_r9_shared_math.py').write_text(
        'def shared_expansion_provider():\n'
        '    build_generic_backward_expansion_provider()\n'
        '    reverse_rules_from_witnesses()\n'
        '    generate_seeded_backward_goals()\n', encoding='utf-8')
    (tmp_path / 'phase165_r52_r23_existing_rule_adapter.py').write_text('pass\n',encoding='utf-8')
    result = audit_repository(tmp_path)
    assert result['status'] == 'REVIEW_REQUIRED'
    assert result['adapter_file_exists'] is True
