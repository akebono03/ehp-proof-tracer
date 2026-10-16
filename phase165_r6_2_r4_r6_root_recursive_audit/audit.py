"""Read-only bounded recursive diagnosis for the three pi_4^3 root candidates."""
from __future__ import annotations

import json
from pathlib import Path


def same(a, b):
    return type(a) is type(b) and a == b


def valid_given(bridge, goal):
    if not bridge.proof_links:
        return []
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    matches = []
    for link in bridge.proof_links:
        assertion = bridge.registry.assertion(link.assertion_id)
        step = link.step
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT and step is not None
                and step.rule is ProofRule.GIVEN and same(step.conclusion, assertion.content)
                and same(assertion.content, goal)):
            matches.append((link.assertion_id, step))
    return matches


def forward_check(rule, premise_steps, goal):
    from proof import find_inference_matches_for_rule
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    matches = [m for m in find_inference_matches_for_rule(rule, tuple(premise_steps))
               if len(m.premises) == len(premise_steps)
               and all(a is b for a, b in zip(m.premises, premise_steps))]
    for m in matches:
        derived = derive_inference_proof_step(m)
        if same(derived.conclusion, goal):
            return derived
    return None


def inspect(goal, bridge, provider, depth, active, budget):
    if budget['remaining'] <= 0:
        return {'goal':repr(goal),'state':'NODE_BUDGET_EXCEEDED','children':[]}, None
    budget['remaining'] -= 1
    record={'goal':repr(goal),'type':type(goal).__name__,'depth_remaining':depth}
    refs=valid_given(bridge,goal)
    record['matching_fixed_given_ids']=[id for id,_ in refs]
    if len(refs)==1:
        record['state']='FIXED_REFERENCE';record['children']=[]
        return record, refs[0][1]
    if len(refs)>1:
        record['state']='AMBIGUOUS_REFERENCES';record['children']=[]
        return record,None
    if any(same(goal,x) for x in active):
        record['state']='CYCLE';record['children']=[]
        return record,None
    if depth==0:
        record['state']='DEPTH_LIMIT';record['children']=[]
        return record,None
    try:
        opts=provider(goal)
    except Exception as exc:
        record['state']='PROVIDER_ERROR';record['error']=f'{type(exc).__name__}: {exc}';record['children']=[]
        return record,None
    record['candidate_count']=len(opts)
    record['children']=[]
    valid=[]
    for idx,op in enumerate(opts):
        branch={'index':idx,'rule_name':getattr(op.rule,'name',repr(op.rule)),'premises':[]}
        substeps=[]
        unresolved=False
        for sub in op.subgoals:
            node, step=inspect(sub,bridge,provider,depth-1,active+(goal,),budget)
            branch['premises'].append(node)
            if step is None:
                unresolved=True
            else:
                substeps.append(step)
        if not unresolved and len(substeps)==len(op.subgoals):
            try:
                verified=forward_check(op.rule,substeps,goal)
                branch['forward_verification']='PASS' if verified is not None else 'NO_MATCH'
                if verified is not None:
                    valid.append(verified)
            except Exception as exc:
                branch['forward_verification']='ERROR';branch['error']=f'{type(exc).__name__}: {exc}'
        else:
            branch['forward_verification']='PREMISES_UNRESOLVED'
        record['children'].append(branch)
    record['verified_derivation_count']=len(valid)
    record['state']=('VERIFIED_UNIQUE' if len(valid)==1 else 'AMBIGUOUS_DERIVATIONS' if len(valid)>1 else 'NO_VERIFIED_DERIVATION')
    return record,valid[0] if len(valid)==1 else None


def audit(bridge, provider, goal, depths=(2,3,4), budget_per_root=500):
    roots=provider(goal)
    results=[]
    for idx,root in enumerate(roots):
        entry={'index':idx,'rule_name':getattr(root.rule,'name',repr(root.rule)),
               'subgoals':[repr(s) for s in root.subgoals], 'depths':{}}
        for depth in depths:
            budget={'remaining':budget_per_root}
            subreports=[];steps=[]
            for child in root.subgoals:
                node,step=inspect(child,bridge,provider,depth-1,(goal,),budget)
                subreports.append(node)
                steps.append(step)
            summary='PREMISES_UNRESOLVED'
            if all(s is not None for s in steps):
                try:
                    summary='FORWARD_PASS' if forward_check(root.rule,steps,goal) is not None else 'FORWARD_NO_MATCH'
                except Exception as exc:
                    summary=f'FORWARD_ERROR:{type(exc).__name__}:{exc}'
            entry['depths'][str(depth)]={'result':summary,'subgoals':subreports,'budget_used':budget_per_root-budget['remaining']}
        results.append(entry)
    return {'status':'ROOT_RECURSIVE_AUDITED','root_candidate_count':len(roots),
            'depths':list(depths),'root_candidates':results,
            'note':'Bounded diagnostic search; only successful forward checks count as derived, not candidate generation.',
            'production_modified':False,'full_pytest_run':False}


def main():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from homotopy_groups import TodaPrimaryGroup,FiniteCyclicGroup
    from expression import HomotopyElement,GeneratorSymbol
    from proof import Relation,RelationType
    goal=Relation(TodaPrimaryGroup(4,3),FiniteCyclicGroup(2,HomotopyElement(name='η_3',dimension=3,source=4,target=3,generator=GeneratorSymbol('η',3))),RelationType.EQUALITY)
    bridge=build_shared_typed_bridge();provider=shared_expansion_provider(bridge)
    report=audit(bridge,provider,goal)
    output=Path(__file__).parent/'audit_output';output.mkdir(exist_ok=True)
    (output/'recursive_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# π₄³ ルート候補の再帰展開監査','',f"ルート候補: {report['root_candidate_count']}",'']
    for root in report['root_candidates']:
        lines += [f"## 候補 {root['index']+1}: {root['rule_name']}", '']
        for sub in root['subgoals']:lines.append(f'- Subgoal: `{sub}`')
        for depth,entry in root['depths'].items():
            lines += [f"- 深度 {depth}: {entry['result']}（探索ノード {entry['budget_used']}）"]
            for node in entry['subgoals']:
                lines += [f"  - `{node['goal']}` → {node['state']}"]
        lines.append('')
    lines += ['## 判定の限界','候補の存在は証明の完成を意味しません。','予算・深度の打ち切りは不可能性の証明ではありません。']
    (output/'recursive_audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'root_candidate_count':report['root_candidate_count'],
      'results':[{ 'candidate':r['index']+1,'rule':r['rule_name'], 'depth_results':{d:x['result'] for d,x in r['depths'].items()}} for r in report['root_candidates']],
      'production_modified':False,'full_pytest_run':False},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
