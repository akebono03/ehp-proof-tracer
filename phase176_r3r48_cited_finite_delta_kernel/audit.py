"""Require an accepted kernel inference in the actual public Web proof search."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
from phase176_r3r48_cited_finite_delta_kernel.rule import RULE_NAME, linked_cited_steps
from phase176_r3r48_cited_finite_delta_kernel.source import canonical_signed_delta
from proof import ProofRule


def observe():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from web_group_proof import build_standard_web_group_proof_view
    from phase165_r14_r6_generic_iso import MapInjective
    from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup

    invocations, results, calls = [], [], []
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
        provider = kwargs['expansion_provider']
        forwarded = dict(kwargs)

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
    signed = canonical_signed_delta()
    delta = signed.map
    a = admitted_prior_group_step(delta.source_group, proof_target=root, bridge=context)
    b = admitted_prior_group_step(delta.target_group, proof_target=root, bridge=context)
    if a is None or b is None or not all(verified_db_step(x, proof_target=root, bridge=context) for x in (a,b)):
        raise RuntimeError('PRIOR_ADMISSION_FAILED')
    if (a.conclusion.rhs.order, b.conclusion.rhs.order) != (8,4):
        raise RuntimeError('EXPECTED_PRIOR_ORDERS_CHANGED')
    kernel = KernelMultipleStatement(delta, delta.source_group, signed.element, b.conclusion.rhs.order)
    cited = linked_cited_steps(context, signed)
    if len(cited) != 1:
        raise RuntimeError('SIGNED_SOURCE_NOT_UNIQUE')
    matches = [s for s in result.proven_steps if s.conclusion == kernel]
    if not matches:
        raise RuntimeError('PUBLIC_KERNEL_NOT_PROVED')
    step = matches[0]
    if (step.rule is not ProofRule.INFERENCE or step.inference_rule is None
            or step.inference_rule.name != RULE_NAME or len(step.premises) != 3
            or tuple(x.conclusion for x in step.premises) != (a.conclusion,b.conclusion,signed)
            or not all(verified_db_step(x, proof_target=root, bridge=context) for x in step.premises[:2])
            or step.premises[2] != cited[0]):
        raise RuntimeError('PUBLIC_KERNEL_PREMISE_PROVENANCE_FAILED')
    if not any(g == kernel and any(o.rule.name == RULE_NAME for o in opts) for g,opts in calls):
        raise RuntimeError('PUBLIC_KERNEL_PROVIDER_NOT_REACHED')
    if any(s.rule is ProofRule.GIVEN and s.conclusion == kernel for s in result.proven_steps):
        raise RuntimeError('KERNEL_GIVEN_FORBIDDEN')
    injective = MapInjective(TodaHopfInvariantMap(TodaPrimaryGroup(8,3), delta.source_group))
    if not any(s.conclusion == injective for s in result.proven_steps):
        raise RuntimeError('HOPF_INJECTIVITY_REGRESSION')
    return {'gate':'PASS_R3R48_PUBLIC_FINITE_CYCLIC_KERNEL', 'status':result.status.value,
            'web_key':view.key, 'accepted_step_count':len(result.proven_steps),
            'open_goals':[repr(g) for g in result.open_goals],
            'kernel_goal':repr(kernel), 'kernel_proved':True, 'kernel_proof_rule':step.rule.value,
            'kernel_rule':RULE_NAME, 'kernel_premises':[repr(s.conclusion) for s in step.premises],
            'domain_prior_verified':True, 'codomain_prior_verified':True,
            'signed_given_verified':True, 'kernel_order':a.conclusion.rhs.order//b.conclusion.rhs.order,
            'hopf_injective_proved':True, 'new_given_registrations':1, 'new_math_rules':1,
            'full_pytest':'NOT_RUN'}


def main():
    report = observe()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r48_cited_finite_delta_kernel'
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / 'report.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key,value in report.items():
        print('PHASE176_R3R48_'+key.upper()+'='+json.dumps(value,ensure_ascii=False))
    print('REPORT='+str(destination))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
