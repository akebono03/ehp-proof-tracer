"""Separate the R20 isolated checks from a failing historical ancestry guard."""
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
PREFIX = 'PHASE178_R20F1_'
HEAD = '6db941ca18158da23fab34eed6b259842feb2cd1'
R20 = 'phase178_r20_suspension_isomorphism_bridge_isolated'
R4C = 'phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py'
GUARD = 'test_r4c_real_screened_iso_proof_has_three_prior_sources'
MISSING = 'Missing cited GIVEN ancestry: TodaProp44UniversalStatement'
ACTIVE = (R20 + '/tests/test_rule.py',
          'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py',
          'phase178_r19r1_finite_cyclic_suspension_transport_public/tests/test_public.py')
PINS = {
    R4C: '165bd5dee76978dd5d3f0cca40b4890f14b9257b',
    'phase165_r52_r9_shared_math.py': '07aadd1bbe04a5c9e14e6f27f9342e34d5cb85c0',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'phase165_r52_partial_proof.py': '0af6b459ed5a136a8e30a9e349ccf9fa601d448b',
    'phase169_r4b_prop44_injectivity/rule.py': '27c9aa86f180a33a99e2d88ea84939ca8a6dbd4c',
}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def store(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')


def classify_baseline(exit_code, xml_path):
    """Do not waive any failure other than the exact reported ancestry guard."""
    cases = list(ET.parse(xml_path).getroot().iter('testcase'))
    require(len(cases) == 6, 'UNEXPECTED_HISTORICAL_TEST_COUNT')
    require(not any(c.find('error') is not None or c.find('skipped') is not None for c in cases), 'HISTORICAL_ERROR_OR_SKIP')
    failures = [(c.attrib.get('name'), c.find('failure')) for c in cases if c.find('failure') is not None]
    if exit_code == 0 and not failures:
        return 'PASS_ALL_6'
    require(exit_code == 1 and len(failures) == 1, 'UNEXPECTED_BASELINE_FAILURE')
    name, failure = failures[0]
    require(name == GUARD and MISSING in failure.attrib.get('message', ''), 'DIFFERENT_BASELINE_FAILURE')
    return 'KNOWN_GUARD_REPRODUCED_OPEN'


def preflight(r1):
    from phase178_r20_suspension_isomorphism_bridge_isolated import audit as r20
    require(r20.preflight(r1) == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not r1.git('status','--porcelain','--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    for path, pin in PINS.items():
        require(r1.git_text('rev-parse','HEAD:'+path) == pin and r1.blob_matches(ROOT/path,pin), 'PIN_CHANGED:'+path)
    return HEAD


def inspect_historical(folder):
    """Reconstruct the unchanged historical goal and replay its actual ancestry.

    No R20 rule or provider is imported in this worker. The temporary result
    wrapper is only for the existing replay gateway, not a group certificate.
    """
    from phase178_r1_k6_source_first_audit import audit as r1
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from homotopy_groups import TodaSuspensionIsomorphismStatement
    from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
    from phase168_r3_41p13_trust_boundary.verification import verify_proof_tree_for_narrative
    from proof import ProofRule
    spec = importlib.util.spec_from_file_location('_r20f1_historical_test', ROOT/R4C)
    require(spec is not None and spec.loader is not None, 'HISTORICAL_TEST_IMPORT_FAILED')
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)
    screened, target, citing, provider = legacy._real_context()
    mapping = legacy._map()
    goal = TodaSuspensionIsomorphismStatement(mapping)
    proof = reconstruct_registered_goal(goal, screened, citing, provider, lookup_mode='typed_reference')
    require(proof.conclusion == goal and proof.rule is ProofRule.INFERENCE, 'HISTORICAL_ISOMORPHISM_NOT_PROVED')
    require(tuple(p.conclusion for p in proof.premises) == (MapInjective(mapping), MapSurjective(mapping))
            and all(p.rule is ProofRule.INFERENCE for p in proof.premises), 'HISTORICAL_MAP_PROPERTIES_CHANGED')
    tree = r1.proof_tree((proof,))
    sources = []
    for step in legacy._ancestors(proof):
        if step.rule is not ProofRule.GIVEN:
            continue
        links = []
        for link in screened.proof_links:
            if link.step is not None and link.step == step:
                assertion = screened.registry.assertion(link.assertion_id)
                ref = screened.registry.reference(assertion.reference_id)
                links.append({'assertion_id':link.assertion_id,'locator':str(ref.locator),
                              'position':ref.publication_position,'origin':assertion.origin.name})
        sources.append({'type':type(step.conclusion).__name__, 'claim':repr(step.conclusion), 'links':links})
    data = {'tree':tree, 'given_sources':sources, 'citing_assertion_id':citing,
            'injectivity_rule':proof.premises[0].inference_rule.name,
            'surjectivity_rule':proof.premises[1].inference_rule.name,
            'missing_historical_types':[t.__name__ for t in (legacy.TodaProp44UniversalStatement,
                    legacy.TodaProp42GeneralExactnessStatement, legacy.Toda51BelowDiagonalZeroStatement)
                    if not any(s['type']==t.__name__ for s in sources)]}
    store(folder/'historical_ancestry.json',data)
    result = PartialProofResult(target=mapping.target_group, status=ProofSearchStatus.COMPLETE,
                                proven_steps=(proof,), conclusion=goal)
    counts = verify_proof_tree_for_narrative(result, screened, citing_assertion_id=citing)
    require(not any(name == R20 or name.startswith(R20+'.') for name in sys.modules), 'R20_IMPORTED_IN_BASELINE_WORKER')
    data.update(trust_replay='VERIFIED', replay_counts=counts, r20_imported=False)
    store(folder/'historical_ancestry.json',data)
    emit('HISTORICAL_REPLAY','VERIFIED')
    emit('HISTORICAL_INJECTIVITY_RULE',data['injectivity_rule'])
    emit('HISTORICAL_SURJECTIVITY_RULE',data['surjectivity_rule'])
    for source in sources:
        emit('HISTORICAL_GIVEN',json.dumps(source,ensure_ascii=False))
    emit('MISSING_HISTORICAL_TYPES',data['missing_historical_types'])
    return data


def pytest_run(nodes, folder, label):
    xml_path = folder/(label+'.xml')
    command = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib',
               '-p','no:cacheprovider','--junitxml='+str(xml_path),*nodes]
    proc = subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                          encoding='utf-8',errors='replace',env=dict(os.environ,PYTHONUTF8='1',
                          PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1'),timeout=180)
    (folder/(label+'.txt')).write_text(proc.stdout,encoding='utf-8')
    print(proc.stdout,flush=True)
    return proc.returncode,xml_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--inspect-worker',type=Path)
    args = parser.parse_args()
    if args.inspect_worker is not None:
        inspect_historical(args.inspect_worker)
        return 0
    from phase178_r1_k6_source_first_audit import audit as r1
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'gate':'FAIL_R20F1','historical_guard':'UNMEASURED','full_pytest':'NOT_RUN'}
    try:
        before = r1.snapshot()
        emit('HEAD',preflight(r1))
        if args.dry_run:
            report['gate'] = 'PASS_R20F1_READ_ONLY_DRYRUN'
        else:
            code, xml_path = pytest_run((R4C,),folder,'historical_baseline')
            report['historical_pytest_exit_code'] = code
            report['historical_guard'] = classify_baseline(code,xml_path)
            emit('HISTORICAL_GUARD',report['historical_guard'])
            # Run ancestry in a fresh interpreter, without importing R20.
            subprocess.run([sys.executable,'-B','-m',PACKAGE+'.audit','--inspect-worker',str(folder)],
                           cwd=ROOT,check=True,timeout=180)
            report['historical_ancestry'] = json.loads((folder/'historical_ancestry.json').read_text(encoding='utf-8'))
            missing = report['historical_ancestry']['missing_historical_types']
            require((report['historical_guard']=='PASS_ALL_6' and not missing)
                    or (report['historical_guard']=='KNOWN_GUARD_REPRODUCED_OPEN'
                        and 'TodaProp44UniversalStatement' in missing), 'BASELINE_AND_ANCESTRY_DISAGREE')
            code, xml_path = pytest_run(ACTIVE+(PACKAGE+'/tests/test_audit.py',),folder,'active_isolated')
            report['active_pytest_exit_code'] = code
            require(code == 0,'ACTIVE_TESTS_FAILED')
            cases = list(ET.parse(xml_path).getroot().iter('testcase'))
            require(len(cases)==50 and not any(c.find(tag) is not None for c in cases for tag in ('failure','error','skipped')),
                    'ACTIVE_TEST_COUNT_OR_STATUS_CHANGED')
            report['active_test_count'] = len(cases)
            emit('ACTIVE_TESTS','50/50_PASS')
            report['gate'] = ('PASS_R20F1_ISOLATED_WITH_HISTORICAL_GUARD_OPEN'
                              if report['historical_guard']=='KNOWN_GUARD_REPRODUCED_OPEN'
                              else 'PASS_R20F1_ALL_FOCUSED_GUARDS')
        require(r1.snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
    except Exception as exc:
        report.update(gate='FAIL_R20F1',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    store(folder/'report.json',report)
    emit('REPORT',folder/'report.json')
    emit('NEW_MATH_RULES',0)
    emit('NEW_GIVEN',0)
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
