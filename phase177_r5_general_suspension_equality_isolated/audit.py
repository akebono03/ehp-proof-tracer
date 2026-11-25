"""Pin reviewed inputs and check that R5 has not changed tracked files."""
from __future__ import annotations

from pathlib import Path

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob, snapshot

ROOT = Path(__file__).resolve().parents[1]
HEAD = '61911911e25b2ae379669be809001c1237051d2c'
PINS = {
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'relation_rules.py': '0da057f35b7ebd51b31c247e04bc4b15b1dcff9e',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase165_r52_r9_shared_math.py': '87e0fe1202fa265c7530d0dd7e2b0adda2f5ebc2',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase177_r4_general_iterated_suspension_audit/audit.py': '9062bb1fa05e57b371699d81b92816d65ddd7ed0',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase169_r10eq_r1_universal_stable_definition/definition.py': '0c74d121419b6755e947a367d7de465d81193174',
    'phase176_r3r34_composite_suspension_isolated/source.py': '2b173d22f0bd75b469b97c5a49739a5a8f474a29',
    'phase171_r2i_eta_hopf_bridge/source.py': '4a15d33964f0c87edfe3e7f8337c720c04d17e91',
}


def preflight():
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT:
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    local, remote = git('rev-parse', 'HEAD'), git('rev-parse', 'origin/develop')
    if (local, remote) != (HEAD, HEAD):
        raise RuntimeError(f'REVIEWED_HEAD_REQUIRED:expected={HEAD};local={local};origin/develop={remote}')
    if git('status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('TRACKED_WORKTREE_NOT_CLEAN')
    for path, pin in PINS.items():
        if git('rev-parse', 'HEAD:' + path) != pin or not matches_blob((ROOT/path).read_bytes(), pin):
            raise RuntimeError('SOURCE_PIN_CHANGED:' + path)


def main():
    before = snapshot()
    preflight()
    if snapshot() != before:
        raise RuntimeError('REPOSITORY_CHANGED_DURING_PREFLIGHT')
    print('PHASE177_R5_HEAD='+HEAD)
    print('PHASE177_R5_PUBLIC_CONNECTION=NOT_ADDED')
    print('PHASE177_R5_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R5_GATE=PASS_R5_READ_ONLY_PREFLIGHT')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
