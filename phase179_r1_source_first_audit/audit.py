"""Phase 179 R1: read-only public proof search and source inventory."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = 'de0c733a18484d866642c170cd341eba35a12b14'
PREFIX = 'PHASE179_R1_'
TARGETS = tuple((n, 7) for n in range(2, 9))
BOUNDARY = (8, 6)
PINS = {
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'stable_rules.py': '1c226f40f658670271a6bcff7076a60515d6eeee',
    'sources/toda/Toda_04_2.tex': '4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'phase165_r52_r9_shared_math.py': '79c3fc2d14080c188ef9284119a6eccb832daac9',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase169_r4b_prop44_injectivity/rule.py': '27c9aa86f180a33a99e2d88ea84939ca8a6dbd4c',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
}
TESTS = (
    'tests/test_phase165_r3_recursive_search.py',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
    'phase178_r27_stable_boundary_source_first_audit/tests/test_audit.py',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'tests/test_phase73_pi14_8_prop44_suspension_isomorphism.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def scope(path, is_stable):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    pairs = {(int(r['n']), int(r['k'])) for r in rows if r['n'] and r['k']
             and int(r['n']) >= 2 and int(r['k']) >= 0}
    targets = tuple(sorted(p for p in pairs if p[1] == 7 and not is_stable(*p)))
    require(targets == TARGETS and BOUNDARY in pairs and is_stable(*BOUNDARY), 'SCOPE_CHANGED')
    return {'targets': targets, 'boundary': BOUNDARY, 'registered_total': len(pairs),
            'stable_count': sum(is_stable(*p) for p in pairs),
            'csv_rows': [{k: r[k] for k in ('n', 'k', 'id', 'orders', 'generator', 'hyouji')}
                         for r in rows if r['n'] and r['k'] and (int(r['n']), int(r['k'])) in TARGETS + (BOUNDARY,)]}


def preflight():
    from phase178_r1_k6_source_first_audit import audit as prior
    from homotopy_groups import TodaPrimaryGroup
    from stable_rules import is_in_toda_stable_range
    gt = prior.git_text
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse', 'HEAD') == gt('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not prior.git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    prior.git('diff', '--check')
    for name, pin in PINS.items():
        require(gt('rev-parse', 'HEAD:' + name) == pin and prior.blob_matches(ROOT / name, pin), 'PIN_CHANGED:' + name)
    require(all((ROOT / p).is_file() for p in TESTS), 'TEST_MISSING')
    result = scope(ROOT / 'data/sphere.csv', lambda n,k: is_in_toda_stable_range(TodaPrimaryGroup(n+k,n)))
    anchors = {'sources/toda/Toda_04_2.tex': ('$n=2,4,8$ のとき, Hopf fibration', r'\begin{proposition}\label{prop:4.4}', r'\begin{lemma}\label{lem:4.5}'),
               'sources/toda/Toda_05_2.tex': (r'\begin{proposition}\label{prop:5.11}', r'\begin{lemma}\label{lemma:5.14}', r'\begin{equation}\label{eq:5.15}', r'\begin{proposition}\label{prop:5.15}')}
    result['source_anchors'] = {}
    for name, keys in anchors.items():
        source = (ROOT / name).read_text(encoding='utf-8-sig')
        require(all(source.count(a) == 1 for a in keys), 'SOURCE_ANCHOR_CHANGED:' + name)
        positions = [source.index(a) for a in keys]
        require(positions == sorted(positions), 'SOURCE_ORDER_CHANGED:' + name)
        result['source_anchors'][name] = {a: source[:p].count('\n') + 1 for a,p in zip(keys, positions)}
    return result


def inventory(bridge, target):
    from proof import ProofRule
    from phase177_r18_final_verified_proof_audit.audit import same_group_claim
    from phase178_r1_k6_source_first_audit.audit import statement
    links = {}
    target_given = []
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        links.setdefault(link.assertion_id, []).append(statement(step.conclusion))
        if same_group_claim(step.conclusion, target):
            target_given.append(link.assertion_id)
    rows = []
    keys = ('proposition4.4', 'lemma4.5', 'proposition5.11', 'lemma5.13', 'lemma5.14', 'proposition5.15', '(5.14)', '(5.15)', '(5.1)', '(4.5)', '(4.8)', 'beforeproposition4.4')
    for a in bridge.registry._assertions.values():
        ref = bridge.registry.reference(a.reference_id)
        locator = str(ref.locator)
        if any(key in locator.lower().replace(' ', '') for key in keys):
            rows.append({'assertion_id': a.assertion_id, 'locator': locator, 'position': ref.publication_position,
                         'origin': a.origin.name, 'given': links.get(a.assertion_id, [])})
    return {'selected': rows, 'target_given': target_given}


def observe(n, k):
    require((n,k) in TARGETS, 'WORKER_OUTSIDE_SCOPE')
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    import phase165_r52_r2_search_adapter as adapter
    import phase165_r52_r3_web_adapter as web_adapter
    import phase168_r3_41p13_trust_boundary as trust
    from phase178_r1_k6_source_first_audit.audit import statement, proof_tree
    from phase177_r18_final_verified_proof_audit.audit import same_group_claim
    from homotopy_groups import TodaPrimaryGroup
    from proof import ProofRule
    from web_group_proof import build_standard_web_group_proof_view
    actual_entry, actual_web, actual_verify = entry.search_group_from_registered_goal, web_adapter.build_partial_web_group_proof_view, trust.verify_proof_tree_for_narrative
    captured, invocations, checks, models, calls = [], [], [], [], []

    def observed_entry(*args, **kwargs):
        result = actual_entry(*args, **kwargs)
        captured.append((result, kwargs.get('bridge')))
        return result

    def wrap(real):
        def observed(*args, **kwargs):
            if (kwargs.get('n'), kwargs.get('k')) != (n,k):
                return real(*args, **kwargs)
            invocations.append(dict(kwargs))
            provider = kwargs['expansion_provider']
            def observed_provider(goal):
                options = provider(goal)
                calls.append({'goal': statement(goal), 'options': [{'rule': o.rule.name, 'subgoals': [statement(g) for g in o.subgoals]} for o in options]})
                return options
            return real(*args, **dict(kwargs, expansion_provider=observed_provider))
        return observed

    def observed_verify(result, bridge, **kwargs):
        counts = actual_verify(result, bridge, **kwargs)
        checks.append((result, counts))
        return counts

    def observed_web(result, **kwargs):
        models.append((result, kwargs.get('narrative_model')))
        return actual_web(result, **kwargs)

    with patch.object(entry, 'search_group_from_registered_goal', observed_entry), \
         patch.object(shared, 'search_registered_partial_proof', wrap(shared.search_registered_partial_proof)), \
         patch.object(adapter, 'search_registered_partial_proof', wrap(adapter.search_registered_partial_proof)), \
         patch.object(trust, 'verify_proof_tree_for_narrative', observed_verify), \
         patch.object(web_adapter, 'build_partial_web_group_proof_view', observed_web):
        view = build_standard_web_group_proof_view(n=n, k=k, max_depth=2, mode='narrative', citation_source='model')
    require(len(captured) == 1 and len(invocations) == 1, 'PUBLIC_SEARCH_CONTEXT_MISSING_OR_AMBIGUOUS')
    result, original = captured[0]
    active = invocations[0]
    require(result.target == TodaPrimaryGroup(n+k,n) and original is not None, 'PUBLIC_TARGET_CHANGED')
    steps = result.proven_steps
    seen, target_given = set(), []
    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        if step.rule is ProofRule.GIVEN and same_group_claim(step.conclusion, result.target):
            target_given.append(statement(step.conclusion))
        for premise in step.premises:
            visit(premise)
    for step in steps:
        visit(step)
    screened = inventory(active['bridge'], result.target)
    status = result.status.value
    verified = len(checks) == 1 and checks[0][0] is result
    roots = [s for s in steps if result.conclusion is not None and s.conclusion == result.conclusion]
    model = models[0][1] if len(models) == 1 and models[0][0] is result else None
    goals = [statement(g) for g in result.open_goals]
    require(not target_given and not screened['target_given'], 'TARGET_GIVEN_PRESENT')
    if status == 'complete':
        require(verified and not goals and len(roots) == 1 and roots[0].rule is ProofRule.INFERENCE and model is not None and view.key == 'generic-complete-proof', 'COMPLETE_NOT_VERIFIED')
    else:
        require(status in ('partial','search_failed','not_searched') and not verified and view.key != 'generic-complete-proof', 'INVALID_OPEN_STATUS')
    return {'n': n, 'k': k, 'status': status, 'web_key': view.key, 'trust_verified': verified,
            'open_goal_count': len(goals), 'target_given_count': len(target_given), 'proven_step_count': len(steps),
            'conclusion': statement(result.conclusion) if result.conclusion is not None else None,
            'frontier': [{'goal': g, 'observed_options': [c for c in calls if c['goal'] == g]} for g in goals],
            'tree': proof_tree(steps), 'provider_calls': calls, 'references': list(result.references),
            'model_citation_count': len(model.citations) if model is not None else None,
            'source_inventory_original': inventory(original, result.target), 'source_inventory_screened': screened,
            'citing_assertion_id': active.get('citing_assertion_id'), 'lookup_mode': active.get('lookup_mode'),
            'diagnostics': list(result.diagnostics), 'rendered_lines': [str(l) for l in view.rendered_lines]}


def run_worker(n, k, folder, timeout):
    path = folder / f'n{n}_k{k}.json'
    command = [sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker', str(n), str(k), '--output', str(path)]
    subprocess.run(command, cwd=ROOT, check=True, timeout=timeout)
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', nargs=2, type=int)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--timeout', type=int, default=180)
    args = parser.parse_args()
    from phase178_r1_k6_source_first_audit import audit as prior
    if args.worker is not None:
        require(args.output is not None, 'OUTPUT_REQUIRED')
        n,k = args.worker
        if (n,k) == BOUNDARY:
            from phase178_r27_stable_boundary_source_first_audit.audit import observe as boundary_observe
            row = boundary_observe()
        else:
            row = observe(n,k)
        prior.store(args.output, row)
        return 0
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R1', 'head': HEAD, 'dry_run': args.dry_run, 'groups': [], 'full_pytest': 'NOT_RUN'}
    try:
        require(args.timeout > 0, 'POSITIVE_TIMEOUT_REQUIRED')
        before = prior.snapshot()
        report['preflight'] = preflight()
        emit('HEAD', HEAD)
        emit('SCOPE', json.dumps(report['preflight'], ensure_ascii=False))
        if args.dry_run:
            report['gate'] = 'PASS_PHASE179_R1_DRYRUN'
        else:
            for n,k in TARGETS + (BOUNDARY,):
                row = run_worker(n,k,folder,args.timeout)
                summary = {key: row.get(key) for key in ('status','web_key','trust_verified','open_goal_count','target_given_count','proven_step_count','model_citation_count')}
                summary.update(n=n,k=k,detail=str(folder / f'n{n}_k{k}.json'))
                report['groups'].append(summary)
                prior.store(folder / 'report.json', report)
                emit('GROUP', json.dumps(summary, ensure_ascii=False))
                for goal in row['frontier']:
                    emit('FRONTIER', json.dumps({'n':n,'k':k,'goal':goal['goal']}, ensure_ascii=False))
                if (n,k) == BOUNDARY:
                    emit('BOUNDARY_ROUTES', json.dumps(row['routes'], ensure_ascii=False))
                    emit('BOUNDARY_SCREENED_SOURCES', json.dumps(row['source_inventory_screened'], ensure_ascii=False))
            command = [sys.executable,'-B','-m','pytest','-q','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command'] = command
            with (folder / 'focused_pytest.txt').open('w', encoding='utf-8') as log:
                proc = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
            print((folder / 'focused_pytest.txt').read_text(encoding='utf-8',errors='replace'), flush=True)
            require(proc.returncode == 0, 'FOCUSED_PYTEST_FAILED')
            report['gate'] = 'PASS_PHASE179_R1_SOURCE_FIRST_AUDIT'
        require(prior.snapshot() == before, 'REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
    except Exception as exc:
        report.update(gate='FAIL_R1', error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    prior.store(folder / 'report.json', report)
    emit('REPORT', folder / 'report.json')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('NEW_RULES', 0)
    emit('NEW_GIVEN', 0)
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
