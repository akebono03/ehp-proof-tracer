"""Production public route test: map display without proof fabrication."""
from __future__ import annotations

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapInjective, MapIsomorphism, MapSurjective
from phase174_r3_r7_r17_typed_map_open_goal.audit import inspect_public_map_display
from web_group_proof_common import _group_proof_statement_latex


def test_generic_typed_map_property_displays_do_not_choose_a_stem() -> None:
    for top, lower, sphere in ((13, 11, 6), (15, 13, 7)):
        mapping = TodaDeltaMap(TodaPrimaryGroup(top, top), TodaPrimaryGroup(lower, sphere))
        source = rf"\pi_{{{top}}}^{{{top}}}"
        target = rf"\pi_{{{lower}}}^{{{sphere}}}"
        assert _group_proof_statement_latex(MapSurjective(mapping)) == (
            rf"\Delta: {source} \twoheadrightarrow {target}", None,
        )
        assert _group_proof_statement_latex(MapInjective(mapping)) == (
            rf"\Delta: {source} \hookrightarrow {target}", None,
        )
        assert _group_proof_statement_latex(MapIsomorphism(mapping)) == (
            rf"\Delta: {source} \xrightarrow{{\cong}} {target}", None,
        )


def test_public_r16_search_still_open_and_map_math_visible() -> None:
    status = inspect_public_map_display()
    assert status["public_root_candidates"] == 1
    assert status["public_delta_surjectivity_candidates"] == 0
    assert status["generic_isomorphism_depends_on_surjectivity"] is True
    assert status["direct_given_for_goal_or_delta"] is False
    assert status["search_status"] != "complete"
    assert status["math_rule_changes"] == 0
    assert status["completion_claimed"] is False
    assert "MapSurjective" in status["open_goal_types"]
