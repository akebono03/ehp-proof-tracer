"""Focused tests for the read-only Phase 173 R4-R1 auditor."""
from __future__ import annotations

import pytest

from phase173_r4_r1_audit_only.audit import (
    inspect_named_function,
    verify_audit_only_changes,
    verify_source_text,
)


def test_accepts_only_reviewed_r3_additions() -> None:
    changes = (
        "A\tphase173_r3_portable/audit.py\n"
        "A\tphase173_r3_frontier_readout/readout.py"
    )
    assert verify_audit_only_changes(changes) == [
        "phase173_r3_portable/audit.py",
        "phase173_r3_frontier_readout/readout.py",
    ]


@pytest.mark.parametrize("record", [
    "M\tphase165_r52_r9_shared_math.py",
    "A\tphase173_r4_r1_audit_only/audit.py",
    "D\tphase173_r3_portable/audit.py",
    "A\tphase173_r3_portable/../wrong.py",
    "R100\tphase173_r3_portable/old.py\tphase173_r3_portable/new.py",
])
def test_rejects_unauthorized_changed_paths(record: str) -> None:
    with pytest.raises(RuntimeError):
        verify_audit_only_changes(record)


def test_extracts_one_named_function_without_patching() -> None:
    source = (
        "def f(x):\n"
        "    return x\n\n"
        "def g(y):\n"
        "    return y\n"
    )
    result = inspect_named_function(source, "f")
    assert result["defined_exactly_once"] is True
    assert result["line"] == 1
    assert result["mentions_direct_sum"] is False
    assert inspect_named_function(source, "missing")["defined_exactly_once"] is False


def test_rejects_duplicate_rule_definitions() -> None:
    source = "def f():\n    return 1\ndef f():\n    return 2\n"
    report = inspect_named_function(source, "f")
    assert report["defined_exactly_once"] is False
    assert report["count"] == 2


def test_toda_source_specialization_metadata() -> None:
    chapter5 = (
        "Prop 4.4 とLem 5.4 から,\n"
        "\\begin{equation}\\label{eq:5.6}\n"
        "\\pi^{\\,3}_{i-1}\\oplus\\pi^{\\,7}_{i} "
        "\\xrightarrow{\\cong}\\pi_{\\,i}^{4} "
        "\\nu_{4}\\circ\\beta\n"
        "\\end{equation}\n"
        "\\begin{lemma}\\label{lem:5.4}"
        "H(\\nu_{4})=\\iota_7, 2E \\nu_{4}=E^{2}\\nu'"
    )
    chapter4 = (
        "\\begin{proposition}\\label{prop:4.4}\n"
        "\\pit{i-1}{n-1}\\oplus\\pit{i}{2n-1} X 同型\n"
        "\\end{proposition}"
    )
    report = verify_source_text(chapter5, chapter4)
    assert report["specialization_i"] == 7
    assert report["specialized_source_groups"] == ["pi_6^3", "pi_7^7"]
    assert report["pi77_free_cyclic_proved_here"] is False


def test_rejects_source_without_mandatory_map() -> None:
    chapter5 = (
        "Prop 4.4 とLem 5.4 から,"
        "\\begin{equation}\\label{eq:5.6}"
        "\\pi^{\\,3}_{i-1}\\oplus\\pi^{\\,7}_{i} "
        "\\xrightarrow{\\cong}\\pi_{\\,i}^{4}"
        "\\end{equation}"
    )
    with pytest.raises(RuntimeError, match="equation"):
        verify_source_text(chapter5, "")
