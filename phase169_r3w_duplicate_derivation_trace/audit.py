"""Phase 169 R3W: trace genuine verified competing backward derivations.

No edits or alternative proof selection. The existing append_unique_verified_derivation
is delegated to unchanged, after recording each verified candidate and its provenance.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import phase165_r3_recursive_search as recursive
from phase165_r6_2_r4_r8_dedup import same_cited_scalar_specialization
from phase165_r12_r33_proof_tree_dedup import same_completed_proof_tree
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation,
    specialize_eta_group_relation,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase165_r52_partial_proof import ProofSearchStatus
from proof import ProofRule
from toda_rules import TodaProp51FiniteDimensionalStatement

PACKAGE = Path(__file__).resolve().parent


def describe_step(step, screened):
    """Describe genuine ProofStep provenance without interpreting rule-name semantics."""
    leaves = []
    seen = set()

    def visit(node):
        if id(node) in seen:
            return
        seen.add(id(node))
        if node.rule is ProofRule.GIVEN:
            links = [link.assertion_id for link in screened.proof_links
                     if link.step is node]
            literature = getattr(getattr(node, 'inference_rule', None), 'literature_reference', None)
            leaves.append({
                'conclusion_type': type(node.conclusion).__name__,
                'conclusion_repr': repr(node.conclusion)[:500],
                'linked_assertion_ids': links,
                'literature_locator': getattr(literature, 'locator', None),
            })
        for premise in node.premises:
            visit(premise)

    visit(step)
    return {
        'rule': step.rule.value,
        'inference_name': getattr(step.inference_rule, 'name', None),
        'premise_types': [type(p.conclusion).__name__ for p in step.premises],
        'premise_rules': [p.rule.value for p in step.premises],
        'premise_rule_names': [getattr(p.inference_rule, 'name', None) for p in step.premises],
        'given_leaves': leaves,
    }


def examine() -> dict:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(goals) != 1:
        raise AssertionError('Expected exactly one π_5^3 database goal')
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if not citing:
        raise AssertionError('Missing π_5^3 source target')
    contexts = []
    completed = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if completed.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise AssertionError('Expected completed π_5^3 baseline')
    screened = contexts[0]
    cited = tuple(link for link in screened.proof_links
                  if link.step is not None
                  and link.step.rule is ProofRule.GIVEN
                  and precedes_citing_assertion(screened, link.assertion_id, citing))
    prop51 = tuple(link.step.conclusion for link in cited
                   if isinstance(link.step.conclusion, TodaProp51FiniteDimensionalStatement))
    if len(prop51) != 1:
        raise AssertionError('Expected exactly one cited Proposition 5.1 composite')
    general = prop51[0].higher_eta_group_relation
    if not _is_generic_eta_group_relation(general):
        raise AssertionError('Unexpected higher-eta proposition schema')
    concrete = specialize_eta_group_relation(general, 5)
    direct = tuple(link.assertion_id for link in cited
                   if type(link.step.conclusion) is type(concrete)
                   and link.step.conclusion == concrete)
    provider = shared_expansion_provider(screened, proof_target=target)
    expansions = provider(concrete)
    proposed = []
    for item in expansions:
        proposed.append({
            'rule': getattr(item.rule, 'name', None),
            'subgoal_types': [type(x).__name__ for x in item.subgoals],
            'subgoal_short': [repr(x)[:450] for x in item.subgoals],
        })

    attempted_steps = []
    attempts = []
    original_append = recursive.append_unique_verified_derivation

    def observing_append(options, candidate):
        previously = len(options)
        original_append(options, candidate)
        if type(candidate.conclusion) is type(concrete) and candidate.conclusion == concrete:
            attempted_steps.append(candidate)
            row = describe_step(candidate, screened)
            row['kept_after_existing_dedup'] = len(options) > previously
            row['options_before'] = previously
            row['options_after'] = len(options)
            attempts.append(row)

    proof_status = 'not_attempted'
    with patch.object(recursive, 'append_unique_verified_derivation', observing_append):
        try:
            proof = recursive.reconstruct_registered_goal(
                concrete, screened, citing, provider,
                lookup_mode='typed_reference_publication',
            )
        except recursive.RegisteredGoalUnresolved as error:
            proof_status = type(error).__name__ + ': ' + str(error)
        else:
            proof_status = 'proved: ' + getattr(proof.inference_rule, 'name', '<unnamed>')

    kept = [i for i, row in enumerate(attempts) if row['kept_after_existing_dedup']]
    comparisons = []
    for position, index1 in enumerate(kept):
        for index2 in kept[position + 1:]:
            comparisons.append({
                'left_index': index1,
                'right_index': index2,
                'same_cited_scalar_specialization': same_cited_scalar_specialization(
                    attempted_steps[index1], attempted_steps[index2],
                ),
                'same_completed_proof_tree': same_completed_proof_tree(
                    attempted_steps[index1], attempted_steps[index2],
                ),
                'same_premise_object_identity': (
                    len(attempted_steps[index1].premises) == len(attempted_steps[index2].premises)
                    and all(a is b for a, b in zip(
                        attempted_steps[index1].premises, attempted_steps[index2].premises,
                    ))
                ),
            })
    return {
        'phase': '169-R3W',
        'mode': 'AUDIT_ONLY',
        'pi53_status': completed.status.value,
        'pi65_proof_status': proof_status,
        'screened_direct_pi65_given_assertions': list(direct),
        'provider_proposal_count': len(proposed),
        'provider_proposals': proposed,
        'verified_candidate_attempts': attempts,
        'verified_candidate_count': len(attempts),
        'verified_candidate_kept_count': len(kept),
        'kept_candidate_pair_comparisons': comparisons,
        'production_modified': False,
        'existing_tests_modified': False,
        'full_pytest_run': False,
    }


def main() -> None:
    report = examine()
    dest = PACKAGE / 'output' / 'r3w_duplicate_derivations.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    for key in ('pi53_status', 'pi65_proof_status', 'screened_direct_pi65_given_assertions',
                'provider_proposal_count', 'verified_candidate_count', 'verified_candidate_kept_count'):
        print('R3W_' + key.upper() + '=' + repr(report[key]))
    for index, item in enumerate(report['verified_candidate_attempts']):
        print('R3W_CANDIDATE=' + json.dumps({'index': index, **item}, ensure_ascii=False))
    for comparison in report['kept_candidate_pair_comparisons']:
        print('R3W_PAIR_COMPARISON=' + json.dumps(comparison, ensure_ascii=False))
    print('R3W_AUDIT_ONLY=True')
    print('R3W_FULL_PYTEST_RUN=False')
    print('R3W_REPORT=' + str(dest))


if __name__ == '__main__':
    main()
