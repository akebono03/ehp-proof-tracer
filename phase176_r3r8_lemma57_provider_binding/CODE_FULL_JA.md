# Phase 176 R3R8 — 追加コード全文

既存コードの置き換えはありません。以下のコードをパッケージに新規追加します。

## audit.py

```python
"""Phase 176 R3R8: isolated source-screened Lemma 5.7 provider binding.

This audit does not modify the shared public search or admit a new GIVEN.
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
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'phase176_r3r8_lemma57_provider_binding'
REVIEWED_HEAD = '0bf1f12b0ba32e197835b4ac68d250e50edaf9cc'
MARKER = 'PHASE176_R3R8_WORKER_JSON='
SOURCES = {
    'phase176_r3r7_lemma57_derived_source_proof/audit.py': (
        'def derive_from_existing_source(', 'def selected_source_steps(',
    ),
    'phase175_r3r9_lemma57_explicit_public/source.py': (
        'def build_explicit_lemma57_source(',
    ),
    'phase175_r3r9_lemma57_explicit_public/rule.py': (
        'def expand_cited_lemma57_explicit_zero(',
    ),
    'phase169_r10e2_unpositioned_citation/source_first.py': (
        'def screen_independent_sources_for_derived_goal(',
    ),
    'phase165_r52_r9_shared_math.py': (
        'def shared_expansion_provider(',
    ),
    'sources/toda/Toda_05_2.tex': (
        r'\label{lemma:5.7}', r"E(\eta_2\circ\nu')=0",
    ),
}


def git(*args: str, check: bool = True) -> tuple[int, str]:
    process = subprocess.run(('git',) + args, cwd=ROOT, capture_output=True,
                             text=True, encoding='utf-8', errors='replace', check=False)
    if check and process.returncode:
        raise RuntimeError('GIT_FAILED: ' + ' '.join(args) + ': ' + process.stderr.strip())
    return process.returncode, process.stdout.strip()


def check_sources(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name, anchors in SOURCES.items():
        path = root / name
        if not path.is_file():
            raise RuntimeError('SOURCE_MISSING: ' + name)
        content = ''.join(path.read_text(encoding='utf-8-sig').split())
        missing = [anchor for anchor in anchors if ''.join(anchor.split()) not in content]
        if missing:
            raise RuntimeError('SOURCE_ANCHORS_MISSING: ' + name + ': ' + repr(missing))
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def preflight() -> dict[str, object]:
    if Path(git('rev-parse', '--show-toplevel')[1]).resolve() != ROOT.resolve():
        raise RuntimeError('REPOSITORY_ROOT_MISMATCH')
    if git('branch', '--show-current')[1] != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    if git('merge-base', '--is-ancestor', REVIEWED_HEAD, 'HEAD', check=False)[0]:
        raise RuntimeError('REVIEWED_HEAD_NOT_ANCESTOR')
    if git('status', '--porcelain', '--untracked-files=no')[1]:
        raise RuntimeError('TRACKED_FILES_DIRTY')
    return {
        'head': git('rev-parse', 'HEAD')[1],
        'source_sha256': check_sources(ROOT),
        'tracked_clean': True,
        'full_pytest': 'NOT_RUN',
        'historical_source_guards': 'FOUR_KNOWN_FAILURES_NOT_PASSING',
    }


def source_bound_provider(
    ordinary: Callable[[object], object],
    screened_source_steps: tuple[object, ...],
    source_type: type,
    source_expander: Callable[[object, tuple[object, ...]], object],
) -> Callable[[object], tuple[object, ...]]:
    """Prepend only an already screened citation's existing inference proposal.

    This closure is *isolated*: it is not registered in production.
    """
    if not isinstance(screened_source_steps, tuple) or len(screened_source_steps) != 1:
        raise ValueError('ONE_SCREENED_SOURCE_STEP_REQUIRED')
    from proof import ProofRule, ProofStep

    source_step = screened_source_steps[0]
    if (
        not isinstance(source_step, ProofStep)
        or source_step.rule is not ProofRule.GIVEN
        or source_step.premises
        or type(source_step.conclusion) is not source_type
    ):
        raise ValueError('INVALID_SCREENED_SOURCE_STEP')
    citation = getattr(getattr(source_step, 'inference_rule', None), 'literature_reference', None)
    if citation is None or citation.locator != 'Lemma 5.7':
        raise ValueError('LEMMA57_CITATION_REQUIRED')
    available = (source_step.conclusion,)

    def expand(goal: object) -> tuple[object, ...]:
        cited = tuple(source_expander(goal, available))
        original = tuple(ordinary(goal))
        if cited and (
            len(cited) != 1
            or tuple(cited[0].subgoals) != available
        ):
            raise RuntimeError('UNEXPECTED_SOURCE_EXPANSION')
        return cited + original

    return expand


def observe() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
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
        selected_source_steps, derive_from_existing_source,
    )
    from proof import ProofRule, Relation

    public = search_group_from_registered_goal(n=3, k=5)
    if public.status.value != 'search_failed' or len(public.open_goals) != 3:
        raise RuntimeError('PUBLIC_FRONTIER_DRIFT')
    target = next((g for g in public.open_goals if isinstance(g, Relation)
                   and g.lhs == TodaPrimaryGroup(8, 3)), None)
    if target is None:
        raise RuntimeError('TARGET_GOAL_MISSING')
    prior = exact_prior_database_result(2, 5)
    if not isinstance(prior, Relation) or prior.lhs != TodaPrimaryGroup(7, 2):
        raise RuntimeError('PRIOR_PRESENTATION_DRIFT')
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError('PRIOR_GENERATOR_DRIFT')
    base = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        Composition(factors[0], factors[1]), Zero(),
    )
    if not exact_lemma57_zero_image_goal(base):
        raise RuntimeError('SOURCE_GOAL_TYPED_MATCH_FAILED')

    default_bridge = build_shared_typed_bridge()
    augmented = merge_isolated_cited_source(default_bridge, build_explicit_lemma57_source(ROOT))
    screened = screen_independent_sources_for_derived_goal(augmented, goal=target)
    sources = selected_source_steps(screened, TodaLemma57ExplicitNuPrimeZero)
    if len(sources) != 1:
        raise RuntimeError('SOURCE_NOT_UNIQUELY_SCREENED')
    ordinary = shared_expansion_provider(screened, proof_target=target)
    baseline = tuple(ordinary(base))
    bound = source_bound_provider(
        ordinary, sources, TodaLemma57ExplicitNuPrimeZero,
        expand_cited_lemma57_explicit_zero,
    )
    options = bound(base)
    cited = tuple(x for x in options if x.rule.name ==
                  'extract explicit nu-prime zero-suspension clause of Toda Lemma 5.7')
    if len(cited) != 1 or len(options) != len(baseline) + 1:
        raise RuntimeError('BASE_PROPOSAL_NOT_CONNECTED')
    step = derive_from_existing_source(cited[0], sources[0])
    if step.rule is not ProofRule.INFERENCE or step.conclusion != base:
        raise RuntimeError('INFERENCE_STEP_INVALID')
    db = admitted_db_step(prior, proof_target=target, bridge=screened)
    if db is None or not verified_db_step(db, proof_target=target, bridge=screened):
        raise RuntimeError('PRIOR_DB_INELIGIBLE')
    unrelated = target
    if bound(unrelated) != tuple(ordinary(unrelated)):
        raise RuntimeError('UNRELATED_GOAL_PROVIDER_CHANGED')
    return {
        'public_search_status': public.status.value,
        'public_open_goals': len(public.open_goals),
        'lemma57_screened_count': len(sources),
        'default_base_proposals': len(baseline),
        'isolated_bound_base_proposals': len(options),
        'isolated_lemma57_proposals': len(cited),
        'isolated_base_proof_step_inferred': True,
        'inferred_step_rule': step.rule.value,
        'source_reference': 'Lemma 5.7',
        'prior_db_verified': True,
        'unrelated_goal_unchanged': True,
        'production_provider_modified': False,
        'production_bridge_modified': False,
        'new_given': 0,
        'new_mathematical_rules': 0,
        'root_proof_complete': False,
        'next_blockers': [
            'RIGHT_COMPOSITION_TRANSPORT_AND_ZERO_NORMALIZATION',
            'ZERO_IMAGE_TO_HOPF_INJECTIVITY',
            'FINITE_ORDER_TWO_IMAGE_SUBGROUP_HOPF_LIFT',
        ],
    }


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    try:
        result = subprocess.run(
            (sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker'),
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding='utf-8', errors='replace', check=False, timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('WORKER_TIMEOUT') from exc
    rows = [line[len(MARKER):] for line in result.stdout.splitlines() if line.startswith(MARKER)]
    if result.returncode or len(rows) != 1:
        raise RuntimeError('WORKER_FAILED: rc=' + str(result.returncode)
                           + ' stderr=' + result.stderr[-4000:]
                           + ' stdout=' + result.stdout[-1000:])
    data = json.loads(rows[0])
    if (data.get('new_given') != 0 or data.get('new_mathematical_rules') != 0
            or data.get('root_proof_complete') is not False
            or data.get('production_provider_modified') is not False
            or data.get('isolated_base_proof_step_inferred') is not True):
        raise RuntimeError('WORKER_FALSE_PROOF_CLAIM')
    return data


def report_path() -> Path:
    target = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    target.mkdir(parents=True, exist_ok=True)
    return target / 'report.json'


def execute(dry_run: bool, timeout: int) -> int:
    record: dict[str, object] = {
        'phase': '176_R3R8',
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'dry_run': dry_run,
        'gate': 'FAIL_R3R8',
        'full_pytest': 'NOT_RUN',
        'new_given': 0,
        'new_mathematical_rules': 0,
        'root_proof_complete': False,
    }
    try:
        record['preflight'] = preflight()
        if not dry_run:
            record['observed'] = worker(timeout)
        record['gate'] = ('PASS_R3R8_READ_ONLY_DRYRUN' if dry_run
                          else 'PASS_R3R8_ISOLATED_SOURCE_PROVIDER_BINDING')
    except Exception as exc:
        record['error'] = type(exc).__name__ + ': ' + str(exc)
        record['traceback'] = traceback.format_exc()[-8000:]
    target = report_path()
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE176_R3R8_GATE=' + str(record['gate']))
    print('PHASE176_R3R8_REPORT=' + str(target))
    print('PHASE176_R3R8_HEAD=' + str(record.get('preflight', {}).get('head', 'UNVERIFIED')))
    if 'observed' in record:
        obj = record['observed']
        print('PHASE176_R3R8_GROUP=(3,5) STATUS=' + obj['public_search_status']
              + ' OPEN=' + str(obj['public_open_goals']))
        print('PHASE176_R3R8_DEFAULT_BASE_PROPOSALS=' + str(obj['default_base_proposals']))
        print('PHASE176_R3R8_ISOLATED_BASE_PROPOSALS=' + str(obj['isolated_bound_base_proposals']))
        print('PHASE176_R3R8_BASE_STEP_INFERRED=' + str(obj['isolated_base_proof_step_inferred']))
    if 'error' in record:
        print('PHASE176_R3R8_ERROR=' + str(record['error']))
    print('PHASE176_R3R8_FULL_PYTEST=NOT_RUN')
    print('(END)')
    return 0 if str(record['gate']).startswith('PASS_') else 1


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

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
$previousAddopts = $env:PYTEST_ADDOPTS
$previousBytes = $env:PYTHONDONTWRITEBYTECODE
$previousEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTEST_ADDOPTS = "$previousAddopts -p no:cacheprovider".Trim()
    if ($DryRun) {
        python -B -m phase176_r3r8_lemma57_provider_binding.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R8 DryRun failed' }
    } else {
        python -B -m pytest -q -p no:cacheprovider phase176_r3r8_lemma57_provider_binding/tests/test_audit.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R8 focused pytest failed' }
        python -B -m phase176_r3r8_lemma57_provider_binding.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R8 audit failed' }
    }
} finally {
    $env:PYTEST_ADDOPTS = $previousAddopts
    $env:PYTHONDONTWRITEBYTECODE = $previousBytes
    $env:PYTHONIOENCODING = $previousEncoding
    Pop-Location
}

```

## tests/test_audit.py

```python
"""R3R8 contract tests; real checkout validation happens in the worker."""
from __future__ import annotations

import json

import pytest

from phase176_r3r8_lemma57_provider_binding import audit


def test_source_contract_accepts_fixture(tmp_path) -> None:
    for name, anchors in audit.SOURCES.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('\n'.join(anchors), encoding='utf-8')
    assert set(audit.check_sources(tmp_path)) == set(audit.SOURCES)


def test_source_contract_rejects_missing_anchor(tmp_path) -> None:
    for name in audit.SOURCES:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('changed source', encoding='utf-8')
    with pytest.raises(RuntimeError, match='SOURCE_ANCHORS_MISSING'):
        audit.check_sources(tmp_path)


def test_source_bound_provider_rejects_empty_sources() -> None:
    with pytest.raises(ValueError, match='ONE_SCREENED_SOURCE_STEP_REQUIRED'):
        audit.source_bound_provider(lambda goal: (), (), object, lambda goal, refs: ())


def test_source_bound_provider_rejects_non_tuple_sources() -> None:
    with pytest.raises(ValueError, match='ONE_SCREENED_SOURCE_STEP_REQUIRED'):
        audit.source_bound_provider(lambda goal: (), [], object, lambda goal, refs: ())


def test_source_bound_provider_rejects_false_step(monkeypatch) -> None:
    import sys
    from types import SimpleNamespace

    class StubProofStep:
        pass

    monkeypatch.setitem(sys.modules, 'proof', SimpleNamespace(
        ProofStep=StubProofStep,
        ProofRule=SimpleNamespace(GIVEN='given'),
    ))
    with pytest.raises(ValueError, match='INVALID_SCREENED_SOURCE_STEP'):
        audit.source_bound_provider(lambda goal: (), ('string not a ProofStep',), str, lambda goal, refs: ())


def test_worker_rejects_false_completion(monkeypatch) -> None:
    import subprocess

    class Result:
        returncode = 0
        stdout = audit.MARKER + json.dumps({
            'new_given': 0,
            'new_mathematical_rules': 0,
            'root_proof_complete': True,
            'production_provider_modified': False,
            'isolated_base_proof_step_inferred': True,
        })
        stderr = ''

    monkeypatch.setattr(subprocess, 'run', lambda *args, **kwargs: Result())
    with pytest.raises(RuntimeError, match='WORKER_FALSE_PROOF_CLAIM'):
        audit.worker(5)


def test_dry_run_does_not_execute_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'test'})
    monkeypatch.setattr(audit, 'worker', lambda timeout: pytest.fail('worker called'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    assert audit.execute(True, 5) == 0
    report = json.loads((tmp_path / 'EHPProofTracerAudit' / audit.PACKAGE / 'report.json').read_text(encoding='utf-8'))
    assert report['full_pytest'] == 'NOT_RUN'
    assert report['new_given'] == 0
    assert report['root_proof_complete'] is False

```

## __init__.py

```python

```

## tests/__init__.py

```python

```
