"""Observe existing left-composition search, without installing a provider."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
import traceback

from expression import Composition, HomotopyElement, IteratedSuspension
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase175_r4r12r10r1_cited_511_public.source import canonical_511
from phase177_r2_cited_511_reuse_audit.audit import capture, git, matches_blob, snapshot
from phase177_r4_general_iterated_suspension_audit.audit import cases
from proof import ProofRule, Relation, RelationType, apply_inference_match, find_inference_matches_for_rule
from relation_rules import equality_preserved_under_left_composition_inference_rule

ROOT = Path(__file__).resolve().parents[1]
HEAD = '59d7a79aa632dbc5d1999b8478361cebd77df540'
LEFT_RULE = 'equality preserved under left composition'
PINS = {
    'phase165_r52_r9_shared_math.py': '43e9785c262653f223c1c5f905310c40b4116774',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'relation_rules.py': '0da057f35b7ebd51b31c247e04bc4b15b1dcff9e',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase176_r3r39_public_equality_transport/source.py': 'ec40a529afeb4fc8b372b88e30119877f2331c9b',
    'phase176_r3r39_public_equality_transport/tests/test_source.py': 'ef06b5b6a9e8a75f89d52262eaaee7949b2fa034',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase177_r3_unsigned_delta_composition_isolated/rule.py': '485591c14c2b1bbdb5b3486ac3fd5797ec89caf6',
    'phase177_r4_general_iterated_suspension_audit/audit.py': '9062bb1fa05e57b371699d81b92816d65ddd7ed0',
    'phase177_r5_general_suspension_equality_isolated/rule.py': 'f8f94381103bf133393caf9c28ec18dfb8a7a006',
    'phase177_r6_general_suspension_public/provider.py': 'd996b74261f3bd6cc439cb6baaf70579b8435bc9',
    'phase177_r6_general_suspension_public/tests/test_public.py': '5da873f103314b83e751dae6e7d8b7c988984a66',
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


def composition_target(alpha, premise):
    """Construct only a well-typed, same-left composition audit target."""
    if type(premise) is not Relation or premise.relation_type is not RelationType.EQUALITY:
        raise ValueError('EQUALITY_REQUIRED')
    a, b, c = map(typed_endpoints, (alpha, premise.lhs, premise.rhs))
    if a is None or b is None or c != b or a[0] != b[1]:
        raise ValueError('COMPOSABLE_TYPED_ENDPOINTS_REQUIRED')
    target = Relation(Composition(alpha, premise.lhs), Composition(alpha, premise.rhs))
    if typed_endpoints(target.lhs) != (b[0], a[1]) or typed_endpoints(target.rhs) != (b[0], a[1]):
        raise ValueError('COMPOSITION_ENDPOINTS_CHANGED')
    return target


def audit_cases():
    """Real R6 premises and arbitrary typed left factors, not new GIVENs."""
    result = {}
    for label in ('eta', 'nu_cited', 'sigma_cited', 'epsilon_cited', 'formal_stable', 'formal_unstable'):
        x, _, z = cases()[label]
        if label.startswith('formal_'):
            from expression import Suspension
            premise = Relation(Suspension(Suspension(x)), IteratedSuspension(x, 2))
        else:
            premise = Relation(IteratedSuspension(x, 2), z)
        degree = typed_endpoints(premise.lhs)[1]
        alpha = (canonical_511().lhs.expression if label == 'eta' else
                 HomotopyElement('audit_left_'+label, 2, degree, 2))
        result[label] = (alpha, premise, composition_target(alpha, premise))
    return result


def rule_name(step):
    return step.inference_rule.name if step.inference_rule is not None else None


def proof_record(step):
    """Report actual chosen proof nodes, including reference leaves."""
    return {'conclusion': repr(step.conclusion), 'trust': step.rule.name,
            'rule': rule_name(step), 'premises': [proof_record(p) for p in step.premises]}


def public_search(target, invocation, provider):
    """Normal source-first DFS, never supplied a test proof or injected proposal."""
    calls = []
    def observed(goal):
        options = provider(goal)
        if type(goal) is type(target) and goal == target:
            calls.append([{'rule': o.rule.name, 'subgoals': [repr(g) for g in o.subgoals]}
                          for o in options])
        return options
    try:
        step = reconstruct_registered_goal(
            target, invocation['bridge'], invocation['citing_assertion_id'], observed,
            lookup_mode=invocation['lookup_mode'],
            verified_assertion_ids=invocation.get('verified_assertion_ids', ()),
            completed_internal_proofs=invocation.get('completed_internal_proofs', ()),
        )
    except RegisteredGoalUnresolved as exc:
        return None, {'proved': False, 'error': str(exc), 'target_calls': calls}
    if type(step.conclusion) is not type(target) or step.conclusion != target:
        raise RuntimeError('PUBLIC_WRONG_CONCLUSION')
    return step, {'proved': True, 'target_calls': calls, 'proof': proof_record(step)}


def replay_left(alpha, premise_step, target):
    """Independently replay the existing inference with an actual DFS premise."""
    if premise_step.rule is not ProofRule.INFERENCE:
        raise RuntimeError('INFERRED_PREMISE_REQUIRED')
    if composition_target(alpha, premise_step.conclusion) != target:
        raise RuntimeError('LEFT_TARGET_MISMATCH')
    rule = equality_preserved_under_left_composition_inference_rule(alpha)
    for match in find_inference_matches_for_rule(rule, (premise_step,)):
        step = apply_inference_match(match)
        if (step.conclusion == target and step.rule is ProofRule.INFERENCE
                and len(step.premises) == 1 and step.premises[0] is premise_step):
            return step
    raise RuntimeError('EXISTING_LEFT_RULE_REPLAY_FAILED')


def classify(premise_proved, isolated_replayed, public_proved, candidate_present):
    if public_proved:
        return 'PUBLIC_COMPOSITION_PROVED'
    if not premise_proved:
        return 'PREMISE_FRONTIER'
    if not isolated_replayed:
        return 'EXISTING_RULE_REPLAY_FRONTIER'
    if candidate_present:
        return 'PUBLIC_CANDIDATE_REPLAY_FRONTIER'
    return 'PUBLIC_BACKWARD_CONNECTION_FRONTIER'


def has_exact_candidate(row, premise):
    return any(o['rule'] == LEFT_RULE and o['subgoals'] == [repr(premise)]
               for batch in row['target_calls'] for o in batch)


def observe():
    invocation, result, calls, model, view = capture()
    if model is None or invocation['goal'].lhs != result.target:
        raise RuntimeError('PUBLIC_CAPTURE_CONTEXT_MISMATCH')
    def fresh():
        return shared_expansion_provider(invocation['bridge'], proof_target=invocation['goal'])
    report = {'root_status': result.status.value, 'root': repr(invocation['goal']),
              'root_open_goals': [repr(g) for g in result.open_goals], 'web_key': view.key,
              'cases': {}, 'new_math_rules': 0, 'new_given_registrations': 0,
              'delta_connection': 'NOT_ADDED'}
    print('PHASE177_R7_ROOT_STATUS='+result.status.value, flush=True)
    print('PHASE177_R7_ROOT_OPEN_GOALS='+str(len(result.open_goals)), flush=True)
    for label, (alpha, premise, target) in audit_cases().items():
        premise_step, premise_row = public_search(premise, invocation, fresh())
        if premise_step is None:
            raise RuntimeError('R6_PREMISE_REGRESSION:'+label)
        replay = replay_left(alpha, premise_step, target)
        public_step, public_row = public_search(target, invocation, fresh())
        inferred = public_step is not None and public_step.rule is ProofRule.INFERENCE
        if public_step is not None and not inferred:
            raise RuntimeError('UNEXPECTED_PUBLIC_TRUST:'+label)
        candidate = has_exact_candidate(public_row, premise)
        state = classify(True, True, inferred, candidate)
        report['cases'][label] = {'diagnosis': state, 'premise': premise_row,
                                  'isolated_existing_rule_replay_not_public_evidence': proof_record(replay),
                                  'public': public_row, 'exact_left_candidate_present': candidate}
        print('PHASE177_R7_CASE='+label+':'+state, flush=True)
    # Independent use of the provider captured during the actual root search.
    # The result is not accepted as evidence for the original root proof.
    _, premise, target = audit_cases()['eta']
    step, row = public_search(target, invocation, invocation['expansion_provider'])
    if step is not None and step.rule is not ProofRule.INFERENCE:
        raise RuntimeError('UNEXPECTED_CAPTURED_PUBLIC_TRUST')
    report['captured_provider_independent_probe'] = row
    print('PHASE177_R7_CAPTURED_ETA_COMPOSITION_PROVED='+str(step is not None).upper(), flush=True)
    return report


def execute(dry_run):
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    base.mkdir(parents=True, exist_ok=True)
    path = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))/'report.json'
    report = {'phase': '177_R7', 'dry_run': dry_run, 'gate': 'FAIL_R7', 'full_pytest': 'NOT_RUN'}
    try:
        before = snapshot()
        report['preflight'] = preflight()
        if not dry_run:
            report['observation'] = observe()
        if snapshot() != before:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
        report['gate'] = 'PASS_R7_READ_ONLY_DRYRUN' if dry_run else 'PASS_R7_LEFT_COMPOSITION_REUSE_AUDITED'
    except Exception as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        print('PHASE177_R7_ERROR='+repr(exc))
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PHASE177_R7_REPORT='+str(path))
    print('PHASE177_R7_NEW_MATH_RULES=0')
    print('PHASE177_R7_NEW_GIVEN=0')
    print('PHASE177_R7_DELTA_CONNECTION=NOT_ADDED')
    print('PHASE177_R7_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R7_GATE='+report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    return execute(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
