"""Distinguish reassociation, typed notation, and equality transport frontiers."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
import traceback

from expression import Composition, HomotopyElement, IteratedSuspension, MapApplication, Suspension
from map_facts import EHP_DELTA_MAP
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase174_r3_r7_r9_composition_associativity.rule import expand_generator_image_associativity
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
from phase175_r4r12r10r1_cited_511_public.source import canonical_511
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import same_typed_generator_notation
from phase176_r3r50_strict_nu_prime_connection.notation import strict_nu_prime_alias
from phase177_r2_cited_511_reuse_audit.audit import capture, git, matches_blob, snapshot
from phase177_r4_general_iterated_suspension_audit.audit import cases
from phase177_r7_left_composition_reuse_audit.audit import public_search, proof_record
from phase177_r8_unsigned_delta_public.provider import build_public_unsigned_delta_provider
from proof import ProofRule, Relation, apply_inference_match, find_inference_matches_for_rule
from relation_rules import equality_transitivity_inference_rule

ROOT = Path(__file__).resolve().parents[1]
HEAD = '8127b7b6424f294a6e03b3e2d12e66a83e77cf5d'
PINS = {
    'phase165_r52_r9_shared_math.py': 'cb89639e7ee2088cf5bb2cf0f1aeaf10cebaf9fb',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'relation_rules.py': '0da057f35b7ebd51b31c247e04bc4b15b1dcff9e',
    'phase174_r3_r7_r9_composition_associativity/rule.py': '2c44c68be90cb761d7bdd35e29f23977b5f93a2e',
    'phase174_r3_r7_r9_composition_associativity/tests/test_rule.py': 'f23fda6f5da69c7bc04fe6493f295d3105b0d807',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase175_r4r12_public_two_summand_quotient/provider.py': '1b34fe0d2707a51af7acc52eaa7d38209e90dfa2',
    'phase175_r4r12r9_delta_generator_image_bridge/rule.py': 'cfff81f4662825b78f30f8b7b4886cb27333b6c2',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase175_r4r12r13r7_typed_nu_prime_notation/notation.py': '70ee0c0a00002f9946ac8d243097fd87b3e4c299',
    'phase175_r4r12r13r7_typed_nu_prime_notation/tests/test_r13r7_notation.py': 'ca8020fca46eabfeccee639d35cc77371b4451c8',
    'phase176_r3r50_strict_nu_prime_connection/notation.py': '2ed8c8b3ee8324ad7f37a61371e8b7323f2bd85c',
    'phase176_r3r50_strict_nu_prime_connection/tests/test_notation_connection.py': '2aee4ed00cabbc01cf9b79a727ec4a6e74bbcdc9',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase177_r3_unsigned_delta_composition_isolated/rule.py': '485591c14c2b1bbdb5b3486ac3fd5797ec89caf6',
    'phase177_r4_general_iterated_suspension_audit/audit.py': '9062bb1fa05e57b371699d81b92816d65ddd7ed0',
    'phase177_r7_left_composition_reuse_audit/audit.py': 'd0951ce94a0deba8106ff641d2394c9389341b0e',
    'phase177_r8_unsigned_delta_public/provider.py': '3243162cfd334e7b71a67753603e3ef5f63237f7',
    'phase177_r8_unsigned_delta_public/tests/test_public.py': '340ad0932ee3df000c5ceec6df76880fe77db562',
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


def canonical_delta():
    base = canonical_511()
    beta, _, gamma = cases()['eta']
    return Relation(MapApplication(EHP_DELTA_MAP, Composition(base.lhs.expression, gamma)),
                    Composition(base.rhs, beta))


def flatten_typed(value):
    """Diagnostic factor list only, never a ProofStep or equality rule."""
    if typed_endpoints(value) is None:
        return None
    if type(value) is Composition:
        left, right = flatten_typed(value.left), flatten_typed(value.right)
        return None if left is None or right is None else left+right
    return (value,)


def route_matches(canonical, target):
    """Locate the exact strict notation variant; do not certify its equality."""
    a, b = flatten_typed(canonical.rhs), flatten_typed(target.rhs)
    return (canonical.lhs == target.lhs and a is not None and b is not None
            and len(a) == len(b) == 3 and a[1:] == b[1:]
            and type(a[0]) is Suspension and type(b[0]) is IteratedSuspension
            and type(b[0].exponent) is int and b[0].exponent == 1
            and strict_nu_prime_alias(a[0].expression, b[0].expression)
            and same_typed_generator_notation(a[0], b[0]))


def probe_goals(canonical, actual):
    """Change one representation feature at a time, keeping exact endpoints."""
    if not route_matches(canonical, actual):
        raise ValueError('EXPECTED_STRICT_ROUTE_VARIANT')
    a, b, c = flatten_typed(canonical.rhs)
    d, _, _ = flatten_typed(actual.rhs)
    if canonical.rhs != Composition(Composition(a,b),c) or actual.rhs != Composition(d,Composition(b,c)):
        raise ValueError('EXPECTED_LEFT_TO_RIGHT_ASSOCIATION')
    canon_atom, db_atom = a.expression, d.expression
    pair = Composition(b,c)
    right = Composition(a,pair)
    wrapper = IteratedSuspension(canon_atom,1)
    db_ordinary = Suspension(db_atom)
    wrapper_rhs = Composition(wrapper,pair)
    db_left = Composition(Composition(d,b),c)
    x = HomotopyElement('audit_a',3,5,3)
    y = HomotopyElement('audit_b',5,6,5)
    z = HomotopyElement('audit_c',6,9,6)
    delta = lambda rhs: Relation(canonical.lhs, rhs)
    probes = {
        'generic_associativity': Relation(Composition(Composition(x,y),z),Composition(x,Composition(y,z))),
        'canonical_associativity': Relation(canonical.rhs,right),
        'reverse_associativity': Relation(right,canonical.rhs),
        'one_suspension_wrapper': Relation(wrapper,a),
        'reverse_one_suspension_wrapper': Relation(a,wrapper),
        'nu_prime_atom_notation': Relation(canon_atom,db_atom),
        'same_wrapper_nu_prime_notation': Relation(a,db_ordinary),
        'exact_suspended_nu_prime_notation': Relation(a,d),
        'wrapper_only_rhs': Relation(right,wrapper_rhs),
        'same_parentheses_rhs_notation': Relation(right,actual.rhs),
        'entire_rhs_equality': Relation(canonical.rhs,actual.rhs),
        'canonical_delta': canonical,
        'reassociated_delta': delta(right),
        'wrapper_only_delta': delta(wrapper_rhs),
        'notation_only_delta': delta(db_left),
        'actual_delta': actual,
    }
    for name, goal in probes.items():
        if name.endswith('_delta'):
            if typed_endpoints(goal.rhs) != typed_endpoints(canonical.rhs):
                raise ValueError('DELTA_VALUE_TYPE_CHANGED:'+name)
        elif typed_endpoints(goal.lhs) is None or typed_endpoints(goal.lhs) != typed_endpoints(goal.rhs):
            raise ValueError('EQUALITY_TYPE_CHANGED:'+name)
    return probes


def replay_transitivity(first, second, target):
    """Use only actual search proofs, not synthetic or assumed parents."""
    if first is None or second is None:
        return None
    if first.rule is not ProofRule.INFERENCE or second.rule is not ProofRule.INFERENCE:
        return None
    rule = equality_transitivity_inference_rule()
    for match in find_inference_matches_for_rule(rule, (first,second)):
        step = apply_inference_match(match)
        if (step.conclusion == target and step.rule is ProofRule.INFERENCE
                and len(step.premises) == 2 and step.premises[0] is first and step.premises[1] is second):
            return step
    return None


def status(row):
    if row['proved']:
        return 'PROVED'
    if any(row['target_calls']):
        return 'CANDIDATES_UNRESOLVED'
    return 'NO_CANDIDATES'


def observe():
    invocation, result, calls, model, view = capture()
    if model is None or invocation['goal'].lhs != result.target:
        raise RuntimeError('PUBLIC_CAPTURE_CONTEXT_MISMATCH')
    root, bridge = invocation['goal'], invocation['bridge']
    def fresh():
        return shared_expansion_provider(bridge, proof_target=root)
    canonical = canonical_delta()
    routes = expand_public_two_summand_quotient(
        CyclicStructureStatement(root.lhs,root.rhs.generator,2), proof_target=root)
    if len(routes) != 2:
        raise RuntimeError('TWO_QUOTIENT_ROUTES_EXPECTED')
    selected = []
    route_rows = []
    for index, route in enumerate(routes):
        image = route.subgoals[2]
        target = delta_image_equality(image)
        if target is None:
            raise RuntimeError('DELTA_IMAGE_NOT_TYPED')
        matched = route_matches(canonical,target)
        route_rows.append({'index': index, 'target': repr(target), 'strict_notation_match': matched,
                           'existing_suspension_image_associativity_candidates': len(expand_generator_image_associativity(image))})
        if matched:
            selected.append((index,target))
    if len(selected) != 1:
        raise RuntimeError('STRICT_ROUTE_DIAGNOSTIC_REQUIRES_REVIEW')
    index, actual = selected[0]
    report = {'root_status': result.status.value, 'root': repr(root), 'web_key': view.key,
              'root_open_goals': [repr(g) for g in result.open_goals], 'routes': route_rows,
              'strict_notation_route_index': index, 'independent_probes_not_root_evidence': {}}
    print('PHASE177_R9_ROOT_STATUS='+result.status.value, flush=True)
    print('PHASE177_R9_ROOT_OPEN_GOALS='+str(len(result.open_goals)), flush=True)
    print('PHASE177_R9_STRICT_NOTATION_ROUTE='+str(index), flush=True)
    targets = probe_goals(canonical,actual)
    steps = {}
    unsigned = build_public_unsigned_delta_provider(bridge)
    for name, target in targets.items():
        step, row = public_search(target, invocation, fresh())
        row['trust'] = None if step is None else step.rule.name
        row['goal'] = repr(target)
        row['status'] = status(row)
        if name.endswith('_delta'):
            row['direct_R8_candidates'] = [{'rule': o.rule.name, 'subgoals': [repr(s) for s in o.subgoals]} for o in unsigned(target)]
        steps[name] = step
        report['independent_probes_not_root_evidence'][name] = row
        print('PHASE177_R9_PROBE='+name+':'+row['status'], flush=True)
    if steps['canonical_delta'] is None or steps['canonical_delta'].rule is not ProofRule.INFERENCE:
        raise RuntimeError('R8_CANONICAL_DELTA_REGRESSION')
    for name, first, second, target in (
        ('reassociated_delta', 'canonical_delta', 'canonical_associativity', targets['reassociated_delta']),
        ('actual_delta', 'canonical_delta', 'entire_rhs_equality', actual),
    ):
        replay = replay_transitivity(steps[first],steps[second],target)
        report.setdefault('isolated_transitivity_not_public_evidence',{})[name] = None if replay is None else proof_record(replay)
        print('PHASE177_R9_TRANSITIVITY='+name+':'+('REPLAYED' if replay is not None else 'NOT_REPLAYED'),flush=True)
    step,row = public_search(actual,invocation,invocation['expansion_provider'])
    if step is not None and step.rule is not ProofRule.INFERENCE:
        raise RuntimeError('UNEXPECTED_CAPTURED_TRUST')
    report['captured_provider_independent_probe_not_root_evidence'] = row
    print('PHASE177_R9_CAPTURED_ACTUAL_DELTA='+status(row),flush=True)
    return report


def execute(dry_run):
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    base.mkdir(parents=True,exist_ok=True)
    path = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))/'report.json'
    report = {'phase':'177_R9','dry_run':dry_run,'gate':'FAIL_R9','full_pytest':'NOT_RUN'}
    try:
        before = snapshot()
        report['preflight'] = preflight()
        if not dry_run:
            report['observation'] = observe()
        if snapshot() != before:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
        report['gate'] = 'PASS_R9_READ_ONLY_DRYRUN' if dry_run else 'PASS_R9_DELTA_RHS_NORMALIZATION_AUDITED'
    except Exception as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc())
        print('PHASE177_R9_ERROR='+repr(exc))
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PHASE177_R9_REPORT='+str(path))
    print('PHASE177_R9_NEW_MATH_RULES=0')
    print('PHASE177_R9_NEW_GIVEN=0')
    print('PHASE177_R9_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R9_GATE='+report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    return execute(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
