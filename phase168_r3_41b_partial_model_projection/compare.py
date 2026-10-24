"""Fail if R3-41B changes any of the four completed Narratives."""
from __future__ import annotations

import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
CASES = ("pi3_2", "pi4_3", "pi5_4", "pi6_5")


def main() -> None:
    before = json.loads((OUTPUT / "before.json").read_text(encoding="utf-8"))
    after = json.loads((OUTPUT / "after.json").read_text(encoding="utf-8"))
    if before != after:
        raise AssertionError("Completed proof model metadata changed")
    for name in CASES:
        original = (OUTPUT / f"{name}_before.md").read_bytes()
        current = (OUTPUT / f"{name}_after.md").read_bytes()
        if original != current:
            raise AssertionError(f"Completed Narrative changed: {name}")
    (OUTPUT / "comparison.json").write_text(
        json.dumps({"cases": list(CASES), "byte_identical": True,
                    "whole_pytest_executed": False}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("FOUR_COMPLETED_NARRATIVES_BYTE_IDENTICAL")


if __name__ == "__main__":
    main()
