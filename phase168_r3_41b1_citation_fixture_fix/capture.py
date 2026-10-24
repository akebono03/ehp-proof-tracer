"""Capture four existing completed Narratives without changing the renderer."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from phase168_r3_38_frozen_fulltext_audit.audit import capture

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1),
         ("pi5_4", 4, 1), ("pi6_5", 5, 1))


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("before", "after"):
        raise SystemExit("Usage: python -m phase168_r3_41b1_citation_fixture_fix.capture before|after")
    stage = sys.argv[1]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = []
    for name, n, k in CASES:
        markdown, model, view = capture(n, k)
        encoded = markdown.encode("utf-8")
        path = OUTPUT / f"{name}_{stage}.md"
        path.write_bytes(encoded)
        entry = {
            "case": name,
            "sha256": hashlib.sha256(encoded).hexdigest(),
            "steps": len(model.steps),
            "references": len(model.citations),
            "complete": not view.partial_result,
        }
        if not entry["complete"]:
            raise AssertionError(f"{name} unexpectedly partial")
        report.append(entry)
        print(stage, name, "steps", len(model.steps), "refs", len(model.citations))
    (OUTPUT / f"{stage}.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
