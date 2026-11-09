"""Guarded, idempotent R38 install; no git reset, pull or checkout."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = 'phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py'
BASE_HEAD = '660cadd928a2cbca00f71c5c35cd3af1230a54e9'
EXPECTED_SUCCESSOR_PREFIX = 'phase174_r3_r7_r37_upper_delta_surjectivity_isolated/'
PINNED = {
    'phase165_r52_r9_shared_math.py': '6b965aa49db2ad8707c75dcc953d3c78cdd3e458',
    'phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py': '66407339808ed4ba8a65c04fd3bfbbf05bde6745',
    'phase174_r3_r7_r7_composite_zero_audit/rule.py': 'd98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6',
    'phase174_r3_r7_r9_composition_associativity/rule.py': '2c44c68be90cb761d7bdd35e29f23977b5f93a2e',
    'phase174_r3_r7_r12_toda59_annihilator_source/rule.py': '32a5a2723cc19506695d4423e7ccb331d6f36ae2',
    'phase174_r3_r7_r13_cited_annihilator_bridge/registry.py': '489380d974d9e3a2869743325d21b15b4d64f808',
    'phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py': 'fac88c852cd4c18e8d013e3dc12ab95ad57d7b03',
    'phase174_r3_r7_r36_cited_kernel_provider_wiring/audit.py': 'b3d74e831edb49a60a54c5b609394fd815870068',
    'phase169_r10b_registered_stable_family_binding/family_registry.py': '4e461795954cc3e7a34fe9e3b47f77d00e5faeda',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
}


def git(*args: str) -> str:
    return subprocess.run(('git',) + args, cwd=ROOT, check=True,
                          capture_output=True, text=True,
                          encoding='utf-8', errors='replace').stdout.strip()


def normalized(raw: bytes) -> bytes:
    return raw.replace(b'\r\n', b'\n')


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def matches_blob(raw: bytes, sha: str) -> bool:
    n = normalized(raw)
    return len(sha) == 40 and any(git_blob(x) == sha for x in (
        raw, n, n.replace(b'\n', b'\r\n'),
    ))


def reviewed_patch_bytes() -> tuple[bytes, bytes]:
    base = normalized((PACKAGE / 'baseline' / 'context_provider_registry.py').read_bytes())
    patched = normalized((PACKAGE / 'replacement' / 'context_provider_registry.py').read_bytes())
    if git_blob(base) != 'da8036f299a02445c5b5b0743919640ca1524354':
        raise RuntimeError('R36 reviewed baseline context source mismatch')
    anchor = b'    for provider_id, function, statements in specifications:\n'
    if base.count(anchor) != 1 or patched.count(anchor) != 1:
        raise RuntimeError('R36 original anchor was changed')
    if patched.count(b'phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider') != 1:
        raise RuntimeError('R38 target source missing one provider import')
    before, after = patched.split(anchor)
    if after != base.split(anchor)[1]:
        raise RuntimeError('R38 changed existing historical provider loop')
    prefix = base.split(anchor)[0]
    if not before.startswith(prefix):
        raise RuntimeError('R38 changed existing historical provider prefix')
    addition = before[len(prefix):]
    if addition.count(b'expand_source_bound_zero_image_chain') != 2:
        raise RuntimeError('R38 added wrong provider use count')
    return base, patched


def verify_checkout() -> dict[str, object]:
    if os.path.normcase(str(Path(git('rev-parse', '--show-toplevel')).resolve())) != (
        os.path.normcase(str(ROOT.resolve()))
    ):
        raise RuntimeError('Extract R38 at repository root')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('R38 requires develop branch')
    local = git('rev-parse', 'HEAD')
    raw_remote = git('ls-remote', 'origin', 'refs/heads/develop')
    remote = raw_remote.split()[0] if raw_remote else ''
    if not remote:
        raise RuntimeError('Cannot verify GitHub origin/develop')
    if remote != BASE_HEAD:
        git('fetch', '-q', 'origin', 'develop')
        if git('rev-parse', 'FETCH_HEAD') != remote:
            raise RuntimeError('Remote advanced during fetch')
        if subprocess.run(('git', 'merge-base', '--is-ancestor', BASE_HEAD, remote),
                          cwd=ROOT, capture_output=True).returncode != 0:
            raise RuntimeError('Unreviewed GitHub develop history')
        changed_upstream = tuple(git('diff', '--name-only', BASE_HEAD, remote).splitlines())
        if not changed_upstream or any(
            not path.startswith(EXPECTED_SUCCESSOR_PREFIX) for path in changed_upstream
        ):
            raise RuntimeError('Upstream changes beyond reviewed R37 require re-audit')
    else:
        changed_upstream = ()
    if local not in (BASE_HEAD, remote):
        raise RuntimeError('Local HEAD differs from reviewed branch lineage')
    if git('diff', '--cached', '--name-only'):
        raise RuntimeError('Staged changes require manual review')
    changed = tuple(git('diff', '--name-only').splitlines())
    if changed not in ((), (TARGET,)):
        raise RuntimeError('Unrelated tracked edits must be reviewed separately')
    for path, sha in PINNED.items():
        file = ROOT / path
        if not file.is_file() or not matches_blob(file.read_bytes(), sha):
            raise RuntimeError('Reviewed source differs: ' + path)
    base, patched = reviewed_patch_bytes()
    live_file = ROOT / TARGET
    if not live_file.is_file():
        raise RuntimeError('R36 context provider is absent')
    contents = normalized(live_file.read_bytes())
    if contents not in (base, patched):
        raise RuntimeError('Context provider differs from approved baseline/replacement')
    if contents == base and changed:
        raise RuntimeError('Baseline content has unexpected tracked diff')
    if contents == patched and changed != (TARGET,) and local == BASE_HEAD:
        raise RuntimeError('Patched working tree lacks expected tracked diff')
    return {
        'local_head': local, 'remote_head': remote,
        'source_guard': 'PASS', 'r36_preserved': True,
        'reviewed_successor_files': len(changed_upstream),
        'mode': 'INSTALLED' if contents == patched else 'BASELINE',
        'tracked_files': list(changed),
    }


def install(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if not dry_run and state['mode'] == 'BASELINE':
        base, patched = reviewed_patch_bytes()
        path = ROOT / TARGET
        original = path.read_bytes()
        endline = b'\r\n' if original.count(b'\r\n') else b'\n'
        path.write_bytes(patched.replace(b'\n', endline))
        new_state = verify_checkout()
        if new_state['mode'] != 'INSTALLED':
            raise RuntimeError('R38 installed contents did not pass Source Guard')
        state = new_state
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    state = install(dry_run=args.dry_run)
    prefix = 'PHASE174_R3R7R38_'
    for key in ('local_head','remote_head','source_guard','r36_preserved',
                'reviewed_successor_files','mode'):
        print(prefix + key.upper() + '=' + str(state[key]))
    print(prefix + 'GATE=' + (
        'PASS_R38_REVIEWED_SOURCE_PREFLIGHT' if args.dry_run else
        'PASS_R38_GUARDED_PROVIDER_INSTALLED'
    ))
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
