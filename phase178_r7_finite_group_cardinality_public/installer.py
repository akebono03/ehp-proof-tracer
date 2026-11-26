"""Install a single public hook against the reviewed shared source."""
from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = '6f0c63086f40cac793f4ad2b8b1658a8a2a03960'
TARGET = 'phase165_r52_r9_shared_math.py'
PINS = {
    TARGET: '459bc08b809fc51e89d89d4c8240b5ce0d591cdf',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r52_r2_search_adapter.py': 'c1d08b803a4d9f9e4e1ad5180a1487422f1cd191',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase165_r12_r11_prop42_unified.py': '79752ec035244677ff6a54debff312e87a76fbf2',
    'phase176_r3r46r1_prior_group_availability/provider.py': 'dda7ac9fb93a60f94631e1a7b0cdf416dbb9cc33',
    'phase178_r3_finite_group_surjectivity_audit/audit.py': 'd69bb7c7bc4d50fbad709890a5a7c97e41cc573a',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
}
R6_HASHES = {
    'phase178_r6_finite_group_cardinality_isolated/rule.py': 'ccf9ec50e485caac537d30c743883db24d8c77b8b43f11282d15090303b05380',
    'phase178_r6_finite_group_cardinality_isolated/tests/test_rule.py': '8f9803a33d2243cdca163f596a4a6035c0d5496c55386df7cdc8656a987327f4',
}
PINS.update({
    'phase177_r15_finite_cyclic_delta_injective_public/provider.py': 'd22833c2ee5ad7c54c7690436e608e225c61a6e0',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase171_r2j_r4_r6_middle_cardinality/source.py': '5df4d3e247d1e3f9a578dd4fc9e7434c3d3f62eb',
    'phase177_r14_finite_cyclic_delta_injective_isolated/rule.py': 'fba57005273dfdf795501df5f71b3822f4ecddfe',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
})
ANCHOR = '    # Phase 177 R8: screened unsigned Prop 2.5 backward candidates.\n'
HOOK = (
    '    # Phase 178 R7: expose the unchanged R6 finite group cardinality rule.\n'
    '    from phase178_r7_finite_group_cardinality_public.provider import (\n'
    '        build_public_finite_cardinality_provider,\n'
    '    )\n'
    '    extra_providers = tuple(extra_providers) + (\n'
    '        build_public_finite_cardinality_provider(bridge=bridge, proof_target=proof_target),\n'
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
    require(source.count(ANCHOR) == 1, 'R7_ANCHOR_NOT_UNIQUE')
    require('build_public_finite_cardinality_provider' not in source, 'R7_ALREADY_PRESENT_IN_BASE')
    tree = ast.parse(source)
    outer, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider']
    line = source[:source.index(ANCHOR)].count('\n') + 1
    require(outer.lineno < line <= outer.end_lineno, 'R7_ANCHOR_OUTSIDE_SHARED_PROVIDER')
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
    for name, digest in R6_HASHES.items():
        actual = hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        require(actual == digest, 'R6_REVIEWED_FILE_CHANGED:'+name)
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
