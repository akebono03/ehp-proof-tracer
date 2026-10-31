"""R20R12R2: genuine unindexed nu-prime generator and safe patch regression."""
from __future__ import annotations

from types import SimpleNamespace

from phase168_r3_27_typed_statement_projection import element_tex
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r20r12_verified_cyclic_narrative.projection import (
    verified_order_four_summary,
)
from phase171_r20r12r2_unindexed_nu_projection_fix.install import (
    SOURCE_NEW_LINE, corrected_source,
)
from toda_human_readable_renderer import render_toda_expression_latex


def test_unindexed_nu_prime_is_renderable_without_unsupported_element_tex():
    root, ancestors, report = build_cyclic_pi63_proof()
    assert report["pi63_cyclic_group_proven"] is True
    generator = root.premises[1].conclusion.element
    assert element_tex(generator) is None
    latex = render_toda_expression_latex(generator)
    assert latex == r"\nu'"
    summary = verified_order_four_summary(SimpleNamespace(
        steps=ancestors,
        root_index=next(i for i, node in enumerate(ancestors) if node is root),
    ))
    assert summary is not None
    assert r"\operatorname{ord}(\nu')=4" in summary
    assert r"\neq0" in summary
    assert "短完全列" in summary


def test_only_registered_projection_generator_line_changes():
    from pathlib import Path
    package = Path(__file__).resolve().parent.parent
    original = (package / "original_projection.py.reviewed").read_bytes()
    updated = corrected_source(original)
    assert SOURCE_NEW_LINE in updated.decode("utf-8")
    assert updated.decode("utf-8").count("render_toda_expression_latex(order.element)") == 1
    assert b"from phase168_r3_27_typed_statement_projection import group_tex" in updated
    assert updated != original
    assert len(updated.splitlines()) == len(original.splitlines())
