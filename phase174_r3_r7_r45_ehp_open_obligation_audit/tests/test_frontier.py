"""Read-only typed R45 proof obligations, not a final-root proof."""
from __future__ import annotations

from functools import lru_cache

from phase174_r3_r7_r45_ehp_open_obligation_audit.audit import (
    inspect_open_ehp_obligations,
)


@lru_cache(maxsize=1)
def report() -> dict[str, object]:
    return inspect_open_ehp_obligations()


def test_r44_source_and_four_distinct_ehp_windows_still_exist():
    observed = report()
    assert observed["toda59_screened_source_count"] == 1
    assert observed["prop42_window_indices"] == {
        "root_delta_e": [6, 12, "delta_e"],
        "root_e_h": [6, 12, "e_h"],
        "hopf_e_h": [5, 11, "e_h"],
        "lower_h_delta": [5, 11, "h_delta"],
    }
    assert observed["public_root_candidates"] == 1
    assert observed["public_upper_delta_candidates"] == 1
    assert observed["public_hopf_injective_candidates"] == 1
    assert observed["public_lower_image_kernel_candidates"] == 1


def test_general_prop42_candidates_only_appear_with_cited_source():
    observed = report()
    source_count = observed["prop42_cited_universal_source_count"]
    assert source_count in (0, 1)
    options = observed["prop42_public_specialization_candidates"]
    assert set(options) == {
        "root_delta_e", "root_e_h", "hopf_e_h", "lower_h_delta"
    }
    assert all(value in (0, 1) for value in options.values())
    if source_count == 0:
        assert all(value == 0 for value in options.values())
    else:
        assert all(value == 1 for value in options.values())


def test_real_inference_steps_have_cited_universal_ancestor():
    observed = report()
    steps = observed["canonical_scoped_prop42_inference_steps"]
    ancestry = observed["canonical_scoped_prop42_has_cited_ancestor"]
    assert set(steps) == set(ancestry)
    assert all(value in (0, 1) for value in steps.values())
    assert all(ancestry[name] for name, count in steps.items() if count == 1)
    assert observed["canonical_scoped_search_status"] in (
        "partial", "search_failed"
    )
    assert observed["canonical_scoped_proven_steps"] >= 0


def test_unproved_hopf_and_root_are_not_short_circuited():
    observed = report()
    assert observed["zero_image_deliberately_outside_r45_scoped_proof"] is True
    assert observed["canonical_scoped_hopf_injectivity_inferred"] is False
    assert observed["canonical_scoped_upper_delta_surjectivity_inferred"] is False
    assert observed["root_complete"] is False
    assert observed["new_givens"] == 0
    assert observed["production_files_changed"] == 0
    assert observed["web_http_checked"] is False
    assert observed["full_pytest"] is False
