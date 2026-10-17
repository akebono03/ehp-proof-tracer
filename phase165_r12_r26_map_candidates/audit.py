"""Audit Web-equivalent backward expansion, never turn a proposal into evidence."""
from __future__ import annotations
import json
from pathlib import Path
from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r26_map_candidates import build_cited_eta_quotient_provider, cited_eta_source_count
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from toda_rules import toda_eta_family_definition_statement


def main() -> None:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=1)
    target = TodaPrimaryGroup(4, 3)
    cyclic = CyclicStructureStatement(target, toda_eta_family_definition_statement(3).element, 2)
    screened_count = cited_eta_source_count(bridge)
    direct = build_cited_eta_quotient_provider(bridge)(cyclic)
    common = shared_expansion_provider(bridge, proof_target=goals[0] if len(goals) == 1 else None)(cyclic)
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    data = {
        'phase': '165 R12-R26',
        'cited_general_eta_source_count': screened_count,
        'candidate_count': len(direct),
        'common_candidate_count': sum(option.subgoals == direct[0].subgoals for option in common) if direct else 0,
        'candidate_subgoals': [repr(x) for x in direct[0].subgoals] if direct else [],
        'web_search_status': result.status.value,
        'web_search_complete': result.conclusion is not None and not result.open_goals,
        'open_goals': [repr(x) for x in result.open_goals],
        'diagnostics': list(result.diagnostics),
        'full_pytest_run': False,
        'status': 'WEB_SEARCH_COMPLETE' if result.conclusion is not None and not result.open_goals else 'CANDIDATE_CONNECTED_SEARCH_PENDING',
    }
    path = Path(__file__).resolve().parent / 'audit_result.json'
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print('Audit saved:', path)


if __name__ == '__main__':
    main()
