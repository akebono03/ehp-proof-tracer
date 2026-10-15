"""Compare exact completed/partial markdown before/after the guarded install."""
from __future__ import annotations

import json
from pathlib import Path
import sys

from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def snapshot() -> dict[str, str]:
    complete = search_group_from_registered_goal(n=2, k=1)
    partial = search_group_from_registered_goal(n=3, k=1)
    return {
        "completed_public": render_partial_proof_markdown(complete),
        "completed_adapter": render_completed_shared_narrative(complete),
        "incomplete_public": render_partial_proof_markdown(partial),
    }


def main() -> None:
    mode, filename = sys.argv[1:]
    path = Path(filename)
    values = snapshot()
    if mode == "before":
        path.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf8")
        print("R3 baseline saved")
    elif mode == "after":
        baseline = json.loads(path.read_text(encoding="utf8"))
        if baseline != values:
            changed = [key for key in values if baseline.get(key) != values[key]]
            raise AssertionError(f"Narrative regression: {changed}")
        print("R3 exact completed/partial Narrative parity confirmed")
    else:
        raise ValueError("expected before or after")


if __name__ == "__main__":
    main()
