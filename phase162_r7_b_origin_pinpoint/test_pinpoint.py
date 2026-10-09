"""Lightweight structural checks for the read-only R7-B pinpoint tool."""
from pinpoint import SUSPECTS, build_report


def test_r7_b_pinpoint_tracks_required_suspects():
    assert "stable_tail" in SUSPECTS
    assert "eta_square_issue" in SUSPECTS
    assert "repeated_delta" in SUSPECTS
    assert "bare_exactness_intro" in SUSPECTS


def test_r7_b_pinpoint_does_not_require_mutating_root():
    import inspect
    from pinpoint import capture_public_stages
    code = inspect.getsource(capture_public_stages)
    assert "finally:" in code
    assert "setattr(public_renderer, name, original)" in code
