"""Read-only Phase 178 R1 audit of registered unstable 6-stem targets."""
from __future__ import annotations

import argparse
import csv
import hashlib
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
HEAD = '15c1efad5003002137243daef6e8771191f63579'
PREFIX = 'PHASE178_R1_'
MARKER = PREFIX + 'WORKER_JSON='
PINS = {
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'stable_rules.py': '1c226f40f658670271a6bcff7076a60515d6eeee',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r52_r9_shared_math.py': 'f4383a0c248fe62903203d1863df345740581c59',
    'phase165_r52_r2_search_adapter.py': 'c1d08b803a4d9f9e4e1ad5180a1487422f1cd191',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'phase165_r52_r3_web_adapter.py': 'dda215780c0468cf421592aff86c79b1f5482eed',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'phase168_r3_41p13_trust_boundary/__init__.py': '5eade56b4c346595d43a8d79ff632d960e602297',
    'tests/test_phase165_r3_recursive_search.py': '708977bb138cec3c45d565d5e81ddc0e4f957a8e',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py': 'bd37cb05011ed0d9413bdd7f7335a116d29dae33',
}
TESTS = ('tests/test_phase165_r3_recursive_search.py',
         'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py')
LOCATORS = ('(5.2)', '(5.3)', '(5.4)', '(5.5)', '(5.6)', '(5.8)', '(5.9)', '(5.10)', '(5.11)', '(5.12)', '(5.13)', '(4.4)', '(4.5)', 'Proposition 2.5', 'Proposition 4.4', 'Proposition 5.6', 'Proposition 5.8', 'Proposition 5.9', 'Proposition 5.11', 'Lemma 5.7', 'Lemma 5.10', 'Proposition 1.4')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def git_text(*args):
    return git(*args).decode('utf-8').strip()


def snapshot():
    return (git('rev-parse', 'HEAD'), git('diff', '--binary', 'HEAD'),
            git('diff', '--cached', '--binary'), git('status', '--porcelain', '--untracked-files=all'))


def blob_matches(path, pin):
    raw = path.read_bytes()
    lf = raw.replace(b'\r\n', b'\n')
    return any(hashlib.sha1(b'blob ' + str(len(x)).encode('ascii') + b'\0' + x).hexdigest() == pin
               for x in (raw, lf, lf.replace(b'\n', b'\r\n')))


def scope(csv_path, is_stable):
    pairs = set()
    records = []
    with csv_path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        require({'n', 'k', 'orders', 'generator'}.issubset(reader.fieldnames or ()), 'CSV_COLUMNS_MISSING')
        for row in reader:
            if not row['n'] or not row['k']:
                continue
            n, k = int(row['n']), int(row['k'])
            if n < 2 or k < 0:
                continue
            pairs.add((n, k))
            if k == 6 and not is_stable(n, k):
                records.append({key: row[key] for key in ('n', 'k', 'id', 'orders', 'generator', 'hyouji')})
    targets = sorted(p for p in pairs if p[1] == 6 and not is_stable(*p))
    require(targets == [(n, 6) for n in range(2, 8)], 'REVIEWED_SCOPE_CHANGED')
    return {'targets': targets, 'csv_rows': records, 'registered_total': len(pairs),
            'stable_excluded': sum(is_stable(*p) for p in pairs),
            'other_unstable_excluded': sum(not is_stable(*p) and p[1] != 6 for p in pairs)}


def preflight():
    require(Path(os.fsdecode(git('rev-parse', '--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(git_text('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(git_text('rev-parse', 'HEAD') == git_text('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:'+HEAD)
    require(not git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    git('diff', '--check')
    for name, pin in PINS.items():
        require(git_text('rev-parse', 'HEAD:'+name) == pin and blob_matches(ROOT/name, pin), 'SOURCE_PIN_CHANGED:'+name)
    from homotopy_groups import TodaPrimaryGroup
    from stable_rules import is_in_toda_stable_range
    result = scope(ROOT/'data/sphere.csv', lambda n,k: is_in_toda_stable_range(TodaPrimaryGroup(n+k,n)))
    require((result['registered_total'], result['stable_excluded'], result['other_unstable_excluded']) == (831,313,512), 'CSV_SCOPE_COUNTS_CHANGED')
    source = (ROOT/'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig')
    anchors = (r'\begin{equation}\label{eq:5.12}', r'\begin{lemma}\label{lemma:5.10}', r'\begin{proposition}\label{prop:5.11}', r'\begin{equation}\label{eq:5.13}')
    require(all(source.count(a) == 1 for a in anchors), 'SOURCE_ANCHOR_MISSING_OR_AMBIGUOUS')
    positions = [source.index(a) for a in anchors]
    require(positions == sorted(positions), 'SOURCE_ORDER_CHANGED')
    result.update(head=HEAD, pins=PINS, source_anchor_lines={a:source[:p].count('\n')+1 for a,p in zip(anchors,positions)})
    return result


def statement(value):
    return {'type': type(value).__name__, 'text': str(value), 'repr': repr(value)}


def proof_tree(steps):
    nodes, seen = [], {}
    def visit(step):
        identity = id(step)
        if identity in seen:
            return seen[identity]
        index = len(nodes)
        seen[identity] = index
        nodes.append(None)
        inference = step.inference_rule
        nodes[index] = {'id': index, 'conclusion': statement(step.conclusion), 'rule': step.rule.name,
                        'inference_rule': inference.name if inference else None,
                        'literature_reference': str(inference.literature_reference) if inference and inference.literature_reference else None,
                        'premises': [visit(p) for p in step.premises]}
        return index
    roots = [visit(s) for s in steps]
    return {'nodes': nodes, 'observed_steps': roots}


def source_inventory(bridge, target):
    from proof import ProofRule
    from phase177_r18_final_verified_proof_audit.audit import same_group_claim
    rows, target_given = [], []
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        ref = bridge.registry.reference(assertion.reference_id)
        locator = str(ref.locator)
        entry = {'assertion_id':link.assertion_id, 'locator':locator, 'position':ref.publication_position,
                 'origin':assertion.origin.name, 'conclusion':statement(step.conclusion), 'premise_count':len(step.premises)}
        normalized = locator.lower().replace(' ', '')
        if any(x.lower().replace(' ', '') == normalized for x in LOCATORS):
            rows.append(entry)
        if same_group_claim(step.conclusion,target):
            target_given.append(entry)
    return {'selected_locator_given_links':rows,'target_group_given_links':target_given}


def observe(n, k, folder):
    require(k == 6 and 2 <= n <= 7, 'WORKER_OUTSIDE_SCOPE')
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    import phase165_r52_r2_search_adapter as adapter
    import phase165_r52_r3_web_adapter as web_adapter
    import phase168_r3_41p13_trust_boundary as trust
    from homotopy_groups import TodaPrimaryGroup
    from phase177_r18_final_verified_proof_audit.audit import same_group_claim
    from proof import ProofRule
    from web_group_proof import build_standard_web_group_proof_view
    actual_entry, actual_web = entry.search_group_from_registered_goal, web_adapter.build_partial_web_group_proof_view
    actual_shared, actual_adapter = shared.search_registered_partial_proof, adapter.search_registered_partial_proof
    actual_verify = trust.verify_proof_tree_for_narrative
    captured, invocations, checks, models = [], [], [], []
    calls = []

    def observed_entry(*args, **kwargs):
        result = actual_entry(*args, **kwargs)
        captured.append((result, kwargs.get('bridge')))
        return result

    def wrap_adapter(real):
        def observed(*args, **kwargs):
            if (kwargs.get('n'), kwargs.get('k')) != (n,k):
                return real(*args, **kwargs)
            invocations.append(dict(kwargs))
            provider = kwargs['expansion_provider']
            def observed_provider(goal):
                options = provider(goal)
                calls.append({'goal': statement(goal), 'options': [{'rule':o.rule.name,'subgoals':[statement(g) for g in o.subgoals]} for o in options]})
                return options
            return real(*args, **dict(kwargs, expansion_provider=observed_provider))
        return observed

    def observed_verify(result, bridge, **kwargs):
        counts = actual_verify(result, bridge, **kwargs)
        checks.append((result, counts, kwargs))
        return counts

    def observed_web(result, **kwargs):
        models.append((result, kwargs.get('narrative_model')))
        return actual_web(result, **kwargs)

    view, web_error = None, None
    with patch.object(entry,'search_group_from_registered_goal',observed_entry), \
         patch.object(shared,'search_registered_partial_proof',wrap_adapter(actual_shared)), \
         patch.object(adapter,'search_registered_partial_proof',wrap_adapter(actual_adapter)), \
         patch.object(trust,'verify_proof_tree_for_narrative',observed_verify), \
         patch.object(web_adapter,'build_partial_web_group_proof_view',observed_web):
        try:
            view = build_standard_web_group_proof_view(n=n,k=k,max_depth=2,mode='narrative',citation_source='model')
        except Exception as exc:
            web_error = repr(exc)
    require(len(captured)==1, 'PUBLIC_SEARCH_CAPTURE_MISSING_OR_AMBIGUOUS:'+str(web_error))
    result, original_bridge = captured[0]
    require(result.target == TodaPrimaryGroup(n+k,n), 'WRONG_RESULT_TARGET')
    require(len(invocations)<=1, 'AMBIGUOUS_SEARCH_CONTEXT')
    steps = result.proven_steps
    tree = proof_tree(steps)
    roots = [s for s in steps if result.conclusion is not None and s.conclusion == result.conclusion]
    target_given = [s for s in steps if s.rule is ProofRule.GIVEN and same_group_claim(s.conclusion,result.target)]
    # All nested leaves are checked separately, not just the flat observed list.
    seen = set()
    def visit(s):
        if id(s) in seen:
            return
        seen.add(id(s))
        if s.rule is ProofRule.GIVEN and same_group_claim(s.conclusion,result.target) and not any(s is x for x in target_given):
            target_given.append(s)
        for p in s.premises:
            visit(p)
    for s in steps:
        visit(s)
    verified = [x for x in checks if x[0] is result]
    status = result.status.value
    complete = status=='complete'
    trust_status = 'VERIFIED' if len(verified)==1 else ('NOT_VERIFIED_COMPLETE' if complete else 'NOT_APPLICABLE_PARTIAL')
    model = models[0][1] if len(models)==1 and models[0][0] is result else None
    consistent = not complete or (len(roots)==1 and not result.open_goals and not target_given and trust_status=='VERIFIED' and view is not None and view.key=='generic-complete-proof' and model is not None)
    invocation = invocations[0] if invocations else None
    open_goals = [statement(g) for g in result.open_goals]
    frontier = []
    for goal in open_goals:
        batches = [c for c in calls if c['goal']==goal]
        frontier.append({'goal':goal,'state':'NOT_REACHED' if not batches else ('CANDIDATES_PRESENT' if any(c['options'] for c in batches) else 'NO_CANDIDATES'), 'observed_expansions':batches})
    detail = {'n':n,'k':k,'status':status,'structure_status':result.structure_status.value,
              'conclusion':statement(result.conclusion) if result.conclusion is not None else None,
              'open_goals':open_goals,'frontier':frontier,'diagnostics':list(result.diagnostics),
              'references':list(result.references),'tree':tree,'provider_calls':calls,
              'search_context':{'lookup_mode':invocation.get('lookup_mode'),'goal':statement(invocation['goal']), 'citing_assertion_id':invocation.get('citing_assertion_id')} if invocation else None,
              'unscreened_source_inventory':source_inventory(original_bridge,result.target) if original_bridge is not None else None,
              'screened_source_inventory':source_inventory(invocation['bridge'],result.target) if invocation else None,
              'web':{'key':view.key,'rendered_lines':[str(x) for x in view.rendered_lines]} if view is not None else None,
              'web_error':web_error,'model':repr(model) if model is not None else None,
              'trust_status':trust_status,'trust_counts':verified[0][1] if len(verified)==1 else None,
              'complete_invariants_hold':consistent,'target_given_count':len(target_given)}
    path = folder/f'n{n}_k{k}.json'
    store(path,detail)
    return {'n':n,'k':k,'status':status,'open_goal_count':len(open_goals),'proven_step_count':len(steps),
            'reference_count':len(result.references),'trust_status':trust_status,'target_given_count':len(target_given),
            'web_key':view.key if view is not None else None,'web_error':web_error,'complete_invariants_hold':consistent,
            'detail':str(path),'detail_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def store(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')


def worker(n,k,folder,timeout):
    try:
        proc = subprocess.run([sys.executable,'-B','-m',PACKAGE+'.audit','--worker',str(n),str(k),'--folder',str(folder)],cwd=ROOT,
                              env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONIOENCODING='utf-8'),capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'n':n,'k':k,'status':'worker_timeout'}
    lines = [s[len(MARKER):] for s in proc.stdout.splitlines() if s.startswith(MARKER)]
    if proc.returncode or len(lines)!=1:
        return {'n':n,'k':k,'status':'worker_error','exit_code':proc.returncode,'stderr':proc.stderr[-10000:],'stdout':proc.stdout[-4000:]}
    row = json.loads(lines[0])
    require((row['n'],row['k'])==(n,k),'WORKER_COORDINATE_CHANGED')
    return row


def execute(dry_run, timeout):
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'phase':'178_R1','dry_run':dry_run,'gate':'FAIL_R1','full_pytest':'NOT_RUN','new_rules':0,'new_given':0,'groups':[]}
    try:
        before = snapshot()
        context = preflight()
        report['preflight'] = context
        emit('HEAD',HEAD)
        emit('TARGETS',context['targets'])
        emit('STABLE_EXCLUDED',context['stable_excluded'])
        emit('OTHER_UNSTABLE_EXCLUDED',context['other_unstable_excluded'])
        if dry_run:
            report['gate'] = 'PASS_R1_READ_ONLY_DRYRUN'
        else:
            for n,k in context['targets']:
                row = worker(n,k,folder,timeout)
                report['groups'].append(row)
                store(folder/'report.json',report)
                emit('GROUP',json.dumps(row,ensure_ascii=False))
            statuses = ('complete','partial','search_failed','not_searched')
            require(all(r['status'] in statuses for r in report['groups']),'UNMEASURED_GROUPS_REQUIRE_REVIEW')
            require(all(r['complete_invariants_hold'] for r in report['groups']),'COMPLETE_TRUST_CONTRACT_FAILED')
            require(all(r['web_error'] is None and r['web_key'] is not None for r in report['groups']),'WEB_GAPS_REQUIRE_REVIEW')
            report['summary'] = {s:sum(r['status']==s for r in report['groups']) for s in statuses}
            report['candidate_targets_in_n_order'] = [[r['n'],r['k']] for r in report['groups'] if r['status']!='complete']
            command = [sys.executable,'-B','-m','pytest','-q','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command'] = command
            with (folder/'focused_pytest.txt').open('w',encoding='utf-8') as log:
                proc = subprocess.run(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),stdout=log,stderr=subprocess.STDOUT)
            report['focused_pytest_exit_code'] = proc.returncode
            print((folder/'focused_pytest.txt').read_text(encoding='utf-8',errors='replace'),flush=True)
            require(proc.returncode==0,'FOCUSED_PYTEST_FAILED')
            report['gate'] = 'PASS_R1_SOURCE_FIRST_AUDIT'
        require(snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
    except BaseException as exc:
        report.update(gate='FAIL_R1',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    store(folder/'report.json',report)
    emit('REPORT',folder/'report.json')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--timeout',type=int,default=180)
    parser.add_argument('--worker',nargs=2,type=int)
    parser.add_argument('--folder',type=Path)
    args = parser.parse_args()
    require(args.timeout>0,'POSITIVE_TIMEOUT_REQUIRED')
    if args.worker is not None:
        require(args.folder is not None and args.folder.is_dir(),'WORKER_FOLDER_REQUIRED')
        print(MARKER+json.dumps(observe(*args.worker,args.folder),ensure_ascii=False),flush=True)
        return 0
    return execute(args.dry_run,args.timeout)


if __name__ == '__main__':
    raise SystemExit(main())
