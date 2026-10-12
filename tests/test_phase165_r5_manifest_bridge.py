"""Phase 165 R5: source order must never become proof authorization."""
from dataclasses import replace
import json
from pathlib import Path

import pytest

from phase164_r2_citation_eligibility import (
    EligibilityStatus,
    assess_phase164_r2_citation,
)
from phase165_r5_manifest_bridge import (
    DEFAULT_MANIFEST,
    build_phase165_r5_manifest_bridge,
)
from unified_statement_registry import AssertionOrigin


def test_source_manifest_is_imported_without_proof_promotion():
    bridge, summary = build_phase165_r5_manifest_bridge()
    assert summary.source_reference_count == 108
    assert summary.source_assertion_count == 117
    assert summary.newly_eligible_count == 0
    archive = tuple(a for a in bridge.registry._assertions.values()
                    if a.origin is AssertionOrigin.SOURCE_ARCHIVE)
    assert len(archive) == 117
    assert all(a.available_after_position is None for a in archive)


def test_archive_citation_is_denied_even_if_reviewed():
    bridge, _ = build_phase165_r5_manifest_bridge()
    archive_id = next(a.assertion_id for a in bridge.registry._assertions.values()
                      if a.origin is AssertionOrigin.SOURCE_ARCHIVE)
    citing_id = next(a.assertion_id for a in bridge.registry._assertions.values()
                     if a.origin is AssertionOrigin.FIXED_STATEMENT)
    result = assess_phase164_r2_citation(
        bridge, archive_id, citing_id,
        verified_assertion_ids=(archive_id,),
    )
    assert result.status is EligibilityStatus.DENIED
    assert not result.usable


def test_corrupted_manifest_rejected(tmp_path: Path):
    data = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8-sig"))
    data["assertions"][0]["source_text"] += " altered"
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        build_phase165_r5_manifest_bridge(path)


def test_eligibility_flag_cannot_be_overridden(tmp_path: Path):
    data = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8-sig"))
    data["proof_eligible_count"] = 1
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="contract invalid"):
        build_phase165_r5_manifest_bridge(path)
