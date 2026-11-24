# R3R47 全コード

# 既存関数の変更後全文

`toda_conclusion_latex_renderer.py` の `render_repository_conclusion_latex()` を置換する。モジュール先頭の import は変更しない。

```python
def render_repository_conclusion_latex(conclusion) -> str:
    """Render established Relation, membership and Expression forms unchanged."""
    # Render subgroup generation, not an assertion of infinite cyclic order.
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase168_r3_27_typed_statement_projection import (
        element_tex, group_tex, map_symbol_tex,
    )
    if type(conclusion) is KernelMultipleStatement:
        mapping = conclusion.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        generator = element_tex(conclusion.source_generator)
        if (source is not None and target is not None and symbol is not None
                and generator is not None and type(conclusion.multiple) is int
                and conclusion.multiple >= 1
                and conclusion.domain == mapping.source_group):
            return (rf"\ker({symbol}:{source}\to {target})="
                    rf"\langle {conclusion.multiple}{generator}\rangle")
        raise TypeError("unsupported typed kernel multiple for LaTeX rendering")
    if isinstance(conclusion, Relation):
        if conclusion.relation_type is not RelationType.EQUALITY:
            raise ValueError(
                "only equality Relation conclusions are supported in Phase 99-18"
            )
        return (
            _render_repository_conclusion_value_latex(conclusion.lhs)
            + " = "
            + _render_repository_conclusion_value_latex(conclusion.rhs)
        )
    if isinstance(
        conclusion,
        (TodaBracketMembershipStatement, TodaBracketMembershipTheoremStatement),
    ):
        return (
            render_toda_expression_latex(conclusion.element)
            + r" \in "
            + render_toda_expression_latex(conclusion.bracket)
        )
    if isinstance(conclusion, Expression):
        return render_toda_expression_latex(conclusion)
    raise TypeError("unsupported repository conclusion for LaTeX rendering")
```

## `__init__.py`

```python
"""Phase 176 R3R47: finite cyclic kernel frontier and display audit."""

```

## `apply.py`

```python
"""Pin and extend the common conclusion renderer, not mathematical inference."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / 'toda_conclusion_latex_renderer.py'
PINS = {
    'toda_conclusion_latex_renderer.py': '8f8b30043fab1cdc207d5d9afbbe332290620ccf',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py': 'fac88c852cd4c18e8d013e3dc12ab95ad57d7b03',
    'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/rule.py': 'adc68818539ddb5975d86b8ce4517107cfb9db78',
    'phase176_r3r44_public_subgroup_lift/provider.py': '551e9105cd35c8df9159cf8027839e7a890d0d81',
}
ANCHOR = '''    """Render established Relation, membership and Expression forms unchanged."""
'''
INSERT = '''    # Render subgroup generation, not an assertion of infinite cyclic order.
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase168_r3_27_typed_statement_projection import (
        element_tex, group_tex, map_symbol_tex,
    )
    if type(conclusion) is KernelMultipleStatement:
        mapping = conclusion.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        generator = element_tex(conclusion.source_generator)
        if (source is not None and target is not None and symbol is not None
                and generator is not None and type(conclusion.multiple) is int
                and conclusion.multiple >= 1
                and conclusion.domain == mapping.source_group):
            return (rf"\\ker({symbol}:{source}\\to {target})="
                    rf"\\langle {conclusion.multiple}{generator}\\rangle")
        raise TypeError("unsupported typed kernel multiple for LaTeX rendering")
'''


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def normalize(raw):
    lf = raw.replace(b'\r\n', b'\n')
    if b'\r' in lf or (b'\r\n' in raw and raw != lf.replace(b'\n', b'\r\n')):
        raise ValueError('MIXED_LINE_ENDINGS')
    return lf.decode('utf-8'), '\r\n' if b'\r\n' in raw else '\n'


def pinned(text, expected):
    return expected in (blob(text.encode('utf-8')), blob(text.replace('\n', '\r\n').encode('utf-8')))


def updated_source(raw):
    source, eol = normalize(raw)
    baseline = source.replace(ANCHOR + INSERT, ANCHOR, 1)
    if not pinned(baseline, PINS['toda_conclusion_latex_renderer.py']):
        raise ValueError('UNREVIEWED_RENDERER_BASELINE')
    if baseline.count(ANCHOR) != 1:
        raise ValueError('RENDERER_ANCHOR_NOT_UNIQUE')
    changed = baseline.replace(ANCHOR, ANCHOR + INSERT, 1)
    if source not in (baseline, changed):
        raise ValueError('PARTIAL_OR_MOVED_PATCH')
    ast.parse(changed)
    return changed.replace('\n', eol).encode('utf-8')


def preflight():
    if subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip() != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    for path, sha in PINS.items():
        if ROOT / path == TARGET:
            continue
        source, _ = normalize((ROOT / path).read_bytes())
        if not pinned(source, sha):
            raise RuntimeError('UNREVIEWED_DEPENDENCY:' + path)
    # R46R1 must already be installed; no clean-tree requirement for its local edits.
    from phase176_r3r46r1_prior_group_availability.apply import planned_changes
    if any(old != new for old, new in planned_changes().values()):
        raise RuntimeError('R3R46R1_NOT_APPLIED')
    old = TARGET.read_bytes()
    return old, updated_source(old)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    old, new = preflight()
    if not args.dry_run:
        if old != new:
            TARGET.write_bytes(new)
        source, _ = normalize(new)
        tree = ast.parse(source)
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == 'render_repository_conclusion_latex')
        function = '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno])
        (PACKAGE / 'SHARED_FUNCTION_FULL_JA.md').write_text(
            '# 変更後の共通表示関数全文\n\n```python\n' + function + '\n```\n', encoding='utf-8')
    print('PHASE176_R3R47_PATCH=' + ('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

```

## `audit.py`

```python
"""Observe the real Web frontier; independent probes are not accepted proofs."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import conditional_inputs, expand_cyclic_delta_kernel
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import RULE_NAME as LIFT_RULE
from phase176_r3r47_finite_cyclic_kernel_frontier.apply import ROOT, TARGET, preflight
from proof import ProofRule, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import AssertionOrigin


def options_record(options):
    return [{'rule': item.rule.name, 'premises': [repr(g) for g in item.subgoals],
             'premise_proof_rules': [getattr(p.proof_rule, 'value', None)
                                     for p in item.rule.premise_patterns]} for item in options]


def signed_source_records(bridge, goal):
    """Distinguish actual linked signed facts, wrappers, and untyped metadata."""
    result = []
    for assertion in bridge.registry._assertions.values():
        reference = bridge.registry.reference(assertion.reference_id)
        content = assertion.content
        signed = content if type(content) is TodaDeltaImageUpToSignStatement else getattr(content, 'statement', None)
        matching_map = type(signed) is TodaDeltaImageUpToSignStatement and signed.map == goal.map
        if reference.locator != 'Lemma 5.7' and not matching_map:
            continue
        links = [link.step for link in bridge.proof_links if link.assertion_id == assertion.assertion_id
                 and link.step is not None]
        fixed = assertion.origin is AssertionOrigin.FIXED_STATEMENT
        eligible = [s for s in links if s.rule is ProofRule.GIVEN and not s.premises
                    and type(s.conclusion) is type(content) and s.conclusion == content and fixed]
        result.append({'id': assertion.assertion_id, 'locator': reference.locator,
                       'publication_position': reference.publication_position,
                       'type': type(content).__name__, 'content': repr(content),
                       'linked_given_count': len(eligible), 'exact_signed_goal': content == goal,
                       'wrapped_exact_signed_goal': type(content) is not TodaDeltaImageUpToSignStatement and signed == goal,
                       'signed_map_matches': matching_map})
    return result


def observe():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from web_group_proof import build_standard_web_group_proof_view
    from web_group_proof_common import _group_proof_statement_latex
    from phase165_r14_r6_generic_iso import MapInjective
    from homotopy_groups import TodaHopfInvariantMap

    calls, invocations, results = [], [], []
    original_entry = entry.search_group_from_registered_goal
    original_adapter = shared.search_registered_partial_proof

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

    with patch.object(entry, 'search_group_from_registered_goal', new=observed_entry), \
         patch.object(shared, 'search_registered_partial_proof', new=observed_adapter):
        view = build_standard_web_group_proof_view(n=3, k=5, max_depth=2, mode='narrative')
    if len(invocations) != 1 or len(results) != 1:
        raise RuntimeError('UNEXPECTED_WEB_ENTRY_COUNT')
    context, root = invocations[0]['bridge'], invocations[0]['goal']
    result = results[0]
    delta = TodaDeltaMap(TodaPrimaryGroup(8, 5), TodaPrimaryGroup(6, 2))
    source = admitted_prior_group_step(delta.source_group, proof_target=root, bridge=context)
    target = admitted_prior_group_step(delta.target_group, proof_target=root, bridge=context)
    for step, group in ((source, delta.source_group), (target, delta.target_group)):
        if (step is None or not verified_db_step(step, proof_target=root, bridge=context)
                or type(step.conclusion) is not Relation or step.conclusion.lhs != group
                or type(step.conclusion.rhs) is not FiniteCyclicGroup):
            raise RuntimeError('REQUIRED_FINITE_PRIOR_UNAVAILABLE:' + repr(group))
    a, b = source.conclusion, target.conclusion
    kernel = KernelMultipleStatement(delta, delta.source_group, a.rhs.generator, b.rhs.order)
    signed = TodaDeltaImageUpToSignStatement(delta, a.rhs.generator, b.rhs.generator)
    # This counterfactual free domain is a type probe only, not a mathematical premise.
    free = Relation(a.lhs, FreeCyclicGroup(a.rhs.generator), RelationType.EQUALITY)
    r35_finite = conditional_inputs(kernel, a, b, signed) is not None
    r35_free = conditional_inputs(kernel, free, b, signed) is not None
    r35_options = expand_cyclic_delta_kernel(kernel, (b, signed))
    provider = invocations[0]['expansion_provider']
    actual_calls = [options_record(options) for goal, options in calls if goal == kernel]
    source_records = signed_source_records(context, signed)
    exact_sources = [row for row in source_records if row['exact_signed_goal'] and row['linked_given_count']]
    accepted = lambda g: any(step.conclusion == g for step in result.proven_steps)
    injective = MapInjective(TodaHopfInvariantMap(TodaPrimaryGroup(8, 3), delta.source_group))
    if not accepted(injective) or not accepted(a):
        raise RuntimeError('R3R46R1_PROOF_REGRESSION')
    lifts = []
    for _, options in calls:
        for option in options:
            if option.rule.name != LIFT_RULE or kernel not in option.subgoals:
                continue
            record = options_record((option,))[0]
            if record not in lifts:
                lifts.append(record)
    if not lifts:
        raise RuntimeError('R3R44_LIFT_CANDIDATE_NOT_OBSERVED')
    latex, fallback = _group_proof_statement_latex(kernel)
    displayed = any(line.statement_latex == latex or any(seg.value == latex for seg in line.segments)
                    for line in view.rendered_lines) if latex is not None else False
    if (latex is None or fallback is not None or r'\langle' not in latex
            or (kernel in result.open_goals and not displayed)):
        raise RuntimeError('PUBLIC_KERNEL_DISPLAY_MISSING')
    if not actual_calls and not accepted(kernel):
        raise RuntimeError('KERNEL_FRONTIER_NOT_REACHED')
    if not r35_free or r35_finite:
        raise RuntimeError('REVIEWED_R35_TYPE_BOUNDARY_DRIFT')
    return {
        'gate': 'PASS_R3R47_FINITE_CYCLIC_KERNEL_FRONTIER',
        'status': result.status.value, 'web_key': view.key,
        'accepted_step_count': len(result.proven_steps),
        'open_goals': [repr(g) for g in result.open_goals],
        'domain_prior': repr(a), 'codomain_prior': repr(b),
        'domain_prior_accepted': accepted(a), 'codomain_prior_accepted': accepted(b),
        'domain_and_codomain_admission_verified': True,
        'kernel_goal': repr(kernel), 'kernel_proved': accepted(kernel),
        'kernel_actual_provider_calls': actual_calls,
        'kernel_independent_options': options_record(provider(kernel)),
        'signed_goal': repr(signed), 'signed_goal_accepted': accepted(signed),
        'signed_goal_independent_options': options_record(provider(signed)),
        'signed_exact_linked_given_count': len(exact_sources),
        'lemma57_and_matching_delta_source_records': source_records,
        'r35_accepts_finite_domain': r35_finite,
        'r35_accepts_counterfactual_free_domain': r35_free,
        'r35_counterfactual_options_not_proofs': options_record(r35_options),
        'lift_observed_premise_contracts': lifts,
        'lift_db_domain_rule': source.rule.value,
        'kernel_latex': latex, 'kernel_actual_web_display': displayed,
        'new_given_registrations': 0, 'new_math_rules': 0, 'full_pytest': 'NOT_RUN',
    }


def main():
    old, new = preflight()
    if old != new:
        raise RuntimeError('R3R47_DISPLAY_PATCH_NOT_APPLIED')
    report = observe()
    if TARGET.read_bytes() != old:
        raise RuntimeError('SOURCE_CHANGED_DURING_AUDIT')
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r47_finite_cyclic_kernel_frontier'
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / 'report.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for key, value in report.items():
        print('PHASE176_R3R47_' + key.upper() + '=' + json.dumps(value, ensure_ascii=False))
    print('REPORT=' + str(destination))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

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
    & python -B -m phase176_r3r47_finite_cyclic_kernel_frontier.apply @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R47 patch guard failed' }
    & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner --check-only
    if ($LASTEXITCODE -ne 0) { throw 'R3R47 canonical import guard failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R47_GATE=PASS_R3R47_DRYRUN'
    } else {
        $groups = @(
            'phase176_r3r47_finite_cyclic_kernel_frontier/tests/test_frontier.py',
            'phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py',
            'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/tests/test_finite_cyclic_subgroup_lift.py',
            'phase176_r3r44_public_subgroup_lift/tests/test_public_subgroup_lift.py',
            'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py',
            'phase176_r3r45_direct_premise_audit/tests/test_audit.py'
        )
        foreach ($group in $groups) {
            Write-Host ('PHASE176_R3R47_TEST_GROUP=' + $group)
            & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner $group
            if ($LASTEXITCODE -ne 0) { throw ('R3R47 focused pytest failed: ' + $group) }
        }
        & python -B -m phase176_r3r47_finite_cyclic_kernel_frontier.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R47 frontier audit failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R47 git diff check failed' }
        Write-Host 'PHASE176_R3R47_GATE=PASS_R3R47_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R47_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally { Pop-Location }

```

## `tests/test_frontier.py`

```python
"""Focused rendering and existing rule-boundary tests, not new mathematical proofs."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import conditional_inputs
from phase176_r3r47_finite_cyclic_kernel_frontier.apply import TARGET, updated_source
from proof import Relation, RelationType
from toda_conclusion_latex_renderer import render_repository_conclusion_latex
from toda_rules import TodaDeltaImageUpToSignStatement
from web_group_proof_common import _group_proof_statement_latex


def kernel_fixture(q, n, m):
    domain = TodaPrimaryGroup(q+2, 2*n+1)
    codomain = TodaPrimaryGroup(q, n)
    a = HomotopyElement('a', 2*n+1, q+2, 2*n+1, GeneratorSymbol('ν', 2*n+1))
    b = HomotopyElement('b', n, q, n, GeneratorSymbol('η', n))
    delta = TodaDeltaMap(domain, codomain)
    kernel = KernelMultipleStatement(delta, domain, a, m)
    dst = Relation(codomain, FiniteCyclicGroup(m,b), RelationType.EQUALITY)
    signed = TodaDeltaImageUpToSignStatement(delta, a,b)
    return kernel, dst, signed


@pytest.mark.parametrize('q,n,m', [(6,2,4),(9,5,2),(13,6,8)])
def test_kernel_display_is_generic_subgroup_not_free_cyclic_claim(q,n,m):
    kernel, _, _ = kernel_fixture(q,n,m)
    direct = render_repository_conclusion_latex(kernel)
    latex, fallback = _group_proof_statement_latex(kernel)
    assert fallback is None and latex == direct
    assert r'\ker(\Delta:' in latex
    assert rf'\pi_{{{q+2}}}^{{{2*n+1}}}' in latex
    assert rf'\pi_{{{q}}}^{{{n}}}' in latex
    assert rf'\langle {m}' in latex and r'\rangle' in latex
    assert r'\mathbb{Z}' not in latex


def test_wrong_domain_has_no_kernel_display():
    kernel, _, _ = kernel_fixture(6,2,4)
    wrong = replace(kernel, domain=TodaPrimaryGroup(7,5))
    with pytest.raises(TypeError, match='unsupported typed kernel'):
        render_repository_conclusion_latex(wrong)


def test_suspension_kernel_display_also_supported():
    domain = TodaPrimaryGroup(8,4)
    generator = HomotopyElement('a',4,8,4,GeneratorSymbol('ν',4))
    goal = KernelMultipleStatement(TodaSuspensionMap(domain,TodaPrimaryGroup(9,5)), domain,generator,2)
    latex, fallback = _group_proof_statement_latex(goal)
    assert fallback is None and r'\ker(E:' in latex
    assert r'\langle 2' in latex


@pytest.mark.parametrize('q,n,m',[(6,2,4),(9,5,2),(13,6,8)])
def test_r35_existing_free_domain_boundary(q,n,m):
    kernel, dst, signed = kernel_fixture(q,n,m)
    free = Relation(kernel.domain,FreeCyclicGroup(kernel.source_generator),RelationType.EQUALITY)
    finite = Relation(kernel.domain,FiniteCyclicGroup(2*m,kernel.source_generator),RelationType.EQUALITY)
    # For q=9,n=5 the free-domain fixture is the historical diagonal case.
    assert conditional_inputs(kernel,free,dst,signed) == (free,dst,signed)
    assert conditional_inputs(kernel,finite,dst,signed) is None


def test_renderer_patch_is_idempotent_and_fails_closed():
    current = TARGET.read_bytes()
    assert updated_source(current) == current
    with pytest.raises(ValueError,match='UNREVIEWED_RENDERER_BASELINE'):
        updated_source(current.replace(b'\r\n', b'\n') + b'\n# unreviewed\n')

```
