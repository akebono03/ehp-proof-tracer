"""Phase 177 R1: read-only observation of the public k=5 proof search."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
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
HEAD = '7053e7c8d32ff30d504ea21df4f57cbf56b9a7f3'
DOCUMENTS = ('README.md', 'docs/design.md', 'docs/development_log.md',
             'docs/roadmap.md', 'docs/proof_records.md')
PINS = {
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r52_partial_proof.py': '0af6b459ed5a136a8e30a9e349ccf9fa601d448b',
    'phase165_r52_r9_shared_math.py': '87e0fe1202fa265c7530d0dd7e2b0adda2f5ebc2',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'web_group_proof_common.py': '6d42e2d5d74e009bc4f8c903f0f4014ba6a9c863',
    'phase165_r52_r3_web_adapter.py': 'dda215780c0468cf421592aff86c79b1f5482eed',
}
EXPECTED_PAIRS = tuple((n, 5) for n in range(2, 8))
REGRESSION_PAIRS = ((3, 5), (6, 5), (7, 5))
MARKER = 'PHASE177_R1_WORKER_JSON='
STATUSES = ('complete', 'partial', 'search_failed', 'not_searched')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True,
                                   encoding='utf-8', errors='strict').strip()


def inventory(path):
    groups = {}
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        required = {'n', 'k', 'id', 'orders', 'generator'}
        if not required.issubset(reader.fieldnames or ()):
            raise RuntimeError('CSV_COLUMNS_MISSING')
        for row in reader:
            if row['k'] != '5' or not row['n']:
                continue
            n = int(row['n'])
            if n < 2:
                raise RuntimeError('UNEXPECTED_SPHERE_DIMENSION')
            groups.setdefault((n, 5), []).append({key: row[key] for key in
                                                  ('id', 'orders', 'generator')})
    if not groups:
        raise RuntimeError('NO_K5_GROUPS')
    return dict(sorted(groups.items()))


def snapshot():
    return (git('rev-parse', 'HEAD'), git('diff', '--cached', '--binary'),
            git('diff', '--binary', 'HEAD'), git('status', '--porcelain', '--untracked-files=all'))


def preflight():
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT:
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    if git('rev-parse', 'HEAD') != HEAD or git('rev-parse', 'origin/develop') != HEAD:
        raise RuntimeError('REVIEWED_HEAD_REQUIRED: ' + HEAD)
    if git('status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('TRACKED_WORKTREE_NOT_CLEAN')
    for name, pin in PINS.items():
        if git('rev-parse', 'HEAD:' + name) != pin:
            raise RuntimeError('SOURCE_PIN_CHANGED: ' + name)
    for name in DOCUMENTS:
        if 'PHASE176_FINAL_CLOSEOUT_20261125' not in (ROOT / name).read_text(encoding='utf-8-sig'):
            raise RuntimeError('CLOSEOUT_MARKER_MISSING: ' + name)
    groups = inventory(ROOT / 'data/sphere.csv')
    if tuple(groups) != EXPECTED_PAIRS or sum(map(len, groups.values())) != 7:
        raise RuntimeError('REVIEWED_INVENTORY_CHANGED')
    return groups


def option_record(option):
    rule = getattr(option, 'rule', None)
    return {'rule': getattr(rule, 'name', None) or type(rule).__name__,
            'subgoals': [repr(g) for g in option.subgoals]}


def frontier(goals, calls):
    records = []
    for goal in goals:
        matching = [options for requested, options in calls if type(requested) is type(goal) and requested == goal]
        records.append({'goal': repr(goal), 'type': type(goal).__name__,
                        'provider_calls': len(matching),
                        'candidate_batches': [[option_record(o) for o in options] for options in matching],
                        'classification': ('NOT_REACHED' if not matching else
                                           'NO_CANDIDATES' if not any(matching) else
                                           'CANDIDATES_NOT_PROVED')})
    return records


def observe(n, k):
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    import phase165_r52_r2_search_adapter as search_adapter
    import phase165_r52_r3_web_adapter as web_adapter
    import phase168_r3_41p13_trust_boundary as trust
    from web_group_proof import build_standard_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from proof import ProofRule

    results, calls, invocations, models, verified = [], [], [], [], []
    real_entry = entry.search_group_from_registered_goal
    real_shared = shared.search_registered_partial_proof
    real_search = search_adapter.search_registered_partial_proof
    real_web = web_adapter.build_partial_web_group_proof_view
    real_verify = trust.verify_proof_tree_for_narrative

    def observed_entry(*args, **kwargs):
        result = real_entry(*args, **kwargs)
        results.append(result)
        return result

    def observe_adapter(real):
        def observed(*args, **kwargs):
            if (kwargs.get('n'), kwargs.get('k')) != (n, k):
                return real(*args, **kwargs)
            provider = kwargs.get('expansion_provider')
            invocations.append({'goal': repr(kwargs.get('goal')),
                                'lookup_mode': kwargs.get('lookup_mode'),
                                'citing_assertion_id': kwargs.get('citing_assertion_id')})
            if provider is not None:
                def observed_provider(goal):
                    options = provider(goal)
                    calls.append((goal, options))
                    return options
                kwargs = dict(kwargs, expansion_provider=observed_provider)
            return real(*args, **kwargs)
        return observed

    def observed_web(result, **kwargs):
        models.append((result, kwargs.get('narrative_model')))
        return real_web(result, **kwargs)

    def observed_verify(*args, **kwargs):
        value = real_verify(*args, **kwargs)
        verified.append(args[0] if args else kwargs.get('result'))
        return value

    view, web_error = None, None
    with patch.object(entry, 'search_group_from_registered_goal', observed_entry), \
         patch.object(shared, 'search_registered_partial_proof', observe_adapter(real_shared)), \
         patch.object(search_adapter, 'search_registered_partial_proof', observe_adapter(real_search)), \
         patch.object(web_adapter, 'build_partial_web_group_proof_view', observed_web), \
         patch.object(trust, 'verify_proof_tree_for_narrative', observed_verify):
        try:
            view = build_standard_web_group_proof_view(n=n, k=k, max_depth=2,
                                                       mode='narrative', citation_source='model')
        except Exception:
            web_error = traceback.format_exc()
    if len(results) != 1:
        raise RuntimeError('PUBLIC_SEARCH_RESULT_NOT_OBSERVED: ' + str(web_error))
    result = results[0]
    steps = result.proven_steps
    roots = [s for s in steps if result.conclusion is not None and s.conclusion == result.conclusion]
    complete = result.status is ProofSearchStatus.COMPLETE
    target = (result.conclusion.group if isinstance(result.conclusion, TodaPrimaryGroupZeroStatement)
              else getattr(result.conclusion, 'lhs', None))
    if result.target != TodaPrimaryGroup(n+k, n):
        raise RuntimeError('WRONG_SEARCH_TARGET')
    model = models[0][1] if len(models) == 1 and models[0][0] is result else None
    rules = Counter(s.inference_rule.name for s in steps if s.inference_rule is not None)
    integrity = (not complete or (not result.open_goals and target == result.target and
                                  len(roots) == 1 and roots[0].rule is not ProofRule.GIVEN))
    web_ok = (view is not None and model is not None and
              view.key == ('generic-complete-proof' if complete else 'generic-partial-proof') and
              view.partial_result == (not complete) and
              (not complete or (len(verified) == 1 and verified[0] is result)))
    options_count = Counter(option_record(option)['rule'] for _, options in calls for option in options)
    return {'n': n, 'k': k, 'status': result.status.value,
            'structure_status': result.structure_status.value,
            'abstract_structure_certified': result.abstract_structure is not None,
            'conclusion': repr(result.conclusion) if complete else None,
            'open_goal_count': len(result.open_goals), 'frontier': frontier(result.open_goals, calls),
            'diagnostics': list(result.diagnostics), 'search_references': list(result.references),
            'model_citations': [repr(c) for c in model.citations] if model is not None else [],
            'proven_step_count': len(steps), 'root_step_count': len(roots),
            'accepted_inference_rules': dict(rules),
            'accepted_steps': [{'conclusion': repr(s.conclusion), 'trust': s.rule.name,
                                'inference_rule': s.inference_rule.name if s.inference_rule else None}
                               for s in steps],
            'provider_invocations': invocations, 'provider_call_count': len(calls),
            'observed_candidate_rules': dict(options_count), 'integrity_ok': integrity,
            'web_ok': web_ok, 'web_error': web_error, 'web_key': view.key if view else None,
            'web_conclusion': view.conclusion_latex if view else None,
            'web_rendered_lines': [repr(line) for line in view.rendered_lines] if view else [],
            'verified_complete_tree': complete and len(verified) == 1 and verified[0] is result}


def worker(n, k, timeout, folder):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    try:
        proc = subprocess.run([sys.executable, '-B', '-m', PACKAGE+'.audit', '--worker',
                               '--n', str(n), '--k', str(k)], cwd=ROOT, env=env,
                              capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        (folder / f'n{n}_stdout.txt').write_bytes(exc.stdout or b'')
        (folder / f'n{n}_stderr.txt').write_bytes(exc.stderr or b'')
        return {'n': n, 'k': k, 'status': 'worker_timeout'}
    (folder / f'n{n}_stdout.txt').write_bytes(proc.stdout)
    (folder / f'n{n}_stderr.txt').write_bytes(proc.stderr)
    lines = [line[len(MARKER):] for line in proc.stdout.decode('utf-8', errors='replace').splitlines()
             if line.startswith(MARKER)]
    if proc.returncode or len(lines) != 1:
        return {'n': n, 'k': k, 'status': 'worker_error', 'exit_code': proc.returncode}
    return json.loads(lines[0])


def summarize(rows):
    counts = Counter(row['status'] for row in rows)
    errors = [row['n'] for row in rows if row['status'] not in STATUSES or
              not row.get('integrity_ok') or not row.get('web_ok')]
    by_pair = {(row['n'], row['k']): row for row in rows}
    regressions = [list(pair) for pair in REGRESSION_PAIRS
                   if by_pair.get(pair, {}).get('status') != 'complete' or
                   not by_pair.get(pair, {}).get('verified_complete_tree')]
    pending = [row['n'] for row in rows if row['status'] in ('partial', 'search_failed', 'not_searched')]
    valid = (not errors and not regressions and tuple(by_pair) == EXPECTED_PAIRS and
             len(rows) == len(EXPECTED_PAIRS) and not counts['not_searched'])
    return {'counts': dict(counts), 'errors': errors, 'regressions': regressions,
            'pending_n': pending, 'gate': 'PASS_R1_K5_COMPLETION_STATUS_AUDIT' if valid else 'FAIL_R1_AUDIT',
            'next_target_candidate_n': min(pending) if valid and pending else None,
            'target_selection_policy': 'lowest unresolved n; mathematical source review required before implementation'}


def execute(dry_run, timeout):
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'phase': '177_R1', 'gate': 'FAIL_R1_AUDIT', 'dry_run': dry_run,
              'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'full_pytest': 'NOT_RUN',
              'new_math_rules': 0, 'new_given': 0, 'historical_source_guard': 'FOUR_KNOWN_FAILURES_NOT_PASSING'}
    try:
        groups = preflight()
        before = snapshot()
        report.update(head=HEAD, inventory=[{'n': n, 'k': k, 'db_rows': data}
                                            for (n, k), data in groups.items()])
        if dry_run:
            report['gate'] = 'PASS_R1_READ_ONLY_DRYRUN'
        else:
            rows = []
            for n, k in groups:
                row = worker(n, k, timeout, folder)
                rows.append(row)
                print(f'PHASE177_R1_GROUP=({n},{k}) STATUS={row["status"]} OPEN={row.get("open_goal_count", "UNKNOWN")} WEB={row.get("web_key")}', flush=True)
            report['groups'] = rows
            report.update(summarize(rows))
        if snapshot() != before:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
    except Exception:
        report.update(gate='FAIL_R1_AUDIT', error=traceback.format_exc())
    path = folder / 'report.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key in ('head', 'counts', 'errors', 'regressions', 'pending_n', 'next_target_candidate_n', 'error', 'gate'):
        if key in report:
            print('PHASE177_R1_'+key.upper()+'='+json.dumps(report[key], ensure_ascii=False))
    print('PHASE177_R1_REPORT='+str(path))
    print('PHASE177_R1_FULL_PYTEST=NOT_RUN')
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--n', type=int)
    parser.add_argument('--k', type=int, default=5)
    parser.add_argument('--timeout', type=int, default=180)
    args = parser.parse_args()
    if args.worker:
        print(MARKER + json.dumps(observe(args.n, args.k), ensure_ascii=False))
        return 0
    return execute(args.dry_run, args.timeout)


if __name__ == '__main__':
    raise SystemExit(main())
