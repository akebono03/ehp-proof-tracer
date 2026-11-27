"""Read-only final audit of the exact historical R4C guard and its live proof."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = 'a6f49c033caba96c1e5ba460f6e639b53ab21f6f'
R4C = 'phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py'
GUARD = 'test_r4c_real_screened_iso_proof_has_three_prior_sources'
MISSING = 'Missing cited GIVEN ancestry: TodaProp44UniversalStatement'
TEST_NAMES = frozenset((
    'test_r4c_only_exact_pi64_map_is_eligible',
    'test_r4c_exact_premise_types_and_map_dimensions',
    'test_r4c_rejects_given_as_completed_map_property',
    'test_r4c_rejects_mismatched_inference_map',
    'test_r4c_shared_provider_contains_typed_iso_link', GUARD,
))
PRELUDE = 'TodaPreProp44SplittingStatement'
PROP42 = 'TodaProp42GeneralExactnessStatement'
ZERO51 = 'Toda51BelowDiagonalZeroStatement'
EXPECTED_GIVEN_TYPES = frozenset((PRELUDE, PROP42, ZERO51))
FOCUSED = (
    PACKAGE + '/tests/test_audit.py',
    'phase178_r20f1_historical_guard_audit/tests/test_audit.py',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'phase178_r20r1_suspension_isomorphism_bridge_public/tests/test_public.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R30_' + key + '=' + str(value), flush=True)


def preflight():
    from phase178_r1_k6_source_first_audit import audit as r1
    gt = r1.git_text
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse', 'HEAD') == gt('rev-parse', 'origin/develop') == HEAD,
            'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not r1.git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    r1.git('diff', '--check')
    require(all((ROOT / p).is_file() for p in (R4C, *FOCUSED)), 'TEST_FILE_MISSING')
    require(gt('rev-parse', 'HEAD:' + R4C) == '165bd5dee76978dd5d3f0cca40b4890f14b9257b', 'HISTORICAL_GUARD_CHANGED')
    require(r1.blob_matches(ROOT / R4C, '165bd5dee76978dd5d3f0cca40b4890f14b9257b'), 'HISTORICAL_GUARD_BYTES_CHANGED')
    return HEAD


def classify_baseline(exit_code, xml_path):
    """Accept only the exact known assertion failure, or an all-pass observation."""
    cases = list(ET.parse(xml_path).getroot().iter('testcase'))
    require(len(cases) == 6 and {c.get('name') for c in cases} == TEST_NAMES, 'HISTORICAL_TEST_SET_CHANGED')
    require(not any(c.find('error') is not None or c.find('skipped') is not None for c in cases), 'HISTORICAL_ERROR_OR_SKIP')
    failures = [(c.get('name'), c.find('failure')) for c in cases if c.find('failure') is not None]
    if exit_code == 0 and not failures:
        return 'PASS_ALL_6_REQUIRES_ROUTE_REVIEW'
    require(exit_code == 1 and len(failures) == 1, 'UNEXPECTED_BASELINE_FAILURE')
    name, failure = failures[0]
    require(name == GUARD and MISSING in failure.get('message', ''), 'DIFFERENT_BASELINE_FAILURE')
    return 'KNOWN_GUARD_REPRODUCED_OPEN'


def validate_observation(baseline, data):
    """The known red test is never a substitute for mathematical verification."""
    require(baseline == 'KNOWN_GUARD_REPRODUCED_OPEN', 'BASELINE_CHANGED_REQUIRES_REVIEW')
    require(data['trust_replay'] == 'VERIFIED' and data['exact_map_and_branches'] is True,
            'HISTORICAL_PROOF_NOT_VERIFIED')
    require(data['injection_direct_prelude'] is True and data['surjection_exactness_and_zero'] is True,
            'HISTORICAL_BRANCH_CHANGED')
    require(data['lemma54_screened_given_count'] == 0 and data['prelude_position'] == 7250,
            'SOURCE_ORDER_CHANGED')
    require(data['missing_historical_types'] == ['TodaProp44UniversalStatement'], 'MISSING_SOURCE_SET_CHANGED')
    rows = data['given_sources']
    require(len(rows) == 3 and {row['type'] for row in rows} == EXPECTED_GIVEN_TYPES, 'GIVEN_SET_CHANGED')
    position = data['citing_position']
    require(type(position) is int, 'TARGET_POSITION_MISSING')
    for row in rows:
        require(row['premise_count'] == 0 and bool(row['links']), 'GIVEN_NOT_LINKED')
        require(any(link['origin'] == 'FIXED_STATEMENT' and type(link['position']) is int
                    and link['position'] < position for link in row['links']), 'GIVEN_NOT_PRIOR_FIXED')
    require(data['replay_counts'][1] == len(rows) and data['replay_counts'][0] > 0, 'REPLAY_COUNT_CHANGED')
    require(data['target_group_given_count'] == 0, 'TARGET_GROUP_GIVEN')
    return 'OUTDATED_TEST_SOURCE_CONTRACT_CONFIRMED'


def inspect_historical():
    """Use the original test's own screened context; replay the actual inferred map."""
    from phase178_r1_k6_source_first_audit import audit as r1
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap, TodaSuspensionIsomorphismStatement
    from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
    from phase168_r3_41p13_trust_boundary.verification import verify_proof_tree_for_narrative
    from phase177_r18_final_verified_proof_audit.audit import same_group_claim
    from phase174_r3_r6_r2_prop44_lemma54.source import TodaPreProp44SplittingStatement, verify_prelude_source
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
    from proof import ProofRule

    spec = importlib.util.spec_from_file_location('_r30_historical_test', ROOT / R4C)
    require(spec is not None and spec.loader is not None, 'HISTORICAL_TEST_IMPORT_FAILED')
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)
    screened, target, citing, provider = legacy._real_context()
    mapping = legacy._map()
    require(mapping == TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4)), 'WRONG_MAP')
    goal = TodaSuspensionIsomorphismStatement(mapping)
    proof = reconstruct_registered_goal(goal, screened, citing, provider, lookup_mode='typed_reference')
    require(proof.conclusion == goal and proof.rule is ProofRule.INFERENCE, 'HISTORICAL_ISOMORPHISM_NOT_PROVED')
    require(tuple(p.conclusion for p in proof.premises) == (MapInjective(mapping), MapSurjective(mapping))
            and all(p.rule is ProofRule.INFERENCE for p in proof.premises), 'HISTORICAL_MAP_PROPERTIES_CHANGED')
    injection, surjection = proof.premises
    direct_prelude = (len(injection.premises) == 1
                      and injection.premises[0].rule is ProofRule.GIVEN
                      and injection.premises[0].conclusion == TodaPreProp44SplittingStatement()
                      and injection.inference_rule.name == 'cited Hopf-fibration splitting implies suspension injectivity')
    sur_ancestors = legacy._ancestors(surjection)
    sur_given_types = {type(s.conclusion).__name__ for s in sur_ancestors if s.rule is ProofRule.GIVEN}
    zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(6, 7))
    exactness_and_zero = (sur_given_types == {PROP42, ZERO51}
                         and any(s.conclusion == zero and s.rule is ProofRule.INFERENCE for s in sur_ancestors))
    ancestors = legacy._ancestors(proof)
    sources = []
    for step in ancestors:
        if step.rule is not ProofRule.GIVEN:
            continue
        links = []
        for link in screened.proof_links:
            if link.step is None or link.step != step:
                continue
            assertion = screened.registry.assertion(link.assertion_id)
            ref = screened.registry.reference(assertion.reference_id)
            links.append({'assertion_id': link.assertion_id, 'locator': str(ref.locator),
                          'position': ref.publication_position, 'origin': assertion.origin.name})
        sources.append({'type': type(step.conclusion).__name__, 'claim': repr(step.conclusion),
                        'premise_count': len(step.premises), 'links': links})
    result = PartialProofResult(target=mapping.target_group, status=ProofSearchStatus.COMPLETE,
                                proven_steps=(proof,), conclusion=goal)
    # This temporary wrapper certifies only the historical map proof, not a group presentation.
    counts = verify_proof_tree_for_narrative(result, screened, citing_assertion_id=citing)
    citing_ref = screened.registry.reference(screened.registry.assertion(citing).reference_id)
    return {'trust_replay': 'VERIFIED', 'replay_counts': list(counts), 'exact_map_and_branches': True,
            'injection_direct_prelude': direct_prelude, 'surjection_exactness_and_zero': exactness_and_zero,
            'injection_rule': injection.inference_rule.name, 'surjection_rule': surjection.inference_rule.name,
            'prelude_position': verify_prelude_source(), 'citing_assertion_id': citing,
            'citing_position': citing_ref.publication_position, 'group_target': r1.statement(target),
            'lemma54_screened_given_count': sum(link.step is not None and link.step.rule is ProofRule.GIVEN
                and isinstance(link.step.conclusion, TodaLemma54TypedSource) for link in screened.proof_links),
            'target_group_given_count': sum(s.rule is ProofRule.GIVEN and same_group_claim(s.conclusion, mapping.target_group) for s in ancestors),
            'missing_historical_types': [name for name in ('TodaProp44UniversalStatement', PROP42, ZERO51)
                                         if not any(row['type'] == name for row in sources)],
            'given_sources': sources, 'tree': r1.proof_tree((proof,))}


def run_tests(nodes, folder, label):
    xml = folder / (label + '.xml')
    command = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '--import-mode=importlib',
               '-p', 'no:cacheprovider', '--junitxml=' + str(xml), *nodes]
    proc = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          encoding='utf-8', errors='replace', timeout=180)
    (folder / (label + '.txt')).write_text(proc.stdout, encoding='utf-8')
    print(proc.stdout, flush=True)
    return proc.returncode, xml, command


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', type=Path)
    args = parser.parse_args()
    from phase178_r1_k6_source_first_audit import audit as r1
    if args.worker is not None:
        r1.store(args.worker, inspect_historical())
        return 0
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R30', 'dry_run': args.dry_run, 'historical_guard': 'UNMEASURED', 'full_pytest': 'NOT_RUN'}
    try:
        head = preflight()
        before = r1.snapshot()
        report['head'] = head
        emit('HEAD', head)
        if args.dry_run:
            report['gate'] = 'PASS_R30_DRYRUN'
        else:
            code, xml, command = run_tests((R4C,), folder, 'historical_baseline')
            report['historical_command'] = command
            report['historical_pytest_exit_code'] = code
            report['historical_guard'] = classify_baseline(code, xml)
            emit('HISTORICAL_GUARD', report['historical_guard'])
            detail = folder / 'historical_ancestry.json'
            subprocess.run([sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker', str(detail)],
                           cwd=ROOT, check=True, timeout=180)
            data = json.loads(detail.read_text(encoding='utf-8'))
            report['observation'] = data
            for key in ('trust_replay', 'replay_counts', 'injection_rule', 'surjection_rule',
                        'injection_direct_prelude', 'surjection_exactness_and_zero', 'prelude_position',
                        'citing_position', 'lemma54_screened_given_count', 'missing_historical_types',
                        'target_group_given_count'):
                emit(key.upper(), json.dumps(data[key], ensure_ascii=False))
            for row in data['given_sources']:
                emit('GIVEN_SOURCE', json.dumps(row, ensure_ascii=False))
            for row in data['tree']['nodes']:
                emit('PROOF_NODE', json.dumps(row, ensure_ascii=False))
            report['classification'] = validate_observation(report['historical_guard'], data)
            emit('CLASSIFICATION', report['classification'])
            code, xml, command = run_tests(FOCUSED, folder, 'focused')
            report['focused_command'] = command
            report['focused_pytest_exit_code'] = code
            cases = list(ET.parse(xml).getroot().iter('testcase'))
            require(code == 0 and bool(cases) and not any(c.find(tag) is not None for c in cases
                    for tag in ('failure', 'error', 'skipped')), 'FOCUSED_TESTS_FAILED_OR_SKIPPED')
            report['focused_test_count'] = len(cases)
            emit('FOCUSED_TEST_COUNT', len(cases))
            report['gate'] = 'PASS_R30_HISTORICAL_GUARD_OPEN_REPLAY_VERIFIED'
        require(r1.snapshot() == before and preflight() == head, 'REPOSITORY_CHANGED_DURING_AUDIT')
    except Exception as exc:
        report.update(gate='FAIL_R30', error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    r1.store(folder / 'report.json', report)
    emit('REPORT', folder / 'report.json')
    emit('EXISTING_TEST_CHANGED', 'NO')
    emit('NEW_MATH_RULES', 0)
    emit('NEW_GIVEN', 0)
    emit('PROVIDER_CHANGED', 'NO')
    emit('RENDERER_CHANGED', 'NO')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
