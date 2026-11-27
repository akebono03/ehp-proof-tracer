"""Read-only regression audit of the original Phase 178 six-group scope."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '33dd6758432779c3b6ee98c7e214674632bdc8cd'
TARGETS = tuple((n, 6) for n in range(2, 8))
TESTS = (
    PACKAGE + '/tests/test_audit.py',
    'phase178_r13_final_verified_proof_audit/tests/test_audit.py',
    'phase178_r12r2_zero_composition_elision/tests/test_projection.py',
    'phase178_r17r3_common_renderer/tests/test_display.py',
    'phase178_r23_common_renderer_elision/tests/test_display.py',
    'phase178_r26_n7_final_verified_proof_audit/tests/test_audit.py',
    'phase178_r27_stable_boundary_source_first_audit/tests/test_audit.py',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R29_' + key + '=' + str(value), flush=True)


def validate_summary(n, summary):
    require((n, 6) in TARGETS and (summary['n'], summary['k']) == (n, 6), 'WRONG_SCOPE')
    expected = dict(status='complete', trust_status='VERIFIED', open_goal_count=0,
                    target_given_count=0, web_error=None, complete_invariants_hold=True,
                    web_key='generic-complete-proof')
    require(all(key in summary and summary[key] == value for key, value in expected.items()),
            'PUBLIC_PROOF_REGRESSION:' + repr(summary))
    for key, minimum in (('proven_step_count', 1), ('reference_count', 0)):
        require(type(summary.get(key)) is int and summary[key] >= minimum, 'INVALID_COUNT:' + key)


def validate_citations(scope, givens, numbers, citations, headings):
    """Check citation scope and both directions of model associations."""
    require(bool(citations), 'NO_MODEL_CITATIONS')
    expected = list(range(1, len(citations) + 1))
    require([c['number'] for c in citations] == expected and headings == expected,
            'CITATION_HEADING_MISMATCH')
    require(all(type(i) is int and 0 <= i < len(numbers) for i in scope), 'INVALID_SCOPE')
    require(set(givens) <= set(scope), 'GIVEN_OUTSIDE_SCOPE')
    cited = set()
    for c in citations:
        indices = set(c['step_indices'])
        require(bool(c['locator']) and bool(indices) and indices <= set(scope), 'CITATION_OUTSIDE_ROOT')
        require(indices == {i for i, ns in enumerate(numbers) if c['number'] in ns}, 'CITATION_BINDING_MISMATCH')
        cited.update(indices)
    require(all(set(ns) <= set(expected) and len(ns) == len(set(ns)) for ns in numbers), 'UNKNOWN_CITATION_NUMBER')
    require(set(givens) <= cited, 'UNCITED_ROOT_GIVEN')


def validate_boundary(data):
    require(data['gate'] == 'PASS_R27_STABLE_BOUNDARY_AUDIT_OPEN'
            and data['status'] == 'partial' and data['web_key'] == 'generic-partial-proof'
            and data['trust_verified'] is False and data['target_given_count'] == 0
            and data['open_goal_count'] > 0, 'STABLE_BOUNDARY_CHANGED_REQUIRES_REVIEW')


def preflight():
    from phase178_r1_k6_source_first_audit import audit as r1
    from homotopy_groups import TodaPrimaryGroup
    from stable_rules import is_in_toda_stable_range
    gt = r1.git_text
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse', 'HEAD') == gt('rev-parse', 'origin/develop') == HEAD,
            'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not r1.git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    r1.git('diff', '--check')
    require(all((ROOT / p).is_file() for p in TESTS), 'FOCUSED_TEST_MISSING')
    data = r1.scope(ROOT / 'data/sphere.csv', lambda n,k: is_in_toda_stable_range(TodaPrimaryGroup(n+k,n)))
    require(tuple(map(tuple, data['targets'])) == TARGETS, 'REGISTERED_SCOPE_CHANGED')
    require(is_in_toda_stable_range(TodaPrimaryGroup(14,8)), 'STABLE_BOUNDARY_CHANGED')
    return data


def observe(n, folder):
    from phase178_r1_k6_source_first_audit import audit as r1
    from phase178_r22_final_verified_proof_audit.audit import ancestry, display_observation
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase165_r52_partial_proof import ProofSearchStatus
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, FiniteCyclicGroup
    from proof import ProofRule, Relation
    import phase165_r52_r3_web_adapter as adapter
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    captures = []
    real = adapter.build_partial_web_group_proof_view

    def capture(result, **kwargs):
        view = real(result, **kwargs)
        captures.append((result, kwargs.get('narrative_model'), view))
        return view

    # R1 observes the real search and trust gate; the outer wrapper only retains
    # the exact model and view from that same public invocation.
    with patch.object(adapter, 'build_partial_web_group_proof_view', capture):
        summary = r1.observe(n, 6, folder)
    validate_summary(n, summary)
    raw = Path(summary['detail']).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == summary['detail_sha256'], 'DETAIL_HASH_CHANGED')
    detail = json.loads(raw.decode('utf-8'))
    require(len(captures) == 1, 'PUBLIC_MODEL_CAPTURE_MISSING_OR_AMBIGUOUS')
    result, model, view = captures[0]
    require(result.status is ProofSearchStatus.COMPLETE and model is not None
            and model.status is ProofSearchStatus.COMPLETE and not result.open_goals
            and not model.open_goals and view.key == 'generic-complete-proof', 'PUBLIC_MODEL_CONTRACT')
    target = TodaPrimaryGroup(n + 6, n)
    expected = exact_prior_database_result(n, 6)
    require(expected is not None and result.target == target and result.conclusion == expected,
            'TYPED_ROOT_DIFFERS_FROM_REGISTERED_TARGET:' + repr(result.conclusion))
    if n == 3:
        require(type(expected) is TodaPrimaryGroupZeroStatement and expected.group == target, 'EXPECTED_ZERO_CHANGED')
    else:
        require(type(expected) is Relation and expected.lhs == target
                and type(expected.rhs) is FiniteCyclicGroup
                and expected.rhs.order == (8 if n == 4 else 2), 'EXPECTED_CYCLIC_ORDER_CHANGED')
    require(detail['conclusion'] == r1.statement(expected) and not detail['open_goals']
            and detail['trust_status'] == 'VERIFIED' and detail['target_given_count'] == 0
            and len(detail['references']) == summary['reference_count'], 'DETAIL_CONTRACT')
    inventory = detail['screened_source_inventory']
    require(inventory is not None and not inventory['target_group_given_links'], 'SCREENED_TARGET_GIVEN_OR_MISSING')
    nodes = {node['id']: node for node in detail['tree']['nodes']}
    require(len(nodes) == len(detail['tree']['nodes']), 'DUPLICATE_TREE_NODE')
    roots = [i for i in detail['tree']['observed_steps'] if nodes[i]['conclusion'] == r1.statement(expected)]
    require(len(roots) == 1 and nodes[roots[0]]['rule'] == 'INFERENCE', 'ROOT_NOT_INFERRED')
    tree_scope = ancestry(nodes, roots[0])
    require(all(nodes[i]['rule'] in ('GIVEN', 'INFERENCE') for i in tree_scope), 'UNKNOWN_ROOT_STEP_KIND')
    require(all(not nodes[i]['premises'] for i in tree_scope if nodes[i]['rule'] == 'GIVEN'), 'GIVEN_HAS_PREMISES')
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    require(model.steps[model.root_index].conclusion == expected
            and model.steps[model.root_index].rule is ProofRule.INFERENCE
            and len(scope) == len(tree_scope), 'MODEL_TREE_ROOT_MISMATCH')
    givens = {i for i in scope if model.steps[i].rule is ProofRule.GIVEN}
    require(len(givens) == sum(nodes[i]['rule'] == 'GIVEN' for i in tree_scope), 'GIVEN_COUNT_MISMATCH')
    citations = [dict(number=c.number, locator=c.reference.locator or c.reference.label,
                      step_indices=list(c.step_indices), assertion_ids=list(c.assertion_ids),
                      reference_ids=list(c.reference_ids)) for c in model.citations]
    headings = []
    for line in view.rendered_lines:
        m = re.match(r'^\*\*\[R(\d+)\] ', line.prefix)
        if m:
            headings.append(int(m.group(1)))
    require(len(model.step_citation_numbers) == len(model.steps), 'MODEL_CITATION_LENGTH')
    validate_citations(scope, givens, model.step_citation_numbers, citations, headings)
    markdown = render_model_backed_narrative_markdown(result, model)
    require(markdown.rstrip().endswith('□'), 'MISSING_PROOF_END')
    if n == 3:
        from phase178_r13_final_verified_proof_audit.audit import check_narrative
        check_narrative(markdown)
    if n in (6,7):
        if n == 6:
            observed = display_observation(detail['web']['rendered_lines'],
                (r'E(\nu_{5})=\nu_{6}', r'E(\nu_{8})=\nu_{9}'),
                r'E(\nu_{5}^{2})=\nu_{6}^{2}', r'E: \pi_{11}^{5}\to \pi_{12}^{6}')
            require(observed == {'factor_line_counts':[0,0], 'composite_line_count':1, 'isomorphism_line_count':1}, 'N6_DISPLAY_REGRESSION')
        else:
            from phase178_r26_n7_final_verified_proof_audit.audit import inspect_proof
            inspect_proof(summary, detail)
    (folder / f'n{n}_narrative.md').write_text(markdown, encoding='utf-8')
    return dict(summary=summary, conclusion=r1.statement(expected), root_ancestor_count=len(tree_scope),
                given_count=len(givens), inference_count=len(tree_scope)-len(givens),
                model_citation_count=len(citations), model_citations=citations, citation_headings=headings,
                root_inference_rule=nodes[roots[0]]['inference_rule'], citation_audit='VERIFIED')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', type=int)
    parser.add_argument('--folder', type=Path)
    parser.add_argument('--timeout', type=int, default=180)
    args = parser.parse_args()
    if args.worker is not None:
        require(args.folder is not None and args.folder.is_dir() and (args.worker, 6) in TARGETS, 'INVALID_WORKER')
        data = observe(args.worker, args.folder)
        (args.folder / f'n{args.worker}_audit.json').write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
        return 0
    from phase178_r1_k6_source_first_audit import audit as r1
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = dict(gate='FAIL_R29', dry_run=args.dry_run, groups=[], full_pytest='NOT_RUN')
    try:
        require(args.timeout > 0, 'INVALID_TIMEOUT')
        report['scope'] = preflight()
        before = r1.snapshot()
        emit('HEAD', HEAD)
        emit('ACTIVE_SCOPE', json.dumps(TARGETS))
        if args.dry_run:
            report['gate'] = 'PASS_R29_DRYRUN'
        else:
            for n, _ in TARGETS:
                cmd = [sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker', str(n), '--folder', str(folder)]
                subprocess.run(cmd, cwd=ROOT, check=True, timeout=args.timeout)
                row = json.loads((folder / f'n{n}_audit.json').read_text(encoding='utf-8'))
                validate_summary(n, row['summary'])
                report['groups'].append(row)
                emit('GROUP', json.dumps(dict(n=n,k=6,status=row['summary']['status'],
                    trust_status=row['summary']['trust_status'], steps=row['summary']['proven_step_count'],
                    ancestors=row['root_ancestor_count'], given=row['given_count'], inference=row['inference_count'],
                    raw_references=row['summary']['reference_count'], citations=row['model_citation_count'],
                    open_goals=row['summary']['open_goal_count'], target_given=row['summary']['target_given_count'],
                    web_key=row['summary']['web_key']), ensure_ascii=False))
            boundary_path = folder / 'stable_boundary.json'
            subprocess.run([sys.executable, '-B', '-m', 'phase178_r27_stable_boundary_source_first_audit.audit',
                '--worker', str(boundary_path)], cwd=ROOT, check=True, timeout=args.timeout)
            boundary = json.loads(boundary_path.read_text(encoding='utf-8'))
            report['stable_boundary'] = boundary
            validate_boundary(boundary)
            emit('STABLE_BOUNDARY', 'DEFERRED_PHASE179_PARTIAL')
            emit('STABLE_BOUNDARY_OPEN_GOALS', boundary['open_goal_count'])
            cmd = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '--import-mode=importlib', '-p', 'no:cacheprovider', *TESTS]
            report['focused_command'] = cmd
            subprocess.run(cmd, cwd=ROOT, check=True)
            require(len(report['groups']) == len(TARGETS), 'INCOMPLETE_SCOPE')
            emit('ACTIVE_COMPLETE', '6/6')
            emit('ACTIVE_OPEN_GOALS', sum(r['summary']['open_goal_count'] for r in report['groups']))
            emit('ACTIVE_TARGET_GIVEN', sum(r['summary']['target_given_count'] for r in report['groups']))
            report['gate'] = 'PASS_R29_FINAL_6STEM_AUDIT'
        require(r1.snapshot() == before and preflight() == report['scope'], 'REPOSITORY_CHANGED_DURING_AUDIT')
    except Exception as exc:
        report.update(gate='FAIL_R29', error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    r1.store(folder / 'report.json', report)
    emit('REPORT', folder / 'report.json')
    emit('NEW_MATH_RULES', 0)
    emit('NEW_GIVEN', 0)
    emit('PROVIDER_CHANGED', 'NO')
    emit('RENDERER_CHANGED', 'NO')
    emit('HISTORICAL_GUARD', 'NOT_RUN_KNOWN_OPEN')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
