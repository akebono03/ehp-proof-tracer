"""Apply a display-only extension to the existing common narrative projections."""
import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
BASE = 'c14b7a9af6f2dc356a48dda172b4cf496b84c7a5'
MATCHER = 'phase177_r17r6r1_suspension_composition_display/projection.py'
COMMON = 'phase178_r17r3_common_renderer/projection.py'
RENDERER = 'phase168_r3_5_model_renderer.py'
PINS = {
    MATCHER: 'dd05a23a458aca832c323fe6320c567734dd4ecb',
    COMMON: '1e9ae1648f5b8e8d249c91d925934ade88082843',
    RENDERER: '1e9896d17ddbfa21c2fca3b86c5a7f7054832c37',
    'phase168_r3_27_typed_statement_projection.py': '1a9793d74c9c2ecbe311e6d1bed95e3920e5b123',
    'phase177_r17r4r1_prop25_suspension_elision/projection.py': '1d6dd710fcedd025a385480b22b12aaee46b4215',
    'phase178_r20_suspension_isomorphism_bridge_isolated/rule.py': '8d23ba92147c3fd151bd2648725a7fd8241ce4ac',
    'phase178_r22_final_verified_proof_audit/audit.py': '82a7f9a51be9601e137565b8e74212864c0fcac3',
    'phase178_r22_final_verified_proof_audit/tests/test_audit.py': '8a4b67a146728485a5d3eabe67955ec72e65a6fa',
    'phase177_r17r6r1_suspension_composition_display/tests/test_display.py': 'aff28b4aab345e41001e338cf7cf0e808cffb4c5',
    'phase178_r17r3_common_renderer/tests/test_display.py': '934fcdec3976b45e7e9570a780a47adca6837cca',
    'phase165_r52_r9_shared_math.py': '79c3fc2d14080c188ef9284119a6eccb832daac9',
    'phase169_r10eq_r1_universal_stable_definition/definition.py': '0c74d121419b6755e947a367d7de465d81193174',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
}
TESTS = (
    PACKAGE + '/tests/test_display.py',
    PACKAGE + '/tests/test_installer.py',
    'phase177_r17r6r1_suspension_composition_display/tests/test_display.py',
    'phase178_r17r3_common_renderer/tests/test_display.py',
    'phase178_r22_final_verified_proof_audit/tests/test_audit.py',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py',
)

ISO_PROJECTION = '''

def project_typed_suspension_iso_lines(lines, model, protected=frozenset()):
    """Hide only a redundant typed reading of a displayed, proved isomorphism."""
    context = graph_context(lines, model)
    if context is None:
        return lines
    scope, parents, boundary = context
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase178_r20_suspension_isomorphism_bridge_isolated.rule import (
        RULE_NAME as bridge_name, suspension_isomorphism_inputs,
    )
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    output = list(lines)
    for index in sorted(scope):
        step = model.steps[index]
        if (index == model.root_index or index in protected
                or model.step_citation_numbers[index]
                or step.inference_rule is None or step.inference_rule.name != bridge_name
                or step.inference_rule.literature_reference is not None
                or len(parents[index]) != 1 or not replayed(step)):
            continue
        parent_index, = parents[index]
        parent = model.steps[parent_index]
        if (parent_index not in scope or parent_index in protected
                or suspension_isomorphism_inputs(step.conclusion) != (parent.conclusion,)
                or parent.inference_rule is None
                or parent.inference_rule.name != 'generic injective and surjective imply isomorphism'
                or tuple(p.conclusion for p in parent.premises) != (
                    MapInjective(step.conclusion.map), MapSurjective(step.conclusion.map))
                or not replayed(parent)):
            continue
        bare = typed_sentence(step.conclusion, step)
        reason = typed_sentence(parent.conclusion, parent)
        if not bare or reason != '単射性と全射性より, ' + bare:
            continue
        pos = unique_body_line(output, boundary, bare)
        previous = unique_body_line(output, boundary, reason)
        if (pos is None or previous is None or previous >= pos
                or any(line.strip() for line in output[previous + 1:pos])):
            continue
        if any(j not in (index, parent_index) and
               typed_sentence(model.steps[j].conclusion, model.steps[j]) in (bare, reason)
               for j in scope):
            continue
        del output[pos]
        if pos < len(output) and not output[pos]:
            del output[pos]
    return output
'''


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R23_' + key + '=' + str(value), flush=True)


def replace_once(text, old, new):
    require(text.count(old) == 1, 'MISSING_OR_AMBIGUOUS_ANCHOR:' + old)
    return text.replace(old, new, 1)


def proposed_matcher(text):
    text = replace_once(text, 'def match_composition_branch(model, index):',
                        'def match_composition_branch(model, index, *, allow_definition_only=False):')
    text = replace_once(text, '    if not leaves or len(set(displays)) != len(displays):',
                        '    if (not leaves and not allow_definition_only) or len(set(displays)) != len(displays):')
    ast.parse(text)
    return text


def proposed_common(text):
    text = replace_once(text, '    match = match_composition_branch(model, index)',
                        '    match = match_composition_branch(model, index, allow_definition_only=True)')
    text = replace_once(text, "    tag = ', '.join(f'[R{n}]' for n in refs) + 'より, '\n    replacement = tag + body",
                        "    replacement = (', '.join(f'[R{n}]' for n in refs) + 'より, ' + body\n                   if refs else body)")
    require('def project_typed_suspension_iso_lines(' not in text, 'ALREADY_CONNECTED')
    text = text.rstrip() + ISO_PROJECTION.rstrip('\n') + '\n'
    ast.parse(text)
    return text


def proposed_renderer(text):
    text = replace_once(text, '            project_composite_suspension_lines, project_finite_quotient_order,\n',
                        '            project_composite_suspension_lines, project_finite_quotient_order,\n'
                        '            project_typed_suspension_iso_lines,\n')
    text = replace_once(text, '        lines = project_composite_suspension_lines(lines, model, protected_equalities)\n',
                        '        lines = project_composite_suspension_lines(lines, model, protected_equalities)\n'
                        '        lines = project_typed_suspension_iso_lines(lines, model, protected_equalities)\n')
    ast.parse(text)
    return text


WRITERS = {MATCHER: proposed_matcher, COMMON: proposed_common, RENDERER: proposed_renderer}


def check_git_diff(r1):
    """Preserve the actual Git diagnostic in stdout and the audit report."""
    try:
        r1.git('diff', '--check')
    except subprocess.CalledProcessError as exc:
        messages = []
        for value in (exc.output, exc.stderr):
            if isinstance(value, bytes):
                value = value.decode('utf-8', errors='replace')
            if value:
                messages.append(value.strip())
        diagnostic = '\n'.join(messages) or str(exc)
        emit('DIFF_CHECK_OUTPUT', diagnostic)
        raise RuntimeError('GIT_DIFF_CHECK_FAILED: ' + diagnostic) from exc


def preflight(r1):
    gt = r1.git_text
    require(Path(gt('rev-parse','--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch','--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = gt('rev-parse','HEAD')
    require(head == gt('rev-parse','origin/develop'), 'HEAD_MISMATCH')
    require(gt('merge-base',BASE,head) == BASE, 'REVIEWED_BASE_REQUIRED')
    require(not gt('diff','--cached','--name-only'), 'STAGED_CHANGES_PRESENT')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    allowed = set(WRITERS) | {PACKAGE + '/' + p for p in ('__init__.py','installer.py','run.ps1','tests/test_display.py','tests/test_installer.py')}
    committed = set(gt('diff','--name-only',BASE,head).splitlines())
    dirty = set(gt('diff','--name-only','HEAD').splitlines())
    require(committed | dirty <= allowed, 'UNRELATED_TRACKED_CHANGES:' + repr(sorted((committed | dirty) - allowed)))
    changes = {}
    from phase178_r20r1_suspension_isomorphism_bridge_public.installer import normalized, encode_like
    for path,pin in PINS.items():
        require(gt('rev-parse',BASE+':'+path) == pin, 'BASE_PIN_CHANGED:' + path)
        base = normalized(r1.git('show',BASE+':'+path))
        raw = (ROOT/path).read_bytes()
        if path in WRITERS:
            proposed = WRITERS[path](base)
            require(normalized(raw) in (base,proposed), 'UNREVIEWED_WORKTREE:' + path)
            require(normalized(r1.git('show',head+':'+path)) in (base,proposed), 'UNREVIEWED_COMMIT:' + path)
            changes[path] = (raw,encode_like(proposed,raw),proposed)
        else:
            require(gt('rev-parse',head+':'+path) == pin and r1.blob_matches(ROOT/path,pin), 'DEPENDENCY_CHANGED:' + path)
    for path in TESTS:
        require((ROOT/path).is_file(), 'TEST_MISSING:' + path)
    check_git_diff(r1)
    return head,changes


def export_code(folder, changes):
    for path, (_, _, source) in changes.items():
        (folder/(path.replace('/','__')+'.full.txt')).write_text(source,encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    from phase178_r1_k6_source_first_audit import audit as r1
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'gate':'FAIL_R23','dry_run':args.dry_run}
    written = []
    try:
        head,changes = preflight(r1)
        emit('HEAD',head)
        export_code(folder,changes)
        emit('FULL_CODE',folder)
        if args.dry_run:
            report['gate'] = 'PASS_R23_DRYRUN'
        else:
            for path,(raw,updated,_) in changes.items():
                require((ROOT/path).read_bytes() == raw,'WORKTREE_CHANGED:'+path)
                if raw != updated:
                    written.append((path,raw,updated))
                    (ROOT/path).write_bytes(updated)
            check_git_diff(r1)
            before = r1.snapshot()
            command = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command'] = command
            subprocess.run(command,cwd=ROOT,check=True)
            require(r1.snapshot() == before,'REPOSITORY_CHANGED_DURING_TESTS')
            _,after = preflight(r1)
            require(all(raw == updated for raw,updated,_ in after.values()),'POST_INSTALL_INTEGRITY_FAILED')
            report['gate'] = 'PASS_R23_COMMON_RENDERER_ELISION'
    except Exception as exc:
        for path,raw,updated in reversed(written):
            if (ROOT/path).read_bytes() == updated:
                (ROOT/path).write_bytes(raw)
        report.update(error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    emit('REPORT',folder/'report.json')
    emit('NEW_MATH_RULES',0)
    emit('NEW_GIVEN',0)
    emit('PROVIDER_CHANGED','NO')
    emit('HISTORICAL_GUARD','NOT_RUN_KNOWN_OPEN')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
