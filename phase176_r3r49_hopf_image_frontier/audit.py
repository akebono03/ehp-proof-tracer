"""Read-only audit of the actual DB Hopf goal and a cited-notation control."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

from expression import Composition, HomotopyElement, MapApplication, Multiple
from homotopy_groups import TodaPrimaryGroup, TodaHopfInvariantMap
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import _nu_prime_element_alias
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement, canonical_quadruple_goal, expand_cited_quadruple,
)
from phase176_r3r39_public_equality_transport.source import right_hopf_transport_backward_plan
from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan
from phase176_r3r41_public_quadruple_connection.source import public_quadruple_backward_plan
from phase176_r3r48_cited_finite_delta_kernel.source import canonical_signed_delta
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
PINS = {
    'phase169_r3h_source_registry.py': '1829e3ac1381e10270dac73a196bfd4983540ea4',
    'phase176_r3r27r1_toda55_quadruple_isolated/source.py': '3e174ff8ffb656f069e1318591785bb7697c7736',
    'phase176_r3r30_generic_hopf_substitution_isolated/source.py': '143021313678b2c30157304c4102aa8fc9f42cc9',
    'phase176_r3r36_composite_right_hopf_isolated/source.py': 'c2dc7f2a2be1a68d8eccac57f12657ca149254d6',
    'phase176_r3r39_public_equality_transport/source.py': 'ec40a529afeb4fc8b372b88e30119877f2331c9b',
    'phase176_r3r40r1_eta_notation_bridge/source.py': 'cd802bbd907440bd8ccae6ee91322391a9f6a834',
    'phase176_r3r41_public_quadruple_connection/source.py': '79bb68a6bdddd29155d92ec027caeaf7a0ad821f',
    'phase175_r4r12r13r7_typed_nu_prime_notation/notation.py': '70ee0c0a00002f9946ac8d243097fd87b3e4c299',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase165_r52_r2_search_adapter.py': 'c1d08b803a4d9f9e4e1ad5180a1487422f1cd191',
}


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def preflight():
    from phase176_r3r48_cited_finite_delta_kernel.apply import planned_changes
    if any(old != new for old, new in planned_changes().values()):
        raise RuntimeError('R3R48_NOT_APPLIED')
    for name, pin in PINS.items():
        raw = (ROOT / name).read_bytes()
        lf = raw.replace(b'\r\n', b'\n')
        if pin not in (blob(raw), blob(lf), blob(lf.replace(b'\n', b'\r\n'))):
            raise RuntimeError('UNREVIEWED_DEPENDENCY:' + name)
        ast.parse(lf.decode('utf-8-sig'), filename=name)
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()


def option_record(options):
    return [{'rule': o.rule.name, 'subgoals': [repr(g) for g in o.subgoals]} for o in options]


def source_rows(bridge, alpha):
    """Read exact source availability; the alias predicate is diagnostic only."""
    rows = []
    for link in bridge.proof_links:
        step = link.step
        assertion = bridge.registry.assertion(link.assertion_id)
        if (step is None or step.rule is not ProofRule.GIVEN or step.premises
                or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or assertion.content != step.conclusion):
            continue
        item = step.conclusion
        if (type(item) is not Relation or item.relation_type is not RelationType.EQUALITY
                or type(item.lhs) is not MapApplication or item.lhs.map != EHP_H_MAP
                or type(item.lhs.expression) is not HomotopyElement
                or type(item.rhs) is not HomotopyElement):
            continue
        other = item.lhs.expression
        if (other.source, other.target) != (alpha.source, alpha.target):
            continue
        ref = bridge.registry.reference(assertion.reference_id)
        rows.append((item, {'assertion_id': link.assertion_id, 'locator': ref.locator,
                            'position': ref.publication_position, 'statement': repr(item),
                            'exact_alpha': other == alpha,
                            'strict_nu_prime_alias': _nu_prime_element_alias(other, alpha)}))
    return rows


def capture_web():
    """Observe the real R3R48 public search, preserving provider return values."""
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from web_group_proof import build_standard_web_group_proof_view
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
    return invocations[0], results[0], calls, view.key


def plan_probe(goal, available):
    """Compare the existing candidate builders without altering source objects."""
    forward = canonical_quadruple_goal(goal.rhs.expression.dimension)
    alpha = goal.lhs.expression.left
    gamma = goal.lhs.expression.right
    witnesses = tuple(x for x in available if type(x) is Relation
                      and x.relation_type is RelationType.EQUALITY
                      and x.lhs == MapApplication(EHP_H_MAP, alpha)
                      and type(x.rhs) is HomotopyElement)
    candidates = []
    for witness in witnesses:
        transported = Relation(goal.lhs, Composition(witness.rhs, gamma))
        candidates.append({'witness': repr(witness),
                           'witness_count': available.count(witness),
                           'transported': repr(transported),
                           'right_hopf_transport_steps': len(right_hopf_transport_backward_plan(transported, available)),
                           'connection_steps': len(connection_backward_plan(transported, forward, available)) if forward else 0})
    plan = public_quadruple_backward_plan(goal, available)
    return {'goal': repr(goal), 'exact_hopf_witness_count': len(witnesses),
            'canonical_quadruple_lhs_matches': forward is not None and forward.lhs == goal.rhs,
            'quadruple_candidate_count': len(expand_cited_quadruple(forward, available)) if forward else 0,
            'transport_candidates': candidates, 'public_plan_steps': len(plan),
            'public_plan': [{'goal': repr(g), **option_record((o,))[0]} for g, o in plan]}


def replay(goal, invocation):
    """Separate standalone DFS; its steps are NOT accepted root proof steps."""
    from phase165_r52_r9_shared_math import shared_expansion_provider
    bridge, root = invocation['bridge'], invocation['goal']
    provider = shared_expansion_provider(bridge, proof_target=root)
    calls, events = [], []

    def observe_provider(target):
        options = provider(target)
        calls.append({'goal': repr(target), 'options': option_record(options)})
        return options

    def observer(kind, target, step):
        events.append({'event': kind, 'goal': repr(target),
                       'rule': step.rule.value if step is not None else None,
                       'inference_rule': step.inference_rule.name if step is not None and step.inference_rule is not None else None})

    try:
        result = reconstruct_registered_goal(
            goal, bridge, invocation['citing_assertion_id'], observe_provider,
            lookup_mode=invocation['lookup_mode'],
            verified_assertion_ids=invocation.get('verified_assertion_ids', ()),
            progress_observer=observer,
        )
    except RegisteredGoalUnresolved as exc:
        return {'proved': False, 'error': str(exc), 'calls': calls, 'events': events}
    if result.conclusion != goal or result.rule is not ProofRule.INFERENCE:
        raise RuntimeError('STANDALONE_RESULT_NOT_EXACT_INFERENCE')
    return {'proved': True, 'calls': calls, 'events': events,
            'inference_rule': result.inference_rule.name}


def observe():
    invocation, result, calls, web_key = capture_web()
    bridge, root = invocation['bridge'], invocation['goal']
    signed = canonical_signed_delta()
    kernel = KernelMultipleStatement(signed.map, signed.map.source_group, signed.element, 4)
    injective = MapInjective(TodaHopfInvariantMap(TodaPrimaryGroup(8, 3), signed.map.source_group))
    if not any(s.conclusion == kernel and s.rule is ProofRule.INFERENCE for s in result.proven_steps):
        raise RuntimeError('R3R48_KERNEL_REGRESSION')
    if not any(s.conclusion == injective for s in result.proven_steps):
        raise RuntimeError('HOPF_INJECTIVITY_REGRESSION')
    generator = root.rhs.generator
    if type(generator) is not Composition or type(generator.right) is not Composition:
        raise RuntimeError('UNEXPECTED_ROOT_GENERATOR_SHAPE')
    alpha, gamma = generator.left, generator.right
    goal = Relation(MapApplication(EHP_H_MAP, generator), Multiple(4, signed.element))
    available = tuple(link.step.conclusion for link in bridge.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN
                      and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT)
    rows = source_rows(bridge, alpha)
    actual = plan_probe(goal, available)
    controls = [(item, record) for item, record in rows if record['locator'] == '(5.3)' and record['strict_nu_prime_alias']]
    control = None
    if len(controls) == 1:
        cited_alpha = controls[0][0].lhs.expression
        control_goal = Relation(MapApplication(EHP_H_MAP, Composition(cited_alpha, gamma)), goal.rhs)
        control = plan_probe(control_goal, available)
        control['standalone_dfs'] = replay(control_goal, invocation)
    actual['standalone_dfs'] = replay(goal, invocation)
    actual_calls = [option_record(options) for target, options in calls if target == goal]
    accepted = any(step.conclusion == goal for step in result.proven_steps)
    if not actual_calls and not accepted:
        raise RuntimeError('ACTUAL_HOPF_FRONTIER_NOT_REACHED')
    if (control is not None and not actual['exact_hopf_witness_count']
            and not actual['public_plan_steps'] and control['public_plan_steps']
            and control['standalone_dfs']['proved'] and not actual['standalone_dfs']['proved']):
        diagnosis = 'STRICT_NU_PRIME_NOTATION_BLOCKS_EXISTING_HOPF_PLAN'
    elif accepted:
        diagnosis = 'ACTUAL_WEB_HOPF_PROVED'
    else:
        diagnosis = 'FRONTIER_RECORDED_REQUIRES_FURTHER_INSPECTION'
    return {'gate': 'PASS_R3R49_HOPF_FRONTIER_AUDITED', 'diagnosis': diagnosis,
            'status': result.status.value, 'web_key': web_key, 'accepted_step_count': len(result.proven_steps),
            'open_goals': [repr(g) for g in result.open_goals], 'actual_root': repr(root),
            'actual_hopf_proved': accepted, 'actual_hopf_open': goal in result.open_goals,
            'actual_web_provider_calls': actual_calls, 'actual_alpha': repr(alpha),
            'actual_gamma': repr(gamma), 'source_rows': [record for _, record in rows],
            'prop22_count': available.count(TodaProp22RightFormula()),
            'toda55_count': available.count(Toda55UniversalQuadrupleStatement()),
            'eta_definition_count': available.count(TodaEtaFamilyGeneralDefinition()),
            'actual_probe': actual, 'canonical_control': control,
            'kernel_preserved': True, 'hopf_injective_preserved': True,
            'new_math_rules': 0, 'new_given_registrations': 0, 'full_pytest': 'NOT_RUN'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    head = preflight()
    if args.dry_run:
        print('PHASE176_R3R49_HEAD=' + head)
        print('PHASE176_R3R49_GATE=PASS_R3R49_DRYRUN')
        return 0
    report = observe()
    report['head'] = head
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / 'report.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for key, value in report.items():
        if key not in ('actual_probe', 'canonical_control'):
            print('PHASE176_R3R49_' + key.upper() + '=' + json.dumps(value, ensure_ascii=False))
    for key in ('actual_probe', 'canonical_control'):
        value = report[key]
        if value is not None:
            summary = {k: v for k, v in value.items() if k not in ('public_plan', 'standalone_dfs')}
            summary['standalone_proved'] = value['standalone_dfs']['proved']
            print('PHASE176_R3R49_' + key.upper() + '=' + json.dumps(summary, ensure_ascii=False))
    print('REPORT=' + str(destination))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
