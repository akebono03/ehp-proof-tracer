from types import SimpleNamespace

from phase168_r2_8_9_renderer_runtime_trace.audit import (
    summarize_entries,
    summarize_event,
    summarize_ids,
)


def test_summarize_entries_preserves_locator_and_step_ids():
    step = object()
    entry = SimpleNamespace(number=1, reference=SimpleNamespace(locator="(5.2)"), proof_steps=(step,))
    assert summarize_entries((entry,)) == [{"number": 1, "locator": "(5.2)", "step_ids": [id(step)]}]


def test_summarize_ids_rejects_nonidentity_values():
    assert summarize_ids(frozenset({3, 2})) == [2, 3]
    assert summarize_ids(frozenset({True})) is None


def test_summarize_filter_event_reports_actual_input_output():
    entry = SimpleNamespace(number=1, reference=SimpleNamespace(locator="Proposition 5.1"), proof_steps=(object(),))
    row = summarize_event("filter_toda_group_proof_narrative_reference_entries_by_step_usage", {
        "entries": (entry,), "used_step_ids": frozenset({id(entry.proof_steps[0])}),
    }, (entry,))
    assert row["used_step_ids"] == [id(entry.proof_steps[0])]
    assert row["output_entries"][0]["locator"] == "Proposition 5.1"
