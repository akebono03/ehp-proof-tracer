"""Read-only gate for isolated generalized Hopf splitting injection."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase178_r1_k6_source_first_audit import audit as prior

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = 'b3effb14bd9645760262fa7f853125ddba4d746c'
PINS = {
    'sources/toda/Toda_04_2.tex': '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7',
    'phase174_r3_r6_r2_prop44_lemma54/source.py': '0f4a020a9f571bbfa17e7d5210e7e7cc192875c2',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py': '7a7bcdfc5cf61b2105b5b4f0d44e1679e6e3ffe9',
    'phase165_r52_r9_shared_math.py': '79c3fc2d14080c188ef9284119a6eccb832daac9',
    'phase176_r3r48_cited_finite_delta_kernel/rule.py': '86cc4a468ffd4601337bbef589a37fa46b449263',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py': 'fb6f340cfec0e9a7f31fa816cb13ca763c5cb277',
    'tests/test_phase57_lemma45_two_iota3.py': '9cf57c9a443085b91624cc2b1fb011127003aea9',
}
TESTS = (PACKAGE + '/tests/test_rule.py',
         'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
         'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py',
         'tests/test_phase57_lemma45_two_iota3.py')


def emit(key,value):
    print('PHASE179_R2_'+key+'='+str(value),flush=True)


def preflight():
    require, gt = prior.require, prior.git_text
    require(Path(gt('rev-parse','--show-toplevel')).resolve()==ROOT,'WRONG_ROOT')
    require(gt('branch','--show-current')=='develop','DEVELOP_REQUIRED')
    require(gt('rev-parse','HEAD')==gt('rev-parse','origin/develop')==HEAD,'REVIEWED_HEAD_REQUIRED:'+HEAD)
    require(not prior.git('status','--porcelain','--untracked-files=no'),'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path,pin in PINS.items():
        require(gt('rev-parse','HEAD:'+path)==pin and prior.blob_matches(ROOT/path,pin),'PIN_CHANGED:'+path)
    require(all((ROOT/p).is_file() for p in TESTS),'TEST_MISSING')
    prior.git('diff','--check')
    from phase174_r3_r6_r2_prop44_lemma54.source import verify_prelude_source
    require(verify_prelude_source()==7250,'SOURCE_POSITION_CHANGED')
    text=(ROOT/'sources/toda/Toda_04_2.tex').read_text(encoding='utf-8-sig')
    start=r'\begin{lemma}\label{lem:4.5}'
    require(text.count(start)==1,'LEMMA45_ANCHOR_CHANGED')
    lemma=text.split(start,1)[1].split(r'\end{lemma}',1)[0]
    require(all(a in lemma for a in ('$n=2,4,8$',r'E:\pis{i-1}{S^{n-1}}\to\pis{i}{S^n}', '任意の $i$ で単射')),'LEMMA45_CONTENT_CHANGED')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    base=Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder=Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report={'gate':'FAIL_PHASE179_R2','dry_run':args.dry_run,'full_pytest':'NOT_RUN','new_given':0,'public_provider_changed':False}
    try:
        preflight()
        before=prior.snapshot()
        emit('HEAD',HEAD)
        emit('SOURCE_POSITION',7250)
        if args.dry_run:
            report['gate']='PASS_PHASE179_R2_DRYRUN'
        else:
            cmd=[sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command']=cmd
            with (folder/'focused_pytest.txt').open('w',encoding='utf-8') as log:
                proc=subprocess.run(cmd,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
            print((folder/'focused_pytest.txt').read_text(encoding='utf-8',errors='replace'),flush=True)
            report['focused_exit_code']=proc.returncode
            prior.require(proc.returncode==0,'FOCUSED_PYTEST_FAILED')
            report['gate']='PASS_PHASE179_R2_ISOLATED_SPLIT_INJECTION'
        prior.require(prior.snapshot()==before,'REPOSITORY_CHANGED')
        preflight()
    except Exception as exc:
        report.update(gate='FAIL_PHASE179_R2',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    emit('REPORT',folder/'report.json')
    emit('FULL_PYTEST','NOT_RUN')
    emit('NEW_GIVEN',0)
    emit('PUBLIC_PROVIDER_CHANGED','NO')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__=='__main__':
    raise SystemExit(main())
