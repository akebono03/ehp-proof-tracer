"""Read-only stable-boundary audit; post-search options are not proofs."""
import argparse
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
HEAD = 'd6d6a644842137f8a239deb732b484a574562786'
TESTS = (
    PACKAGE + '/tests/test_audit.py',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'tests/test_phase73_pi14_8_prop44_suspension_isomorphism.py',
)
SELF_FILES = frozenset(PACKAGE + '/' + name for name in (
    '__init__.py', 'audit.py', 'run.ps1', 'tests/test_audit.py',
))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R27_' + key + '=' + str(value), flush=True)


def preflight():
    from phase178_r1_k6_source_first_audit import audit as r1
    gt = r1.git_text
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = gt('rev-parse', 'HEAD')
    require(head == gt('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not r1.git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    r1.git('diff', '--check')
    require(all((ROOT / path).is_file() for path in SELF_FILES | set(TESTS)), 'AUDIT_FILE_MISSING')
    # Check the adopted source text at the reviewed revision, not a paraphrase.
    for path, anchors in (
        ('sources/toda/Toda_04_2.tex', (r'\begin{proposition}\label{prop:4.4}', r'\begin{lemma}\label{lem:4.5}', r'\begin{equation}\label{4.5}', '$n=2,4,8$ のとき, Hopf fibration')),
        ('sources/toda/Toda_05_2.tex', (r'\begin{lemma}\label{lemma:5.14}', r'\begin{equation}\label{eq:5.15}')),
    ):
        pin = gt('rev-parse', head + ':' + path)
        require(r1.blob_matches(ROOT / path, pin), 'SOURCE_BLOB_CHANGED:' + path)
        source = (ROOT / path).read_text(encoding='utf-8-sig')
        require(all(source.count(anchor) == 1 for anchor in anchors), 'SOURCE_ANCHOR_CHANGED:' + path)
    return head


def classify(status, verified, open_count, target_given_count, key, root_matches):
    """An audited open result is not a completed mathematical proof."""
    require(target_given_count == 0, 'TARGET_GIVEN_PRESENT')
    if status == 'complete':
        require(verified and open_count == 0 and key == 'generic-complete-proof'
                and root_matches, 'COMPLETE_NOT_VERIFIED')
        return 'PASS_R27_STABLE_BOUNDARY_VERIFIED_COMPLETE'
    require(status in ('partial', 'search_failed', 'not_searched') and not verified
            and key != 'generic-complete-proof', 'INVALID_OPEN_RESULT')
    return 'PASS_R27_STABLE_BOUNDARY_AUDIT_OPEN'


def source_rows(bridge):
    """Distinguish registry archive entries from linked typed GIVEN steps."""
    from proof import ProofRule
    selected = ('proposition4.4', 'proposition4.2', 'lemma4.5', '(5.1)', '(5.12)',
                '(5.15)', 'lemma5.14', '(4.5)')
    links = {}
    for link in bridge.proof_links:
        if link.step is not None and link.step.rule is ProofRule.GIVEN:
            links.setdefault(link.assertion_id, []).append(link.step)
    rows = []
    for assertion in bridge.registry._assertions.values():
        ref = bridge.registry.reference(assertion.reference_id)
        locator = str(ref.locator)
        compact = locator.lower().replace(' ', '')
        if not any(key in compact for key in selected):
            continue
        rows.append({'assertion_id': assertion.assertion_id, 'locator': locator,
                     'position': ref.publication_position, 'origin': assertion.origin.name,
                     'given_types': [type(step.conclusion).__name__ for step in links.get(assertion.assertion_id, [])]})
    return rows


def observe():
    from phase178_r1_k6_source_first_audit import audit as r1
    from phase178_r22_final_verified_proof_audit.audit import ancestry
    from phase177_r18_final_verified_proof_audit.audit import same_group_claim
    from phase169_r10e4_ordered_db_prior.db_prior import (
        exact_prior_database_result, admitted_prior_group_step, verified_db_step,
    )
    from phase178_r19_finite_cyclic_suspension_transport_isolated.provider import suspension_transport_inputs
    from phase178_r20_suspension_isomorphism_bridge_isolated.rule import RULE_NAME as ISO_RULE
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective, MapIsomorphism
    from phase174_r3_r6_r2_prop44_lemma54.source import TodaPreProp44SplittingStatement, expand_cited_preprop44_splitting
    from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase178_r15_toda512_isolated.source import canonical_512
    from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, FiniteCyclicGroup, TodaDeltaMap
    from toda_rules import TodaDeltaZeroStatement
    from stable_rules import is_in_toda_stable_range, is_freudenthal_boundary_range, SuspensionMapStatement
    from proof import ProofRule
    from web_group_proof import build_standard_web_group_proof_view
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    import phase165_r52_r2_search_adapter as adapter
    import phase165_r52_r3_web_adapter as web_adapter
    import phase168_r3_41p13_trust_boundary as trust

    root = exact_prior_database_result(8, 6)
    lower = exact_prior_database_result(7, 6)
    require(root is not None and lower is not None and root.lhs == TodaPrimaryGroup(14, 8)
            and lower.lhs == TodaPrimaryGroup(13, 7)
            and type(root.rhs) is FiniteCyclicGroup and root.rhs.order == lower.rhs.order == 2,
            'REVIEWED_DB_GOALS_CHANGED')
    transport = suspension_transport_inputs(root, lower)
    require(transport is not None, 'TRANSPORT_INPUTS_MISSING')
    _, typed_iso, image = transport
    e = typed_iso.map
    inj, surj, generic = MapInjective(e), MapSurjective(e), MapIsomorphism(e)
    zero_h = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(14, 15))
    delta = TodaDeltaZeroStatement(TodaDeltaMap(TodaPrimaryGroup(15, 15), lower.lhs))
    factors = component_image_obligations(image)
    require(factors is not None and len(factors) == 2, 'COMPOSITE_FACTORS_MISSING')
    require(is_in_toda_stable_range(root.lhs) and not is_in_toda_stable_range(lower.lhs)
            and is_freudenthal_boundary_range(SuspensionMapStatement(7, 6)), 'BOUNDARY_CONTRACT_CHANGED')
    try:
        canonical_512(7)
    except ValueError:
        pass
    else:
        raise RuntimeError('512_OUTSIDE_SOURCE_RANGE_ACCEPTED')

    results, invocations, models, verified, calls = [], [], [], [], []
    actual_entry = entry.search_group_from_registered_goal
    actual_web = web_adapter.build_partial_web_group_proof_view
    actual_verify = trust.verify_proof_tree_for_narrative

    def capture_entry(*args, **kwargs):
        result = actual_entry(*args, **kwargs)
        results.append((result, kwargs.get('bridge')))
        return result

    def capture_search(real):
        def wrapped(*args, **kwargs):
            if (kwargs.get('n'), kwargs.get('k')) != (8, 6):
                return real(*args, **kwargs)
            invocations.append(dict(kwargs))
            provider = kwargs['expansion_provider']
            def observed_provider(goal):
                options = provider(goal)
                calls.append({'goal': r1.statement(goal), 'options': [
                    {'rule': opt.rule.name, 'subgoals': [r1.statement(g) for g in opt.subgoals]}
                    for opt in options]})
                return options
            return real(*args, **dict(kwargs, expansion_provider=observed_provider))
        return wrapped

    def capture_web(result, **kwargs):
        models.append((result, kwargs.get('narrative_model')))
        return actual_web(result, **kwargs)

    def capture_verify(result, bridge, **kwargs):
        value = actual_verify(result, bridge, **kwargs)
        verified.append(result)
        return value

    with patch.object(entry, 'search_group_from_registered_goal', capture_entry), \
         patch.object(shared, 'search_registered_partial_proof', capture_search(shared.search_registered_partial_proof)), \
         patch.object(adapter, 'search_registered_partial_proof', capture_search(adapter.search_registered_partial_proof)), \
         patch.object(web_adapter, 'build_partial_web_group_proof_view', capture_web), \
         patch.object(trust, 'verify_proof_tree_for_narrative', capture_verify):
        view = build_standard_web_group_proof_view(n=8, k=6, max_depth=2, mode='narrative', citation_source='model')
    require(len(results) == len(models) == 1 and len(invocations) == 1, 'ACTIVE_PUBLIC_SEARCH_CONTEXT_MISSING_OR_AMBIGUOUS')
    result, original = results[0]
    require(result.target == root.lhs and models[0][0] is result and models[0][1] is not None, 'PUBLIC_RESULT_MISMATCH')
    model = models[0][1]
    active = invocations[0]
    require(active['goal'] == root, 'ACTIVE_GOAL_CHANGED')
    bridge, provider = active['bridge'], active['expansion_provider']
    require(original is not None, 'ORIGINAL_BRIDGE_MISSING')
    tree = r1.proof_tree(result.proven_steps)
    nodes = {node['id']: node for node in tree['nodes']}
    direct = [node for node in nodes.values() if node['rule'] == 'GIVEN' and node['conclusion'] == r1.statement(root)]
    # Check actual nested ProofSteps using group-level equality, not just spelling.
    seen, target_given = set(), []
    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        if step.rule is ProofRule.GIVEN and same_group_claim(step.conclusion, root):
            target_given.append(step)
        for premise in step.premises:
            visit(premise)
    for step in result.proven_steps:
        visit(step)
    require(not direct and not target_given, 'TARGET_GIVEN_IN_TREE')
    require(not any(link.step is not None and link.step.rule is ProofRule.GIVEN
                    and same_group_claim(link.step.conclusion, root) for link in bridge.proof_links), 'TARGET_GIVEN_IN_SCREENED_BRIDGE')
    roots = [i for i in tree['observed_steps'] if nodes[i]['conclusion'] == r1.statement(root)]
    root_matches = result.conclusion == root and len(roots) == 1 and nodes[roots[0]]['rule'] == 'INFERENCE'
    scope = ancestry(nodes, roots[0]) if root_matches else set()
    is_verified = len(verified) == 1 and verified[0] is result
    gate = classify(result.status.value, is_verified, len(result.open_goals), len(target_given), view.key, root_matches)
    prior = admitted_prior_group_step(lower.lhs, proof_target=root, bridge=bridge)
    prior_ok = prior is not None and prior.conclusion == lower and verified_db_step(prior, proof_target=root, bridge=bridge)
    available = tuple(link.step.conclusion for link in bridge.proof_links if link.step is not None and link.step.rule is ProofRule.GIVEN)
    prelude = TodaPreProp44SplittingStatement()
    prop44 = TodaProp44UniversalStatement()
    goals = [('ROOT', root), ('PRIOR', lower), ('TYPED_ISO', typed_iso), ('GENERIC_ISO', generic),
             ('E_INJECTIVE', inj), ('E_SURJECTIVE', surj), ('BELOW_DIAGONAL_ZERO', zero_h),
             ('LOWER_DELTA_ZERO', delta), ('COMPOSITE_IMAGE', image), ('FACTOR_1', factors[0]), ('FACTOR_2', factors[1])]
    before = tuple(bridge.proof_links), tuple(bridge.registry._assertions.items())
    probes = []
    for name, goal in goals:
        g = r1.statement(goal)
        options = provider(goal)
        probes.append({'name': name, 'goal': g, 'actual_visits': sum(call['goal'] == g for call in calls),
                       'tree_node_ids': [i for i in nodes if nodes[i]['conclusion'] == g],
                       'root_ancestor_ids': [i for i in sorted(scope) if nodes[i]['conclusion'] == g],
                       'candidates': [{'rule': option.rule.name, 'subgoals': [r1.statement(s) for s in option.subgoals]} for option in options]})
    def candidate(name, rule, subgoals):
        row = next(p for p in probes if p['name'] == name)
        return any(o['rule'] == rule and o['subgoals'] == [r1.statement(g) for g in subgoals] for o in row['candidates'])
    route = {'prior_admitted_verified': bool(prior_ok),
             'transport_candidate': candidate('ROOT', 'finite cyclic presentation transported by proved suspension isomorphism', transport),
             'typed_iso_candidate': candidate('TYPED_ISO', ISO_RULE, (generic,)),
             'generic_iso_candidate': candidate('GENERIC_ISO', 'generic injective and surjective imply isomorphism', (inj, surj)),
             'prelude_link_count': len(linked_cited_steps(bridge, prelude)),
             'prop44_link_count': len(linked_cited_steps(bridge, prop44)),
             'prelude_n8_injection_candidates': len(expand_cited_preprop44_splitting(inj, available)),
             'conditional_prop44_n8_injection_candidates': len(expand_cited_prop44_injectivity(inj, available)),
             '512_n7_refused': True}
    require(before == (tuple(bridge.proof_links), tuple(bridge.registry._assertions.items())), 'PROBE_MUTATED_BRIDGE')
    frontier = []
    for goal in result.open_goals:
        g = r1.statement(goal)
        matching = [call for call in calls if call['goal'] == g]
        frontier.append({'goal': g, 'actual_visits': len(matching), 'observed_options': matching})
    return {'gate': gate, 'status': result.status.value, 'web_key': view.key,
            'trust_verified': is_verified, 'proven_step_count': len(result.proven_steps),
            'root_ancestor_count': len(scope), 'root_given_count': sum(nodes[i]['rule'] == 'GIVEN' for i in scope),
            'target_given_count': len(target_given), 'open_goal_count': len(result.open_goals),
            'raw_search_reference_count': len(result.references), 'model_citation_count': len(model.citations),
            'model_citations': [str(c.reference) for c in model.citations],
            'conclusion': r1.statement(result.conclusion) if result.conclusion is not None else None,
            'diagnostics': list(result.diagnostics), 'routes': route, 'probes': probes,
            'source_inventory_original': source_rows(original), 'source_inventory_screened': source_rows(bridge),
            'search_context': {'lookup_mode': active.get('lookup_mode'), 'citing_assertion_id': active.get('citing_assertion_id')},
            'frontier': frontier, 'tree': tree, 'actual_provider_calls': calls,
            'rendered_lines': [str(line) for line in view.rendered_lines],
            'probe_policy': 'POST_SEARCH_CANDIDATES_ONLY_NOT_PROOFS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', type=Path)
    args = parser.parse_args()
    if args.worker is not None:
        args.worker.write_text(json.dumps(observe(), ensure_ascii=False, indent=2, default=str), encoding='utf-8')
        return 0
    from phase178_r1_k6_source_first_audit import audit as r1
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R27', 'dry_run': args.dry_run}
    try:
        head = preflight()
        before = r1.snapshot()
        emit('HEAD', head)
        if args.dry_run:
            report['gate'] = 'PASS_R27_DRYRUN'
        else:
            path = folder / 'observation.json'
            subprocess.run([sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker', str(path)], cwd=ROOT, check=True, timeout=180)
            data = json.loads(path.read_text(encoding='utf-8'))
            report['observation'] = data
            for key in ('status', 'web_key', 'trust_verified', 'proven_step_count', 'root_ancestor_count', 'root_given_count', 'target_given_count', 'open_goal_count', 'model_citation_count'):
                emit('PUBLIC_' + key.upper(), data[key])
            for key in ('routes', 'source_inventory_original', 'source_inventory_screened', 'search_context'):
                emit(key.upper(), json.dumps(data[key], ensure_ascii=False))
            for item in data['probes']:
                emit('PROBE', json.dumps(item, ensure_ascii=False))
            for item in data['frontier']:
                emit('FRONTIER', json.dumps(item, ensure_ascii=False))
            for line in data['rendered_lines']:
                emit('WEB_LINE', line)
            cmd = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '--import-mode=importlib', '-p', 'no:cacheprovider', *TESTS]
            report['focused_command'] = cmd
            subprocess.run(cmd, cwd=ROOT, check=True)
            report['gate'] = data['gate']
        require(r1.snapshot() == before and preflight() == head, 'AUDIT_CHANGED_REPOSITORY')
    except Exception as exc:
        report.update(gate='FAIL_R27', error=repr(exc), traceback=traceback.format_exc())
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
