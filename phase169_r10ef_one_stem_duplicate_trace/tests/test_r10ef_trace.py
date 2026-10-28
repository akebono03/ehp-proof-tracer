"""Pure focused audit tests; no live proof is created or reclassified."""
from __future__ import annotations

from dataclasses import dataclass

from phase169_r10ef_one_stem_duplicate_trace.trace import (
    AppendObservation,
    forward_and_observe,
    is_exact_goal_conclusion,
    pairwise_kept_indices,
)


@dataclass(frozen=True)
class Dummy:
    conclusion: object


def test_r10ef_exact_root_match_requires_type_and_value():
    assert is_exact_goal_conclusion(Dummy(42), 42)
    assert not is_exact_goal_conclusion(Dummy("42"), 42)
    assert not is_exact_goal_conclusion(Dummy(43), 42)


def test_r10ef_observer_delegates_and_records_kept():
    options = []
    observations = []
    item = Dummy((4, 1))
    calls = []

    def append(items, step):
        calls.append(step)
        items.append(step)

    forward_and_observe(options, item, goal=(4, 1), delegate=append,
                        observations=observations)
    assert calls == [item] and options == [item]
    assert observations == [AppendObservation(True, 0, 1, item)]


def test_r10ef_observer_does_not_reclassify_rejected_duplicates():
    options = [Dummy((4, 1))]
    observations = []
    item = Dummy((4, 1))

    def dedup(items, step):
        if step not in items:
            items.append(step)

    forward_and_observe(options, item, goal=(4, 1), delegate=dedup,
                        observations=observations)
    assert len(options) == 1
    assert observations == [AppendObservation(False, 1, 1, item)]


def test_r10ef_nonroot_candidate_is_forwarded_but_not_recorded():
    options = []
    observations = []
    forward_and_observe(options, Dummy("nested"), goal="root",
                        delegate=lambda items, step: items.append(step),
                        observations=observations)
    assert len(options) == 1 and observations == []


def test_r10ef_pairwise_kept_never_ranks_or_merges():
    observations = [
        AppendObservation(True, 0, 1, object()),
        AppendObservation(False, 1, 1, object()),
        AppendObservation(True, 1, 2, object()),
        AppendObservation(True, 2, 3, object()),
    ]
    assert pairwise_kept_indices(observations) == ((0, 2), (0, 3), (2, 3))
    assert len(observations) == 4
