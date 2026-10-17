from pathlib import Path

import pytest

from r2_audit import analyze, markdown, required_parameters, write_reports
import ast


def test_required_parameter_modes() -> None:
    tree = ast.parse('def f(a: int, /, b: str, c=1, *, d: bool, e=False, **kwargs):\n    pass\n')
    found = required_parameters(tree.body[0])
    assert [(x['name'], x['kind']) for x in found] == [
        ('a', 'POSITIONAL_ONLY'), ('b', 'POSITIONAL_OR_KEYWORD'), ('d', 'KEYWORD_ONLY')
    ]


def _root(tmp_path: Path) -> Path:
    (tmp_path / 'sample_rules.py').write_text('from proof import InferenceRule\n'
        'def a_inference_rule(witness: object):\n    return InferenceRule("a")\n'
        'def b_inference_rule():\n    return InferenceRule("b")\n', encoding='utf-8')
    return tmp_path


def test_only_required_factories_are_inventoried(tmp_path: Path) -> None:
    from r2_audit import inspect_factory_sources
    rows = inspect_factory_sources(_root(tmp_path), ('sample_rules',))
    assert [r['rule_id'] for r in rows] == ['sample_rules.a_inference_rule']
    assert rows[0]['registration'] == 'REQUIRES_EXPLICIT_TYPED_ARGUMENTS'


def test_reports_remain_uncertified(tmp_path: Path) -> None:
    report = analyze(_root(tmp_path), modules=('sample_rules',))
    assert report['rule_count'] == 1
    assert report['rules'][0]['source_witness_required'] == 'UNKNOWN_REQUIRES_REVIEW'
    assert report['rules'][0]['certification'] == 'NOT_CERTIFIED'
    assert report['registration_policy']['no_automatic_witness_synthesis']


def test_markdown_does_not_certify_rules(tmp_path: Path) -> None:
    output = markdown(analyze(_root(tmp_path), modules=('sample_rules',)))
    assert 'sample_rules.a_inference_rule' in output
    assert 'EXPLICIT_ONLY' in output


def test_missing_source_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        analyze(tmp_path, modules=('missing_rules',))


def test_reports_do_not_modify_source(tmp_path: Path) -> None:
    root = _root(tmp_path)
    before = (root / 'sample_rules.py').read_bytes()
    # Test isolated module selection through analyze; production write uses nine modules.
    analyze(root, modules=('sample_rules',))
    assert (root / 'sample_rules.py').read_bytes() == before
