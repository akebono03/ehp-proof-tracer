"""Read-only R4 audit: distinguish one-step images from iterated equalities."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
import traceback

from phase177_r2_cited_511_reuse_audit.audit import (
    capture, git, replay_source, snapshot, matches_blob,
)

ROOT = Path(__file__).resolve().parents[1]
HEAD = '1578f128b960c555376f8c477bbb688890d37c74'
PINS = {
    'phase165_r52_r9_shared_math.py': '87e0fe1202fa265c7530d0dd7e2b0adda2f5ebc2',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase165_r12_r21_eta_generator_chain.py': '1620c97b00637f72d13cabe6490e5561263c5ea5',
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
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
    for path, pin in PINS.items():
        if git('rev-parse', 'HEAD:' + path) != pin or not matches_blob((ROOT/path).read_bytes(), pin):
            raise RuntimeError('SOURCE_PIN_CHANGED:' + path)
    return {'head': HEAD, 'pins': PINS}


def family_member(family, index):
    from expression import GeneratorSymbol, HomotopyElement
    return HomotopyElement(family.name_at(index), index, index + family.stem,
                           index, GeneratorSymbol(family.symbol_family, index))


def cases():
    from expression import HomotopyElement, IteratedSuspension
    from phase169_r10b_registered_stable_family_binding.family_registry import read_registered_stable_families
    rows = {r.family_id: r for r in read_registered_stable_families()}
    result = {}
    for label, identifier, n in (('eta', 2, 8), ('nu_cited', 4, 4),
                                  ('sigma_cited', 9, 8), ('epsilon_cited', 10, 3)):
        family = rows[identifier]
        if n < family.minimum_n:
            raise RuntimeError('CASE_BELOW_FAMILY_DEFINITION:' + label)
        result[label] = tuple(family_member(family, n+i) for i in range(3))
    for label, x in (('formal_stable', HomotopyElement('audit_x', 16, 30, 16)),
                     ('formal_unstable', HomotopyElement('audit_y', 3, 6, 3))):
        result[label] = (x, IteratedSuspension(x, 1), IteratedSuspension(x, 2))
    return result


def span(value):
    from expression import Suspension, IteratedSuspension
    from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
    if isinstance(value, Suspension):
        a = span(value.expression)
        return None if a is None else (a[0]+1, a[1]+1)
    if isinstance(value, IteratedSuspension):
        if type(value.exponent) is not int or value.exponent < 0:
            return None
        a = span(value.expression)
        return None if a is None else (a[0]+value.exponent, a[1]+value.exponent)
    return typed_element_span(value)


def image(x, y):
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    a, b = span(x), span(y)
    if a is None or b != (a[0]+1, a[1]+1):
        raise ValueError('not consecutive typed suspension endpoints')
    return GeneratorImage(TodaSuspensionMap(TodaPrimaryGroup(*a), TodaPrimaryGroup(*b)), x, y)


def goals(x, y, z):
    from expression import IteratedSuspension, Suspension
    from proof import Relation
    if span(x) is None or span(y) is None or span(z) is None:
        raise ValueError('untyped audit case')
    return {
        'first_image': image(x, y),
        'second_image': image(y, z),
        'first_equality': Relation(Suspension(x), y),
        'second_equality': Relation(Suspension(y), z),
        'double_equality': Relation(IteratedSuspension(x, 2), z),
        'nested_to_iterated': Relation(Suspension(Suspension(x)), IteratedSuspension(x, 2)),
    }


def classify(rows):
    if rows['double_equality'].get('reflexive'):
        return ('FORMAL_ITERATION_REUSABLE' if rows['nested_to_iterated']['proved']
                else 'FORMAL_ITERATED_NOTATION_FRONTIER')
    if rows['double_equality']['proved']:
        return 'DOUBLE_EQUALITY_REUSABLE'
    if not all(rows[key]['proved'] for key in ('first_image', 'second_image')):
        return 'ONE_STEP_IMAGE_FRONTIER'
    if not all(rows[key]['proved'] for key in ('first_equality', 'second_equality')):
        return 'IMAGE_TO_EQUALITY_FRONTIER'
    if not rows['nested_to_iterated']['proved']:
        return 'ITERATED_NOTATION_FRONTIER'
    return 'DOUBLE_EQUALITY_SEARCH_OR_COMPOSITION_FRONTIER'


def observe():
    from expression import Composition, IteratedSuspension
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase175_r4r12r10r1_cited_511_public.source import canonical_511
    from proof import Relation
    invocation, result, calls, model, view = capture()
    if model is None or invocation['goal'].lhs != result.target:
        raise RuntimeError('PUBLIC_CAPTURE_CONTEXT_MISMATCH')
    bridge = invocation['bridge']
    root = invocation['goal']
    report = {'root_status': result.status.value, 'web_key': view.key,
              'root_open_goals': [repr(g) for g in result.open_goals],
              'cases': {}, 'new_math_rules': 0, 'new_given_registrations': 0}
    for label, values in cases().items():
        targets = goals(*values)
        rows = {}
        for name, target in targets.items():
            # The formal double equality is reflexive; record it, not as evidence
            # of transport. The non-reflexive nested form is a separate probe.
            fresh = shared_expansion_provider(bridge, proof_target=root)
            row = replay_source(target, dict(invocation, expansion_provider=fresh))
            row['goal'] = repr(target)
            row['reflexive'] = isinstance(target, Relation) and target.lhs == target.rhs
            rows[name] = row
        report['cases'][label] = {'diagnosis': classify(rows), 'probes': rows}
        print('PHASE177_R4_CASE='+label+':'+classify(rows), flush=True)
    # Reuse the actual captured public provider for the precise R3 obligations.
    x, _, z = cases()['eta']
    alpha = canonical_511().lhs.expression
    exact = {
        'eta_double': Relation(IteratedSuspension(x, 2), z),
        'composition_identity': Relation(Composition(alpha, IteratedSuspension(x, 2)),
                                         Composition(alpha, z)),
    }
    report['actual_public_provider_independent_probes'] = {
        name: replay_source(target, invocation) for name, target in exact.items()
    }
    return report


def execute(dry_run):
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / Path(__file__).parent.name
    base.mkdir(parents=True, exist_ok=True)
    path = Path(tempfile.mkdtemp(prefix='attempt_', dir=base)) / 'report.json'
    report = {'phase': '177_R4', 'dry_run': dry_run, 'full_pytest': 'NOT_RUN', 'gate': 'FAIL_R4'}
    try:
        before = snapshot()
        report['preflight'] = preflight()
        if not dry_run:
            report['observation'] = observe()
        if snapshot() != before:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
        report['gate'] = 'PASS_R4_READ_ONLY_DRYRUN' if dry_run else 'PASS_R4_GENERAL_ITERATED_SUSPENSION_AUDITED'
    except Exception as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        print('PHASE177_R4_ERROR='+repr(exc))
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PHASE177_R4_REPORT='+str(path))
    print('PHASE177_R4_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R4_GATE='+report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    return execute(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
