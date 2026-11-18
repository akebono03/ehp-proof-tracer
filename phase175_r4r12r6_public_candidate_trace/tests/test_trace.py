"""R4R12R6 pure control contracts; no group proof is executed."""
from pathlib import Path

import pytest

from phase175_r4r12r6_public_candidate_trace import trace


def test_known_head_is_pinned() -> None:
    assert trace.EXPECTED_HEADS == ("9203e1a8c077320a58214bda40d9bfeb17704f58",)


def test_git_reports_unknown_commands(monkeypatch: pytest.MonkeyPatch) -> None:
    class Failed:
        returncode = 1
        stderr = "missing"
        stdout = ""
    monkeypatch.setattr(trace.subprocess, "run", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="R4R12R6_GIT_FAILED"):
        trace.git(Path("."), "rev-parse", "HEAD")
