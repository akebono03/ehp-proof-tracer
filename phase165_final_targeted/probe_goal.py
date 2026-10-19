"""Read-only goal search probe; outputs actual partial/complete state."""
from __future__ import annotations

import json
import sys
import traceback


def main() -> int:
    n, k = map(int, sys.argv[1:3])
    try:
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        result = search_group_from_registered_goal(n=n, k=k)
        status = getattr(result, 'status', None)
        name = getattr(status, 'name', str(status))
        steps = getattr(result, 'proven_steps', ())
        open_goals = getattr(result, 'open_goals', ())
        conclusion = getattr(result, 'conclusion', None)
        diagnostics = getattr(result, 'diagnostics', ())
        payload = {'group': f'pi_{n+k}^{n}', 'status': name,
                   'proven_step_count': len(steps), 'open_goal_count': len(open_goals),
                   'conclusion': str(conclusion),
                   'diagnostics': [str(x) for x in diagnostics],
                   'proof_verified': False}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        # A search result is an observation, not yet a proof integrity certification.
        return 0 if name == 'COMPLETE' and not open_goals and conclusion is not None else 2
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
