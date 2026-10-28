"""Local shadow-provider behavior tests; no existing code patches."""
from __future__ import annotations

from expression import HomotopyElement, IteratedSuspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10et_r2_shadow_common_definition_comparison.audit import (
    compare_case,
    prioritize_common_definition,
    shadow_provider_factory,
)


def test_shadow_eligible_image_uses_common_definition_without_legacy_call():
    source = HomotopyElement("x", 16, 30, 16)
    target = IteratedSuspension(source, 1)
    goal = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(30, 16), TodaPrimaryGroup(31, 17)),
        source, target,
    )
    calls = []
    def original(value):
        calls.append(value)
        return ("legacy",)
    proposals = prioritize_common_definition(original)(goal)
    assert len(proposals) == 1
    assert proposals[0].subgoals == ()
    assert calls == []


def test_shadow_noneligible_goal_retains_legacy_search():
    calls = []
    def factory(name):
        def original(goal):
            calls.append((name, goal))
            return ("original", goal)
        return original
    wrapper = shadow_provider_factory(factory)
    assert wrapper("context")("unrelated goal") == ("original", "unrelated goal")
    assert calls == [("context", "unrelated goal")]


def test_shadow_comparison_does_not_classify_removed_reference_as_unused():
    previous = {
        "references": [
            {"locator": "DB prior"}, {"locator": "(4.5)"},
            {"locator": "Chapter V, arbitrary-definition"},
        ],
        "image_actual_common": 0,
        "image_cited_but_common_eligible": 4,
        "direct_sum_projection": {"statement": "prior proof"},
    }
    current = {
        "trust": "PASS",
        "references": [{"locator": "DB prior"}, {"locator": "(4.5)"}],
        "image_actual_common": 4,
        "image_cited_but_common_eligible": 0,
        "direct_sum_projection": None,
    }
    comparison = compare_case(current, previous)
    assert comparison["removed_references"] == ["Chapter V, arbitrary-definition"]
    assert comparison["baseline_projection_present"]
    assert not comparison["shadow_projection_present"]
