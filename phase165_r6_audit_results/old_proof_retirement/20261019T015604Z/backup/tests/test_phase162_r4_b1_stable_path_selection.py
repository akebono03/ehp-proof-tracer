import pytest

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_stable_proof_path_selection import (
    TodaStableProofPathKind,
    select_toda_stable_proof_path,
)


def _selection(n: int, k: int):
    presentation, _, _, _ = _method_evidence_data(n, k)
    return select_toda_stable_proof_path(
        presentation.source_replay.group_result
    )


def test_phase162_r4_b1_stable_base_keeps_existing_path():
    choice = _selection(3, 1)
    assert choice.kind is TodaStableProofPathKind.STABLE_BASE_EXISTING
    assert choice.uses_existing_root
    assert choice.suspension_count == 0
    assert not choice.requires_transport_proof


@pytest.mark.parametrize(
    ("n", "count"),
    [(4, 1), (5, 2)],
)
def test_phase162_r4_b1_higher_stable_targets_select_toda45(n, count):
    choice = _selection(n, 1)
    assert choice.kind is TodaStableProofPathKind.STABLE_TODA45_TRANSPORT
    assert choice.base.group_dimension == 4
    assert choice.base.sphere_dimension == 3
    assert choice.suspension_count == count
    assert choice.requires_transport_proof
    assert not choice.uses_existing_root


def test_phase162_r4_b1_unstable_preserves_existing_path():
    choice = _selection(2, 1)
    assert choice.kind is TodaStableProofPathKind.UNSTABLE_EXISTING
    assert choice.base is None
    assert choice.suspension_count is None
    assert choice.uses_existing_root


def test_phase162_r4_b1_stem_seven_uses_canonical_base():
    choice = _selection(10, 7)
    assert choice.kind is TodaStableProofPathKind.STABLE_TODA45_TRANSPORT
    assert choice.base.group_dimension == 16
    assert choice.base.sphere_dimension == 9
    assert choice.suspension_count == 1


def test_phase162_r4_b1_rejects_non_group_result():
    with pytest.raises(TypeError, match="TodaGroupResult"):
        select_toda_stable_proof_path(None)
