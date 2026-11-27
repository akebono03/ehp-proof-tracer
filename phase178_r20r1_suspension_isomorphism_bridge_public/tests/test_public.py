"""Verify public bridge proposals without bypassing the screened source context."""
import importlib.util
from unittest.mock import patch

import pytest
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement
from phase165_r14_r6_generic_iso import MapIsomorphism, MapInjective, MapSurjective
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase178_r20_suspension_isomorphism_bridge_isolated import rule
from phase178_r20r1_suspension_isomorphism_bridge_public import installer
from proof import ProofStep, ProofRule


def signature(options):
    return tuple((o.rule.name, o.subgoals) for o in options)


@pytest.fixture(scope='module')
def context():
    root = exact_prior_database_result(6,6)
    bridge = prefer_universal_prop42_derivation(screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root))
    return root, bridge


@pytest.mark.parametrize('n,k', [(3,2),(5,6),(6,6),(8,3)])
def test_append_only(context,n,k):
    root,bridge = context
    original_links, original_assertions = tuple(bridge.proof_links), tuple(bridge.registry._assertions.items())
    e = TodaSuspensionMap(TodaPrimaryGroup(n+k,n), TodaPrimaryGroup(n+k+1,n+1))
    goal = TodaSuspensionIsomorphismStatement(e)
    public = shared_expansion_provider(bridge,proof_target=root)
    extra = signature(rule.expand_suspension_isomorphism_bridge(goal))
    with patch.object(rule,'expand_suspension_isomorphism_bridge',return_value=()):
        baseline = signature(public(goal))
        unchanged = tuple(signature(public(g)) for g in (root, MapIsomorphism(e),MapInjective(e),MapSurjective(e)))
    assert signature(public(goal)) == baseline + tuple(x for x in extra if x not in baseline)
    assert tuple(signature(public(g)) for g in (root,MapIsomorphism(e),MapInjective(e),MapSurjective(e))) == unchanged
    assert all(not isinstance(g,ProofStep) for o in public(goal) if o.rule.name == rule.RULE_NAME for g in o.subgoals)
    assert tuple(bridge.proof_links) == original_links
    assert tuple(bridge.registry._assertions.items()) == original_assertions


def test_historical_proof_still_replays():
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
    from phase168_r3_41p13_trust_boundary.verification import verify_proof_tree_for_narrative
    spec = importlib.util.spec_from_file_location('_r20r1_historical', installer.ROOT/installer.R4C)
    assert spec is not None and spec.loader is not None
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)
    screened, _, citing, public = legacy._real_context()
    e = legacy._map()
    goal = TodaSuspensionIsomorphismStatement(e)
    proof = reconstruct_registered_goal(goal,screened,citing,public,lookup_mode='typed_reference')
    assert proof.conclusion == goal and proof.rule is ProofRule.INFERENCE
    assert tuple(p.conclusion for p in proof.premises) == (MapInjective(e),MapSurjective(e))
    result = PartialProofResult(target=e.target_group,status=ProofSearchStatus.COMPLETE,proven_steps=(proof,),conclusion=goal)
    verify_proof_tree_for_narrative(result,screened,citing_assertion_id=citing)
    print('PHASE178_R20R1_HISTORICAL_REPLAY=VERIFIED')
