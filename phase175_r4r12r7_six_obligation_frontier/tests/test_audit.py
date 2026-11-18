"""Read-only contract tests for Phase 175 R4R12R7."""
from pathlib import Path
import pytest
from phase175_r4r12r7_six_obligation_frontier import audit


def test_git_failure_is_not_silently_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    class Failed:
        returncode = 1
        stdout = ""
        stderr = "failure"
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="GIT_FAILED"):
        audit.git(Path("."), "rev-parse", "HEAD")


def test_describe_truncates_long_statements() -> None:
    assert audit.describe("x" * 800).endswith("...")
    assert len(audit.describe("x" * 800)) == 450


def test_dirty_allowlist_is_not_broad() -> None:
    assert audit.ALLOWED_DIRTY == {
        ".pytest_cache/v/cache/nodeids", "phase175_r4r3_two_summand_quotient/rule.py"
    }


def test_reviewed_commit_pin_and_exact_diff() -> None:
    assert audit.REVIEWED_HEAD == "94c5d6839889bbfa03aad166ac9c6fd1558b8c5b"
    assert "phase175_r4r12r6_public_candidate_trace/trace.py" in audit.REVIEWED_COMMITTED_PATHS
    assert "phase175_r4r3_two_summand_quotient/rule.py" in audit.REVIEWED_COMMITTED_PATHS
    assert "phase175_r4r12r7_six_obligation_frontier/audit.py" not in audit.REVIEWED_COMMITTED_PATHS
