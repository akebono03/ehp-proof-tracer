"""Focused R16 tests: guards, reports and canonical-map diagnostic shapes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from phase171_r2j_r4_r9_r16_hopf_route_audit import audit


def test_git_operations_are_read_only():
    with pytest.raises(ValueError):
        audit.git_read("reset", "--hard")
    with pytest.raises(ValueError):
        audit.git_read("add", "phase165_r52_r9_shared_math.py")


def test_reviewed_provider_and_head():
    data = audit.preflight()
    assert data["branch"] == "develop"
    assert len(data["head"]) == 40
    assert data["provider_blob"] == audit.REVIEWED_PROVIDER_BLOB


def test_r14_r15_report_link_is_checked():
    data = audit.read_prior_reports()
    assert data["r14_search"] == "partial"
    assert data["r15_no_derivation_goals"] == 16
    assert data["r15_classes"] == {"PROPOSALS_UNPROVED": 15, "NO_EXPANSION": 1}
    assert len(data["r14_sha256"]) == 64
    assert len(data["r15_sha256"]) == 64


def test_classification_has_no_success_from_available_routes():
    routes = [{"rule": "an inference route", "subgoals": ["unproved"]}]
    assert audit.observation_class(routes, "unresolved") == "ROUTES_EXIST_BUT_NOT_PROVED"
    assert audit.observation_class([], "unresolved") == "NO_PROVIDER_ROUTE"
    assert audit.observation_class(routes, "proved") == "INDEPENDENTLY_PROVED"


def test_false_suspension_isomorphism_is_not_connected():
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context

    screened, group_root, _ = _screened_context()
    source = TodaPrimaryGroup(5, 2)
    target = TodaPrimaryGroup(6, 3)
    iso = TodaSuspensionIsomorphismStatement(TodaSuspensionMap(source, target))
    provider = shared_expansion_provider(screened, proof_target=group_root)
    assert provider(iso) == ()


def test_hopf_map_provider_exposes_real_obligations_only():
    from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase165_r3_recursive_search import GoalExpansion

    screened, group_root, _ = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=group_root)
    goal = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))
    proposals = provider(goal)
    assert isinstance(proposals, tuple)
    assert all(isinstance(item, GoalExpansion) for item in proposals)
    assert all(not hasattr(subgoal, "premises") for item in proposals for subgoal in item.subgoals)
