"""Capture byte-exact public narratives and citation identities before/after."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from phase168_r3_38_frozen_fulltext_audit.audit import capture

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1))


def snapshot(name: str, n: int, k: int, folder: Path) -> None:
    rendered, model, _ = capture(n, k)
    content = rendered.encode("utf-8")
    (folder / f"{name}.md").write_bytes(content)
    meta = {
        "n": n,
        "k": k,
        "proof_step_count": len(model.steps),
        "reference_count": len(model.citations),
        "sha256": hashlib.sha256(content).hexdigest(),
        "step_citation_numbers": model.step_citation_numbers,
        "citations": [
            {
                "number": item.number,
                "label": item.reference.label,
                "locator": item.reference.locator,
                "assertion_ids": item.assertion_ids,
                "reference_ids": item.reference_ids,
                "statement_bodies": item.statement_bodies,
                "step_indices": item.step_indices,
            } for item in model.citations
        ],
    }
    (folder / f"{name}.json").write_text(
        json.dumps(meta, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("before", "after"):
        raise SystemExit("Usage: python snapshot.py before|after")
    stage = sys.argv[1]
    folder = OUTPUT / stage
    folder.mkdir(parents=True, exist_ok=True)
    for name, n, k in CASES:
        snapshot(name, n, k, folder)
        if stage == "after":
            for extension in ("md", "json"):
                current = (folder / f"{name}.{extension}").read_bytes()
                baseline_path = OUTPUT / "before" / f"{name}.{extension}"
                if current != baseline_path.read_bytes():
                    raise AssertionError(f"{name} {extension} changed across trust boundary")
        print(stage.upper(), name, "FULLTEXT_REFERENCE_CITATION", "UNCHANGED" if stage == "after" else "SAVED")


if __name__ == "__main__":
    main()
