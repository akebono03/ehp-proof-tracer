"""DryRun-compatible verifier of the unchanged cited Toda source and order."""
from __future__ import annotations

from phase174_r3_r6_source_extension.source import verify_extension_texts


def main() -> int:
    positions = dict(verify_extension_texts())
    print("PHASE174_R3R6_TODA48_SOURCE_POSITION=" + str(positions["(4.8)"]))
    print("PHASE174_R3R6_TODA55_SOURCE_POSITION=" + str(positions["(5.5)"]))
    print("PHASE174_R3R6_SOURCE_TEXT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
