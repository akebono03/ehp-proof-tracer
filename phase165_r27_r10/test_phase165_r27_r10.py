import ast
import inspect
from pathlib import Path

import phase165_r52_r3_web_adapter as adapter
import web_group_proof as legacy
import web_group_proof_common as common
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result


def test_shared_types_keep_public_compatibility():
    for name in ('WebGroupProofView', 'WebGroupProofStepView', 'WebGroupProofInlineSegmentView', 'WebGroupProofRenderedLineView'):
        assert getattr(legacy, name) is getattr(common, name)
    assert adapter.WebGroupProofView is common.WebGroupProofView


def test_common_module_never_imports_legacy_proof_builder():
    tree = ast.parse(Path(inspect.getfile(common)).read_text(encoding='utf-8'))
    modules = {node.module for node in tree.body if isinstance(node, ast.ImportFrom)}
    assert 'web_group_proof' not in modules
    assert 'toda_calculation_facade' not in modules
    assert 'standard_production_repository' not in modules
    assert not any(isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == 'build_standard_web_group_proof_view' for node in tree.body)


def test_failed_proof_stays_partial_in_common_web_view():
    result = make_partial_proof_result(n=50, k=7, status=ProofSearchStatus.SEARCH_FAILED, open_goals=('unproved',), diagnostics=('No verified derivation',))
    view = adapter.build_partial_web_group_proof_view(result)
    assert view.partial_result is True
    assert view.theorem is None
    assert view.conclusion_latex == r'\pi_{57}^{50}'
    assert view.rendered_lines
