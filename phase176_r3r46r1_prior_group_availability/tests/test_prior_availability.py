"""Focused admission, pruning, and existing inference-provider contracts."""
from __future__ import annotations

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion, RegisteredGoalUnresolved, reconstruct_registered_goal
from phase169_r10e4_ordered_db_prior import db_prior
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME
from phase176_r3r46r1_prior_group_availability.apply import ROOT, PINS, updated_source
from phase176_r3r46r1_prior_group_availability.provider import build_prior_zero_image_provider
from phase176_r3r46r1_prior_group_availability.pruning import contradiction_witness
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep
from unified_statement_registry import AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry


def root_and_group(n=2, k=5, target_n=3, target_k=5):
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(target_n + target_k, target_n))
    group = TodaPrimaryGroup(n + k, n)
    return root, group


def bridge_fixture(*, zero=None, later=False):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('target', ReferenceKind.PROPOSITION, 'test target', publication_position=2))
    registry.add_reference(LiteratureEntry('src', ReferenceKind.PROPOSITION, 'test premise', publication_position=3 if later else 1))
    registry.add_assertion(AssertionEntry('root', 'target', AssertionKind.STATEMENT, 'test root'))
    registry.add_assertion(AssertionEntry('good', 'src', AssertionKind.STATEMENT, 'good'))
    links = [ProofStepLink('good', step=ProofStep('good', (), ProofRule.GIVEN))]
    if zero is not None:
        registry.add_assertion(AssertionEntry('zero', 'src', AssertionKind.STATEMENT, zero))
        links.append(ProofStepLink('zero', step=ProofStep(zero, (), ProofRule.GIVEN)))
    return RegistryBridgeResult(registry, (), tuple(links))


def witness(zero, root, bridge, mode='typed_reference_publication'):
    return contradiction_witness(zero, bridge=bridge, citing_id='root', lookup_mode=mode,
                                 verified_assertion_ids=(), proof_target=root)


@pytest.mark.parametrize('n,k,target_n,target_k', [(2,5,3,5),(5,5,7,5),(3,4,2,5)])
def test_discovery_matches_exact_existing_admission(n,k,target_n,target_k):
    root, group = root_and_group(n,k,target_n,target_k)
    statement = db_prior.exact_prior_database_result(n,k)
    assert statement is not None
    step = db_prior.admitted_prior_group_step(group, proof_target=root)
    assert step is not None
    assert step == db_prior.admitted_db_step(statement, proof_target=root)
    assert db_prior.verified_db_step(step, proof_target=root)


def test_discovery_rejects_self_later_invalid_and_untyped_root():
    root, group = root_and_group()
    assert db_prior.admitted_prior_group_step(root.group, proof_target=root) is None
    assert db_prior.admitted_prior_group_step(TodaPrimaryGroup(9,4), proof_target=root) is None
    assert db_prior.admitted_prior_group_step(TodaPrimaryGroup(True,2), proof_target=root) is None
    assert db_prior.admitted_prior_group_step(group, proof_target='untyped') is None


def test_missing_explicit_row_cannot_supply_admitted_step(tmp_path):
    root, group = root_and_group()
    missing = tmp_path / 'missing.csv'
    assert db_prior.admitted_prior_group_step(group, proof_target=root, csv_path=missing) is None


def test_db_prior_rejects_zero_without_toda52_or_reproof():
    root, group = root_and_group()
    bridge = bridge_fixture()
    zero = TodaPrimaryGroupZeroStatement(group)
    step = witness(zero, root, bridge)
    assert step is not None and step.rule is ProofRule.GIVEN
    assert db_prior.verified_db_step(step, proof_target=root, bridge=bridge)
    assert witness(zero, root, bridge, mode='legacy') is None
    assert witness(TodaPrimaryGroupZeroStatement(root.group), root, bridge) is None


def test_exact_eligible_zero_reference_precedes_conflicting_database_prior():
    root, group = root_and_group()
    zero = TodaPrimaryGroupZeroStatement(group)
    assert witness(zero, root, bridge_fixture(zero=zero)) is None
    assert witness(zero, root, bridge_fixture(zero=zero, later=True)) is not None


def test_adopted_prior_zero_preflight_skips_all_siblings_and_keeps_next_route():
    root, group = root_and_group()
    zero = TodaPrimaryGroupZeroStatement(group)
    # Use a nonzero root presentation to avoid a separate root-zero DB issue.
    root_goal = db_prior.exact_prior_database_result(3,5)
    assert root_goal is not None
    bridge = bridge_fixture()
    called, events = [], []
    rule = InferenceRule(name='test-only fallback', premise_patterns=(PremisePattern(statement_type=str),),
                         conclusion_pattern=root_goal)

    def provider(goal):
        called.append(goal)
        if goal == root_goal:
            return (GoalExpansion(object(), ('unnecessary', zero)), GoalExpansion(rule, ('good',)))
        return ()

    result = reconstruct_registered_goal(root_goal, bridge, 'root', provider,
                  lookup_mode='typed_reference_publication', progress_observer=lambda *args: events.append(args))
    assert result.conclusion == root_goal and result.inference_rule is rule
    assert called == [root_goal]
    assert not any(event[1] in (zero,'unnecessary') for event in events)


def test_unadmitted_zero_goal_is_not_pruned():
    root, group = root_and_group()
    # The same root is never an admitted earlier result.
    called = []
    with pytest.raises(RegisteredGoalUnresolved, match='found 0'):
        reconstruct_registered_goal(root, bridge_fixture(), 'root', lambda g: called.append(g) or (),
                                    lookup_mode='typed_reference_publication')
    assert called == [root]


@pytest.mark.parametrize('n,k,target_n,target_k', [(2,5,3,5),(5,5,7,5)])
def test_zero_image_provider_uses_existing_r40_without_stable_source_gate(n,k,target_n,target_k):
    root, group = root_and_group(n,k,target_n,target_k)
    bridge = bridge_fixture()
    statement = db_prior.admitted_prior_group_step(group, proof_target=root, bridge=bridge)
    assert statement is not None
    goal = ImageZeroStatement(TodaSuspensionMap(group, TodaPrimaryGroup(group.group_dimension+1,n+1)))
    expand = build_prior_zero_image_provider(bridge=bridge, proof_target=root)
    routes = expand(goal)
    assert len(routes) == 1 and routes[0].rule.name == RULE_NAME
    assert routes[0].subgoals[0] == statement.conclusion
    image = routes[0].subgoals[1]
    from expression import Zero
    from phase165_r14_r6_generic_iso import GeneratorImage
    assert image == GeneratorImage(goal.map, statement.conclusion.rhs.generator, Zero())
    # A candidate remains a candidate, not a proof of the image or zero map.
    assert all(not isinstance(g, ProofStep) for g in routes[0].subgoals)
    assert build_prior_zero_image_provider(bridge=bridge, proof_target=statement.conclusion)(goal) == ()


def test_patch_idempotent_and_rejects_unknown_bytes():
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        # This is a historical R46 installer contract, not a pin on all future Phases.
        if path == 'phase165_r52_r9_shared_math.py':
            import subprocess
            raw = subprocess.check_output(
                ['git', 'cat-file', 'blob', '73e8a6b1d3127502a5459fc36cc439f00a745107'],
                cwd=ROOT,
            )
        assert updated_source(path, raw) == raw
        with pytest.raises(ValueError):
            updated_source(path, raw + b'\n# unexpected edit\n')
