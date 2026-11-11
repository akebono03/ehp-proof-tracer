"""R62: distinct attribution policy boundaries, invalid inputs and source pins."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r62_attribution_policy_boundary_audit.audit import (
    PINS, counterexample_contract, git_blob_sha, hypothetical_route_choices,
    renderer_policy_contract, source_guard, validate_number_set,
)


def test_reviewed_file_pins_and_renderer_policy_contract() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 7
    assert source_guard(root) == tuple(PINS)
    source = (root / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8-sig")
    contract = renderer_policy_contract(source)
    assert contract["distinct_policy_routes"] == 3
    assert len(contract["call_sites"]) == 7
    assert contract["safe_to_replace_with_unconditional_all_ancestors"] is False


def test_two_ancestor_types_are_not_the_same_policy() -> None:
    choices = hypothetical_route_choices((1, 2), (2,), ())
    assert choices == {
        "typed_general": (2,), "direct_given": (), "unique_ancestor": (),
    }


def test_direct_given_does_not_inherit_unrelated_source() -> None:
    choices = hypothetical_route_choices((1, 2), (), (1,))
    assert choices["direct_given"] == (1,)
    assert choices["typed_general"] == ()
    assert choices["unique_ancestor"] == ()


def test_unique_ancestor_is_selected_only_if_unique() -> None:
    assert hypothetical_route_choices((5,), (), ())['unique_ancestor'] == (5,)
    assert hypothetical_route_choices((), (), ())['unique_ancestor'] == ()
    assert hypothetical_route_choices((5, 6), (), ())['unique_ancestor'] == ()


def test_hypothetical_policy_refuses_source_outside_ancestry() -> None:
    with pytest.raises(ValueError):
        hypothetical_route_choices((1, 2), (3,), ())
    with pytest.raises(ValueError):
        hypothetical_route_choices((1, 2), (), (3,))


@pytest.mark.parametrize('bad', [(-1,), (0,), (True,), (1, 1)])
def test_invalid_source_number_sets_fail_closed(bad: tuple[object, ...]) -> None:
    with pytest.raises(ValueError):
        validate_number_set(bad)


def test_non_tuple_source_numbers_fail_closed() -> None:
    with pytest.raises(TypeError):
        validate_number_set([1, 2])


def test_reviewed_renderer_guard_rejects_missing_routes() -> None:
    with pytest.raises(RuntimeError):
        renderer_policy_contract('def render_model_backed_narrative_markdown(result, model):\n    return None\n')


def test_counterexamples_reject_unconditional_cite_all() -> None:
    contract = counterexample_contract()
    assert contract['unconditional_cite_all_equivalent'] is False
    assert contract['counterexamples_are_fixture_logic_only'] is True


def test_source_guard_rejects_tampered_blob(tmp_path: Path) -> None:
    source = next(iter(PINS))
    target = tmp_path / source
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('tampered source', encoding='utf-8')
    with pytest.raises(RuntimeError):
        source_guard(tmp_path)


def test_blob_hash_known_fixture() -> None:
    assert git_blob_sha(b"hello\n") == 'ce013625030ba8dba906f756967f9e9ca394464a'
