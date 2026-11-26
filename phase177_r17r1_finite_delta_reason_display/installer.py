"""Install the R17R1 hook and complete narrative display-only compression."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import subprocess
import tempfile

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob
from phase177_r6_general_suspension_public.installer import normalize

ROOT = Path(__file__).resolve().parents[1]
HEAD = '6d61c70b985bef4550b35ce6fb3f6c130cd8631b'
TARGET = 'phase168_r3_27_typed_statement_projection.py'
MODEL = 'phase168_r3_5_model_renderer.py'
PINS = {
    TARGET: '633fa68bd789ab3d4b61e34f47e952d35535b672',
    'toda_human_readable_renderer.py': 'cebe266300f31ce50abba8065235a6646915088d',
    'phase168_r3_5_model_renderer.py': 'c58c19f7234def48b743491c6a9c045345ac35e6',
    'phase177_r14_finite_cyclic_delta_injective_isolated/rule.py': 'fba57005273dfdf795501df5f71b3822f4ecddfe',
    'phase165_r52_r9_shared_math.py': 'f4383a0c248fe62903203d1863df345740581c59',
}
ANCHOR = 'def typed_sentence(statement, step):\n'
PATCH = (
    '    from phase177_r17r1_finite_delta_reason_display.projection import project_finite_delta_reason\n'
    '    finite_delta_reason = project_finite_delta_reason(statement, step)\n'
    '    if finite_delta_reason is not None:\n'
    '        return finite_delta_reason\n'
)


def proposed_source(source):
    if source.count(ANCHOR) != 1 or 'project_finite_delta_reason' in source:
        raise ValueError('R17R1_ANCHOR_OR_DUPLICATE')
    tree = ast.parse(source)
    outer, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'typed_sentence']
    line = source[:source.index(ANCHOR)].count('\n') + 1
    if line != outer.lineno:
        raise ValueError('R17R1_ANCHOR_OUTSIDE_SHARED_PROVIDER')
    revised = source.replace(ANCHOR, ANCHOR + PATCH, 1)
    ast.parse(revised)
    return revised


def preflight():
    if Path(git('rev-parse','--show-toplevel')).resolve() != ROOT or git('branch','--show-current') != 'develop':
        raise RuntimeError('WRONG_ROOT_OR_BRANCH')
    local, remote = git('rev-parse','HEAD'), git('rev-parse','origin/develop')
    if (local, remote) != (HEAD, HEAD):
        raise RuntimeError(f'REVIEWED_HEAD_REQUIRED:expected={HEAD};local={local};remote={remote}')
    if git('diff','--cached','--name-only'):
        raise RuntimeError('STAGED_CHANGES_REFUSED')
    if set(git('diff','--name-only','HEAD').splitlines()) - {TARGET, MODEL}:
        raise RuntimeError('UNRELATED_TRACKED_CHANGES_REFUSED')
    for name, pin in PINS.items():
        if git('rev-parse','HEAD:'+name) != pin:
            raise RuntimeError('HEAD_BLOB_CHANGED:'+name)
        if name not in (TARGET, MODEL) and not matches_blob((ROOT/name).read_bytes(),pin):
            raise RuntimeError('DEPENDENCY_CHANGED:'+name)
    files = []
    for name, transform in ((TARGET, proposed_source), (MODEL, proposed_model_source)):
        original = normalize(subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT))
        revised = transform(original)
        current = (ROOT/name).read_bytes()
        if normalize(current) not in (original,revised):
            raise RuntimeError('UNRELATED_TARGET_CHANGE_REFUSED:'+name)
        rest = current.replace(b'\r\n',b'')
        if b'\r' in rest or (b'\r\n' in current and b'\n' in rest):
            raise RuntimeError('UNSUPPORTED_MIXED_EOL:'+name)
        eol = '\r\n' if b'\r\n' in current else '\n'
        encoding = 'utf-8-sig' if current.startswith(b'\xef\xbb\xbf') else 'utf-8'
        files.append((name,current,revised.replace('\n',eol).encode(encoding),revised))
    return tuple(files)


def proposed_model_source(source):
    anchor = '    for index in order:\n        if order_summary is not None and index == model.root_index:'
    sentence = '        sentence = typed_sentence(step.conclusion, step)\n'
    if (source.count(anchor) != 1 or source.count(sentence) != 1
            or 'project_concise_delta_display' in source):
        raise ValueError('R17R1R2_MODEL_ANCHOR_OR_DUPLICATE')
    hook = (
        '    concise_delta_sentences = {}\n'
        '    if not incomplete:\n'
        '        from phase177_r17r1_finite_delta_reason_display.projection import project_concise_delta_display\n'
        '        hidden, concise_delta_sentences = project_concise_delta_display(\n'
        '            model, order, suppressed_body_indices,\n'
        '        )\n'
        '        suppressed_body_indices.update(hidden)\n'
    )
    revised = source.replace(anchor,hook+anchor,1).replace(
        sentence,'        sentence = concise_delta_sentences.get(index)\n'
        '        if sentence is None:\n'
        '            sentence = typed_sentence(step.conclusion, step)\n',1)
    ast.parse(revised)
    return revised


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    files = preflight()
    output = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    output.mkdir(parents=True,exist_ok=True)
    for name,current,updated,revised in files:
        review = output/(name+'.full.txt')
        review.write_text(revised,encoding='utf-8')
        if not args.dry_run and current != updated:
            (output/(name+'.before')).write_bytes(current)
            (ROOT/name).write_bytes(updated)
        if not args.dry_run and (ROOT/name).read_bytes() != updated:
            raise RuntimeError('INSTALL_BYTE_MISMATCH:'+name)
        print('PHASE177_R17R1R2_FULL_CODE='+str(review))
    print('PHASE177_R17R1R2_HEAD='+HEAD)
    print('PHASE177_R17R1R2_GATE='+('PASS_R17R1R2_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R17R1R2_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
