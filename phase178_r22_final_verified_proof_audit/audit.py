"""Read-only final proof and display-frontier audit for n=6, k=6."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
BASE = '73a77aedcebabb8b4c6a2ee2edf4df7e9ac8a3aa'
PREVIOUS = 'phase178_r21r1_finite_cyclic_generator_zero_image_public/'
REVIEWED_R22_HEAD = 'dfadbdbdc0cdd31cab708f7336a1b65e4914668f'
R22_COMMITTED_PATHS = frozenset(PACKAGE + '/' + name for name in (
    '__init__.py', 'audit.py', 'run.ps1', 'tests/test_audit.py',
))
R22_FIX_PATHS = frozenset(PACKAGE + '/' + name for name in (
    'audit.py', 'tests/test_audit.py',
))
R22_ORIGINAL_PINS = {
    PACKAGE + '/__init__.py': 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    PACKAGE + '/audit.py': 'e394e66a5f5577683b9f9db5351eaa2e282f4023',
    PACKAGE + '/run.ps1': 'f5bf913bd400dc2693a38fcfb477ec3851d718b5',
    PACKAGE + '/tests/test_audit.py': 'fefc2053fe2a317e3053f52e6fcdcae99286d148',
}
TARGET = 'phase165_r52_r9_shared_math.py'
OLD_TEST = 'phase178_r21_finite_cyclic_generator_zero_image_isolated/tests/test_rule.py'
PINS = {
    TARGET: '726da9783e96b5ecd82e2ca49b786fb488d8a1a7',
    OLD_TEST: 'e2994df8fbfffeb17c0493060ee0b2c89dd417ef',
    'phase178_r21_finite_cyclic_generator_zero_image_isolated/rule.py': '3ff46d65aee3c7ae2fdc3b3ba3f8c68d282d0b8d',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase178_r20r1_suspension_isomorphism_bridge_public/installer.py': 'b6d7f1731dff5610df45c0af56e800c899f2973f',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'phase168_r3_5_model_renderer.py': '1e9896d17ddbfa21c2fca3b86c5a7f7054832c37',
    'phase177_r17r6r1_suspension_composition_display/projection.py': 'dd05a23a458aca832c323fe6320c567734dd4ecb',
    'phase178_r17r3_common_renderer/projection.py': '1e9ae1648f5b8e8d249c91d925934ade88082843',
    'phase178_r17r3_common_renderer/tests/test_display.py': '934fcdec3976b45e7e9570a780a47adca6837cca',
    'phase169_r10e5_composite_generator_image/rule.py': '01acace3eb273d47091421a61291ee54b51c369f',
    'phase169_r10eq_r1_universal_stable_definition/definition.py': '0c74d121419b6755e947a367d7de465d81193174',
    'phase178_r15_toda512_isolated/provider.py': 'b7114fb01a851d0ad9a5a16ee794e4ec603b7d50',
    'phase178_r16_toda513_isolated/source.py': '73300491e27c4d4298e07d8b0bd9c6653328b609',
    'phase178_r20_suspension_isomorphism_bridge_isolated/rule.py': '8d23ba92147c3fd151bd2648725a7fd8241ce4ac',
    'phase165_r12_r24_web_search_connection.py': '71d0c6c365a46e833a2bfe304c771d2e010178ca',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
}
PACKAGE_PINS = {
    PREVIOUS + '__init__.py': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    PREVIOUS + 'installer.py': '2f589281a21b27e8141baa281b9d7001a0c34347c233b7f767c2d693505b095b',
    PREVIOUS + 'run.ps1': '4e53bf1ec1e017da38aa3407fc395fffc52196ea5a24f2fd0655db66f12263ba',
    PREVIOUS + 'tests/test_public.py': '7cc4c1c162744f63758c3112e897e3e710e55b1ff2a1809575cfec7f4aa5a989',
}
TESTS = (
    PACKAGE + '/tests/test_audit.py',
    PREVIOUS + 'tests/test_public.py', OLD_TEST,
    'phase178_r20r1_suspension_isomorphism_bridge_public/tests/test_public.py',
    'phase178_r17r3_common_renderer/tests/test_display.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R22_' + key + '=' + str(value), flush=True)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def normalize(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def digest(raw):
    return hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()


def validate_change_scope(committed, later_committed, dirty):
    """Allow the reviewed R21R1 and R22 additions, not unrelated changes."""
    expected = {TARGET, OLD_TEST} | set(PACKAGE_PINS) | R22_COMMITTED_PATHS
    require(set(committed) == expected,
            'UNRELATED_TRACKED_CHANGES:' + repr(sorted(set(committed) ^ expected)))
    require(set(later_committed) <= R22_FIX_PATHS,
            'UNRELATED_LATER_COMMIT:' + repr(sorted(set(later_committed) - R22_FIX_PATHS)))
    require(set(dirty) <= R22_FIX_PATHS,
            'UNRELATED_WORKTREE_CHANGES:' + repr(sorted(set(dirty) - R22_FIX_PATHS)))


def preflight():
    """Audit reviewed R21R1 content and R22's own committed audit files."""
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = gt('rev-parse', 'HEAD')
    require(head == gt('rev-parse', 'origin/develop'), 'LOCAL_REMOTE_HEAD_MISMATCH')
    require(gt('merge-base', BASE, head) == BASE, 'REVIEWED_BASE_REQUIRED')
    require(not gt('diff', '--cached', '--name-only'), 'STAGED_CHANGES_PRESENT')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    require(gt('merge-base', REVIEWED_R22_HEAD, head) == REVIEWED_R22_HEAD,
            'REVIEWED_R22_HEAD_REQUIRED')
    committed = set(gt('diff', '--name-only', BASE, head).splitlines())
    later_committed = set(gt('diff', '--name-only', REVIEWED_R22_HEAD, head).splitlines())
    dirty = set(gt('diff', '--name-only', 'HEAD').splitlines())
    validate_change_scope(committed, later_committed, dirty)
    for path, pin in R22_ORIGINAL_PINS.items():
        require(gt('rev-parse', REVIEWED_R22_HEAD+':'+path) == pin,
                'R22_REVIEWED_PIN_CHANGED:' + path)
        if path not in R22_FIX_PATHS:
            require(gt('rev-parse', head+':'+path) == pin,
                    'R22_FIXED_FILE_COMMIT_CHANGED:' + path)
            require(normalize((ROOT/path).read_bytes()) == normalize(git('show', head+':'+path)),
                    'R22_FIXED_FILE_WORKTREE_CHANGED:' + path)
    for path, pin in PACKAGE_PINS.items():
        require((ROOT/path).is_file() and digest((ROOT/path).read_bytes()) == pin,
                'R21R1_PACKAGE_CHANGED:' + path)
        if path in committed:
            require(digest(git('show', head+':'+path)) == pin, 'R21R1_COMMITTED_PACKAGE_CHANGED:' + path)
    for path, pin in PINS.items():
        require(gt('rev-parse', BASE+':'+path) == pin, 'BASE_PIN_CHANGED:' + path)
        if path not in (TARGET, OLD_TEST):
            require(gt('rev-parse', head+':'+path) == pin, 'DEPENDENCY_COMMIT_CHANGED:' + path)
            require(normalize((ROOT/path).read_bytes()) == normalize(git('show', BASE+':'+path)),
                    'DEPENDENCY_WORKTREE_CHANGED:' + path)
    from phase178_r21r1_finite_cyclic_generator_zero_image_public import installer
    require(installer.HEAD == BASE, 'R21R1_INSTALLER_BASE_CHANGED')
    for path, writer in ((TARGET, installer.proposed_source), (OLD_TEST, installer.proposed_test)):
        expected = writer(normalize(git('show', BASE+':'+path)))
        require(normalize((ROOT/path).read_bytes()) == expected, 'R21R1_NOT_INSTALLED:' + path)
        if path in committed:
            require(normalize(git('show', head+':'+path)) == expected, 'R21R1_COMMIT_CHANGED:' + path)
    for path in TESTS:
        require((ROOT/path).is_file(), 'FOCUSED_TEST_MISSING:' + path)
    git('diff', '--check')
    return head


def ancestry(nodes, start):
    """Collect the actual transitive premise closure, rejecting invalid graphs."""
    seen, active = set(), set()
    def visit(i):
        require(i in nodes and i not in active, 'INVALID_PROOF_GRAPH')
        if i in seen:
            return
        active.add(i)
        for parent in nodes[i]['premises']:
            visit(parent)
        active.remove(i)
        seen.add(i)
    visit(start)
    return seen


def display_observation(lines, factor_tex, composite_tex, iso_tex):
    """Observe exact rendered math fields; display issues do not invalidate a proof."""
    def count(tex, suffix=None):
        prefix = 'statement_latex=' + repr(tex) + ','
        return sum(prefix in line and (suffix is None or suffix in line) for line in lines)
    return {'factor_line_counts': [count(tex) for tex in factor_tex],
            'composite_line_count': count(composite_tex),
            'isomorphism_line_count': count(iso_tex, 'は同型')}


def inspect_proof(r1, summary, detail):
    """Validate root ancestry and retain the precise renderer frontier for R23."""
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
    require((summary['n'], summary['k']) == (6, 6), 'WRONG_TARGET')
    require(summary['status'] == 'complete' and summary['trust_status'] == 'VERIFIED'
            and summary['open_goal_count'] == 0 and summary['target_given_count'] == 0
            and summary['web_error'] is None and summary['complete_invariants_hold']
            and summary['web_key'] == 'generic-complete-proof', 'N6_NOT_VERIFIED_COMPLETE')
    require(not detail['open_goals'] and detail['screened_source_inventory'] is not None
            and not detail['screened_source_inventory']['target_group_given_links'], 'SCREENED_ROOT_GIVEN_OR_OPEN')
    root, lower = exact_prior_database_result(6,6), exact_prior_database_result(5,6)
    require(root is not None and root.lhs == TodaPrimaryGroup(12,6), 'ROOT_DB_CHANGED')
    require(detail['conclusion'] == r1.statement(root), 'WRONG_ROOT_CONCLUSION')
    transport = suspension_transport_inputs(root, lower)
    require(transport is not None, 'TRANSPORT_INPUTS_MISSING')
    prior, typed_iso, composite = transport
    e = typed_iso.map
    generic, inj, surj = MapIsomorphism(e), MapInjective(e), MapSurjective(e)
    image = canonical_513()[1]
    delta = TodaDeltaZeroStatement(image.map)
    domain = exact_prior_database_result(11,2)
    upper = canonical_512(5)
    nodes = {node['id']:node for node in detail['tree']['nodes']}
    roots = [i for i in detail['tree']['observed_steps'] if nodes[i]['conclusion'] == r1.statement(root)]
    require(len(roots) == 1, 'ROOT_NODE_MISSING_OR_AMBIGUOUS')
    scope = ancestry(nodes, roots[0])
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
                and locator in str(node['literature_reference']), 'GIVEN_PROVENANCE_CHANGED')
    root_node = nodes[roots[0]]
    require(root_node['rule'] == 'INFERENCE' and root_node['inference_rule'] ==
            'finite cyclic presentation transported by proved suspension isomorphism', 'ROOT_RULE_CHANGED')
    lower_node, iso_node, composite_node = children(root_node, transport)
    given(lower_node, 'DB prior: sphere.csv')
    require(iso_node['inference_rule'] == ISO_RULE, 'TYPED_ISO_RULE_CHANGED')
    generic_node, = children(iso_node, (generic,))
    require(generic_node['inference_rule'] == 'generic injective and surjective imply isomorphism', 'GENERIC_ISO_RULE_CHANGED')
    inj_node, surj_node = children(generic_node, (inj,surj))
    delta_node = find(delta, ZERO_RULE, ancestry(nodes,inj_node['id']))
    domain_node, image_node = children(delta_node, (domain,image))
    given(domain_node, 'DB prior: sphere.csv')
    given(image_node, '(5.13)')
    upper_node = find(upper.statement, within=ancestry(nodes,surj_node['id']))
    upper_leaf = find(upper, within=ancestry(nodes,upper_node['id']))
    given(upper_leaf, '(5.12)')
    require(any(nodes[i]['rule'] == 'GIVEN' and nodes[i]['conclusion']['type'] == 'TodaProp42GeneralExactnessStatement'
                for i in scope), 'PROP42_ANCESTRY_MISSING')
    factors = component_image_obligations(composite)
    require(factors is not None and len(factors) == 2, 'COMPOSITE_INPUTS_MISSING')
    require(composite_node['inference_rule'] == 'suspension preserves composition of separately proved maps',
            'COMPOSITE_RULE_CHANGED')
    factor_nodes = children(composite_node, factors)
    branches = [ancestry(nodes, node['id']) for node in factor_nodes]
    users = {node['id']: [i for i in sorted(nodes) if node['id'] in nodes[i]['premises']]
             for node in factor_nodes}
    definition_only = all(node['rule'] == 'INFERENCE' and not node['premises']
                          and node['inference_rule'] == 'stable representative definitional suspension'
                          for node in factor_nodes)
    # Exact known display spellings are diagnostics, not mathematical premises.
    display = display_observation(detail['web']['rendered_lines'],
        (r'E(\nu_{5})=\nu_{6}', r'E(\nu_{8})=\nu_{9}'),
        r'E(\nu_{5}^{2})=\nu_{6}^{2}', r'E: \pi_{11}^{5}\to \pi_{12}^{6}')
    cited = [nodes[i] for i in sorted(scope) if nodes[i]['rule'] == 'GIVEN']
    return {'root_id': roots[0], 'root_ancestor_count': len(scope), 'given_nodes': cited,
            'root_rule': root_node['inference_rule'], 'delta_zero_node': delta_node,
            'upper_delta_node': upper_node, 'generic_iso_node': generic_node, 'typed_iso_node': iso_node,
            'composite_node': composite_node, 'factor_nodes': factor_nodes,
            'factor_ancestor_ids': [sorted(b) for b in branches], 'factor_users': users,
            'definition_only_factors': definition_only, 'display': display}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R22', 'dry_run': args.dry_run, 'full_pytest': 'NOT_RUN'}
    try:
        head = preflight()
        from phase178_r1_k6_source_first_audit import audit as r1
        before = r1.snapshot()
        emit('HEAD', head)
        emit('R21R1_INSTALLED_CONTENT', 'VERIFIED')
        if args.dry_run:
            report['gate'] = 'PASS_R22_DRYRUN'
        else:
            summary = r1.worker(6,6,folder,180)
            report['summary'] = summary
            require('detail' in summary, 'WORKER_FAILED:' + repr(summary))
            detail = json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
            observation = inspect_proof(r1, summary, detail)
            report['proof_audit'] = observation
            for key in ('status','proven_step_count','open_goal_count','trust_status','target_given_count','web_key'):
                emit('ROOT_'+key.upper(), summary[key])
            emit('ROOT_ANCESTOR_COUNT', observation['root_ancestor_count'])
            emit('GIVEN_COUNT', len(observation['given_nodes']))
            emit('DELTA_ZERO_ANCESTRY', 'VERIFIED')
            emit('SUSPENSION_ISOMORPHISM_ANCESTRY', 'VERIFIED')
            emit('COMPOSITE_SUSPENSION_ANCESTRY', 'VERIFIED')
            emit('FACTOR_RULES', json.dumps([n['inference_rule'] for n in observation['factor_nodes']], ensure_ascii=False))
            emit('DEFINITION_ONLY_FACTORS', observation['definition_only_factors'])
            emit('FACTOR_USERS', json.dumps(observation['factor_users'], ensure_ascii=False))
            emit('DISPLAY_OBSERVATION', json.dumps(observation['display'], ensure_ascii=False))
            for node in detail['tree']['nodes']:
                emit('PROOF_NODE', json.dumps(node, ensure_ascii=False))
            command = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command'] = command
            subprocess.run(command,cwd=ROOT,check=True)
            report['gate'] = 'PASS_R22_N6_FINAL_VERIFIED_PROOF_AUDIT'
        require(r1.snapshot() == before, 'REPOSITORY_CHANGED_DURING_AUDIT')
        require(preflight() == head, 'POST_AUDIT_INTEGRITY_FAILED')
    except Exception as exc:
        report.update(gate='FAIL_R22', error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    emit('REPORT', folder/'report.json')
    emit('NEW_MATH_RULES', 0)
    emit('NEW_GIVEN', 0)
    emit('RENDERER_CHANGED', 'NO')
    emit('HISTORICAL_GUARD', 'NOT_RUN_KNOWN_OPEN')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
