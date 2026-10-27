"""Production-facing audit of adopted prior DB policy, never inventing proofs."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step, exact_prior_database_result, group_coordinates,
)

HERE = Path(__file__).resolve().parent
CASES = ((14, 7), (15, 7), (8, 4), (8, 6), (15, 8), (15, 9))


def main() -> None:
    bridge = build_shared_typed_bridge()
    items = []
    for n, k in CASES:
        from phase165_r55_nk_only_goal import registered_group_goal_candidates
        from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
        zero = database_zero_group_goal_candidates(n=n, k=k)
        goals = zero or registered_group_goal_candidates(bridge, n=n, k=k)
        base = exact_prior_database_result(k + 2, k)
        candidate = admitted_db_step(base, proof_target=goals[0], bridge=bridge) if base is not None and len(goals) == 1 else None
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        entry = dict(n=n, k=k, group=f"pi_{n+k}^{n}", status=result.status.value,
                     stable_base=f"pi_{2*k+2}^{k+2}",
                     base_db_explicit=base is not None,
                     db_prior_admitted=candidate is not None,
                     accepted_proof_steps=len(result.proven_steps),
                     open_goals=len(result.open_goals),
                     diagnostics=list(result.diagnostics),
                     db_antecedents=[
                         dict(coords=group_coordinates(step.conclusion), note=step.note)
                         for step in result.proven_steps
                         if step.note == "ADOPTED_DATABASE_PRIOR; independent reference not asserted"
                     ])
        print(f"R10E4_{entry['group']}_BASE_DB={entry['base_db_explicit']}")
        print(f"R10E4_{entry['group']}_PRIOR_ADMITTED={entry['db_prior_admitted']}")
        print(f"R10E4_{entry['group']}_STATUS={entry['status']}")
        items.append(entry)
    regressions = []
    for n,k in ((8,1),(8,2),(8,3)):
        result=search_group_from_registered_goal(n=n,k=k,bridge=bridge)
        regressions.append(dict(n=n,k=k,status=result.status.value))
        print(f"R10E4_PI_{n+k}^{n}_REGRESSION={result.status.value}")
    if any(x['status']!='complete' for x in regressions):
        raise RuntimeError('previous 1/2/3 stem result regressed')
    report={"phase":"169 R10E4","order":"(source_k,source_n)<(target_k,target_n)",
            "provenance":"adopted prior DB data; not a Toda fixed theorem",
            "results":items,"regressions":regressions,"full_pytest_run":False}
    output=HERE/"output"
    output.mkdir(exist_ok=True)
    (output/"audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Phase 169 R10E4 — DB の先行群構造監査", "", "辞書式順序 `(k,n)` を採用。文献掲載順序とは別の基準。", "", "| 群 | 基点 DB | 採用可能 | 探索 |", "|---|---|---|---|"]
    for item in items:
        lines.append(f"| {item['group']} | {item['base_db_explicit']} | {item['db_prior_admitted']} | {item['status']} |")
    lines.extend(["", "DB 結果を使う証明は、DB 群構造を既知の前提とする条件付き証明。", "全体 pytest は実行しない。", ""])
    (output/"audit.md").write_text("\n".join(lines),encoding="utf-8")
    print("R10E4_AUDIT="+str(output/"audit.json"))
    print("R10E4_FULL_PYTEST_RUN=False")


if __name__ == '__main__':
    main()
