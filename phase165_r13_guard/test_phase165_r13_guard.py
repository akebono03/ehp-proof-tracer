import pytest
import phase164_r5_r2_common_replay as selector


@pytest.mark.parametrize('mode', ['trace', 'outline', 'narrative'])
def test_pi3_2_does_not_fall_back_to_legacy_replay(monkeypatch, mode):
    def forbidden(*args, **kwargs):
        raise AssertionError('legacy replay was invoked')

    monkeypatch.setattr(selector, 'build_toda_group_result_proof_replay', forbidden)
    with pytest.raises(ValueError, match='no certified typed-statement proof'):
        selector.build_phase164_r5_r2_common_replay(2, 1, object(), 2, mode)


def test_other_group_legacy_route_unchanged_in_this_step(monkeypatch):
    marker = object()
    monkeypatch.setattr(
        selector, 'build_toda_group_result_proof_replay',
        lambda result, max_depth: (result, max_depth),
    )
    assert selector.build_phase164_r5_r2_common_replay(6, 3, marker, 2, 'trace') == (marker, 2)
