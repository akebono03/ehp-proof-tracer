import ast
from pathlib import Path
import pytest
from phase165_r6_2_unified_registry_r3.r3_inventory import (
    audit, discover_factories, dotted, find_shared_providers, render,
)


def test_dotted():
    assert dotted(ast.parse('a.b.c',mode='eval').body)=='a.b.c'
    assert dotted(ast.Constant(1)) is None


def test_shared_provider_connections(tmp_path):
    src='''def shared_expansion_provider(bridge):
    def expand(goal):
        options=[]
        options.extend(expand_foo(goal))
        for provider in (expand_bar, *extra_providers):
            new=provider(goal)
        return options
    return expand
'''
    path=tmp_path/'file.py'
    path.write_text(src)
    found=find_shared_providers(path)
    symbols={x['symbol'] for x in found}
    assert 'expand_foo' in symbols
    assert 'expand_bar' in symbols
    assert 'extra_providers' in symbols


def test_missing_shared_function(tmp_path):
    path=tmp_path/'empty.py'
    path.write_text('value=3\n')
    with pytest.raises(ValueError):
        find_shared_providers(path)


def test_r8_factory_inventory(tmp_path):
    (tmp_path/'rules.py').write_text('def first_inference_rule(x):\n    return x\n')
    assert discover_factories(tmp_path,('rules',))==['rules.first_inference_rule']


def test_audit_read_only(tmp_path):
    (tmp_path/'phase165_r52_r9_shared_math.py').write_text('def shared_expansion_provider(bridge):\n    return ()\n')
    before={p.name:p.read_bytes() for p in tmp_path.iterdir()}
    data=audit(tmp_path)
    assert data['runtime_verified'] is False
    assert data['status']=='INVENTORY_ONLY'
    assert before=={p.name:p.read_bytes() for p in tmp_path.iterdir()}


def test_render():
    s=render({'shared_provider_connections':[{'symbol':'expand_sample','connection':'DIRECT_OPTIONS_EXTEND','line':4}], 'other_expand_function_count':1})
    assert 'expand_sample' in s
    assert 'INVENTORY_ONLY' in s
