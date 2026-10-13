from dataclasses import dataclass
from pathlib import Path

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from hopf_facts import ETA_2, IOTA_3
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r8_source_link import (
    audit_source_link, expand_source_mapped_group_goal,
    find_pi33_source_candidate, find_eta2_hopf_source_candidate,
)
from proof import Relation


def _goal():
    return Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))


def _bridge():
    return build_phase165_r5_manifest_bridge()[0]


def test_diagonal_uses_toda51_adjacent_clause():
    result = find_pi33_source_candidate(_goal(), _bridge())
    assert len(result) == 1
    assert result[0].locator == '(5.1)'
    assert result[0].claim.lhs == TodaPrimaryGroup(3, 3)
    assert result[0].claim.rhs.generator == IOTA_3
    assert result[0].status == 'SOURCE_MAPPED_NOT_CERTIFIED'


def test_generator_image_uses_proposition51_not_equation51():
    result = find_eta2_hopf_source_candidate(_goal())
    assert len(result) == 1
    assert result[0].locator == 'Proposition 5.1'
    assert result[0].claim.source_generator == ETA_2
    assert result[0].claim.target_generator == IOTA_3


def test_root_expansion_has_three_unverified_obligations():
    result = expand_source_mapped_group_goal(_goal(), _bridge())
    assert len(result) == 1
    assert len(result[0].subgoals) == 3
    assert result[0].subgoals[1] == find_pi33_source_candidate(_goal(),_bridge())[0].claim
    assert result[0].subgoals[2] == find_eta2_hopf_source_candidate(_goal())[0].claim


def test_unrelated_generator_has_no_image_or_root_expansion():
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup('unrelated'))
    assert not find_eta2_hopf_source_candidate(goal)
    assert not expand_source_mapped_group_goal(goal, _bridge())


def test_no_proof_certification_from_source_mapping():
    report = audit_source_link(_goal(), _bridge())
    assert report['source_certified'] is False
    assert report['eligible_new_leaves'] == 0
    assert report['proof_steps_created'] == 0
    assert report['legacy_proof_used'] is False
