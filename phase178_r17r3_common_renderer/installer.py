"""Apply three audited Renderer hooks; refuse unrelated or unreviewed changes."""
import argparse
import ast
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HEAD = '720a7e8658a3f7e94f92a20ab530f763f1b421e1'
RENDERER = 'phase168_r3_5_model_renderer.py'
TYPED = 'phase168_r3_27_typed_statement_projection.py'
REFERENCE = 'phase168_r3_37c_reference_projection.py'
PINS = {
    RENDERER: '5c03a4cb06a1e517bd6817bebc1f1d5fa786cfca',
    TYPED: '2c6636f1118bacff96f64a7f8983f9cdbb847972',
    REFERENCE: 'a4140294f53c62972c35dd67fbfdfa1430232cae',
    'phase177_r17r6r1_suspension_composition_display/projection.py': 'dd05a23a458aca832c323fe6320c567734dd4ecb',
    'phase178_r17_finite_cyclic_quotient_isolated/rule.py': 'd743fda8b347910fe0d7ab6873d35f68973bcbf4',
    'phase178_r15_toda512_isolated/source.py': 'c0dedf1aa758adf6f7f925ea86ec7a85c5f994dc',
    'phase178_r17r2_cited_512_priority/audit.py': '078cb8361a159e5dd19ba9f7272d7d54b056248b',
    'phase177_r17r3_rank_two_quotient_display/tests/test_display.py': 'd57adccbe17a1f3037b1e247e6da78b4b18f15dc',
    'phase177_r17r6r1_suspension_composition_display/tests/test_display.py': 'aff28b4aab345e41001e338cf7cf0e808cffb4c5',
}
PATCHES = {
    TYPED: ('typed_sentence',
        '    from phase177_r17r1_finite_delta_reason_display.projection import project_finite_delta_reason\n',
        '    from phase178_r17r3_common_renderer.projection import finite_cyclic_quotient_reason\n'
        '    cyclic_quotient_reason = finite_cyclic_quotient_reason(statement, step)\n'
        '    if cyclic_quotient_reason is not None:\n'
        '        return cyclic_quotient_reason\n'),
    REFERENCE: ('_verified_source_sentence',
        '    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource\n',
        '    from phase178_r17r3_common_renderer.projection import cited_512_reference_sentence\n'
        '    cited_512 = cited_512_reference_sentence(statement)\n'
        '    if cited_512 is not None:\n'
        '        return cited_512\n'),
    RENDERER: ('render_model_backed_narrative_markdown',
        '        from phase178_r12r1_suspension_composition_display.projection import (\n',
        '        from phase178_r17r3_common_renderer.projection import (\n'
        '            project_composite_suspension_lines, project_finite_quotient_order,\n'
        '        )\n'
        '        lines = project_composite_suspension_lines(lines, model, protected_equalities)\n'
        '        lines = project_finite_quotient_order(lines, model, protected_equalities)\n'),
}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def git_text(*args):
    return git(*args).decode('utf-8').strip()


def normalized(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def matches_blob(raw, pin):
    lf = raw.replace(b'\r\n', b'\n')
    return any(hashlib.sha1(b'blob ' + str(len(b)).encode('ascii') + b'\0' + b).hexdigest() == pin
               for b in (raw, lf, lf.replace(b'\n', b'\r\n')))


def proposed(source, function, anchor, addition):
    tree = ast.parse(source)
    fn, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == function]
    if source.count(anchor) != 1:
        raise RuntimeError('UNEXPECTED_ANCHOR:' + function)
    line = source[:source.index(anchor)].count('\n') + 1
    if not fn.lineno < line <= fn.end_lineno:
        raise RuntimeError('ANCHOR_OUTSIDE_FUNCTION:' + function)
    updated = source.replace(anchor, addition + anchor, 1)
    ast.parse(updated)
    return updated


def preflight():
    if Path(git_text('rev-parse', '--show-toplevel')).resolve() != ROOT:
        raise RuntimeError('WRONG_ROOT')
    if git_text('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    if git_text('rev-parse', 'HEAD') != HEAD or git_text('rev-parse', 'origin/develop') != HEAD:
        raise RuntimeError('REVIEWED_HEAD_REQUIRED:' + HEAD)
    if git_text('diff', '--cached', '--name-only'):
        raise RuntimeError('STAGED_CHANGES_PRESENT')
    if set(git_text('diff', '--name-only', 'HEAD').splitlines()) - set(PATCHES):
        raise RuntimeError('UNRELATED_TRACKED_CHANGES')
    if os.environ.get('PYTEST_ADDOPTS', '').strip():
        raise RuntimeError('PYTEST_ADDOPTS_REQUIRES_REVIEW')
    changes = {}
    for name, pin in PINS.items():
        if git_text('rev-parse', 'HEAD:' + name) != pin:
            raise RuntimeError('DEPENDENCY_BLOB_CHANGED:' + name)
        raw = (ROOT / name).read_bytes()
        if name not in PATCHES:
            if not matches_blob(raw, pin):
                raise RuntimeError('DEPENDENCY_WORKTREE_CHANGED:' + name)
            continue
        baseline = git('show', HEAD + ':' + name)
        if not matches_blob(baseline, pin):
            raise RuntimeError('BASELINE_CHANGED:' + name)
        source = normalized(baseline)
        updated = proposed(source, *PATCHES[name])
        if normalized(raw) not in (source, updated):
            raise RuntimeError('UNREVIEWED_WORKTREE_CHANGE:' + name)
        rest = raw.replace(b'\r\n', b'')
        if b'\r' in rest or (b'\r\n' in raw and b'\n' in rest):
            raise RuntimeError('MIXED_EOL:' + name)
        eol = '\r\n' if b'\r\n' in raw else '\n'
        encoding = 'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
        changes[name] = (raw, updated.replace('\n', eol).encode(encoding), updated)
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    changes = preflight()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / Path(__file__).parent.name
    folder.mkdir(parents=True, exist_ok=True)
    for name, (raw, updated, text) in changes.items():
        (folder / (name + '.full.txt')).write_text(text, encoding='utf-8')
        if not args.dry_run and raw != updated:
            (folder / (name + '.before')).write_bytes(raw)
    if not args.dry_run:
        for name, (raw, updated, text) in changes.items():
            if (ROOT / name).read_bytes() != raw:
                raise RuntimeError('WORKTREE_CHANGED_DURING_INSTALL:' + name)
        for name, (raw, updated, text) in changes.items():
            if raw != updated:
                (ROOT / name).write_bytes(updated)
            if (ROOT / name).read_bytes() != updated:
                raise RuntimeError('INSTALL_BYTE_MISMATCH:' + name)
    print('PHASE178_R17R3_HEAD=' + HEAD)
    print('PHASE178_R17R3_FULL_CODE=' + str(folder))
    print('PHASE178_R17R3_INSTALL=' + ('PASS_DRYRUN' if args.dry_run else 'PASS'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
