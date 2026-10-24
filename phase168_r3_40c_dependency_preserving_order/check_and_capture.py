"""Check four-group premise order and capture post-patch narrative outputs."""
from __future__ import annotations

import json
from pathlib import Path

from phase168_r3_38_frozen_fulltext_audit.audit import capture
from phase168_r3_29_order_projection import project_narrative_order

OUT = Path(__file__).resolve().parent / "output"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    summary = []
    for label, n, k in (("pi3_2", 2, 1), ("pi4_3", 3, 1),
                        ("pi5_4", 4, 1), ("pi6_5", 5, 1)):
        markdown, model, _ = capture(n, k)
        (OUT / (label + "_current.md")).write_text(markdown, encoding="utf-8")
        order = project_narrative_order(model)
        visible = [i for entry in order
                   for i in (entry.step_index, *entry.after_indices)]
        position = {i: j for j, i in enumerate(visible)}
        inversion = []
        for child_index, step in enumerate(model.steps):
            for premise in step.premises:
                matches = [i for i, parent in enumerate(model.steps) if parent is premise]
                if not matches:
                    matches = [i for i, parent in enumerate(model.steps) if parent == premise]
                if not matches or position[matches[0]] >= position[child_index]:
                    inversion.append((matches[0] if matches else None, child_index))
        if inversion:
            raise AssertionError(f"Proof dependencies inverted: {label}: {inversion}")
        summary.append({"case": label, "step_count": len(model.steps),
                        "dependency_inversions": inversion,
                        "source_references": len(model.citations),
                        "order": visible})
        print(label, "steps", len(model.steps), "inversions", len(inversion))
    (OUT / "dependency_order.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REPORT:", OUT / "dependency_order.json")


if __name__ == "__main__":
    main()
