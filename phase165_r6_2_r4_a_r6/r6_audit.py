"""Read-only comparison of pi4^3 adapter with existing generic backward machinery."""
from __future__ import annotations
import argparse
import ast
import importlib
import inspect
import json
from pathlib import Path

TARGETS = (
    ('generator_substitution', 'phase165_r57_r18_generator_substitution', 'finite_cyclic_generator_substitution_rule'),
    ('finite_cyclic_group', 'toda_rules', 'toda_pi4_3_finite_cyclic_inference_rule'),
    ('kernel_from_exactness', 'toda_rules', 'toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule'),
    ('surjectivity_from_exactness', 'toda_rules', 'toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule'),
)


def source_info(root: Path, module_name: str, name: str) -> dict:
    path = root / (module_name + '.py')
    item = {'module': module_name, 'factory': name, 'source': str(path), 'source_found': path.is_file(),
            'function_found': False, 'line': None, 'hardcoded_dimensions': [], 'constants_in_factory': []}
    if not path.is_file():
        return item
    tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    function = next((n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name), None)
    if function is None:
        return item
    item['function_found'] = True
    item['line'] = function.lineno
    for call in ast.walk(function):
        if isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == 'TodaPrimaryGroup' and len(call.args) >= 2:
            values = []
            for expr in call.args[:2]:
                values.append(expr.value if isinstance(expr, ast.Constant) and type(expr.value) is int else None)
            if all(v is not None for v in values):
                item['hardcoded_dimensions'].append(values)
    return item


def rule_info(module_name: str, name: str) -> dict:
    from proof import InferenceRule
    result = {'factory_runtime': 'NOT_TESTED', 'rule_name': None, 'conclusion_pattern': False,
              'premise_count': None, 'required_parameters': [], 'generic_r8_discoverable': False,
              'pattern_backward_structural': False, 'unknown_premise_variables': [], 'error': None}
    try:
        module = importlib.import_module(module_name)
        function = getattr(module, name)
        signature = inspect.signature(function)
        required = [p.name for p in signature.parameters.values() if p.default is inspect.Parameter.empty and
                    p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
        result['required_parameters'] = required
        if required:
            result['factory_runtime'] = 'REQUIRES_INPUT'
            return result
        rule = function()
        if not isinstance(rule, InferenceRule):
            result['factory_runtime'] = 'NOT_INFERENCE_RULE'
            return result
        result['factory_runtime'] = 'INSTANTIATED'
        result['rule_name'] = rule.name
        result['conclusion_pattern'] = rule.conclusion_pattern is not None
        result['premise_count'] = len(rule.premise_patterns)
        result['generic_r8_discoverable'] = (module_name in (
            'ehp_rules', 'stable_rules', 'set_rules', 'hopf_rules', 'scalar_rules', 'relation_rules',
            'map_property_rules', 'homomorphism_rules', 'indeterminacy_rules') and name.endswith('_inference_rule'))
        if rule.conclusion_pattern is not None and rule.premise_patterns:
            from phase165_r8_rule_provider import _pattern_variable_names
            bound = _pattern_variable_names(rule.conclusion_pattern)
            missing = set()
            for p in rule.premise_patterns:
                pattern = p.relation_pattern if p.relation_pattern is not None else p.statement_pattern
                if pattern is not None:
                    missing.update(_pattern_variable_names(pattern) - bound)
            result['unknown_premise_variables'] = sorted(missing)
            result['pattern_backward_structural'] = not missing
        return result
    except Exception as e:
        result['factory_runtime'] = 'ERROR'
        result['error'] = type(e).__name__ + ': ' + str(e)[:240]
        return result


def source_connection(root: Path) -> dict:
    adapter = root / 'phase165_r52_r23_existing_rule_adapter.py'
    shared = root / 'phase165_r52_r9_shared_math.py'
    out = {'adapter_found': adapter.is_file(), 'shared_found': shared.is_file(), 'adapter_provider_referenced': False,
           'explicit_adapter_dimensions': [], 'factory_mentions': {}}
    if adapter.is_file():
        text = adapter.read_text(encoding='utf-8-sig')
        tree = ast.parse(text)
        out['factory_mentions'] = {name: any(isinstance(x, ast.Call) and
           ((isinstance(x.func, ast.Name) and x.func.id == name) or
            (isinstance(x.func, ast.Attribute) and x.func.attr == name)) for x in ast.walk(tree))
                                  for _, _, name in TARGETS}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'TodaPrimaryGroup' and len(node.args) == 2:
                if all(isinstance(x, ast.Constant) and type(x.value) is int for x in node.args):
                    value = [x.value for x in node.args]
                    if value not in out['explicit_adapter_dimensions']:
                        out['explicit_adapter_dimensions'].append(value)
    if shared.is_file():
        tree = ast.parse(shared.read_text(encoding='utf-8-sig'))
        funcs = [f for f in tree.body if isinstance(f, ast.FunctionDef) and f.name == 'shared_expansion_provider']
        out['adapter_provider_referenced'] = bool(funcs and any(isinstance(n, ast.Name) and
             n.id == 'expand_existing_pi43_rules' for n in ast.walk(funcs[0])))
    return out


def audit(root: Path) -> dict:
    root = root.resolve()
    conn = source_connection(root)
    rows = []
    for branch, module, factory in TARGETS:
        source = source_info(root, module, factory)
        runtime = rule_info(module, factory) if source['function_found'] else {'factory_runtime':'NOT_FOUND'}
        rows.append({'branch':branch, 'rule_id':module+'.'+factory, 'source':source, 'runtime':runtime,
                     'adapter_mentions_factory':conn['factory_mentions'].get(factory, False),
                     'generic_goal_application':'NOT_TESTED', 'witness_seeded_application':'NOT_TESTED',
                     'recursive_proof_verified':False,
                     'replacement_status':'NOT_DEMONSTRATED'})
    return {'phase':'165 R6-2 R4-A-R6', 'status':'AUDITED_READ_ONLY', 'source_root':str(root),
            'adapter':conn, 'branches':rows,
            'counts':{'branches':len(rows),'factories_instantiated':sum(r['runtime']['factory_runtime']=='INSTANTIATED' for r in rows),
                      'r8_default_eligible':sum(r['runtime'].get('generic_r8_discoverable',False) for r in rows),
                      'generic_replacements_verified':0,'proofs_verified':0},
            'limitations':['Structural analysis and zero-input factory instantiation do not establish mathematical generality.',
                           'Specialized or parameterized factories can be usable through other providers even if absent from R8.',
                           'No synthetic Goal and no proof Step is treated as evidence of replacement.',
                           'No Adapter branch is removed; actual search substitution remains future work.']}


def markdown(data: dict) -> str:
    lines=['# Phase 165 R6-2 R4-A-R6 監査', '', '状態: `'+data['status']+'`', '',
           '## pi4^3 の既存4分岐', '', '| 分岐 | factory | 生成状況 | R8既定収集 | 結論パターン | 置換実証 |',
           '|---|---|---|---|---|---|']
    for row in data['branches']:
        v=row['runtime']
        lines.append('| '+row['branch']+' | `'+row['rule_id']+'` | '+v['factory_runtime']+' | '+
                     ('対象' if v.get('generic_r8_discoverable') else '対象外')+' | '+
                     ('あり' if v.get('conclusion_pattern') else 'なし／不明')+' | 未実証 |')
    lines += ['', '## 専用 Adapter', '',
              '- 共通 Provider からの静的参照: '+str(data['adapter']['adapter_provider_referenced']),
              '- 固定次元の型付き生成: '+str(data['adapter']['explicit_adapter_dimensions']), '',
              '## 判定', '',
              '4分岐の一般規則への置換は未実証。規則の生成可能性と、任意の群へ適用できることを混同しない。',
              'R4-A-R7 では実際の pi4^3 Goal に対して Adapter あり／なしで同一の前提候補が得られるか確認する。',
              '', '## 制約', '']
    lines += ['- '+x for x in data['limitations']]
    return '\n'.join(lines)+'\n'


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    data=audit(args.root)
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'r6_capability.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (args.out/'r6_capability.md').write_text(markdown(data),encoding='utf-8')
    print(json.dumps({'status':data['status'],'counts':data['counts'],'adapter':data['adapter']['adapter_provider_referenced'],
                      'output':str(args.out)},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
