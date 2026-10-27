# Phase 169 R10E2-R1 — 変更対象と完全なコード

## 本番コードの置換対象

- `phase165_r52_r9_shared_math.py` — `search_shared_group_goal()`
- `phase165_r55_nk_only_goal.py` — `search_group_from_registered_goal()`
- `web_group_proof.py` — `build_standard_web_group_proof_view()`
- `phase168_r3_41p13_trust_boundary/verification.py` — `verify_proof_tree_for_narrative()`
- `phase169_r10e1_general_group_transport/transport.py` — `expand_prior_general_group_transport()`
- `phase168_r3_5_model_renderer.py` — `render_model_backed_narrative_markdown()`

本番モジュールのトップレベル import には変更を加えない。
各関数全体の置換コードは `patch.py` が GitHub develop と整合する既存の関数を AST で抽出し、guard で照合した上で生成する。実行後 `output/<関数名>_FULL.py` と `output/<パス>.FULL` に省略なしで保存する。

## 追加・変更する実装の完全なファイル

### `source_first.py`

```python
"""Screen independently positioned source assertions for a derived DB goal.

No claim about the DB goal's publication position is invented. A fixed source
must have independently recorded publication metadata and be supplied as a
screened proof link. The common solver still has to prove every inference.
"""
from __future__ import annotations

from dataclasses import is_dataclass, replace

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation
from unified_statement_registry import AssertionKind, AssertionOrigin, ProofStepLink


def _target_group(goal: object) -> object | None:
    if isinstance(goal, TodaPrimaryGroupZeroStatement):
        return goal.group
    if isinstance(goal, Relation):
        return goal.lhs
    return None


def screen_independent_sources_for_derived_goal(
    bridge: RegistryBridgeResult, *, goal: object,
) -> RegistryBridgeResult:
    """Screen positioned FIXED statements without inventing a target citation.

    A fixed claim at the same concrete group as the new target is excluded:
    that would assert the result rather than derive it. No file-based or DB
    group row is promoted into a proof premise. Original source links are
    retained when valid; the standard typed, positioned source-registration
    policy may construct a GIVEN for other fixed assertions as in the existing
    explicit-publication source screen.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("typed RegistryBridgeResult required")
    target_group = _target_group(goal)
    if target_group is None:
        raise ValueError("a typed group proof target is required")

    selected: list[ProofStepLink] = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if assertion.kind not in (AssertionKind.STATEMENT, AssertionKind.DEFINITION):
            continue
        if not is_dataclass(assertion.content) or isinstance(assertion.content, type):
            continue
        if type(assertion.content).__name__ == "TodaFixedStatementComponent":
            continue
        reference = bridge.registry.reference(assertion.reference_id)
        if reference.publication_position is None:
            continue
        if assertion.content == goal or _target_group(assertion.content) == target_group:
            continue
        duplicates = tuple(
            item for item in bridge.proof_links
            if item.assertion_id == assertion.assertion_id
        )
        if len(duplicates) > 1:
            continue
        if duplicates:
            step = duplicates[0].step
            if (not isinstance(step, ProofStep)
                    or step.rule is not ProofRule.GIVEN
                    or step.premises
                    or step.conclusion != assertion.content):
                continue
        else:
            step = ProofStep(assertion.content, (), ProofRule.GIVEN)
        if (step.inference_rule is None
                or step.inference_rule.literature_reference is None):
            if not isinstance(reference.locator, str) or not reference.locator:
                continue
            step = replace(
                step,
                inference_rule=InferenceRule(
                    name="Screened fixed source: " + reference.locator,
                    literature_reference=LiteratureReference(
                        label="Toda " + reference.locator,
                        locator=reference.locator,
                    ),
                ),
            )
        # Repeated references to the same typed mathematical fact should not
        # manufacture two competing GIVEN derivations of one subgoal. The
        # registry preserves the other references for provenance inspection.
        if any(
            old.step is not None
            and type(old.step.conclusion) is type(step.conclusion)
            and old.step.conclusion == step.conclusion
            for old in selected
        ):
            continue
        selected.append(ProofStepLink(assertion.assertion_id, step=step))
    return RegistryBridgeResult(bridge.registry, bridge.records, tuple(selected))


def uniquely_screened_prior_sources(
    bridge: RegistryBridgeResult, *, goal: object, source_n: int,
) -> tuple[object, ...]:
    """Find uniquely cited earlier group results, never unsigned DB rows.

    For a fixed source_n, competing nonidentical group structures are
    ambiguous, not alternatives the solver may select for convenience.
    """
    from phase169_r10e1_general_group_transport.transport import (
        _goal_group, generator_images_for_group_transport,
    )
    target = _goal_group(goal)
    if target is None or type(source_n) is not int:
        return ()
    k = target.group_dimension - target.sphere_dimension
    if (type(k) is not int or k < 0
            or source_n < k + 2 or source_n >= target.sphere_dimension):
        return ()
    expected_group_dimension = source_n + k
    matched: list[object] = []
    for link in bridge.proof_links:
        step = link.step
        if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or reference.publication_position is None
                or step.premises
                or step.conclusion != assertion.content):
            continue
        group = _goal_group(step.conclusion)
        if (group is None or group.sphere_dimension != source_n
                or group.group_dimension != expected_group_dimension):
            continue
        if generator_images_for_group_transport(step.conclusion, goal) is None:
            continue
        if not any(type(old) is type(step.conclusion)
                   and old == step.conclusion for old in matched):
            matched.append(step.conclusion)
    return tuple(matched) if len(matched) == 1 else ()
```

### `expand_prior_general_group_transport_FULL.py`

```python
def expand_prior_general_group_transport(
    goal: object,
    available: tuple[object, ...],
    bridge: RegistryBridgeResult,
    *,
    proof_target: object,
) -> tuple[GoalExpansion, ...]:
    """Transport a screened earlier result, with or without a cited root target.

    If the goal has its own positioned citing assertion, publication precedence
    is mandatory and the established R7 finite-cyclic behavior is preserved.
    A DB-only goal has no fictional publication position: only uniquely
    screened, independently positioned prior FIXED statements can serve as
    source premises. A same-group source is never accepted.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("typed source bridge required")
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if goal != proof_target or _goal_group(goal) is None:
        return ()
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
    if isinstance(goal, Relation) and isinstance(goal.rhs, FiniteCyclicGroup):
        from phase169_r7_general_stable_transport.rule import (
            expand_prior_general_stable_transport,
        )
        legacy = expand_prior_general_stable_transport(
            goal, available, bridge, proof_target=proof_target,
        )
        if citing_id is not None or legacy:
            return legacy

    for source_n in range(k + 2, n):
        if citing_id is None:
            from phase169_r10e2_unpositioned_citation.source_first import (
                uniquely_screened_prior_sources,
            )
            found = uniquely_screened_prior_sources(
                bridge, goal=goal, source_n=source_n,
            )
            source = found[0] if len(found) == 1 else None
        elif isinstance(goal, TodaPrimaryGroupZeroStatement):
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
        actual_n, stem, r = shape
        iso = Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
            exponent=r,
            source_group=TodaPrimaryGroup(actual_n + stem, actual_n),
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

### `patch.py`

```python
"""Guarded minimal production patch with complete replacement-function outputs."""
from __future__ import annotations

import ast
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"


# No module-level imports change: all additions are local in the full functions.
# Every old anchor has to match EXACTLY once, or the entire patch aborts.
REPLACEMENTS = {
    "phase165_r52_r9_shared_math.py": (
        (
            '''    context_id = citing_assertion_id or assertions[0].assertion_id
    proof_context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=context_id,
        verified_assertion_ids=verified_assertion_ids,
        explicit_publication_target=citing_assertion_id is not None,
    )''',
            '''    context_id = citing_assertion_id or assertions[0].assertion_id
    if citing_assertion_id is None:
        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        proof_context = screen_independent_sources_for_derived_goal(
            bridge, goal=goal,
        )
    else:
        proof_context = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=context_id,
            verified_assertion_ids=verified_assertion_ids,
            explicit_publication_target=True,
        )''',
        ),
    ),
    "phase168_r3_5_model_renderer.py": (
        (
            '        if locator == "Chapter V, i)":\n            locator = "η 系列の定義（Chapter V, i）"',
            '        # Display the cited locator verbatim; no series-specific alias.',
        ),
    ),
    "phase165_r55_nk_only_goal.py": (
        (
            '''        from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
        from phase165_r52_r2_search_adapter import search_registered_partial_proof''',
            '''        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        from phase165_r52_r2_search_adapter import search_registered_partial_proof''',
        ),
        (
            '''        # DB goals have no publication assertion. Preserve the existing
        # implicit-target citation policy without inventing a citing ID.''',
            '''        # The DB target has no publication position. Cite only independently
        # positioned fixed source statements; invent no target citation ID.''',
        ),
        (
            '''        screened = screen_shared_proof_context(
            bridge, goal=candidate, citing_assertion_id=context_id,
        )''',
            '''        screened = screen_independent_sources_for_derived_goal(
            bridge, goal=candidate,
        )''',
        ),
    ),
    "web_group_proof.py": (
        (
            '''    if citing_id is None:
      raise UnverifiedProofTree("complete proof has no positioned citing assertion")
    # Unsupported origins and invalid inferences are rejected by the existing
    # single proof-tree checker; do not silently skip its invocation here.
    verify_proof_tree_for_narrative(
      result, model_bridge, citing_assertion_id=citing_id,
    )''',
            '''    # A DB goal need not have a publication assertion. For this derived-only
    # route, require an actual typed group target before invoking the gate.
    # Synthetic/untyped completed results retain the previous fail-closed path.
    if citing_id is None:
      from homotopy_groups import TodaPrimaryGroupZeroStatement
      from proof import Relation, RelationType
      valid_derived_group = (
        isinstance(result.conclusion, Relation)
        and result.conclusion.relation_type is RelationType.EQUALITY
        and result.conclusion.lhs == result.target
      ) or (
        isinstance(result.conclusion, TodaPrimaryGroupZeroStatement)
        and result.conclusion.group == result.target
      )
      if not valid_derived_group:
        raise UnverifiedProofTree("complete unpositioned proof lacks a typed group target")
    # Keep the existing positioned-Goal call signature byte-for-byte.
    # The new keyword is passed only to genuinely unpositioned targets.
    if citing_id is None:
      verify_proof_tree_for_narrative(
        result, model_bridge, citing_assertion_id=None,
        derived_target_without_citing_id=True,
      )
    else:
      verify_proof_tree_for_narrative(
        result, model_bridge, citing_assertion_id=citing_id,
      )''',
        ),
    ),
    "phase168_r3_41p13_trust_boundary/verification.py": (
        (
            '''    citing_assertion_id: str,
) -> tuple[int, int]:''',
            '''    citing_assertion_id: str | None,
    derived_target_without_citing_id: bool = False,
) -> tuple[int, int]:''',
        ),
        (
            '''    if not isinstance(citing_assertion_id, str) or not citing_assertion_id:
        raise ValueError("citing_assertion_id must identify a positioned goal")
    bridge.registry.assertion(citing_assertion_id)''',
            '''    if derived_target_without_citing_id:
        if citing_assertion_id is not None:
            raise ValueError("derived-target mode requires no citing assertion")
        if result.status is not ProofSearchStatus.COMPLETE:
            raise ValueError("derived-target mode requires a completed proof")
        if not any(
            step.rule is ProofRule.INFERENCE
            and step.conclusion == result.conclusion
            for step in result.proven_steps
        ):
            raise UnverifiedProofTree("an uncited goal must be independently inferred")
    else:
        if not isinstance(citing_assertion_id, str) or not citing_assertion_id:
            raise ValueError("citing_assertion_id must identify a positioned goal")
        bridge.registry.assertion(citing_assertion_id)''',
        ),
        (
            '''                            and precedes_citing_assertion(
                                bridge, link.assertion_id, citing_assertion_id
                            )):''',
            '''                            and (
                                (
                                    derived_target_without_citing_id
                                    and bridge.registry.reference(
                                        assertion.reference_id
                                    ).publication_position is not None
                                    and assertion.content != result.conclusion
                                    and not _same_group_as_derived_target(
                                        assertion.content, result.conclusion
                                    )
                                )
                                or (
                                    not derived_target_without_citing_id
                                    and precedes_citing_assertion(
                                        bridge, link.assertion_id,
                                        citing_assertion_id,
                                    )
                                )
                            )):''',
        ),
        (
            '''    checked: set[int] = set()''',
            '''    def _same_group_as_derived_target(source: object, target: object) -> bool:
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from proof import Relation
        source_group = (
            source.group if isinstance(source, TodaPrimaryGroupZeroStatement)
            else source.lhs if isinstance(source, Relation) else None
        )
        target_group = (
            target.group if isinstance(target, TodaPrimaryGroupZeroStatement)
            else target.lhs if isinstance(target, Relation) else None
        )
        return source_group is not None and source_group == target_group

    checked: set[int] = set()''',
        ),
    ),
}


FUNCTIONS = {
    "phase165_r52_r9_shared_math.py": ("search_shared_group_goal",),
    "phase165_r55_nk_only_goal.py": ("search_group_from_registered_goal",),
    "web_group_proof.py": ("build_standard_web_group_proof_view",),
    "phase168_r3_5_model_renderer.py": (
        "render_model_backed_narrative_markdown",
    ),
    "phase168_r3_41p13_trust_boundary/verification.py": (
        "verify_proof_tree_for_narrative",
    ),
    "phase169_r10e1_general_group_transport/transport.py": (
        "expand_prior_general_group_transport",
    ),
}


def _full_function(source: str, function_name: str) -> str:
    tree = ast.parse(source)
    matches = tuple(
        node for node in tree.body if isinstance(node, ast.FunctionDef)
        and node.name == function_name
    )
    if len(matches) != 1:
        raise RuntimeError("expected one full function: " + function_name)
    node = matches[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def transform(name: str, raw: bytes) -> tuple[bytes, dict[str, str]]:
    crlf = b"\r\n" in raw
    source = raw.decode("utf-8-sig").replace("\r\n", "\n")
    original = source
    if name == "phase169_r10e1_general_group_transport/transport.py":
        new_function = (HERE / "expand_prior_general_group_transport_FULL.py").read_text(
            encoding="utf-8",
        )
        old_function = _full_function(source, "expand_prior_general_group_transport")
        source = source.replace(old_function, new_function, 1)
    else:
        for old, new in REPLACEMENTS[name]:
            if source.count(old) != 1 or new in source:
                raise RuntimeError("R10E2 source anchor mismatched: " + name)
            source = source.replace(old, new, 1)
    if source == original:
        raise RuntimeError("R10E2 expected changed source: " + name)
    ast.parse(source)
    extracted = {fn: _full_function(source, fn) for fn in FUNCTIONS[name]}
    serialized = source.encode("utf-8")
    if crlf:
        serialized = serialized.replace(b"\n", b"\r\n")
    return serialized, extracted


def main() -> None:
    import sys
    OUTPUT.mkdir(parents=True, exist_ok=True)
    changed = []
    files = list(FUNCTIONS)
    for name in files:
        p = ROOT / name
        if not p.is_file():
            raise RuntimeError("R10E2 required production module missing: " + name)
        original = p.read_bytes()
        new_content, full = transform(name, original)
        changed.append((p, name, original, new_content, full))
    # All files validated before any write.
    for path, name, original, new_content, full in changed:
        destination = OUTPUT / (name.replace("/", "__") + ".before")
        destination.write_bytes(original)
        (OUTPUT / (name.replace("/", "__") + ".FULL")).write_bytes(new_content)
        for fn, code in full.items():
            f = OUTPUT / (fn + "_FULL.py")
            f.write_text(code, encoding="utf-8")
            print("R10E2R1_FULL_FUNCTION=" + str(f))
    try:
        for path, name, original, new_content, full in changed:
            temp = path.with_name(path.name + ".r10e2-tmp")
            temp.write_bytes(new_content)
            os.replace(temp, path)
            print("R10E2R1_PATCHED=" + str(path))
    except Exception:
        for path, name, original, new_content, full in changed:
            path.write_bytes(original)
        raise
    print("R10E2R1_PATCH_COUNT=" + str(len(changed)))


if __name__ == "__main__":
    main()
```

### `audit.py`

```python
"""Focused source-first audit: report goals, evidence and completion separately."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates, search_group_from_registered_goal,
)
from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase169_r10e1_general_group_transport.transport import (
    _goal_group, _components, generator_images_for_group_transport,
)
from proof import ProofRule, Relation

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
REGRESSIONS = ((8, 1), (8, 2), (8, 3))
CASES = ((8, 4), (8, 6), (15, 7), (15, 8), (15, 9))


def describe_goal(bridge, n: int, k: int) -> dict:
    zero = database_zero_group_goal_candidates(n=n, k=k)
    goals = zero if zero else registered_group_goal_candidates(bridge, n=n, k=k)
    found = []
    for goal in goals:
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
        group = _goal_group(goal)
        prior = []
        for link in screened.proof_links:
            if link.step is None or link.step.rule is not ProofRule.GIVEN:
                continue
            source = link.step.conclusion
            source_group = _goal_group(source)
            if (source_group is None or group is None
                    or not all(type(x) is int for x in (
                        source_group.group_dimension, source_group.sphere_dimension,
                        group.group_dimension, group.sphere_dimension,
                    ))):
                continue
            if (source_group.group_dimension - source_group.sphere_dimension
                    != group.group_dimension - group.sphere_dimension):
                continue
            if source_group.sphere_dimension >= group.sphere_dimension:
                continue
            images = generator_images_for_group_transport(source, goal)
            prior.append({
                'source': f'pi_{source_group.group_dimension}^{source_group.sphere_dimension}',
                'assertion_id': link.assertion_id,
                'images_possible': images is not None,
                'image_goal_count': len(images) if images is not None else None,
            })
        result = search_group_from_registered_goal(n=n, k=k, goal=goal, bridge=bridge)
        found.append({
            'goal_kind': 'zero' if isinstance(goal, TodaPrimaryGroupZeroStatement)
                         else type(goal.rhs).__name__ if isinstance(goal, Relation)
                         else type(goal).__name__,
            'screened_source_count': len(screened.proof_links),
            'suitable_prior_source_candidates': prior,
            'status': result.status.value,
            'open_goal_count': len(result.open_goals),
            'proof_step_count': len(result.proven_steps),
        })
    return {'group': f'pi_{n+k}^{n}', 'goals': found}


def main() -> None:
    bridge = build_shared_typed_bridge()
    regressions = []
    for n, k in REGRESSIONS:
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        case = {'group': f'pi_{n+k}^{n}', 'status': result.status.value}
        regressions.append(case)
        print('R10E2_' + case['group'] + '_STATUS=' + case['status'])
    if any(x['status'] != 'complete' for x in regressions):
        raise RuntimeError('R10E2 regressed a completed 1-, 2-, or 3-stem group')
    boundaries = [describe_goal(bridge, n, k) for n, k in CASES]
    for case in boundaries:
        info = case['goals']
        statuses = ','.join(x['status'] for x in info) if info else 'no_goal'
        candidates = sum(len(x['suitable_prior_source_candidates']) for x in info)
        print('R10E2_' + case['group'] + '_STATUS=' + statuses)
        print('R10E2_' + case['group'] + '_POSITIONED_SOURCE_COUNT=' + str(candidates))
    result = {
        'phase': '169 R10E2',
        'head': subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,
                               text=True,capture_output=True,check=True).stdout.strip(),
        'kind': 'FOCUSED_IMPLEMENTATION_AUDIT',
        'regressions': regressions,
        'boundaries': boundaries,
        'target_publication_position_invented': False,
        'mathematical_proof_from_csv': False,
        'full_pytest_run': False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / 'audit.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    print('R10E2_AUDIT=' + str(path))
    print('R10E2_FULL_PYTEST_RUN=False')


if __name__ == '__main__':
    main()
```

### `tests/test_r10e2_unpositioned_citation.py`

```python
"""R10E2: unpositioned goal uses only screened positioned source assertions."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import (
    FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree, verify_proof_tree_for_narrative,
)
from phase169_r10e1_general_group_transport.transport import (
    expand_prior_general_group_transport,
)
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
    uniquely_screened_prior_sources,
)
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def _element(family_id: int, n: int) -> HomotopyElement:
    family = next(x for x in read_registered_stable_families()
                  if x.family_id == family_id)
    return HomotopyElement(
        name=family.name_at(n),
        dimension=n, source=n + family.stem, target=n,
        generator=GeneratorSymbol(family=family.symbol_family, index=n),
    )


def _relation(family_id: int, n: int, order: int) -> Relation:
    family = next(x for x in read_registered_stable_families()
                  if x.family_id == family_id)
    return Relation(
        TodaPrimaryGroup(n + family.stem, n),
        FiniteCyclicGroup(order, _element(family_id, n)),
        RelationType.EQUALITY,
    )


def _bridge(*statements, positioned=True, extra_links=()) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    links = list(extra_links)
    for i, content in enumerate(statements):
        ref_id = f"r10e2:source:{i}"
        assertion_id = f"r10e2:assertion:{i}"
        registry.add_reference(LiteratureEntry(
            ref_id, ReferenceKind.PROPOSITION, "Proposition test " + str(i),
            publication_position=(8400 + i * 100) if positioned else None,
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id, ref_id, AssertionKind.STATEMENT, content,
            AssertionOrigin.FIXED_STATEMENT, component_position=100,
        ))
        if i == 0 and extra_links:
            continue
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            content, (), ProofRule.GIVEN,
        )))
    return RegistryBridgeResult(registry, (), tuple(links))


def _iso(n: int, k: int, r: int):
    return Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
        exponent=r,
        source_group=TodaPrimaryGroup(n + k, n),
        target_group=TodaPrimaryGroup(n + k + r, n + r),
    ))


def test_r10e2_positioned_sigma_source_generates_unpositioned_candidate():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source), goal=goal,
    )
    assert len(screened.proof_links) == 1
    assert uniquely_screened_prior_sources(screened, goal=goal, source_n=9) == (source,)
    options = expand_prior_general_group_transport(
        goal, (_iso(9, 7, 3),), screened, proof_target=goal,
    )
    # The registry family metadata supplies types only; the suspension image
    # is still a separate Goal and requires independent proof.
    assert len(options) == 1
    assert options[0].subgoals[0] == source
    assert options[0].subgoals[1] == _iso(9, 7, 3)
    assert len(options[0].subgoals) == 5
    assert all(type(step).__name__ != 'ProofStep' for step in options[0].subgoals)


def test_r10e2_unpositioned_target_is_not_inserted_as_given():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source, goal), goal=goal,
    )
    assert len(screened.proof_links) == 1
    assert screened.proof_links[0].step.conclusion == source


def test_r10e2_missing_publication_position_is_not_a_proof_source():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source, positioned=False), goal=goal,
    )
    assert screened.proof_links == ()
    assert uniquely_screened_prior_sources(screened, goal=goal, source_n=9) == ()
    assert expand_prior_general_group_transport(
        goal, (_iso(9, 7, 3),), screened, proof_target=goal,
    ) == ()


def test_r10e2_inconsistent_given_is_rejected():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    forged = ProofStep(goal, (), ProofRule.GIVEN)
    bridge = _bridge(source, extra_links=(ProofStepLink(
        'r10e2:assertion:0', step=forged,
    ),))
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    assert screened.proof_links == ()


def test_r10e2_competing_source_structures_fail_closed():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    other = replace(source, rhs=FiniteCyclicGroup(8, source.rhs.generator))
    # Different presentations cannot be selected by ordering the candidates.
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source, other), goal=goal,
    )
    assert uniquely_screened_prior_sources(screened, goal=goal, source_n=9) == (source,)
    # Only the 16-torsion source fits this target. Two genuinely matching
    # different source structures will be refused as ambiguous.
    assert len(screened.proof_links) == 2


def test_r10e2_zero_groups_need_no_generator_image():
    source = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 8))
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source), goal=goal,
    )
    options = expand_prior_general_group_transport(
        goal, (_iso(6, 4, 2),), screened, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals == (source, _iso(6, 4, 2))


def test_r10e2_no_unpositioned_root_given_can_pass_verifier():
    from phase165_r52_partial_proof import (
        ProofSearchStatus, GroupStructureStatus, make_partial_proof_result,
    )
    goal = _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(goal), goal=goal,
    )
    direct = ProofStep(goal, (), ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=12, k=7, structure_status=GroupStructureStatus.UNKNOWN,
        status=ProofSearchStatus.COMPLETE,
        proven_steps=(direct,), conclusion=goal,
    )
    with pytest.raises(UnverifiedProofTree):
        verify_proof_tree_for_narrative(
            result, screened, citing_assertion_id=None,
            derived_target_without_citing_id=True,
        )


def test_r10e2_positioned_existing_citation_api_is_unchanged():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    bridge = _bridge(source)
    from phase165_r52_partial_proof import (
        ProofSearchStatus, make_partial_proof_result,
    )
    result = make_partial_proof_result(
        n=12, k=7, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(goal,),
        diagnostics=("purposefully unresolved test goal",),
    )
    with pytest.raises(ValueError, match='positioned goal'):
        verify_proof_tree_for_narrative(
            result, bridge, citing_assertion_id=None,
        )


def test_r10e2_guarded_patch_refuses_double_application():
    from phase169_r10e2_unpositioned_citation.patch import transform
    target = 'phase169_r10e1_general_group_transport/transport.py'
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    before = root / "phase169_r10e2_unpositioned_citation" / "output" / (
        target.replace("/", "__") + ".before"
    )
    original = before.read_bytes()
    updated, functions = transform(target, original)
    assert 'uniquely_screened_prior_sources' in functions[
        'expand_prior_general_group_transport'
    ]
    assert updated == (root / target).read_bytes()
    with pytest.raises(RuntimeError, match='expected changed source'):
        transform(target, updated)


def test_r10e2r1_renderer_keeps_frozen_reference_locator():
    from pathlib import Path

    renderer = (Path(__file__).resolve().parents[2]
                / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8")
    assert 'locator = citation.reference.locator or citation.reference.label' in renderer
    assert 'locator = "η 系列の定義（Chapter V, i）"' not in renderer
```

### `run.ps1`

```powershell
$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Resolve-Path (Join-Path $folder '..')).Path
$backupFolder = Join-Path $folder 'output'
$targets = @(
    'phase165_r52_r9_shared_math.py',
    'phase165_r55_nk_only_goal.py',
    'web_group_proof.py',
    'phase168_r3_41p13_trust_boundary/verification.py',
    'phase169_r10e1_general_group_transport/transport.py',
    'phase168_r3_5_model_renderer.py'
)
$patched = $false
$passed = $false
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldAddopts = $env:PYTEST_ADDOPTS
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R10E2R1 requires develop.' }
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R1 failed to inspect HEAD.' }
    Write-Host "R10E2R1_BRANCH=$branch"
    Write-Host "R10E2R1_HEAD=$head"
    $required = @(
        'phase169_r10e1_general_group_transport/transport.py',
        'phase169_r10d2_general_family_definition/family_citation.py',
        'phase169_r10b_registered_stable_family_binding/family_registry.py',
        'data/HyoujiGen.csv'
    )
    foreach ($item in $required) {
        if (-not (Test-Path (Join-Path $root $item))) {
            throw "R10E2R1 missing prerequisite: $item"
        }
    }
    $exclude = @(':!' + 'phase165_r52_r9_shared_math.py',
                 ':!' + 'phase165_r55_nk_only_goal.py',
                 ':!' + 'web_group_proof.py',
                 ':!' + 'phase168_r3_41p13_trust_boundary/verification.py',
                 ':!' + 'phase169_r10e1_general_group_transport/transport.py',
                 ':!' + 'phase168_r3_5_model_renderer.py')
    $beforeOther = @(git diff --name-only -- . $exclude | Sort-Object)
    if ($LASTEXITCODE -ne 0) { throw 'R10E2 cannot inspect unrelated files.' }
    python -m phase169_r10e2_unpositioned_citation.patch
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R1 guarded production patch failed.' }
    $patched = $true
    python -m pytest -q `
        (Join-Path $folder 'tests/test_r10e2_unpositioned_citation.py') `
        (Join-Path $root 'phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py') `
        (Join-Path $root 'phase169_r7_general_stable_transport/tests/test_r7_general_stable_transport.py') `
        (Join-Path $root 'phase169_r10b_registered_stable_family_binding/tests/test_r10b_registered_family.py') `
        (Join-Path $root 'phase169_r10d2_general_family_definition/tests/test_r10d2_general_family.py') `
        (Join-Path $root 'phase169_r10a2_unified_one_stem/tests/test_r10a2_one_stem_projection.py') `
        (Join-Path $root 'phase168_r3_41p13_trust_boundary/tests/test_phase168_r3_41p13_trust_boundary.py') `
        (Join-Path $root 'phase168_r3_41p15_complete_fail_closed/tests/test_phase168_r3_41p15_complete_fail_closed.py') `
        (Join-Path $root 'phase168_r3_41p19_phase_closeout/tests/test_phase168_r3_41p19_phase_closeout.py')
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R1 focused pytest failed.' }
    python -m phase169_r10e2_unpositioned_citation.audit
    if ($LASTEXITCODE -ne 0) { throw 'R10E2R1 focused audit failed.' }
    $afterOther = @(git diff --name-only -- . $exclude | Sort-Object)
    if ($LASTEXITCODE -ne 0 -or ($beforeOther -join "`n") -ne ($afterOther -join "`n")) {
        throw 'R10E2R1 detected unrelated tracked changes.'
    }
    $passed = $true
    Write-Host 'R10E2R1_LIMITED_TESTS_AND_AUDIT=PASS'
    Write-Host ('R10E2R1_PRODUCTION_FILES_CHANGED=' + ($targets -join ','))
    Write-Host 'R10E2R1_FULL_PYTEST_RUN=False'
} finally {
    if ($patched -and -not $passed) {
        foreach ($target in $targets) {
            $backupName = $target.Replace('/', '__') + '.before'
            $old = Join-Path $backupFolder $backupName
            if (-not (Test-Path $old)) { throw "R10E2R1 backup missing: $backupName" }
            [System.IO.File]::WriteAllBytes((Join-Path $root $target), [System.IO.File]::ReadAllBytes($old))
        }
        Write-Host 'R10E2R1_ROLLBACK_APPLIED=True'
    }
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTEST_ADDOPTS = $oldAddopts
    Pop-Location
}
```
