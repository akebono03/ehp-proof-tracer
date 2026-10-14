from pathlib import Path

from audit import audit, consumer_summary, extract_factory


def test_r25_reads_rule_shapes():
    data = extract_factory('def demo():\n return InferenceRule(premise_patterns=(PremisePattern(statement_type=Relation),),match_guard=g,conclusion_builder=b)\n', 'demo')
    assert data['present']
    assert data['premise_types'] == ['Relation']
    assert data['has_guard'] and data['has_conclusion_builder']


def test_r25_records_missing_factory():
    assert extract_factory('def other():\n return 1\n', 'missing')['present'] is False


def test_r25_finds_old_consumers():
    found = consumer_summary('from r import old\na=old()\n', 'old')
    assert found['factory_calls'] == [2]
    assert found['import_lines'] == [1]


def test_r25_requires_semantic_gate_even_for_same_names(tmp_path: Path):
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'toda_rules.py').write_text('def toda_pi3_2_free_cyclic_generator_inference_rule():\n return InferenceRule(premise_patterns=(PremisePattern(statement_type=Relation),), match_guard=g, conclusion_builder=b)\n')
    (tmp_path / 'phase165_r14_r33_final_group.py').write_text('def reverse_free_cyclic_transport_rule():\n return InferenceRule(premise_patterns=(PremisePattern(statement_type=Relation),), match_guard=g, conclusion_builder=b)\n')
    (tmp_path / 'toda_upstream_bootstrap.py').write_text('x=toda_pi3_2_free_cyclic_generator_inference_rule()\n')
    (tmp_path / 'probes' / 'probe_phase49_capabilities.py').write_text('x=1\n')
    (tmp_path / 'test_phase165_r52_r9_shared_math.py').write_text('def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n pass\n')
    result = audit(tmp_path)
    assert result['premise_type_names_identical']
    assert not result['deletion_approved']
    assert result['old_factory_call_count'] == 1
