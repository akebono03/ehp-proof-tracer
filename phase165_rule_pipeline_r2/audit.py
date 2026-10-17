"""Read-only audit of generic rule pipeline for a supplied typed goal."""
from __future__ import annotations
import json
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r57_r23_conclusion_unification import unify_inference_conclusion
from phase165_r57_r25_premise_generation import generate_candidate_premises
from phase165_r57_r24_candidate_discovery import DiscoveredRuleCandidate
from phase165_r8_rule_provider import discover_inference_rules
from proof import Relation, ProofRule
from unified_statement_registry import AssertionOrigin


def main() -> dict:
    root = Path.cwd()
    assert not (root / 'phase165_r52_r23_existing_rule_adapter.py').exists(), 'group adapter still present'
    eta = HomotopyElement(name='η_3', dimension=3, source=4, target=3,
                           generator=GeneratorSymbol(family='η', index=3))
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta))
    bridge = build_shared_typed_bridge()
    assertion_id = next(iter(bridge.registry._assertions))
    screened = screen_shared_proof_context(bridge, goal=goal, citing_assertion_id=assertion_id)
    rules, discovery = discover_inference_rules()
    unified = []
    generated = []
    rejected = []
    for idx, rule in enumerate(rules):
        match = unify_inference_conclusion(rule, goal)
        if match is None:
            continue
        row = {'index': idx, 'rule': rule.name, 'premise_patterns': len(rule.premise_patterns),
               'conclusion_pattern_present': rule.conclusion_pattern is not None}
        unified.append(row)
        candidate = DiscoveredRuleCandidate(key=f'audit:{idx}', unification=match, source='audit')
        result = generate_candidate_premises(candidate)
        if result is None:
            rejected.append(row)
        else:
            generated.append({**row, 'premises': [repr(p) for p in result.expansion.subgoals]})
    cited = [l for l in screened.proof_links if l.step is not None and l.step.rule is ProofRule.GIVEN and
             screened.registry.assertion(l.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT]
    proposals = shared_expansion_provider(screened, proof_target=goal)(goal)
    summary = {
        'phase': '165 common rules R2', 'mode':'READ_ONLY_DYNAMIC',
        'group_adapter_absent': True, 'rules_discovered':len(rules),
        'discovery_modules':list(discovery.modules),
        'skipped_factories':list(discovery.skipped_factories),
        'rules_without_conclusion_pattern':list(discovery.skipped_rules),
        'unified_count':len(unified), 'unified':unified,
        'generic_generated_count':len(generated), 'generic_generated':generated,
        'premise_generation_rejected':rejected,
        'screened_cited_given_count':len(cited),
        'shared_root_proposals':len(proposals),
        'shared_root_rules':[p.rule.name for p in proposals],
        'full_pytest_run':False,
    }
    out = Path(__file__).with_name('audit_result.json')
    out.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({key: summary[key] for key in (
        'phase','group_adapter_absent','rules_discovered','unified_count',
        'generic_generated_count','screened_cited_given_count','shared_root_proposals','shared_root_rules','full_pytest_run')},ensure_ascii=False,indent=2))
    print('Audit saved:',out)
    return summary


if __name__ == '__main__':
    main()
