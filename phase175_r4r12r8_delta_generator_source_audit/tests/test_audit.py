"""Focused read-only tests for Phase 175 R4R12R8."""
from pathlib import Path
import pytest
from phase175_r4r12r8_delta_generator_source_audit import audit


def test_delta_source_expected_proof_fragments() -> None:
    source = (
        r"\begin{equation}\label{eq:5.8}\Delta(\iota_9)=\pm(2\nu_4-E\nu')\end{equation}"
        r"\begin{proposition}\label{prop:5.8}"
        r"\Delta(\iota_9)\circ\eta_7\text{by Prop2.5}"
        r"(2\nu_4-E\nu')\circ\eta_7\text{by (5.8)}"
        r"\nu_4\circ(2\eta_7)-E\nu'\circ\eta_7"
        r"E\nu'\circ\eta_7\qed"
        r"\begin{equation}\label{eq:5.11}\Delta(\eta_9)=E\nu'\circ\eta_7\end{equation}"
    )
    result = audit.inspect_source(source)
    assert all(result["markers"].values())
    assert result["sign_disappears_only_after_order_two_argument"]
    assert not result["source_edition_is_original_print"]


def test_missing_signed_equation_fails_closed() -> None:
    source = (
        r"\begin{equation}\label{eq:5.8}\Delta(\iota_9)=0\end{equation}"
        r"\begin{proposition}\label{prop:5.8}\qed"
        r"\begin{equation}\label{eq:5.11}\Delta(\eta_9)=0\end{equation}"
    )
    with pytest.raises(RuntimeError, match="source markers missing"):
        audit.inspect_source(source)


def test_existing_rule_is_not_mistaken_for_image_proof() -> None:
    rule = (
        "def free_cyclic_generator_delta_image_inference_rule():\n"
        "    pass\n"
        "# TodaDeltaImageUpToSignStatement\n"
        "# TodaDeltaImageFreeCyclicStatement\n"
    )
    r7 = 'def audit_obligations():\n    return {"proved": False}\n'
    result = audit.inspect_existing_rule(rule, r7)
    assert result["existing_rule_requires_signed_image_as_premise"]
    assert not result["typed_proof_of_equation_5_11"]


def test_wrong_repository_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="repository root"):
        audit.verify_repository(tmp_path)
