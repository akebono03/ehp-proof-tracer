from pathlib import Path
from r6_audit import TARGETS, audit, markdown, source_connection, source_info


def test_four_adapter_branches():
    assert len(TARGETS) == 4
    assert len({name for _, _, name in TARGETS}) == 4


def test_missing_source_fails_closed(tmp_path: Path):
    info = source_info(tmp_path, 'absent', 'factory')
    assert info['source_found'] is False
    assert info['function_found'] is False


def test_ast_detects_source_and_constant_dimensions(tmp_path: Path):
    (tmp_path/'example.py').write_text('def target_rule():\n    return TodaPrimaryGroup(4, 3)\n',encoding='utf-8')
    info = source_info(tmp_path, 'example', 'target_rule')
    assert info['hardcoded_dimensions'] == [[4, 3]]


def test_missing_adapter_is_not_claimed_connected(tmp_path: Path):
    result=source_connection(tmp_path)
    assert result['adapter_found'] is False
    assert result['adapter_provider_referenced'] is False


def test_shared_adapter_reference(tmp_path: Path):
    (tmp_path/'phase165_r52_r9_shared_math.py').write_text('def shared_expansion_provider():\n    return expand_existing_pi43_rules\n', encoding='utf-8')
    assert source_connection(tmp_path)['adapter_provider_referenced'] is True


def test_report_keeps_no_proof_claim(tmp_path: Path):
    data=audit(tmp_path)
    assert data['counts']['generic_replacements_verified'] == 0
    assert data['counts']['proofs_verified'] == 0
    assert '未実証' in markdown(data)
