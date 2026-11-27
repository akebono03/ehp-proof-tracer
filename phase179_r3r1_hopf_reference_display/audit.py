"""Change only the common Hopf splitting reference sentence; verify the proof is unchanged."""
import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase178_r1_k6_source_first_audit import audit as prior

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = 'ff1d5e6d2419e39b85337fb878d743361124c86a'
TARGET = 'phase168_r3_37c_reference_projection.py'
PINS = {
    TARGET: 'cf58b0379cf67f09ae9b6f959ba610d0718f5819',
    'sources/toda/Toda_04_2.tex': '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7',
    'phase179_r3_hopf_splitting_public/audit.py': '5faddd5a3de627c23562faa6147119efe548096f',
    'phase179_r3_hopf_splitting_public/tests/test_public.py': '89d268d6921d1729716f5f2bf1f924ae8ef37cf8',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py': '7a7bcdfc5cf61b2105b5b4f0d44e1679e6e3ffe9',
}
TESTS = (
    PACKAGE + '/tests/test_display.py',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'phase179_r3_hopf_splitting_public/tests/test_public.py',
)
OLD = r'''                sentence = (
                    r"$n=2,4,8$ では Hopf fibration $h:S^{2n-1}\to S^n$ "
                    r"が存在し, 任意の $i$ で "
                    r"$E+h_*:\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\cong}\pi_i^n$ が成り立つ "
                    r"(Steenrod 1951 を引用)."
                )'''
NEW = r'''                sentence = (
                    r"$n=2,4,8$ のとき,"
                    "\n"
                    r"Hopf fibration $h:S^{2n-1}\to S^n$ が存在し,"
                    "\n"
                    r"$E+h_*:\pi_{i-1}(S^{n-1})\oplus\pi_i(S^{2n-1})"
                    r"\xrightarrow{\cong}\pi_i(S^n)$"
                    "\n"
                    r"は任意の $i$ で同型である (Steenrod 1951 を引用)."
                )'''
FORMULA = r'E+h_*:\pi_{i-1}(S^{n-1})\oplus\pi_i(S^{2n-1})\xrightarrow{\cong}\pi_i(S^n)'


def emit(key, value):
    print('PHASE179_R3R1_' + key + '=' + str(value), flush=True)


def preflight():
    require, gt = prior.require, prior.git_text
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse', 'HEAD') == gt('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not prior.git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for name, pin in PINS.items():
        require(gt('rev-parse', 'HEAD:' + name) == pin and prior.blob_matches(ROOT / name, pin), 'PIN_CHANGED:' + name)
    require(all((ROOT / path).is_file() for path in TESTS), 'TEST_MISSING')
    source = (ROOT / 'sources/toda/Toda_04_2.tex').read_text(encoding='utf-8-sig')
    start = '$n=2,4,8$ のとき, Hopf fibration'
    end = r'\begin{proposition}\label{prop:4.4}'
    require(source.count(start) == source.count(end) == 1, 'SOURCE_BOUNDARY_CHANGED')
    passage = source.split(start, 1)[1].split(end, 1)[0]
    require(r'\pis{i-1}{S^{n-1}}\oplus\pis{i}{S^{2n-1}}' in passage
            and r'\pis{i}{S^n}' in passage, 'SOURCE_SPHERE_NOTATION_CHANGED')
    prior.git('diff', '--check')
    return HEAD


def patched_source(original):
    text = original.decode('utf-8')
    newline = '\r\n' if '\r\n' in text else '\n'
    old, new = OLD.replace('\n', newline), NEW.replace('\n', newline)
    prior.require(text.count(old) == 1 and new not in text, 'REFERENCE_ANCHOR_CHANGED')
    result = text.replace(old, new, 1)
    tree = ast.parse(result)
    fn, = tuple(node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == 'project_reference_bodies')
    full_function = ''.join(result.splitlines(keepends=True)[fn.lineno - 1:fn.end_lineno])
    prior.require(new in full_function, 'PATCH_OUTSIDE_FUNCTION')
    compile(result, TARGET, 'exec')
    return result.encode('utf-8'), full_function


def observe(folder, name):
    path = folder / (name + '.json')
    subprocess.run([sys.executable, '-B', '-m', 'phase178_r27_stable_boundary_source_first_audit.audit',
                    '--worker', str(path)], cwd=ROOT, check=True, timeout=240)
    data = json.loads(path.read_text(encoding='utf-8'))
    prior.require(data['status'] == 'complete' and data['trust_verified']
                  and data['web_key'] == 'generic-complete-proof'
                  and data['open_goal_count'] == data['target_given_count'] == 0,
                  'BOUNDARY_NOT_VERIFIED:' + name)
    prior.require(data['root_ancestor_count'] == 14 and data['model_citation_count'] == 4,
                  'R3_BASELINE_CHANGED:' + name)
    return data


def compare(before, after):
    for key in ('tree', 'conclusion', 'status', 'web_key', 'trust_verified', 'root_ancestor_count',
                'root_given_count', 'target_given_count', 'open_goal_count', 'model_citation_count',
                'model_citations', 'source_inventory_screened', 'source_inventory_original'):
        prior.require(before[key] == after[key], 'PROOF_OR_SOURCE_CHANGED:' + key)
    lines = after['rendered_lines']
    formula_repr = repr(FORMULA)[1:-1]
    matches = [i for i, line in enumerate(lines) if formula_repr in line]
    prior.require(len(matches) == 1, 'SPHERE_NOTATION_MISSING_OR_DUPLICATED')
    i = matches[0]
    prior.require(i >= 2 and i + 1 < len(lines), 'REFERENCE_LAYOUT_INCOMPLETE')
    prior.require('のとき,' in lines[i-2] and 'Hopf fibration' not in lines[i-2]
                  and 'Hopf fibration' in lines[i-1] and 'が存在し,' in lines[i-1]
                  and '同型である' in lines[i+1] and 'Steenrod 1951' in lines[i+1],
                  'REFERENCE_LINE_BREAKS_NOT_PRESERVED')
    prior.require(not any(repr(r'E+h_*:\pi_{i-1}^{n-1}')[1:-1] in line for line in lines),
                  'ABBREVIATED_SOURCE_NOTATION_REMAINS')
    # Other rendered lines, including the proof body, must be exactly unchanged.
    old = before['rendered_lines']
    old_matches = [j for j, line in enumerate(old) if 'Hopf fibration' in line and 'Steenrod 1951' in line]
    prior.require(len(old_matches) == 1, 'R3_REFERENCE_BASELINE_MISSING')
    j = old_matches[0]
    prior.require(old[:j] == lines[:i-2] and old[j+1:] == lines[i+2:], 'OTHER_WEB_LINES_CHANGED')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_PHASE179_R3R1', 'dry_run': args.dry_run,
              'full_pytest': 'NOT_RUN', 'new_given': 0, 'new_rules': 0}
    target = ROOT / TARGET
    original = updated = None
    applied = False
    try:
        head = preflight()
        report['head'] = head
        emit('HEAD', head)
        original = target.read_bytes()
        updated, function = patched_source(original)
        (folder / (TARGET + '.FULL')).write_bytes(updated)
        (folder / 'project_reference_bodies_FULL.py').write_text(function + '\n', encoding='utf-8')
        emit('FULL_FILE', folder / (TARGET + '.FULL'))
        emit('FULL_FUNCTION', folder / 'project_reference_bodies_FULL.py')
        if args.dry_run:
            report['gate'] = 'PASS_PHASE179_R3R1_DRYRUN'
        else:
            before = observe(folder, 'before')
            (folder / (TARGET + '.before')).write_bytes(original)
            target.write_bytes(updated)
            applied = True
            cmd = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '--import-mode=importlib', '-p', 'no:cacheprovider', *TESTS]
            report['focused_command'] = cmd
            subprocess.run(cmd, cwd=ROOT, check=True, timeout=240)
            after = observe(folder, 'after')
            compare(before, after)
            report['proof_unchanged'] = True
            report['web_lines'] = after['rendered_lines']
            for line in after['rendered_lines']:
                emit('WEB_LINE', line)
            prior.require(prior.git_text('rev-parse', 'HEAD') == head, 'HEAD_CHANGED')
            prior.require(prior.git_text('diff', '--name-only', 'HEAD').splitlines() == [TARGET], 'UNEXPECTED_TRACKED_CHANGE')
            prior.require(not prior.git('diff', '--cached', '--binary'), 'INDEX_CHANGED')
            prior.require(target.read_bytes() == updated, 'REFERENCE_FILE_CHANGED_DURING_TEST')
            prior.git('diff', '--check')
            emit('PROOF_TREE_UNCHANGED', 'VERIFIED')
            emit('REFERENCE_SPHERE_NOTATION', 'VERIFIED')
            emit('REFERENCE_LINE_BREAKS', 'VERIFIED')
            report['gate'] = 'PASS_PHASE179_R3R1_REFERENCE_DISPLAY'
    except Exception as exc:
        report.update(gate='FAIL_PHASE179_R3R1', error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
        if applied and target.read_bytes() == updated:
            target.write_bytes(original)
            emit('ROLLBACK', 'REFERENCE_RESTORED')
        elif applied:
            emit('ROLLBACK', 'REFUSED_UNEXPECTED_REFERENCE_CHANGE')
    prior.store(folder / 'report.json', report)
    emit('REPORT', folder / 'report.json')
    emit('NEW_RULES', 0)
    emit('NEW_GIVEN', 0)
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
