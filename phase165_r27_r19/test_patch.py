import ast
from pathlib import Path
from apply import TARGETS, rewrite


def _fixture_source():
    return '''from repository_generator_applicability_facade import (\n  explore_standard_repository_generator_applicability_input,\n)\nfrom repository_generator_applicability_renderer import (\n  render_repository_generator_applicability_compact_markdown,\n)\nrender_repository_generator_applicability_markdown = (\n  render_repository_generator_applicability_compact_markdown\n)\n\ndef _run_explore_proof_command(\n  generator_input: str,\n) -> int:\n  return old_scope(generator_input)\n\ndef _run_explore_applicable_command(\n  generator_input: str,\n  detailed: bool = False,\n) -> int:\n  return old_app(generator_input)\n\ndef _run_show_proof_command(\n  generator_input: str,\n  max_depth: int | None = None,\n) -> int:\n  return old_replay(generator_input)\n\ndef _run_execute_command(\n  generator_input: str,\n  candidate_number: int | None = None,\n) -> int:\n  return old_exec(generator_input)\n\ndef ordinary():\n  return 123\n'''


def test_rewrite_retains_public_signatures_and_other_functions():
    old = ast.parse(_fixture_source())
    new = ast.parse(rewrite(_fixture_source()))
    originals = {x.name: ast.unparse(x.args) for x in old.body if isinstance(x, ast.FunctionDef)}
    changed = {x.name: ast.unparse(x.args) for x in new.body if isinstance(x, ast.FunctionDef)}
    assert originals == changed
    assert 'return 123' in rewrite(_fixture_source())


def test_rewrite_removes_old_calls_and_unused_imports():
    result = rewrite(_fixture_source())
    assert 'old_scope(' not in result
    assert 'old_app(' not in result
    assert 'old_replay(' not in result
    assert 'old_exec(' not in result
    assert 'from repository_generator_applicability_facade import' not in result


def test_rewrite_preserves_distinct_cli_argument_shapes():
    result = rewrite(_fixture_source())
    scope = {}
    parsed = ast.parse(result)
    isolated = ast.Module(body=[node for node in parsed.body if isinstance(node, ast.FunctionDef)], type_ignores=[])
    exec(compile(isolated, "<generated-functions>", "exec"),scope)
    for name,args in [('_run_explore_proof_command',('nu_prime',)),('_run_explore_applicable_command',('nu_prime',True)),('_run_show_proof_command',('nu_prime',2)),('_run_execute_command',('nu_prime',3))]:
        assert scope[name](*args) == 1


def test_repo_cli_legacy_paths_are_disabled_without_touching_group():
    main_py = Path.cwd()/'main.py'
    if not main_py.exists():
        return
    tree=ast.parse(main_py.read_text(encoding='utf-8-sig'))
    funcs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    for name in TARGETS:
        assert name in funcs
        body=funcs[name]
        assert any(isinstance(node,ast.Constant) and node.value==1 for node in ast.walk(body))
        assert not any(isinstance(node,ast.Name) and node.id.startswith('build_standard_repository_generator') for node in ast.walk(body))
    assert '_run_group_proof_command' in funcs
    assert '_run_query_command' in funcs
