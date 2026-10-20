"""Read-only R3-T runtime diagnostic using the user's installed production modules."""
from __future__ import annotations
import json
from pathlib import Path
from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
from proof import ProofRule
from toda_rules import Toda45IsomorphismStatement


def run() -> dict:
    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=4, k=1)
    bases = registered_group_goal_candidates(bridge, n=3, k=1)
    report = {
        'audit': 'phase166-r3t-connection',
        'production_code_modified': False,
        'pi54_goal_candidate_count': len(targets),
        'pi43_goal_candidate_count': len(bases),
        'pi54_candidates': [repr(x) for x in targets],
        'pi43_candidates': [repr(x) for x in bases],
    }
    catalog, diagnostic = resolve_reviewed_order_catalog(bridge, n=4, k=1)
    report['reviewed_order_catalog_available'] = catalog is not None
    report['reviewed_order_diagnostic'] = diagnostic
    if len(targets) != 1:
        report['blocker'] = 'Target goal is not unique; no arbitrary assertion ID selected'
        return report
    goal = targets[0]
    matching = [a for a in bridge.registry._assertions.values() if type(a.content) is type(goal) and a.content == goal]
    report['exact_target_assertion_ids'] = [a.assertion_id for a in matching]
    report['exact_target_assertion_count'] = len(matching)
    if len(matching) != 1:
        report['blocker'] = 'No unique exact target assertion ID; do not synthesize one'
        return report
    citing_id = matching[0].assertion_id
    screened = screen_shared_proof_context(bridge, goal=goal, citing_assertion_id=citing_id, explicit_publication_target=True)
    available = tuple(link.step.conclusion for link in screened.proof_links if link.step is not None and link.step.rule is ProofRule.GIVEN)
    report['screened_given_count'] = len(available)
    report['pi43_source_given'] = [base in available for base in bases]
    report['screened_toda45_iso_count'] = sum(isinstance(x, Toda45IsomorphismStatement) for x in available)
    general = [x for x in available if isinstance(x, Toda45IsomorphismStatement)]
    report['screened_iso_reprs'] = [repr(x) for x in general]
    provider = shared_expansion_provider(screened, proof_target=goal)
    proposals = provider(goal)
    report['goal_proposal_count'] = len(proposals)
    report['goal_proposal_rules'] = [getattr(x.rule, 'name', str(x.rule)) for x in proposals]
    report['direct_transport_options'] = len(expand_registered_toda45_finite_cyclic_goal(goal, available))
    report['transport_options_with_pi43_source'] = len(expand_registered_toda45_finite_cyclic_goal(goal, available + tuple(bases)))
    report['diagnostic'] = 'Read-only diagnostics; no claims about a complete proof or pytest PASS'
    return report


if __name__ == '__main__':
    result = run()
    output = Path(__file__).resolve().parent / 'audit_result.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    print('REPORT:', output)
