import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from apply import transform


def sample():
    return '''from repository_proof_scope import (\n  build_repository_proof_scope,\n)\nfrom standard_production_repository import (\n  build_standard_production_proof_repository,\n)\nclass InferenceRuleCatalog: pass\nclass InferenceRuleCatalogEntry: pass\ndef build_standard_production_applicability_catalog() -> InferenceRuleCatalog:\n  repository = build_standard_production_proof_repository()\n  scope = build_repository_proof_scope(repository)\n  return scope\n_original = build_standard_production_applicability_catalog\ndef build_standard_production_applicability_catalog():\n  return _original()\n'''


def test_replace_only_base():
    s = transform(sample())
    assert 'discover_inference_rules()' in s
    assert 'build_repository_proof_scope' not in s
    assert '_original = build_standard_production_applicability_catalog' in s


def test_ast_valid():
    ast.parse(transform(sample()))


def test_idempotence():
    s = transform(sample())
    assert transform(s) == s


def test_mismatch_fails():
    x = sample().replace('scope = build_repository_proof_scope(repository)', 'scope = None')
    try:
        transform(x)
    except RuntimeError:
        return
    assert False


def test_missing_builder_fails():
    try:
        transform('x=1\n')
    except RuntimeError:
        return
    assert False


def test_no_fake_proofstep():
    assert 'ProofStep(' not in transform(sample())


def test_catalog_is_not_execution():
    assert 'apply_inference_match(' not in transform(sample())
