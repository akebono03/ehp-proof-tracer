import ast
from pathlib import Path
from phase165_r6_2_unified_registry_r3_r2.r3_r2_audit import (
    imports_for, resolve, inspect_function, inspect_shared, markdown,
)


def test_import_resolution():
    tree = ast.parse('from relation_rules import sum_commutativity_inference_rule as rule\nimport set_rules as sets\n')
    m = imports_for(tree)
    assert resolve('rule',m,'demo') == 'relation_rules.sum_commutativity_inference_rule'
    assert resolve('sets.kernel_inference_rule',m,'demo') == 'set_rules.kernel_inference_rule'


def test_local_function_resolution():
    assert resolve('expand_x',{},'module_a') == 'module_a.expand_x'


def test_direct_factory_mapping(tmp_path):
    (tmp_path/'a.py').write_text('from relation_rules import sample_inference_rule as rule\ndef expand_case(goal):\n    return rule()\n')
    entry = inspect_function(tmp_path,'a.expand_case',{'relation_rules.sample_inference_rule'})
    assert entry['rule_links'][0]['kind'] == 'DIRECT_R8_FACTORY'


def test_unknown_factory_does_not_certify(tmp_path):
    (tmp_path/'a.py').write_text('def expand_case(goal):\n    return other_inference_rule()\n')
    entry = inspect_function(tmp_path,'a.expand_case',set())
    assert entry['rule_links'][0]['kind'] == 'OUTSIDE_R8_OR_UNRESOLVED_FACTORY'
    assert entry['mathematical_equivalence_verified'] is False


def test_missing_source(tmp_path):
    assert inspect_function(tmp_path,'missing.expand_x',set())['status']=='SOURCE_NOT_FOUND'


def test_shared_mapping(tmp_path):
    (tmp_path/'phase165_r52_r9_shared_math.py').write_text('from alpha import expand_x as xx\n')
    out=inspect_shared(tmp_path,[{'symbol':'xx','line':1,'connection':'PROVIDER_LOOP_MEMBER'}],set())
    assert out[0]['provider_id']=='alpha.expand_x'


def test_render():
    s=markdown({'r8_factory_count':77,'r3_shared_connection_count':1,
                'r3_other_expand_candidate_count':0,'shared_connections':[], 'providers':[]})
    assert 'R3-2' in s and '77' in s
