"""Targeted R52-R7 tests: registered R38 proof and generic routing."""
from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r7_registered_common_proof import (
    RegisteredProofProvider, build_registered_common_replay,
    registered_proof_providers,
)
from phase164_r5_r2_common_replay import build_phase164_r5_r2_common_replay
from phase165_goal_only_search import GoalSearchIncompleteError
from toda_calculation_facade import build_standard_toda_report
from web_group_proof import build_standard_web_group_proof_view


def _group_result(n, k):
    report = build_standard_toda_report(n=n, k=k)
    return report.candidates[0].source_candidate.group_result


def test_r7_pi32_regenerates_registered_backward_proof():
    result = build_phase164_r5_r2_common_replay(
        2, 1, _group_result(2, 1), 2, "narrative",
    )
    assert result.root_step.conclusion.lhs == TodaPrimaryGroup(3, 2)
    assert result.source_entry.phase == "165"
    assert result.source_entry.key == "phase165:registered:pi3_2"
    assert result.max_depth >= 2
    assert len(result.steps) > 1


def test_r7_pi32_original_narrative_still_visible():
    view = build_standard_web_group_proof_view(2, 1, max_depth=2, mode="narrative")
    text = "\n".join(line.prefix + " " + " ".join(
        segment.value for segment in line.segments
    ) for line in view.rendered_lines)
    assert "証明対象" in text
    assert "使用する結果" in text
    assert "証明" in text
    assert view.phase == "165"


def test_r7_pi32_trace_is_bounded():
    result = build_phase164_r5_r2_common_replay(2, 1, _group_result(2, 1), 1, "trace")
    assert result.max_depth == 1
    assert max(step.depth for step in result.steps) <= 1


def test_r7_unregistered_goal_fail_closed():
    source = _group_result(2, 1)
    alternate = replace(source, target=TodaPrimaryGroup(4, 3))
    with pytest.raises(GoalSearchIncompleteError):
        build_registered_common_replay(
            group_result=alternate, max_depth=2, mode="narrative",
            providers=registered_proof_providers(),
        )


def test_r7_duplicate_goal_provider_rejected():
    source = _group_result(2, 1)
    provider = registered_proof_providers()[0]
    with pytest.raises(GoalSearchIncompleteError):
        build_registered_common_replay(
            group_result=source, max_depth=2, mode="narrative",
            providers=(provider, provider),
        )


def test_r7_invalid_depth_and_mode_rejected():
    source = _group_result(2, 1)
    for invalid in (True, -1, "2"):
        with pytest.raises(ValueError):
            build_registered_common_replay(
                group_result=source, max_depth=invalid, mode="narrative",
            )
    with pytest.raises(ValueError):
        build_registered_common_replay(group_result=source, max_depth=2, mode="strange")
