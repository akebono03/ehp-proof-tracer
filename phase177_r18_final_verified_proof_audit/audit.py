"""Audit the actual verified public proof and final narrative; no installation."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

from phase177_r2_cited_511_reuse_audit import audit as r2
from phase177_r16_verified_proof_tree_audit.audit import audit_actual
from phase168_r3_41p13_trust_boundary import verification as verifier
import phase168_r3_41p13_trust_boundary as trust
from proof import ProofRule, Relation
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase175_r4r10_cited_58_prop25_public.source import source_positions
from phase175_r4r12r10r1_cited_511_public.source import verify_cited_511

ROOT = Path(__file__).resolve().parents[1]
HEAD = 'c4e6728aa1ae2b0e7e231bdd0f378df5a0a04faf'
PINS = {
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase165_r52_r9_shared_math.py': 'f4383a0c248fe62903203d1863df345740581c59',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'phase168_r3_41p13_trust_boundary/__init__.py': '5eade56b4c346595d43a8d79ff632d960e602297',
    'phase168_r3_3_proof_narrative_model.py': '6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52',
    'phase168_r3_5_model_renderer.py': '9afd21ed344beea80699f49cba16ddd68197198b',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase177_r16_verified_proof_tree_audit/audit.py': '7808f40b83f76f697849c3ad6ec96c980b9ad841',
    'phase177_r17r3_rank_two_quotient_display/tests/test_display.py': 'd57adccbe17a1f3037b1e247e6da78b4b18f15dc',
    'phase177_r17r4r1_prop25_suspension_elision/projection.py': '1d6dd710fcedd025a385480b22b12aaee46b4215',
    'phase177_r17r4r2_prop25_equality_chain/projection.py': 'a5f35b71b053c603f540f9750b3af50101dde3ab',
    'phase177_r17r5_duplicate_cited_equality/projection.py': '211e90eb4ba9d799d4e7cb15bef754db19dcff9f',
    'phase177_r17r6r1_suspension_composition_display/projection.py': 'dd05a23a458aca832c323fe6320c567734dd4ecb',
    'phase177_r17r6r1_suspension_composition_display/tests/test_display.py': 'aff28b4aab345e41001e338cf7cf0e808cffb4c5',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py': 'bd37cb05011ed0d9413bdd7f7335a116d29dae33',
    'tests/test_phase165_r3_recursive_search.py': '708977bb138cec3c45d565d5e81ddc0e4f957a8e',
    'phase176_r3r60r1_citation_premise_elision_isolated/tests/test_projection.py': 'bcc40ee8211a95c50ffa64412b0d0279922b0a9b',
    'phase175_r4r10_cited_58_prop25_public/source.py': 'b5162bdaac25e4578973816290207379734229f6',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase169_r10e5_composite_generator_image/rule.py': '01acace3eb273d47091421a61291ee54b51c369f',
    'phase175_r4r3_two_summand_quotient/rule.py': 'b854491dff8b42817c5e1fe2771e4f2dc2c16713',
    'phase177_r15_finite_cyclic_delta_injective_public/tests/test_public.py': '8f6d2419933f3748a40749cbbdc3c65f4228fa24',
}
TESTS = (
    'phase177_r17r6r1_suspension_composition_display/tests',
    'phase177_r17r5_duplicate_cited_equality/tests',
    'phase177_r17r4r2_prop25_equality_chain/tests',
    'phase177_r17r4r1_prop25_suspension_elision/tests',
    'phase177_r17r3_rank_two_quotient_display/tests',
    'phase177_r17r1_finite_delta_reason_display/tests',
    'phase168_r3_27_typed_projection/tests',
    'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py',
    'phase177_r15_finite_cyclic_delta_injective_public/tests/test_public.py',
    'phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py',
    'phase177_r3_unsigned_delta_composition_isolated/tests/test_rule.py',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
    'tests/test_phase165_r3_recursive_search.py',
    'phase176_r3r60r1_citation_premise_elision_isolated/tests/test_projection.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE177_R18_'+key+'='+str(value), flush=True)


def preflight():
    require(Path(r2.git('rev-parse','--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(r2.git('branch','--show-current') == 'develop', 'WRONG_BRANCH')
    head = r2.git('rev-parse','HEAD')
    require(head == r2.git('rev-parse','origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:'+HEAD+';actual='+head)
    require(not r2.git('status','--porcelain','--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    for path, pin in PINS.items():
        require(r2.git('rev-parse','HEAD:'+path) == pin and r2.matches_blob((ROOT/path).read_bytes(),pin), 'DEPENDENCY_CHANGED:'+path)
    for path in TESTS:
        require((ROOT/path).exists(), 'FOCUSED_TEST_MISSING:'+path)
    positions = source_positions(ROOT)
    positions['toda:(5.11)'] = verify_cited_511(ROOT)
    require(positions['toda:Proposition 2.5'] < positions['toda:(5.11)'], 'SOURCE_ORDER_INVALID')
    emit('HEAD',head)
    emit('REVIEWED_SOURCE_PINS',len(PINS))
    emit('SOURCE_POSITIONS','VERIFIED')
    return {'head':head,'pins':PINS,'source_positions':positions}


def same_group_claim(statement, target):
    if isinstance(statement, Relation):
        return statement.lhs == target or statement.rhs == target
    if isinstance(statement, (CyclicStructureStatement, TodaPrimaryGroupZeroStatement)):
        return statement.group == target
    return False


def observe(folder):
    # Observe the real trust boundary, never substitute a success result.
    actual_capture, actual_verify = r2.capture, verifier.verify_proof_tree_for_narrative
    captured, checks = [], []

    def observed_verify(result, bridge, **kwargs):
        counts = actual_verify(result, bridge, **kwargs)
        checks.append((result, bridge, dict(kwargs), counts))
        return counts

    def observed_capture():
        value = actual_capture()
        captured.append(value)
        return value

    with patch.object(trust, 'verify_proof_tree_for_narrative', observed_verify), \
         patch.object(verifier, 'verify_proof_tree_for_narrative', observed_verify), \
         patch.object(r2, 'capture', observed_capture):
        details = audit_actual(folder)
    require(len(captured) == 1, 'PUBLIC_CAPTURE_COUNT_CHANGED')
    invocation, result, calls, model, view = captured[0]
    verified = [item for item in checks if item[0] is result]
    require(len(verified) == 1, 'ACTUAL_WEB_VERIFICATION_MISSING_OR_AMBIGUOUS')
    _, bridge, gate_kwargs, counts = verified[0]
    steps = model.steps
    require(len(result.proven_steps) == len(steps) == 43, 'PROOF_STEP_COUNT_CHANGED')
    require(details['root_ancestor_nodes'] == 43 and details['reference_count'] == 8, 'ROOT_SCOPE_CHANGED')
    inferred, given = counts
    require(inferred == details['root_inferences'] and given == details['root_given_leaves'] and inferred + given == 43, 'TRUST_COUNTS_MISMATCH')
    require(not any(s.rule is ProofRule.GIVEN and same_group_claim(s.conclusion,result.target) for s in steps), 'TARGET_GROUP_GIVEN_IN_TREE')
    require(not any(link.step is not None and link.step.rule is ProofRule.GIVEN
                    and same_group_claim(link.step.conclusion,result.target)
                    for link in invocation['bridge'].proof_links), 'TARGET_GROUP_GIVEN_IN_SCREENED_SEARCH_LINKS')
    require(not any(link.step is not None and link.step.rule is ProofRule.GIVEN
                    and same_group_claim(link.step.conclusion,result.target)
                    for link in bridge.proof_links), 'TARGET_GROUP_GIVEN_IN_WEB_TRUST_LINKS')
    numbers = model.step_citation_numbers
    citations = model.citations
    require(tuple(c.number for c in citations) == tuple(range(1,9)), 'REFERENCE_NUMBER_MISMATCH')
    require(len(numbers) == len(steps), 'CITATION_MODEL_LENGTH_MISMATCH')
    require(all(set(c.step_indices) == {i for i,ns in enumerate(numbers) if c.number in ns}
                and c.step_indices for c in citations), 'REFERENCE_ASSOCIATION_MISMATCH')
    require(all(set(ns) <= set(range(1,9)) for ns in numbers), 'UNKNOWN_MODEL_REFERENCE')
    require(all(ns for s,ns in zip(steps,numbers) if s.rule is ProofRule.GIVEN), 'UNCITED_GIVEN')
    narrative = (folder/'narrative.md').read_text(encoding='utf-8')
    lines = narrative.splitlines()
    require(lines.count('証明') == 1, 'PROOF_BODY_BOUNDARY_CHANGED')
    boundary = lines.index('証明')
    body = lines[boundary+1:]
    refs = [int(m.group(1)) for s in lines[:boundary] if (m := re.match(r'^\*\*\[R(\d+)\] ',s))]
    require(refs == list(range(1,9)), 'DISPLAY_REFERENCE_COUNT_CHANGED')
    tags = {int(n) for s in body for n in re.findall(r'\[R(\d+)\]',s)}
    require(tags == set(range(1,9)), 'DISPLAY_CITATION_MISSING_OR_UNKNOWN')
    expected = (
        r"[R4]より, $\Delta\left(\eta_{9}\right) = E\nu'\eta_{7}$.",
        r"[R3]を用いて, $\Delta\left(\eta_{9}^{2}\right) = E\nu'\eta_{7}^{2}$.",
        r"よって, $\Delta:\pi_{10}^{9}\to \pi_{8}^{4}$ は単射.",
        r"完全性より, $E: \pi_{9}^{4}\to \pi_{10}^{5}$ は全射.",
        r"完全性より, $\ker E=\operatorname{Im}\Delta=\mathbb{Z}/2\{E\nu'\eta_{7}^{2}\}$.",
        r"[R8]を用いて, $E(\nu_{4}\eta_{7}^{2})=\nu_{5}\eta_{8}^{2}$.",
        r"$E$ は全射なので, 準同型定理より $\pi_{10}^{5}\cong \pi_{9}^{4}/\ker E$.",
        r"以上より, $\pi_{10}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}^{2}\}$.",
    )
    require(all(body.count(s) == 1 for s in expected), 'FINAL_NARRATIVE_EXPECTATION_CHANGED')
    require([body.index(s) for s in expected] == sorted(body.index(s) for s in expected), 'FINAL_NARRATIVE_ORDER_CHANGED')
    forbidden = (r'$E(\nu_{4})=\nu_{5}$.', r'$E(\eta_{7}^{2})=\eta_{8}^{2}$.',
                 r"$\Delta\left(\eta_{9}^{2}\right) = E\nu'\eta_{7}\eta_{8}$.",
                 r"$E\nu'\eta_{7}^{2} = E\nu'\eta_{7}\eta_{8}$.")
    require(not any(fragment in s for s in body for fragment in forbidden), 'SUPPRESSED_AUXILIARY_REAPPEARED')
    require(body[-1] == '□', 'PROOF_END_MISSING')
    emit('WEB_KEY',view.key)
    emit('ROOT_STEPS',43)
    emit('VERIFIED_INFERENCES',inferred)
    emit('VERIFIED_GIVEN_LEAVES',given)
    emit('REFERENCE_COUNT',8)
    emit('OPEN_GOALS',len(result.open_goals))
    emit('TARGET_GROUP_GIVEN',0)
    emit('SEARCH_LOOKUP_MODE',invocation['lookup_mode'])
    emit('WEB_TRUST_BOUNDARY','VERIFIED')
    emit('NARRATIVE','VERIFIED')
    details.update(trust_counts={'inferences':inferred,'given':given}, trust_gate_arguments=gate_kwargs,
                   search_lookup_mode=invocation['lookup_mode'], provider_call_count=len(calls),
                   target_group_given=0, displayed_reference_numbers=refs, body_citation_numbers=sorted(tags),
                   narrative_verified=True)
    return details


def execute(dry_run):
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'phase':'177_R18','dry_run':dry_run,'gate':'FAIL_R18','full_pytest':'NOT_RUN'}
    try:
        before = r2.snapshot()
        report['preflight'] = preflight()
        if not dry_run:
            report['actual'] = observe(folder)
            report['focused_tests'] = list(TESTS)
            command = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            completed = subprocess.run(command, cwd=ROOT, env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'))
            report['focused_pytest_exit_code'] = completed.returncode
            require(completed.returncode == 0, 'FOCUSED_PYTEST_FAILED')
            emit('FIRST_SUCCESS_REGRESSION','PASS')
            emit('PHASE176_DISPLAY_REGRESSION','PASS')
        require(r2.snapshot() == before, 'REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
        report['gate'] = 'PASS_R18_READ_ONLY_DRYRUN' if dry_run else 'PASS_R18_FINAL_VERIFIED_PROOF_AUDIT'
    except Exception as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    path = folder/'report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    emit('REPORT',path)
    emit('NEW_MATH_RULES',0)
    emit('NEW_GIVEN',0)
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    return execute(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
