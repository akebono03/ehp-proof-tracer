# Phase 175 R4R14R4 完全コード

新規ファイルの配置先は各見出しのパスです。既存のクラスや関数の変更はありません。

## rule.py

```python
"""A proved image f(g)=c and a proved relation c=0 imply f(g)=0.

This is a generic inference, independent of the number of composition factors.
No source theorem, database group presentation or root group is asserted here.
"""
from __future__ import annotations

from expression import Composition, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = "proved composite image and proved composite zero imply generator zero"


def composite_value_zero_inputs(
    goal: object, composite_image: object,
) -> tuple[GeneratorImage, Relation] | None:
    """Require the very same map, generator and typed nonzero composite value."""
    if (not isinstance(goal, GeneratorImage)
            or not isinstance(goal.map, TodaSuspensionMap)
            or not isinstance(goal.target_generator, Zero)
            or not isinstance(composite_image, GeneratorImage)
            or composite_image.map != goal.map
            or composite_image.source_generator != goal.source_generator
            or not isinstance(composite_image.target_generator, Composition)):
        return None
    mapping = goal.map
    domain, codomain = mapping.source_group, mapping.target_group
    if (not isinstance(domain, TodaPrimaryGroup)
            or not isinstance(codomain, TodaPrimaryGroup)):
        return None
    q, n = domain.group_dimension, domain.sphere_dimension
    if (type(q) is not int or type(n) is not int or n < 2 or q < n
            or codomain != TodaPrimaryGroup(q + 1, n + 1)):
        return None
    if (typed_element_span(goal.source_generator) != (q, n)
            or typed_element_span(composite_image.target_generator)
            != (q + 1, n + 1)):
        return None
    return (composite_image, Relation(
        composite_image.target_generator, Zero(), RelationType.EQUALITY,
    ))


def proved_composite_zero_image_rule(
    goal: GeneratorImage, composite_image: GeneratorImage,
) -> InferenceRule:
    """No conclusion is admitted unless both independently proved steps match."""
    required = composite_value_zero_inputs(goal, composite_image)
    if required is None:
        raise ValueError("a typed suspension composite image is required")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and composite_value_zero_inputs(goal, composite_image) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "If a separately verified image E(g)=c and an independently "
            "verified relation c=0 hold, then E(g)=0. The composite may "
            "contain two or more factors; neither premise is created here."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=GeneratorImage,
                statement_pattern=required[0],
                proof_rule=ProofRule.INFERENCE,
            ),
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[1],
                proof_rule=ProofRule.INFERENCE,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_proved_composite_zero_image(
    goal: object, composite_image: object,
) -> tuple[GoalExpansion, ...]:
    """Return unproved backward obligations; never insert a ProofStep."""
    required = composite_value_zero_inputs(goal, composite_image)
    if required is None:
        return ()
    return (GoalExpansion(
        rule=proved_composite_zero_image_rule(goal, composite_image),
        subgoals=required,
    ),)
```

## tests/test_rule.py

```python
"""Tests for generic source-free transport of a proved zero composite."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase175_r4r14r4_general_zero_transport.rule import (
    RULE_NAME,
    composite_value_zero_inputs,
    expand_proved_composite_zero_image,
    proved_composite_zero_image_rule,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule,
)


def _element(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(
        name=name, dimension=target, source=source, target=target,
        generator=GeneratorSymbol(name),
    )


def _cases(factors: int) -> tuple[GeneratorImage, GeneratorImage]:
    first = _element("a", 7, 4)
    second = _element("b", 11, 7)
    value: object = Composition(first, second)
    if factors == 3:
        value = Composition(value, _element("c", 13, 11))
    source_degree = 10 if factors == 2 else 12
    source_generator = _element("g", source_degree, 3)
    mapping = TodaSuspensionMap(
        TodaPrimaryGroup(source_degree, 3),
        TodaPrimaryGroup(source_degree + 1, 4),
    )
    return (
        GeneratorImage(mapping, source_generator, Zero()),
        GeneratorImage(mapping, source_generator, value),
    )


@pytest.mark.parametrize("factors", (2, 3))
def test_two_premises_prove_zero_image_for_any_factor_count(factors: int) -> None:
    goal, image = _cases(factors)
    required = composite_value_zero_inputs(goal, image)
    assert required is not None
    options = expand_proved_composite_zero_image(goal, image)
    assert len(options) == 1
    assert options[0].rule.name == RULE_NAME
    assert options[0].subgoals == required
    steps = tuple(ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only proof witness"),
    ) for statement in required)
    matches = find_inference_matches_for_rule(options[0].rule, steps)
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.conclusion == goal
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == steps


def test_unproved_or_given_premise_cannot_complete() -> None:
    goal, image = _cases(2)
    required = composite_value_zero_inputs(goal, image)
    assert required is not None
    rule = proved_composite_zero_image_rule(goal, image)
    first = ProofStep(required[0], (), ProofRule.INFERENCE)
    second = ProofStep(required[1], (), ProofRule.INFERENCE)
    assert find_inference_matches_for_rule(rule, (first,)) == ()
    assert find_inference_matches_for_rule(
        rule, (first, replace(second, rule=ProofRule.GIVEN)),
    ) == ()
    assert find_inference_matches_for_rule(rule, ()) == ()


def test_wrong_image_value_and_mismatched_map_rejected() -> None:
    goal, image = _cases(2)
    wrong = replace(image, map=TodaSuspensionMap(
        TodaPrimaryGroup(12, 3), TodaPrimaryGroup(13, 4),
    ))
    assert composite_value_zero_inputs(goal, wrong) is None
    assert expand_proved_composite_zero_image(goal, wrong) == ()
    wrong_value = replace(image, target_generator=Zero())
    assert composite_value_zero_inputs(goal, wrong_value) is None
    with pytest.raises(ValueError):
        proved_composite_zero_image_rule(goal, wrong)


def test_no_new_sources_or_proof_steps_are_created() -> None:
    goal, image = _cases(2)
    options = expand_proved_composite_zero_image(goal, image)
    assert len(options) == 1
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'Expected develop branch' }
    $pins = @{
        'phase174_r3_r7_r7_composite_zero_audit/rule.py' = 'd98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6'
        'phase169_r10e5_composite_generator_image/rule.py' = '01acace3eb273d47091421a61291ee54b51c369f'
        'phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py' = '6aa48096b41714fbdf588c3ba423d264a4a13bb9'
    }
    foreach ($path in $pins.Keys) {
        $sha = (git rev-parse "HEAD:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $sha -ne $pins[$path]) { throw "Source blob mismatch: $path" }
        $worktreeSha = (git hash-object $path).Trim()
        if ($LASTEXITCODE -ne 0 -or $worktreeSha -ne $pins[$path]) { throw "Worktree source differs: $path" }
    }
    Write-Output 'PHASE175_R4R14R4_SOURCE_GUARD=PASS'
    Write-Output 'PHASE175_R4R14R4_NEW_GIVEN=0'
    Write-Output 'PHASE175_R4R14R4_PRODUCTION_CHANGED=0'
    if ($DryRun) {
        Write-Output 'PHASE175_R4R14R4_GATE=PASS_DRYRUN_SOURCE_GUARD'
        exit 0
    }
    python -m pytest --import-mode=importlib -q `
        phase175_r4r14r4_general_zero_transport/tests/test_rule.py `
        phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py `
        phase174_r3_r7_r7_composite_zero_audit/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R4 focused pytest failed' }
    Write-Output 'PHASE175_R4R14R4_GATE=PASS_ISOLATED_GENERIC_ZERO_TRANSPORT'
    Write-Output 'PHASE175_R4R14R4_PUBLIC_PROOF_COMPLETE=False'
} finally {
    Pop-Location
}
```
