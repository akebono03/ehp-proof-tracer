"""Read-only R16 registration and existing-source audit after R15R2."""
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
BASE = '198e6b56e5d54cfa3eb4d1a44fc5890f64eec053'
TARGET = 'phase165_r52_r9_shared_math.py'
TESTS = (PACKAGE+'/tests/test_source_contract.py', PACKAGE+'/tests/test_registration.py',
         'phase178_r15r2_toda512_public/tests/test_public.py',
         'phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py',
         'phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py',
         'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py')


def require(ok,message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def emit(key,value):
    print('PHASE178_R16_'+key+'='+str(value),flush=True)


def snapshot():
    return (git('rev-parse','HEAD'),git('diff','--binary','HEAD'),git('diff','--cached','--binary'),
            git('status','--porcelain','--untracked-files=all'))


def preflight():
    require(Path(gt('rev-parse','--show-toplevel')).resolve()==ROOT,'WRONG_ROOT')
    head=gt('rev-parse','HEAD')
    require(gt('branch','--show-current')=='develop' and head==gt('rev-parse','origin/develop'),'HEAD_OR_BRANCH_MISMATCH')
    require(gt('merge-base',BASE,head)==BASE,'REVIEWED_ANCESTRY_REQUIRED')
    require(not gt('diff','--cached','--name-only'),'STAGED_CHANGES_REFUSED')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    from hashlib import sha256
    def digest(data):
        return sha256(data.decode('utf-8-sig').replace('\r\n','\n').encode()).hexdigest()
    pins=json.loads((Path(__file__).parent/'reviewed_r15r2_hashes.json').read_text(encoding='utf-8'))
    changes=set(gt('diff','--name-only',BASE,head).splitlines())
    require(changes <= {TARGET,*pins},'UNREVIEWED_COMMITTED_CHANGES:'+repr(sorted(changes-{TARGET,*pins})))
    for path,expected in pins.items():
        require((ROOT/path).is_file() and digest((ROOT/path).read_bytes())==expected,'R15R2_PACKAGE_CHANGED:'+path)
        if path in changes:
            require(digest(git('show',head+':'+path))==expected,'R15R2_COMMITTED_CONTENT_CHANGED:'+path)
    from phase178_r15r2_toda512_public.installer import proposed_source,normalize
    require(gt('rev-parse',BASE+':'+TARGET)=='4556e76736a3d5624632900ee9c4ab45599ffb0f','BASE_SHARED_MATH_CHANGED')
    expected=proposed_source(normalize(git('show',BASE+':'+TARGET)))
    require(normalize((ROOT/TARGET).read_bytes())==expected,'R15R2_PUBLIC_CONNECTION_NOT_INSTALLED_EXACTLY')
    if TARGET in changes:
        require(normalize(git('show',head+':'+TARGET))==expected,'UNREVIEWED_SHARED_MATH_COMMIT')
    dirty=set(gt('diff','--name-only','HEAD').splitlines())
    require(dirty <= {TARGET},'UNRELATED_TRACKED_CHANGES:'+repr(sorted(dirty-{TARGET})))
    # R15 was committed at BASE: its contents must still match the reviewed commit.
    for path in gt('ls-tree','-r','--name-only',BASE,'phase178_r15_toda512_isolated').splitlines():
        require(digest((ROOT/path).read_bytes())==digest(git('show',BASE+':'+path)),'R15_SOURCE_CHANGED:'+path)
    require(all((ROOT/p).is_file() for p in TESTS),'FOCUSED_TEST_MISSING')
    gt('diff','--check')
    return head


def classify_existing_513(bridge, claims):
    """Separate reviewed metadata-only components from actual source conflicts."""
    from toda_literature_statement_boundary import (
        TodaFixedStatementComponent, TodaLiteratureStatementRole,
    )
    from unified_statement_registry import AssertionOrigin

    expected_keys = {
        'delta_nu9_relation', 'delta_eta11_squared_zero', 'delta_eta13_zero',
    }
    linked_ids = {link.assertion_id for link in bridge.proof_links}
    metadata, conflicts = [], []
    for a in bridge.registry._assertions.values():
        if a.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        ref = bridge.registry.reference(a.reference_id)
        locator = str(ref.locator).replace(' ', '')
        if locator != '(5.13)' and not any(a.content == c for c in claims):
            continue
        row = {'id': a.assertion_id, 'locator': str(ref.locator),
               'content': repr(a.content)}
        component = a.content
        if (locator == '(5.13)'
                and type(component) is TodaFixedStatementComponent
                and component.reference_locator == '(5.13)'
                and component.component_key in expected_keys
                and component.statement_role is TodaLiteratureStatementRole.MAP_VALUE
                and component.order is None and component.range_text is None
                and component.range_is_explicit_in_current_aggregate is True
                and a.assertion_id not in linked_ids):
            row['component_key'] = component.component_key
            metadata.append(row)
        else:
            conflicts.append(row)
    return metadata, conflicts


def audit_existing():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase178_r15_toda512_isolated.source import CitedToda512
    from proof import ProofRule
    from .source import canonical_513

    bridge = build_shared_typed_bridge()
    metadata, existing = classify_existing_513(bridge, canonical_513())
    count512 = sum(link.step is not None and link.step.rule is ProofRule.GIVEN
                   and type(link.step.conclusion) is CitedToda512
                   for link in bridge.proof_links)
    emit('PUBLIC_512_GIVEN_COUNT', count512)
    emit('EXISTING_513_BOUNDARY_METADATA', json.dumps(metadata, ensure_ascii=False))
    emit('EXISTING_513_BOUNDARY_METADATA_COUNT', len(metadata))
    emit('EXISTING_TYPED_513', json.dumps(existing, ensure_ascii=False))
    require(count512 == 3, 'PUBLIC_512_REGRESSION')
    require(not existing, 'EXISTING_513_REQUIRES_REUSE_REVIEW')
    require(len(metadata) == 3 and {row['component_key'] for row in metadata} == {
        'delta_nu9_relation', 'delta_eta11_squared_zero', 'delta_eta13_zero',
    }, 'REVIEWED_513_BOUNDARY_METADATA_CHANGED')
    return {'boundary_metadata': metadata, 'typed_conflicts': existing}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dry-run',action='store_true')
    args=p.parse_args()
    base=Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder=Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report={'gate':'FAIL_R16','dry_run':args.dry_run,'full_pytest':'NOT_RUN','production_changes':0}
    try:
        before=snapshot()
        head=preflight()
        emit('HEAD',head)
        emit('R15R2_PUBLIC_CONNECTION','VERIFIED')
        report['existing']=audit_existing()
        from .source import build_cited_513_source
        source=build_cited_513_source()
        require(len(source.proof_links)==3,'WRONG_SOURCE_COUNT')
        report['isolated_claims']=[repr(l.step.conclusion) for l in source.proof_links]
        emit('SOURCE_POSITION',10000)
        emit('ISOLATED_GIVEN_COUNT',3)
        if args.dry_run:
            report['gate']='PASS_R16_READ_ONLY_DRYRUN'
        else:
            command=[sys.executable,'-B','-m','pytest','-q','-s','-p','no:cacheprovider','--import-mode=importlib',*TESTS]
            report['focused_command']=command
            subprocess.run(command,cwd=ROOT,check=True)
            emit('SOURCE_ORDER_SCREEN','VERIFIED')
            report['gate']='PASS_R16_TODA513_ISOLATED'
        require(snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
    except Exception as exc:
        report.update(gate='FAIL_R16',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    path=folder/'report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    emit('REPORT',path)
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__=='__main__':
    raise SystemExit(main())
