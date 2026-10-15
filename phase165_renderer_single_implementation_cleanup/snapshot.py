"""Compare exact public Markdown before/after the renderer implementation cleanup."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def snapshot() -> dict[str, str]:
    completed = search_group_from_registered_goal(n=2, k=1)
    partial = search_group_from_registered_goal(n=3, k=1)
    return {
        "pi3_2_completed": render_completed_shared_narrative(completed),
        "pi4_3_partial": render_partial_proof_markdown(partial),
    }


def main() -> None:
    mode, path_text = sys.argv[1:]
    path = Path(path_text)
    values = snapshot()
    if mode == "before":
        path.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf8")
        print("Saved pre-install complete/partial Narrative baselines")
    elif mode == "after":
        before = json.loads(path.read_text(encoding="utf8"))
        for key, value in values.items():
            if before.get(key) != value:
                raise AssertionError("Narrative changed: " + key)
        print("Complete and partial Narrative Markdown identical to pre-install outputs")
    else:
        raise ValueError("mode must be before or after")


if __name__ == "__main__":
    main()
