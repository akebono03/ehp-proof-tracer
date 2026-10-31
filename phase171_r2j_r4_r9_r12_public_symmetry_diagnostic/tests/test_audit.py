"""Read-only R12 stage and observation tests; no completed tree is injected."""
from __future__ import annotations

import pytest

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
from phase165_r57_r26_generic_search_connection import merge_backward_expansions
from phase171_r2j_r4_r9_r12_public_symmetry_diagnostic.audit import (
    TracingProvider,
    git_blob_sha,
    git_read,
    normalized_source,
    route_matches,
    route_profile,
)
from proof import Relation, RelationType
from relation_rules import equality_symmetry_inference_rule


def test_only_read_only_git_commands_are_allowed():
    with pytest.raises(ValueError, match="read-only"):
        git_read("reset", "--hard")
    with pytest.raises(ValueError, match="read-only"):
        git_read("checkout", "develop")


def test_exact_symmetry_route_is_preserved_by_merge_and_nonroot_gate():
    forward = Relation("x", "y", RelationType.EQUALITY)
    reverse = Relation("y", "x", RelationType.EQUALITY)
    candidate = GoalExpansion(equality_symmetry_inference_rule(), (forward,))
    initial = (candidate,)
    merged = merge_backward_expansions(initial, ())
    gated = retain_ordered_root_expansions(object(), reverse, merged)
    for routes in (initial, merged, gated):
        assert route_matches(routes, "equality symmetry", (forward,)) == 1
        assert route_profile(routes)["symmetry_count"] == 1
    assert gated[0] is candidate


def test_tracing_provider_retains_original_candidates_and_observes_calls():
    forward = Relation("x", "y", RelationType.EQUALITY)
    reverse = Relation("y", "x", RelationType.EQUALITY)
    candidate = GoalExpansion(equality_symmetry_inference_rule(), (forward,))
    calls = []

    def provider(goal):
        calls.append(goal)
        return (candidate,)

    tracing = TracingProvider(provider)
    actual = tracing(reverse)
    assert actual == (candidate,)
    assert actual[0] is candidate
    assert calls == [reverse]
    assert tracing.count == 1
    assert tracing.calls[0]["routes"]["symmetry_count"] == 1


def test_route_profile_rejects_non_expansion_results():
    with pytest.raises(TypeError):
        route_profile([])
    with pytest.raises(TypeError):
        route_profile((object(),))
    assert route_profile(())["count"] == 0


def test_git_blob_and_crlf_normalization_do_not_mutate_source():
    payload = b"a\r\nb\r\n"
    assert normalized_source(payload) == "a\nb\n"
    assert normalized_source(b"\xef\xbb\xbfa\n") == "a\n"
    assert git_blob_sha(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
