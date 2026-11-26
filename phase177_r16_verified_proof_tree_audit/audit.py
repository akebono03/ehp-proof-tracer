"""Read-only audit of the actual completed R15 public proof tree."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob, snapshot
from phase177_r15_finite_cyclic_delta_injective_public.installer import (
    PINS as R15_PINS, proposed_source, normalize,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = 'da3e1b93d853fc9f4ded3b169af565561a1c7a95'
TARGET = 'phase165_r52_r9_shared_math.py'
PACKAGE = Path(__file__).resolve().parent.name
R15 = 'phase177_r15_finite_cyclic_delta_injective_public'
PINS = dict(R15_PINS, **{
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'phase168_r3_3_proof_narrative_model.py': '6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52',
    'phase168_r3_5_model_renderer.py': 'c58c19f7234def48b743491c6a9c045345ac35e6',
    'phase175_r4r3_two_summand_quotient/rule.py': 'b854491dff8b42817c5e1fe2771e4f2dc2c16713',
})
R15_SHA256 = {'__init__.py': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'installer.py': 'bf163c4ea2bed6fed14eaa73c58a1fee1449b7f2fa3b2d63f20ff26237f07835', 'provider.py': '7a4cd2ebc921a9ade9b9a2bb937a92fd33bcfe0b13493e9758f3321fb948984d', 'tests/test_installer.py': 'f1c6fb0ab2540d1b982f57af4e963d3ace6b92212288408c94c631f85cf5b91e', 'tests/test_public.py': '7ce3f3057cf58262f2bcfdfdf8764af18cd87c455b3a4fe56170aa0050eafbff'}
TESTS = (
    R15 + '/tests',
    'phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py',
    'phase175_r4r12r9_delta_generator_image_bridge/tests/test_rule.py',
    'phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py',
    'phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py',
    'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def preflight():
    require(Path(git('rev-parse','--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(git('branch','--show-current') == 'develop', 'WRONG_BRANCH')
    head = git('rev-parse','HEAD')
    require(head == git('rev-parse','origin/develop'), 'LOCAL_REMOTE_HEAD_MISMATCH')
    git('merge-base','--is-ancestor',BASE,head)
    require(not git('diff','--cached','--name-only'), 'STAGED_CHANGES_REFUSED')
    require(not (set(git('diff','--name-only','HEAD').splitlines()) - {TARGET}), 'UNRELATED_TRACKED_CHANGES')
    for path, pin in PINS.items():
        if path == TARGET:
            continue
        require(git('rev-parse','HEAD:'+path) == pin and matches_blob((ROOT/path).read_bytes(),pin), 'DEPENDENCY_CHANGED:'+path)
    baseline = subprocess.check_output(['git','show',BASE+':'+TARGET],cwd=ROOT)
    require(matches_blob(baseline,PINS[TARGET]), 'REVIEWED_BASE_BLOB_CHANGED')
    expected = proposed_source(normalize(baseline))
    committed = normalize(subprocess.check_output(['git','show','HEAD:'+TARGET],cwd=ROOT))
    require(committed in (normalize(baseline),expected), 'UNREVIEWED_COMMITTED_SHARED_SOURCE')
    require(normalize((ROOT/TARGET).read_bytes()) == expected, 'R15_HOOK_MISSING_OR_CHANGED')
    for path, digest in R15_SHA256.items():
        raw = (ROOT/R15/path).read_bytes()
        require(hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest() == digest, 'R15_PACKAGE_CHANGED:'+path)
    print('PHASE177_R16_HEAD='+head,flush=True)
    print('PHASE177_R16_R15_HOOK=VERIFIED',flush=True)
    return {'head':head,'reviewed_base':BASE,'hook_committed':committed == expected}


def rule_name(step):
    return step.inference_rule.name if step.inference_rule is not None else None


def nodes_of(root):
    """Identity-deduplicated postorder of the actual root's ancestors."""
    seen, active, nodes = set(), set(), []
    def visit(step):
        key = id(step)
        require(key not in active, 'PROOF_TREE_CYCLE')
        if key in seen:
            return
        active.add(key)
        for parent in step.premises:
            visit(parent)
        active.remove(key)
        seen.add(key)
        nodes.append(step)
    visit(root)
    return tuple(nodes)


def audit_actual(folder):
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, verified_db_step
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
    from phase175_r4r12r13r2_delta_injective_e_surjective.rule import E_RULE_NAME, e_surjective_inputs
    from phase175_r4r3_two_summand_quotient.rule import RULE_NAME as QUOTIENT_RULE
    from phase177_r2_cited_511_reuse_audit.audit import capture
    from phase177_r9_delta_rhs_normalization_audit.audit import canonical_delta, route_matches
    from phase177_r14_finite_cyclic_delta_injective_isolated.rule import ORDER_RULE, INJECTIVE_RULE
    from phase177_r15_finite_cyclic_delta_injective_public.tests.test_public import verify_step
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from proof import ProofRule

    invocation, result, calls, model, view = capture()
    root, bridge = invocation['goal'], invocation['bridge']
    require(root.lhs == result.target == TodaPrimaryGroup(10,5), 'WRONG_TARGET')
    require(root == exact_prior_database_result(5,5) and isinstance(root.rhs,FiniteCyclicGroup) and root.rhs.order == 2, 'WRONG_GROUP_PRESENTATION')
    require(result.status.value == 'complete' and result.conclusion == root and not result.open_goals, 'ROOT_NOT_COMPLETE')
    require(view.key == 'generic-complete-proof' and not view.partial_result and model is not None, 'WEB_NOT_COMPLETE')
    roots = [s for s in result.proven_steps if s.conclusion == root]
    require(bool(roots), 'ROOT_PROOFSTEP_MISSING')
    proof = roots[-1]
    require(proof.rule is ProofRule.INFERENCE, 'ROOT_NOT_INFERRED')
    nodes = nodes_of(proof)
    require(model.root_index is not None and model.steps[model.root_index] is proof, 'MODEL_ROOT_MISMATCH')
    model_scope = root_ancestor_step_indices(model.steps, model.root_index)
    require({id(model.steps[i]) for i in model_scope} == {id(s) for s in nodes}, 'MODEL_ANCESTRY_MISMATCH')
    require(all(set(c.step_indices) <= model_scope for c in model.citations), 'NON_ROOT_CITATION')
    require(not any(s.rule is ProofRule.GIVEN and s.conclusion == root for s in nodes), 'ROOT_GIVEN_REFUSED')
    cyclic = CyclicStructureStatement(root.lhs,root.rhs.generator,2)
    routes = expand_public_two_summand_quotient(cyclic,proof_target=root)
    chosen, = [r for r in routes if route_matches(canonical_delta(),delta_image_equality(r.subgoals[2]))]
    quotient, = [s for s in nodes if s.conclusion == cyclic and rule_name(s) == QUOTIENT_RULE]
    verify_step(quotient,QUOTIENT_RULE,chosen.subgoals)
    middle, upper_domain, upper_image, exact, surj, survivor = quotient.premises
    verify_step(surj,E_RULE_NAME,e_surjective_inputs(surj.conclusion))
    delta, h_delta, e_h = surj.premises
    require(rule_name(delta) == INJECTIVE_RULE and len(delta.premises) == 3, 'R14_INJECTIVITY_NOT_USED')
    domain, lower_image, order = delta.premises
    verify_step(delta,INJECTIVE_RULE,(domain.conclusion,lower_image.conclusion,order.conclusion))
    codomain, = order.premises
    verify_step(order,ORDER_RULE,(codomain.conclusion,))
    require(domain.conclusion == exact_prior_database_result(9,1) and codomain.conclusion == exact_prior_database_result(4,4), 'LOWER_PRESENTATION_MISMATCH')
    from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
    from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25
    for image in (upper_image,lower_image):
        require(any(s.rule is ProofRule.GIVEN and s.conclusion == CitedToda511(canonical_511()) for s in nodes_of(image)), 'CITED_511_NOT_ANCESTOR')
    require(any(s.rule is ProofRule.GIVEN and s.conclusion == CitedTodaProp25() for s in nodes_of(upper_image)), 'PROP25_NOT_ANCESTOR')
    db = []
    for step in nodes:
        if step.rule is ProofRule.GIVEN and step.note == 'ADOPTED_DATABASE_PRIOR; independent reference not asserted':
            require(verified_db_step(step,proof_target=root,bridge=bridge), 'DB_PROVENANCE_INVALID')
            db.append(repr(step.conclusion))
    require(len(db) >= 4, 'EXPECTED_PRIOR_GROUPS_NOT_RETAINED')
    # Web entry already runs verify_proof_tree_for_narrative before returning.
    # Report actual ancestor nodes separately from search-wide observations.
    indexes = {id(s):i for i,s in enumerate(nodes,1)}
    rows = [{'id':indexes[id(s)],'statement':repr(s.conclusion),'trust':s.rule.name,
             'rule':rule_name(s),'premises':[indexes[id(p)] for p in s.premises],
             'note':s.note} for s in nodes]
    citations = [{'number':c.number,'label':c.reference.label,'locator':c.reference.locator,
                  'model_step_indices':list(c.step_indices),'assertion_ids':list(c.assertion_ids),
                  'reference_ids':list(c.reference_ids)} for c in model.citations]
    narrative = render_model_backed_narrative_markdown(result,model)
    (folder/'narrative.md').write_text(narrative,encoding='utf-8')
    (folder/'root_proof_tree.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    details = {'status':result.status.value,'web_key':view.key,'open_goals':len(result.open_goals),
               'root_ancestor_nodes':len(nodes),'root_inferences':sum(s.rule is ProofRule.INFERENCE for s in nodes),
               'root_given_leaves':sum(s.rule is ProofRule.GIVEN for s in nodes),
               'search_observed_steps':len(result.proven_steps),
               'narrative_model_steps':len(model.steps),'reference_count':len(citations),'citations':citations,
               'db_prior_leaves':db,'quotient_rule':rule_name(quotient),'quotient_premises':len(quotient.premises),
               'surjectivity_rule':rule_name(surj),'surjectivity_premises':[repr(s.conclusion) for s in surj.premises],
               'order_rule':rule_name(order),'injectivity_rule':rule_name(delta),'survivor':repr(survivor.conclusion),
               'hopf_zero_separate_step':any(type(s.conclusion).__name__ == 'TodaHopfInvariantZeroStatement' for s in nodes)}
    for name in ('status','web_key','open_goals','root_ancestor_nodes','root_inferences','root_given_leaves','search_observed_steps','narrative_model_steps','reference_count','quotient_premises','surjectivity_rule','hopf_zero_separate_step'):
        print('PHASE177_R16_'+name.upper()+'='+str(details[name]),flush=True)
    print('PHASE177_R16_DB_PRIOR_VERIFIED='+str(len(db)),flush=True)
    print('PHASE177_R16_ROOT_TREE=VERIFIED',flush=True)
    return details


def execute(dry_run):
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'phase':'177_R16','dry_run':dry_run,'gate':'FAIL_R16','full_pytest':'NOT_RUN'}
    try:
        before = snapshot()
        report['preflight'] = preflight()
        if not dry_run:
            report['actual'] = audit_actual(folder)
            subprocess.run([sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS],cwd=ROOT,check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'))
        require(snapshot() == before,'REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
        report['gate'] = 'PASS_R16_READ_ONLY_DRYRUN' if dry_run else 'PASS_R16_VERIFIED_COMPLETE_PROOF_TREE_AUDITED'
    except Exception as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc())
        print('PHASE177_R16_ERROR='+repr(exc),flush=True)
    path = folder/'report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PHASE177_R16_REPORT='+str(path),flush=True)
    print('PHASE177_R16_NEW_MATH_RULES=0')
    print('PHASE177_R16_NEW_GIVEN=0')
    print('PHASE177_R16_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R16_GATE='+report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    return execute(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
