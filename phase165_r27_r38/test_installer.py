import ast
from pathlib import Path
import pytest
from apply import replace_function, prune_unused_repository_imports, dependency_graph, prepare


def test_r38_replace_function_keeps_other_methods():
    before = 'def foo():\n    return 1\n\ndef bar():\n    return 2\n'
    after = replace_function(before, 'foo', 'def foo():\n    return 3\n')
    module = ast.parse(after)
    assert len(module.body) == 2
    assert 'return 3' in after and 'return 2' in after


def test_r38_replace_function_rejects_missing():
    with pytest.raises(RuntimeError):
        replace_function('x=1\n', 'foo', 'def foo():\n    return 1\n')


def test_r38_prunes_old_query_imports():
    src = 'from repository_operation_query_facade import query_standard_repository_operation_input\nx=1\n'
    out, removed = prune_unused_repository_imports(src)
    assert 'repository_operation_query_facade' not in out
    assert len(removed) == 1


def test_r38_preserves_used_repository_import():
    src = 'from repository_x import used, unused\nprint(used)\n'
    out, removed = prune_unused_repository_imports(src)
    assert 'from repository_x import used' in out
    assert removed == ['repository_x.unused']


def test_r38_pruning_preserves_syntax():
    src = 'from repository_x import (\n a,\n b,\n)\nprint(b)\n'
    out, _ = prune_unused_repository_imports(src)
    ast.parse(out)
    assert 'import b' in out


def test_r38_dependency_removes_disconnected_cycle(tmp_path):
    (tmp_path / 'main.py').write_text('x = 1\n')
    (tmp_path / 'repository_a.py').write_text('import repository_b\n')
    (tmp_path / 'repository_b.py').write_text('import repository_a\n')
    assert dependency_graph(tmp_path, {})['deletable'] == ['repository_a', 'repository_b']


def test_r38_dependency_keeps_reachable(tmp_path):
    (tmp_path / 'main.py').write_text('import repository_a\n')
    (tmp_path / 'repository_a.py').write_text('import repository_b\n')
    (tmp_path / 'repository_b.py').write_text('x = 1\n')
    assert dependency_graph(tmp_path, {})['deletable'] == []


def test_r38_prepared_entrypoints_do_not_call_legacy(tmp_path):
    main = 'def _run_query_command(query_input):\n return 0\ndef _run_query_proof_command(query_input, fact_number=None, max_depth=None):\n return 0\n'
    web = 'def build_standard_web_operation_query_proof_view(query_input, fact_number, max_depth=1):\n return None\n'
    (tmp_path / 'main.py').write_text(main)
    (tmp_path / 'web_operation_query_proof.py').write_text(web)
    changes, report = prepare(tmp_path)
    for content in changes.values():
        assert 'query_standard_repository_operation_input' not in content
        assert 'build_repository_operation_query_proof_replay(' not in content
    assert len(report['modified_files']) == 2


def test_r38_web_proof_validates_inputs_before_search():
    module = ast.parse(__import__('apply').WEB_PROOF)
    assert isinstance(module.body[0], ast.FunctionDef)
    assert 'fact_number <= 0' in __import__('apply').WEB_PROOF


def test_r38_no_fake_execution_in_migrated_commands():
    from apply import QUERY, QUERY_PROOF
    assert 'reconstruct_registered_goal' not in QUERY
    assert 'search_typed_operation_statements' in QUERY_PROOF
    assert 'build_standard_production_proof_repository' not in QUERY_PROOF
