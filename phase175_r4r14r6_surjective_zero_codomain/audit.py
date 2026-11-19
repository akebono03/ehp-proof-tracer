"""Actual search observation; a connected rule is not a completed proof."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase175_r4r14r6_surjective_zero_codomain.rule import RULE_NAME


def inspect_public_search() -> dict[str, object]:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    options = tuple(shared_expansion_provider(bridge, proof_target=root)(root))
    matches = tuple(option for option in options if option.rule.name == RULE_NAME)
    if len(matches) != 1:
        raise RuntimeError("SHARED_ROOT_ZERO_BRANCH_MISSING_OR_DUPLICATE")
    result = search_group_from_registered_goal(n=6, k=4)
    return {
        "target": "pi_10^6",
        "new_root_expansion": RULE_NAME,
        "new_root_subgoals": [str(x) for x in matches[0].subgoals],
        "root_proposal_count": len(options),
        "search_status": getattr(result.status, "value", str(result.status)),
        "proven_steps": len(result.proven_steps),
        "references": len(result.references),
        "open_goals": [str(x) for x in result.open_goals],
        "root_conclusion": str(result.conclusion) if result.conclusion is not None else None,
        "new_given": 0,
        "full_pytest": False,
    }


def main() -> int:
    report = inspect_public_search()
    path = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "EHP_Phase175_R4R14R6_search.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R14R6_NEW_ROOT_OPTIONS=1")
    print("PHASE175_R4R14R6_SEARCH_STATUS=" + report["search_status"])
    print("PHASE175_R4R14R6_PROVEN_STEPS=" + str(report["proven_steps"]))
    print("PHASE175_R4R14R6_OPEN_GOALS=" + str(len(report["open_goals"])))
    print("PHASE175_R4R14R6_REPORT=" + str(path))
    print("PHASE175_R4R14R6_COMPLETE_CLAIMED=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
