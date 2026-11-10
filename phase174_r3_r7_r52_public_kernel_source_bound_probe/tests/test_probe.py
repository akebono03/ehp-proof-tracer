"""R52 tests the generic proposal shape and real canonical proof boundaries."""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r3_recursive_search import SourceBoundGoal
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import upper_delta_surjectivity_inputs
from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
from phase174_r3_r7_r52_public_kernel_source_bound_probe.audit import (
    inspect_public_kernel_source_bound_probe,
)
from phase174_r3_r7_r52_public_kernel_source_bound_probe.probe import (
    build_source_bound_kernel_probe,
)


def proposal_contract(option: object) -> tuple[object, ...]:
    """Compare a generated rule's public contract, not closure identity."""
    rule = option.rule
    return (
        type(rule), rule.name, rule.description,
        rule.premise_patterns, rule.conclusion_pattern,
        rule.literature_reference, option.subgoals,
    )


def test_generic_wrapper_adds_only_cited_r35_kernel_obligation() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    original = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(original, goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    wrapper = build_source_bound_kernel_probe(provider, screened)
    upper = ehp_zero_inputs(root)[0]
    kernel = upper_delta_surjectivity_inputs(upper)[2]
    before = provider(kernel)
    after = wrapper(kernel)
    bound = tuple(x for x in after if x.rule.name == KERNEL_RULE
                  and isinstance(x.subgoals[0], SourceBoundGoal))
    assert all(x.rule.name == KERNEL_RULE for x in bound)
    original_r35 = tuple(x for x in before if x.rule.name == KERNEL_RULE)
    assert len(original_r35) == 1
    assert all(x.subgoals[0].conclusion == original_r35[0].subgoals[0]
               for x in bound)
    assert tuple(proposal_contract(x) for x in after[-len(before):]) == tuple(
        proposal_contract(x) for x in before
    )
    assert tuple(proposal_contract(x) for x in wrapper(root)) == tuple(
        proposal_contract(x) for x in provider(root)
    )


def test_generated_rule_closure_identity_does_not_change_root_contract() -> None:
    """A provider may rebuild an equivalent inference guard on each call."""
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        expand_ehp_zero_from_delta_surjectivity,
    )

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    first = expand_ehp_zero_from_delta_surjectivity(goal)
    second = expand_ehp_zero_from_delta_surjectivity(goal)
    assert len(first) == len(second) == 1
    assert first[0].rule.match_guard is not second[0].rule.match_guard
    assert proposal_contract(first[0]) == proposal_contract(second[0])


def test_missing_screened_cited_proof_link_never_adds_source_bound() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    no_links = RegistryBridgeResult(screened.registry, screened.records, ())
    wrapper = build_source_bound_kernel_probe(provider, no_links)
    kernel = upper_delta_surjectivity_inputs(ehp_zero_inputs(root)[0])[2]
    assert tuple(proposal_contract(x) for x in wrapper(kernel)) == tuple(
        proposal_contract(x) for x in provider(kernel)
    )


def test_probe_reports_actual_canonical_progress_and_does_not_claim_web() -> None:
    report = inspect_public_kernel_source_bound_probe()
    assert report["public_provider_unchanged"] is True
    assert report["public_web_http_checked"] is False
    assert type(report["probe_r35_source_bound_candidates"]) is int
    assert report["probe_r35_source_bound_candidates"] >= 0
    assert report["public_r35_unbound_candidates"] == 1
    assert report["probe_root_candidate_unchanged"] is True
    assert report["new_given"] == 0
    assert report["new_mathematical_rules"] == 0
    assert report["production_files_changed"] == 0
    if report["probe_status"] == "complete":
        assert report["probe_root_complete"] is True
        assert report["probe_root_inference_count"] == 1
        assert report["probe_root_four_inferred_parents"] is True
        assert report["probe_root_six_cited_ancestors"] is True
        assert report["probe_kernel_domain_inferred"] is True
    else:
        assert report["probe_root_inference_count"] == 0
        assert report["probe_root_complete"] is False
        assert report["probe_open_goal_types"]
