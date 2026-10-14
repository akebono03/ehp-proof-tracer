from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parent.parent


def test_r36_web_entrypoints_use_typed_search():
    files = {
        'web_generator_proof.py': 'build_standard_web_generator_proof_view',
        'web_generator_proof_scope.py': 'build_standard_web_generator_proof_scope_view',
        'web_generator_applicability.py': 'build_standard_web_generator_applicability_view',
        'web_generator_execution.py': 'build_standard_web_generator_execution_view',
    }
    for file, name in files.items():
        tree = ast.parse((ROOT / file).read_text(encoding='utf-8'))
        fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)
        src = ast.unparse(fn)
        assert 'search_typed_generator_statements' in src
        assert 'build_standard_repository' not in src
        assert 'explore_standard_repository' not in src
        assert 'run_standard_repository' not in src


def test_r36_cli_proof_entrypoints_use_typed_search():
    tree = ast.parse((ROOT / 'main.py').read_text(encoding='utf-8'))
    for name in ('_run_show_proof_command', '_run_explore_proof_command'):
        fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)
        assert 'search_typed_generator_statements' in ast.unparse(fn)


def test_r36_web_views_keep_search_status_fields():
    for file, name in (
        ('web_generator_proof.py', 'WebGeneratorProofView'),
        ('web_generator_proof_scope.py', 'WebGeneratorProofScopeView'),
        ('web_generator_applicability.py', 'WebGeneratorApplicabilityView'),
        ('web_generator_execution.py', 'WebGeneratorExecutionView'),
    ):
        tree = ast.parse((ROOT / file).read_text(encoding='utf-8'))
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name)
        fields = {item.target.id for item in cls.body if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)}
        assert {'search_status', 'diagnostics', 'open_goal_count'} <= fields
