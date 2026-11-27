"""Align the single cited eta generator with the reviewed simple typed notation."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
BASE = '1d8c87dfc3aa3aac79aa86b5e2ae142541b02da0'
TARGET = 'phase178_r16_toda513_isolated/source.py'
PINS = {
    TARGET: '73300491e27c4d4298e07d8b0bd9c6653328b609',
    'phase166_r3af_goal_adapter.py': 'd85f595c9c8be18a2db760b8a20868b40eb15300',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase178_r21_finite_cyclic_generator_zero_image_isolated/rule.py': '3ff46d65aee3c7ae2fdc3b3ba3f8c68d282d0b8d',
    'phase178_r21_finite_cyclic_generator_zero_image_isolated/tests/test_rule.py': '6e9a0f7548460a2a4fd6d24c2a6415f10fa18bfc',
    'phase178_r16_toda513_isolated/tests/test_registration.py': 'b16cbb51c8f7463237b7e31458cb8205041a993e',
    'phase178_r16_toda513_isolated/source_contract.py': '8e6aa8beac6bc3c5f490f64b262aaa83d33a829b',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase165_r52_r9_shared_math.py': '79c3fc2d14080c188ef9284119a6eccb832daac9',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py': '910766ecc613bda7470fcbf804783aea88678d93',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py': 'fb6f340cfec0e9a7f31fa816cb13ca763c5cb277',
    'phase178_r23_common_renderer_elision/tests/test_display.py': '31deb821841f3224774112aea1e38879d3bf85f5',
    'phase178_r17r3_common_renderer/tests/test_display.py': '934fcdec3976b45e7e9570a780a47adca6837cca',
    'phase168_r3_5_model_renderer.py': 'f622c3d134c2613a286dc126ba970641f9856a68',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
}
R24_PINS = {'phase178_r24_n7_source_first_audit/audit.py': 'fd0651ac143b333f24d75eae252d870f3f6cad6db3cfe1c40d8a23d3c509ae4f', 'phase178_r24_n7_source_first_audit/run.ps1': 'bef9e67bbb1c6a6677534d69cd7e6ad8f4744adf6920cbe9069f7597de63d0e8', 'phase178_r24_n7_source_first_audit/__init__.py': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'phase178_r24_n7_source_first_audit/tests/test_audit.py': '948b69427ec4aa8a2d57077be3c372f314eb60db091e21c95f14eefaf33437ed'}
OLD = "    eta13 = _element('η', 13, 1)\n"
NEW = "    # Single generators use the existing simple DB adapter's indexed notation.\n    # The structured composite generators above retain their Unicode names.\n    eta13 = HomotopyElement('η_13', 13, 14, 13, GeneratorSymbol('η', index=13))\n"

SELF_FILES = {PACKAGE + '/' + path for path in (
    '__init__.py', 'installer.py', 'run.ps1', 'tests/test_installer.py', 'tests/test_alignment.py',
)}
TESTS = (
    PACKAGE + '/tests/test_installer.py', PACKAGE + '/tests/test_alignment.py',
    'phase178_r16_toda513_isolated/tests/test_registration.py',
    'phase178_r21_finite_cyclic_generator_zero_image_isolated/tests/test_rule.py',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py',
    'phase178_r17r3_common_renderer/tests/test_display.py',
    'phase178_r23_common_renderer_elision/tests/test_display.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R25_' + key + '=' + str(value), flush=True)


def normalized(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def encode_like(text, raw):
    if b'\r\n' in raw:
        text = text.replace('\n', '\r\n')
    return text.encode('utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8')


def proposed_source(text):
    require(text.count(OLD) == 1 and NEW not in text, 'MISSING_OR_AMBIGUOUS_ETA13_ANCHOR')
    updated = text.replace(OLD, NEW, 1)
    ast.parse(updated)
    return updated


def validate_scope(committed, dirty):
    allowed = {TARGET} | SELF_FILES | set(R24_PINS)
    require(set(committed) <= allowed, 'UNREVIEWED_COMMITTED_PATHS:' + repr(sorted(set(committed)-allowed)))
    require(set(dirty) <= {TARGET}, 'UNREVIEWED_WORKTREE_PATHS:' + repr(sorted(set(dirty)-{TARGET})))


def check_git_diff():
    check = subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    require(check.returncode == 0, 'GIT_DIFF_CHECK:' + check.stdout + check.stderr)


def preflight(r1):
    gt = r1.git_text
    require(Path(gt('rev-parse','--show-toplevel')).resolve() == ROOT,'WRONG_ROOT')
    require(gt('branch','--show-current') == 'develop','DEVELOP_REQUIRED')
    head = gt('rev-parse','HEAD')
    require(head == gt('rev-parse','origin/develop'),'HEAD_MISMATCH')
    require(gt('merge-base',BASE,head) == BASE,'REVIEWED_BASE_REQUIRED')
    require(not gt('diff','--cached','--name-only'),'STAGED_CHANGES_PRESENT')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    validate_scope(gt('diff','--name-only',BASE,head).splitlines(), gt('diff','--name-only','HEAD').splitlines())
    for path,pin in PINS.items():
        require(gt('rev-parse',BASE+':'+path) == pin,'BASE_PIN_CHANGED:'+path)
        if path != TARGET:
            require(gt('rev-parse',head+':'+path) == pin and r1.blob_matches(ROOT/path,pin),'DEPENDENCY_CHANGED:'+path)
    for path,pin in R24_PINS.items():
        require((ROOT/path).is_file() and hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==pin,'R24_FILE_CHANGED:'+path)
    original = normalized(r1.git('show',BASE+':'+TARGET))
    proposed = proposed_source(original)
    raw = (ROOT/TARGET).read_bytes()
    require(normalized(raw) in (original,proposed),'SOURCE_WORKTREE_CHANGED')
    require(normalized(r1.git('show',head+':'+TARGET)) in (original,proposed),'SOURCE_COMMIT_CHANGED')
    for path in TESTS:
        require((ROOT/path).is_file(),'FOCUSED_TEST_MISSING:'+path)
    check_git_diff()
    return head, raw, encode_like(proposed,raw), proposed


def check_complete(summary, n):
    require((summary['n'],summary['k']) == (n,6),'WRONG_TARGET')
    require(summary['status']=='complete' and summary['trust_status']=='VERIFIED'
            and summary['open_goal_count']==0 and summary['target_given_count']==0
            and summary['complete_invariants_hold'] and summary['web_error'] is None
            and summary['web_key']=='generic-complete-proof','REGRESSION_OR_UNVERIFIED:'+repr(summary))


def audit_public(r1, folder, report):
    for n in (5,6):
        summary = r1.worker(n,6,folder,180)
        check_complete(summary,n)
        report['regression_'+str(n)] = summary
        emit('REGRESSION_N'+str(n),'VERIFIED')
    # Run only the read-only worker of R24. Its historical preflight pins the
    # uncorrected source; R25 preflight replaces that check for this run.
    subprocess.run([sys.executable,'-B','-m','phase178_r24_n7_source_first_audit.audit',
                    '--worker','--folder',str(folder)],cwd=ROOT,check=True,timeout=180)
    obs = json.loads((folder/'observation.json').read_text(encoding='utf-8'))
    report['n7_observation'] = obs
    summary, probes = obs['summary'],obs['probes']
    sources = probes['sources_and_prior_eligibility']
    require(sources['513_generator_matches_db'] and sources['513_screened_link_count']==1
            and sources['512_screened_link_count']==1 and all(v['eligible'] for v in sources['prior_checks'].values()),
            'SOURCE_ALIGNMENT_NOT_VERIFIED')
    require(probes['expected_candidates']['DELTA_ZERO'],'R21_CANDIDATE_STILL_MISSING')
    emit('GENERATOR_ALIGNMENT','VERIFIED')
    emit('EXPECTED_CANDIDATES',json.dumps(probes['expected_candidates'],ensure_ascii=False))
    emit('R21_PUBLIC_CANDIDATE','VERIFIED')
    for key in ('status','proven_step_count','open_goal_count','trust_status','target_given_count','web_key'):
        emit('PUBLIC_'+key.upper(),summary[key])
    for row in probes['goals']:
        emit('PROBE',json.dumps({k:row[k] for k in ('name','actual_provider_visits','root_ancestor_ids','candidate_count')},ensure_ascii=False))
    for row in obs['analysis']['frontier']:
        emit('FRONTIER',json.dumps(row,ensure_ascii=False))
    detail = json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
    for line in detail['web']['rendered_lines']:
        print(line)
    if obs['analysis']['root_complete']:
        check_complete(summary,7)
        emit('ROOT_ANCESTOR_COUNT',probes['root_ancestor_count'])
        emit('ROOT_GIVEN_COUNT',len(probes['root_given_nodes']))
        return 'PASS_R25_N7_VERIFIED_COMPLETE'
    return 'PASS_R25_NOTATION_ALIGNED_PROOF_OPEN'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    from phase178_r1_k6_source_first_audit import audit as r1
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'gate':'FAIL_R25','dry_run':args.dry_run}
    written = False
    try:
        head,raw,updated,source = preflight(r1)
        emit('HEAD',head)
        (folder/'source.full.py.txt').write_text(source,encoding='utf-8')
        emit('FULL_CODE',folder/'source.full.py.txt')
        if args.dry_run:
            report['gate'] = 'PASS_R25_DRYRUN'
        else:
            require((ROOT/TARGET).read_bytes()==raw,'WORKTREE_CHANGED')
            if raw != updated:
                (ROOT/TARGET).write_bytes(updated)
                written = True
            check_git_diff()
            before = r1.snapshot()
            command = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command'] = command
            subprocess.run(command,cwd=ROOT,check=True)
            report['gate'] = audit_public(r1,folder,report)
            require(r1.snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
            _,post,wanted,_ = preflight(r1)
            require(post==wanted,'POST_INSTALL_INTEGRITY_FAILED')
    except Exception as exc:
        if written and (ROOT/TARGET).read_bytes()==updated:
            (ROOT/TARGET).write_bytes(raw)
        report.update(gate='FAIL_R25',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    emit('REPORT',folder/'report.json')
    emit('NEW_MATH_RULES',0)
    emit('NEW_GIVEN',0)
    emit('EXISTING_GIVEN_NOTATION_CHANGED',1)
    emit('PROVIDER_CHANGED','NO')
    emit('RENDERER_CHANGED','NO')
    emit('HISTORICAL_GUARD','NOT_RUN_KNOWN_OPEN')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__=='__main__':
    raise SystemExit(main())
