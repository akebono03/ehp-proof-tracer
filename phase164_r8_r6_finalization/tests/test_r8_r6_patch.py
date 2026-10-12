from pathlib import Path
import ast
import pytest
from apply import OLD_RENDER,NEW_RENDER,OLD_REFERENCE,NEW_REFERENCE,ADD_FACTORY,replace_exact,add_import


def test_reference_replacement_requires_exact_match():
    original='def f():\n    '+OLD_REFERENCE+'\n'
    changed=replace_exact(original,OLD_REFERENCE,NEW_REFERENCE,'reference')
    assert changed.count('annotate_derived_reference_step')==1
    with pytest.raises(ValueError,match='expected exactly one'):
        replace_exact(changed,OLD_REFERENCE,NEW_REFERENCE,'reference')


def test_renderer_projection_removes_direct_constructor():
    original='def f(proof_step,component):\n'+OLD_RENDER+'\n  return component_step\n'
    changed=replace_exact(original,OLD_RENDER,NEW_RENDER,'renderer')
    assert 'ProofStep(' not in changed
    assert 'project_reference_component_step(' in changed


def test_add_import_is_parseable():
    old='from proof import ProofStep\n\ndef f():\n    return 1\n'
    result=add_import(old,'annotate_derived_reference_step')
    assert ast.parse(result)
    assert 'from phase164_r8_proofstep_factory import' in result


def test_factory_additions_syntax_and_guards():
    source='from dataclasses import dataclass\n'+ADD_FACTORY
    assert ast.parse(source)
    assert 'cannot overwrite another foundational reference' in source
    assert 'display-only' in source


def test_manifest_scope_and_expected_site():
    import json
    root=Path(__file__).resolve().parents[1]
    audit=json.loads((root/'r8_r4_sites.json').read_text(encoding='utf-8'))
    sites=audit['sites']
    assert sum(s['category']=='dataclass_replace_type_review' for s in sites)==66
    assert sum(s['category']=='core_engine_keep_or_internal_refactor' for s in sites)==10
    assert sum(s['category']=='other_constructor_review' for s in sites)==1
