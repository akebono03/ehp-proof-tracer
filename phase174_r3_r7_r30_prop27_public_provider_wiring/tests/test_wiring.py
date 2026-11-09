"""Only R30 production connections and strict provenance regressions."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge, shared_expansion_provider,
)
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, typed_specialization,
)
from phase174_r3_r7_r30_prop27_public_provider_wiring.audit import audit_public_wiring
from phase174_r3_r7_r30_prop27_public_provider_wiring.install import (
    BRIDGE_ADDITION, PROVIDER_ADDITION, patch_source, preflight,
)
from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
    expand_public_cited_prop27_goal, has_certified_prop27_leaf,
    register_positioned_prop27,
)

ROOT = Path(__file__).resolve().parents[2]


def test_source_patching_idempotent_and_scoped():
    sample = (ROOT / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8-sig")
    patched = patch_source(sample)
    assert patch_source(patched) == patched
    assert patched.count(BRIDGE_ADDITION) == 1
    assert patched.count(PROVIDER_ADDITION) == 1


def test_reviewed_manifest_connects_real_proposition_source_order():
    bridge = register_positioned_prop27(ROOT)
    ref = next(iter(bridge.registry._references.values()))
    assert ref.locator == "Proposition 2.7"
    assert type(ref.publication_position) is int
    assert ref.publication_position > 0
    assert has_certified_prop27_leaf(bridge)


def test_forged_or_missing_link_does_not_offer_inference():
    original = register_positioned_prop27(ROOT)
    absent = RegistryBridgeResult(original.registry, original.records, ())
    assert not has_certified_prop27_leaf(absent)
    assert expand_public_cited_prop27_goal(typed_specialization(6), absent) == ()
    assert expand_public_cited_prop27_goal("pi_12^7=0", original) == ()
    assert expand_public_cited_prop27_goal(
        replace(typed_specialization(6), sign_undetermined=False), original,
    ) == ()


@pytest.mark.parametrize("n", [2, 4, 6, 8])
def test_default_shared_provider_has_source_derived_general_rule(n):
    bridge = build_shared_typed_bridge()
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    assert has_certified_prop27_leaf(screened)
    provider = shared_expansion_provider(screened, proof_target=goal)
    target = typed_specialization(n)
    assert any(option.subgoals == (Prop27GeneralTheoremPremise(),)
               for option in provider(target))


def test_full_public_source_screen_and_canonical_inference():
    report = audit_public_wiring()
    assert report["public_verified_n6_inference"] is True
    assert report["delta_surjectivity_proved"] is False
    assert report["root_complete"] is False


def test_source_guard_accepts_reviewed_change():
    _head, _expected, installed = preflight()
    assert installed is True
