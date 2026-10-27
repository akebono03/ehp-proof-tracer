"""Focused source-first audit: report goals, evidence and completion separately."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates, search_group_from_registered_goal,
)
from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase169_r10e1_general_group_transport.transport import (
    _goal_group, _components, generator_images_for_group_transport,
)
from proof import ProofRule, Relation

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
REGRESSIONS = ((8, 1), (8, 2), (8, 3))
CASES = ((8, 4), (8, 6), (15, 7), (15, 8), (15, 9))


def describe_goal(bridge, n: int, k: int) -> dict:
    zero = database_zero_group_goal_candidates(n=n, k=k)
    goals = zero if zero else registered_group_goal_candidates(bridge, n=n, k=k)
    found = []
    for goal in goals:
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
        group = _goal_group(goal)
        prior = []
        for link in screened.proof_links:
            if link.step is None or link.step.rule is not ProofRule.GIVEN:
                continue
            source = link.step.conclusion
            source_group = _goal_group(source)
            if (source_group is None or group is None
                    or not all(type(x) is int for x in (
                        source_group.group_dimension, source_group.sphere_dimension,
                        group.group_dimension, group.sphere_dimension,
                    ))):
                continue
            if (source_group.group_dimension - source_group.sphere_dimension
                    != group.group_dimension - group.sphere_dimension):
                continue
            if source_group.sphere_dimension >= group.sphere_dimension:
                continue
            images = generator_images_for_group_transport(source, goal)
            prior.append({
                'source': f'pi_{source_group.group_dimension}^{source_group.sphere_dimension}',
                'assertion_id': link.assertion_id,
                'images_possible': images is not None,
                'image_goal_count': len(images) if images is not None else None,
            })
        result = search_group_from_registered_goal(n=n, k=k, goal=goal, bridge=bridge)
        found.append({
            'goal_kind': 'zero' if isinstance(goal, TodaPrimaryGroupZeroStatement)
                         else type(goal.rhs).__name__ if isinstance(goal, Relation)
                         else type(goal).__name__,
            'screened_source_count': len(screened.proof_links),
            'suitable_prior_source_candidates': prior,
            'status': result.status.value,
            'open_goal_count': len(result.open_goals),
            'proof_step_count': len(result.proven_steps),
        })
    return {'group': f'pi_{n+k}^{n}', 'goals': found}


def main() -> None:
    bridge = build_shared_typed_bridge()
    regressions = []
    for n, k in REGRESSIONS:
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        case = {'group': f'pi_{n+k}^{n}', 'status': result.status.value}
        regressions.append(case)
        print('R10E2_' + case['group'] + '_STATUS=' + case['status'])
    if any(x['status'] != 'complete' for x in regressions):
        raise RuntimeError('R10E2 regressed a completed 1-, 2-, or 3-stem group')
    boundaries = [describe_goal(bridge, n, k) for n, k in CASES]
    for case in boundaries:
        info = case['goals']
        statuses = ','.join(x['status'] for x in info) if info else 'no_goal'
        candidates = sum(len(x['suitable_prior_source_candidates']) for x in info)
        print('R10E2_' + case['group'] + '_STATUS=' + statuses)
        print('R10E2_' + case['group'] + '_POSITIONED_SOURCE_COUNT=' + str(candidates))
    result = {
        'phase': '169 R10E2',
        'head': subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,
                               text=True,capture_output=True,check=True).stdout.strip(),
        'kind': 'FOCUSED_IMPLEMENTATION_AUDIT',
        'regressions': regressions,
        'boundaries': boundaries,
        'target_publication_position_invented': False,
        'mathematical_proof_from_csv': False,
        'full_pytest_run': False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / 'audit.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    print('R10E2_AUDIT=' + str(path))
    print('R10E2_FULL_PYTEST_RUN=False')


if __name__ == '__main__':
    main()
