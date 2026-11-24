# R3R44 新規コード全文

共有関数は `apply.py` が検証済み現行ソースから全文を `SHARED_FUNCTION_FULL_JA.md` に生成します。

## __init__.py

```python
"""Phase 176 R3R44: public candidate wiring only."""

```

## provider.py

```python
"""Bind the existing subgroup-lift rule to ordinary backward goals.

Concrete presentations (including DB candidates) are only variable bindings.
The rule still requires five independently inferred ProofSteps.
"""
from __future__ import annotations

from expression import MapApplication, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_H_MAP
from phase165_r12_r2_quotient_rules import CyclicStructureStatement, KernelMultipleStatement
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import expand_finite_cyclic_subgroup_lift
from proof import Relation, RelationType


def build_public_subgroup_lift_provider(available: tuple, prior_conclusions: tuple = ()):
    """Source/prior candidates first, typed DB candidate last; no proof insertion."""
    if not isinstance(available, tuple) or not isinstance(prior_conclusions, tuple):
        raise TypeError("source and prior candidates must be tuples")

    def expand(goal):
        if (type(goal) is not CyclicStructureStatement
                or type(goal.group) is not TodaPrimaryGroup
                or type(goal.order) is not int or goal.order < 2):
            return ()
        a = goal.group
        i, n = a.group_dimension, a.sphere_dimension
        if type(i) is not int or type(n) is not int or n < 3 or i < 2*n-1:
            return ()
        b, c = TodaPrimaryGroup(i, 2*n-1), TodaPrimaryGroup(i-2, n-1)
        exact = EHPImageEqualsKernelStatement(TodaEHPExactnessWindow(a, b, c, EHP_H_MAP, EHP_DELTA_MAP))
        groups = []

        def add(item):
            if (type(item) is Relation and item.relation_type is RelationType.EQUALITY
                    and item.lhs == b and type(item.rhs) is FiniteCyclicGroup
                    and type(item.rhs.order) is int and item.rhs.order > goal.order
                    and item.rhs.order % goal.order == 0 and item not in groups):
                groups.append(item)

        for item in available + prior_conclusions:
            add(item)
            if type(item) is Relation:
                add(specialize_registered_higher_stem(item, b.sphere_dimension))
        # A DB presentation is a candidate for an OPEN codomain goal, never a
        # source leaf or a verified result. It can bind otherwise unknown b,m.
        for item in database_structured_group_goal_candidates(n=b.sphere_dimension,
                                                              k=i-b.sphere_dimension):
            add(item)
        options = []
        for group in groups:
            # Canonical generator of a subgroup of the requested order. The
            # equality H(a)=qb must still be proved; no unit/sign is assumed.
            q = group.rhs.order // goal.order
            generator = group.rhs.generator
            kernel = KernelMultipleStatement(TodaDeltaMap(b,c), b, generator, q)
            image = Relation(MapApplication(EHP_H_MAP, goal.generator), Multiple(q,generator), RelationType.EQUALITY)
            for option in expand_finite_cyclic_subgroup_lift(goal, exact, group, kernel, image):
                if not any(old.subgoals == option.subgoals for old in options):
                    options.append(option)
        return tuple(options)

    return expand

```

## apply.py

```python
"""Apply exactly two local hooks to the reviewed shared provider, preserving bytes."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r52_r9_shared_math.py'
BASE = '165f2d0ad78e0dcb05d01ec0784b974a92c5ee02'
ISOLATED = ROOT / 'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/rule.py'
RULE_HASH = 'f0df5964beb9c32eec0ae2ec674e0330b046327e6e4aeb18ad0d60e0926ad401'
SETUP_ANCHOR = '    if not isinstance(prior_conclusions, tuple):\n        raise TypeError("prior_conclusions must be a tuple")\n'
SETUP = '''    # Phase 176 R3R44: bind five open obligations to the existing isolated rule.
    from phase176_r3r44_public_subgroup_lift.provider import (
        build_public_subgroup_lift_provider,
    )
    public_subgroup_lift = build_public_subgroup_lift_provider(
        tuple(available), prior_conclusions,
    )
'''
DISPATCH_ANCHOR = '        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))\n'
DISPATCH = '        options.extend(public_subgroup_lift(goal))\n'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8').strip()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def unique_function(nodes, name):
    matches = [node for node in nodes if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise ValueError('FUNCTION_NOT_UNIQUE:' + name)
    return matches[0]


def updated_source(source):
    if '\r' in source or source.startswith('\ufeff'):
        raise ValueError('EXPECTED_LF_SOURCE')
    tree = ast.parse(source)
    fn = unique_function(tree.body, 'shared_expansion_provider')
    expand = unique_function(fn.body, 'expand')
    lines = source.splitlines(keepends=True)
    setup_body = ''.join(lines[fn.lineno-1:expand.lineno-1])
    dispatch_body = ''.join(lines[expand.lineno-1:expand.end_lineno])
    if setup_body.count(SETUP_ANCHOR) != 1 or dispatch_body.count(DISPATCH_ANCHOR) != 1:
        raise ValueError('HOOK_ANCHOR_NOT_UNIQUE')
    if 'public_subgroup_lift' in source:
        if (source.count(SETUP) != 1 or source.count(DISPATCH) != 1
                or SETUP_ANCHOR+SETUP not in setup_body
                or DISPATCH_ANCHOR+DISPATCH not in dispatch_body
                or source.count('public_subgroup_lift') != (SETUP+DISPATCH).count('public_subgroup_lift')):
            raise ValueError('PARTIAL_OR_MOVED_PATCH')
        return source
    changed = source.replace(SETUP_ANCHOR, SETUP_ANCHOR+SETUP, 1).replace(DISPATCH_ANCHOR, DISPATCH_ANCHOR+DISPATCH, 1)
    if source.count(SETUP_ANCHOR) != 1 or source.count(DISPATCH_ANCHOR) != 1:
        raise ValueError('GLOBAL_HOOK_ANCHOR_NOT_UNIQUE')
    ast.parse(changed)
    return changed


def reviewed_source():
    if git('branch','--show-current') != 'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    if not ISOLATED.is_file() or hashlib.sha256(ISOLATED.read_bytes().replace(b'\r\n',b'\n')).hexdigest() != RULE_HASH:
        raise RuntimeError('R3R43R1_REVIEWED_RULE_MISSING_OR_CHANGED')
    original = TARGET.read_bytes().decode('utf-8')
    changed = updated_source(original)
    baseline = changed.replace(SETUP,'',1).replace(DISPATCH,'',1)
    if blob(baseline.encode('utf-8')) != BASE:
        raise RuntimeError('SHARED_BASELINE_CHANGED')
    # Permit only the exact pre/post patch shared file; never overwrite other edits.
    head_blob = git('rev-parse','HEAD:phase165_r52_r9_shared_math.py')
    if head_blob not in (BASE, blob(changed.encode('utf-8'))):
        raise RuntimeError('SHARED_HEAD_CHANGED')
    tracked = set(git('diff','--name-only','HEAD').splitlines())
    if tracked - {TARGET.name}:
        raise RuntimeError('UNRELATED_TRACKED_CHANGES:' + repr(sorted(tracked - {TARGET.name})))
    if git('diff','--cached','--name-only'):
        raise RuntimeError('STAGED_CHANGES_PRESENT')
    return original, changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    original, changed = reviewed_source()
    fn = unique_function(ast.parse(changed).body,'shared_expansion_provider')
    full = '\n'.join(changed.splitlines()[fn.lineno-1:fn.end_lineno])
    if not args.dry_run:
        if original != changed:
            TARGET.write_bytes(changed.encode('utf-8'))
        (Path(__file__).parent/'SHARED_FUNCTION_FULL_JA.md').write_bytes(('# 変更後の共有関数全文\n\n```python\n'+full+'\n```\n').encode('utf-8'))
    print('PHASE176_R3R44_HEAD='+git('rev-parse','HEAD'))
    print('PHASE176_R3R44_PATCH='+('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

```

## audit.py

```python
"""Observe actual Web calls and independently probe every proposed premise."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import RULE_NAME
from phase176_r3r44_public_subgroup_lift.apply import reviewed_source
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def observe():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from web_group_proof import build_standard_web_group_proof_view

    real_entry = entry.search_group_from_registered_goal
    real_adapter = shared.search_registered_partial_proof
    calls, invocations, results = [], [], []

    def observed_entry(*args, **kwargs):
        result = real_entry(*args, **kwargs)
        results.append(result)
        return result

    def observed_adapter(*args, **kwargs):
        if (kwargs.get('n'), kwargs.get('k')) != (3,5):
            return real_adapter(*args, **kwargs)
        invocations.append(dict(kwargs))
        forwarded = dict(kwargs)
        provider = kwargs['expansion_provider']

        def observed_provider(goal):
            options = provider(goal)
            calls.append((goal, options))
            return options

        forwarded['expansion_provider'] = observed_provider
        return real_adapter(*args, **forwarded)

    with patch.object(entry,'search_group_from_registered_goal',new=observed_entry), \
         patch.object(shared,'search_registered_partial_proof',new=observed_adapter):
        view = build_standard_web_group_proof_view(n=3,k=5,max_depth=2,mode='narrative')
    if len(invocations) != 1 or len(results) != 1:
        raise RuntimeError('UNEXPECTED_WEB_ENTRY_COUNT')
    invocation, result = invocations[0], results[0]
    root, context = invocation['goal'], invocation['bridge']
    cyclic = CyclicStructureStatement(root.lhs, root.rhs.generator, root.rhs.order)
    available = tuple(link.step.conclusion for link in context.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN
                      and context.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
                      and context.registry.assertion(link.assertion_id).content == link.step.conclusion)
    if root in available or cyclic in available:
        raise RuntimeError('TARGET_PRESENT_AS_GIVEN')
    candidates = []
    for requested, options in calls:
        if requested != cyclic:
            continue
        for option in options:
            if option.rule.name == RULE_NAME and not any(old.subgoals == option.subgoals for old in candidates):
                candidates.append(option)
    if not candidates or any(len(option.subgoals) != 5 for option in candidates):
        raise RuntimeError('ACTUAL_WEB_SUBGROUP_LIFT_CANDIDATE_MISSING')
    steps = tuple(result.proven_steps)
    prior = tuple(item.root.conclusion for item in invocation.get('completed_internal_proofs', ()))
    candidate_reports = []
    for option in candidates:
        premises = []
        for child in option.subgoals:
            provider = shared.shared_expansion_provider(context, proof_target=root, prior_conclusions=prior)
            probe = provider(child)
            actual = [options for requested, options in calls if requested == child]
            accepted = [step for step in steps if step.conclusion == child]
            premises.append({'goal':repr(child), 'actual_calls':len(actual),
                             'actual_candidate_counts':[len(x) for x in actual],
                             'accepted_steps':len(accepted),
                             'independent_candidate_count':len(probe),
                             'independent_rules':[p.rule.name for p in probe],
                             'screened_given':child in available})
        candidate_reports.append({'rule':option.rule.name,'premises':premises})
    return {'gate':'PASS_R3R44_PUBLIC_WEB_CANDIDATE_CONNECTED',
            'status':result.status.value,'web_key':view.key,
            'web_step_count':len(view.steps),'root_group_proved':result.status.value=='complete',
            'accepted_step_count':len(steps),'accepted_lift_steps':sum(s.inference_rule is not None and s.inference_rule.name==RULE_NAME for s in steps),
            'cyclic_candidate_count':len(candidates),'candidates':candidate_reports,
            'open_goals':[repr(g) for g in result.open_goals],
            'diagnostics':[str(x) for x in result.diagnostics],
            'new_given':0,'new_math_rules':0,'full_pytest':'NOT_RUN'}


def main():
    original, changed = reviewed_source()
    if original != changed:
        raise RuntimeError('PUBLIC_PATCH_NOT_APPLIED')
    report = observe()
    if reviewed_source() != (original,changed):
        raise RuntimeError('SHARED_SOURCE_CHANGED_DURING_AUDIT')
    destination = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r44_public_subgroup_lift' / 'report.json'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for key,value in report.items():
        if key not in ('candidates','open_goals','diagnostics'):
            print('PHASE176_R3R44_'+key.upper()+'='+str(value))
    for idx,candidate in enumerate(report['candidates'],1):
        for j,premise in enumerate(candidate['premises'],1):
            print(f'PHASE176_R3R44_CANDIDATE_{idx}_PREMISE_{j}='+json.dumps(premise,ensure_ascii=False))
    for goal in report['open_goals']:
        print('PHASE176_R3R44_OPEN_GOAL='+goal)
    print('REPORT='+str(destination))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $parameters = @()
    if ($DryRun) { $parameters += '--dry-run' }
    & python -B -m phase176_r3r44_public_subgroup_lift.apply @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R44 patch guard failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R44_GATE=PASS_R3R44_DRYRUN'
    } else {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r44_public_subgroup_lift\tests\test_public_subgroup_lift.py `
            .\phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated\tests\test_finite_cyclic_subgroup_lift.py `
            .\phase176_r3r41_public_quadruple_connection\tests\test_public_connection.py `
            .\phase176_r3r42_root_backward_frontier_audit\tests\test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R44 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R44 git diff check failed' }
        & python -B -m phase176_r3r44_public_subgroup_lift.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R44 real Web audit failed' }
        Write-Host 'PHASE176_R3R44_GATE=PASS_R3R44_PUBLIC_CONNECTION_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R44_NEW_MATH_RULES=0'
        Write-Host 'PHASE176_R3R44_NEW_GIVEN=0'
        Write-Host 'PHASE176_R3R44_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally {
    Pop-Location
}

```

## tests/test_public_subgroup_lift.py

```python
"""Candidate wiring, no proof fabrication; actual Web integration is audited separately."""
from dataclasses import replace

import pytest

from expression import Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import RULE_NAME
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.tests.test_finite_cyclic_subgroup_lift import fixture
from phase176_r3r44_public_subgroup_lift import provider
from phase176_r3r44_public_subgroup_lift.apply import TARGET, SETUP, DISPATCH, updated_source
from proof import ProofStep, find_inference_matches_for_rule


def test_source_candidate_keeps_five_obligations(monkeypatch):
    goal, exact, group, kernel, image = fixture()
    monkeypatch.setattr(provider,'database_structured_group_goal_candidates',lambda **kwargs: ())
    options = provider.build_public_subgroup_lift_provider((group,))(goal)
    assert len(options)==1
    option=options[0]
    assert option.rule.name==RULE_NAME
    assert option.subgoals[1:]==(exact,group,kernel,image)
    assert len(option.subgoals)==5
    assert not any(isinstance(x,ProofStep) for x in option.subgoals)
    assert not find_inference_matches_for_rule(option.rule,())


def test_db_candidate_is_open_and_deduplicated(monkeypatch):
    goal, exact, group, kernel, image = fixture()
    seen=[]
    def db(**kwargs):
        seen.append(kwargs)
        return (group,group)
    monkeypatch.setattr(provider,'database_structured_group_goal_candidates',db)
    options=provider.build_public_subgroup_lift_provider((),(group,))(goal)
    assert seen==[{'n':5,'k':3}]
    assert len(options)==1
    assert options[0].subgoals[1:]==(exact,group,kernel,image)
    assert not find_inference_matches_for_rule(options[0].rule,())
    assert len(provider.build_public_subgroup_lift_provider(())(goal))==1


@pytest.mark.parametrize('n,i,m,q',[(4,10,16,4),(5,12,32,8)])
def test_no_target_specific_dimensions(monkeypatch,n,i,m,q):
    goal, exact, group, kernel, image=fixture(n,i,m,q)
    monkeypatch.setattr(provider,'database_structured_group_goal_candidates',lambda **kwargs:(group,))
    option,=provider.build_public_subgroup_lift_provider(())(goal)
    assert option.subgoals[1:]==(exact,group,kernel,image)


def test_wrong_group_or_order_is_not_a_candidate(monkeypatch):
    goal, _, group, _, _=fixture()
    wrong=(replace(group,lhs=TodaPrimaryGroup(9,5)),
           replace(group,rhs=FiniteCyclicGroup(3,group.rhs.generator)),
           replace(group,rhs=FiniteCyclicGroup(2,group.rhs.generator)))
    monkeypatch.setattr(provider,'database_structured_group_goal_candidates',lambda **kwargs:wrong)
    expand=provider.build_public_subgroup_lift_provider(wrong)
    assert expand(goal)==()
    assert expand(group)==()


def test_actual_db_root_candidate_requires_same_typed_goal():
    root,=database_structured_group_goal_candidates(n=3,k=5)
    goal=CyclicStructureStatement(root.lhs,root.rhs.generator,root.rhs.order)
    options=provider.build_public_subgroup_lift_provider(())(goal)
    assert options
    for option in options:
        assert option.rule.name==RULE_NAME and len(option.subgoals)==5
        assert option.subgoals[2].lhs==TodaPrimaryGroup(8,5)
        assert option.subgoals[3].multiple==4
        assert option.subgoals[4].lhs.expression==goal.generator
        assert option.subgoals[4].rhs==Multiple(4,option.subgoals[2].rhs.generator)
        assert not find_inference_matches_for_rule(option.rule,())


def test_patch_minimal_and_idempotent():
    source=TARGET.read_bytes().decode('utf-8')
    assert updated_source(source)==source
    assert source.count(SETUP)==source.count(DISPATCH)==1
    baseline=source.replace(SETUP,'',1).replace(DISPATCH,'',1)
    assert updated_source(baseline)==source
    with pytest.raises(ValueError):
        updated_source(source.replace(DISPATCH,'',1))
    with pytest.raises(ValueError):
        updated_source(source.replace('\n','\r\n'))

```

