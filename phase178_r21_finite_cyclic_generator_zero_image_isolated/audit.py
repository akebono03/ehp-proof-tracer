"""Reviewed-HEAD preflight and focused isolated regression tests."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '980e3b2c759ca08b23321064a4b60bf0fe4b3ba7'
TESTS = (
    PACKAGE + '/tests/test_rule.py',
    'phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py',
    'phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py',
    'phase178_r16_toda513_isolated/tests/test_registration.py',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py',
)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True,
                                   encoding='utf-8').strip()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R21_' + key + '=' + str(value), flush=True)


def preflight():
    require(Path(git('rev-parse','--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(git('branch','--show-current') == 'develop', 'DEVELOP_REQUIRED')
    actual = git('rev-parse','HEAD')
    require(actual == HEAD == git('rev-parse','origin/develop'), 'REVIEWED_HEAD_REQUIRED:' + actual)
    require(not git('status','--porcelain','--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path in TESTS:
        require((ROOT/path).is_file(), 'FOCUSED_TEST_MISSING:' + path)
    git('diff','--check')
    return actual


def snapshot():
    return git('rev-parse','HEAD'), git('status','--porcelain','--untracked-files=all')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        emit('HEAD', preflight())
        before = snapshot()
        if not args.dry_run:
            subprocess.run([sys.executable,'-B','-m','pytest','-q','-s',
                            '--import-mode=importlib','-p','no:cacheprovider',*TESTS],
                           cwd=ROOT, check=True)
        require(snapshot() == before, 'REPOSITORY_CHANGED_DURING_AUDIT')
    except Exception as exc:
        emit('ERROR', repr(exc))
        emit('GATE','FAIL_R21')
        return 1
    emit('NEW_TYPED_RULES',1)
    emit('NEW_MATHEMATICAL_LEMMAS',0)
    emit('NEW_GIVEN',0)
    emit('PUBLIC_WIRING','NOT_CHANGED')
    emit('HISTORICAL_GUARD','NOT_RUN_KNOWN_OPEN')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE','PASS_R21_DRYRUN' if args.dry_run else 'PASS_R21_FINITE_CYCLIC_DELTA_ZERO_ISOLATED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
