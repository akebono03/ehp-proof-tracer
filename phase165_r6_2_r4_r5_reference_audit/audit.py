"""Read-only audit of the shared typed Reference environment for pi_4^3."""
from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any


def walk(value: Any, prefix: str = 'content', depth: int = 0):
    yield prefix, value
    if depth >= 8:
        return
    if is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            yield from walk(getattr(value, field.name), prefix + '.' + field.name, depth + 1)
    elif isinstance(value, (tuple, list)):
        for index, item in enumerate(value):
            yield from walk(item, f'{prefix}[{index}]', depth + 1)


def audit_bridge(bridge):
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup
    from proof import Relation, RelationType
    from expression import HomotopyElement, GeneratorSymbol
    from phase165_r8_rule_provider import discover_inference_rules

    links = {}
    for link in bridge.proof_links:
        links.setdefault(link.assertion_id, []).append(link)
    assertions = list(bridge.registry._assertions.values())
    records = []
    prop51 = []
    for a in assertions:
        ls = links.get(a.assertion_id, [])
        valid = [l for l in ls if l.step is not None and l.step.rule is ProofRule.GIVEN and l.step.conclusion == a.content and a.origin is AssertionOrigin.FIXED_STATEMENT]
        entry = {'assertion_id':a.assertion_id,'origin':getattr(a.origin,'name',str(a.origin)),'content_type':type(a.content).__name__,'linked_given':bool(valid),'component_paths':[{'path':p,'type':type(v).__name__} for p,v in walk(a.content) if p != 'content' and (p.count('.')<=2)]}
        records.append(entry)
        if 'prop5.1' in a.assertion_id.lower() or 'prop51' in a.assertion_id.lower():
            prop51.append(entry)
    rules, report = discover_inference_rules()
    eta3 = HomotopyElement(name='η_3',dimension=3,source=4,target=3,generator=GeneratorSymbol(family='η',index=3))
    goal = Relation(lhs=TodaPrimaryGroup(group_dimension=4,sphere_dimension=3),rhs=FiniteCyclicGroup(order=2,generator=eta3),relation_type=RelationType.EQUALITY)
    provider=shared_expansion_provider(bridge)
    options=provider(goal)
    result = {
        'phase':'165 R6-2 R4-5 Reference audit', 'status':'AUDITED_READ_ONLY',
        'assertion_count':len(assertions),'linked_given_assertion_count':sum(x['linked_given'] for x in records),
        'prop51_records':prop51,
        'candidate_goal':repr(goal),
        'root_candidate_count':len(options),
        'root_candidates':[{'rule_name':x.rule.name,'subgoals':[repr(y) for y in x.subgoals]} for x in options],
        'rule_count':len(rules),
        'observations':{
            'prop51_typed_given_present':any(x['linked_given'] for x in prop51),
            'prop51_delta_component_present':any(any('delta_iota5_relation' in c['path'] for c in x['component_paths']) for x in prop51),
            'root_has_non_symmetry_expansion':any('symmetr' not in x.rule.name.lower() for x in options),
        },
        'limitations':['Presence of a composite GIVEN does not prove automatic applicability of a component.','Root candidate count is not proof success.','This audit does not execute a recursive proof search.','Reference source edition is not independently verified.'],
        'production_modified':False,'full_pytest_run':False,
    }
    return result


def main():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    output=Path(__file__).resolve().parent/'audit_output'
    output.mkdir(exist_ok=True)
    report=audit_bridge(build_shared_typed_bridge())
    (output/'reference_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    lines=['# π₄³ Reference 接続監査','',f"- 登録命題: {report['assertion_count']}",f"- 型付き GIVEN と一致する命題: {report['linked_given_assertion_count']}",f"- ルート逆向き候補: {report['root_candidate_count']}",'','## Proposition 5.1','']
    for r in report['prop51_records']:
        lines += [f"- `{r['assertion_id']}`：GIVEN={'あり' if r['linked_given'] else 'なし'}", *[f"  - `{p['path']}` ({p['type']})" for p in r['component_paths']]]
    lines += ['','## ルート候補','']
    for r in report['root_candidates']:
        lines += [f"- {r['rule_name']}", *[f"  - {v}" for v in r['subgoals']]]
    lines+=['','## 注意','- 命題の登録と、探索への適用は別です。','- 未解決の前提を証明済みとは判定しません。']
    (output/'reference_audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['status','assertion_count','linked_given_assertion_count','rule_count','root_candidate_count','observations','production_modified','full_pytest_run']},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
