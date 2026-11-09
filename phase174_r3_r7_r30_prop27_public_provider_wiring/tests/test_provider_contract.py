"""R30R1 pre-install regression: the missing provider module is implemented."""
from pathlib import Path
from dataclasses import replace

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, typed_specialization,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    Prop27UniversalLiteratureStatement,
)
from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
    register_positioned_prop27, has_certified_prop27_leaf,
    expand_public_cited_prop27_goal,
)

ROOT = Path(__file__).resolve().parents[2]


def test_exact_manifest_positioned_universal_source():
    bridge = register_positioned_prop27(ROOT)
    assert has_certified_prop27_leaf(bridge)
    assert len(bridge.proof_links) == 1
    assert type(bridge.proof_links[0].step.conclusion) is Prop27UniversalLiteratureStatement


def test_nonexistent_link_never_proposes_a_theorem():
    bridge = register_positioned_prop27(ROOT)
    no_link = RegistryBridgeResult(bridge.registry, bridge.records, ())
    assert not has_certified_prop27_leaf(no_link)
    assert expand_public_cited_prop27_goal(typed_specialization(6), no_link) == ()


def test_cited_general_and_n6_proposals_are_backward_inferences():
    bridge = register_positioned_prop27(ROOT)
    general = expand_public_cited_prop27_goal(Prop27GeneralTheoremPremise(), bridge)
    concrete = expand_public_cited_prop27_goal(typed_specialization(6), bridge)
    assert len(general) == 1
    assert general[0].subgoals == (Prop27UniversalLiteratureStatement(),)
    assert len(concrete) == 1
    assert concrete[0].subgoals == (Prop27GeneralTheoremPremise(),)


def test_invalid_instance_and_unrelated_root_have_no_candidates():
    bridge = register_positioned_prop27(ROOT)
    forged = replace(typed_specialization(6), sign_undetermined=False)
    assert expand_public_cited_prop27_goal(forged, bridge) == ()
    assert expand_public_cited_prop27_goal("pi_12^7=0", bridge) == ()
