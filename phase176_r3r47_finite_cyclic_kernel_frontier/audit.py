"""Observe the real Web frontier; independent probes are not accepted proofs."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import conditional_inputs, expand_cyclic_delta_kernel
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import RULE_NAME as LIFT_RULE
from phase176_r3r47_finite_cyclic_kernel_frontier.apply import ROOT, TARGET, preflight
from proof import ProofRule, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import AssertionOrigin


def options_record(options):
    return [{'rule': item.rule.name, 'premises': [repr(g) for g in item.subgoals],
             'premise_proof_rules': [getattr(p.proof_rule, 'value', None)
                                     for p in item.rule.premise_patterns]} for item in options]


def signed_source_records(bridge, goal):
    """Distinguish actual linked signed facts, wrappers, and untyped metadata."""
    result = []
    for assertion in bridge.registry._assertions.values():
        reference = bridge.registry.reference(assertion.reference_id)
        content = assertion.content
        signed = content if type(content) is TodaDeltaImageUpToSignStatement else getattr(content, 'statement', None)
        matching_map = type(signed) is TodaDeltaImageUpToSignStatement and signed.map == goal.map
        if reference.locator != 'Lemma 5.7' and not matching_map:
            continue
        links = [link.step for link in bridge.proof_links if link.assertion_id == assertion.assertion_id
                 and link.step is not None]
        fixed = assertion.origin is AssertionOrigin.FIXED_STATEMENT
        eligible = [s for s in links if s.rule is ProofRule.GIVEN and not s.premises
                    and type(s.conclusion) is type(content) and s.conclusion == content and fixed]
        result.append({'id': assertion.assertion_id, 'locator': reference.locator,
                       'publication_position': reference.publication_position,
                       'type': type(content).__name__, 'content': repr(content),
                       'linked_given_count': len(eligible), 'exact_signed_goal': content == goal,
                       'wrapped_exact_signed_goal': type(content) is not TodaDeltaImageUpToSignStatement and signed == goal,
                       'signed_map_matches': matching_map})
    return result


def observe():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from web_group_proof import build_standard_web_group_proof_view
    from web_group_proof_common import _group_proof_statement_latex
    from phase165_r14_r6_generic_iso import MapInjective
    from homotopy_groups import TodaHopfInvariantMap

    calls, invocations, results = [], [], []
    original_entry = entry.search_group_from_registered_goal
    original_adapter = shared.search_registered_partial_proof

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

    with patch.object(entry, 'search_group_from_registered_goal', new=observed_entry), \
         patch.object(shared, 'search_registered_partial_proof', new=observed_adapter):
        view = build_standard_web_group_proof_view(n=3, k=5, max_depth=2, mode='narrative')
    if len(invocations) != 1 or len(results) != 1:
        raise RuntimeError('UNEXPECTED_WEB_ENTRY_COUNT')
    context, root = invocations[0]['bridge'], invocations[0]['goal']
    result = results[0]
    delta = TodaDeltaMap(TodaPrimaryGroup(8, 5), TodaPrimaryGroup(6, 2))
    source = admitted_prior_group_step(delta.source_group, proof_target=root, bridge=context)
    target = admitted_prior_group_step(delta.target_group, proof_target=root, bridge=context)
    for step, group in ((source, delta.source_group), (target, delta.target_group)):
        if (step is None or not verified_db_step(step, proof_target=root, bridge=context)
                or type(step.conclusion) is not Relation or step.conclusion.lhs != group
                or type(step.conclusion.rhs) is not FiniteCyclicGroup):
            raise RuntimeError('REQUIRED_FINITE_PRIOR_UNAVAILABLE:' + repr(group))
    a, b = source.conclusion, target.conclusion
    kernel = KernelMultipleStatement(delta, delta.source_group, a.rhs.generator, b.rhs.order)
    signed = TodaDeltaImageUpToSignStatement(delta, a.rhs.generator, b.rhs.generator)
    # This counterfactual free domain is a type probe only, not a mathematical premise.
    free = Relation(a.lhs, FreeCyclicGroup(a.rhs.generator), RelationType.EQUALITY)
    r35_finite = conditional_inputs(kernel, a, b, signed) is not None
    r35_free = conditional_inputs(kernel, free, b, signed) is not None
    r35_options = expand_cyclic_delta_kernel(kernel, (b, signed))
    provider = invocations[0]['expansion_provider']
    actual_calls = [options_record(options) for goal, options in calls if goal == kernel]
    source_records = signed_source_records(context, signed)
    exact_sources = [row for row in source_records if row['exact_signed_goal'] and row['linked_given_count']]
    accepted = lambda g: any(step.conclusion == g for step in result.proven_steps)
    injective = MapInjective(TodaHopfInvariantMap(TodaPrimaryGroup(8, 3), delta.source_group))
    if not accepted(injective) or not accepted(a):
        raise RuntimeError('R3R46R1_PROOF_REGRESSION')
    lifts = []
    for _, options in calls:
        for option in options:
            if option.rule.name != LIFT_RULE or kernel not in option.subgoals:
                continue
            record = options_record((option,))[0]
            if record not in lifts:
                lifts.append(record)
    if not lifts:
        raise RuntimeError('R3R44_LIFT_CANDIDATE_NOT_OBSERVED')
    latex, fallback = _group_proof_statement_latex(kernel)
    displayed = any(line.statement_latex == latex or any(seg.value == latex for seg in line.segments)
                    for line in view.rendered_lines) if latex is not None else False
    if (latex is None or fallback is not None or r'\langle' not in latex
            or (kernel in result.open_goals and not displayed)):
        raise RuntimeError('PUBLIC_KERNEL_DISPLAY_MISSING')
    if not actual_calls and not accepted(kernel):
        raise RuntimeError('KERNEL_FRONTIER_NOT_REACHED')
    if not r35_free or r35_finite:
        raise RuntimeError('REVIEWED_R35_TYPE_BOUNDARY_DRIFT')
    return {
        'gate': 'PASS_R3R47_FINITE_CYCLIC_KERNEL_FRONTIER',
        'status': result.status.value, 'web_key': view.key,
        'accepted_step_count': len(result.proven_steps),
        'open_goals': [repr(g) for g in result.open_goals],
        'domain_prior': repr(a), 'codomain_prior': repr(b),
        'domain_prior_accepted': accepted(a), 'codomain_prior_accepted': accepted(b),
        'domain_and_codomain_admission_verified': True,
        'kernel_goal': repr(kernel), 'kernel_proved': accepted(kernel),
        'kernel_actual_provider_calls': actual_calls,
        'kernel_independent_options': options_record(provider(kernel)),
        'signed_goal': repr(signed), 'signed_goal_accepted': accepted(signed),
        'signed_goal_independent_options': options_record(provider(signed)),
        'signed_exact_linked_given_count': len(exact_sources),
        'lemma57_and_matching_delta_source_records': source_records,
        'r35_accepts_finite_domain': r35_finite,
        'r35_accepts_counterfactual_free_domain': r35_free,
        'r35_counterfactual_options_not_proofs': options_record(r35_options),
        'lift_observed_premise_contracts': lifts,
        'lift_db_domain_rule': source.rule.value,
        'kernel_latex': latex, 'kernel_actual_web_display': displayed,
        'new_given_registrations': 0, 'new_math_rules': 0, 'full_pytest': 'NOT_RUN',
    }


def main():
    old, new = preflight()
    if old != new:
        raise RuntimeError('R3R47_DISPLAY_PATCH_NOT_APPLIED')
    report = observe()
    if TARGET.read_bytes() != old:
        raise RuntimeError('SOURCE_CHANGED_DURING_AUDIT')
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r47_finite_cyclic_kernel_frontier'
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / 'report.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for key, value in report.items():
        print('PHASE176_R3R47_' + key.upper() + '=' + json.dumps(value, ensure_ascii=False))
    print('REPORT=' + str(destination))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
