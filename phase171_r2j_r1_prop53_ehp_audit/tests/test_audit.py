"""Focused R2J-R1 tests of EHP indices and the existing inference direction."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
from phase171_r2j_r1_prop53_ehp_audit.audit import (
    _source_claim_audit,
    delta_map,
    h_delta_exactness_goal,
    hopf_map,
)
from toda_rules import TodaDeltaZeroStatement


def test_r2j_earlier_prop53_adopted_source_has_explicit_scope():
    result = _source_claim_audit()
    assert result["adopted_text_contains_statement"] is True
    assert result["printed_scope"] == "n >= 2"
    assert result["original_printed_edition_independently_verified"] is False
    assert result["audit_does_not_upgrade_registration"] is True


def test_r2j_hopf_and_delta_maps_have_compatible_source_targets():
    h = hopf_map()
    delta = delta_map()
    assert h.source_group == TodaPrimaryGroup(7, 3)
    assert h.target_group == delta.source_group == TodaPrimaryGroup(7, 5)
    assert delta.target_group == TodaPrimaryGroup(5, 2)


def test_r2j_h_delta_exactness_is_valid_toda_prop42_window():
    statement = h_delta_exactness_goal()
    assert prop42_exactness_indices(statement) == (2, 7, "h_delta")
    assert statement.window.source_term == TodaPrimaryGroup(7, 3)
    assert statement.window.target_term == TodaPrimaryGroup(5, 2)


def test_r2j_existing_hopf_surjectivity_direction_requires_delta_zero():
    options = expand_generic_ehp_hopf_goal(MapSurjective(hopf_map()))
    assert len(options) == 1
    assert options[0].subgoals == (
        TodaDeltaZeroStatement(delta_map()), h_delta_exactness_goal(),
    )
    assert options[0].rule.name == (
        "EHP: subsequent zero delta and exactness imply Hopf surjectivity"
    )


def test_r2j_mistyped_hopf_map_has_no_generic_ehp_expansion():
    from homotopy_groups import TodaHopfInvariantMap
    wrong = TodaHopfInvariantMap(TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 6))
    assert expand_generic_ehp_hopf_goal(MapSurjective(wrong)) == ()
