"""Production-facing proof/status audit, with no invented completion claims."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e1_general_group_transport.transport import (
    _zero_citing_assertion_id,
    expand_prior_general_group_transport,
)
from proof import ProofRule, Relation

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / 'output'
GOALS = ((8, 4), (8, 6), (15, 7), (15, 8), (15, 9))


def inspect_goal(bridge, n: int, k: int) -> dict:
    zero_goals = database_zero_group_goal_candidates(n=n, k=k)
    relation_goals = registered_group_goal_candidates(bridge, n=n, k=k)
    goals = zero_goals if zero_goals else relation_goals
    report = {
        'target': f'pi_{n+k}^{n}',
        'shapes': [],
        'citation_resolved': False,
        'candidate_count': None,
        'reason': 'no_typed_goal' if not goals else 'not_a_cited_target',
    }
    for goal in goals:
        shape = 'zero' if isinstance(goal, TodaPrimaryGroupZeroStatement) else (
            type(goal.rhs).__name__ if isinstance(goal, Relation) else type(goal).__name__
        )
        report['shapes'].append(shape)
        citing_id = (
            _zero_citing_assertion_id(bridge, goal)
            if isinstance(goal, TodaPrimaryGroupZeroStatement)
            else resolve_specialized_goal_citing_id(bridge, goal)
        )
        if citing_id is None:
            continue
        report['citation_resolved'] = True
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing_id,
            explicit_publication_target=True,
        )
        available = tuple(
            link.step.conclusion for link in screened.proof_links
            if link.step is not None and link.step.rule is ProofRule.GIVEN
        )
        # This is a candidate count, not a completed proof.
        options = expand_prior_general_group_transport(
            goal, available, screened, proof_target=goal,
        )
        report['candidate_count'] = len(options)
        report['reason'] = 'typed_candidates_only' if options else 'no_eligible_transport_candidate'
        provider = shared_expansion_provider(screened, proof_target=goal)
        report['provider_option_count'] = len(provider(goal))
    return report


def main() -> None:
    bridge = build_shared_typed_bridge()
    regressions = []
    for n, k in ((8, 1), (8, 2), (8, 3)):
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        case = {'group': f'pi_{n+k}^{n}', 'status': result.status.value,
                'proof_steps': len(result.proven_steps),
                'open_goals': len(result.open_goals)}
        regressions.append(case)
        print(f'R10E1_{case["group"]}_STATUS={case["status"]}')
    if any(case['status'] != 'complete' for case in regressions):
        raise RuntimeError('R10E1 regressed a previously complete 1-, 2- or 3-stem proof')
    boundaries = [inspect_goal(bridge, n, k) for n, k in GOALS]
    for case in boundaries:
        print('R10E1_' + case['target'] + '_CITATION_RESOLVED=' + str(case['citation_resolved']))
        print('R10E1_' + case['target'] + '_CANDIDATE_COUNT=' + str(case['candidate_count']))
    report = {
        'phase': '169 R10E1',
        'branch': 'develop',
        'head': subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.strip(),
        'limited_regressions': regressions,
        'group_shapes': boundaries,
        'data_is_not_a_proof': True,
        'unresolved_citation_is_not_missing_math': True,
        'full_pytest_run': False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / 'audit.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    lines = [
        '# Phase 169 R10E1 — 共通群構造輸送監査', '',
        '群構造に依存しない型付き輸送の検証。DB は証明ではない。', '',
        '| 群 | Goal の形 | 引用境界 | 候補数 |', '|---|---|---|---:|',
    ]
    for case in boundaries:
        count = 'not checked' if case['candidate_count'] is None else str(case['candidate_count'])
        lines.append(f"| {case['target']} | {', '.join(case['shapes'])} | "
                     f"{'resolved' if case['citation_resolved'] else 'unresolved'} | {count} |")
    lines.extend(['', '未解決の引用は、文献命題の数学的不在を意味しない。',
                  '全体 pytest は未実行。', ''])
    (OUTPUT / 'audit.md').write_text('\n'.join(lines), encoding='utf-8')
    print('R10E1_AUDIT=' + str(OUTPUT / 'audit.json'))
    print('R10E1_FULL_PYTEST_RUN=False')


if __name__ == '__main__':
    main()
