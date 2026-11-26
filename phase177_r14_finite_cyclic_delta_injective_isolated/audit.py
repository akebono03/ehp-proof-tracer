"""Read-only preflight and focused isolated regression runner."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob, snapshot

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
BASE = '6482605898a83a3007565988c252cb594cef9a1d'
PINS = {
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase165_r52_r9_shared_math.py': 'b30a086b318ea9d78e9d5d3217f77a2c920ca8ca',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase171_r2j_r4_r7_nonzero_nu_order/source.py': '5862ffaa1cc4a6c1046bc153eb8893a75ced3e7a',
    'phase174_r3_r7_r32_lower_delta_kernel_audit/kernel_contract.py': 'c2357859b00ed0b446bac7a060a6d0c134fc7de5',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase175_r4r12r9_delta_generator_image_bridge/rule.py': 'cfff81f4662825b78f30f8b7b4886cb27333b6c2',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase175_r4r12r10r1_cited_511_public/provider.py': '6a57c443d8c69192ba58e213821cb62aac37553f',
    'phase175_r4r12r13r2_delta_injective_e_surjective/rule.py': '763b98521f8d78bbca1f07944194384c55a9ed57',
    'phase175_r4r12r13r4_hopf_zero_public/rule.py': '74b7e8dee9032f5b0cbfc0086646bb423e73be74',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase177_r7_left_composition_reuse_audit/audit.py': 'd0951ce94a0deba8106ff641d2394c9389341b0e',
}
TESTS = (
    PACKAGE + '/tests',
    'phase175_r4r12r9_delta_generator_image_bridge/tests/test_rule.py',
    'phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py',
    'phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py',
    'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
)


def preflight():
    if Path(git('rev-parse','--show-toplevel')).resolve() != ROOT:
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch','--show-current') != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    head = git('rev-parse','HEAD')
    if head != git('rev-parse','origin/develop'):
        raise RuntimeError('LOCAL_REMOTE_HEAD_MISMATCH')
    git('merge-base','--is-ancestor',BASE,head)
    if git('status','--porcelain','--untracked-files=no'):
        raise RuntimeError('TRACKED_WORKTREE_NOT_CLEAN')
    for name, pin in PINS.items():
        if git('rev-parse','HEAD:'+name) != pin or not matches_blob((ROOT/name).read_bytes(),pin):
            raise RuntimeError('SOURCE_PIN_CHANGED:'+name)
    for name in TESTS:
        if not (ROOT/name).exists():
            raise RuntimeError('FOCUSED_TEST_MISSING:'+name)
    print('PHASE177_R14_HEAD='+head,flush=True)
    print('PHASE177_R14_REVIEWED_BASE='+BASE,flush=True)


def execute(dry_run):
    before = snapshot()
    preflight()
    if not dry_run:
        env = dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
        cmd = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
        subprocess.run(cmd,cwd=ROOT,env=env,check=True)
    if snapshot() != before:
        raise RuntimeError('REPOSITORY_CHANGED_DURING_ISOLATED_TEST')
    print('PHASE177_R14_PUBLIC_CONNECTION=NOT_ADDED')
    print('PHASE177_R14_NEW_MATH_RULES_ISOLATED=2')
    print('PHASE177_R14_NEW_GIVEN=0')
    print('PHASE177_R14_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R14_GATE='+('PASS_R14_READ_ONLY_DRYRUN' if dry_run else 'PASS_R14_FINITE_CYCLIC_DELTA_INJECTIVITY_ISOLATED'))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    return execute(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
