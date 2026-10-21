"""Read-only audit of 112 Toda group targets and the current DB Goal adapter."""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from math import inf
from pathlib import Path

from phase166_r3af_goal_adapter import database_group_goal_candidates
from repository import SphereRepository


@dataclass(frozen=True)
class GoalAuditRecord:
    n: int
    k: int
    source_n: int | None
    source_kind: str
    orders: tuple[str, ...]
    generators: tuple[str, ...]
    conversion: str
    goal_type: str | None
    explanation: str


def _candidate_result(n: int, k: int, repo: SphereRepository) -> GoalAuditRecord:
    """Classify source data and actual adapter result, without creating evidence."""
    direct = repo.df[(repo.df['n'] == n) & (repo.df['k'] == k)]
    source_n = n if not direct.empty else min(n, k + 2)
    source_rows = direct if not direct.empty else repo.df[(repo.df['n'] == source_n) & (repo.df['k'] == k)]
    source_kind = 'direct' if not direct.empty else ('stable_fallback' if not source_rows.empty else 'missing')
    group = repo.get_group(n, k)
    generators = tuple(str(item.generator) for item in group.components)
    orders = tuple('inf' if item.order == inf else str(item.order) for item in group.components)
    candidates = database_group_goal_candidates(n=n, k=k)
    if len(candidates) == 1:
        conversion = 'typed_goal'
        goal_type = type(candidates[0].rhs).__name__
        explanation = 'DB Goal adapter returned one typed candidate (not a ProofStep)'
    elif len(candidates) > 1:
        conversion = 'ambiguous'
        goal_type = None
        explanation = f'DB Goal adapter returned {len(candidates)} candidates'
    elif not group.components:
        conversion = 'missing'
        goal_type = None
        explanation = 'No source group components'
    elif all(item.order == 0 for item in group.components):
        conversion = 'zero_unhandled'
        goal_type = None
        explanation = 'Zero group needs a typed zero-goal representation'
    else:
        conversion = 'unsupported'
        goal_type = None
        explanation = 'Check generator syntax, sum decomposition, and typed identity before conversion'
    return GoalAuditRecord(n, k, source_n if source_kind != 'missing' else None,
                           source_kind, orders, generators, conversion, goal_type, explanation)


def audit(root: Path) -> dict:
    """Measure all 112 requested pairs (n=2..15, k=0..7)."""
    repo = SphereRepository(root / 'data' / 'sphere.csv')
    records = [_candidate_result(n, k, repo) for n in range(2, 16) for k in range(8)]
    return {
        'phase': '166-3AI-112-goal-audit',
        'read_only': True,
        'count': len(records),
        'source_counts': dict(sorted(Counter(x.source_kind for x in records).items())),
        'conversion_counts': dict(sorted(Counter(x.conversion for x in records).items())),
        'records': [asdict(x) for x in records],
    }


def main() -> None:
    root = Path.cwd()
    if not (root / 'phase166_r3af_goal_adapter.py').is_file():
        raise SystemExit('Run from EHP Proof Tracer repository root')
    payload = audit(root)
    output = root / 'phase166_r3ai_112_goal_audit' / 'results' / 'report.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: payload[key] for key in ('phase', 'count', 'source_counts', 'conversion_counts')}, ensure_ascii=False, indent=2))
    print('REPORT:', output)
    print('NO_PRODUCTION_CODE_MODIFIED; full pytest NOT run')


if __name__ == '__main__':
    main()
