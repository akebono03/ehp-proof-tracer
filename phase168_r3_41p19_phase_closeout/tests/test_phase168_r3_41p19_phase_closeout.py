"""Phase 168 final gate: typed target is part of an accepted proof."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from phase168_r3_38_frozen_fulltext_audit.audit import capture
from proof import ProofRule


@pytest.fixture(scope="module")
def canonical_cases():
    cases = {}
    for name, n, k, expected in (
        ("pi3_2", 2, 1, (13, 5)),
        ("pi4_3", 3, 1, (19, 6)),
        ("pi5_4", 4, 1, (7, 3)),
    ):
        bridge = build_shared_typed_bridge()
        screens = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=screens.append,
        )
        assert result.status is ProofSearchStatus.COMPLETE
        assert screens
        citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        assert citing is not None
        cases[name] = (result, screens[-1], citing, expected, n, k)
    return cases


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3", "pi5_4"))
def test_canonical_targets_pass_and_rendering_is_byte_identical(canonical_cases, name):
    result, screened, citing, expected, n, k = canonical_cases[name]
    assert verify_proof_tree_for_narrative(
        result, screened, citing_assertion_id=citing,
    ) == expected
    rendered, model, view = capture(n, k)
    baseline = (Path(__file__).resolve().parents[2]
                / "phase168_r3_41p12_publication_boundary_audit"
                / "baselines" / (name + ".md"))
    assert rendered == baseline.read_text(encoding="utf-8")
    assert len(model.steps) == sum(expected)
    assert not view.partial_result


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3", "pi5_4"))
def test_mismatched_typed_target_is_rejected(canonical_cases, name):
    result, screened, citing, expected, n, k = canonical_cases[name]
    different = TodaPrimaryGroup(
        group_dimension=result.target.group_dimension + 1,
        sphere_dimension=result.target.sphere_dimension,
    )
    altered = replace(result, target=different)
    assert altered.proven_steps is result.proven_steps
    with pytest.raises(UnverifiedProofTree, match="target does not match group"):
        verify_proof_tree_for_narrative(
            altered, screened, citing_assertion_id=citing,
        )


def test_this_phase_does_not_promote_observational_origins_to_trust():
    from phase168_r3_41p17_origin_handoff.origin_handoff import (
        build_origin_bound_narrative_model,
    )
    import inspect
    from web_group_proof import build_standard_web_group_proof_view
    code = inspect.getsource(build_standard_web_group_proof_view)
    assert "verify_proof_tree_for_narrative" in code
    assert "build_origin_bound_narrative_model" not in code
    assert callable(build_origin_bound_narrative_model)


def test_two_compatibility_projection_guards_remain():
    from phase168_r3_27_typed_statement_projection import (
        project_stable_eta_notation_transition,
        typed_sentence,
    )
    import inspect
    assert "_stable_eta_renaming_shape" in inspect.getsource(project_stable_eta_notation_transition)
    assert "prop42_exactness_indices" in inspect.getsource(typed_sentence)
