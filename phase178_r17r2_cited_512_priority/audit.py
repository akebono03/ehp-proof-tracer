"""Observe the real verified Web proof and its Narrative model; no proof injection."""
import argparse
import json
from pathlib import Path
from unittest.mock import patch

from phase178_r1_k6_source_first_audit import audit as r1
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase178_r15_toda512_isolated.source import canonical_512
from phase178_r15_toda512_isolated.provider import RULE_NAME as CITED_RULE
from phase178_r16_toda513_isolated.source import canonical_513
from phase178_r17_finite_cyclic_quotient_isolated.rule import RULE_NAME, finite_cyclic_quotient_inputs
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase177_r18_final_verified_proof_audit.audit import same_group_claim
from proof import ProofRule
from .installer import emit, require


def audit_actual(folder):
    import phase165_r52_r3_web_adapter as adapter
    real = adapter.build_partial_web_group_proof_view
    captured = []

    def capture(result, **kwargs):
        captured.append((result, kwargs.get('narrative_model')))
        return real(result, **kwargs)

    with patch.object(adapter, 'build_partial_web_group_proof_view', capture):
        summary = r1.observe(5, 6, folder)
    require(summary['status'] == 'complete' and summary['open_goal_count'] == 0
            and summary['web_key'] == 'generic-complete-proof'
            and summary['trust_status'] == 'VERIFIED'
            and summary['web_error'] is None and summary['complete_invariants_hold']
            and summary['target_given_count'] == 0, 'PUBLIC_PROOF_NOT_VERIFIED:' + repr(summary))
    require(len(captured) == 1, 'NARRATIVE_CAPTURE_COUNT')
    result, model = captured[0]
    require(model is not None and not model.open_goals, 'NARRATIVE_MODEL_MISSING')
    root = exact_prior_database_result(5,6)
    require(root is not None and result.conclusion == root, 'ROOT_CHANGED')
    steps = model.steps
    scope = root_ancestor_step_indices(steps, model.root_index)
    require(steps[model.root_index].conclusion == root and steps[model.root_index].rule is ProofRule.INFERENCE,
            'UNEXPECTED_ROOT_STEP')
    require(not any(s.rule is ProofRule.GIVEN and same_group_claim(s.conclusion, result.target) for s in steps),
            'TARGET_GIVEN_IN_MODEL')
    proof = tuple(steps[i] for i in sorted(scope))
    claim = canonical_512(4)
    signed = canonical_513()[0]
    direct = [s for s in proof if s.conclusion == claim.statement and s.rule is ProofRule.INFERENCE
              and s.inference_rule is not None and s.inference_rule.name == CITED_RULE]
    require(len(direct) == 1 and len(direct[0].premises) == 1
            and direct[0].premises[0].conclusion == claim
            and direct[0].premises[0].rule is ProofRule.GIVEN, 'CITED_512_NOT_IN_ROOT_ANCESTRY')
    quotients = [s for s in proof if s.rule is ProofRule.INFERENCE and s.inference_rule is not None
                 and s.inference_rule.name == RULE_NAME]
    require(len(quotients) == 1 and len(quotients[0].premises) == 6, 'QUOTIENT_PROOF_MISSING')
    q = quotients[0]
    values = tuple(p.conclusion for p in q.premises)
    require(values[2] == signed and q.premises[2].rule is ProofRule.GIVEN
            and finite_cyclic_quotient_inputs(q.conclusion, values[0], values[1], values[2], values[5]) == values,
            'QUOTIENT_PREMISES_CHANGED')
    numbers = model.step_citation_numbers
    citations = model.citations
    require(len(numbers) == len(steps) and len(citations) > 0, 'MODEL_CITATIONS_MISSING')
    require(tuple(c.number for c in citations) == tuple(range(1, len(citations)+1)), 'CITATION_NUMBERS_INVALID')
    for c in citations:
        require(set(c.step_indices) == {i for i, ns in enumerate(numbers) if c.number in ns}, 'CITATION_ASSOCIATION_INVALID')
    for leaf, locator in ((direct[0].premises[0], '(5.12)'), (q.premises[2], '(5.13)')):
        index = next(i for i in scope if steps[i] is leaf or steps[i] == leaf)
        require(any(c.number in numbers[index] and c.reference.locator == locator for c in citations),
                'SOURCE_CITATION_MISSING:' + locator)
    detail = json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
    inventory = detail['screened_source_inventory']
    require(inventory is not None and not inventory['target_group_given_links'], 'TARGET_GIVEN_IN_SCREENED_SOURCE')
    report = {'summary': summary, 'root_ancestor_count': len(scope), 'model_step_count':len(steps),
              'legacy_reference_count': summary['reference_count'], 'model_reference_count': len(citations),
              'model_citations': [{'number': c.number, 'locator': c.reference.locator,
                                   'step_indices': list(c.step_indices)} for c in citations],
              'cited_512_in_ancestry': True, 'cited_513_in_quotient': True,
              'quotient_six_premises': True, 'renderer_changed': False}
    (folder / 'proof_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    for key in ('status','proven_step_count','open_goal_count','trust_status','target_given_count','web_key'):
        emit('PUBLIC_' + key.upper(), summary[key])
    emit('ROOT_ANCESTOR_COUNT', len(scope))
    emit('LEGACY_REFERENCE_COUNT', summary['reference_count'])
    emit('MODEL_REFERENCE_COUNT', len(citations))
    emit('CITED_512_IN_ROOT_ANCESTRY', 'VERIFIED')
    emit('CITED_513_IN_QUOTIENT', 'VERIFIED')
    emit('QUOTIENT_SIX_PREMISES', 'VERIFIED')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, required=True)
    args = parser.parse_args()
    audit_actual(args.folder)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
