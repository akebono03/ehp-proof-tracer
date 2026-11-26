"""Install the reviewed R17R5 emission-only hook, preserving the verified proof."""
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
BASE = 'b30678c9aca3188d0190bbf2b5e36fcdb2b24c16'
TARGET = 'phase168_r3_5_model_renderer.py'
PINS = {
    TARGET: 'c2557db64091344e48dc3c32b3bd2a93addb6a5c',
    'phase168_r2_8_3_generator_identity/identity.py': '9052b3d75809a4a45e026d93da80f6d4aaad8b62',
    'phase168_r3_27_typed_statement_projection.py': 'fc19a65386b92ce096c3f4c55fc10622b19c3d65',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase175_r4r12r10r1_cited_511_public/provider.py': '6a57c443d8c69192ba58e213821cb62aac37553f',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase176_r3r55_equality_display_isolated/projection.py': 'f2bedfc04f96f27a771fbdebaa282fd9c2c9a075',
    'phase177_r17r4r1_prop25_suspension_elision/projection.py': '1d6dd710fcedd025a385480b22b12aaee46b4215',
    'phase177_r17r4r2_prop25_equality_chain/projection.py': 'a5f35b71b053c603f540f9750b3af50101dde3ab',
    'phase177_r17r4r2_prop25_equality_chain/tests/test_display.py': 'f8ab82d2d1ad5d40f10c9e271e5c7195616b28a8',
    'phase177_r17r1_finite_delta_reason_display/tests/test_display.py': '5c145a1a8a04d45384cfe52fbc112aa3c5616941',
    'phase177_r17r3_rank_two_quotient_display/tests/test_display.py': '9d3c1d32cb44fcc9210d2535ca7fbabd583e7278',
}
INIT = '    prop25_chain_sentences = {}\n'
START = '        if sentence is not None:\n            # The certified kernel step'
END = '            lines.append("")\n    if incomplete:\n'
HOOK = '''        if (not incomplete and len(lines) == cited_equality_start + 2
                and lines[-1] == ""):
            from phase177_r17r5_duplicate_cited_equality.projection import (
                omit_duplicate_cited_equality,
            )
            if omit_duplicate_cited_equality(
                model, index, lines[cited_equality_start], retained_cited_equalities,
                protected_equalities,
            ):
                del lines[cited_equality_start:]
'''


def replace_inside(source, anchor, replacement):
    if source.count(anchor) != 1:
        raise RuntimeError('UNEXPECTED_RENDERER_ANCHOR:'+repr(anchor))
    tree = ast.parse(source)
    fn, = [n for n in tree.body if isinstance(n, ast.FunctionDef)
           and n.name == 'render_model_backed_narrative_markdown']
    line = source[:source.index(anchor)].count('\n') + 1
    if not fn.lineno < line < fn.end_lineno:
        raise RuntimeError('ANCHOR_OUTSIDE_RENDERER')
    result = source.replace(anchor, replacement, 1)
    ast.parse(result)
    return result


def proposed_source(source):
    source = replace_inside(source, INIT, INIT+'    retained_cited_equalities = {}\n')
    source = replace_inside(source, START, '        cited_equality_start = len(lines)\n'+START)
    return replace_inside(source, END, '            lines.append("")\n'+HOOK+'    if incomplete:\n')


def preflight():
    if Path(git('rev-parse','--show-toplevel')).resolve() != ROOT or git('branch','--show-current') != 'develop':
        raise RuntimeError('WRONG_ROOT_OR_BRANCH')
    head = git('rev-parse','HEAD')
    if head != BASE or git('rev-parse','origin/develop') != BASE:
        raise RuntimeError('REVIEWED_HEAD_REQUIRED:'+BASE+';actual='+head)
    if git('diff','--cached','--name-only') or set(git('diff','--name-only','HEAD').splitlines()) - {TARGET}:
        raise RuntimeError('UNRELATED_TRACKED_OR_STAGED_CHANGES')
    for path,pin in PINS.items():
        if git('rev-parse','HEAD:'+path) != pin:
            raise RuntimeError('COMMITTED_DEPENDENCY_CHANGED:'+path)
        if path != TARGET and not matches_blob((ROOT/path).read_bytes(),pin):
            raise RuntimeError('WORKTREE_DEPENDENCY_CHANGED:'+path)
    baseline = subprocess.check_output(['git','show',BASE+':'+TARGET],cwd=ROOT)
    if not matches_blob(baseline,PINS[TARGET]):
        raise RuntimeError('BASE_BLOB_CHANGED')
    source = normalize(baseline)
    updated = proposed_source(source)
    raw = (ROOT/TARGET).read_bytes()
    if normalize(raw) not in (source,updated):
        raise RuntimeError('UNREVIEWED_RENDERER_CHANGE')
    rest = raw.replace(b'\r\n',b'')
    if b'\r' in rest or (b'\r\n' in raw and b'\n' in rest):
        raise RuntimeError('UNSUPPORTED_MIXED_EOL')
    eol = '\r\n' if b'\r\n' in raw else '\n'
    encoding = 'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
    return head, raw, updated.replace('\n',eol).encode(encoding), updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    head, raw, updated, source = preflight()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    folder.mkdir(parents=True,exist_ok=True)
    review = folder/'MODEL_RENDERER_FULL.py.txt'
    review.write_text(source,encoding='utf-8')
    if not args.dry_run:
        if (ROOT/TARGET).read_bytes() != raw:
            raise RuntimeError('WORKTREE_CHANGED_DURING_INSTALL')
        if raw != updated:
            (folder/'model_renderer.before').write_bytes(raw)
            (ROOT/TARGET).write_bytes(updated)
        if (ROOT/TARGET).read_bytes() != updated:
            raise RuntimeError('INSTALL_BYTE_MISMATCH')
    print('PHASE177_R17R5_HEAD='+head)
    print('PHASE177_R17R5_FULL_CODE='+str(review))
    print('PHASE177_R17R5_GATE='+('PASS_R17R5_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R17R5_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
