"""Compare the real provider with and without the R19 append-only hook."""
from unittest.mock import patch

import pytest

from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase178_r19_finite_cyclic_suspension_transport_isolated import provider
from phase178_r19r1_finite_cyclic_suspension_transport_public import installer
from proof import ProofStep


def signature(options):
    return tuple((o.rule.name, o.subgoals) for o in options)


@pytest.fixture(scope='module')
def base_bridge():
    return build_shared_typed_bridge()


@pytest.mark.parametrize('n,k', [(6,6),(5,6),(3,2),(4,3),(5,5),(7,6)])
def test_append_only_and_no_source_mutation(base_bridge,n,k):
    root = exact_prior_database_result(n,k)
    assert root is not None
    bridge = prefer_universal_prop42_derivation(screen_independent_sources_for_derived_goal(base_bridge,goal=root))
    links = tuple(bridge.proof_links)
    assertions = tuple(bridge.registry._assertions.items())
    original = provider.build_finite_cyclic_suspension_transport_provider(bridge=bridge,proof_target=root)
    with patch.object(provider,'build_finite_cyclic_suspension_transport_provider',return_value=lambda goal: ()):
        baseline = shared_expansion_provider(bridge,proof_target=root)
    actual = shared_expansion_provider(bridge,proof_target=root)
    old = signature(baseline(root))
    additional = signature(original(root))
    expected = old + tuple(x for x in additional if x not in old)
    assert signature(actual(root)) == expected
    for option in original(root):
        assert all(not isinstance(g,ProofStep) for g in option.subgoals)
        for goal in option.subgoals[1:]:
            assert signature(actual(goal)) == signature(baseline(goal))
    assert tuple(bridge.proof_links) == links
    assert tuple(bridge.registry._assertions.items()) == assertions


def test_real_n6_three_premises_and_frontier(base_bridge):
    root = exact_prior_database_result(6,6)
    lower = exact_prior_database_result(5,6)
    bridge = prefer_universal_prop42_derivation(screen_independent_sources_for_derived_goal(base_bridge,goal=root))
    public = shared_expansion_provider(bridge,proof_target=root)
    required = provider.suspension_transport_inputs(root,lower)
    assert required is not None
    selected, = [o for o in public(root) if o.rule.name == 'finite cyclic presentation transported by proved suspension isomorphism' and o.subgoals == required]
    assert selected.rule.literature_reference is None
    assert not any(link.step is not None and link.step.conclusion == root for link in bridge.proof_links)
    print('PHASE178_R19R1_N6_THREE_PUBLIC_PREMISES=VERIFIED')


def test_installer_refuses_missing_or_duplicate_anchors():
    with pytest.raises(RuntimeError):
        installer.proposed_source('def unrelated(): pass\n')
    with pytest.raises(RuntimeError):
        installer.proposed_source(installer.BUILD_ANCHOR * 2 + installer.RETURN_ANCHOR)
    with pytest.raises(RuntimeError):
        installer.proposed_test('def unrelated(): pass\n')
