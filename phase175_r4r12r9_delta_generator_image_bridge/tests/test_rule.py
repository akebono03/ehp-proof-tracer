"""Focused bridge tests: no proof source or group conclusion is manufactured."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import GeneratorImage
from phase175_r4r12r9_delta_generator_image_bridge import installer
from phase175_r4r12r9_delta_generator_image_bridge.rule import (
    RULE_NAME, delta_image_equality, expand_proved_delta_equality_image,
)
from proof import InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule


def target_goal():
    eta9 = HomotopyElement('η₉', 9, 10, 9, GeneratorSymbol('η', index=9))
    enup = HomotopyElement('Eν′', 4, 7, 4)
    eta7 = HomotopyElement('η₇', 7, 8, 7, GeneratorSymbol('η', index=7))
    value = Composition(enup, eta7)
    return GeneratorImage(TodaDeltaMap(TodaPrimaryGroup(10, 9),
                                       TodaPrimaryGroup(8, 4)), eta9, value)


def test_bridge_creates_only_equality_subgoal():
    target = target_goal()
    options = expand_proved_delta_equality_image(target)
    assert len(options) == 1
    assert options[0].rule.name == RULE_NAME
    assert options[0].subgoals == (delta_image_equality(target),)


def test_bridge_needs_independent_inference_not_given():
    expansion = expand_proved_delta_equality_image(target_goal())[0]
    equality = expansion.subgoals[0]
    inferred = ProofStep(equality, (), ProofRule.INFERENCE,
                         inference_rule=InferenceRule('test parent'))
    given = ProofStep(equality, (), ProofRule.GIVEN)
    assert len(find_inference_matches_for_rule(expansion.rule, (inferred,))) == 1
    assert not find_inference_matches_for_rule(expansion.rule, (given,))


def test_wrong_delta_type_does_not_make_candidate():
    goal = target_goal()
    assert not expand_proved_delta_equality_image(replace(goal,
        map=TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(8, 4))))
    assert not expand_proved_delta_equality_image(replace(goal,
        target_generator=goal.source_generator))


def test_installer_is_idempotent_and_preserves_other_functions():
    sample = ('from __future__ import annotations\n'
              'def before():\n    return 1\n\n'
              'def shared_expansion_provider(bridge):\n'
              '    """Sample."""\n'
              + installer.ANCHOR + '    return bridge\n\n'
              'def after():\n    return 2\n')
    updated, function = installer.replacement(sample)
    assert installer.INSERT in function
    assert updated.startswith('from __future__ import annotations\ndef before()')
    assert updated.endswith('def after():\n    return 2\n')
    again, function2 = installer.replacement(updated)
    assert again == updated and function2 == function
