"""Install a single public hook against the reviewed shared source."""
from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = '4ce2178c5eb23aba8aa5e179fdde8e266fa772af'
TARGET = 'phase165_r52_r9_shared_math.py'
PINS = {
    TARGET: '6501600e8683a812b9a08771e2d54c216535f8e6',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r52_r2_search_adapter.py': 'c1d08b803a4d9f9e4e1ad5180a1487422f1cd191',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase165_r12_r11_prop42_unified.py': '79752ec035244677ff6a54debff312e87a76fbf2',
    'phase176_r3r46r1_prior_group_availability/provider.py': 'dda7ac9fb93a60f94631e1a7b0cdf416dbb9cc33',
    'phase178_r3_finite_group_surjectivity_audit/audit.py': 'd69bb7c7bc4d50fbad709890a5a7c97e41cc573a',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
}
R8_HASHES = {'phase178_r8_finite_group_surjective_injective_isolated/rule.py': '8729188fe7398ba7406059671788b3733e0c9d70fe09206e4852ad14ef145b71', 'phase178_r8_finite_group_surjective_injective_isolated/tests/test_rule.py': '01e2cc0068d14c6b4a85cfd12c9016d26057b00663ae55c993f882c0cf200f27'}
PINS.update({
    'phase177_r15_finite_cyclic_delta_injective_public/provider.py': 'd22833c2ee5ad7c54c7690436e608e225c61a6e0',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase171_r2j_r4_r6_middle_cardinality/source.py': '5df4d3e247d1e3f9a578dd4fc9e7434c3d3f62eb',
    'phase177_r14_finite_cyclic_delta_injective_isolated/rule.py': 'fba57005273dfdf795501df5f71b3822f4ecddfe',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
})
PINS.update({
    'phase178_r6_finite_group_cardinality_isolated/rule.py': '8c6de74a331d75b38d592603062d99c591a040b9',
    'phase178_r6_finite_group_cardinality_isolated/tests/test_rule.py': '4c2a181164acf13ac1fb85ae8c81e3e5bdd0dffc',
    'phase178_r7_finite_group_cardinality_public/provider.py': '51b616d49ffed46d0589406a7e3856fed45c29b4',
    'phase178_r7_finite_group_cardinality_public/tests/test_provider.py': '2bf5c387098e20a1f6decc8bf2089f31693794ab',
    'phase178_r4_delta_surjective_zero_suspension_isolated/rule.py': '60b91c4ba674ca4680f0c3b353ceb873ecebc7ee',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase174_r3_r7_r32_lower_delta_kernel_audit/kernel_contract.py': 'c2357859b00ed0b446bac7a060a6d0c134fc7de5',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'phase177_r18_final_verified_proof_audit/audit.py': '704d5af7a98111e0365ad15fd1e2190891e23df5',
})
ANCHOR = '    # Phase 177 R8: screened unsigned Prop 2.5 backward candidates.\n'
HOOK = (
    '    # Phase 178 R9: expose the unchanged R8 equal-cardinality injectivity rule.\n'
    '    from phase178_r9_finite_group_surjective_injective_public.provider import (\n'
    '        build_public_finite_surjective_injective_provider,\n'
    '    )\n'
    '    extra_providers = tuple(extra_providers) + (\n'
    '        build_public_finite_surjective_injective_provider(bridge=bridge, proof_target=proof_target),\n'
    '    )\n\n'
)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def git_text(*args):
    return git(*args).decode('utf-8').strip()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalize(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def proposed_source(source):
    require(source.count(ANCHOR) == 1, 'R9_ANCHOR_NOT_UNIQUE')
    require('build_public_finite_surjective_injective_provider' not in source, 'R9_ALREADY_PRESENT_IN_BASE')
    tree = ast.parse(source)
    outer, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider']
    line = source[:source.index(ANCHOR)].count('\n') + 1
    require(outer.lineno < line <= outer.end_lineno, 'R9_ANCHOR_OUTSIDE_SHARED_PROVIDER')
    revised = source.replace(ANCHOR, HOOK + ANCHOR, 1)
    ast.parse(revised)
    return revised


def full_review_source(source):
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    selected = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom)) or (isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider')]
    return '\n'.join(''.join(lines[n.lineno-1:n.end_lineno]) for n in selected)


def preflight():
    require(Path(os.fsdecode(git('rev-parse', '--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(git_text('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = git_text('rev-parse', 'HEAD')
    require(head == git_text('rev-parse', 'origin/develop'), 'HEAD_NOT_REMOTE')
    require(git_text('merge-base', BASE, head) == BASE, 'REVIEWED_BASE_REQUIRED')
    require(not git_text('diff', '--cached', '--name-only'), 'STAGED_CHANGES_REFUSED')
    changed = set(git_text('diff', '--name-only', 'HEAD').splitlines())
    require(not changed - {TARGET}, 'UNRELATED_TRACKED_CHANGES:'+repr(sorted(changed)))
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for name, pin in PINS.items():
        require(git_text('rev-parse', 'HEAD:'+name) == pin, 'PIN_CHANGED:'+name)
        if name != TARGET:
            require(normalize((ROOT/name).read_bytes()) == normalize(git('show', 'HEAD:'+name)), 'DEPENDENCY_CHANGED:'+name)
    for name, digest in R8_HASHES.items():
        actual = hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        require(actual == digest, 'R8_REVIEWED_FILE_CHANGED:'+name)
    original = normalize(git('show', 'HEAD:'+TARGET))
    revised = proposed_source(original)
    current = (ROOT/TARGET).read_bytes()
    require(normalize(current) in (original, revised), 'UNREVIEWED_TARGET_CHANGE')
    rest = current.replace(b'\r\n', b'')
    require(b'\r' not in rest and not (b'\r\n' in current and b'\n' in rest), 'UNSUPPORTED_MIXED_EOL')
    eol = '\r\n' if b'\r\n' in current else '\n'
    encoding = 'utf-8-sig' if current.startswith(b'\xef\xbb\xbf') else 'utf-8'
    updated = revised.replace('\n', eol).encode(encoding)
    git('diff', '--check')
    return head, current, updated, revised
