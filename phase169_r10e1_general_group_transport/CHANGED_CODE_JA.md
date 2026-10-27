# R10E1 変更コード全文

本番コードの変更は `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` だけ。変更後の関数全文は `run.ps1` 実行時に `output/shared_expansion_provider_FULL.py`、ファイル全文は `output/phase165_r52_r9_shared_math.py.FULL` として保存する。既存ファイルの import は変更しない。新規クラスは追加しない。

## 新規モジュール `transport.py`（ルートパッケージ直下に追加）

```python
"""Shape-neutral Toda (4.5) transport with independently proved generator images.

No DB row, candidate generator identity or stable-range test creates a GIVEN.
The citation gate remains authoritative; unavailable source citations fail closed.
"""
from __future__ import annotations

from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaIteratedSuspensionMap,
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
    TodaSuspensionMap,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from phase169_r7_general_stable_transport.rule import _intermediate_typed_generator
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from unified_statement_registry import AssertionOrigin


def _goal_group(goal: object) -> TodaPrimaryGroup | None:
    if isinstance(goal, TodaPrimaryGroupZeroStatement):
        return goal.group if isinstance(goal.group, TodaPrimaryGroup) else None
    if (isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)):
        return goal.lhs
    return None


def _components(goal: object) -> tuple[object, ...] | None:
    """Return an ordered cyclic presentation, or () for an explicitly zero group.

    Direct-sum correspondence is position-preserving.  We do not infer a
    permutation or a change of basis from a DB presentation.
    """
    if isinstance(goal, TodaPrimaryGroupZeroStatement):
        return ()
    if not isinstance(goal, Relation):
        return None
    structure = goal.rhs
    if isinstance(structure, (FiniteCyclicGroup, FreeCyclicGroup)):
        return (structure,)
    if isinstance(structure, DirectSumGroup):
        if not structure.summands:
            return None
        if not all(isinstance(item, (FiniteCyclicGroup, FreeCyclicGroup))
                   for item in structure.summands):
            return None
        return tuple(structure.summands)
    return None


def _transport_shape(source: object, goal: object) -> tuple[int, int, int] | None:
    """Return (source sphere n, stem k, suspension count r) in Toda stable range."""
    left, right = _goal_group(source), _goal_group(goal)
    if left is None or right is None:
        return None
    if type(source) is not type(goal):
        return None
    values = (left.group_dimension, left.sphere_dimension,
              right.group_dimension, right.sphere_dimension)
    if not all(type(value) is int for value in values):
        return None
    q, n, p, m = values
    k, r = q - n, m - n
    if (k < 0 or n < 2 or n < k + 2 or r < 1
            or p - q != r):
        return None
    return n, k, r


def generator_images_for_group_transport(
    source: object, goal: object,
) -> tuple[GeneratorImage, ...] | None:
    """Build typed image *obligations* for any supported group presentation.

    Zero groups have no generator obligations.  For an ordered direct sum,
    every component must independently preserve cyclic type and order.
    """
    dimensions = _transport_shape(source, goal)
    left_components = _components(source)
    right_components = _components(goal)
    if (dimensions is None or left_components is None or right_components is None
            or len(left_components) != len(right_components)):
        return None
    n, k, r = dimensions
    if not left_components:
        return ()
    images = []
    for left, right in zip(left_components, right_components):
        if type(left) is not type(right):
            return None
        if (isinstance(left, FiniteCyclicGroup)
                and (type(left.order) is not int or left.order < 2
                     or left.order != right.order)):
            return None
        candidates = tuple(
            _intermediate_typed_generator(left.generator, right.generator, i, r)
            for i in range(r + 1)
        )
        if any(value is None for value in candidates):
            return None
        for i in range(r):
            images.append(GeneratorImage(
                map=TodaSuspensionMap(
                    TodaPrimaryGroup(n + k + i, n + i),
                    TodaPrimaryGroup(n + k + i + 1, n + i + 1),
                ),
                source_generator=candidates[i],
                target_generator=candidates[i + 1],
            ))
    return tuple(images)


def general_group_transport_rule(goal: object, source: object) -> InferenceRule:
    """One typed group-structure rule: source, cited isomorphism, proved images."""
    shape = _transport_shape(source, goal)
    images = generator_images_for_group_transport(source, goal)
    if shape is None or images is None:
        raise ValueError("source/target stable structures cannot be transported")
    n, k, r = shape
    source_group = TodaPrimaryGroup(n + k, n)
    target_group = TodaPrimaryGroup(n + k + r, n + r)
    iso = Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
        exponent=r, source_group=source_group, target_group=target_group,
    ))
    expected = (source, iso) + images

    def guard(premises, bindings):
        return (len(premises) == len(expected)
                and tuple(item.conclusion for item in premises) == expected
                and all(item.rule is ProofRule.INFERENCE for item in premises[1:])
                and generator_images_for_group_transport(source, goal) == images)

    return InferenceRule(
        name="typed arbitrary-fold stable transport of group structure",
        description=(
            "Transfer a cited source presentation along a proved Toda (4.5) "
            "isomorphism, discharging each generator image independently. "
            "An empty tuple of images is valid only for a typed zero group."
        ),
        premise_patterns=(
            PremisePattern(statement_type=type(source), statement_pattern=source),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Toda45IsomorphismStatement,
                           statement_pattern=iso),
        ) + tuple(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=GeneratorImage,
                           statement_pattern=image)
            for image in images
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def _zero_citing_assertion_id(bridge: RegistryBridgeResult, goal: object) -> str | None:
    """Zero targets require one independently positioned, exactly typed source."""
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        return None
    matches = []
    for assertion in bridge.registry._assertions.values():
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and assertion.content == goal
                and assertion.component_position is not None
                and bridge.registry.reference(assertion.reference_id).publication_position is not None):
            matches.append(assertion.assertion_id)
    return matches[0] if len(matches) == 1 else None


def _prior_zero_goal(
    bridge: RegistryBridgeResult, *, source_n: int, stem: int, citing_id: str,
) -> TodaPrimaryGroupZeroStatement | None:
    """Find an *earlier cited* zero assertion, not merely a zero DB row."""
    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
    from phase166_r3c_publication_order import precedes_citing_assertion

    candidates = database_zero_group_goal_candidates(n=source_n, k=stem)
    if len(candidates) != 1:
        return None
    source = candidates[0]
    eligible = tuple(
        assertion for assertion in bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT
        and assertion.content == source
        and precedes_citing_assertion(bridge, assertion.assertion_id, citing_id)
    )
    if len(eligible) != 1:
        return None
    return source


def expand_prior_general_group_transport(
    goal: object,
    available: tuple[object, ...],
    bridge: RegistryBridgeResult,
    *,
    proof_target: object,
) -> tuple[GoalExpansion, ...]:
    """Common proof search entry without a stem- or group-type-specific theorem.

    Finite-cyclic goals keep the already-tested R7 route for API and narrative
    compatibility; all other shapes use the same typed transport obligations.
    Any absent/ambiguous citation or isomorphism returns no proof candidate.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("typed source bridge required")
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if goal != proof_target or _goal_group(goal) is None:
        return ()
    if isinstance(goal, Relation) and isinstance(goal.rhs, FiniteCyclicGroup):
        from phase169_r7_general_stable_transport.rule import (
            expand_prior_general_stable_transport,
        )
        return expand_prior_general_stable_transport(
            goal, available, bridge, proof_target=proof_target,
        )
    group = _goal_group(goal)
    if not all(type(x) is int for x in (group.group_dimension, group.sphere_dimension)):
        return ()
    n = group.sphere_dimension
    k = group.group_dimension - n
    if k < 0 or n <= k + 2 or _components(goal) is None:
        return ()
    citing_id = (
        _zero_citing_assertion_id(bridge, goal)
        if isinstance(goal, TodaPrimaryGroupZeroStatement)
        else resolve_specialized_goal_citing_id(bridge, goal)
    )
    if citing_id is None:
        return ()
    for source_n in range(k + 2, n):
        if isinstance(goal, TodaPrimaryGroupZeroStatement):
            source = _prior_zero_goal(
                bridge, source_n=source_n, stem=k, citing_id=citing_id,
            )
        else:
            prior = resolve_prior_group_result(
                bridge, source_n=source_n, source_k=k,
                citing_assertion_id=citing_id,
            )
            source = prior.relation if prior.eligible else None
        if source is None:
            continue
        images = generator_images_for_group_transport(source, goal)
        shape = _transport_shape(source, goal)
        if images is None or shape is None:
            continue
        source_n, stem, r = shape
        iso = Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
            exponent=r,
            source_group=TodaPrimaryGroup(source_n + stem, source_n),
            target_group=group,
        ))
        if not any(
            isinstance(schema, Toda45IsomorphismStatement)
            and (schema == iso or specialize_typed_statement(schema, iso) is not None)
            for schema in available
        ):
            continue
        return (GoalExpansion(
            general_group_transport_rule(goal, source),
            (source, iso) + images,
        ),)
    return ()

```

## パッチ全体 `patch.py`

```python
"""Guarded single-call-site replacement for the common backward provider."""
from __future__ import annotations

import ast
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / 'phase165_r52_r9_shared_math.py'
OUTPUT = HERE / 'output'
BACKUP = OUTPUT / 'phase165_r52_r9_shared_math.py.before'
OLD = '''        # R10D2: stem-neutral R7 transport, with publication order checked
        # by the prior-source resolver and each generator image independently proved.
        # Retain the already verified R5B/R6A expansions when they are available.
        from phase169_r7_general_stable_transport.rule import (
            expand_prior_general_stable_transport,
        )
        if (not legacy_one_step_options and not legacy_two_step_options
                and isinstance(goal, Relation)
                and isinstance(goal.lhs, TodaPrimaryGroup)
                and type(goal.lhs.group_dimension) is int
                and type(goal.lhs.sphere_dimension) is int):
            options.extend(expand_prior_general_stable_transport(
                goal, tuple(available), bridge, proof_target=proof_target,
            ))
'''.encode('utf-8')
NEW = '''        # R10E1: one typed entry for zero, cyclic, free and direct-sum groups.
        # Previously verified finite-cyclic derivations retain their R7 adapter.
        # Neither DB results nor candidate generators become GIVEN proof leaves.
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from phase169_r10e1_general_group_transport.transport import (
            expand_prior_general_group_transport,
        )
        if (not legacy_one_step_options and not legacy_two_step_options
                and ((isinstance(goal, Relation)
                      and isinstance(goal.lhs, TodaPrimaryGroup)
                      and type(goal.lhs.group_dimension) is int
                      and type(goal.lhs.sphere_dimension) is int)
                     or isinstance(goal, TodaPrimaryGroupZeroStatement))):
            options.extend(expand_prior_general_group_transport(
                goal, tuple(available), bridge, proof_target=proof_target,
            ))
'''.encode('utf-8')


def transform(raw: bytes) -> tuple[bytes, str]:
    if not isinstance(raw, bytes):
        raise TypeError('raw source must be bytes')
    crlf = b'\r\n' in raw
    normalized = raw.replace(b'\r\n', b'\n')
    if normalized.count(OLD) != 1 or NEW in normalized:
        raise RuntimeError('R10E1 patch boundary changed; stop without writing')
    changed = normalized.replace(OLD, NEW, 1)
    tree = ast.parse(changed.decode('utf-8'))
    funcs = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == 'shared_expansion_provider']
    if len(funcs) != 1:
        raise RuntimeError('expected one complete shared_expansion_provider')
    node = funcs[0]
    full = ''.join(changed.decode('utf-8').splitlines(True)[node.lineno - 1:node.end_lineno])
    if crlf:
        changed = changed.replace(b'\n', b'\r\n')
    return changed, full


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    raw = TARGET.read_bytes()
    changed, full = transform(raw)
    # All outputs are prepared before mutating production source.
    BACKUP.write_bytes(raw)
    (OUTPUT / 'shared_expansion_provider_FULL.py').write_text(full, encoding='utf-8')
    (OUTPUT / 'phase165_r52_r9_shared_math.py.FULL').write_bytes(changed)
    temporary = TARGET.with_name(TARGET.name + '.r10e1-tmp')
    try:
        temporary.write_bytes(changed)
        os.replace(temporary, TARGET)
    finally:
        if temporary.exists():
            temporary.unlink()
    print('R10E1_PATCHED=' + str(TARGET))
    print('R10E1_BACKUP=' + str(BACKUP))
    print('R10E1_FULL_FUNCTION=' + str(OUTPUT / 'shared_expansion_provider_FULL.py'))
    print('R10E1_FULL_FILE=' + str(OUTPUT / 'phase165_r52_r9_shared_math.py.FULL'))


if __name__ == '__main__':
    main()

```

## 限定テスト全文 `tests/test_r10e1_general_transport.py`

```python
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
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=goal,
    ) == ()


def test_r10e1_zero_citation_absence_not_inferred_from_db():
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    goal = _zero(8, 4)
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
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(5, 3, 2),), bridge, proof_target=goal,
    ) == ()
    assert seen == [(goal, goal)]


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

```

## 監査全文 `audit.py`

```python
"""Production-facing proof/status audit, with no invented completion claims."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e1_general_group_transport.transport import (
    _zero_citing_assertion_id,
    expand_prior_general_group_transport,
)
from proof import ProofRule, Relation

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / 'output'
GOALS = ((8, 4), (8, 6), (15, 7), (15, 8), (15, 9))


def inspect_goal(bridge, n: int, k: int) -> dict:
    zero_goals = database_zero_group_goal_candidates(n=n, k=k)
    relation_goals = registered_group_goal_candidates(bridge, n=n, k=k)
    goals = zero_goals if zero_goals else relation_goals
    report = {
        'target': f'pi_{n+k}^{n}',
        'shapes': [],
        'citation_resolved': False,
        'candidate_count': None,
        'reason': 'no_typed_goal' if not goals else 'not_a_cited_target',
    }
    for goal in goals:
        shape = 'zero' if isinstance(goal, TodaPrimaryGroupZeroStatement) else (
            type(goal.rhs).__name__ if isinstance(goal, Relation) else type(goal).__name__
        )
        report['shapes'].append(shape)
        citing_id = (
            _zero_citing_assertion_id(bridge, goal)
            if isinstance(goal, TodaPrimaryGroupZeroStatement)
            else resolve_specialized_goal_citing_id(bridge, goal)
        )
        if citing_id is None:
            continue
        report['citation_resolved'] = True
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing_id,
            explicit_publication_target=True,
        )
        available = tuple(
            link.step.conclusion for link in screened.proof_links
            if link.step is not None and link.step.rule is ProofRule.GIVEN
        )
        # This is a candidate count, not a completed proof.
        options = expand_prior_general_group_transport(
            goal, available, screened, proof_target=goal,
        )
        report['candidate_count'] = len(options)
        report['reason'] = 'typed_candidates_only' if options else 'no_eligible_transport_candidate'
        provider = shared_expansion_provider(screened, proof_target=goal)
        report['provider_option_count'] = len(provider(goal))
    return report


def main() -> None:
    bridge = build_shared_typed_bridge()
    regressions = []
    for n, k in ((8, 1), (8, 2), (8, 3)):
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        case = {'group': f'pi_{n+k}^{n}', 'status': result.status.value,
                'proof_steps': len(result.proven_steps),
                'open_goals': len(result.open_goals)}
        regressions.append(case)
        print(f'R10E1_{case["group"]}_STATUS={case["status"]}')
    if any(case['status'] != 'complete' for case in regressions):
        raise RuntimeError('R10E1 regressed a previously complete 1-, 2- or 3-stem proof')
    boundaries = [inspect_goal(bridge, n, k) for n, k in GOALS]
    for case in boundaries:
        print('R10E1_' + case['target'] + '_CITATION_RESOLVED=' + str(case['citation_resolved']))
        print('R10E1_' + case['target'] + '_CANDIDATE_COUNT=' + str(case['candidate_count']))
    report = {
        'phase': '169 R10E1',
        'branch': 'develop',
        'head': subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.strip(),
        'limited_regressions': regressions,
        'group_shapes': boundaries,
        'data_is_not_a_proof': True,
        'unresolved_citation_is_not_missing_math': True,
        'full_pytest_run': False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / 'audit.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    lines = [
        '# Phase 169 R10E1 — 共通群構造輸送監査', '',
        '群構造に依存しない型付き輸送の検証。DB は証明ではない。', '',
        '| 群 | Goal の形 | 引用境界 | 候補数 |', '|---|---|---|---:|',
    ]
    for case in boundaries:
        count = 'not checked' if case['candidate_count'] is None else str(case['candidate_count'])
        lines.append(f"| {case['target']} | {', '.join(case['shapes'])} | "
                     f"{'resolved' if case['citation_resolved'] else 'unresolved'} | {count} |")
    lines.extend(['', '未解決の引用は、文献命題の数学的不在を意味しない。',
                  '全体 pytest は未実行。', ''])
    (OUTPUT / 'audit.md').write_text('\n'.join(lines), encoding='utf-8')
    print('R10E1_AUDIT=' + str(OUTPUT / 'audit.json'))
    print('R10E1_FULL_PYTEST_RUN=False')


if __name__ == '__main__':
    main()

```

## 変更一覧・実行する pytest・完了条件

- **変更**: 共有 Provider の呼び出し先を R10E1 に変更。既存 API は保持。
- **新規**: 型付き群構造輸送、零群の出典検査、テスト、監査、ロールバック付き実行スクリプト。
- **pytest**: R10E1、新旧 R7、R10B、R10D2、R10A2 の限定テスト。全体 pytest は実行しない。
- **完了条件**: 限定テストおよび監査 PASS。既存 1・2・3-stem の完成状況維持、引用なしでの完成防止。
- **次段階**: `citing_assertion_id=None` を起点とする目標引用の不足を独立監査し、必要な出典を補う。