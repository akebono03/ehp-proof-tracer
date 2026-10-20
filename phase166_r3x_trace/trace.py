"""Read-only trace of the actual registered pi_5^4 backward search."""
from __future__ import annotations

import json
from pathlib import Path

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase165_r57_r20_general_specialization import specialize_typed_statement
from proof import ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement, toda_eta_family_definition_statement

TARGET = 'shared:2:toda:adopted:prop5.1:higher_eta_group_relation'

def info(options):
    return [{'rule': item.rule.name, 'subgoals': [repr(g) for g in item.subgoals]}
            for item in options]

def run():
    bridge = build_shared_typed_bridge()
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    goals = registered_group_goal_candidates(bridge, n=4, k=1)
    if len(goals) != 1:
        raise RuntimeError(f'Expected one pi5^4 goal, got {len(goals)}')
    root = goals[0]
    screened = screen_shared_proof_context(bridge, goal=root, citing_assertion_id=TARGET,
                                           explicit_publication_target=True)
    fixed = tuple(link.step.conclusion for link in screened.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN)
    base = [v for v in fixed if isinstance(v, Relation) and v.lhs == TodaPrimaryGroup(4,3)
            and isinstance(v.rhs, FiniteCyclicGroup) and v.rhs.order == 2]
    refs = [v for v in fixed if isinstance(v, Toda45IsomorphismStatement)]
    eta3 = toda_eta_family_definition_statement(3).element
    base_generator = base[0].rhs.generator if len(base) == 1 else None
    targets = []
    for gen in (eta3, base_generator):
        if gen is None:
            continue
        candidate = Relation(TodaPrimaryGroup(5,4), FiniteCyclicGroup(2, IteratedSuspension(gen,1)))
        if candidate not in targets:
            targets.append(candidate)
    provider = shared_expansion_provider(screened, proof_target=root)
    cases=[]
    for candidate in targets:
        direct=expand_registered_toda45_finite_cyclic_goal(candidate, fixed)
        full=provider(candidate)
        cases.append({'goal':repr(candidate), 'direct':info(direct), 'common':info(full)})
    root_options=provider(root)
    report={'phase':'166 R3-X', 'read_only':True, 'goal':repr(root),
            'base_count':len(base),'base': [repr(v) for v in base],
            'eta3':repr(eta3), 'base_equal_definition':base_generator==eta3,
            'toda45_source_count':len(refs), 'root_options':info(root_options),
            'transport_candidates':cases,
            'source_specializations':[
                {'source':repr(r), 'bindings':repr(specialize_typed_statement(r, goal))}
                for r in refs
                for goal in (sub for item in root_options for sub in item.subgoals
                             if isinstance(sub,Toda45IsomorphismStatement))
            ]}
    path=Path(__file__).with_name('report.json')
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    summary={'root_rule_names':[x['rule'] for x in report['root_options']],
             'transport_rules':[[x['rule'] for x in t['common']] for t in cases],
             'base_count':len(base), 'toda45_source_count':len(refs), 'report':str(path)}
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':
    run()
