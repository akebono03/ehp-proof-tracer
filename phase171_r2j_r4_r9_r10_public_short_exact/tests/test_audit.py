"""Focused short-exact public-provider and fail-closed proof tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r5_short_exact_sequence.audit import build_short_exact_proof
from phase171_r2j_r4_r5_short_exact_sequence.source import (
    EHPShortExactSequence,
    expand_ehp_short_exact,
    short_exact_from_ehp,
)
from phase171_r2j_r4_r9_r10_public_short_exact.audit import (
    _git,
    equivalent_short_exact_routes,
    inspect_public_short_exact,
)
from phase171_r2j_r4_r9_r10_public_short_exact.install import (
    R10_HOOK,
    _complete_function,
    install,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def _premises():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    c = TodaPrimaryGroup(6, 5)
    return (
        MapInjective(TodaSuspensionMap(a, b)),
        TodaProp42ExactnessStatement(TodaEHPExactnessWindow(a, b, c, EHP_E_MAP, EHP_H_MAP)),
        MapSurjective(TodaHopfInvariantMap(b, c)),
    )


def test_generic_short_exact_requires_only_three_unproven_typed_subgoals():
    goal = short_exact_from_ehp(*_premises())
    assert isinstance(goal, EHPShortExactSequence)
    proposal, = expand_ehp_short_exact(goal)
    assert proposal.subgoals == _premises()
    assert all(not isinstance(item, ProofStep) for item in proposal.subgoals)


def test_short_exact_rule_refuses_given_map_properties():
    goal = short_exact_from_ehp(*_premises())
    proposal, = expand_ehp_short_exact(goal)
    for forged in range(3):
        parents = tuple(ProofStep(value, (), ProofRule.GIVEN if i == forged else ProofRule.INFERENCE)
                        for i, value in enumerate(proposal.subgoals))
        assert find_inference_matches_for_rule(proposal.rule, parents) == ()


def test_malformed_ehp_window_or_wrong_middle_group_fails_closed():
    injection, exact, hopf = _premises()
    goal = short_exact_from_ehp(injection, exact, hopf)
    assert goal is not None
    assert expand_ehp_short_exact(replace(goal, middle_group=TodaPrimaryGroup(7, 3))) == ()
    assert short_exact_from_ehp(injection, replace(exact, window=replace(
        exact.window, first_map=EHP_DELTA_MAP,
    )), hopf) is None
    assert expand_ehp_short_exact(object()) == ()


def test_wrong_map_endpoints_are_not_accepted():
    injection, exact, hopf = _premises()
    assert short_exact_from_ehp(replace(injection, map=TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    )), exact, hopf) is None
    assert short_exact_from_ehp(injection, exact, replace(hopf, map=TodaHopfInvariantMap(
        TodaPrimaryGroup(6, 4), TodaPrimaryGroup(6, 5),
    ))) is None


def test_shared_provider_reuses_actual_verified_ehp_rule():
    screened, target, _ = _screened_context()
    root, _, report = build_short_exact_proof()
    candidates = shared_expansion_provider(screened, proof_target=target)(root.conclusion)
    assert equivalent_short_exact_routes(candidates, root) == 1
    assert report["new_given_added"] == 0
    assert len(root.premises) == 3


def test_public_audit_never_reports_fabricated_group_or_success():
    report = inspect_public_short_exact()
    assert report["shared_short_exact_connected"] is True
    assert report["short_exact_inference_matched"] is True
    assert report["completed_proof_imported"] is False
    assert report["new_given_added"] == 0
    assert report["public_search_status"] in ("complete", "partial", "search_failed")
    if report["public_complete"]:
        assert report["public_search_status"] == "complete"
        assert report["public_open_goals"] == []


def test_patch_keeps_full_function_and_is_idempotent_in_dry_run():
    assert install(dry_run=True) is False
    content = (pytest.importorskip("phase165_r52_r9_shared_math").__file__)
    from pathlib import Path
    source = Path(content).read_text(encoding="utf-8-sig")
    function = _complete_function(source.replace("\r\n", "\n"))
    assert function.count(R10_HOOK) == 1
    assert "def shared_expansion_provider(" in function


def test_git_guard_prevents_mutating_commands():
    with pytest.raises(ValueError):
        _git("reset", "--hard")
