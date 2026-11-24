# Phase 176 R3R46R1 変更コード全文

既存ファイルの変更後関数全文は実行時に `SHARED_FUNCTIONS_FULL_JA.md` を生成します。新規の Python コードおよび追加関数は以下のとおりです。

## `__init__.py`

```python
"""Shared admitted prior-group availability and zero-goal pruning."""
```

## `apply.py`

```python
"""Guarded three-file patch. Preserve EOLs and all unrelated source bytes."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
DB = 'phase169_r10e4_ordered_db_prior/db_prior.py'
DFS = 'phase165_r3_recursive_search.py'
SHARED = 'phase165_r52_r9_shared_math.py'
PINS = {
    DB: 'ed8c6a1f0f6f130005d42a2edba4ab40991e879b',
    DFS: '06009bfcf57f99cac58c229d99c53f16324692d0',
    SHARED: '2dca975cd4a9e1353c3022c791d98817575f2ced',
}
# Rule bodies relied on by the new connection, not modified here.
DEPENDENCIES = {
    'phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py': '66407339808ed4ba8a65c04fd3bfbbf05bde6745',
    'phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py': 'dfa1519c629eef92ca1c5dae265acc050883649b',
    'phase175_r4r14r9_literature_zero_image/rule.py': '82d69284c16a3e77eacf1b23a4eb84a13249dd56',
    'phase176_r3r16_public_connection/provider.py': 'c34306ab748fb3a6ca559efc596e2f4e98b100ca',
}
DFS_SETUP_ANCHOR = '    def resolve(target: object) -> ProofStep:\n'
DFS_SETUP = '''    from phase176_r3r46r1_prior_group_availability.pruning import contradiction_witness

    def contradicted(target: object) -> bool:
        return contradiction_witness(
            target, bridge=bridge, citing_id=citing_assertion_id,
            lookup_mode=lookup_mode, verified_assertion_ids=verified_assertion_ids,
            proof_target=goal, solved=tuple(solved),
            completed_internal_proofs=completed_internal_proofs,
        ) is not None

'''
DFS_GOAL_ANCHOR = '            expansions = expansion_provider(actual)\n'
DFS_GOAL = '''            # Reject an impossible unproved zero obligation before its Provider.
            if contradicted(target):
                raise RegisteredGoalUnresolved("zero goal contradicted by eligible nonzero evidence")
'''
DFS_BRANCH_ANCHOR = '                try:\n                    premises = tuple(resolve(child) for child in expansion.subgoals)\n'
DFS_BRANCH = '''                # Preflight all immediate zero obligations before visiting any.
                if any(contradicted(child) for child in expansion.subgoals):
                    continue
'''
SHARED_ANCHOR = '    shared_provider_registry = build_shared_expansion_provider_registry(\n'
SHARED_SETUP = '''    # R3R46R1: reuse admitted prior domains without the stable-family gate.
    # Append after the existing source-specific providers; no new rule.
    from phase176_r3r46r1_prior_group_availability.provider import build_prior_zero_image_provider
    extra_providers = tuple(extra_providers) + (
        build_prior_zero_image_provider(bridge=bridge, proof_target=proof_target),
    )

'''


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def normalize(raw):
    if b'\r' in raw.replace(b'\r\n', b'') or (b'\r\n' in raw and b'\n' in raw.replace(b'\r\n', b'')):
        raise ValueError('MIXED_LINE_ENDINGS')
    return raw.decode('utf-8').replace('\r\n', '\n'), '\r\n' if b'\r\n' in raw else '\n'


def pinned(text, pin):
    return pin in (blob(text.encode('utf-8')), blob(text.replace('\n','\r\n').encode('utf-8')))


def checked_insertions(text, pairs, pin):
    """Accept only the reviewed baseline or the exact idempotent new patch."""
    if any(chunk in text for chunk, _ in pairs):
        if not all(text.count(chunk + anchor) == 1 for chunk, anchor in pairs):
            raise ValueError('PARTIAL_OR_MOVED_PATCH')
        for chunk, anchor in pairs:
            text = text.replace(chunk + anchor, anchor, 1)
    if not pinned(text, pin):
        raise ValueError('UNREVIEWED_SOURCE_BLOB')
    for chunk, anchor in pairs:
        if text.count(anchor) != 1:
            raise ValueError('ANCHOR_NOT_UNIQUE')
        text = text.replace(anchor, chunk + anchor, 1)
    return text


def updated_source(path, raw):
    text, newline = normalize(raw)
    if path == DB:
        addition = '\n\n' + (PACKAGE / 'db_addition.py.txt').read_text(encoding='utf-8')
        if text.endswith(addition):
            text = text[:-len(addition)]
        if not pinned(text, PINS[path]):
            raise ValueError('UNREVIEWED_DB_PRIOR_BLOB')
        changed = text + addition
    elif path == DFS:
        changed = checked_insertions(text, ((DFS_SETUP, DFS_SETUP_ANCHOR),
                    (DFS_GOAL, DFS_GOAL_ANCHOR), (DFS_BRANCH, DFS_BRANCH_ANCHOR)), PINS[path])
    elif path == SHARED:
        changed = checked_insertions(text, ((SHARED_SETUP, SHARED_ANCHOR),), PINS[path])
    else:
        raise ValueError('UNKNOWN_PATCH_TARGET')
    ast.parse(changed)
    return changed.replace('\n', newline).encode('utf-8')


def planned_changes():
    if subprocess.check_output(['git','branch','--show-current'], cwd=ROOT, text=True).strip() != 'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    for path, pin in DEPENDENCIES.items():
        text, _ = normalize((ROOT / path).read_bytes())
        if not pinned(text, pin):
            raise ValueError('UNREVIEWED_DEPENDENCY:' + path)
    planned = {}
    for path in PINS:
        original = (ROOT / path).read_bytes()
        try:
            changed = updated_source(path, original)
        except ValueError as exc:
            raise ValueError(path + ': ' + str(exc)) from exc
        planned[path] = original, changed
    return planned


def write_full_functions(planned):
    names = {DB:'admitted_prior_group_step', DFS:'reconstruct_registered_goal',
             SHARED:'shared_expansion_provider'}
    docs = ['# 変更後の関数全文\n']
    for path, (_, raw) in planned.items():
        source, _ = normalize(raw)
        node = next(n for n in ast.parse(source).body
                    if isinstance(n, ast.FunctionDef) and n.name == names[path])
        full = '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno])
        docs.append('## `' + path + '`\n\n```python\n' + full + '\n```\n')
    (PACKAGE / 'SHARED_FUNCTIONS_FULL_JA.md').write_text('\n'.join(docs), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    planned = planned_changes()
    if not args.dry_run:
        # Check all files before writing any, and roll back a failed write.
        written = []
        try:
            for path, (old, new) in planned.items():
                if old != new:
                    written.append(path)
                    (ROOT / path).write_bytes(new)
            write_full_functions(planned)
        except BaseException:
            for path in written:
                (ROOT / path).write_bytes(planned[path][0])
            raise
    print('PHASE176_R3R46R1_HEAD=' + subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    print('PHASE176_R3R46R1_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## `audit.py`

```python
"""Actual public query audit; distinguish candidate, admitted, and accepted evidence."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective, MapSurjective
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME
from phase176_r3r46r1_prior_group_availability import pruning
from phase176_r3r46r1_prior_group_availability.apply import planned_changes
from proof import ProofRule


def observe():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from web_group_proof import build_standard_web_group_proof_view

    calls, rejected, invocations, results = [], [], [], []
    original_entry = entry.search_group_from_registered_goal
    original_adapter = shared.search_registered_partial_proof
    original_check = pruning.contradiction_witness

    def observed_entry(*args, **kwargs):
        result = original_entry(*args, **kwargs)
        results.append(result)
        return result

    def observed_adapter(*args, **kwargs):
        if (kwargs.get('n'), kwargs.get('k')) != (3, 5):
            return original_adapter(*args, **kwargs)
        invocations.append(dict(kwargs))
        forwarded = dict(kwargs)
        provider = kwargs['expansion_provider']

        def observed_provider(goal):
            options = provider(goal)
            calls.append((goal, options))
            return options

        forwarded['expansion_provider'] = observed_provider
        return original_adapter(*args, **forwarded)

    def recorded_check(goal, **kwargs):
        evidence = original_check(goal, **kwargs)
        if evidence is not None:
            rejected.append((goal, evidence))
        return evidence

    with patch.object(entry, 'search_group_from_registered_goal', new=observed_entry), \
         patch.object(shared, 'search_registered_partial_proof', new=observed_adapter), \
         patch.object(pruning, 'contradiction_witness', new=recorded_check):
        view = build_standard_web_group_proof_view(n=3, k=5, max_depth=2, mode='narrative')
    if len(invocations) != 1 or len(results) != 1:
        raise RuntimeError('UNEXPECTED_PUBLIC_ENTRY_COUNT')
    invocation, result = invocations[0], results[0]
    root, context = invocation['goal'], invocation['bridge']
    source = TodaPrimaryGroup(7, 2)
    zero = TodaPrimaryGroupZeroStatement(source)
    unwanted = MapSurjective(TodaDeltaMap(TodaPrimaryGroup(8, 3), TodaPrimaryGroup(6, 1)))
    zero_map = ImageZeroStatement(TodaSuspensionMap(source, TodaPrimaryGroup(8, 3)))
    injective = MapInjective(TodaHopfInvariantMap(TodaPrimaryGroup(8, 3), TodaPrimaryGroup(8, 5)))
    prior = admitted_prior_group_step(source, proof_target=root, bridge=context)
    if prior is None or not verified_db_step(prior, proof_target=root, bridge=context):
        raise RuntimeError('PRIOR_GROUP_ADMISSION_NOT_AVAILABLE')
    prior_rejections = [step for goal, step in rejected if goal == zero and step == prior]
    zero_calls = [options for goal, options in calls if goal == zero]
    unwanted_calls = [options for goal, options in calls if goal == unwanted]
    map_calls = [options for goal, options in calls if goal == zero_map]
    routes = [option for options in map_calls for option in options if option.rule.name == RULE_NAME]
    accepted_db = [step for step in result.proven_steps if step == prior and verified_db_step(step, proof_target=root, bridge=context)]
    image_goal = None
    if routes:
        candidate = routes[0]
        if (len(candidate.subgoals) != 2 or candidate.subgoals[0] != prior.conclusion
                or type(candidate.subgoals[1]) is not GeneratorImage):
            raise RuntimeError('PRIOR_ZERO_MAP_PREMISES_CHANGED')
        image_goal = candidate.subgoals[1]
    accepted = lambda goal: any(step.conclusion == goal and step.rule is ProofRule.INFERENCE for step in result.proven_steps)
    passed = (bool(prior_rejections) and not zero_calls and not unwanted_calls
              and zero not in result.open_goals and unwanted not in result.open_goals
              and bool(routes) and bool(accepted_db))
    return {
        'gate': 'PASS_R3R46R1_PUBLIC_PRIOR_AVAILABILITY' if passed else 'FAIL_R3R46R1_PUBLIC_PRIOR_AVAILABILITY',
        'status': result.status.value,
        'web_key': view.key,
        'prior_group': repr(prior.conclusion),
        'prior_note': prior.note,
        'prior_db_accepted_count': len(accepted_db),
        'preceding_zero_pruned': bool(prior_rejections),
        'preceding_zero_provider_calls': len(zero_calls),
        'unnecessary_delta_provider_calls': len(unwanted_calls),
        'zero_map_provider_calls': len(map_calls),
        'prior_zero_map_candidate_count': len(routes),
        'generator_image_goal': repr(image_goal),
        'generator_image_proved': image_goal is not None and accepted(image_goal),
        'suspension_zero_proved': accepted(zero_map),
        'hopf_injective_proved': accepted(injective),
        'accepted_step_count': len(result.proven_steps),
        'open_goals': [repr(goal) for goal in result.open_goals],
        'pruning_evidence_not_accepted_by_pruning': [
            {'goal': repr(goal), 'witness': repr(step.conclusion), 'note': step.note,
             'rule': step.rule.value} for goal, step in rejected],
        'actual_provider_order': [
            {'goal': repr(goal), 'rules': [option.rule.name for option in options]}
            for goal, options in calls],
        'new_given_registrations': 0,
        'new_math_rules': 0,
        'full_pytest': 'NOT_RUN',
    }


def main():
    planned = planned_changes()
    if any(old != new for old, new in planned.values()):
        raise RuntimeError('PATCH_NOT_APPLIED')
    report = observe()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r46r1_prior_group_availability'
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / 'report.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key, value in report.items():
        if key != 'actual_provider_order':
            print('PHASE176_R3R46R1_'+key.upper()+'='+json.dumps(value, ensure_ascii=False))
    print('REPORT='+str(destination))
    if any(old != new for old, new in planned_changes().values()):
        raise RuntimeError('SOURCE_CHANGED_DURING_AUDIT')
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
```

## `db_addition.py.txt`

```python
def admitted_prior_group_step(
    group: object, *, proof_target: object,
    bridge: object | None = None,
    csv_path: str | Path | None = None,
    generator_csv: str | Path | None = None,
) -> ProofStep | None:
    """Discover an earlier group by coordinates, then reuse the exact admission gate.

    This is not an additional admission policy. No stable fallback, root
    self-citation or ambiguous row is accepted. A discovered step is not an
    accepted search ProofStep until the ordinary resolver accepts its conclusion.
    """
    if (type(group) is not TodaPrimaryGroup
            or type(group.group_dimension) is not int
            or type(group.sphere_dimension) is not int):
        return None
    n = group.sphere_dimension
    k = group.group_dimension - n
    target = group_coordinates(proof_target)
    if target is None or not precedes_db_goal(n, k, *target):
        return None
    statement = exact_prior_database_result(n, k, csv_path=csv_path,
                                            generator_csv=generator_csv)
    if statement is None or group_coordinates(statement) != (n, k):
        return None
    return admitted_db_step(statement, proof_target=proof_target, bridge=bridge,
                            csv_path=csv_path, generator_csv=generator_csv)
```

## `provider.py`

```python
"""General prior-domain discovery for the existing finite-cyclic zero-image rules."""
from __future__ import annotations

from homotopy_groups import TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import expand_adopted_prior_zero_image
from phase175_r4r14r9_literature_zero_image.rule import expand_literature_zero_image


def build_prior_zero_image_provider(*, bridge, proof_target):
    """Propose the existing two-premise inference without stable-family preconditions.

    The prior's presentation selects a goal; only the ordinary resolver may
    accept the source ProofStep. A linked literature route retains priority.
    Neither the generator image nor the final zero map is assumed here.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError('typed registry bridge required')

    def expand(goal):
        if type(goal) is not ImageZeroStatement or type(goal.map) is not TodaSuspensionMap:
            return ()
        prior = admitted_prior_group_step(goal.map.source_group,
                                          proof_target=proof_target, bridge=bridge)
        if prior is None:
            return ()
        presentation = prior.conclusion
        literature = expand_literature_zero_image(goal, presentation,
                        proof_target=proof_target, bridge=bridge)
        if literature:
            return literature
        return expand_adopted_prior_zero_image(goal, presentation,
                        proof_target=proof_target, bridge=bridge)

    return expand
```

## `pruning.py`

```python
"""Reject zero obligations using eligible nonzero evidence, without proof insertion."""
from __future__ import annotations

from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup,
    TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
)
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import AssertionOrigin

TYPED_MODES = ('typed_reference', 'typed_reference_ordered', 'typed_reference_publication')


def nonzero_presentation(statement, group):
    """Only supported concrete, nontrivial group presentations contradict zero."""
    if (type(group) is not TodaPrimaryGroup
            or type(group.group_dimension) is not int
            or type(group.sphere_dimension) is not int
            or group.sphere_dimension < 2
            or group.group_dimension < group.sphere_dimension
            or type(statement) is not Relation
            or statement.relation_type is not RelationType.EQUALITY
            or statement.lhs != group):
        return False

    def nontrivial(part):
        return (type(part) is FreeCyclicGroup
                or (type(part) is FiniteCyclicGroup
                    and type(part.order) is int and part.order > 1))

    structure = statement.rhs
    return (nontrivial(structure)
            or (type(structure) is DirectSumGroup
                and isinstance(structure.summands, tuple)
                and any(nontrivial(part) for part in structure.summands)))


def fixed_steps(bridge, statement, citing_id, lookup_mode, verified_assertion_ids):
    """Use exactly the solver's fixed-reference eligibility, not the raw catalog."""
    if lookup_mode == 'typed_reference':
        from phase165_r3_recursive_search import _typed_reference_steps
        return _typed_reference_steps(bridge, statement)
    if lookup_mode == 'typed_reference_ordered':
        from phase165_r52_r15_ordered_citation import ordered_typed_reference_steps
        return ordered_typed_reference_steps(
            bridge, statement, citing_id, verified_assertion_ids=verified_assertion_ids,
        )
    if lookup_mode != 'typed_reference_publication':
        return ()
    from phase166_r3c_publication_order import precedes_citing_assertion
    steps = []
    for assertion in bridge.registry._assertions.values():
        if (type(assertion.content) is not type(statement)
                or assertion.content != statement
                or not precedes_citing_assertion(bridge, assertion.assertion_id, citing_id)):
            continue
        links = tuple(link for link in bridge.proof_links
                      if link.assertion_id == assertion.assertion_id)
        if len(links) != 1 or links[0].step is None:
            continue
        step = links[0].step
        if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
                or type(step.conclusion) is not type(statement)
                or step.conclusion != statement):
            raise ValueError('ordered reference has inconsistent ProofStep')
        steps.append(step)
    return tuple(steps)


def contradiction_witness(goal, *, bridge, citing_id, lookup_mode,
                          verified_assertion_ids, proof_target, solved=(),
                          completed_internal_proofs=()):
    """Find a nonzero witness without recursively proving another group.

    Direct eligible zero evidence and reusable exact zero proofs retain
    precedence. SourceBoundGoal is intentionally not unwrapped here. A raw
    DB row or a proposed expansion is never enough for rejection. A returned
    witness is diagnostic only; it is not inserted into the accepted tree.
    """
    if type(goal) is not TodaPrimaryGroupZeroStatement or lookup_mode not in TYPED_MODES:
        return None
    group = goal.group
    if (type(group) is not TodaPrimaryGroup
            or type(group.group_dimension) is not int
            or type(group.sphere_dimension) is not int
            or group.sphere_dimension < 2
            or group.group_dimension < group.sphere_dimension):
        return None
    # Preserve direct source priority and citation ambiguity semantics.
    if fixed_steps(bridge, goal, citing_id, lookup_mode, verified_assertion_ids):
        return None
    for _, step in solved:
        if isinstance(step, ProofStep) and type(step.conclusion) is type(goal) and step.conclusion == goal:
            return None
    if completed_internal_proofs:
        from phase165_r52_r17_internal_dependency import find_reusable_internal_proof
        if find_reusable_internal_proof(goal, proof_target, completed_internal_proofs) is not None:
            return None
    # Prefer an already accepted nonzero result, then eligible fixed sources.
    for _, step in solved:
        if (isinstance(step, ProofStep) and step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
                and step.conclusion != proof_target and nonzero_presentation(step.conclusion, group)):
            return step
    for assertion in bridge.registry._assertions.values():
        statement = assertion.content
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or statement == proof_target or not nonzero_presentation(statement, group)):
            continue
        evidence = fixed_steps(bridge, statement, citing_id, lookup_mode, verified_assertion_ids)
        if len(evidence) == 1 and not evidence[0].premises:
            return evidence[0]
    # The existing admission policy is the authority; no Toda (5.2)
    # re-derivation or independent proof of an adopted DB prior is needed.
    prior = admitted_prior_group_step(group, proof_target=proof_target, bridge=bridge)
    if prior is not None and nonzero_presentation(prior.conclusion, group):
        return prior
    return None
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $parameters = @()
    if ($DryRun) { $parameters += '--dry-run' }
    & python -B -m phase176_r3r46r1_prior_group_availability.apply @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R46R1 guarded patch failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R46R1_GATE=PASS_R3R46R1_DRYRUN'
    } else {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r46r1_prior_group_availability\tests\test_prior_availability.py `
            .\phase169_r10e4_ordered_db_prior\tests\test_r10e4_ordered_db_prior.py `
            .\phase174_r3_r7_r40_adopted_db_zero_image_isolated\tests\test_rule.py `
            .\phase171_r20r2_first_successful_search\tests\test_first_successful_search.py `
            .\tests\test_phase165_r3_recursive_search.py `
            .\phase176_r3r45_direct_premise_audit\tests\test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R46R1 focused pytest failed' }
        & python -B -m phase176_r3r46r1_prior_group_availability.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R46R1 Web audit failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R46R1 diff check failed' }
        Write-Host 'PHASE176_R3R46R1_GATE=PASS_R3R46R1_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R46R1_NEW_MATH_RULES=0'
        Write-Host 'PHASE176_R3R46R1_NEW_GIVEN_REGISTRATIONS=0'
        Write-Host 'PHASE176_R3R46R1_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally { Pop-Location }
```

## `tests/test_prior_availability.py`

```python
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
        assert updated_source(path, raw) == raw
        with pytest.raises(ValueError):
            updated_source(path, raw + b'\n# unexpected edit\n')
```
