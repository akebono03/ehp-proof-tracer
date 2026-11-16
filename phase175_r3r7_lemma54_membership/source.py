"""Read-only verification of Toda Lemma 5.4 before Lemma 5.7.

The adopted Chapter V transcription has a pinned reviewed Git blob. The
original printed edition has not been independently checked. No conclusion
about pi_7^3 or E(eta_2 nu-prime) is registered as a GIVEN here.
"""
from __future__ import annotations

import json
from pathlib import Path

from phase173_r4_r1_lemma54_source_bridge.source import (
    DOUBLE_TEXT,
    HOPF_TEXT,
    MEMBERSHIP_TEXT,
    SOURCE_ID as LEMMA54_SOURCE_ID,
    TodaLemma54TypedSource,
    validate_lemma54_text,
)
from phase175_r3r5_pi73_lemma57_frontier.source import verify_reviewed_toda_source
from phase175_r3r6_lemma57_general.source import verify_lemma57_manifest

MANIFEST = Path("phase163_r4_r94_output/manifest.json")
CHAPTER = Path("sources/toda/Toda_05_2.tex")
LEMMA54_SHA256 = "30f72eb36033b069ca814d409d87a4195569c28f50b31501bf3599999e185faa"
LEMMA54_POSITION = 8300
LEMMA57_POSITION = 9100
PROPOSITION58_POSITION = 9200


def verify_lemma54_before_lemma57(root: Path) -> dict[str, object]:
    """Verify the entire existing typed Lemma 5.4, source and citation order."""
    root = Path(root)
    source_evidence = verify_reviewed_toda_source(root)
    source = (root / CHAPTER).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    validate_lemma54_text(source)
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8-sig"))
    if manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST":
        raise ValueError("R3R7 unexpected source-manifest mode")
    assertions = manifest.get("assertions")
    if not isinstance(assertions, list):
        raise ValueError("R3R7 source assertions missing")
    expected = (
        ("toda:Lemma 5.4", LEMMA54_SOURCE_ID, LEMMA54_SHA256, LEMMA54_POSITION),
        ("toda:Lemma 5.7", "toda:tex:ch5:0015",
         "01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c",
         LEMMA57_POSITION),
        ("toda:Proposition 5.8", "toda:tex:ch5:0016",
         "4e41470cead5382bc042b39634ae4bbc9bc184cda06801ddafa1331be6f0d124",
         PROPOSITION58_POSITION),
    )
    selected: dict[str, dict] = {}
    for reference_id, statement_id, sha256, position in expected:
        matches = [item for item in assertions if item.get("reference_id") == reference_id]
        if len(matches) != 1:
            raise ValueError("R3R7 missing or ambiguous literature reference: " + reference_id)
        row = matches[0]
        if (row.get("statement_id") != statement_id
                or row.get("source_sha256") != sha256
                or row.get("publication_position") != position
                or row.get("review_needed") is not False):
            raise ValueError("R3R7 unreviewed or reordered citation: " + reference_id)
        selected[reference_id] = row
    actual_lemma = selected["toda:Lemma 5.4"]["source_text"]
    validate_lemma54_text(actual_lemma)
    if any(term not in actual_lemma for term in (DOUBLE_TEXT, HOPF_TEXT, MEMBERSHIP_TEXT)):
        raise ValueError("R3R7 Lemma 5.4 double-suspension source clause absent")
    if actual_lemma not in source:
        raise ValueError("R3R7 manifest lemma is not a literal source passage")
    verify_lemma57_manifest(root)
    if not LEMMA54_POSITION < LEMMA57_POSITION < PROPOSITION58_POSITION:
        raise ValueError("R3R7 unexpected literature order")
    return {
        "source_blob": source_evidence["source_blob"],
        "lemma54_statement_id": LEMMA54_SOURCE_ID,
        "lemma54_source_sha256": LEMMA54_SHA256,
        "lemma54_position": LEMMA54_POSITION,
        "lemma57_position": LEMMA57_POSITION,
        "proposition58_position": PROPOSITION58_POSITION,
        "printed_edition_independently_checked": False,
        "new_specific_given": 0,
        "new_production_source": 0,
        "source_statement": repr(TodaLemma54TypedSource()),
    }
