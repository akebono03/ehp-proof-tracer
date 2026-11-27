"""Real screened registry and public proposals; no fabricated proof premises."""
from dataclasses import replace
import pytest

from homotopy_groups import FiniteCyclicGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, admitted_db_step
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from phase178_r16_toda513_isolated.source import canonical_513
from phase178_r17_finite_cyclic_quotient_isolated.rule import RULE_NAME, finite_cyclic_quotient_inputs
from phase178_r17r1_finite_cyclic_quotient_public.provider import build_public_finite_cyclic_quotient_provider
from proof import ProofStep, Relation


@pytest.fixture(scope='module')
def context():
    root = exact_prior_database_result(5,6)
    assert type(root) is Relation and type(root.rhs) is FiniteCyclicGroup
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, root.rhs.order)
    bridge = prefer_universal_prop42_derivation(screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root))
    return root,goal,bridge


def test_public_candidate_and_six_obligations(context):
    root,goal,bridge = context
    public = shared_expansion_provider(bridge, proof_target=root)
    option, = (o for o in public(goal) if o.rule.name == RULE_NAME)
    middle,source,signed,exact,onto,image = option.subgoals
    assert middle == exact_prior_database_result(4,6)
    assert source == exact_prior_database_result(9,3)
    assert signed == canonical_513()[0]
    assert len(linked_cited_steps(bridge,signed)) == 1
    assert finite_cyclic_quotient_inputs(goal,middle,source,signed,image) == option.subgoals
    assert all(not isinstance(g,ProofStep) for g in option.subgoals)
    assert root not in option.subgoals and goal not in option.subgoals
    assert all(admitted_db_step(g,proof_target=root,bridge=bridge) is not None or linked_cited_steps(bridge,g) for g in (middle,source))
    assert all(public(g) for g in (exact,onto,image))
    print('PHASE178_R17R1_PUBLIC_CANDIDATE_COUNT=1')
    print('PHASE178_R17R1_SIX_OBLIGATIONS=VERIFIED')


def test_source_removed_disables_candidate(context):
    root,goal,bridge = context
    signed = canonical_513()[0]
    reduced = RegistryBridgeResult(bridge.registry,bridge.records,tuple(l for l in bridge.proof_links if l.step is None or l.step.conclusion != signed))
    assert not build_public_finite_cyclic_quotient_provider(bridge=reduced,proof_target=root)(goal)
    assert not any(o.rule.name == RULE_NAME for o in shared_expansion_provider(reduced,proof_target=root)(goal))


def test_wrong_order_or_root_refused(context):
    root,goal,bridge = context
    provider = build_public_finite_cyclic_quotient_provider(bridge=bridge,proof_target=root)
    assert not provider(replace(goal,order=4))
    assert not provider(root)
    assert not build_public_finite_cyclic_quotient_provider(bridge=bridge,proof_target=None)(goal)
    wrong = Relation(root.lhs,FiniteCyclicGroup(4,goal.generator))
    assert not build_public_finite_cyclic_quotient_provider(bridge=bridge,proof_target=wrong)(goal)
    assert not build_public_finite_cyclic_quotient_provider(bridge=bridge,proof_target=wrong)(replace(goal,order=4))


def test_no_db_admission_no_route(context,monkeypatch):
    root,goal,bridge = context
    import phase178_r17r1_finite_cyclic_quotient_public.provider as module
    monkeypatch.setattr(module,'admitted_prior_group_step',lambda *args,**kwargs: None)
    # R17 actual premises have no screened concrete group GIVENs.
    assert not module.build_public_finite_cyclic_quotient_provider(bridge=bridge,proof_target=root)(goal)
