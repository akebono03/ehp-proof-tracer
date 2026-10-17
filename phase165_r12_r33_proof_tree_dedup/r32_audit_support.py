"""Read-only capture of accepted derivations in canonical Web search."""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import fields, is_dataclass
from collections import defaultdict
import phase165_r3_recursive_search as search
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r6_2_r4_r8_dedup import same_cited_scalar_specialization
from proof import ProofRule, ProofStep


def describe_step(root: ProofStep) -> dict:
    """Inspect ancestry with actual object identities; never certify a step."""
    seen = set()
    active = set()
    cycles = []
    nodes = []
    references = []

    def walk(step, depth):
        if not isinstance(step, ProofStep):
            return
        identity = id(step)
        if identity in active:
            cycles.append(repr(step.conclusion))
            return
        if identity in seen:
            return
        seen.add(identity)
        active.add(identity)
        rule = getattr(step.inference_rule, 'name', None)
        ref = getattr(step.inference_rule, 'literature_reference', None)
        node = {'depth': depth, 'conclusion': repr(step.conclusion),
                'proof_rule': step.rule.value, 'inference_rule': rule,
                'premise_count': len(step.premises), 'literature_reference': repr(ref) if ref else None}
        nodes.append(node)
        if ref is not None:
            references.append(repr(ref))
        for parent in step.premises:
            walk(parent, depth + 1)
        active.remove(identity)
    walk(root, 0)
    return {'root_conclusion':repr(root.conclusion),
            'root_inference_rule':getattr(root.inference_rule,'name',None),
            'root_premises':[repr(x.conclusion) for x in root.premises],
            'node_count':len(nodes), 'proof_nodes':nodes,
            'references':list(dict.fromkeys(references)), 'cycles':cycles}


def compare_derivations(steps: list[ProofStep]) -> dict:
    """Report equivalence evidence without selecting either route."""
    pairs=[]
    for i,left in enumerate(steps):
        for j in range(i+1,len(steps)):
            right=steps[j]
            pairs.append({'left':i,'right':j,
                          'same_object':left is right,
                          'same_conclusion':left.conclusion==right.conclusion,
                          'same_rule_name':getattr(left.inference_rule,'name',None)==getattr(right.inference_rule,'name',None),
                          'same_premise_conclusions':tuple(p.conclusion for p in left.premises)==tuple(p.conclusion for p in right.premises),
                          'known_scalar_specialization_alias':same_cited_scalar_specialization(left,right)})
    return {'candidate_count':len(steps),'pair_comparisons':pairs}


def run_diagnostic() -> dict:
    bridge=build_shared_typed_bridge()
    goals=registered_group_goal_candidates(bridge,n=3,k=1)
    if len(goals)!=1:
        raise RuntimeError('expected exactly one typed Web goal')
    goal=goals[0]
    captured=[]
    original=search.append_unique_verified_derivation

    def observe(options,candidate):
        before=len(options)
        original(options,candidate)
        if candidate.conclusion==goal:
            captured.append({'accepted':len(options)>before,'step':candidate})

    # Restore immediately after the ordinary search, even on failure.
    search.append_unique_verified_derivation=observe
    try:
        result=search_group_from_registered_goal(n=3,k=1,bridge=bridge)
    finally:
        search.append_unique_verified_derivation=original
    accepted=[event['step'] for event in captured if event['accepted']]
    return {'phase':'165 R12-R32', 'mode':'READ_ONLY_ACCEPTED_DERIVATION_AUDIT',
            'web_target':repr(goal), 'web_search_status':result.status.value,
            'diagnostics':list(result.diagnostics),
            'open_goals':[repr(g) for g in result.open_goals],
            'captured_root_events':len(captured),
            'accepted_root_count':len(accepted),
            'rejected_root_events':len(captured)-len(accepted),
            'root_derivations':[describe_step(step) for step in accepted],
            'comparison':compare_derivations(accepted),
            'diagonal_inverse_unresolved':any('ι_5' in repr(g) and 'FreeCyclicGroup' in repr(g) for g in result.open_goals),
            'no_persistent_patches':search.append_unique_verified_derivation is original,
            'full_pytest_run':False,
            'status':'AUDIT_CAPTURED' if len(accepted)>=2 else 'DERIVATION_COUNT_DIFFERS_FROM_PRIOR_RUN'}


def main():
    data=run_diagnostic()
    location=Path(__file__).resolve().parent/'audit_result.json'
    location.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({key:value for key,value in data.items() if key!='root_derivations'},ensure_ascii=False,indent=2))
    print('Detailed proof trees:',location)


if __name__=='__main__':
    main()
