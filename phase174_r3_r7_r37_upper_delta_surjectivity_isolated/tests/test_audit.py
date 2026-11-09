"""Regression of actual source-first EHP frontier; no result is declared complete."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.audit import (
    inspect_isolated_upper_delta,
    report,
)
from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
    upper_delta_surjectivity_inputs,
)


def test_upper_delta_is_exact_earlier_root_obligation() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    requirements = ehp_zero_inputs(root)
    assert requirements is not None
    upper = requirements[0]
    second = upper_delta_surjectivity_inputs(upper)
    assert second is not None
    assert len(second) == 4
    assert second[2].map.source_group == TodaPrimaryGroup(11, 11)
    assert second[2].map.target_group == TodaPrimaryGroup(9, 5)


def test_real_r36_sources_reach_isolated_r37_obligations() -> None:
    result = inspect_isolated_upper_delta()
    assert result["isolated_upper_surjectivity_expansions"] == 1
    assert result["four_independent_obligations_typed"] is True
    assert result["r36_kernel_inference_audit_preserved"] is True
    assert result["prop27_public_instance_proposed"] is True
    assert result["upper_delta_surjectivity_proved_in_r37"] is False
    assert result["root_complete"] is False


def test_source_guard_preflight_never_certifies_root() -> None:
    result = report(True)
    assert result["git_state"]["source_guard"] == "PASS"
    assert result["details"] is None
    assert result["gate"] == "PASS_R37_REVIEWED_SOURCE_PREFLIGHT_ONLY"
