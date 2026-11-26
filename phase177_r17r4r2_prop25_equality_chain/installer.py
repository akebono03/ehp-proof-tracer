"""Install R17R4R2 only on the reviewed develop baseline."""
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
BASE = '954e28b2aba788d7b1e66c8ce1d709458ab3fe3e'
TARGET = 'phase168_r3_5_model_renderer.py'
TEST = 'phase177_r17r4r1_prop25_suspension_elision/tests/test_display.py'
PINS = {
    TARGET: '995d4df7315b19674c64641f7981281f293c178c',
    TEST: 'd7532c99a9b2ca51a4d52011fa646e9d4cc0bdcd',
    'phase177_r17r4r1_prop25_suspension_elision/projection.py': '1d6dd710fcedd025a385480b22b12aaee46b4215',
    'phase177_r10_composition_associativity_isolated/rule.py': '02d361bca9f273d1fe0a955d57a47e5705ab8abc',
    'relation_rules.py': '0da057f35b7ebd51b31c247e04bc4b15b1dcff9e',
    'phase176_r3r55_equality_display_isolated/projection.py': 'f2bedfc04f96f27a771fbdebaa282fd9c2c9a075',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase177_r12_reassociation_transitivity_public/provider.py': 'a6ab33da710c6fd52a0f3ebdee8e31c82399c84a',
    'phase177_r3_unsigned_delta_composition_isolated/rule.py': '485591c14c2b1bbdb5b3486ac3fd5797ec89caf6',
    'phase177_r17r3_rank_two_quotient_display/tests/test_display.py': '9d3c1d32cb44fcc9210d2535ca7fbabd583e7278',
    'phase177_r17r1_finite_delta_reason_display/tests/test_display.py': '5c145a1a8a04d45384cfe52fbc112aa3c5616941',
}
RENDER_ANCHOR = ('        suppressed_body_indices.update(project_prop25_suspension_elision(\n'
                 '            model, order, suppressed_body_indices, protected_equalities,\n'
                 '        ))\n    for index in order:\n')
RENDER_INSERT = ('        from phase177_r17r4r2_prop25_equality_chain.projection import (\n'
                 '            project_prop25_equality_chain,\n'
                 '        )\n'
                 '        hidden, prop25_chain_sentences = project_prop25_equality_chain(\n'
                 '            model, order, suppressed_body_indices, protected_equalities,\n'
                 '        )\n'
                 '        suppressed_body_indices.update(hidden)\n')
INIT_ANCHOR = '    concise_delta_sentences = {}\n'
LINE_ANCHOR = ('        if index in suppressed_body_indices:\n'
               '            continue\n'
               '        if hopf_display is not None and index in (\n')
LINE_INSERT = ('        if index in prop25_chain_sentences:\n'
               '            lines.extend((prop25_chain_sentences[index], ""))\n'
               '            continue\n')
TEST_ANCHOR = '    for step in (prop,prop.premises[1]):\n'
TEST_REPLACEMENT = ('    # R17R4R2 may replace the Prop 2.5 intermediate with its certified\n'
                    '    # transitivity conclusion. The base equality must still be printed.\n'
                    '    from phase177_r17r4r2_prop25_equality_chain.projection import project_prop25_equality_chain\n'
                    '    compressed, sentences = project_prop25_equality_chain(model,order,hidden)\n'
                    '    prop_index, = [i for i,s in enumerate(model.steps) if s is prop]\n'
                    '    visible = (prop,prop.premises[1])\n'
                    '    if prop_index in compressed:\n'
                    '        final_index, = sentences\n'
                    '        visible = (model.steps[final_index],prop.premises[1])\n'
                    '    for step in visible:\n')


def replace_inside(source, function, anchor, replacement):
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
    name = 'render_model_backed_narrative_markdown'
    source = replace_inside(source,name,INIT_ANCHOR,INIT_ANCHOR+'    prop25_chain_sentences = {}\n')
    source = replace_inside(source,name,RENDER_ANCHOR,RENDER_ANCHOR.removesuffix('    for index in order:\n')+RENDER_INSERT+'    for index in order:\n')
    source = replace_inside(source,name,LINE_ANCHOR,LINE_ANCHOR.replace('        if hopf_display',LINE_INSERT+'        if hopf_display',1))
    return source


def proposed_test(source):
    return replace_inside(source,'test_actual_elision',TEST_ANCHOR,TEST_REPLACEMENT)


def preflight():
    if Path(git('rev-parse','--show-toplevel')).resolve() != ROOT or git('branch','--show-current') != 'develop':
        raise RuntimeError('WRONG_ROOT_OR_BRANCH')
    head = git('rev-parse','HEAD')
    if head != BASE or git('rev-parse','origin/develop') != BASE:
        raise RuntimeError('REVIEWED_HEAD_REQUIRED:'+BASE+';actual='+head)
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
    head, changes = preflight()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    folder.mkdir(parents=True,exist_ok=True)
    for path,(raw,updated,source) in changes.items():
        name = 'MODEL_RENDERER_FULL.py.txt' if path == TARGET else 'R17R4R1_TEST_FULL.py.txt'
        review = folder/name
        review.write_text(source,encoding='utf-8')
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
    print('PHASE177_R17R4R2_HEAD='+head)
    print('PHASE177_R17R4R2_FULL_CODE='+str(folder))
    print('PHASE177_R17R4R2_GATE='+('PASS_R17R4R2_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R17R4R2_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
