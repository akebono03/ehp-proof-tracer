"""Run the reviewed isolated R5 tests and confirm unchanged public frontier."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase178_r1_k6_source_first_audit import audit as common

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = 'e6227e26462656686eee9aa13baa56fd8882773b'
PINS = {
    'phase179_r4_zero_group_source_first_audit/audit.py': 'fb3437d26e638512dcb61d7c27ef65c3ae9af263',
    'phase165_r52_r9_shared_math.py': 'ec76955d1d36e0d8cd9f92a6733d97bcfd4a6d2b',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'map_property_rules.py': '4adeebc9dedb3daf210cd8755be811aca32f1e8b',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'phase175_r4r14r6_surjective_zero_codomain/rule.py': '5acfbe1116b660cc26e576c7dadf36ae7cf02164',
    'phase175_r4r14r6_surjective_zero_codomain/tests/test_rule.py': '4d80e174df7771d8bb8ac7370c8ce72684ba8b4a',
    'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py': 'd5509da37a914f08b99279aad5bb949d81454c25',
}
TESTS = (
    PACKAGE + '/tests/test_rule.py',
    'phase175_r4r14r6_surjective_zero_codomain/tests/test_rule.py',
    'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py::test_discovery_matches_exact_existing_admission',
    'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py::test_discovery_rejects_self_later_invalid_and_untyped_root',
)


def emit(key,value):
    print('PHASE179_R5_' + key + '=' + str(value),flush=True)


def preflight():
    require, gt = common.require, common.git_text
    require(Path(gt('rev-parse','--show-toplevel')).resolve() == ROOT,'WRONG_ROOT')
    require(gt('branch','--show-current') == 'develop','DEVELOP_REQUIRED')
    require(gt('rev-parse','HEAD') == gt('rev-parse','origin/develop') == HEAD,'REVIEWED_HEAD_REQUIRED:'+HEAD)
    require(not common.git('status','--porcelain','--untracked-files=no'),'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path,pin in PINS.items():
        require(gt('rev-parse','HEAD:'+path) == pin and common.blob_matches(ROOT/path,pin),'PIN_CHANGED:'+path)
    require(all((ROOT/p.split('::',1)[0]).is_file() for p in TESTS),'TEST_MISSING')
    common.git('diff','--check')
    for path in (ROOT/PACKAGE).rglob('*.py'):
        compile(path.read_bytes(),str(path),'exec')
    return HEAD


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'gate':'FAIL_PHASE179_R5','dry_run':args.dry_run,'new_given':0,'full_pytest':'NOT_RUN','public_provider_changed':False}
    try:
        head = preflight()
        emit('HEAD',head)
        report['head'] = head
        before = common.snapshot()
        if args.dry_run:
            report['gate'] = 'PASS_PHASE179_R5_DRYRUN'
        else:
            cmd = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command'] = cmd
            with (folder/'focused_pytest.txt').open('w',encoding='utf-8') as log:
                proc = subprocess.run(cmd,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=240)
            print((folder/'focused_pytest.txt').read_text(encoding='utf-8',errors='replace'),flush=True)
            common.require(proc.returncode == 0,'FOCUSED_PYTEST_FAILED')
            from phase179_r4_zero_group_source_first_audit.audit import observe
            data = observe()
            report['public_baseline'] = data
            common.require(data['status'] == 'partial' and data['open_goal_count'] == 2
                           and data['target_given_count'] == 0,'PUBLIC_BASELINE_CHANGED')
            summary = data['route_summary']
            common.require(summary['upper_image_public_candidate_count'] == 0
                           and not summary['upper_image_accepted'],'ISOLATION_BROKEN')
            common.require(next(p for p in data['prior_rows'] if p['name']=='LEFT_ZERO')['admitted_verified'],'PRIOR_ZERO_NOT_VERIFIED')
            emit('PUBLIC_STATUS',data['status'])
            emit('PUBLIC_OPEN_GOALS',data['open_goal_count'])
            emit('PUBLIC_TARGET_GIVEN',data['target_given_count'])
            emit('PUBLIC_UNCONNECTED','VERIFIED')
            common.require(common.snapshot() == before,'WORKTREE_OR_INDEX_CHANGED')
            common.git('diff','--check')
            report['gate'] = 'PASS_PHASE179_R5_ZERO_DOMAIN_IMAGE_ISOLATED'
    except Exception as exc:
        report.update(gate='FAIL_PHASE179_R5',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    common.store(folder/'report.json',report)
    emit('REPORT',folder/'report.json')
    emit('NEW_GIVEN',0)
    emit('PUBLIC_PROVIDER_CHANGED','NO')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
