from pathlib import Path

from inventory import audit, markdown_report


def test_r8_factory_and_other_factory_distinguished(tmp_path: Path):
    (tmp_path / 'ehp_rules.py').write_text(
        'from proof import InferenceRule\n'
        'def zero_inference_rule():\n    return InferenceRule(name="x")\n'
        'def input_inference_rule(step):\n    return InferenceRule(name="y")\n', encoding='utf-8'
    )
    report = audit(tmp_path)
    records = {item['function']: item for item in report['definitions']}
    assert records['zero_inference_rule']['r8_factory_eligible_by_ast']
    assert not records['input_inference_rule']['r8_factory_eligible_by_ast']


def test_connection_and_missing_files_fail_closed(tmp_path: Path):
    report = audit(tmp_path)
    assert not report['connections']['paths']['seeded_witness']['evidence']
    assert not report['connections']['paths']['pi43_adapter']['evidence']
    assert report['summary']['runtime_usable_rules_verified'] == 0


def test_static_connections_are_not_claimed_to_be_runtime_proofs(tmp_path: Path):
    (tmp_path / 'phase165_r52_r9_shared_math.py').write_text(
        'def shared_expansion_provider():\n'
        '    generate_seeded_backward_goals()\n'
        '    reverse_rules_from_witnesses()\n', encoding='utf-8'
    )
    report = audit(tmp_path)
    assert report['connections']['paths']['seeded_witness']['evidence']
    assert report['connections']['paths']['verified_witness']['evidence']
    assert report['summary']['runtime_usable_rules_verified'] == 0
    assert '未実施' in markdown_report(report)


def test_does_not_change_source_files(tmp_path: Path):
    path = tmp_path / 'hopf_rules.py'
    path.write_text('def x_inference_rule():\n    return InferenceRule(name="x")\n', encoding='utf-8')
    before = path.read_bytes()
    audit(tmp_path)
    assert path.read_bytes() == before


def test_test_function_inventory(tmp_path: Path):
    directory = tmp_path / 'tests'
    directory.mkdir()
    (directory / 'test_rules.py').write_text('def test_example():\n    assert True\n', encoding='utf-8')
    report = audit(tmp_path)
    assert report['summary']['test_functions_discovered'] == 1
