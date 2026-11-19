"""Focused read-only R13R1 tests."""
from pathlib import Path
import pytest
from phase175_r4r12r13r1_delta_injective_frontier import audit


def test_toda58_checks_exact_equation_only() -> None:
    good = (r"\begin{equation}\label{eq:5.8}" + "\n"
            + r"\Delta(\iota_9) = \pm(2\nu_4 - E\nu')" + "\n"
            + r"\end{equation}")
    assert audit.source_formula_present(good)
    assert not audit.source_formula_present(good.replace(r"\iota_9", r"\eta_9"))
    assert not audit.source_formula_present(good.replace(r"\label{eq:5.8}", r"\label{eq:5.9}"))


def test_git_failure_is_not_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    class Failed:
        returncode = 1
        stdout = ""
        stderr = "simulated failure"
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="GIT_FAILED"):
        audit.git(Path("."), "rev-parse", "HEAD")


def test_required_dependencies_are_explicit() -> None:
    assert "sources/toda/Toda_05_2.tex" in audit.REQUIRED_PATHS
    assert "phase165_r12_r11_prop42_unified.py" in audit.REQUIRED_PATHS
    assert "phase165_r52_r9_shared_math.py" in audit.REQUIRED_PATHS
