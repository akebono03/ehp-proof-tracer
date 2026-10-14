import ast
from pathlib import Path
import pytest
from apply import patch

SOURCE = '''from web_generator_proof import (\n  WebGeneratorProofView,\n  build_standard_web_generator_proof_view,\n)\nfrom web_generator_proof_scope import (\n  WebGeneratorProofScopeView,\n  build_standard_web_generator_proof_scope_view,\n)\nfrom web_generator_applicability import (\n  WebGeneratorApplicabilityView,\n  build_standard_web_generator_applicability_view,\n)\nfrom web_generator_execution import (\n  WebGeneratorExecutionView,\n  build_standard_web_generator_execution_view,\n)\ndef create_app():\n  generator_proof_view: WebGeneratorProofView | None = None\n  generator_execution_view: WebGeneratorExecutionView | None = None\n  generator_proof_scope_view: WebGeneratorProofScopeView | None = None\n  generator_applicability_view: WebGeneratorApplicabilityView | None = None\n  if form_kind == "generator_proof":\n    generator_proof_view = build_standard_web_generator_proof_view("x")\n  elif form_kind == "generator_execution":\n    generator_execution_view = build_standard_web_generator_execution_view("x")\n  elif form_kind == "generator_proof_scope":\n    generator_proof_scope_view = build_standard_web_generator_proof_scope_view("x")\n  elif form_kind == "generator_applicability":\n    generator_applicability_view = build_standard_web_generator_applicability_view("x")\n  else:\n    pass\n  return render_template("index.html",generator_proof_view=generator_proof_view,generator_execution_view=generator_execution_view,generator_proof_scope_view=generator_proof_scope_view,generator_applicability_view=generator_applicability_view)\n'''

def test_all_four_legacy_routes_are_disabled():
    result=patch(SOURCE)
    assert result.count('Legacy generator workflow is disabled')==4
    assert 'build_standard_web_generator_proof_view' not in result
    ast.parse(result)

def test_template_arguments_remain_compatible():
    result=patch(SOURCE)
    assert result.count('=None')==4
    assert 'render_template(' in result

def test_missing_legacy_routes_refuse_partial_patch():
    with pytest.raises(RuntimeError, match='four legacy route branches'):
        patch(SOURCE.replace('"generator_execution"','"not_execution"'))
