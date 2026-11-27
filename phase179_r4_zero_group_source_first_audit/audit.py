"""Measure the actual public n=3,k=7 zero-group route; no proof insertion."""
from __future__ import annotations

import argparse
import copy
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

from phase178_r1_k6_source_first_audit import audit as common
from phase179_r1_source_first_audit import audit as r1

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = 'c9036499d38bff8f03b26446995319fbb4ffb649'
PREFIX = 'PHASE179_R4_'
PINS = {
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'phase165_r52_r9_shared_math.py': 'ec76955d1d36e0d8cd9f92a6733d97bcfd4a6d2b',
    'phase179_r1_source_first_audit/audit.py': '8bc6a616e466803836623fd20b5a5a9f4b9ae201',
    'phase165_r14_r9_ehp_exactness.py': 'c39759f0b693ce89100ef8439e8aec7fe325694f',
    'phase165_r14_r9_ehp_exactness/test_phase165_r14_r9_ehp_exactness.py': '35ca9fc36b0afb2a37beee85cd8d9e1116e553bc',
    'phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py': 'a819eaebf33870443a8a0df9db2c8da78d1c4a5c',
    'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py': 'd5509da37a914f08b99279aad5bb949d81454c25',
    'phase178_r9_finite_group_surjective_injective_public/tests/test_provider.py': '46b5daa6f7b9ddb96cda1991104c53848a5777e8',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase176_r3r46r1_prior_group_availability/provider.py': 'dda7ac9fb93a60f94631e1a7b0cdf416dbb9cc33',
    'phase174_r3_r7_r5_zero_image_hopf_injective/rule.py': '62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc',
    'phase178_r4_delta_surjective_zero_suspension_isolated/rule.py': '60b91c4ba674ca4680f0c3b353ceb873ecebc7ee',
    'phase178_r9_finite_group_surjective_injective_public/provider.py': '77ca4649b42b137be0de35364a79c8c9da270f7e',
}
TESTS = (
    'phase165_r14_r9_ehp_exactness/test_phase165_r14_r9_ehp_exactness.py',
    'phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py',
    'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py::test_discovery_matches_exact_existing_admission',
    'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py::test_zero_image_provider_uses_existing_r40_without_stable_source_gate',
    'phase178_r9_finite_group_surjective_injective_public/tests/test_provider.py',
)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def preflight():
    require, gt = common.require, common.git_text
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse', 'HEAD') == gt('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not common.git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    common.git('diff', '--check')
    for path, pin in PINS.items():
        require(gt('rev-parse', 'HEAD:' + path) == pin and common.blob_matches(ROOT / path, pin), 'PIN_CHANGED:' + path)
    require(all((ROOT / p.split('::', 1)[0]).is_file() for p in TESTS), 'TEST_MISSING')
    text = (ROOT / 'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig')
    anchor = r'\paragraph*{vii). The Group \(\pi^{n}_{n+7}\).}'
    require(text.count(anchor) == 1, 'SEVEN_STEM_SECTION_CHANGED')
    passage = text.split(anchor, 1)[1].split(r'\switchcolumn', 1)[0]
    terms = (r'0=\pi^{2}_{9}\xto', r'\pi^{3}_{10}\xrightarrow{H}', r'\pi_{10}^5\xrightarrow{\Delta}', r'\pi^{2}_{8}\xrightarrow{E}\pi^{3}_{9}=0', r'\(\Delta\) は同型で')
    require(all(passage.count(t) == 1 for t in terms), 'REVIEWED_EHP_PASSAGE_CHANGED')
    require([passage.index(t) for t in terms] == sorted(passage.index(t) for t in terms), 'EHP_SOURCE_ORDER_CHANGED')
    return {'head': HEAD, 'pins': PINS, 'section_line': text[:text.index(anchor)].count('\n') + 1,
            'source_passage': passage.split(r'さらに', 1)[0].strip()}


def unique_steps(steps):
    """Collect actual accepted steps and their ancestors, not invented witnesses."""
    seen, result = set(), []
    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        result.append(step)
        for parent in step.premises:
            visit(parent)
    for step in steps:
        visit(step)
    return tuple(result)


def describe_option(option, accepted):
    """Probe exact premise matching; no inference is applied or stored."""
    from proof import find_inference_matches_for_rule
    matches = tuple(tuple(p for p in accepted if type(p.conclusion) is type(g) and p.conclusion == g)
                    for g in option.subgoals)
    replay = 'MISSING_PREMISE'
    if all(matches):
        count = 1
        for pool in matches:
            count *= len(pool)
        if count > 64:
            replay = 'COMBINATION_LIMIT_NOT_TESTED'
        else:
            try:
                replay = 'MATCH' if any(find_inference_matches_for_rule(option.rule, p) for p in itertools.product(*matches)) else 'NO_MATCH'
            except Exception as exc:
                replay = 'MATCH_ERROR:' + repr(exc)
    return {'rule': option.rule.name, 'subgoals': [common.statement(g) for g in option.subgoals],
            'accepted_premise_counts': [len(pool) for pool in matches], 'replay': replay}


def observe():
    import phase165_r52_r9_shared_math as shared
    import phase165_r52_r2_search_adapter as adapter
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap, TodaHopfInvariantMap, TodaDeltaMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
    from phase176_r3r46r1_prior_group_availability.provider import build_prior_zero_image_provider
    from phase178_r6_finite_group_cardinality_isolated.rule import cardinality_from_presentation
    from proof import ProofRule

    captured = []
    def capture(real):
        def call(*args, **kwargs):
            result = real(*args, **kwargs)
            if (kwargs.get('n'), kwargs.get('k')) == (3, 7):
                captured.append((dict(kwargs), result))
            return result
        return call

    # Reuse the existing R1 observers. The outer observers capture the exact
    # screened search context and result; they do not change any arguments.
    with patch.object(shared, 'search_registered_partial_proof', capture(shared.search_registered_partial_proof)), \
         patch.object(adapter, 'search_registered_partial_proof', capture(adapter.search_registered_partial_proof)):
        data = copy.deepcopy(r1.observe(3, 7))
    common.require(len(captured) == 1, 'ACTIVE_SEARCH_CONTEXT_MISSING_OR_AMBIGUOUS')
    active, result = captured[0]
    bridge, provider = active['bridge'], active['expansion_provider']
    a, b, c, d, e = (TodaPrimaryGroup(q, n) for q, n in ((9,2),(10,3),(10,5),(8,2),(9,3)))
    root = TodaPrimaryGroupZeroStatement(b)
    common.require(active['goal'] == root, 'ROOT_CHANGED')
    zero_a, zero_e = TodaPrimaryGroupZeroStatement(a), TodaPrimaryGroupZeroStatement(e)
    upper_e, lower_e = TodaSuspensionMap(a, b), TodaSuspensionMap(d, e)
    hopf, delta = TodaHopfInvariantMap(b, c), TodaDeltaMap(c, d)
    inj_h, inj_d, surj_d = MapInjective(hopf), MapInjective(delta), MapSurjective(delta)
    image_upper, image_lower = ImageZeroStatement(upper_e), ImageZeroStatement(lower_e)
    accepted = unique_steps(result.proven_steps)
    snap = (tuple(bridge.proof_links), tuple(bridge.registry._assertions.items()))
    prior_rows = []
    for name, group in (('LEFT_ZERO',a),('H_TARGET',c),('DELTA_TARGET',d),('RIGHT_ZERO',e)):
        step = admitted_prior_group_step(group, proof_target=root, bridge=bridge)
        verified = step is not None and verified_db_step(step, proof_target=root, bridge=bridge)
        order = cardinality_from_presentation(step.conclusion) if verified else None
        prior_rows.append({'name': name, 'group': common.statement(group), 'admitted_verified': bool(verified),
                           'conclusion': common.statement(step.conclusion) if step is not None else None,
                           'cardinality_candidate': common.statement(order) if order is not None else None,
                           'accepted_in_actual_tree': bool(step is not None and any(p == step for p in accepted))})
    direct, = expand_generic_ehp_hopf_goal(inj_h)
    goals = [('ROOT',root),('LEFT_ZERO',zero_a),('UPPER_E_IMAGE_ZERO',image_upper),('H_INJECTIVE',inj_h),
             ('E_H_EXACTNESS',direct.subgoals[1]),('DELTA_INJECTIVE',inj_d),('DELTA_SURJECTIVE',surj_d),
             ('LOWER_E_IMAGE_ZERO',image_lower),('RIGHT_ZERO',zero_e)]
    probes = []
    for name, goal in goals:
        rendered = common.statement(goal)
        actual_visits = [call for call in data['provider_calls'] if call['goal'] == rendered]
        # Post-search queries are diagnostics only, and are NOT included in actual_visits.
        options = provider(goal)
        probes.append({'name': name, 'goal': rendered, 'actual_visits': len(actual_visits),
                       'actual_candidates': actual_visits,
                       'accepted_steps': [{'rule': p.rule.name, 'inference': p.inference_rule.name if p.inference_rule else None}
                                          for p in accepted if type(p.conclusion) is type(goal) and p.conclusion == goal],
                       'post_search_candidates': [describe_option(o, accepted) for o in options]})
    old_provider = build_prior_zero_image_provider(bridge=bridge, proof_target=root)
    isolated = describe_option(direct, accepted)
    h_row = next(p for p in probes if p['name'] == 'H_INJECTIVE')
    image_row = next(p for p in probes if p['name'] == 'UPPER_E_IMAGE_ZERO')
    summary = {'existing_direct_hopf_rule': isolated,
               'existing_direct_hopf_in_public_candidates': any(o['rule'] == direct.rule.name and o['subgoals'] == isolated['subgoals'] for o in h_row['post_search_candidates']),
               'existing_prior_zero_image_provider_candidates': len(old_provider(image_upper)),
               'upper_image_public_candidate_count': len(image_row['post_search_candidates']),
               'upper_image_actual_visit_count': image_row['actual_visits'],
               'upper_image_accepted': bool(image_row['accepted_steps'])}
    common.require(snap == (tuple(bridge.proof_links), tuple(bridge.registry._assertions.items())), 'PROBE_MUTATED_BRIDGE')
    common.require(data['target_given_count'] == 0, 'TARGET_GIVEN_PRESENT')
    data.update(prior_rows=prior_rows, probes=probes, route_summary=summary,
                probe_policy='POST_SEARCH_CANDIDATES_ONLY; NO NEW PROOF STEPS',
                accepted_root_inference=bool(any(p.conclusion == root and p.rule is ProofRule.INFERENCE for p in accepted)))
    return data



def run_focused_tests(folder, report):
    """Run every reviewed test; avoid the historical same-name namespace collision."""
    source = ROOT / TESTS[0]
    # The historical test contains no __file__-relative fixtures. Copy its exact
    # bytes outside the checkout, not its identically named implementation.
    stage = folder / 'isolated_legacy_tests'
    stage.mkdir()
    test_copy = stage / 'test_phase179_r4_legacy_ehp_exactness.py'
    test_copy.write_bytes(source.read_bytes())
    common.require(test_copy.read_bytes() == source.read_bytes()
                   and common.blob_matches(test_copy, PINS[TESTS[0]]),
                   'LEGACY_TEST_COPY_MISMATCH')
    report['legacy_test_original'] = str(source)
    report['legacy_test_copy'] = str(test_copy)
    report['legacy_test_copy_exact'] = True
    emit('LEGACY_TEST_COPY_EXACT', 'VERIFIED')
    # Resolve the production module before pytest collection. Refuse a namespace
    # package or an archived implementation, rather than changing sys.modules.
    bootstrap = (
        'import sys; from pathlib import Path; '
        'import phase165_r14_r9_ehp_exactness as ehp; '
        'assert Path(ehp.__file__).resolve() == '
        '(Path.cwd() / "phase165_r14_r9_ehp_exactness.py").resolve(); '
        'print("PHASE179_R4R1_PRODUCTION_EHP_IMPORT=VERIFIED", flush=True); '
        'import pytest; sys.exit(pytest.main(sys.argv[1:]))'
    )
    cmd = [sys.executable, '-B', '-c', bootstrap, '-q', '-s',
           '--import-mode=importlib', '-p', 'no:cacheprovider',
           '--rootdir', str(ROOT), str(test_copy), *TESTS[1:]]
    report['focused_command'] = cmd
    with (folder / 'focused_pytest.txt').open('w', encoding='utf-8') as log:
        proc = subprocess.run(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=240)
    output = (folder / 'focused_pytest.txt').read_text(encoding='utf-8', errors='replace')
    print(output, flush=True)
    common.require(proc.returncode == 0, 'FOCUSED_PYTEST_FAILED')
    common.require('PHASE179_R4R1_PRODUCTION_EHP_IMPORT=VERIFIED' in output,
                   'PRODUCTION_IMPORT_NOT_VERIFIED')
    report['focused_pytest_exit_code'] = proc.returncode
    emit('R1_TEST_COLLECTION_REPAIR', 'VERIFIED')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', type=Path)
    args = parser.parse_args()
    if args.worker is not None:
        common.store(args.worker, observe())
        return 0
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate':'FAIL_PHASE179_R4','dry_run':args.dry_run,'new_rules':0,'new_given':0,'full_pytest':'NOT_RUN'}
    try:
        report['preflight'] = preflight()
        emit('HEAD', HEAD)
        emit('SOURCE_SECTION_LINE', report['preflight']['section_line'])
        before = common.snapshot()
        if args.dry_run:
            report['gate'] = 'PASS_PHASE179_R4_DRYRUN'
        else:
            output = folder / 'n3_k7.json'
            subprocess.run([sys.executable,'-B','-m',PACKAGE+'.audit','--worker',str(output)],cwd=ROOT,check=True,timeout=240)
            data = json.loads(output.read_text(encoding='utf-8'))
            report['audit'] = data
            for key in ('status','web_key','trust_verified','open_goal_count','target_given_count','proven_step_count','model_citation_count'):
                emit('ROOT_'+key.upper(),data[key])
            for row in data['prior_rows']:
                emit('PRIOR',json.dumps(row,ensure_ascii=False))
            emit('ROUTE_SUMMARY',json.dumps(data['route_summary'],ensure_ascii=False))
            for row in data['probes']:
                emit('PROBE',json.dumps({k:v for k,v in row.items() if k!='actual_candidates'},ensure_ascii=False))
            for row in data['frontier']:
                emit('FRONTIER',json.dumps(row,ensure_ascii=False))
            for line in data['rendered_lines']:
                emit('WEB_LINE',line)
            run_focused_tests(folder, report)
            common.require(common.snapshot() == before,'WORKTREE_CHANGED')
            common.git('diff','--check')
            report['gate'] = 'PASS_PHASE179_R4_ZERO_GROUP_SOURCE_FIRST_AUDIT'
    except Exception as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    common.store(folder/'report.json',report)
    emit('REPORT',folder/'report.json')
    emit('NEW_RULES',0)
    emit('NEW_GIVEN',0)
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
