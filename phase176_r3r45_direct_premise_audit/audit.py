"""Read-only observation of real search and independently probed premises."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase176_r3r45_direct_premise_audit.apply import TARGET, updated_source


def candidate_records(options):
    return [{'rule': option.rule.name, 'premises': [repr(x) for x in option.subgoals]}
            for option in options]


def nonzero_presentation(statement, group):
    from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
    from proof import Relation, RelationType
    return (type(statement) is Relation and statement.relation_type is RelationType.EQUALITY
            and statement.lhs == group
            and (type(statement.rhs) is FreeCyclicGroup
                 or (type(statement.rhs) is FiniteCyclicGroup
                     and type(statement.rhs.order) is int and statement.rhs.order > 1)))


def observe():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from homotopy_groups import (TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
                                 TodaHopfInvariantMap, TodaSuspensionMap)
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import MapInjective
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, admitted_db_step
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import lifted_stable_composition
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import expand_zero_image_from_cyclic_generator
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    from web_group_proof import build_standard_web_group_proof_view
    from web_group_proof_common import _group_proof_statement_latex
    from phase168_r3_27_typed_statement_projection import typed_sentence

    calls, invocations, results = [], [], []
    original_entry = entry.search_group_from_registered_goal
    original_adapter = shared.search_registered_partial_proof

    def observed_entry(*args, **kwargs):
        result = original_entry(*args, **kwargs)
        results.append(result)
        return result

    def observed_adapter(*args, **kwargs):
        if (kwargs.get('n'), kwargs.get('k')) != (3,5):
            return original_adapter(*args, **kwargs)
        invocations.append(dict(kwargs))
        forwarded = dict(kwargs)
        provider = kwargs['expansion_provider']
        def observed_provider(goal):
            options = provider(goal)
            calls.append((goal, options))
            return options
        forwarded['expansion_provider'] = observed_provider
        return original_adapter(*args, **forwarded)

    with patch.object(entry,'search_group_from_registered_goal',new=observed_entry), \
         patch.object(shared,'search_registered_partial_proof',new=observed_adapter):
        view = build_standard_web_group_proof_view(n=3,k=5,max_depth=2,mode='narrative')
    if len(invocations) != 1 or len(results) != 1:
        raise RuntimeError('UNEXPECTED_WEB_ENTRY_COUNT')
    invocation, result = invocations[0], results[0]
    root, context = invocation['goal'], invocation['bridge']
    from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import RULE_NAME
    if not any(option.rule.name == RULE_NAME for _, options in calls for option in options):
        raise RuntimeError('R3R44_PUBLIC_LIFT_CANDIDATE_NOT_OBSERVED')
    prior = tuple(invocation.get('completed_internal_proofs', ()))
    goals = {'hopf_injective': MapInjective(TodaHopfInvariantMap(TodaPrimaryGroup(8,3), TodaPrimaryGroup(8,5))),
             'preceding_zero_group': TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(7,2)),
             'hopf_target_zero_group': TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(7,3)),
             'suspension_zero': ImageZeroStatement(TodaSuspensionMap(TodaPrimaryGroup(7,2), TodaPrimaryGroup(8,3)))}
    report = {'gate':'PASS_R3R45_DIRECT_PREMISE_AUDIT', 'status':result.status.value,
              'web_key':view.key,'accepted_step_count':len(result.proven_steps),
              'open_goals':[repr(g) for g in result.open_goals], 'probes':{}, 'nonzero_evidence':{},
              'new_given':0,'new_math_rules':0,'search_policy_changed':False,'full_pytest':'NOT_RUN'}
    for name, goal in goals.items():
        provider = shared.shared_expansion_provider(context, proof_target=root,
                    prior_conclusions=tuple(x.root.conclusion for x in prior))
        report['probes'][name] = {'goal':repr(goal), 'actual_calls':[
            {'index':i,'options':candidate_records(options)} for i,(requested,options) in enumerate(calls) if requested==goal],
            'independent_options':candidate_records(provider(goal)),
            'open':goal in result.open_goals}
    for name, n in (('preceding_group',2),('hopf_target_group',3)):
        group = TodaPrimaryGroup(7,n)
        fixed = []
        for link in context.proof_links:
            step = link.step
            if step is None or step.rule is not ProofRule.GIVEN:
                continue
            assertion = context.registry.assertion(link.assertion_id)
            if (assertion.origin is AssertionOrigin.FIXED_STATEMENT and assertion.content==step.conclusion
                    and nonzero_presentation(step.conclusion, group)):
                fixed.append({'id':link.assertion_id,'conclusion':repr(step.conclusion)})
        internal = [repr(x.root.conclusion) for x in prior if nonzero_presentation(x.root.conclusion,group)]
        accepted = [repr(x.conclusion) for x in result.proven_steps if nonzero_presentation(x.conclusion,group)]
        db = exact_prior_database_result(n,7-n)
        # Admission is probed only; nothing is passed back to search or reported as proved.
        admitted = admitted_db_step(db,proof_target=root,bridge=context) if db is not None else None
        report['nonzero_evidence'][name] = {'screened_fixed_links':fixed,'completed_internal':internal,
                'actual_accepted':accepted,'db_candidate':repr(db),'admitted_db_probe':repr(admitted),
                'db_is_nonzero_candidate':nonzero_presentation(db,group)}
        if n==2 and nonzero_presentation(db,group):
            report['zero_image_reuse_probe'] = {'stable_lift_available':lifted_stable_composition(db.rhs.generator) is not None,
                'generic_rule_options':candidate_records(expand_zero_image_from_cyclic_generator(goals['suspension_zero'],db))}
    zero = goals['suspension_zero']
    latex, fallback = _group_proof_statement_latex(zero)
    report['zero_display']={'latex':latex,'fallback':fallback,'typed_sentence':typed_sentence(zero,None),
        'actual_web_lines':[repr(x) for x in view.rendered_lines if latex is not None and latex in repr(x).replace('\\\\','\\')]}
    if latex is None or fallback is not None or r'\xrightarrow{0}' not in latex:
        raise RuntimeError('ZERO_MAP_DISPLAY_MISSING')
    if zero in result.open_goals and not any(line.statement_latex == latex or any(segment.value == latex for segment in line.segments) for line in view.rendered_lines):
        raise RuntimeError('ACTUAL_WEB_ZERO_GOAL_DISPLAY_MISSING')
    report['actual_provider_order']=[{'index':i,'goal':repr(goal),'rules':[x.rule.name for x in options]}
                                     for i,(goal,options) in enumerate(calls)]
    return report


def main():
    original = TARGET.read_bytes()
    if updated_source(original) != original:
        raise RuntimeError('DISPLAY_PATCH_NOT_APPLIED')
    report = observe()
    if TARGET.read_bytes() != original:
        raise RuntimeError('SOURCE_CHANGED_DURING_AUDIT')
    destination = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/'phase176_r3r45_direct_premise_audit'/'report.json'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for key,value in report.items():
        if key != 'actual_provider_order':
            print('PHASE176_R3R45_'+key.upper()+'='+json.dumps(value,ensure_ascii=False))
    print('REPORT='+str(destination))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
