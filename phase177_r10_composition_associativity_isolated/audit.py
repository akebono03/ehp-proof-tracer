"""Pin R8 sources; permit only a subsequent R9 audit-only commit."""
from pathlib import Path
import subprocess

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob, snapshot

ROOT = Path(__file__).resolve().parents[1]
HEAD = '8127b7b6424f294a6e03b3e2d12e66a83e77cf5d'
PINS = {
    'phase165_r52_r9_shared_math.py': 'cb89639e7ee2088cf5bb2cf0f1aeaf10cebaf9fb',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'relation_rules.py': '0da057f35b7ebd51b31c247e04bc4b15b1dcff9e',
    'phase174_r3_r7_r9_composition_associativity/rule.py': '2c44c68be90cb761d7bdd35e29f23977b5f93a2e',
    'phase174_r3_r7_r9_composition_associativity/tests/test_rule.py': 'f23fda6f5da69c7bc04fe6493f295d3105b0d807',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase175_r4r12_public_two_summand_quotient/provider.py': '1b34fe0d2707a51af7acc52eaa7d38209e90dfa2',
    'phase175_r4r12r9_delta_generator_image_bridge/rule.py': 'cfff81f4662825b78f30f8b7b4886cb27333b6c2',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase175_r4r12r13r7_typed_nu_prime_notation/notation.py': '70ee0c0a00002f9946ac8d243097fd87b3e4c299',
    'phase176_r3r50_strict_nu_prime_connection/notation.py': '2ed8c8b3ee8324ad7f37a61371e8b7323f2bd85c',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase177_r4_general_iterated_suspension_audit/audit.py': '9062bb1fa05e57b371699d81b92816d65ddd7ed0',
    'phase177_r7_left_composition_reuse_audit/audit.py': 'd0951ce94a0deba8106ff641d2394c9389341b0e',
    'phase177_r8_unsigned_delta_public/provider.py': '3243162cfd334e7b71a67753603e3ef5f63237f7',
    'phase177_r8_unsigned_delta_public/tests/test_public.py': '340ad0932ee3df000c5ceec6df76880fe77db562',
}


def preflight():
    if Path(git('rev-parse','--show-toplevel')).resolve() != ROOT or git('branch','--show-current') != 'develop':
        raise RuntimeError('WRONG_REPOSITORY_OR_BRANCH')
    local,remote = git('rev-parse','HEAD'),git('rev-parse','origin/develop')
    if local != remote:
        raise RuntimeError('LOCAL_REMOTE_HEAD_MISMATCH')
    if local != HEAD:
        if subprocess.run(['git','merge-base','--is-ancestor',HEAD,local],cwd=ROOT).returncode:
            raise RuntimeError('REVIEWED_BASE_NOT_ANCESTOR')
        changes = git('diff','--name-status','--no-renames',HEAD,local).splitlines()
        if not changes or any(not line.startswith('A\tphase177_r9_delta_rhs_normalization_audit/') for line in changes):
            raise RuntimeError('NON_R9_BASELINE_CHANGE_REFUSED')
    if git('status','--porcelain','--untracked-files=no'):
        raise RuntimeError('TRACKED_WORKTREE_NOT_CLEAN')
    for path,pin in PINS.items():
        if git('rev-parse','HEAD:'+path) != pin or not matches_blob((ROOT/path).read_bytes(),pin):
            raise RuntimeError('SOURCE_PIN_CHANGED:'+path)
    return local


def main():
    before = snapshot()
    head = preflight()
    if snapshot() != before:
        raise RuntimeError('REPOSITORY_CHANGED_DURING_PREFLIGHT')
    print('PHASE177_R10_HEAD='+head)
    print('PHASE177_R10_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R10_GATE=PASS_R10_READ_ONLY_PREFLIGHT')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
