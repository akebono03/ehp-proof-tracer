# Phase 176 R3R5 — 変更対象・追加コード全文

変更対象は新規 `phase176_r3r5_lemma57_right_composition_frontier/` のみ。既存ファイル・クラス・関数・import の変更はない。以下は新規ファイル全文である。

## audit.py

```python
"""Phase 176 R3R5: read-only typed Lemma 5.7 right-composition frontier.

Do not create a proof, assert a new GIVEN, or change production source.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'phase176_r3r5_lemma57_right_composition_frontier'
REVIEWED_HEAD = '62e5153cddb1afb4508e900052ebde4913b35190'
MARKER = 'PHASE176_R3R5_WORKER_JSON='
SOURCE_PATHS = (
    'phase176_r3r4_zero_image_and_hopf_lift_frontier/audit.py',
    'phase175_r3r9_lemma57_explicit_public/rule.py',
    'phase175_r3r9_lemma57_explicit_public/source.py',
    'phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py',
    'phase174_r3_r7_r5_zero_image_hopf_injective/rule.py',
    'phase165_r52_r9_shared_math.py',
    'phase165_r55_nk_only_goal.py',
    'relation_rules.py',
    'sources/toda/Toda_05_2.tex',
)
ANCHORS = {
    'relation_rules.py': (
        'def equality_preserved_under_right_composition_inference_rule(',
        'def suspension_composition_functoriality_inference_rule(',
        'def zero_composition_equality_implies_zero_inference_rule(',
    ),
    'phase175_r3r9_lemma57_explicit_public/rule.py': (
        'def exact_lemma57_zero_image_goal(',
        'def expand_cited_lemma57_explicit_zero(',
    ),
    'sources/toda/Toda_05_2.tex': (r'\label{lemma:5.7}', r"E(\eta_2\circ\nu')=0"),
}


def git(*arguments: str) -> str:
    p = subprocess.run(('git',) + arguments, cwd=ROOT, capture_output=True,
                       text=True, encoding='utf-8', errors='replace', check=False)
    if p.returncode:
        raise RuntimeError('GIT_FAILED: ' + ' '.join(arguments) + ': ' + p.stderr.strip())
    return p.stdout.strip()


def verify_source_contract(root: Path = ROOT) -> dict[str, str]:
    hashes = {}
    for name in SOURCE_PATHS:
        path = root / name
        if not path.is_file():
            raise RuntimeError('SOURCE_MISSING: ' + name)
        content = path.read_text(encoding='utf-8-sig')
        normalized = ''.join(content.split())
        missing = [s for s in ANCHORS.get(name, ()) if ''.join(s.split()) not in normalized]
        if missing:
            raise RuntimeError('SOURCE_ANCHOR_MISSING: ' + name + ': ' + repr(missing))
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def preflight() -> dict[str, object]:
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT.resolve():
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    if subprocess.run(('git', 'merge-base', '--is-ancestor', REVIEWED_HEAD, 'HEAD'),
                      cwd=ROOT, capture_output=True, check=False).returncode:
        raise RuntimeError('R3R4_REVIEWED_HEAD_NOT_ANCESTOR')
    if git('status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('TRACKED_WORKTREE_DIRTY')
    hashes = verify_source_contract()
    return {'head': git('rev-parse', 'HEAD'), 'source_hashes': hashes,
            'historical_source_guards': 'FOUR_KNOWN_FAILURES_NOT_PASSING',
            'full_pytest': 'NOT_RUN'}


def detail(value: object) -> dict[str, str]:
    return {'type': type(value).__module__ + '.' + type(value).__name__,
            'repr': repr(value)[:2200]}


def analyze_generator_factors(factors: tuple[object, ...]) -> dict[str, object]:
    """Assess structure without claiming any equality or element identity."""
    return {'factor_count': len(factors),
            'factors': [detail(x) for x in factors],
            'can_form_two_factor_lemma57_prefix': len(factors) >= 3,
            'right_factor_count': max(0, len(factors) - 2)}


def summarize_options(options: tuple[object, ...]) -> dict[str, object]:
    return {'count': len(options), 'status': 'UNVERIFIED_PROPOSALS',
            'options': [{'rule': getattr(item.rule, 'name', None),
                         'subgoals': [detail(x) for x in item.subgoals]}
                        for item in options[:10]]}


def observe() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import expand_zero_image_from_cyclic_generator
    from phase175_r3r9_lemma57_explicit_public.rule import (
        exact_lemma57_zero_image_goal, expand_cited_lemma57_explicit_zero,
    )
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
    from proof import Relation, RelationType

    result = search_group_from_registered_goal(n=3, k=5)
    prior = exact_prior_database_result(2, 5)
    if (not isinstance(prior, Relation) or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != TodaPrimaryGroup(7, 2)):
        raise RuntimeError('PRECEDING_CYCLIC_PRESENTATION_CHANGED')
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None:
        raise RuntimeError('PRIOR_GENERATOR_IS_NOT_TYPED_COMPOSITION')
    report: dict[str, object] = {
        'target': [3, 5], 'search_status': result.status.value,
        'open_goals': len(result.open_goals),
        'prior_group_presentation_is_candidate_only': detail(prior),
        'generator_structure': analyze_generator_factors(factors),
        'proof_complete': False, 'new_given': 0, 'new_rules': 0,
    }
    bridge = build_shared_typed_bridge()
    available = tuple(link.step.conclusion for link in bridge.proof_links
                      if link.step is not None and link.step.conclusion is not None)
    report['explicit_lemma57_in_default_shared_bridge'] = sum(
        type(x) is TodaLemma57ExplicitNuPrimeZero for x in available
    )
    mapped = TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3))
    from map_property_rules import ImageZeroStatement
    zero_image = ImageZeroStatement(mapped)
    report['isolated_zero_image_candidates'] = summarize_options(
        expand_zero_image_from_cyclic_generator(zero_image, prior)
    )
    if len(factors) >= 3:
        base = Composition(factors[0], factors[1])
        suffix = factors[2:]
        base_map = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
        direct_goal = GeneratorImage(base_map, base, Zero())
        report['lemma57_base_zero_goal'] = detail(direct_goal)
        report['lemma57_base_match'] = exact_lemma57_zero_image_goal(direct_goal)
        report['lemma57_base_source_proposal_with_explicit_leaf'] = summarize_options(
            expand_cited_lemma57_explicit_zero(direct_goal, (TodaLemma57ExplicitNuPrimeZero(),))
        )
        report['lemma57_base_source_proposal_default_shared'] = summarize_options(
            expand_cited_lemma57_explicit_zero(direct_goal, available)
        )
        report['right_composition_suffix'] = [detail(x) for x in suffix]
        report['lemma57_composite_direct_match'] = exact_lemma57_zero_image_goal(
            GeneratorImage(mapped, prior.rhs.generator, Zero())
        )
        ordinary = shared_expansion_provider(bridge, proof_target=result.open_goals[-1])
        report['shared_base_zero_proposals'] = summarize_options(tuple(ordinary(direct_goal)))
        composite_goal = GeneratorImage(mapped, prior.rhs.generator, Zero())
        report['shared_composite_zero_proposals'] = summarize_options(tuple(ordinary(composite_goal)))
        report['shared_whole_zero_image_proposals'] = summarize_options(tuple(ordinary(zero_image)))
    else:
        report['lemma57_base_match'] = False
        report['explanation'] = 'PRIOR_GENERATOR_NEEDS_MORE_THAN_TWO_FACTORS_FOR_RIGHT_COMPOSITION'
    report['math_contract'] = (
        'A proof of E(a)=0 may be right-composed with E(b), but the composed generator'
        ' requires exact typed suspension functoriality, zero-composition reduction,'
        ' and a verified source-first proof of the prior cyclic presentation.'
    )
    return report


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    try:
        p = subprocess.run((sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker'),
                           cwd=ROOT, env=env, capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('WORKER_TIMEOUT') from exc
    lines = [line[len(MARKER):] for line in p.stdout.splitlines() if line.startswith(MARKER)]
    if p.returncode or len(lines) != 1:
        raise RuntimeError('WORKER_FAILED: ' + p.stderr[-4500:])
    value = json.loads(lines[0])
    if value.get('new_given') != 0 or value.get('proof_complete') is not False:
        raise RuntimeError('AUDIT_MAY_NOT_CERTIFY_MATHEMATICS')
    return value


def report_path() -> Path:
    directory = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    directory.mkdir(parents=True, exist_ok=True)
    return directory / 'report.json'


def execute(dry_run: bool, timeout: int) -> int:
    report: dict[str, object] = {
        'phase': '176_R3R5', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'dry_run': dry_run, 'gate': 'FAIL_R3R5', 'full_pytest': 'NOT_RUN',
        'new_given': 0, 'new_rules': 0, 'proof_complete': False,
    }
    try:
        report['preflight'] = preflight()
        if not dry_run:
            report['observed'] = worker(timeout)
        report['gate'] = ('PASS_R3R5_READ_ONLY_DRYRUN' if dry_run
                          else 'PASS_R3R5_LEMMA57_COMPOSITION_FRONTIER')
    except Exception as exc:
        report['error'] = type(exc).__name__ + ': ' + str(exc)
        report['traceback'] = traceback.format_exc()[-8500:]
    path = report_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE176_R3R5_GATE=' + str(report['gate']))
    print('PHASE176_R3R5_REPORT=' + str(path))
    print('PHASE176_R3R5_HEAD=' + str(report.get('preflight', {}).get('head', 'UNVERIFIED')))
    if 'observed' in report:
        value = report['observed']
        print('PHASE176_R3R5_GROUP=(3,5) STATUS=' + value['search_status'] + ' OPEN=' + str(value['open_goals']))
        print('PHASE176_R3R5_GENERATOR_FACTORS=' + str(value['generator_structure']['factor_count']))
        print('PHASE176_R3R5_LEMMA57_BASE_MATCH=' + str(value['lemma57_base_match']).lower())
        print('PHASE176_R3R5_DEFAULT_LEMMA57_SOURCE=' + str(value['explicit_lemma57_in_default_shared_bridge']))
        for key in ('shared_base_zero_proposals', 'shared_composite_zero_proposals', 'shared_whole_zero_image_proposals'):
            if key in value:
                print('PHASE176_R3R5_' + key.upper() + '=' + str(value[key]['count']))
    if 'error' in report:
        print('PHASE176_R3R5_ERROR=' + report['error'])
    print('PHASE176_R3R5_FULL_PYTEST=NOT_RUN')
    print('(END)')
    return 0 if report['gate'].startswith('PASS_') else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--timeout', type=int, default=120)
    a = parser.parse_args()
    if a.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return execute(a.dry_run, a.timeout)


if __name__ == '__main__':
    raise SystemExit(main())

```

## run.ps1

```powershell
param([switch]$DryRun, [int]$TimeoutSeconds = 120)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r5_lemma57_right_composition_frontier.audit --dry-run --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R5 DryRun failed' }
    } else {
        & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r3r5_lemma57_right_composition_frontier/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R5 focused tests failed' }
        & python -B -m phase176_r3r5_lemma57_right_composition_frontier.audit --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R5 audit failed' }
    }
} finally { Pop-Location }

```

## tests/test_audit.py

```python
"""Focused R3R5 audit contracts, no mathematical proof certification."""
from __future__ import annotations

import json
import pytest

from phase176_r3r5_lemma57_right_composition_frontier import audit


def test_source_contract_fixture(tmp_path):
    for name in audit.SOURCE_PATHS:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(audit.ANCHORS.get(name, ())), encoding='utf-8')
    assert len(audit.verify_source_contract(tmp_path)) == len(audit.SOURCE_PATHS)


def test_missing_source_anchor_refused(tmp_path):
    for name in audit.SOURCE_PATHS:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('unrelated text', encoding='utf-8')
    with pytest.raises(RuntimeError, match='SOURCE_ANCHOR_MISSING'):
        audit.verify_source_contract(tmp_path)


def test_nu_prime_apostrophe_not_escaped():
    values = audit.ANCHORS['sources/toda/Toda_05_2.tex']
    assert r"E(\eta_2\circ\nu')=0" in values
    assert all(r"\nu\'" not in s for s in values)


def test_factor_analysis_does_not_claim_proof():
    row = audit.analyze_generator_factors(('eta2', 'nu_prime', 'eta6'))
    assert row['factor_count'] == 3
    assert row['right_factor_count'] == 1
    assert row['can_form_two_factor_lemma57_prefix'] is True
    assert 'proved' not in row


def test_options_not_proof():
    class Rule:
        name = 'hypothetical'
    class Option:
        rule = Rule()
        subgoals = ('unproved',)
    value = audit.summarize_options((Option(),))
    assert value['status'] == 'UNVERIFIED_PROPOSALS'
    assert value['count'] == 1


def test_dryrun_no_worker(monkeypatch, tmp_path):
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'fixture'})
    monkeypatch.setattr(audit, 'worker', lambda timeout: pytest.fail('Worker invoked'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    assert audit.execute(True, 120) == 0
    report = json.loads((tmp_path / 'EHPProofTracerAudit' / audit.PACKAGE / 'report.json').read_text(encoding='utf-8'))
    assert report['proof_complete'] is False
    assert report['new_given'] == 0
    assert report['full_pytest'] == 'NOT_RUN'

```

## __init__.py

```python

```

## tests/__init__.py

```python

```

