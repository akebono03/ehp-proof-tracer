"""The R53 public patch and the actual HTTP/Renderer files must match review."""
from __future__ import annotations

from phase174_r3_r7_r54_public_http_narrative_audit.source_guard import (
    PINNED_WEB_BLOBS, verify_checkout,
)


def test_reviewed_source_guard_allows_only_installed_r53() -> None:
    report = verify_checkout()
    assert report["source_guard"] == "PASS"
    assert report["r53_public_wiring_installed"] is True
    assert report["production_files_changed_by_r54"] == 0
    assert report["new_given"] == 0
    assert report["new_math_rules"] == 0


def test_fixed_pins_include_http_template_renderer_and_trust_gate() -> None:
    assert len(PINNED_WEB_BLOBS) == 8
    assert "web_app.py" in PINNED_WEB_BLOBS
    assert "templates/index.html" in PINNED_WEB_BLOBS
    assert "phase168_r3_5_model_renderer.py" in PINNED_WEB_BLOBS
    assert "phase168_r3_41p13_trust_boundary/verification.py" in PINNED_WEB_BLOBS
    assert all(len(value) == 40 for value in PINNED_WEB_BLOBS.values())
