"""Read-only Phase 177 R13: observe existing proof search, never install a rule."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
import traceback

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, precedes_db_goal
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder, NonZeroGroupElement
from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
from phase175_r4r12r10r1_cited_511_public.provider import same_registered_cited_511
from phase175_r4r12r10r1_cited_511_public.source import canonical_511
from phase175_r4r12r13r4_hopf_zero_public.rule import hopf_zero_inputs, suspension_surjective_inputs
from phase177_r2_cited_511_reuse_audit.audit import capture, git, matches_blob, snapshot
from phase177_r7_left_composition_reuse_audit.audit import public_search, proof_record
from phase177_r9_delta_rhs_normalization_audit.audit import canonical_delta, route_matches
from proof import ProofRule, Relation

ROOT = Path(__file__).resolve().parents[1]
HEAD = '6482605898a83a3007565988c252cb594cef9a1d'
PINS = {
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase165_r52_r9_shared_math.py': 'b30a086b318ea9d78e9d5d3217f77a2c920ca8ca',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase175_r4r12_public_two_summand_quotient/provider.py': '1b34fe0d2707a51af7acc52eaa7d38209e90dfa2',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase175_r4r12r13r2_delta_injective_e_surjective/rule.py': '763b98521f8d78bbca1f07944194384c55a9ed57',
    'phase175_r4r12r13r3_public_delta_e_bridge/provider.py': '17657b9eb278c020cf484f1a31d87aad7997e05b',
    'phase175_r4r12r13r4_hopf_zero_public/rule.py': '74b7e8dee9032f5b0cbfc0086646bb423e73be74',
    'phase175_r4r12r9_delta_generator_image_bridge/rule.py': 'cfff81f4662825b78f30f8b7b4886cb27333b6c2',
    'phase175_r4r3_two_summand_quotient/rule.py': 'b854491dff8b42817c5e1fe2771e4f2dc2c16713',
    'phase177_r12_reassociation_transitivity_public/provider.py': 'a6ab33da710c6fd52a0f3ebdee8e31c82399c84a',
    'phase177_r12_reassociation_transitivity_public/tests/test_public.py': 'd96cd78eb12c78b1d3a9f3f13fee8cb1efe002d7',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase177_r7_left_composition_reuse_audit/audit.py': 'd0951ce94a0deba8106ff641d2394c9389341b0e',
    'phase177_r9_delta_rhs_normalization_audit/audit.py': 'be32e413a49e71f0a15585712b09c3249c1ee06d',
}


def preflight():
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT:
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    local, remote = git('rev-parse', 'HEAD'), git('rev-parse', 'origin/develop')
    if (local, remote) != (HEAD, HEAD):
        raise RuntimeError(f'REVIEWED_HEAD_REQUIRED:expected={HEAD};local={local};origin/develop={remote}')
    if git('status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('TRACKED_WORKTREE_NOT_CLEAN')
    for name, pin in PINS.items():
        if git('rev-parse', 'HEAD:'+name) != pin or not matches_blob((ROOT/name).read_bytes(), pin):
            raise RuntimeError('SOURCE_PIN_CHANGED:'+name)
    return {'head': HEAD, 'pins': PINS}


def same(left, right):
    return type(left) is type(right) and left == right


def option_records(options):
    return [{'rule': o.rule.name, 'subgoals': [repr(g) for g in o.subgoals]} for o in options]


def ancestors(steps):
    pending = list(steps)
    seen = set()
    while pending:
        step = pending.pop()
        if id(step) in seen:
            continue
        seen.add(id(step))
        yield step
        pending.extend(step.premises)


def actual_record(goal, calls, steps, open_goals):
    direct = [s for s in steps if same(s.conclusion, goal)]
    nested = [s for s in ancestors(steps) if same(s.conclusion, goal)]
    batches = [option_records(options) for requested, options in calls if same(requested, goal)]
    return {
        'goal': repr(goal),
        'accepted_direct': [proof_record(s) for s in direct],
        'accepted_in_tree': [proof_record(s) for s in nested],
        'listed_open': any(same(g, goal) for g in open_goals),
        'actual_provider_calls': batches,
        'actual_state': 'PROVED' if nested else ('REACHED_NOT_ACCEPTED' if batches else 'NOT_REACHED'),
    }


def inspect():
    invocation, result, calls, model, view = capture()
    root = invocation['goal']
    if (model is None or root.lhs != TodaPrimaryGroup(10, 5) or root.lhs != result.target
            or not isinstance(root.rhs, FiniteCyclicGroup) or root.rhs.order != 2):
        raise RuntimeError('ROOT_CAPTURE_MISMATCH')
    steps, open_goals = tuple(result.proven_steps), tuple(result.open_goals)
    def fresh():
        return shared_expansion_provider(invocation['bridge'], proof_target=root)
    cyclic = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    routes = expand_public_two_summand_quotient(cyclic, proof_target=root)
    if len(routes) != 2 or any(len(route.subgoals) != 6 for route in routes):
        raise RuntimeError('TWO_SIX_PREMISE_ROUTES_EXPECTED')
    chosen = [r for r in routes if delta_image_equality(r.subgoals[2]) is not None
              and route_matches(canonical_delta(), delta_image_equality(r.subgoals[2]))]
    if len(chosen) != 1:
        raise RuntimeError('CANONICAL_DELTA_ROUTE_NOT_UNIQUE')
    chosen = chosen[0]
    middle, delta_domain, image, exact, e_surj, e_image = chosen.subgoals
    h_zero, e_h = suspension_surjective_inputs(e_surj)
    injective, h_delta = hopf_zero_inputs(h_zero)
    if injective != MapInjective(TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4))):
        raise RuntimeError('LOWER_DELTA_DIMENSIONS_CHANGED')
    if not all(precedes_db_goal(n, k, 5, 5) for n, k in ((9, 1), (4, 4))):
        raise RuntimeError('LOWER_DELTA_DB_ORDER_INVALID')
    domain = exact_prior_database_result(9, 1)
    codomain = exact_prior_database_result(4, 4)
    if (not isinstance(domain, Relation) or domain.lhs != injective.map.source_group
            or not isinstance(domain.rhs, FiniteCyclicGroup) or domain.rhs.order != 2
            or not isinstance(codomain, Relation) or codomain.lhs != injective.map.target_group
            or not isinstance(codomain.rhs, DirectSumGroup)):
        raise RuntimeError('LOWER_DELTA_PRIOR_GROUP_SHAPE_CHANGED')
    # Select the actual registered summand using the existing cited identity check.
    lower_images = [GeneratorImage(injective.map, domain.rhs.generator, summand.generator)
                    for summand in codomain.rhs.summands if isinstance(summand, FiniteCyclicGroup)]
    matched_lower_images = [g for g in lower_images if delta_image_equality(g) is not None
                            and same_registered_cited_511(delta_image_equality(g))]
    lower_image = matched_lower_images[0] if len(matched_lower_images) == 1 else None
    probes = {
        'quotient_middle_group': middle,
        'quotient_delta_domain': delta_domain,
        'actual_delta_equality': delta_image_equality(image),
        'actual_delta_generator_image': image,
        'quotient_exactness': exact,
        'lower_delta_domain': domain,
        'lower_delta_codomain': codomain,
        'lower_delta_511_canonical_equality': canonical_511(),
        'lower_delta_injective': injective,
        'h_delta_exactness': h_delta,
        'hopf_zero': h_zero,
        'e_h_exactness': e_h,
        'suspension_surjective': e_surj,
        'surviving_suspension_image': e_image,
    }
    # A notation mismatch is a diagnostic result, not a reason to omit the other probes.
    if lower_image is not None:
        probes.update({
            'lower_delta_511_equality': delta_image_equality(lower_image),
            'lower_delta_511_generator_image': lower_image,
            'lower_delta_image_nonzero': NonZeroGroupElement(codomain.lhs, lower_image.target_generator),
            'lower_delta_image_order_two': FiniteElementOrder(codomain.lhs, lower_image.target_generator, 2),
        })
    else:
        for index, candidate in enumerate(lower_images):
            equality = delta_image_equality(candidate)
            if equality is not None:
                probes[f'lower_delta_db_equality_{index}'] = equality
                probes[f'lower_delta_db_generator_image_{index}'] = candidate
    report = {
        'lower_delta_511_registered_matches': len(matched_lower_images),
        'lower_delta_db_image_candidates': [repr(g) for g in lower_images],
        'root': repr(root), 'root_status': result.status.value, 'web_key': view.key,
        'open_goals': [repr(g) for g in open_goals], 'open_goal_count': len(open_goals),
        'accepted_steps': [proof_record(s) for s in steps],
        'citations': [repr(c) for c in model.citations],
        'lookup_mode': str(invocation['lookup_mode']),
        'quotient_root': actual_record(cyclic, calls, steps, open_goals),
        'quotient_candidates': [], 'probes': {},
    }
    provider = fresh()
    report['quotient_root']['fresh_options'] = option_records(provider(cyclic))
    for route in routes:
        report['quotient_candidates'].append({
            'cited_route': route is chosen,
            'rule': route.rule.name,
            'obligations': [actual_record(g, calls, steps, open_goals) for g in route.subgoals],
            'other_route_independent_search_required': False,
        })
    print('PHASE177_R13_ROOT_STATUS='+result.status.value, flush=True)
    print('PHASE177_R13_ROOT_OPEN_GOALS='+str(len(open_goals)), flush=True)
    print('PHASE177_R13_LOWER_DELTA_511_REGISTERED_MATCHES='+str(len(matched_lower_images)), flush=True)
    for label, goal in probes.items():
        print('PHASE177_R13_PROBE='+label, flush=True)
        actual = actual_record(goal, calls, steps, open_goals)
        current = fresh()
        options = option_records(current(goal))
        step, independent = public_search(goal, invocation, current)
        if step is not None and not same(step.conclusion, goal):
            raise RuntimeError('PROBE_CONCLUSION_MISMATCH:'+label)
        actual['fresh_options'] = options
        actual['independent_search_not_root_evidence'] = independent
        actual['independent_state'] = ('PROVED_'+step.rule.name if step is not None
                                       else ('OPEN_WITH_CANDIDATES' if options else 'OPEN_NO_CANDIDATES'))
        report['probes'][label] = actual
        print('PHASE177_R13_CASE='+label+':'+actual['actual_state']+':'+actual['independent_state'], flush=True)
    # R12 is a genuine regression guard, not an assertion that R13 is complete.
    if report['probes']['actual_delta_equality']['independent_state'] != 'PROVED_INFERENCE':
        raise RuntimeError('R12_ACTUAL_DELTA_REGRESSION')
    return report


def execute(dry_run):
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    base.mkdir(parents=True, exist_ok=True)
    path = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))/'report.json'
    report = {'phase': '177_R13', 'dry_run': dry_run, 'gate': 'FAIL_R13',
              'new_math_rules': 0, 'new_given': 0, 'full_pytest': 'NOT_RUN'}
    before = None
    try:
        before = snapshot()
        report['preflight'] = preflight()
        if not dry_run:
            report['observation'] = inspect()
        if snapshot() != before:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
        report['gate'] = 'PASS_R13_READ_ONLY_DRYRUN' if dry_run else 'PASS_R13_FRONTIER_OBSERVED_NOT_COMPLETION_GATE'
    except Exception as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        if before is not None:
            try:
                report['repository_unchanged'] = snapshot() == before
            except Exception:
                report['repository_unchanged'] = None
        print('PHASE177_R13_ERROR='+repr(exc), flush=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PHASE177_R13_REPORT='+str(path))
    print('PHASE177_R13_AUDIT_GATE='+report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    return execute(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
