"""Observe actual Web calls and independently probe every proposed premise."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import RULE_NAME
from phase176_r3r44_public_subgroup_lift.apply import reviewed_source
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def observe():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from web_group_proof import build_standard_web_group_proof_view

    real_entry = entry.search_group_from_registered_goal
    real_adapter = shared.search_registered_partial_proof
    calls, invocations, results = [], [], []

    def observed_entry(*args, **kwargs):
        result = real_entry(*args, **kwargs)
        results.append(result)
        return result

    def observed_adapter(*args, **kwargs):
        if (kwargs.get('n'), kwargs.get('k')) != (3,5):
            return real_adapter(*args, **kwargs)
        invocations.append(dict(kwargs))
        forwarded = dict(kwargs)
        provider = kwargs['expansion_provider']

        def observed_provider(goal):
            options = provider(goal)
            calls.append((goal, options))
            return options

        forwarded['expansion_provider'] = observed_provider
        return real_adapter(*args, **forwarded)

    with patch.object(entry,'search_group_from_registered_goal',new=observed_entry), \
         patch.object(shared,'search_registered_partial_proof',new=observed_adapter):
        view = build_standard_web_group_proof_view(n=3,k=5,max_depth=2,mode='narrative')
    if len(invocations) != 1 or len(results) != 1:
        raise RuntimeError('UNEXPECTED_WEB_ENTRY_COUNT')
    invocation, result = invocations[0], results[0]
    root, context = invocation['goal'], invocation['bridge']
    cyclic = CyclicStructureStatement(root.lhs, root.rhs.generator, root.rhs.order)
    available = tuple(link.step.conclusion for link in context.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN
                      and context.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
                      and context.registry.assertion(link.assertion_id).content == link.step.conclusion)
    if root in available or cyclic in available:
        raise RuntimeError('TARGET_PRESENT_AS_GIVEN')
    candidates = []
    for requested, options in calls:
        if requested != cyclic:
            continue
        for option in options:
            if option.rule.name == RULE_NAME and not any(old.subgoals == option.subgoals for old in candidates):
                candidates.append(option)
    if not candidates or any(len(option.subgoals) != 5 for option in candidates):
        raise RuntimeError('ACTUAL_WEB_SUBGROUP_LIFT_CANDIDATE_MISSING')
    steps = tuple(result.proven_steps)
    prior = tuple(item.root.conclusion for item in invocation.get('completed_internal_proofs', ()))
    candidate_reports = []
    for option in candidates:
        premises = []
        for child in option.subgoals:
            provider = shared.shared_expansion_provider(context, proof_target=root, prior_conclusions=prior)
            probe = provider(child)
            actual = [options for requested, options in calls if requested == child]
            accepted = [step for step in steps if step.conclusion == child]
            premises.append({'goal':repr(child), 'actual_calls':len(actual),
                             'actual_candidate_counts':[len(x) for x in actual],
                             'accepted_steps':len(accepted),
                             'independent_candidate_count':len(probe),
                             'independent_rules':[p.rule.name for p in probe],
                             'screened_given':child in available})
        candidate_reports.append({'rule':option.rule.name,'premises':premises})
    return {'gate':'PASS_R3R44_PUBLIC_WEB_CANDIDATE_CONNECTED',
            'status':result.status.value,'web_key':view.key,
            'web_step_count':len(view.steps),'root_group_proved':result.status.value=='complete',
            'accepted_step_count':len(steps),'accepted_lift_steps':sum(s.inference_rule is not None and s.inference_rule.name==RULE_NAME for s in steps),
            'cyclic_candidate_count':len(candidates),'candidates':candidate_reports,
            'open_goals':[repr(g) for g in result.open_goals],
            'diagnostics':[str(x) for x in result.diagnostics],
            'new_given':0,'new_math_rules':0,'full_pytest':'NOT_RUN'}


def main():
    original, changed = reviewed_source()
    if original != changed:
        raise RuntimeError('PUBLIC_PATCH_NOT_APPLIED')
    report = observe()
    if reviewed_source() != (original,changed):
        raise RuntimeError('SHARED_SOURCE_CHANGED_DURING_AUDIT')
    destination = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r44_public_subgroup_lift' / 'report.json'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for key,value in report.items():
        if key not in ('candidates','open_goals','diagnostics'):
            print('PHASE176_R3R44_'+key.upper()+'='+str(value))
    for idx,candidate in enumerate(report['candidates'],1):
        for j,premise in enumerate(candidate['premises'],1):
            print(f'PHASE176_R3R44_CANDIDATE_{idx}_PREMISE_{j}='+json.dumps(premise,ensure_ascii=False))
    for goal in report['open_goals']:
        print('PHASE176_R3R44_OPEN_GOAL='+goal)
    print('REPORT='+str(destination))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
