"""R53 source-first generic kernel binding and real public Group query."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import SourceBoundGoal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import upper_delta_surjectivity_inputs
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
from phase174_r3_r7_r53_public_source_bound_kernel.provider import (
    build_public_source_bound_kernel_provider,
)
from phase174_r3_r7_r53_public_source_bound_kernel.audit import inspect_public_root_completion
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


def test_cited_generic_kernel_prefers_source_bound_but_retains_fallback() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    base = shared_expansion_provider(screened, proof_target=root)
    improved = build_public_source_bound_kernel_provider(base, screened)
    kernel = upper_delta_surjectivity_inputs(ehp_zero_inputs(root)[0])[2]
    before = tuple(x for x in base(kernel) if x.rule.name == KERNEL_RULE)
    after = tuple(x for x in improved(kernel) if x.rule.name == KERNEL_RULE)
    assert len(before) == 1
    assert len(after) >= 2
    assert isinstance(after[0].subgoals[0], SourceBoundGoal)
    assert after[0].subgoals[0].conclusion == before[0].subgoals[0]
    assert after[-1].subgoals == before[0].subgoals
    assert improved(root)[0].subgoals == base(root)[0].subgoals


def test_missing_independent_cited_step_never_adds_bound_candidate() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    base = shared_expansion_provider(screened, proof_target=root)
    empty = RegistryBridgeResult(screened.registry, screened.records, ())
    improved = build_public_source_bound_kernel_provider(base, empty)
    kernel = upper_delta_surjectivity_inputs(ehp_zero_inputs(root)[0])[2]
    before = tuple(x for x in base(kernel) if x.rule.name == KERNEL_RULE)
    after = tuple(x for x in improved(kernel) if x.rule.name == KERNEL_RULE)
    assert len(after) == len(before) == 1
    assert all(not isinstance(x.subgoals[0], SourceBoundGoal) for x in after)


def test_actual_public_zero_goal_is_completed_by_verified_proof_steps() -> None:
    result = search_group_from_registered_goal(n=7, k=5)
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == goal
    assert result.open_goals == ()
    roots = tuple(x for x in result.proven_steps
                  if x.rule is ProofRule.INFERENCE and x.conclusion == goal)
    assert len(roots) == 1
    assert len(roots[0].premises) == 4
    assert all(x.rule is ProofRule.INFERENCE for x in roots[0].premises)


def test_public_web_model_uses_common_verified_renderer() -> None:
    view = build_standard_web_group_proof_view(
        n=7, k=5, max_depth=2, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert view.rendered_lines
    assert view.n == 7 and view.k == 5


def test_public_audit_rechecks_citations_in_one_real_tree() -> None:
    report = inspect_public_root_completion()
    assert report["public_root_complete"] is True
    assert report["public_kernel_domain_cited_inference"] is True
    assert report["public_root_four_inferred_parents"] is True
    assert report["public_root_six_cited_ancestors"] is True
    assert report["public_web_key"] == "generic-complete-proof"
    assert report["public_http_checked"] is False
    assert report["new_given"] == 0
    assert report["new_mathematical_rules"] == 0
