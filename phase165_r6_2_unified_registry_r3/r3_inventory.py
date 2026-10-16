"""Conservative inventory of non-R8 rule and provider connections.

Does not invoke providers or infer that an AST reference proves reachability.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


def dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted(node.value)
        return parent + '.' + node.attr if parent else None
    return None


def read_source(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))


def find_shared_providers(path: Path) -> list[dict]:
    tree = read_source(path)
    fn = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == 'shared_expansion_provider'), None)
    if fn is None:
        raise ValueError('shared_expansion_provider not found')
    result = []
    for node in ast.walk(fn):
        if not isinstance(node, ast.Call):
            continue
        callee = dotted(node.func)
        if callee is None:
            continue
        if callee.endswith('options.extend') and node.args:
            arg = node.args[0]
            inner = dotted(arg.func) if isinstance(arg, ast.Call) else dotted(arg)
            if inner and inner != 'new':
                result.append({'symbol':inner,'line':node.lineno,'connection':'DIRECT_OPTIONS_EXTEND','invoked':False})
        if callee == 'merge_backward_expansions' and node.args:
            for arg in node.args:
                target = dotted(arg.func) if isinstance(arg, ast.Call) else dotted(arg)
                if target and (target.endswith('provider') or target in ('witness_options','seeded_options')):
                    result.append({'symbol':target,'line':node.lineno,'connection':'MERGE_PATH','invoked':False})
        if callee == 'provider' and node.args:
            result.append({'symbol':'provider(goal)','line':node.lineno,'connection':'PROVIDER_LOOP','invoked':False})
    for node in ast.walk(fn):
        if isinstance(node, ast.For) and isinstance(node.target,ast.Name) and node.target.id == 'provider' and isinstance(node.iter,ast.Tuple):
            for elt in node.iter.elts:
                name=dotted(elt)
                if name:
                    result.append({'symbol':name,'line':node.lineno,'connection':'PROVIDER_LOOP_MEMBER','invoked':False})
                elif isinstance(elt,ast.Starred):
                    result.append({'symbol':dotted(elt.value) or 'dynamic','line':node.lineno,'connection':'PROVIDER_LOOP_DYNAMIC','invoked':False})
    return sorted(result, key=lambda x:(x['line'],x['symbol']))


def discover_factories(root: Path, modules: tuple[str, ...]) -> list[str]:
    entries=[]
    for module in modules:
        path=root/(module+'.py')
        if not path.is_file():
            continue
        tree=read_source(path)
        for n in tree.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.endswith('_inference_rule'):
                entries.append(module+'.'+n.name)
    return sorted(entries)


def discover_other_provider_functions(root: Path, excluded: tuple[str,...]) -> list[dict]:
    result=[]
    for path in sorted(root.glob('*.py')):
        if path.stem in excluded:
            continue
        try:
            tree=read_source(path)
        except (SyntaxError, UnicodeError):
            continue
        for n in tree.body:
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and (n.name.startswith('expand_') or n.name.endswith('_expansion_provider')):
                result.append({'symbol':path.stem+'.'+n.name,'line':n.lineno,'status':'SOURCE_ONLY_NOT_PROVEN_CONNECTED'})
    return result


def audit(root: Path) -> dict:
    from_r8=('ehp_rules','stable_rules','set_rules','hopf_rules','scalar_rules','relation_rules','map_property_rules','homomorphism_rules','indeterminacy_rules')
    shared=root/'phase165_r52_r9_shared_math.py'
    if not shared.is_file():
        raise FileNotFoundError(shared)
    connected=find_shared_providers(shared)
    rule_ids=discover_factories(root,from_r8)
    other=discover_other_provider_functions(root,from_r8)
    return {'status':'INVENTORY_ONLY','r8_factory_id_count':len(rule_ids),'r8_factory_ids':rule_ids,
            'shared_provider_connections':connected,'other_expand_function_count':len(other),
            'other_expand_functions':other,'runtime_verified':False,'mathematical_soundness_verified':False,
            'notes':['Static references do not prove execution or mathematical correctness.',
                     'Potential expand_ functions may not be providers.',
                     'Only top-level Python files are scanned; this is not a complete global inventory.',
                     'No group-specific adapter or source witness is registered automatically.']}


def render(data: dict) -> str:
    lines=['# Phase 165 R6-2 統一規則台帳 R3：非R8経路の棚卸し','',
           '- 状態: `INVENTORY_ONLY`','- 本番コード変更: なし',
           '- 推論・証明の実行検証: なし','',
           '## 共通 Provider の静的接続箇所','', '| symbol | connection | 行 |','|---|---|---:|']
    for x in data['shared_provider_connections']:
        lines.append('| `'+x['symbol']+'` | '+x['connection']+' | '+str(x['line'])+' |')
    lines+=['','## R8以外の expand_ 系関数候補', '',
            '検出数: '+str(data['other_expand_function_count']),
            '', 'これらは関数名による候補であり、一般規則や到達可能な Provider と認定したものではない。',
            '', '## 次段階', '',
            '各接続箇所に対して Rule/Provider の分類、実行条件、入力証人、逆向き生成能力を検証してから統一台帳に登録する。', '']
    return '\n'.join(lines)


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,default=Path('.'))
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    data=audit(a.root)
    a.output.mkdir(parents=True,exist_ok=True)
    (a.output/'provider_inventory.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (a.output/'provider_inventory.md').write_text(render(data),encoding='utf-8')
    print(json.dumps({'status':data['status'],'r8_factory_id_count':data['r8_factory_id_count'],
                      'shared_connections':len(data['shared_provider_connections']),
                      'other_expand_candidates':data['other_expand_function_count'],
                      'production_modified':False,'full_pytest_run':False},indent=2))


if __name__=='__main__':
    main()
