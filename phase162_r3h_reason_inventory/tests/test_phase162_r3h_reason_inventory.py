"""Focused read-only inventory tests; no full repository suite."""

import pytest

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace
from phase162_r3h_reason_inventory import (
    build_phase162_r3h_inventory,
    classify_r3h_unexplained_step,
)


@pytest.fixture(scope='module')
def presentation():
    return build_r3b_presentation()[1]


@pytest.fixture(scope='module')
def inventory(presentation):
    return build_phase162_r3h_inventory(presentation)


def test_phase162_r3h_inventory_covers_exactly_unexplained_indices(presentation, inventory):
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    entries, report = inventory
    expected = [record.index for record in baseline.records if record.reason_status == 'UNEXPLAINED']
    assert [entry.index for entry in entries] == expected
    assert report['unexplained_count'] == len(expected)
    assert sum(report['category_counts'].values()) == len(expected)


def test_phase162_r3h_preserves_graph_and_baseline(presentation, inventory):
    entries, report = inventory
    assert report['node_count'] == len(presentation.nodes)
    assert report['edge_count'] == len(presentation.edges)
    assert report['dependency_first']
    assert report['root_is_last']
    assert report['all_nodes_once']
    assert report['already_explained_count'] + len(entries) + report['given_count'] == len(presentation.nodes)


def test_phase162_r3h_does_not_count_generic_result_label_as_reason(inventory):
    entries, _ = inventory
    assert all(entry.category != 'DIRECT_REUSE_READY' or entry.existing_reason_kinds for entry in entries)
    assert all(entry.category != 'GENERIC_RESULT_LABEL_ONLY' or not entry.existing_reason_kinds for entry in entries)


def test_phase162_r3h_direct_matches_have_real_premises(presentation, inventory):
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    records = {record.index: record for record in baseline.records}
    entries, _ = inventory
    for entry in entries:
        assert entry.premise_indices == records[entry.index].premise_indices
        assert all(index < entry.index for index in entry.premise_indices)
        if entry.category == 'DIRECT_REUSE_READY':
            assert len(entry.existing_reason_kinds) == 1


def test_phase162_r3h_avoids_public_markdown(presentation, monkeypatch):
    import toda_group_proof_narrative_renderer

    def prohibited(_):
        raise AssertionError('Public renderer must not be used')

    monkeypatch.setattr(toda_group_proof_narrative_renderer, 'render_toda_group_proof_narrative_markdown', prohibited)
    assert build_phase162_r3h_inventory(presentation)[1]['node_count'] == len(presentation.nodes)


def test_phase162_r3h_rejects_nonpresentation():
    with pytest.raises(TypeError, match='TodaGroupProofPresentation'):
        build_phase162_r3h_inventory(None)


def test_phase162_r3h_refuses_to_classify_explained(presentation):
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    explained = next(r for r in baseline.records if r.reason_status == 'EXPLAINED')
    with pytest.raises(ValueError, match='unexplained inference'):
        classify_r3h_unexplained_step(explained)
