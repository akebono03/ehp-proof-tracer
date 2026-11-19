"""Observe the real public search after the shared zero transport was connected."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus


def inspect_public_target() -> dict[str, object]:
    """Return the actual search state, never manufacture a completed proof."""
    contexts: list[object] = []
    result = search_group_from_registered_goal(n=6, k=4, context_sink=contexts.append)
    state = getattr(result.status, "value", str(result.status))
    complete = result.status is ProofSearchStatus.COMPLETE
    return {
        "target": "pi_10^6",
        "status": state,
        "complete": complete,
        "conclusion": str(result.conclusion) if result.conclusion is not None else None,
        "open_goals": [str(item) for item in result.open_goals],
        "proven_steps": len(result.proven_steps),
        "references": len(result.references),
        "new_given": 0,
        "full_pytest": False,
    }


def main() -> int:
    inspected = inspect_public_target()
    dest = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "EHP_Phase175_R4R14R5_public_search.json"
    dest.write_text(json.dumps(inspected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R14R5_SEARCH_STATUS=" + str(inspected["status"]))
    print("PHASE175_R4R14R5_OPEN_GOALS=" + str(len(inspected["open_goals"])))
    print("PHASE175_R4R14R5_PROVEN_STEPS=" + str(inspected["proven_steps"]))
    print("PHASE175_R4R14R5_REPORT=" + str(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
