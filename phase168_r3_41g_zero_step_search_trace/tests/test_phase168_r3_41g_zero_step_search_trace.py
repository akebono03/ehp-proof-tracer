"""Focused tests for read-only search instrumentation."""
from __future__ import annotations

from dataclasses import dataclass

from phase168_r3_41g_zero_step_search_trace.audit import (
    SearchObservation, classify_search, instrument_reconstruction,
)


@dataclass(frozen=True)
class FakeExpansionRule:
    name: str


@dataclass(frozen=True)
class FakeExpansion:
    rule: FakeExpansionRule
    subgoals: tuple[str, ...]


def test_instrumentation_forwards_provider_and_observer_unchanged():
    observation = SearchObservation()
    provided_goal = "root"
    expected = (FakeExpansion(FakeExpansionRule("rule"), ("child",)),)
    original_events = []
    calls = []

    def provider(goal):
        calls.append(("provider", goal))
        return expected

    def callback(kind, goal, step):
        original_events.append((kind, goal, step))

    def original(goal, bridge, citing_id, injected_provider, *, progress_observer, lookup_mode):
        assert goal == provided_goal
        assert lookup_mode == "typed_reference"
        assert injected_provider(goal) is expected
        progress_observer("proved", goal, "proved-step")
        progress_observer("unresolved", "child", None)
        return "original-return"

    output = instrument_reconstruction(
        original, (provided_goal, object(), "context", provider),
        {"lookup_mode": "typed_reference", "progress_observer": callback},
        observation,
    )
    assert output == "original-return"
    assert calls == [("provider", provided_goal)]
    assert original_events == [
        ("proved", "root", "proved-step"),
        ("unresolved", "child", None),
    ]
    assert observation.reconstruction_calls == 1
    assert observation.root_provider_calls == 1
    assert observation.root_option_count == 1
    assert observation.root_rule_names == ["rule"]
    assert observation.event_counts["proved"] == 1
    assert observation.event_counts["unresolved"] == 1


def test_instrumentation_does_not_change_empty_expansion_result():
    observation = SearchObservation()
    original_empty = ()

    def provider(goal):
        return original_empty

    def original(goal, bridge, citing_id, injected_provider, *, progress_observer):
        assert injected_provider(goal) is original_empty
        progress_observer("unresolved", goal, None)
        return "no-proof"

    outcome = instrument_reconstruction(
        original, ("root", object(), "context", provider), {}, observation,
    )
    assert outcome == "no-proof"
    assert observation.root_option_count == 0
    assert observation.no_option_targets == ["root"]
    assert observation.event_counts["proved"] == 0


def test_classification_distinguishes_no_rules_from_failed_premises():
    assert classify_search(
        status="search_failed", reconstruct_calls=1,
        root_provider_calls=1, root_option_count=0, accepted_event_count=0,
    ) == "ROOT_NO_EXPANSIONS"
    assert classify_search(
        status="search_failed", reconstruct_calls=1,
        root_provider_calls=1, root_option_count=3, accepted_event_count=0,
    ) == "ROOT_EXPANSIONS_BUT_NO_ACCEPTED_PROOF_STEPS"


def test_classification_preserves_presearch_and_proved_branches():
    assert classify_search(
        status="search_failed", reconstruct_calls=0,
        root_provider_calls=0, root_option_count=0, accepted_event_count=0,
    ) == "FAILED_BEFORE_RECONSTRUCTION"
    assert classify_search(
        status="partial", reconstruct_calls=1,
        root_provider_calls=1, root_option_count=2, accepted_event_count=1,
    ) == "ROOT_EXPANSIONS_WITH_SOME_ACCEPTED_STEPS_BUT_UNRESOLVED"
    assert classify_search(
        status="complete", reconstruct_calls=1,
        root_provider_calls=0, root_option_count=0, accepted_event_count=1,
    ) == "COMPLETE_CONTROL"


def test_observer_does_not_fabricate_proved_steps():
    observation = SearchObservation()
    observation.observe("unresolved", "missing-premise", None)
    assert observation.accepted_steps == []
    assert observation.event_counts["proved"] == 0
    assert len(observation.unresolved_targets) == 1
