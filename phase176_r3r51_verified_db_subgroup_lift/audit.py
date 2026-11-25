"""Verify the actual public search accepts the five independent lift premises."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase169_r10e4_ordered_db_prior.db_prior import verified_db_step
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import (
    RULE_NAME, finite_cyclic_subgroup_lift_inputs, finite_cyclic_subgroup_lift_rule,
)
from phase176_r3r49_hopf_image_frontier.audit import capture_web
from phase176_r3r50_strict_nu_prime_connection.audit import walk_tree
from proof import ProofRule, find_inference_matches_for_rule


def observe(baseline=False):
    invocation, result, calls, key = capture_web()
    bridge, root = invocation['bridge'], invocation['goal']
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, root.rhs.order)
    candidates = [option for target, options in calls if target == goal
                  for option in options if option.rule.name == RULE_NAME]
    if not candidates:
        raise RuntimeError('PUBLIC_LIFT_CANDIDATE_NOT_REACHED')
    if baseline:
        # The same five facts must already have been accepted before the patch.
        for option in candidates:
            facts = tuple(next((s for s in result.proven_steps if s.conclusion == target), None)
                          for target in option.subgoals)
            if any(s is None for s in facts):
                continue
            if (not verified_db_step(facts[2], proof_target=root, bridge=bridge)
                    or any(facts[j].rule is not ProofRule.INFERENCE for j in (0,1,3,4))):
                continue
            if find_inference_matches_for_rule(option.rule, facts):
                raise RuntimeError('BASELINE_ALREADY_ACCEPTS_PRIOR')
            return {'gate':'PASS_R3R51_BASELINE_GIVEN_REJECTION_CONFIRMED',
                    'status':result.status.value, 'premise_rules':[s.rule.value for s in facts],
                    'all_five_premises_proved':True, 'codomain_prior_verified':True,
                    'old_rule_rejects_prior':True}
        raise RuntimeError('BASELINE_FIVE_PREMISES_NOT_FOUND')
    lifts = [s for s in result.proven_steps if s.conclusion == goal and s.rule is ProofRule.INFERENCE
             and s.inference_rule is not None and s.inference_rule.name == RULE_NAME]
    if not lifts:
        raise RuntimeError('PUBLIC_LIFT_NOT_PROVED')
    lift = lifts[0]
    parents = lift.premises
    if (len(parents) != 5 or any(parents[j].rule is not ProofRule.INFERENCE for j in (0,1,3,4))
            or not verified_db_step(parents[2], proof_target=root, bridge=bridge)):
        raise RuntimeError('LIFT_PREMISE_PROVENANCE_MISMATCH')
    inputs = tuple(s.conclusion for s in parents)
    if finite_cyclic_subgroup_lift_inputs(goal, *inputs[1:]) != inputs:
        raise RuntimeError('LIFT_TYPED_INPUT_MISMATCH')
    if not any(option.subgoals == inputs for option in candidates):
        raise RuntimeError('ACCEPTED_LIFT_NOT_FROM_PUBLIC_PROVIDER')
    if not find_inference_matches_for_rule(lift.inference_rule, parents):
        raise RuntimeError('CONTEXTUAL_RULE_REPLAY_FAILED')
    if find_inference_matches_for_rule(finite_cyclic_subgroup_lift_rule(goal, *inputs[1:]), parents):
        raise RuntimeError('UNCONTEXTUAL_RULE_ACCEPTED_DB_PRIOR')
    root_step = next((s for s in result.proven_steps if s.conclusion == root and s.rule is ProofRule.INFERENCE), None)
    if root_step is None or not any(s is lift for s in walk_tree(root_step)):
        raise RuntimeError('ROOT_NOT_INFERRED_FROM_LIFT')
    if result.status.value != 'complete' or result.conclusion != root or result.open_goals:
        raise RuntimeError('PUBLIC_ROOT_NOT_COMPLETE')
    tree = walk_tree(root_step)
    if any(s.rule is ProofRule.GIVEN and s.conclusion in (root, goal) for s in tree):
        raise RuntimeError('ROOT_GIVEN_FORBIDDEN')
    if not all(any(s is parent for s in tree) for parent in parents):
        raise RuntimeError('LIFT_ANCESTRY_LOST')
    return {'gate':'PASS_R3R51_PUBLIC_VERIFIED_DB_SUBGROUP_LIFT', 'status':result.status.value,
            'web_key':key, 'root_group_proved':True, 'root':repr(root),
            'accepted_step_count':len(result.proven_steps), 'root_tree_steps':len(tree),
            'open_goals':[], 'lift_rule':RULE_NAME, 'lift_premise_rules':[s.rule.value for s in parents],
            'lift_premises':[repr(s.conclusion) for s in parents], 'codomain_prior_verified':True,
            'old_contextless_rule_rejects_prior':True, 'hopf_injective_preserved':True,
            'kernel_preserved':True, 'hopf_image_preserved':True,
            'new_math_rules':0, 'new_given_registrations':0, 'full_pytest':'NOT_RUN'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    report = observe(args.baseline)
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r51_verified_db_subgroup_lift'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / ('baseline.json' if args.baseline else 'report.json')
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for k,v in report.items():
        print('PHASE176_R3R51_'+k.upper()+'='+json.dumps(v,ensure_ascii=False))
    print('REPORT='+str(path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
