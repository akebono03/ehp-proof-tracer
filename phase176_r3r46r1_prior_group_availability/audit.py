"""Actual public query audit; distinguish candidate, admitted, and accepted evidence."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective, MapSurjective
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME
from phase176_r3r46r1_prior_group_availability import pruning
from phase176_r3r46r1_prior_group_availability.apply import planned_changes
from proof import ProofRule


def observe():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from web_group_proof import build_standard_web_group_proof_view

    calls, rejected, invocations, results = [], [], [], []
    original_entry = entry.search_group_from_registered_goal
    original_adapter = shared.search_registered_partial_proof
    original_check = pruning.contradiction_witness

    def observed_entry(*args, **kwargs):
        result = original_entry(*args, **kwargs)
        results.append(result)
        return result

    def observed_adapter(*args, **kwargs):
        if (kwargs.get('n'), kwargs.get('k')) != (3, 5):
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

    def recorded_check(goal, **kwargs):
        evidence = original_check(goal, **kwargs)
        if evidence is not None:
            rejected.append((goal, evidence))
        return evidence

    with patch.object(entry, 'search_group_from_registered_goal', new=observed_entry), \
         patch.object(shared, 'search_registered_partial_proof', new=observed_adapter), \
         patch.object(pruning, 'contradiction_witness', new=recorded_check):
        view = build_standard_web_group_proof_view(n=3, k=5, max_depth=2, mode='narrative')
    if len(invocations) != 1 or len(results) != 1:
        raise RuntimeError('UNEXPECTED_PUBLIC_ENTRY_COUNT')
    invocation, result = invocations[0], results[0]
    root, context = invocation['goal'], invocation['bridge']
    source = TodaPrimaryGroup(7, 2)
    zero = TodaPrimaryGroupZeroStatement(source)
    unwanted = MapSurjective(TodaDeltaMap(TodaPrimaryGroup(8, 3), TodaPrimaryGroup(6, 1)))
    zero_map = ImageZeroStatement(TodaSuspensionMap(source, TodaPrimaryGroup(8, 3)))
    injective = MapInjective(TodaHopfInvariantMap(TodaPrimaryGroup(8, 3), TodaPrimaryGroup(8, 5)))
    prior = admitted_prior_group_step(source, proof_target=root, bridge=context)
    if prior is None or not verified_db_step(prior, proof_target=root, bridge=context):
        raise RuntimeError('PRIOR_GROUP_ADMISSION_NOT_AVAILABLE')
    prior_rejections = [step for goal, step in rejected if goal == zero and step == prior]
    zero_calls = [options for goal, options in calls if goal == zero]
    unwanted_calls = [options for goal, options in calls if goal == unwanted]
    map_calls = [options for goal, options in calls if goal == zero_map]
    routes = [option for options in map_calls for option in options if option.rule.name == RULE_NAME]
    accepted_db = [step for step in result.proven_steps if step == prior and verified_db_step(step, proof_target=root, bridge=context)]
    image_goal = None
    if routes:
        candidate = routes[0]
        if (len(candidate.subgoals) != 2 or candidate.subgoals[0] != prior.conclusion
                or type(candidate.subgoals[1]) is not GeneratorImage):
            raise RuntimeError('PRIOR_ZERO_MAP_PREMISES_CHANGED')
        image_goal = candidate.subgoals[1]
    accepted = lambda goal: any(step.conclusion == goal and step.rule is ProofRule.INFERENCE for step in result.proven_steps)
    passed = (bool(prior_rejections) and not zero_calls and not unwanted_calls
              and zero not in result.open_goals and unwanted not in result.open_goals
              and bool(routes) and bool(accepted_db))
    return {
        'gate': 'PASS_R3R46R1_PUBLIC_PRIOR_AVAILABILITY' if passed else 'FAIL_R3R46R1_PUBLIC_PRIOR_AVAILABILITY',
        'status': result.status.value,
        'web_key': view.key,
        'prior_group': repr(prior.conclusion),
        'prior_note': prior.note,
        'prior_db_accepted_count': len(accepted_db),
        'preceding_zero_pruned': bool(prior_rejections),
        'preceding_zero_provider_calls': len(zero_calls),
        'unnecessary_delta_provider_calls': len(unwanted_calls),
        'zero_map_provider_calls': len(map_calls),
        'prior_zero_map_candidate_count': len(routes),
        'generator_image_goal': repr(image_goal),
        'generator_image_proved': image_goal is not None and accepted(image_goal),
        'suspension_zero_proved': accepted(zero_map),
        'hopf_injective_proved': accepted(injective),
        'accepted_step_count': len(result.proven_steps),
        'open_goals': [repr(goal) for goal in result.open_goals],
        'pruning_evidence_not_accepted_by_pruning': [
            {'goal': repr(goal), 'witness': repr(step.conclusion), 'note': step.note,
             'rule': step.rule.value} for goal, step in rejected],
        'actual_provider_order': [
            {'goal': repr(goal), 'rules': [option.rule.name for option in options]}
            for goal, options in calls],
        'new_given_registrations': 0,
        'new_math_rules': 0,
        'full_pytest': 'NOT_RUN',
    }


def main():
    planned = planned_changes()
    if any(old != new for old, new in planned.values()):
        raise RuntimeError('PATCH_NOT_APPLIED')
    report = observe()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r46r1_prior_group_availability'
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / 'report.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key, value in report.items():
        if key != 'actual_provider_order':
            print('PHASE176_R3R46R1_'+key.upper()+'='+json.dumps(value, ensure_ascii=False))
    print('REPORT='+str(destination))
    if any(old != new for old, new in planned_changes().values()):
        raise RuntimeError('SOURCE_CHANGED_DURING_AUDIT')
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
