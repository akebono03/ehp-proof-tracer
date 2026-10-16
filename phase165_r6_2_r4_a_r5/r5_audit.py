"""Read-only Phase 165 R6-2 R4-A-R5 diagnostics."""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from importlib import util
import json
from pathlib import Path
import sys


def classify_goal(rule, goal, unify, pattern_names, instantiate):
    """Describe the observable reverse-pattern failure, not mathematical impossibility."""
    if rule.conclusion_pattern is None:
        return 'NO_CONCLUSION_PATTERN'
    try:
        unified = unify(rule, goal)
    except Exception as exc:
        return 'MATCH_ERROR:' + type(exc).__name__
    if unified is None:
        return 'NO_CONCLUSION_MATCH'
    premises = tuple(rule.premise_patterns or ())
    if not premises:
        return 'NO_PREMISE_PATTERNS'
    bound = {item.variable.name for item in unified.bindings}
    required = set()
    for p in premises:
        target = p.relation_pattern if p.relation_pattern is not None else p.statement_pattern
        if target is None:
            return 'OPAQUE_PREMISE'
        required.update(pattern_names(target))
    if required - bound:
        return 'UNBOUND_VARIABLE'
    try:
        result = instantiate(unified)
    except Exception as exc:
        return 'PREMISE_ERROR:' + type(exc).__name__
    return 'PREMISES_GENERATED' if result else 'PREMISE_REJECTED_OR_GUARD_UNKNOWN'


def audit_adapter(path):
    """Inspect actual source; do not import or call target-specific adapter."""
    data={'path': str(path), 'status':'MISSING', 'branches':[], 'rule_factories':[], 'shared_provider_mentions_adapter':None}
    if not path.is_file():
        return data
    src=path.read_text(encoding='utf-8-sig')
    tree=ast.parse(src,filename=str(path))
    f=next((x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name=='expand_existing_pi43_rules'),None)
    if f is None:
        data['status']='FUNCTION_MISSING';return data
    data['status']='FOUND'
    factories=[]
    for call in ast.walk(f):
        if isinstance(call,ast.Call) and isinstance(call.func,ast.Attribute) and call.func.attr.endswith('_rule'):
            factories.append({'symbol':ast.unparse(call.func),'line':call.lineno})
        if isinstance(call,ast.Call) and isinstance(call.func,ast.Name) and call.func.id.endswith('_rule'):
            factories.append({'symbol':call.func.id,'line':call.lineno})
    data['rule_factories']=factories
    for node in ast.walk(f):
        if isinstance(node,ast.Return) and isinstance(node.value,ast.Tuple) and any(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='GoalExpansion' for x in node.value.elts):
            data['branches'].append({'line':node.lineno,'category':'GOAL_EXPANSION_RETURN'})
    return data


def audit_shared(root,adapter):
    path=root/'phase165_r52_r9_shared_math.py'
    if not path.is_file():
        adapter['shared_provider_mentions_adapter']=False
        adapter['shared_provider_status']='SOURCE_MISSING'
        return
    tree=ast.parse(path.read_text(encoding='utf-8-sig'))
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='shared_expansion_provider']
    name='expand_existing_pi43_rules'
    adapter['shared_provider_mentions_adapter']=bool(functions and any(isinstance(n,ast.Name) and n.id==name for n in ast.walk(functions[0])))
    adapter['shared_provider_status']='STATIC_REFERENCED' if adapter['shared_provider_mentions_adapter'] else 'NOT_REFERENCED'


def perform(root,max_goals=250):
    """Import the R4 audit only from the user's repository and preserve its Goal selection."""
    root=root.resolve()
    r4=root/'phase165_r6_2_r4_a_r4'/'r4_probe.py'
    if not r4.is_file():
        return {'status':'MISSING_R4_BASE','details':str(r4),'rules':[]}
    sys.path.insert(0,str(root))
    spec=util.spec_from_file_location('_r4a_r4_probe',str(r4))
    module=util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base=module.probe(root,max_goals=max_goals)
    adapter=audit_adapter(root/'phase165_r52_r23_existing_rule_adapter.py')
    audit_shared(root,adapter)
    if base.get('status')!='OK':
        return {'status':'BASE_INCOMPLETE','base_status':base.get('status'),'adapter':adapter,'rules':[]}
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r57_r23_conclusion_unification import unify_inference_conclusion
    from phase165_r57_r25_premise_generation import generate_candidate_premises
    from phase165_r8_rule_provider import _pattern_variable_names
    from importlib import import_module
    bridge=build_shared_typed_bridge()
    goals=[]
    for assertion in bridge.registry._assertions.values():
        v=getattr(assertion,'content',None)
        if v is not None and not any(type(v) is type(old) and v==old for old in goals):
            goals.append(v)
    goals=goals[:max_goals]
    rows=[]
    for entry in base['rules']:
        row={k:v for k,v in entry.items() if k not in ('goal_errors',)}
        row['reason_counts']={}
        if entry['status']=='INSTANTIATED':
            module_name,factory_name=entry['rule_id'].rsplit('.',1)
            try:
                rule=getattr(import_module(module_name),factory_name)()
                def generate(unification):
                    return generate_candidate_premises(unification)
                reasons=Counter(classify_goal(rule,g,unify_inference_conclusion,_pattern_variable_names,generate) for g in goals)
                row['reason_counts']=dict(sorted(reasons.items()))
                row['goal_probe_status']='OBSERVED_ON_REGISTERED_GOALS' if goals else 'NO_GOALS'
            except Exception as exc:
                row['goal_probe_status']='AUDIT_ERROR'
                row['reason_counts']={'AUDIT_ERROR:'+type(exc).__name__:1}
        else:
            row['reason_counts']={'REQUIRES_INPUT_OR_FACTORY_UNAVAILABLE':1}
        row['common_search_connection']='STATIC_R8_PATH' if entry['status']=='INSTANTIATED' else 'NOT_IN_R8_DEFAULT'
        row['recursive_proof_verified']=False
        rows.append(row)
    result={'phase':'165 R6-2 R4-A-R5','status':'OK','source':'REGISTERED_ASSERTION_CONTENT',
            'goals_examined':len(goals),'rules':rows,'adapter':adapter,
            'reason_totals':dict(sorted(sum((Counter(x['reason_counts']) for x in rows if x['status']=='INSTANTIATED'),Counter()).items())),
            'runtime_proof_verified':0,
            'limitations':['NO_CONCLUSION_MATCH means only that no selected registered Goal matches.',
              'UNBOUND_VARIABLE does not prove witness unavailability.',
              'PREMISE_REJECTED_OR_GUARD_UNKNOWN does not identify a failing guard.',
              'STATIC_R8_PATH is not recursive execution proof.',
              'R8 factory family only; other providers and source witnesses remain outside the counts.',
              'The adapter branch source is inspected, not executed.']}
    return result


def markdown(d):
    lines=['# Phase 165 R6-2 R4-A-R5 失敗理由・pi4^3 接続監査','',
           '- 状態: `'+d['status']+'`','- Goal 検査数: '+str(d.get('goals_examined',0)),
           '- 証明成功の検証件数: 0（この監査では実行しない）','',
           '## 観測された失敗・成功理由','', '| 理由 | 観測回数 |','|---|---:|']
    for k,v in d.get('reason_totals',{}).items():lines.append('| `'+k+'` | '+str(v)+' |')
    a=d.get('adapter',{})
    lines+=['','## pi4^3 Adapter','', '- status: `'+a.get('status','UNKNOWN')+'`',
            '- shared provider: `'+str(a.get('shared_provider_status','UNKNOWN'))+'`',
            '- 直接参照された規則 factory: '+str(len(a.get('rule_factories',[]))),
            '- AST で検出した GoalExpansion return: '+str(len(a.get('branches',[]))), '',
            '| factory | 行 |','|---|---:|']
    for item in a.get('rule_factories',[]): lines.append('| `'+item['symbol']+'` | '+str(item['line'])+' |')
    lines+=['','## 規則別の理由','', '| Rule ID | R8 実行候補 | 理由の集計 |','|---|---:|---|']
    for r in d.get('rules',[]):
        reasons=', '.join(k+': '+str(v) for k,v in r['reason_counts'].items())
        lines.append('| `'+r['rule_id']+'` | '+str(r.get('r8_proposed',0))+' | '+reasons.replace('|','/')+' |')
    lines+=['','## 解釈上の制約','']+['- '+x for x in d.get('limitations',[])]
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--max-goals',type=int,default=250)
    a=p.parse_args()
    if a.max_goals<1:p.error('max-goals must be positive')
    report=perform(a.root,a.max_goals)
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'failure_reasons.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (a.out/'failure_reasons.md').write_text(markdown(report),encoding='utf-8')
    print(json.dumps({k:report.get(k) for k in ('status','goals_examined','reason_totals','runtime_proof_verified')},ensure_ascii=False,indent=2))
    print('adapter:',report.get('adapter',{}).get('shared_provider_status','UNKNOWN'))
    if report['status']!='OK':raise SystemExit(2)


if __name__=='__main__':main()
