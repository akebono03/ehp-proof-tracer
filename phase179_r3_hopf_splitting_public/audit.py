"""Apply one reviewed Provider connection, verify it, and audit the real Web proof."""
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
BASE = 'b3effb14bd9645760262fa7f853125ddba4d746c'
TARGET = 'phase165_r52_r9_shared_math.py'
R2 = 'phase179_r2_hopf_splitting_injectivity_isolated/'
R2_PINS = {
    R2 + '__init__.py': 'b98cd43c357ac98ef3da678545bcce488e1c747a',
    R2 + 'audit.py': 'd20053e0a60e904e9b1917e3b38585095cdda779',
    R2 + 'rule.py': '0a2e085ddbfbba182791719f608ad12eada2351b',
    R2 + 'run.ps1': '8991abd83637182f91909d2e42d26b592129a333',
    R2 + 'tests/test_rule.py': '12e0d47565e929170676ebbe36abdfa422d7627b',
}
PINS = {
    TARGET: '79c3fc2d14080c188ef9284119a6eccb832daac9',
    'sources/toda/Toda_04_2.tex': '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7',
    'phase174_r3_r6_r2_prop44_lemma54/source.py': '0f4a020a9f571bbfa17e7d5210e7e7cc192875c2',
    'phase178_r27_stable_boundary_source_first_audit/audit.py': 'f25e20b54115e9a66e23b1d29de6d4e1728272ca',
    'phase178_r22_final_verified_proof_audit/audit.py': '82a7f9a51be9601e137565b8e74212864c0fcac3',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py': '7a7bcdfc5cf61b2105b5b4f0d44e1679e6e3ffe9',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py': 'fb6f340cfec0e9a7f31fa816cb13ca763c5cb277',
}
TESTS = (
    PACKAGE + '/tests/test_public.py',
    R2 + 'tests/test_rule.py::test_cited_split_injection_general',
    R2 + 'tests/test_rule.py::test_wrong_map_or_dimensions_rejected',
    R2 + 'tests/test_rule.py::test_missing_duplicate_and_unlinked_hypotheses_rejected',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py',
    'phase178_r27_stable_boundary_source_first_audit/tests/test_audit.py',
    'tests/test_phase73_pi14_8_prop44_suspension_isomorphism.py',
)
OLD = '        options.extend(expand_cited_preprop44_splitting(goal, tuple(available)))'
NEW = '''        legacy_splitting = expand_cited_preprop44_splitting(goal, tuple(available))
        options.extend(legacy_splitting)
        # Phase 179 R3: reuse the isolated, source-linked general splitting rule.
        # Preserve the legacy n=4 route and its Lemma 5.4 priority.
        if not legacy_splitting:
            from phase179_r2_hopf_splitting_injectivity_isolated.rule import (
                expand_splitting_injectivity,
            )
            options.extend(expand_splitting_injectivity(goal, bridge=bridge))'''
RULE = 'cited Hopf-fibration splitting implies suspension injectivity'


def emit(key, value):
    print('PHASE179_R3_' + key + '=' + str(value), flush=True)


def preflight():
    require, gt = prior.require, prior.git_text
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = gt('rev-parse', 'HEAD')
    require(head == gt('rev-parse', 'origin/develop'), 'HEAD_ORIGIN_MISMATCH')
    require(not prior.git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    require(subprocess.run(['git', 'merge-base', '--is-ancestor', BASE, head], cwd=ROOT).returncode == 0, 'REVIEWED_BASE_NOT_ANCESTOR')
    require(set(gt('diff', '--name-only', BASE, head).splitlines()) == set(R2_PINS), 'COMMIT_ONLY_REVIEWED_R2_FILES_FIRST')
    for path, pin in {**PINS, **R2_PINS}.items():
        require(prior.blob_matches(ROOT / path, pin), 'PIN_CHANGED:' + path)
    require(all((ROOT / path.split('::', 1)[0]).is_file() for path in TESTS), 'TEST_MISSING')
    prior.git('diff', '--check')
    from phase174_r3_r6_r2_prop44_lemma54.source import verify_prelude_source
    require(verify_prelude_source() == 7250, 'SOURCE_POSITION_CHANGED')
    return head


def patched_source(original):
    text = original.decode('utf-8')
    prior.require(text.count(OLD) == 1 and NEW not in text, 'PROVIDER_ANCHOR_CHANGED')
    newline = '\r\n' if '\r\n' in text else '\n'
    result = text.replace(OLD, NEW.replace('\n', newline), 1)
    tree = ast.parse(result)
    fn, = tuple(node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == 'shared_expansion_provider')
    full_function = ''.join(result.splitlines(keepends=True)[fn.lineno - 1:fn.end_lineno])
    prior.require(NEW.replace('\n', newline) in full_function, 'PATCH_OUTSIDE_FUNCTION')
    compile(result, TARGET, 'exec')
    return result.encode('utf-8'), full_function


def observe_boundary(folder):
    path = folder / 'boundary.json'
    subprocess.run([sys.executable, '-B', '-m', 'phase178_r27_stable_boundary_source_first_audit.audit',
                    '--worker', str(path)], cwd=ROOT, check=True, timeout=240)
    data = json.loads(path.read_text(encoding='utf-8'))
    probes = [p for p in data['probes'] if p['name'] == 'E_INJECTIVE']
    prior.require(len(probes) == 1, 'BOUNDARY_INJECTION_PROBE_MISSING')
    candidates = [o for o in probes[0]['candidates'] if o['rule'] == RULE]
    prior.require(len(candidates) == 1, 'PUBLIC_BOUNDARY_CANDIDATE_NOT_UNIQUE')
    prior.require(data['target_given_count'] == 0, 'TARGET_GIVEN_PRESENT')
    used = [node for node in data['tree']['nodes'] if node['rule'] == 'INFERENCE'
            and node['inference_rule'] == RULE and node['conclusion'] == probes[0]['goal']]
    prior.require(data['status'] in ('complete', 'partial', 'search_failed', 'not_searched'), 'UNKNOWN_PROOF_STATUS')
    if data['status'] == 'complete':
        prior.require(data['trust_verified'] and data['open_goal_count'] == 0
                      and data['web_key'] == 'generic-complete-proof', 'COMPLETE_NOT_VERIFIED')
    else:
        prior.require(not data['trust_verified'] and data['web_key'] != 'generic-complete-proof', 'PARTIAL_MISCLASSIFIED')
    return data, len(used)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_PHASE179_R3', 'dry_run': args.dry_run, 'full_pytest': 'NOT_RUN', 'new_given': 0}
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
        (folder / 'shared_expansion_provider_FULL.py').write_text(function + '\n', encoding='utf-8')
        emit('FULL_FILE', folder / (TARGET + '.FULL'))
        emit('FULL_FUNCTION', folder / 'shared_expansion_provider_FULL.py')
        if args.dry_run:
            report['gate'] = 'PASS_PHASE179_R3_DRYRUN'
        else:
            (folder / (TARGET + '.before')).write_bytes(original)
            target.write_bytes(updated)
            applied = True
            cmd = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '--import-mode=importlib', '-p', 'no:cacheprovider', *TESTS]
            report['focused_command'] = cmd
            with (folder / 'focused_pytest.txt').open('w', encoding='utf-8') as log:
                proc = subprocess.run(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=240)
            print((folder / 'focused_pytest.txt').read_text(encoding='utf-8', errors='replace'), flush=True)
            prior.require(proc.returncode == 0, 'FOCUSED_PYTEST_FAILED')
            data, used = observe_boundary(folder)
            report['boundary'] = data
            report['new_rule_observed_steps'] = used
            for key in ('status', 'web_key', 'trust_verified', 'open_goal_count', 'target_given_count',
                        'root_ancestor_count', 'model_citation_count'):
                emit('BOUNDARY_' + key.upper(), data[key])
            emit('BOUNDARY_NEW_RULE_OBSERVED_STEPS', used)
            for item in data['frontier']:
                emit('FRONTIER', json.dumps(item, ensure_ascii=False))
            for line in data['rendered_lines']:
                emit('WEB_LINE', line)
            prior.require(prior.git_text('rev-parse', 'HEAD') == head, 'HEAD_CHANGED')
            prior.require(prior.git_text('diff', '--name-only', 'HEAD').splitlines() == [TARGET], 'UNEXPECTED_TRACKED_CHANGE')
            prior.require(not prior.git('diff', '--cached', '--binary'), 'INDEX_CHANGED')
            prior.require(target.read_bytes() == updated, 'PROVIDER_CHANGED_DURING_TEST')
            prior.git('diff', '--check')
            report['gate'] = ('PASS_PHASE179_R3_PUBLIC_CONNECTED_VERIFIED_COMPLETE' if data['status'] == 'complete'
                              else 'PASS_PHASE179_R3_PUBLIC_CONNECTED_ROOT_OPEN')
    except Exception as exc:
        report.update(gate='FAIL_PHASE179_R3', error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
        if applied and target.read_bytes() == updated:
            target.write_bytes(original)
            emit('ROLLBACK', 'PROVIDER_RESTORED')
        elif applied:
            emit('ROLLBACK', 'REFUSED_UNEXPECTED_PROVIDER_CHANGE')
    prior.store(folder / 'report.json', report)
    emit('REPORT', folder / 'report.json')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('NEW_GIVEN', 0)
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
