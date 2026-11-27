"""Read-only, reviewed-base audit of the isolated suspension isomorphism bridge."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
BASE = '7390660dc6eda0364d93a29cc255d670c51c4871'
PREFIX = 'PHASE178_R20_'
PREVIOUS = 'phase178_r19r1_finite_cyclic_suspension_transport_public/'
TARGET = 'phase165_r52_r9_shared_math.py'
OLD_TEST = 'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py'
R4C = 'phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py'
PINS = {
    TARGET: '5b23a40f62069c00ae30bee6ed670d66f8a3daf9',
    OLD_TEST: 'f79a3e80bb513b8c55e0bfe7760576a191f42698',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/provider.py': 'c20a6c2d8466cd30adee8bb92ed61283c6c6fe9d',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase169_r4c_pi64_suspension_iso/rule.py': 'c5cc2190d243997fccb11751f5d530bf8fc12085',
    'phase165_r12_r24_web_search_connection.py': '71d0c6c365a46e833a2bfe304c771d2e010178ca',
    'phase165_r14_r14_diagonal_and_prop42.py': 'a831b975fd355baa41251da30ad78d8eaa3029b1',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    R4C: '165bd5dee76978dd5d3f0cca40b4890f14b9257b',
}
TESTS = (PACKAGE + '/tests/test_rule.py', R4C, OLD_TEST, PREVIOUS + 'tests/test_public.py')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def digest(raw):
    return hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()


def preflight(r1):
    gt = r1.git_text
    require(Path(os.fsdecode(r1.git('rev-parse','--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch','--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = gt('rev-parse','HEAD')
    require(head == gt('rev-parse','origin/develop'), 'LOCAL_REMOTE_HEAD_MISMATCH')
    require(gt('merge-base',BASE,head) == BASE, 'REVIEWED_BASE_REQUIRED')
    require(not gt('diff','--cached','--name-only'), 'STAGED_CHANGES_PRESENT')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    manifest = json.loads((Path(__file__).parent/'reviewed_r19r1.json').read_text(encoding='utf-8'))
    allowed = {TARGET, OLD_TEST} | set(manifest)
    committed = set(gt('diff','--name-only',BASE,head).splitlines())
    dirty = set(gt('diff','--name-only','HEAD').splitlines())
    require(not (committed | dirty) - allowed, 'UNRELATED_TRACKED_CHANGES')
    for path, expected in manifest.items():
        require((ROOT/path).is_file() and digest((ROOT/path).read_bytes()) == expected,
                'R19R1_PACKAGE_CHANGED:' + path)
        if path in committed:
            require(digest(r1.git('show',head+':'+path)) == expected,'R19R1_COMMITTED_PACKAGE_CHANGED:'+path)
    # Import the previous installer only after verifying its bytes.
    from phase178_r19r1_finite_cyclic_suspension_transport_public import installer as previous
    require(previous.HEAD == BASE, 'R19R1_BASE_CHANGED')
    pins = dict(previous.PINS)
    pins.update(PINS)
    writers = {TARGET:previous.proposed_source, OLD_TEST:previous.proposed_test}
    for path,pin in pins.items():
        require(gt('rev-parse',BASE+':'+path) == pin,'BASE_PIN_CHANGED:'+path)
        if path in writers:
            base = previous.normalized(r1.git('show',BASE+':'+path))
            expected = writers[path](base)
            require(previous.normalized((ROOT/path).read_bytes()) == expected,'R19R1_NOT_INSTALLED_OR_CHANGED:'+path)
            if path in committed:
                require(previous.normalized(r1.git('show',head+':'+path)) == expected,'R19R1_COMMITTED_CONTENT_CHANGED:'+path)
        else:
            require(gt('rev-parse',head+':'+path) == pin and r1.blob_matches(ROOT/path,pin),'DEPENDENCY_CHANGED:'+path)
    for path in TESTS:
        require((ROOT/path).is_file(),'FOCUSED_TEST_MISSING:'+path)
    r1.git('diff','--check')
    return head


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    try:
        from phase178_r1_k6_source_first_audit import audit as r1
        before = r1.snapshot()
        emit('HEAD',preflight(r1))
        emit('R19R1_INSTALLED_CONTENT','VERIFIED')
        if not args.dry_run:
            subprocess.run([sys.executable,'-B','-m','pytest','-q','-s',
                            '--import-mode=importlib','-p','no:cacheprovider',*TESTS],cwd=ROOT,check=True)
        require(r1.snapshot() == before,'REPOSITORY_CHANGED_DURING_AUDIT')
    except Exception as exc:
        emit('ERROR',repr(exc))
        emit('GATE','FAIL_R20')
        return 1
    emit('NEW_TYPED_BRIDGE_RULES',1)
    emit('NEW_ISOMORPHISM_THEOREMS',0)
    emit('NEW_GIVEN',0)
    emit('PUBLIC_WIRING','NOT_CHANGED')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE','PASS_R20_DRYRUN' if args.dry_run else 'PASS_R20_ISOLATED_SUSPENSION_ISOMORPHISM_BRIDGE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
