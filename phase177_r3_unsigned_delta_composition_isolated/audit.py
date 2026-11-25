"""Verify reviewed repository dependencies and source integrity without modifying them."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
HEAD = '2d09ecbe10b60a38179022da561931a8e4bb39ba'
PINS = {
    'phase165_r52_r9_shared_math.py': '87e0fe1202fa265c7530d0dd7e2b0adda2f5ebc2',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase175_r4r12r10r1_cited_511_public/provider.py': '6a57c443d8c69192ba58e213821cb62aac37553f',
    'phase175_r4r10_cited_58_prop25_public/source.py': 'b5162bdaac25e4578973816290207379734229f6',
    'phase175_r4r10_cited_58_prop25_public/provider.py': 'be1d726fe98c0258685674ea41099aab1103f318',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase175_r4r12_public_two_summand_quotient/provider.py': '1b34fe0d2707a51af7acc52eaa7d38209e90dfa2',
    'phase175_r4r12r9_delta_generator_image_bridge/rule.py': 'cfff81f4662825b78f30f8b7b4886cb27333b6c2',
    'phase175_r4r12r13r2_delta_injective_e_surjective/rule.py': '763b98521f8d78bbca1f07944194384c55a9ed57',
    'phase168_r2_8_3_generator_identity/identity.py': '9052b3d75809a4a45e026d93da80f6d4aaad8b62',
    'sources/toda/Toda_02_2.tex': 'ed3667788805a429140dedf5d183736e43e0f2c3',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
    'map_facts.py': '86fbf404783e15d344595bf54df5a9a8bafc35fc',
    'phase175_r4r7_prop25_typed_composition/tests/test_rule.py': 'aefd725eb326ea9bcca54f93019b479f58a93ad5',
}

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8').strip()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def matches_blob(raw, pin):
    lf = raw.replace(b'\r\n', b'\n')
    return pin in (blob(raw), blob(lf), blob(lf.replace(b'\n', b'\r\n')))


def snapshot():
    return (git('rev-parse', 'HEAD'), git('diff', '--binary', 'HEAD'),
            git('diff', '--cached', '--binary'), git('status', '--porcelain', '--untracked-files=all'))


def preflight():
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT:
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    local_head = git('rev-parse', 'HEAD')
    remote_head = git('rev-parse', 'origin/develop')
    if local_head != HEAD or remote_head != HEAD:
        raise RuntimeError(
            f'REVIEWED_HEAD_REQUIRED:expected={HEAD};local={local_head};origin/develop={remote_head}'
        )
    if git('status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('TRACKED_WORKTREE_NOT_CLEAN')
    for name, pin in PINS.items():
        if git('rev-parse', 'HEAD:' + name) != pin or not matches_blob((ROOT/name).read_bytes(), pin):
            raise RuntimeError('SOURCE_PIN_CHANGED:' + name)
    from phase175_r4r12r10r1_cited_511_public.source import verify_cited_511
    from phase175_r4r10_cited_58_prop25_public.source import source_positions
    positions = source_positions(ROOT)
    positions['toda:(5.11)'] = verify_cited_511(ROOT)
    if not positions['toda:Proposition 2.5'] < positions['toda:(5.11)']:
        raise RuntimeError('SOURCE_ORDER_INVALID')
    return {'head': HEAD, 'source_positions': positions, 'pins': PINS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        before = snapshot()
        result = preflight()
        if snapshot() != before:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_PREFLIGHT')
        print('PHASE177_R3_HEAD=' + result['head'])
        print('PHASE177_R3_SOURCE_POSITIONS=' + repr(result['source_positions']))
        print('PHASE177_R3_PUBLIC_CONNECTION=NOT_ADDED')
        print('PHASE177_R3_FULL_PYTEST=NOT_RUN')
        print('PHASE177_R3_GATE=' + ('PASS_R3_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R3_DEPENDENCIES_VERIFIED'))
        return 0
    except Exception as exc:
        print('PHASE177_R3_ERROR=' + repr(exc))
        print('PHASE177_R3_GATE=FAIL_R3')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
