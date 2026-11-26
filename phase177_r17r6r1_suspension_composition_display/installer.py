"""Install only the complete-narrative compression and its regression expectation."""
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
BASE = '0c4cca439910f7e2f0c5d99f00519d852dba321e'
TARGET = 'phase168_r3_5_model_renderer.py'
TEST = 'phase177_r17r3_rank_two_quotient_display/tests/test_display.py'
PINS = {
    TARGET:'88ee28d76c00f033f5cedbc533c820795ccfc902',
    TEST:'9d3c1d32cb44fcc9210d2535ca7fbabd583e7278',
    'phase168_r3_3_proof_narrative_model.py':'6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52',
    'phase168_r3_27_typed_statement_projection.py':'fc19a65386b92ce096c3f4c55fc10622b19c3d65',
    'phase169_r10d2_general_family_definition/family_citation.py':'b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8',
    'phase169_r10e5_composite_generator_image/rule.py':'01acace3eb273d47091421a61291ee54b51c369f',
    'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py':'48bae67c01b6a22a21ec2b9e90255c07b4e53696',
    'phase169_r10eq_r1_universal_stable_definition/definition.py':'0c74d121419b6755e947a367d7de465d81193174',
    'phase171_r20r13_eta_sentence_layout/projection.py':'58768a115c7a89cb524a07f5f441178b9fc10154',
    'phase175_r4r3_two_summand_quotient/rule.py':'b854491dff8b42817c5e1fe2771e4f2dc2c16713',
    'phase177_r17r3_rank_two_quotient_display/projection.py':'b7ffda82255b0d3c6e7d37389515b376c902edc0',
    'phase177_r17r4r1_prop25_suspension_elision/projection.py':'1d6dd710fcedd025a385480b22b12aaee46b4215',
    'phase177_r17r4r1_prop25_suspension_elision/tests/test_display.py':'390fed9301c14091415f184f295267996b73c1d1',
    'phase177_r17r4r2_prop25_equality_chain/projection.py':'a5f35b71b053c603f540f9750b3af50101dde3ab',
    'phase177_r17r4r2_prop25_equality_chain/tests/test_display.py':'f8ab82d2d1ad5d40f10c9e271e5c7195616b28a8',
    'phase177_r17r5_duplicate_cited_equality/projection.py':'211e90eb4ba9d799d4e7cb15bef754db19dcff9f',
    'phase177_r17r5_duplicate_cited_equality/tests/test_display.py':'4b039671642bb4748481953311d6167e2020195f',
    'phase177_r17r1_finite_delta_reason_display/tests/test_display.py':'5c145a1a8a04d45384cfe52fbc112aa3c5616941',
}
RENDER_ANCHOR = '        lines = format_complete_proof_sentences(lines, model)\n'
RENDER_INSERT = '''        from phase177_r17r6r1_suspension_composition_display.projection import (
            project_suspension_composition_display,
        )
        lines, _ = project_suspension_composition_display(lines, model, protected_equalities)
'''
TEST_ANCHOR = '    positions = [body.index(s) for s in sentences]\n'
TEST_INSERT = '''    # R17R6R1 transfers the factor-definition citation to the same
    # certified composite image; the other quotient sentences stay intact.
    assert sentences[1].startswith('また, ')
    sentences[1] = '[R8]を用いて, '+sentences[1].removeprefix('また, ')
'''


def replace_inside(source,function,anchor,replacement):
    if source.count(anchor) != 1:
        raise RuntimeError('UNEXPECTED_ANCHOR:'+function)
    tree = ast.parse(source)
    fn, = [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name == function]
    line = source[:source.index(anchor)].count('\n')+1
    if not fn.lineno < line <= fn.end_lineno:
        raise RuntimeError('ANCHOR_OUTSIDE_FUNCTION:'+function)
    result = source.replace(anchor,replacement,1)
    ast.parse(result)
    return result


def proposed_renderer(source):
    return replace_inside(source,'render_model_backed_narrative_markdown',RENDER_ANCHOR,RENDER_ANCHOR+RENDER_INSERT)


def proposed_test(source):
    return replace_inside(source,'test_actual_rank_two_quotient_display',TEST_ANCHOR,TEST_INSERT+TEST_ANCHOR)


def preflight():
    if Path(git('rev-parse','--show-toplevel')).resolve() != ROOT or git('branch','--show-current') != 'develop':
        raise RuntimeError('WRONG_ROOT_OR_BRANCH')
    head = git('rev-parse','HEAD')
    if head != git('rev-parse','origin/develop'):
        raise RuntimeError('LOCAL_REMOTE_HEAD_MISMATCH')
    git('merge-base','--is-ancestor',BASE,head)
    # The immediately preceding read-only audit package may have been committed.
    allowed_prefix = 'phase177_r17r6_suspension_composition_audit/'
    if any(not p.startswith(allowed_prefix) for p in git('diff','--name-only',BASE,head).splitlines()):
        raise RuntimeError('UNREVIEWED_COMMITTED_CHANGES')
    if git('diff','--cached','--name-only') or set(git('diff','--name-only','HEAD').splitlines()) - {TARGET,TEST}:
        raise RuntimeError('UNRELATED_TRACKED_OR_STAGED_CHANGES')
    changes = {}
    for path,pin in PINS.items():
        if git('rev-parse','HEAD:'+path) != pin:
            raise RuntimeError('COMMITTED_DEPENDENCY_CHANGED:'+path)
        raw = (ROOT/path).read_bytes()
        if path not in (TARGET,TEST):
            if not matches_blob(raw,pin):
                raise RuntimeError('WORKTREE_DEPENDENCY_CHANGED:'+path)
            continue
        baseline = subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
        if not matches_blob(baseline,pin):
            raise RuntimeError('BASE_BLOB_CHANGED:'+path)
        source = normalize(baseline)
        updated = (proposed_renderer if path == TARGET else proposed_test)(source)
        if normalize(raw) not in (source,updated):
            raise RuntimeError('UNREVIEWED_WORKTREE_CHANGE:'+path)
        rest = raw.replace(b'\r\n',b'')
        if b'\r' in rest or (b'\r\n' in raw and b'\n' in rest):
            raise RuntimeError('UNSUPPORTED_MIXED_EOL:'+path)
        eol = '\r\n' if b'\r\n' in raw else '\n'
        encoding = 'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
        changes[path] = (raw,updated.replace('\n',eol).encode(encoding),updated)
    return head,changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    head,changes = preflight()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    folder.mkdir(parents=True,exist_ok=True)
    for path,(raw,updated,source) in changes.items():
        name = 'MODEL_RENDERER_FULL.py.txt' if path == TARGET else 'R17R3_TEST_FULL.py.txt'
        (folder/name).write_text(source,encoding='utf-8')
        if not args.dry_run and raw != updated:
            (folder/(name+'.before')).write_bytes(raw)
    if not args.dry_run:
        for path,(raw,updated,source) in changes.items():
            if (ROOT/path).read_bytes() != raw:
                raise RuntimeError('WORKTREE_CHANGED_DURING_INSTALL:'+path)
        for path,(raw,updated,source) in changes.items():
            if raw != updated:
                (ROOT/path).write_bytes(updated)
            if (ROOT/path).read_bytes() != updated:
                raise RuntimeError('INSTALL_BYTE_MISMATCH:'+path)
    print('PHASE177_R17R6R1_HEAD='+head)
    print('PHASE177_R17R6R1_FULL_CODE='+str(folder))
    print('PHASE177_R17R6R1_GATE='+('PASS_R17R6R1_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R17R6R1_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
