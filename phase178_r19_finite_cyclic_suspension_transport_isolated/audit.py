"""Run only isolated transport and historical transport regression tests."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '4d982fcdb8f5d2e2e749c1bae8656a7bb2029c0c'
PREFIX = 'PHASE178_R19_'
LEGACY = 'phase169_r3b_finite_cyclic_suspension/tests/test_phase169_r3b_finite_cyclic_suspension.py'
PINS = {
    'phase165_r12_r24_web_search_connection.py': '71d0c6c365a46e833a2bfe304c771d2e010178ca',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase176_r3r48_cited_finite_delta_kernel/rule.py': '86cc4a468ffd4601337bbef589a37fa46b449263',
    'phase165_r52_r9_shared_math.py': '5b23a40f62069c00ae30bee6ed670d66f8a3daf9',
    'phase178_r18_n6_source_first_audit/audit.py': 'd9577c8d77c73e21e112a37f56942ecc7adbfdfe',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    LEGACY: 'f1f6c5169107677c94c183aeb4ef49794dc4a174',
}
TESTS = (
    PACKAGE + '/tests/test_provider.py',
    LEGACY + '::test_expansion_contains_three_unproved_typed_premises',
    LEGACY + '::test_inference_derives_only_from_all_three_verified_premises',
    LEGACY + '::test_wrong_isomorphism_or_generator_image_rejected',
    LEGACY + '::test_missing_or_ambiguous_registered_source_retains_previous_route',
    LEGACY + '::test_other_stems_are_unchanged',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def preflight(r1):
    require(Path(os.fsdecode(r1.git('rev-parse','--show-toplevel').strip())).resolve() == ROOT,'WRONG_ROOT')
    require(r1.git_text('branch','--show-current') == 'develop','DEVELOP_REQUIRED')
    head = r1.git_text('rev-parse','HEAD')
    require(head == r1.git_text('rev-parse','origin/develop') == HEAD,'REVIEWED_HEAD_REQUIRED:'+HEAD)
    require(not r1.git('status','--porcelain','--untracked-files=no'),'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path,pin in PINS.items():
        require(r1.git_text('rev-parse','HEAD:'+path) == pin and r1.blob_matches(ROOT/path,pin),'PIN_CHANGED:'+path)
    for node in TESTS:
        require((ROOT/node.split('::',1)[0]).is_file(),'FOCUSED_TEST_MISSING:'+node)
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
        if not args.dry_run:
            subprocess.run([sys.executable,'-B','-m','pytest','-q','-s',
                            '--import-mode=importlib','-p','no:cacheprovider',*TESTS],cwd=ROOT,check=True)
        require(r1.snapshot() == before,'REPOSITORY_CHANGED_DURING_AUDIT')
    except Exception as exc:
        emit('ERROR',repr(exc))
        emit('GATE','FAIL_R19')
        return 1
    emit('NEW_MATH_RULES',0)
    emit('NEW_GIVEN',0)
    emit('PUBLIC_WIRING','NOT_CHANGED')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE','PASS_R19_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R19_ISOLATED_FINITE_CYCLIC_TRANSPORT')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
