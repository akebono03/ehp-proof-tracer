# Phase 176 R3R9 — 追加コード全文

既存コードの変更はありません。追加位置はリポジトリ直下の `phase176_r3r9_right_composition_type_boundary/` です。新規クラスはありません。新規関数は `audit.py` の各関数と、`tests/test_audit.py` の各テスト関数です。import を含め、各ファイルの全文を記載します。

## `__init__.py`

```python

```

## `audit.py`

```python
"""R3R9: read-only audit of the typed right-composition boundary after Lemma 5.7."""
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
PACKAGE = 'phase176_r3r9_right_composition_type_boundary'
REVIEWED_HEAD = '0e37263340af732e95e1b573041bbf3c8ae11792'
MARKER = 'PHASE176_R3R9_WORKER_JSON='
SOURCES = {
    'phase176_r3r8_lemma57_provider_binding/audit.py': ('def source_bound_provider(', 'def observe('),
    'phase175_r3r9_lemma57_explicit_public/rule.py': ('def exact_lemma57_zero_image_goal(',),
    'phase174_r3_r7_r9_composition_associativity/rule.py': ('def typed_composition_factors(',),
    'phase174_r3_r7_r7_composite_zero_audit/rule.py': ('def composite_zero_generator_inputs(',),
    'phase169_r10e5_composite_generator_image/rule.py': ('def component_image_obligations(',),
    'phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py': ('def cyclic_generator_zero_image_inputs(',),
    'relation_rules.py': ('def equality_preserved_under_right_composition_inference_rule(',),
    'sources/toda/Toda_05_2.tex': (r'\label{lemma:5.7}', r"E(\eta_2\circ\nu')=0"),
}


def git(*args: str, check: bool = True) -> tuple[int, str]:
    result = subprocess.run(('git',) + args, cwd=ROOT, capture_output=True,
                            text=True, encoding='utf-8', errors='replace', check=False)
    if check and result.returncode:
        raise RuntimeError('GIT_FAILED: ' + ' '.join(args) + ': ' + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def check_sources(root: Path) -> dict[str, str]:
    hashes = {}
    for name, anchors in SOURCES.items():
        path = root / name
        if not path.is_file():
            raise RuntimeError('REQUIRED_FILE_MISSING: ' + name)
        content = ''.join(path.read_text(encoding='utf-8-sig').split())
        if any(''.join(anchor.split()) not in content for anchor in anchors):
            raise RuntimeError('SOURCE_ANCHOR_MISSING: ' + name)
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def preflight() -> dict[str, object]:
    if Path(git('rev-parse', '--show-toplevel')[1]).resolve() != ROOT.resolve():
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current')[1] != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    if git('merge-base', '--is-ancestor', REVIEWED_HEAD, 'HEAD', check=False)[0]:
        raise RuntimeError('REVIEWED_HEAD_NOT_ANCESTOR')
    if git('status', '--porcelain', '--untracked-files=no')[1]:
        raise RuntimeError('TRACKED_FILES_DIRTY')
    return {'head': git('rev-parse', 'HEAD')[1], 'source_sha256': check_sources(ROOT),
            'full_pytest': 'NOT_RUN', 'historical_source_guards': 'FOUR_KNOWN_FAILURES_NOT_PASSING'}


def summarize(options: object) -> dict[str, object]:
    rows = tuple(options)
    return {'count': len(rows), 'status': 'UNVERIFIED_PROPOSALS',
            'rules': [getattr(option.rule, 'name', 'UNKNOWN') for option in rows[:12]],
            'subgoal_counts': [len(option.subgoals) for option in rows[:12]]}


def observe() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        expression_endpoints, expand_generator_zero_from_composite,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase175_r3r6_lemma57_general.source import merge_isolated_cited_source
    from phase175_r3r9_lemma57_explicit_public.rule import (
        exact_lemma57_zero_image_goal, expand_cited_lemma57_explicit_zero,
    )
    from phase175_r3r9_lemma57_explicit_public.source import (
        TodaLemma57ExplicitNuPrimeZero, build_explicit_lemma57_source,
    )
    from phase176_r3r7_lemma57_derived_source_proof.audit import (
        derive_from_existing_source, selected_source_steps,
    )
    from phase176_r3r8_lemma57_provider_binding.audit import source_bound_provider
    from proof import ProofRule, Relation

    result = search_group_from_registered_goal(n=3, k=5)
    if result.status.value != 'search_failed' or len(result.open_goals) != 3:
        raise RuntimeError('PUBLIC_SEARCH_FRONTIER_DRIFT')
    target = next((g for g in result.open_goals if type(g) is Relation
                   and g.lhs == TodaPrimaryGroup(8, 3)), None)
    if target is None:
        raise RuntimeError('TARGET_GOAL_MISSING')
    prior = exact_prior_database_result(2, 5)
    if type(prior) is not Relation or prior.lhs != TodaPrimaryGroup(7, 2):
        raise RuntimeError('PRIOR_GOAL_DRIFT')
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError('PRIOR_GENERATOR_FACTORIZATION_DRIFT')
    first_two = Composition(factors[0], factors[1])
    source_map = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    whole_map = TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3))
    base_goal = GeneratorImage(source_map, first_two, Zero())
    whole_goal = GeneratorImage(whole_map, prior.rhs.generator, Zero())
    if not exact_lemma57_zero_image_goal(base_goal):
        raise RuntimeError('LEMMA57_BASE_MISMATCH')
    if expression_endpoints(prior.rhs.generator) != (7, 2):
        raise RuntimeError('COMPOSITE_TYPE_MISMATCH')

    augmented = merge_isolated_cited_source(build_shared_typed_bridge(), build_explicit_lemma57_source(ROOT))
    screened = screen_independent_sources_for_derived_goal(augmented, goal=target)
    sources = selected_source_steps(screened, TodaLemma57ExplicitNuPrimeZero)
    if len(sources) != 1:
        raise RuntimeError('LEMMA57_SOURCE_NOT_UNIQUE')
    ordinary = shared_expansion_provider(screened, proof_target=target)
    bound = source_bound_provider(
        ordinary, sources, TodaLemma57ExplicitNuPrimeZero, expand_cited_lemma57_explicit_zero,
    )
    cited = [x for x in bound(base_goal) if x.rule.name ==
             'extract explicit nu-prime zero-suspension clause of Toda Lemma 5.7']
    if len(cited) != 1:
        raise RuntimeError('LEMMA57_PROPOSAL_DRIFT')
    base_step = derive_from_existing_source(cited[0], sources[0])
    if base_step.rule is not ProofRule.INFERENCE or base_step.conclusion != base_goal:
        raise RuntimeError('LEMMA57_PROOF_STEP_DRIFT')

    # Existing generic factorizations must not be mistaken for a zero-image proof.
    # The endpoint audit records whether the zero target can enter either rule.
    composite_zero_direct = expand_generator_zero_from_composite(whole_goal, base_goal)
    composite_image_direct = expand_composite_generator_image(whole_goal)
    ordinary_whole = summarize(ordinary(whole_goal))
    bound_whole = summarize(bound(whole_goal))
    if bound_whole != ordinary_whole:
        raise RuntimeError('UNRELATED_WHOLE_PROVIDER_MUTATED')
    return {
        'search_status': result.status.value,
        'open_goals': len(result.open_goals),
        'source_count': len(sources),
        'base_step_inferred': True,
        'base_zero_goal': repr(base_goal),
        'full_zero_goal': repr(whole_goal),
        'base_source_endpoints': expression_endpoints(first_two),
        'full_source_endpoints': expression_endpoints(prior.rhs.generator),
        'trailing_factor_endpoints': expression_endpoints(factors[2]),
        'composition_image_inputs_for_zero_target': component_image_obligations(whole_goal) is not None,
        'generic_composite_image_proposals_for_zero_target': summarize(composite_image_direct),
        'generic_composite_zero_proposals_from_base_zero_goal': summarize(composite_zero_direct),
        'public_whole_zero_proposals': ordinary_whole,
        'isolated_source_whole_zero_proposals': bound_whole,
        'typed_base_to_full_zero_rule_proved': False,
        'new_given': 0, 'new_mathematical_rules': 0,
        'production_modified': False, 'root_proof_complete': False,
        'blocker': 'GENERATOR_IMAGE_BASE_ZERO_TO_RIGHT_COMPOSITION_ZERO_TRANSPORT_NOT_CERTIFIED',
    }


def worker(timeout: int) -> dict[str, object]:
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    try:
        process = subprocess.run((sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker'),
                                 cwd=ROOT, env=environment, capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('WORKER_TIMEOUT') from exc
    lines = [line[len(MARKER):] for line in process.stdout.splitlines() if line.startswith(MARKER)]
    if process.returncode or len(lines) != 1:
        raise RuntimeError('WORKER_FAILED: ' + str(process.returncode) + ' ' + process.stderr[-3500:])
    value = json.loads(lines[0])
    if value.get('root_proof_complete') is not False or value.get('new_given') != 0 or value.get('base_step_inferred') is not True:
        raise RuntimeError('FALSE_PROOF_CLAIM')
    return value


def report_path() -> Path:
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / 'report.json'


def execute(dry_run: bool, timeout: int) -> int:
    report = {'phase': '176_R3R9', 'dry_run': dry_run,
              'timestamp_utc': datetime.now(timezone.utc).isoformat(),
              'gate': 'FAIL_R3R9', 'new_given': 0, 'new_mathematical_rules': 0,
              'full_pytest': 'NOT_RUN', 'root_proof_complete': False}
    try:
        report['preflight'] = preflight()
        if not dry_run:
            report['observed'] = worker(timeout)
        report['gate'] = ('PASS_R3R9_READ_ONLY_DRYRUN' if dry_run else
                          'PASS_R3R9_RIGHT_COMPOSITION_TYPE_FRONTIER')
    except Exception as exc:
        report['error'] = type(exc).__name__ + ': ' + str(exc)
        report['traceback'] = traceback.format_exc()[-6500:]
    report_path().write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE176_R3R9_GATE=' + report['gate'])
    print('PHASE176_R3R9_REPORT=' + str(report_path()))
    print('PHASE176_R3R9_HEAD=' + str(report.get('preflight', {}).get('head', 'UNVERIFIED')))
    if 'observed' in report:
        row = report['observed']
        print('PHASE176_R3R9_GROUP=(3,5) STATUS=' + row['search_status'] + ' OPEN=' + str(row['open_goals']))
        print('PHASE176_R3R9_BASE_STEP_INFERRED=' + str(row['base_step_inferred']))
        print('PHASE176_R3R9_SHARED_WHOLE_ZERO_PROPOSALS=' + str(row['public_whole_zero_proposals']['count']))
        print('PHASE176_R3R9_COMPOSITE_IMAGE_ZERO_PROPOSALS=' + str(row['generic_composite_image_proposals_for_zero_target']['count']))
    if 'error' in report:
        print('PHASE176_R3R9_ERROR=' + report['error'])
    print('PHASE176_R3R9_FULL_PYTEST=NOT_RUN')
    print('(END)')
    return 0 if report['gate'].startswith('PASS_') else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return execute(args.dry_run, args.timeout)


if __name__ == '__main__':
    raise SystemExit(main())

```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
$oldAddopts = $env:PYTEST_ADDOPTS
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTEST_ADDOPTS = "$oldAddopts -p no:cacheprovider".Trim()
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r9_right_composition_type_boundary.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R9 DryRun failed' }
    } else {
        python -B -m pytest -q -p no:cacheprovider phase176_r3r9_right_composition_type_boundary/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R9 focused pytest failed' }
        python -B -m phase176_r3r9_right_composition_type_boundary.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R9 audit failed' }
    }
} finally {
    $env:PYTEST_ADDOPTS = $oldAddopts
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTHONIOENCODING = $oldEncoding
    Pop-Location
}

```

## `tests/__init__.py`

```python

```

## `tests/test_audit.py`

```python
"""Focused read-only contract tests for the R3R9 typing boundary."""
from __future__ import annotations

import json

import pytest

from phase176_r3r9_right_composition_type_boundary import audit


def test_source_contract_accepts_literal_fixture(tmp_path) -> None:
    for name, anchors in audit.SOURCES.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(anchors), encoding='utf-8')
    assert set(audit.check_sources(tmp_path)) == set(audit.SOURCES)


def test_source_contract_rejects_changed_source(tmp_path) -> None:
    for name in audit.SOURCES:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('unrelated', encoding='utf-8')
    with pytest.raises(RuntimeError, match='SOURCE_ANCHOR_MISSING'):
        audit.check_sources(tmp_path)


def test_summary_does_not_report_proof() -> None:
    class Rule:
        name = 'fixture only'

    class Candidate:
        rule = Rule()
        subgoals = ('one',)

    info = audit.summarize((Candidate(),))
    assert info == {'count': 1, 'status': 'UNVERIFIED_PROPOSALS',
                    'rules': ['fixture only'], 'subgoal_counts': [1]}


def test_summary_preserves_empty_candidate_count() -> None:
    assert audit.summarize(())['count'] == 0


def test_dryrun_does_not_execute_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'test'})
    monkeypatch.setattr(audit, 'worker', lambda timeout: pytest.fail('worker was started'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    assert audit.execute(True, 120) == 0
    report = json.loads((tmp_path / 'EHPProofTracerAudit' / audit.PACKAGE / 'report.json').read_text(encoding='utf-8'))
    assert report['root_proof_complete'] is False
    assert report['full_pytest'] == 'NOT_RUN'


def test_worker_rejects_false_proof_claim(monkeypatch) -> None:
    class Result:
        returncode = 0
        stdout = audit.MARKER + json.dumps({'root_proof_complete': True,
                                            'new_given': 0, 'base_step_inferred': True})
        stderr = ''

    monkeypatch.setattr(audit.subprocess, 'run', lambda *args, **kwargs: Result())
    with pytest.raises(RuntimeError, match='FALSE_PROOF_CLAIM'):
        audit.worker(5)

```

