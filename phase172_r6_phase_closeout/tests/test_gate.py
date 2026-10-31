"""Pure closeout guards; no full pytest or Web search in these unit tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase172_r6_phase_closeout.audit import (
    FULL_PYTEST_COMMAND,
    TARGETS,
    check_pi63_markdown,
    count_passed_summary,
    normalized,
    renderer_state,
)


def test_active_suite_targets_only_tests_directory():
    assert FULL_PYTEST_COMMAND[-1] == "tests"
    assert FULL_PYTEST_COMMAND.count("tests") == 1
    assert TARGETS == ((2, 1), (3, 1), (3, 2), (4, 2), (3, 3))


def test_normalize_crlf_equivalence_and_reject_mixed_newline():
    assert normalized(b"one\r\ntwo\r\n") == "one\ntwo\n"
    assert normalized(b"one\ntwo\n") == "one\ntwo\n"
    with pytest.raises(RuntimeError, match="mixed line endings"):
        normalized(b"one\rtwo")


def test_full_suite_count_passed_accepts_exactly_one_record():
    assert count_passed_summary("3546 passed in 125.50s", 0) == 3546
    assert count_passed_summary("3547 passed in 123.00s", 0) == 3547
    with pytest.raises(RuntimeError, match="exit code"):
        count_passed_summary("3546 passed in 1.0s", 1)
    with pytest.raises(RuntimeError, match="decreased"):
        count_passed_summary("3545 passed in 1.0s", 0)
    with pytest.raises(RuntimeError, match="exactly one"):
        count_passed_summary("no recognized summary", 0)
    with pytest.raises(RuntimeError, match="exactly one"):
        count_passed_summary("3546 passed in 1.0s\n3546 passed in 2.0s", 0)


def test_renderer_state_rejects_unreviewed_content(monkeypatch):
    import phase172_r6_phase_closeout.audit as audit
    monkeypatch.setattr(audit.r5_installer, "updated_renderer", lambda data: data + b"\nR5")
    assert renderer_state(b"BASE", b"BASE\nR5", b"BASE") == "R5_UNCOMMITTED"
    assert renderer_state(b"BASE\nR5", b"BASE\nR5", b"BASE") == "R5_COMMITTED"
    with pytest.raises(RuntimeError, match="working Renderer"):
        renderer_state(b"BASE", b"UNKNOWN", b"BASE")
    with pytest.raises(RuntimeError, match="HEAD Renderer"):
        renderer_state(b"UNKNOWN", b"BASE\nR5", b"BASE")


def test_pi63_prose_guard_rejects_missing_heading():
    with pytest.raises(RuntimeError, match="heading missing"):
        check_pi63_markdown("使用する結果\n証明欄なし")


def test_no_full_suite_is_invoked_in_guard_unit_tests(monkeypatch):
    import phase172_r6_phase_closeout.audit as audit
    def forbidden(*args, **kwargs):
        raise AssertionError("unit tests must not run the active full pytest")
    monkeypatch.setattr(audit, "run_full_suite_once", forbidden)
    assert Path(audit.ROOT).name != ""
