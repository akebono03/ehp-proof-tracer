"""Focused, typed proof obligations for structure-neutral Toda (4.5) transport."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup,
    TodaIteratedSuspensionMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase169_r10e1_general_group_transport import transport as universal
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r3m_prior_result_catalog.prior_results import PriorGroupResult
from proof import (
    ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from toda_rules import Toda45IsomorphismStatement
from unified_statement_registry import UnifiedStatementRegistry


def _family(family_id: int):
    return next(family for family in read_registered_stable_families()
                if family.family_id == family_id)


def _element(family_id: int, n: int) -> HomotopyElement:
    family = _family(family_id)
    return HomotopyElement(
        name=family.name_at(n), dimension=n,
        source=n + family.stem, target=n,
        generator=GeneratorSymbol(family=family.symbol_family, index=n),
    )


def _relation(n: int, k: int, structure: object) -> Relation:
    return Relation(TodaPrimaryGroup(n + k, n), structure, RelationType.EQUALITY)


def _zero(n: int, k: int) -> TodaPrimaryGroupZeroStatement:
    return TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + k, n))


def _iso(n: int, k: int, r: int) -> Toda45IsomorphismStatement:
    return Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
        exponent=r,
        source_group=TodaPrimaryGroup(n + k, n),
        target_group=TodaPrimaryGroup(n + k + r, n + r),
    ))


def _two_component(n: int) -> Relation:
    return _relation(n, 8, DirectSumGroup((
        FiniteCyclicGroup(2, _element(11, n)),
        FiniteCyclicGroup(2, _element(10, n)),
    )))


def _three_component(n: int) -> Relation:
    nu_cubed = Composition(
        _element(4, n),
        Composition(_element(4, n + 3), _element(4, n + 6)),
    )
    eta_epsilon = Composition(_element(2, n), _element(10, n + 1))
    return _relation(n, 9, DirectSumGroup((
        FiniteCyclicGroup(2, nu_cubed),
        FiniteCyclicGroup(2, _element(12, n)),
        FiniteCyclicGroup(2, eta_epsilon),
    )))


@pytest.mark.parametrize('r', [1, 2, 3, 5])
def test_r10e1_zero_transports_without_generator_image(r):
    source, goal = _zero(6, 4), _zero(6 + r, 4)
    images = universal.generator_images_for_group_transport(source, goal)
    assert images == ()
    rule = universal.general_group_transport_rule(goal, source)
    steps = (
        ProofStep(source, (), ProofRule.GIVEN),
        ProofStep(_iso(6, 4, r), (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal
    assert find_inference_matches_for_rule(
        rule, (steps[0], replace(steps[1], rule=ProofRule.GIVEN)),
    ) == ()


@pytest.mark.parametrize('r', [1, 3, 5])
def test_r10e1_two_cyclic_summands_require_all_generator_images(r):
    source, goal = _two_component(10), _two_component(10 + r)
    images = universal.generator_images_for_group_transport(source, goal)
    assert images is not None and len(images) == 2 * r
    assert all(type(image).__name__ == 'GeneratorImage' for image in images)
    rule = universal.general_group_transport_rule(goal, source)
    steps = (
        ProofStep(source, (), ProofRule.GIVEN),
        ProofStep(_iso(10, 8, r), (), ProofRule.INFERENCE),
    ) + tuple(ProofStep(image, (), ProofRule.INFERENCE) for image in images)
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal
    assert find_inference_matches_for_rule(rule, steps[:-1]) == ()
    assert find_inference_matches_for_rule(
        rule, steps[:2] + (replace(steps[2], rule=ProofRule.GIVEN),) + steps[3:],
    ) == ()


def test_r10e1_three_summands_with_composites_have_nine_independent_images():
    source, goal = _three_component(11), _three_component(14)
    images = universal.generator_images_for_group_transport(source, goal)
    assert images is not None and len(images) == 9
    rule = universal.general_group_transport_rule(goal, source)
    assert len(rule.premise_patterns) == 11


@pytest.mark.parametrize('r', [1, 3])
def test_r10e1_free_cyclic_group_does_not_require_an_order(r):
    source = _relation(9, 7, FreeCyclicGroup(_element(9, 9)))
    goal = _relation(9 + r, 7, FreeCyclicGroup(_element(9, 9 + r)))
    images = universal.generator_images_for_group_transport(source, goal)
    assert images is not None and len(images) == r
    assert universal.general_group_transport_rule(goal, source)


def test_r10e1_original_finite_cyclic_shape_is_supported():
    source = _relation(5, 3, FiniteCyclicGroup(8, _element(4, 5)))
    goal = _relation(8, 3, FiniteCyclicGroup(8, _element(4, 8)))
    images = universal.generator_images_for_group_transport(source, goal)
    assert images is not None and len(images) == 3
    assert universal.general_group_transport_rule(goal, source)


def test_r10e1_wrong_order_type_or_number_of_summands_fail_closed():
    source = _two_component(10)
    goal = _two_component(12)
    wrong_order = replace(goal, rhs=DirectSumGroup((
        FiniteCyclicGroup(4, goal.rhs.summands[0].generator),
        goal.rhs.summands[1],
    )))
    wrong_type = replace(goal, rhs=DirectSumGroup((
        FreeCyclicGroup(goal.rhs.summands[0].generator),
        goal.rhs.summands[1],
    )))
    missing = replace(goal, rhs=DirectSumGroup((goal.rhs.summands[0],)))
    for bad in (wrong_order, wrong_type, missing):
        assert universal.generator_images_for_group_transport(source, bad) is None
        with pytest.raises(ValueError):
            universal.general_group_transport_rule(bad, source)


def test_r10e1_stable_range_mismatch_rejected():
    source = _two_component(9)
    target = _two_component(11)
    assert universal.generator_images_for_group_transport(source, target) is None
    assert universal.generator_images_for_group_transport(_zero(5, 4), _zero(8, 4)) is None
    assert universal.generator_images_for_group_transport(_zero(6, 4), _zero(6, 4)) is None


def test_r10e1_unknown_generator_citation_does_not_become_proof():
    source = _two_component(10)
    goal = _two_component(12)
    unknown = replace(goal.rhs.summands[0].generator, name='unregistered_12')
    wrong = replace(goal, rhs=DirectSumGroup((
        FiniteCyclicGroup(2, unknown), goal.rhs.summands[1],
    )))
    assert universal.generator_images_for_group_transport(source, wrong) is None


def test_r10e1_prior_citation_and_iso_required_for_direct_sum(monkeypatch):
    source, goal = _two_component(10), _two_component(12)
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    monkeypatch.setattr(universal, 'resolve_specialized_goal_citing_id',
                        lambda b, target: 'registered_target')
    calls = []

    def fake_prior(b, *, source_n, source_k, citing_assertion_id):
        calls.append((source_n, source_k, citing_assertion_id))
        if source_n == 10 and source_k == 8:
            return PriorGroupResult(10, 8, source, 'registered_target',
                                    'registered_prior', True, 'prior_fixed_source')
        return PriorGroupResult(source_n, source_k, None, 'registered_target',
                                None, False, 'db_result_missing')

    monkeypatch.setattr(universal, 'resolve_prior_group_result', fake_prior)
    assert universal.expand_prior_general_group_transport(
        goal, (), bridge, proof_target=goal,
    ) == ()
    options = universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=goal,
    )
    assert len(options) == 1
    assert len(options[0].subgoals) == 6
    assert options[0].subgoals[0] == source
    assert calls[0] == (10, 8, 'registered_target')
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=source,
    ) == ()
    monkeypatch.setattr(universal, 'resolve_specialized_goal_citing_id',
                        lambda b, target: None)
    # R10E4 permits an independent, earlier DB group without a target cite.
    db_options = universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=goal,
    )
    assert len(db_options) == 1
    assert db_options[0].subgoals[0] == source
    from phase169_r10e4_ordered_db_prior import db_prior
    monkeypatch.setattr(
        db_prior, 'exact_prior_database_result', lambda *args, **kwargs: None,
    )
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=goal,
    ) == ()


def test_r10e1_zero_citation_absence_not_inferred_from_db(monkeypatch):
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    goal = _zero(8, 4)
    # The real (n=6, k=4) DB zero result may be used even without a
    # separately registered proposition, but only as an adopted DB prior.
    options = universal.expand_prior_general_group_transport(
        goal, (_iso(6, 4, 2),), bridge, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals[0] == _zero(6, 4)
    from phase169_r10e4_ordered_db_prior import db_prior
    monkeypatch.setattr(
        db_prior, 'exact_prior_database_result', lambda *args, **kwargs: None,
    )
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(6, 4, 2),), bridge, proof_target=goal,
    ) == ()


def test_r10e1_existing_finite_cyclic_route_keeps_compatibility(monkeypatch):
    source = _relation(5, 3, FiniteCyclicGroup(8, _element(4, 5)))
    goal = _relation(7, 3, FiniteCyclicGroup(8, _element(4, 7)))
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    import phase169_r7_general_stable_transport.rule as old
    seen = []

    def fake(old_goal, available, old_bridge, *, proof_target):
        seen.append((old_goal, proof_target))
        return ()

    monkeypatch.setattr(old, 'expand_prior_general_stable_transport', fake)
    # R7 is still tried first; when it offers nothing, the authorized
    # R10E4 DB prior may supply the identical typed source obligation.
    options = universal.expand_prior_general_group_transport(
        goal, (_iso(5, 3, 2),), bridge, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals[0] == source
    assert seen == [(goal, goal)]
    from phase169_r10e4_ordered_db_prior import db_prior
    monkeypatch.setattr(
        db_prior, 'exact_prior_database_result', lambda *args, **kwargs: None,
    )
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(5, 3, 2),), bridge, proof_target=goal,
    ) == ()
    assert seen == [(goal, goal), (goal, goal)]


def test_r10e1_patch_is_guarded_and_does_not_duplicate():
    from phase169_r10e1_general_group_transport.patch import OLD, NEW, transform
    sample = (b'def shared_expansion_provider():\r\n'
              b'    def expand(goal):\r\n'
              + OLD.replace(b'\n', b'\r\n')
              + b'        return ()\r\n'
                b'    return expand\r\n')
    result, full = transform(sample)
    assert NEW in result.replace(b'\r\n', b'\n')
    assert 'def shared_expansion_provider' not in full or 'expand_prior_general_group_transport' in full
    with pytest.raises(RuntimeError):
        transform(result)
