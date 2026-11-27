"""Read-only R15 preflight and isolated source registration audit."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).parent.name
HEAD = '4f445faccd12a6f148834173d5054fcb58ad1eed'
TESTS = (PACKAGE+'/tests/test_source_contract.py', PACKAGE+'/tests/test_registration.py',
         'phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py',
         'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8').strip()


def snapshot():
    return (git('rev-parse','HEAD'), git('diff','--binary','HEAD'),
            git('diff','--cached','--binary'), git('status','--porcelain','--untracked-files=all'))


def emit(key,value):
    print('PHASE178_R15_'+key+'='+str(value), flush=True)


def preflight():
    require(Path(git('rev-parse','--show-toplevel')).resolve()==ROOT,'WRONG_ROOT')
    require(git('branch','--show-current')=='develop','DEVELOP_REQUIRED')
    require(git('rev-parse','HEAD')==git('rev-parse','origin/develop')==HEAD,'REVIEWED_HEAD_REQUIRED')
    require(not git('status','--porcelain','--untracked-files=no'),'TRACKED_CHANGES_REFUSED')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    require(all((ROOT/p).is_file() for p in TESTS),'FOCUSED_TEST_MISSING')
    git('diff','--check')
    from .source import build_cited_512_source
    source = build_cited_512_source()
    require(len(source.proof_links)==3,'WRONG_CITED_LINK_COUNT')
    return source


def audit_existing(source):
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from proof import ProofRule
    from .source import canonical_512
    bridge = build_shared_typed_bridge()
    claims = tuple(canonical_512(n) for n in (4,5,6))
    existing = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        a = bridge.registry.assertion(link.assertion_id)
        ref = bridge.registry.reference(a.reference_id)
        if str(ref.locator).replace(' ','')=='(5.12)' or any(link.step.conclusion in (c,c.statement) for c in claims):
            existing.append({'id':link.assertion_id,'locator':str(ref.locator),'content':repr(a.content)})
    emit('EXISTING_TYPED_512_GIVEN',json.dumps(existing,ensure_ascii=False))
    require(not existing,'EXISTING_TYPED_512_REQUIRES_REUSE_REVIEW')
    return existing


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dry-run',action='store_true')
    args=p.parse_args()
    base=Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder=Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report={'gate':'FAIL_R15','dry_run':args.dry_run,'full_pytest':'NOT_RUN','public_changes':0}
    try:
        before=snapshot()
        source=preflight()
        emit('HEAD',HEAD)
        emit('SOURCE_POSITION',9700)
        report['existing']=audit_existing(source)
        report['isolated_claims']=[repr(l.step.conclusion) for l in source.proof_links]
        emit('ISOLATED_GIVEN_COUNT',len(source.proof_links))
        if args.dry_run:
            report['gate']='PASS_R15_READ_ONLY_DRYRUN'
        else:
            command=[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',*TESTS]
            report['focused_command']=command
            subprocess.run(command,cwd=ROOT,check=True)
            report['gate']='PASS_R15_TODA512_ISOLATED'
        require(snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
    except Exception as exc:
        report.update(gate='FAIL_R15',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    path=folder/'report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    emit('REPORT',path)
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__=='__main__':
    raise SystemExit(main())
