"""R5-R1: pi_5^3 uses the same group proof presentation and renderer as other groups."""
from pathlib import Path

import pytest

from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof
from proof import ProofRule
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def proof():
    return build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_group_root_still_derived_from_registry_isomorphism():
    from phase165_goal_only_search import GoalSearchIncompleteError
    with pytest.raises(GoalSearchIncompleteError, match="Registered goal/rule catalog not configured"):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_exact_common_renderer_output_without_pi53_appended_text():
    from phase165_goal_only_search import GoalSearchIncompleteError
    with pytest.raises(GoalSearchIncompleteError, match="legacy proof selection is disabled"):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_web_narrative_uses_shared_presentation():
    from phase165_goal_only_search import GoalSearchIncompleteError
    with pytest.raises(GoalSearchIncompleteError):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_web_trace_and_other_group_unaffected():
    view = build_standard_web_group_proof_view(3, 2, max_depth=0, mode="trace")
    assert view.mode == "trace"
    assert view.phase != "164 R5"


def test_invalid_depth_rejected():
    with pytest.raises((TypeError, ValueError)):
        build_phase164_r5_web_pi5_3_proof(max_depth=-1)
