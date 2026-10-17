"""Audit actual Web entry without claiming a proof that was not found."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r24_web_search_connection import expand_finite_cyclic_relation
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from proof import Relation
from toda_rules import toda_eta_family_definition_statement


def run_audit() -> dict:
    eta3 = toda_eta_family_definition_statement(3).element
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta3))
    candidates = expand_finite_cyclic_relation(goal)
    report = {
        'phase': '165 R12-R24',
        'generic_finite_cyclic_backward_available': len(candidates) == 1,
        'cyclic_subgoal_correct': len(candidates) == 1 and candidates[0].subgoals == (
            CyclicStructureStatement(goal.lhs, eta3, 2),
        ),
        'web_goal_used': repr(goal),
        'web_search_complete': False,
        'web_search_status': 'NOT_RUN',
        'open_goals': [],
        'diagnostics': [],
        'pi43_web_proof_certified': False,
        'full_pytest_run': False,
    }
    try:
        result = search_group_from_registered_goal(n=3, k=1, goal=goal)
        report['web_search_status'] = result.status.value
        report['web_search_complete'] = (
            result.status is ProofSearchStatus.COMPLETE and result.conclusion == goal
            and not result.open_goals
        )
        report['open_goals'] = [repr(x) for x in result.open_goals]
        report['diagnostics'] = list(result.diagnostics)
        report['proven_step_count'] = len(result.proven_steps)
        report['pi43_web_proof_certified'] = report['web_search_complete']
    except (ValueError, TypeError, ImportError) as exc:
        report['web_search_status'] = 'ERROR'
        report['diagnostics'] = [type(exc).__name__ + ': ' + str(exc)]
    report['status'] = ('WEB_CANONICAL_SEARCH_COMPLETE' if report['pi43_web_proof_certified']
                        else 'WEB_SEARCH_STILL_HAS_UNRESOLVED_PREMISES')
    return report


def main() -> None:
    report = run_audit()
    file = Path(__file__).with_name('audit_result.json')
    file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('Audit saved:', file)


if __name__ == '__main__':
    main()
