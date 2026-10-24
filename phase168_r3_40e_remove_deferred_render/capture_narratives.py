"""Capture four actual web Narratives before/after a Renderer-only cleanup."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from phase168_r3_38_frozen_fulltext_audit.audit import capture
from phase168_r3_29_order_projection import project_narrative_order

OUTPUT = Path(__file__).resolve().parent / "output"
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1),
         ("pi5_4", 4, 1), ("pi6_5", 5, 1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("before", "after"))
    mode = parser.parse_args().mode
    OUTPUT.mkdir(exist_ok=True)
    results = []
    for name, n, k in CASES:
        narrative, model, _ = capture(n, k)
        entries = project_narrative_order(model)
        if any(entry.after_indices for entry in entries):
            raise AssertionError(f"Deferred indices remain in projection: {name}")
        indices = [entry.step_index for entry in entries]
        if sorted(indices) != list(range(len(model.steps))):
            raise AssertionError(f"Missing/duplicate proof steps: {name}")
        path = OUTPUT / (name + "_" + mode + ".md")
        path.write_text(narrative, encoding="utf-8")
        results.append({"case": name,
                        "sha256": hashlib.sha256(narrative.encode("utf-8")).hexdigest(),
                        "steps": len(model.steps),
                        "citations": len(model.citations)})
    if mode == "after":
        previous = json.loads((OUTPUT / "before.json").read_text(encoding="utf-8"))
        if results != previous:
            raise AssertionError(f"Narrative output changed after no-op Renderer cleanup: {results} != {previous}")
        for name, _, _ in CASES:
            before = (OUTPUT / (name + "_before.md")).read_bytes()
            after = (OUTPUT / (name + "_after.md")).read_bytes()
            if before != after:
                raise AssertionError(f"Narrative content changed for {name}")
    (OUTPUT / (mode + ".json")).write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in results:
        print(mode, row["case"], "steps", row["steps"], "refs", row["citations"],
              "unchanged" if mode == "after" else "captured")
    if mode == "after":
        print("ALL FOUR NARRATIVES BYTE-IDENTICAL")


if __name__ == "__main__":
    main()
