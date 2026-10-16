"""Read-only comparison of canonical proof reconstruction with root candidates."""
from __future__ import annotations

import json
from pathlib import Path


def same(a: object, b: object) -> bool:
    return type(a) is type(b) and a == b


def classify(error: str | None, proved: int, root_proved: bool) -> str:
    if root_proved:
        return 'CANONICAL_COMPLETE'
    if error is None:
        return 'NO_RESULT'
    if 'cyclic proof dependency' in error:
        return 'CYCLE'
    if 'expected one registered derivation' in error:
        return 'UNRESOLVED_OR_AMBIGUOUS'
    return 'EXCEPTION'


def compare(bridge, provider, goal, citing_assertion_id: str) -> dict:
    from phase165_r3_recursive_search import reconstruct_registered_goal, RegisteredGoalUnresolved
    from proof import ProofStep

    roots = provider(goal)
    rows = []
    for selected in [None] + list(range(len(roots))):
        events = []
        calls = {'count': 0}
        def observer(kind, target, step):
            events.append({'event': kind, 'goal': repr(target),
                           'step_rule': str(step.rule) if isinstance(step, ProofStep) else None})
        def filtered(target):
            calls['count'] += 1
            if same(target, goal) and selected is not None:
                return (roots[selected],)
            return provider(target)
        error = None
        step = None
        try:
            step = reconstruct_registered_goal(
                goal, bridge, citing_assertion_id, filtered,
                lookup_mode='typed_reference', progress_observer=observer,
            )
        except RegisteredGoalUnresolved as exc:
            error = str(exc)
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
        rows.append({
            'path': 'ALL_ROOTS' if selected is None else f'ROOT_{selected+1}',
            'root_rule': None if selected is None else getattr(roots[selected].rule, 'name', repr(roots[selected].rule)),
            'subgoals': [] if selected is None else [repr(s) for s in roots[selected].subgoals],
            'status': classify(error, len(events), step is not None),
            'canonical_root_step': step is not None,
            'error': error,
            'provider_calls': calls['count'],
            'proved_observations': sum(x['event'] == 'proved' for x in events),
            'unresolved_observations': sum(x['event'] == 'unresolved' for x in events),
            'events': events[:100],
        })
    return {
        'status': 'CANONICAL_RECONCILIATION_AUDITED',
        'root_candidate_count': len(roots),
        'results': rows,
        'interpretation_note': 'UNRESOLVED_OR_AMBIGUOUS aggregates zero and multiple derivations; consult error and proof events.',
        'production_modified': False,
        'full_pytest_run': False,
    }


def markdown(report: dict) -> str:
    lines = ['# π₄³ 正規探索・ルート候補照合', '',
             f"Root Candidate 数: {report['root_candidate_count']}", '',
             '| 経路 | 規則 | 正規探索 | ProofStep 観測 | 未解決 |',
             '|---|---|---|---:|---:|']
    for row in report['results']:
        lines.append(f"| {row['path']} | {row['root_rule'] or '全候補'} | {row['status']} | {row['proved_observations']} | {row['unresolved_observations']} |")
    lines.extend(['', '## 正規探索の失敗情報', ''])
    for row in report['results']:
        lines.append(f"- {row['path']}: `{row['error']}`")
    lines.extend(['', '## 限界',
                  '- `FORWARD_PASS` はこの監査の正規一意性判定とは別です。',
                  '- 各候補単独の実行でも、下位 Goal は元の共通 Provider を使います。',
                  '- 型付き Reference の厳格な一致を使い、未確認の文献を追加しません。',
                  '- 公開 Renderer はこの監査の対象外です。', ''])
    return '\n'.join(lines)


def main() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup
    from expression import HomotopyElement, GeneratorSymbol
    from proof import Relation, RelationType

    goal = Relation(
        TodaPrimaryGroup(4, 3),
        FiniteCyclicGroup(2, HomotopyElement(
            name='η_3', dimension=3, source=4, target=3,
            generator=GeneratorSymbol('η', 3))),
        RelationType.EQUALITY,
    )
    bridge = build_shared_typed_bridge()
    provider = shared_expansion_provider(bridge)
    ids = tuple(bridge.registry._assertions)
    if not ids:
        raise ValueError('No assertions in typed bridge')
    report = compare(bridge, provider, goal, ids[0])
    directory = Path(__file__).resolve().parent / 'audit_output'
    directory.mkdir(exist_ok=True)
    (directory / 'canonical_reconciliation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (directory / 'canonical_reconciliation.md').write_text(markdown(report), encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'interpretation_note'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
