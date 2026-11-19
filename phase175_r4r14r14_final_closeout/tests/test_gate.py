"""Focused one-shot gate contracts; never run the full suite here."""
from __future__ import annotations

import pytest

from phase175_r4r14r14_final_closeout import gate


def test_active_command_runs_only_tests_directory() -> None:
    assert gate.ACTIVE_COMMAND == (
        "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings",
        "-p", "no:cacheprovider", "tests",
    )


def test_success_summary_is_strict() -> None:
    assert gate.parse_summary("3546 passed in 40.86s\n", 0) == (3546, "3546 passed in 40.86s")


@pytest.mark.parametrize("output, code", [
    ("10 passed, 1 failed in 2.00s", 1),
    ("10 passed, 1 skipped in 2.00s", 0),
    ("10 passed, 1 deselected in 2.00s", 0),
    ("10 passed in 2.00s\n12 passed in 3.00s", 0),
    ("collection interrupted", 0),
    ("0 passed in 1.00s", 0),
])
def test_invalid_summary_fails_closed(output: str, code: int) -> None:
    with pytest.raises(RuntimeError):
        gate.parse_summary(output, code)


def test_five_full_documents_require_final_marker() -> None:
    sections = gate.final_sections({
        "head": "test-head", "summary": "10 passed in 2.00s",
        "stdout_sha256": "0" * 64, "stderr_sha256": "1" * 64,
    })
    assert set(sections) == set(gate.DOCUMENT_BLOBS)
    assert all(text.count(gate.FINAL_MARKER) == 1 for text in sections.values())
    assert "formally closed" in sections["README.md"]
    assert all("正式終了" in text for name, text in sections.items() if name != "README.md")
    assert all("4" in text or "four" in text for text in sections.values())


def test_dry_run_never_calls_full_pytest(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(gate, "evidence_dir", lambda: tmp_path)
    monkeypatch.setattr(gate, "preflight", lambda: {"head": "fake-head"})
    monkeypatch.setattr(gate.subprocess, "run", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("MUST NOT RUN")))
    assert gate.run(True, 30) == 0
    assert not (tmp_path / "attempt.json").exists()


def test_existing_attempt_blocks_repeat(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(gate, "evidence_dir", lambda: tmp_path)
    (tmp_path / "attempt.json").write_text("{}", encoding="utf-8")
    assert gate.run(False, 30) == 1
