"""Read-only public n=7, k=6 proof and renderer final audit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase178_r1_k6_source_first_audit import audit as r1
from phase178_r22_final_verified_proof_audit.audit import ancestry, display_observation

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '4f5d4e6e240fef35352f87429c2120288a85f0ad'
TESTS = (
    PACKAGE + '/tests/test_audit.py',
    'phase178_r25_typed_generator_notation_alignment/tests/test_alignment.py',
    'phase178_r21r1_finite_cyclic_generator_zero_image_public/tests/test_public.py',
    'phase178_r23_common_renderer_elision/tests/test_display.py',
    'phase178_r22_final_verified_proof_audit/tests/test_audit.py',
    'phase178_r20r1_suspension_isomorphism_bridge_public/tests/test_public.py',
)
EXPECTED_DISPLAY = {'factor_line_counts': [0, 0], 'composite_line_count': 1,
                    'isomorphism_line_count': 1}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R26_' + key + '=' + str(value), flush=True)


def preflight():
    gt = r1.git_text
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse', 'HEAD') == gt('rev-parse', 'origin/develop') == HEAD,
            'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not r1.git('status', '--porcelain', '--untracked-files=no'),
            'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    r1.git('diff', '--check')
    require(all((ROOT / p).is_file() for p in TESTS), 'FOCUSED_TEST_MISSING')
    return HEAD


def validate_summary(summary):
    require((summary['n'], summary['k']) == (7, 6), 'WRONG_TARGET')
    expected = dict(status='complete', trust_status='VERIFIED', open_goal_count=0,
                    target_given_count=0, web_error=None, complete_invariants_hold=True,
                    web_key='generic-complete-proof', proven_step_count=18)
    require(all(summary.get(key) == value and key in summary for key, value in expected.items()),
            'N7_COMPLETE_CONTRACT_CHANGED:' + repr(summary))
    count = summary.get('reference_count')
    require(type(count) is int and count >= 0, 'INVALID_RAW_REFERENCE_COUNT')


def validate_display(lines):
    result = display_observation(lines,
        (r'E(\nu_{6})=\nu_{7}', r'E(\nu_{9})=\nu_{10}'),
        r'E(\nu_{6}^{2})=\nu_{7}^{2}', r'E: \pi_{12}^{6}\to \pi_{13}^{7}')
    require(result == EXPECTED_DISPLAY, 'N7_RENDERER_CONTRACT_CHANGED:' + repr(result))
    return result


def inspect_proof(summary, detail):
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective, MapIsomorphism
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase178_r15_toda512_isolated.source import canonical_512
    from phase178_r16_toda513_isolated.source import canonical_513
    from phase178_r19_finite_cyclic_suspension_transport_isolated.provider import suspension_transport_inputs
    from phase178_r20_suspension_isomorphism_bridge_isolated.rule import RULE_NAME as ISO_RULE
    from phase178_r21_finite_cyclic_generator_zero_image_isolated.rule import RULE_NAME as ZERO_RULE
    from toda_rules import TodaDeltaZeroStatement

    validate_summary(summary)
    require((detail['n'], detail['k']) == (7, 6) and not detail['open_goals'], 'WRONG_DETAIL_OR_OPEN')
    require(detail['trust_status'] == 'VERIFIED' and detail['complete_invariants_hold']
            and detail['target_given_count'] == 0, 'DETAIL_TRUST_CHANGED')
    require(isinstance(detail['references'], list)
            and len(detail['references']) == summary['reference_count'],
            'RAW_REFERENCE_COUNT_MISMATCH')
    inventory = detail['screened_source_inventory']
    require(inventory is not None and not inventory['target_group_given_links'], 'SCREENED_ROOT_GIVEN_OR_MISSING')
    root, lower = exact_prior_database_result(7, 6), exact_prior_database_result(6, 6)
    require(root is not None and root.lhs == TodaPrimaryGroup(13, 7)
            and root.rhs.order == 2, 'ROOT_PRESENTATION_CHANGED')
    require(lower is not None and lower.lhs == TodaPrimaryGroup(12, 6)
            and lower.rhs.order == 2, 'LOWER_PRESENTATION_CHANGED')
    require(detail['conclusion'] == r1.statement(root), 'WRONG_ROOT_CONCLUSION')
    transport = suspension_transport_inputs(root, lower)
    require(transport is not None, 'TRANSPORT_INPUTS_MISSING')
    prior, typed_iso, composite = transport
    e = typed_iso.map
    generic, inj, surj = MapIsomorphism(e), MapInjective(e), MapSurjective(e)
    image = canonical_513()[2]
    delta = TodaDeltaZeroStatement(image.map)
    domain = exact_prior_database_result(13, 1)
    upper = canonical_512(6)
    rows = detail['tree']['nodes']
    nodes = {node['id']: node for node in rows}
    require(len(rows) == len(nodes), 'DUPLICATE_NODE_IDS')
    observed = detail['tree']['observed_steps']
    roots = [i for i in observed if nodes[i]['conclusion'] == r1.statement(root)]
    require(len(roots) == 1, 'ROOT_NODE_MISSING_OR_AMBIGUOUS')
    scope = ancestry(nodes, roots[0])
    require(len(scope) == 18 and scope == set(nodes) == set(observed), 'ROOT_CLOSURE_CHANGED')

    def find(statement, rule_name=None, within=None):
        ids = scope if within is None else within
        matches = [nodes[i] for i in ids if nodes[i]['conclusion'] == r1.statement(statement)
                   and (rule_name is None or nodes[i]['inference_rule'] == rule_name)]
        require(len(matches) == 1, 'EXPECTED_PROOF_NODE_NOT_UNIQUE:' + repr(statement))
        return matches[0]

    def children(node, statements):
        parents = [nodes[i] for i in node['premises']]
        require([p['conclusion'] for p in parents] == [r1.statement(s) for s in statements],
                'PREMISES_CHANGED:' + str(node['inference_rule']))
        return parents

    def given(node, locator):
        require(node['rule'] == 'GIVEN' and not node['premises']
                and locator in str(node['literature_reference']), 'GIVEN_PROVENANCE_CHANGED:' + locator)

    root_node = nodes[roots[0]]
    require(root_node['rule'] == 'INFERENCE' and root_node['inference_rule'] ==
            'finite cyclic presentation transported by proved suspension isomorphism', 'ROOT_RULE_CHANGED')
    lower_node, iso_node, composite_node = children(root_node, transport)
    given(lower_node, 'DB prior: sphere.csv')
    require(iso_node['inference_rule'] == ISO_RULE, 'TYPED_ISO_RULE_CHANGED')
    generic_node, = children(iso_node, (generic,))
    require(generic_node['inference_rule'] == 'generic injective and surjective imply isomorphism',
            'GENERIC_ISO_RULE_CHANGED')
    inj_node, surj_node = children(generic_node, (inj, surj))
    inj_scope, surj_scope = ancestry(nodes, inj_node['id']), ancestry(nodes, surj_node['id'])
    delta_node = find(delta, ZERO_RULE, inj_scope)
    domain_node, image_node = children(delta_node, (domain, image))
    given(domain_node, 'DB prior: sphere.csv')
    given(image_node, '(5.13)')
    upper_node = find(upper.statement, within=surj_scope)
    upper_leaf = find(upper, within=ancestry(nodes, upper_node['id']))
    given(upper_leaf, '(5.12)')
    exact = [nodes[i] for i in scope if nodes[i]['rule'] == 'GIVEN'
             and nodes[i]['conclusion']['type'] == 'TodaProp42GeneralExactnessStatement']
    require(len(exact) == 1, 'PROP42_ANCESTRY_MISSING_OR_AMBIGUOUS')
    exact_node = exact[0]
    require(not exact_node['premises'] and exact_node['literature_reference']
            and exact_node['id'] in inj_scope and exact_node['id'] in surj_scope,
            'PROP42_NOT_SHARED_BY_BOTH_BRANCHES')
    factors = component_image_obligations(composite)
    require(factors is not None and len(factors) == 2, 'COMPOSITE_INPUTS_MISSING')
    require(composite_node['inference_rule'] == 'suspension preserves composition of separately proved maps',
            'COMPOSITE_RULE_CHANGED')
    factor_nodes = children(composite_node, factors)
    require(all(node['rule'] == 'INFERENCE' and not node['premises'] and
                node['inference_rule'] == 'stable representative definitional suspension'
                for node in factor_nodes), 'FACTOR_DEFINITION_CHANGED')
    given_nodes = [nodes[i] for i in sorted(scope) if nodes[i]['rule'] == 'GIVEN']
    require({n['id'] for n in given_nodes} == {n['id'] for n in
            (lower_node, domain_node, image_node, upper_leaf, exact_node)}, 'GIVEN_SET_CHANGED')
    require(sum(nodes[i]['rule'] == 'INFERENCE' for i in scope) == 13, 'INFERENCE_COUNT_CHANGED')
    require(detail['web']['key'] == 'generic-complete-proof', 'WRONG_WEB_KEY')
    display = validate_display(detail['web']['rendered_lines'])
    return dict(root_id=roots[0], root_ancestor_count=len(scope), given_nodes=given_nodes,
                delta_zero_node=delta_node, upper_delta_node=upper_node,
                exactness_node=exact_node, generic_iso_node=generic_node, typed_iso_node=iso_node,
                composite_node=composite_node, factor_nodes=factor_nodes, display=display)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = dict(gate='FAIL_R26', dry_run=args.dry_run, full_pytest='NOT_RUN')
    try:
        head = preflight()
        before = r1.snapshot()
        emit('HEAD', head)
        if args.dry_run:
            report['gate'] = 'PASS_R26_DRYRUN'
        else:
            summary = r1.worker(7, 6, folder, 180)
            report['summary'] = summary
            require('detail' in summary, 'WORKER_FAILED:' + repr(summary))
            path = Path(summary['detail'])
            raw = path.read_bytes()
            require(hashlib.sha256(raw).hexdigest() == summary['detail_sha256'], 'DETAIL_HASH_CHANGED')
            detail = json.loads(raw.decode('utf-8'))
            observation = inspect_proof(summary, detail)
            report['proof_audit'] = observation
            for key in ('status', 'proven_step_count', 'open_goal_count', 'trust_status',
                        'target_given_count', 'web_key'):
                emit('ROOT_' + key.upper(), summary[key])
            emit('RAW_SEARCH_REFERENCE_COUNT', summary['reference_count'])
            emit('ROOT_ANCESTOR_COUNT', observation['root_ancestor_count'])
            emit('GIVEN_COUNT', len(observation['given_nodes']))
            emit('DELTA_ZERO_ANCESTRY', 'VERIFIED')
            emit('SUSPENSION_ISOMORPHISM_ANCESTRY', 'VERIFIED')
            emit('COMPOSITE_SUSPENSION_ANCESTRY', 'VERIFIED')
            emit('DISPLAY_OBSERVATION', json.dumps(observation['display']))
            for node in detail['tree']['nodes']:
                emit('PROOF_NODE', json.dumps(node, ensure_ascii=False))
            for line in detail['web']['rendered_lines']:
                emit('WEB_LINE', line)
            command = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '--import-mode=importlib',
                       '-p', 'no:cacheprovider', *TESTS]
            report['focused_command'] = command
            subprocess.run(command, cwd=ROOT, check=True)
            report['model_citation_audit'] = 'VERIFIED_BY_FOCUSED_TEST'
            emit('MODEL_CITATION_AUDIT', 'VERIFIED')
            report['gate'] = 'PASS_R26_N7_FINAL_VERIFIED_PROOF_AUDIT'
        require(r1.snapshot() == before, 'REPOSITORY_CHANGED_DURING_AUDIT')
        require(preflight() == head, 'POST_AUDIT_INTEGRITY_FAILED')
    except Exception as exc:
        report.update(gate='FAIL_R26', error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
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
