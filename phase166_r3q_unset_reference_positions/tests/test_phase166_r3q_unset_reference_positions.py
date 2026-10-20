"""Small tests of reviewed source mapping and existing Web regression boundary."""
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase166_r3l_reference_order import REVIEWED_REFERENCE_ALIASES
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal

IDS = (
    'shared:1:adopted:ref:7',
    'shared:1:adopted:ref:8',
    'shared:1:adopted:ref:9',
    'shared:5:adopted:reference:prop42:general',
)

def test_r3q_prop42_reviewed_aliases_have_identical_manifest_target():
    for ref_id in IDS:
        suffix = ref_id.split(':', 2)[2]
        assert REVIEWED_REFERENCE_ALIASES[suffix] == 'toda:Proposition 4.2'


def test_r3q_prop42_four_references_have_same_registered_order():
    bridge = build_shared_typed_bridge()
    positions = {bridge.registry.reference(ref_id).publication_position for ref_id in IDS}
    assert len(positions) == 1
    assert None not in positions
    for ref_id in IDS:
        assert bridge.registry.reference(ref_id).locator.startswith('Proposition 4.2')


def test_r3q_existing_r3p_locations_remain_unchanged():
    bridge = build_shared_typed_bridge()
    assert bridge.registry.reference('shared:1:adopted:ref:3').publication_position == 7701
    assert bridge.registry.reference('shared:7:adopted:reference:toda5:eta_family_definition').publication_position == 7800
    assert bridge.registry.assertion('shared:7:adopted:assertion:toda5:eta_family_definition').component_position == 300


def test_r3q_pi32_existing_search_stays_complete():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
