import pytest
from homotopy_groups import TodaPrimaryGroup,TodaSuspensionMap
from phase165_r14_r19_registry_gate import (
    DiagonalSourceReview, reviewed_diagonal_bridge, audit_r19,
)
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r18_diagonal_integration import derive_diagonal_iso_from_certified_groups
from phase165_r2_registry_lookup import find_eligible_goal_candidates
from phase165_r14_r15_typed_diagonal import match_diagonal_toda51_claims

IDS = ("phase165:r14r19:toda51:diagonal:n1","phase165:r14r19:toda51:diagonal:n2")

def test_unreviewed_no_registration():
    base, _ = build_phase165_r5_manifest_bridge()
    bridge, ids, status = reviewed_diagonal_bridge(base)
    assert bridge is base and ids == () and status == "REVIEW_REQUIRED"

def test_wrong_review_ids_rejected():
    base, _ = build_phase165_r5_manifest_bridge()
    with pytest.raises(ValueError):
        reviewed_diagonal_bridge(base,DiagonalSourceReview(("wrong","wrong"),True))

def test_reviewed_typed_entries_are_isolated():
    base, _ = build_phase165_r5_manifest_bridge()
    before = len(base.registry._assertions)
    bridge, ids, status = reviewed_diagonal_bridge(base,DiagonalSourceReview(IDS,True))
    assert len(ids)==2
    assert len(base.registry._assertions)==before
    assert len(bridge.registry._assertions)==before+2
    assert status=="REVIEWED_ADOPTED_TEX"

def test_reviewed_group_steps_can_drive_general_iso_rule():
    base,_=build_phase165_r5_manifest_bridge()
    bridge,ids,_=reviewed_diagonal_bridge(base,DiagonalSourceReview(IDS,True))
    suspension=TodaSuspensionMap(TodaPrimaryGroup(1,1),TodaPrimaryGroup(2,2))
    goals=match_diagonal_toda51_claims(suspension)
    steps=tuple(next(link.step for link in bridge.proof_links if link.assertion_id==aid) for aid in ids)
    assert tuple(s.conclusion for s in steps)==tuple(row.goal for row in goals[:2])
    derived=derive_diagonal_iso_from_certified_groups(suspension,*steps)
    assert derived.conclusion.map==suspension
    assert len(derived.premises)==3

def test_review_gate_does_not_automatically_approve_citations():
    base,_=build_phase165_r5_manifest_bridge()
    bridge,ids,_=reviewed_diagonal_bridge(base,DiagonalSourceReview(IDS,True))
    for aid in ids:
        result=find_eligible_goal_candidates(bridge,bridge.registry.assertion(aid).content,aid)
        assert result==()

def test_audit_not_a_proof():
    report=audit_r19()
    assert report["new_proof_steps"]==0
    assert report["fail_closed_unreviewed"]
