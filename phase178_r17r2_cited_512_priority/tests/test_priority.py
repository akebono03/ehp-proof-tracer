"""Only existing screened cited candidates move; ordinary fallback remains."""
import pytest
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase178_r15_toda512_isolated.source import canonical_512
from phase178_r15_toda512_isolated.provider import RULE_NAME
from phase177_r14_finite_cyclic_delta_injective_isolated.rule import INJECTIVE_RULE
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result


@pytest.fixture(scope='module')
def bridge():
    return build_shared_typed_bridge()


@pytest.mark.parametrize('n', (4,5,6))
def test_screened_cited_candidate_first(bridge,n):
    root = exact_prior_database_result(n+1,6)
    assert root is not None
    screened = screen_independent_sources_for_derived_goal(bridge,goal=root)
    claim = canonical_512(n)
    options = shared_expansion_provider(screened,proof_target=root)(claim.statement)
    assert options[0].rule.name == RULE_NAME
    assert options[0].subgoals == (claim,)
    assert sum(o.rule.name == RULE_NAME for o in options) == 1
    if n == 4:
        assert any(o.rule.name == INJECTIVE_RULE for o in options[1:])
    reduced = RegistryBridgeResult(screened.registry,screened.records,
        tuple(l for l in screened.proof_links if l.step is None or l.step.conclusion != claim))
    fallback = shared_expansion_provider(reduced,proof_target=root)(claim.statement)
    assert not any(o.rule.name == RULE_NAME for o in fallback)
    if n == 4:
        assert any(o.rule.name == INJECTIVE_RULE for o in fallback)
