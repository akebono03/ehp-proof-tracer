"""Read-only source check before any production code changes."""
from __future__ import annotations

from phase165_r52_r27_r5_literature import verify_prop44_hopf_fibration_source
from phase174_r3_r6_r2_prop44_lemma54.source import verify_prelude_source
from phase173_r4_r1_lemma54_source_bridge.source import validate_lemma54_text
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    verify_prop44_hopf_fibration_source()
    rank = verify_prelude_source()
    chapter = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    validate_lemma54_text(chapter)
    print("PHASE174_R3R6R2_PRELUDE_POSITION=" + str(rank))
    print("PHASE174_R3R6R2_LEMMA54_SOURCE=PASS")
    print("PHASE174_R3R6R2_SOURCE_TEXT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
