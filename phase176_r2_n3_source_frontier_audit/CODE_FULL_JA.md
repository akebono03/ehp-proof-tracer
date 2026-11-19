# Phase 176 R2 — 追加コード全文

追加位置：リポジトリ直下の `phase176_r2_n3_source_frontier_audit/`。既存クラス・関数・import の変更はありません。

## `audit.py`

```python
"""Phase 176 R2: read-only Toda source and n=3, k=5 proof-frontier audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'phase176_r2_n3_source_frontier_audit'
R1_PACKAGE = 'phase176_r1_k5_source_first_audit'
R1_HEAD = 'bc318d6a66bd124cb6707559a6d2dc42128443b3'
MARKER = 'PHASE176_R2_WORKER_JSON='
SOURCE_CH5 = 'sources/toda/Toda_05_2.tex'
SOURCE_CH2 = 'sources/toda/Toda_02_2.tex'
EVIDENCE = {
    'Lemma 5.7': (SOURCE_CH5, ('\\label{lemma:5.7}', 'E(\\eta_2\\circ\\nu\')=0')),
    '(5.5)': (SOURCE_CH5, ('\\textbf{(5.5).}', '4\\nu_{n}=\\eta_n^{3}')),
    '(5.3)': (SOURCE_CH5, ('\\textbf{(5.3).}', 'H(\\nu\')=\\eta_5')),
    'Proposition 5.6': (SOURCE_CH5, ('\\label{prop:5.6}', '\\mathbb Z_{8}')),
    '(5.2)': (SOURCE_CH5, ('\\textbf{(5.2).}', '\\pi^{3}_{i}')),
    'Proposition 2.2': (SOURCE_CH2, ('\\label{prop:2.2}', 'H(\\alpha\\circ E\\beta)')),
    'Proposition 5.9 proof': (SOURCE_CH5, ('\\label{prop:5.9}', '0\\to \\pi^{3}_{8}', '\\ker\\Delta', 'H(\\nu\'\\circ \\eta_6^2)')),
}


def git(*args: str) -> str:
    command = subprocess.run(('git',) + args, cwd=ROOT, capture_output=True,
                             text=True, encoding='utf-8', errors='replace', check=False)
    if command.returncode:
        raise RuntimeError('GIT_READ_FAILED: ' + ' '.join(args) + ': ' + command.stderr.strip())
    return command.stdout.strip()


def normalize(text: str) -> str:
    return re.sub(r'\s+', '', text)


def inspect_sources(root: Path = ROOT) -> dict[str, object]:
    source_texts = {}
    for path in sorted(set(path for path, _ in EVIDENCE.values())):
        source = root / path
        if not source.is_file():
            raise RuntimeError('SOURCE_NOT_FOUND: ' + path)
        source_texts[path] = source.read_text(encoding='utf-8-sig')
    result = {}
    for name, (path, anchors) in EVIDENCE.items():
        content = normalize(source_texts[path])
        missing = [anchor for anchor in anchors if normalize(anchor) not in content]
        result[name] = {'file': path, 'anchors_present': not missing, 'missing_anchors': missing}
    return result


def preflight() -> dict[str, object]:
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT.resolve():
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    head = git('rev-parse', 'HEAD')
    completed = subprocess.run(('git', 'merge-base', '--is-ancestor', R1_HEAD, 'HEAD'),
                               cwd=ROOT, capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError('R1_REVIEWED_HEAD_NOT_ANCESTOR')
    changed = git('status', '--porcelain', '--untracked-files=no')
    if changed:
        raise RuntimeError('TRACKED_FILES_DIRTY_REVIEW_REQUIRED: ' + changed[:700])
    source = inspect_sources()
    missing = [name for name, record in source.items() if not record['anchors_present']]
    if missing:
        raise RuntimeError('SOURCE_ANCHORS_REQUIRE_REVIEW: ' + ', '.join(missing))
    return {'head': head, 'r1_head_is_ancestor': True, 'source_anchors': source,
            'tracked_files_clean': True, 'full_pytest': 'NOT_RUN'}


def observe() -> dict[str, object]:
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from web_group_proof import build_standard_web_group_proof_view
    result = search_group_from_registered_goal(n=3, k=5)
    record: dict[str, object] = {
        'n': 3, 'k': 5,
        'search_status': str(result.status.value),
        'open_goals': len(result.open_goals),
        'proven_steps': len(result.proven_steps),
        'references': list(result.references),
        'open_goal_types': [type(goal).__name__ for goal in result.open_goals],
        'open_goal_strings': [str(goal)[:500] for goal in result.open_goals],
        'diagnostics': list(result.diagnostics),
        'conclusion_claimed': result.conclusion is not None,
    }
    try:
        view = build_standard_web_group_proof_view(3, 5, max_depth=2, mode='narrative')
        record['web_status'] = 'BUILT'
        record['web_view_type'] = type(view).__name__
        record['web_view_fields'] = {key: repr(value)[:1500]
                                     for key, value in vars(view).items()
                                     if key in {'provenance', 'proof_markdown', 'narrative_markdown', 'references', 'status', 'open_goals'}}
    except Exception as exc:
        record['web_status'] = 'ERROR'
        record['web_error'] = type(exc).__name__ + ': ' + str(exc)
    return record


def run_worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    try:
        process = subprocess.run((sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker'),
                                 cwd=ROOT, env=env, capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('N3_K5_SEARCH_TIMEOUT') from exc
    markers = [line[len(MARKER):] for line in process.stdout.splitlines() if line.startswith(MARKER)]
    if process.returncode or len(markers) != 1:
        raise RuntimeError('N3_K5_WORKER_FAILED: ' + process.stderr[-2000:])
    return json.loads(markers[0])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False, default=str))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    report: dict[str, object] = {'phase': '176_R2', 'mode': 'READ_ONLY_SOURCE_FRONTIER',
                                 'dry_run': args.dry_run, 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                                 'gate': 'FAIL_R2', 'full_pytest': 'NOT_RUN',
                                 'source_first': True, 'new_given': 0, 'new_rules': 0}
    try:
        report['preflight'] = preflight()
        if not args.dry_run:
            report['observed'] = run_worker(args.timeout)
        report['gate'] = 'PASS_R2_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R2_SOURCE_FRONTIER_AUDIT'
    except Exception as exc:
        report['error'] = type(exc).__name__ + ': ' + str(exc)
        report['traceback'] = traceback.format_exc()[-7000:]
    output = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    output.mkdir(parents=True, exist_ok=True)
    target = output / 'report.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE176_R2_GATE=' + report['gate'])
    print('PHASE176_R2_REPORT=' + str(target))
    print('PHASE176_R2_HEAD=' + report.get('preflight', {}).get('head', 'UNVERIFIED'))
    if 'observed' in report:
        record = report['observed']
        print('PHASE176_R2_GROUP=(3,5) STATUS=' + record['search_status'] + ' OPEN=' + str(record['open_goals']))
        print('PHASE176_R2_WEB=' + record['web_status'])
    if 'error' in report:
        print('PHASE176_R2_ERROR=' + report['error'])
    print('PHASE176_R2_FULL_PYTEST=NOT_RUN')
    print('(END)')
    return 1 if 'error' in report else 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase176_r2_n3_source_frontier_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R2 DryRun failed' }
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r2_n3_source_frontier_audit/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R2 focused pytest failed' }
        python -B -m phase176_r2_n3_source_frontier_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R2 Source Frontier audit failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R2 git diff check failed' }
    }
} finally {
    Pop-Location
}
```

## `__init__.py`

```python
"""Read-only Phase 176 R2 source frontier package."""
```

## `tests/__init__.py`

```python
"""Focused audit tests."""
```

## `tests/test_audit.py`

```python
from __future__ import annotations

import pytest

from phase176_r2_n3_source_frontier_audit import audit


def test_source_anchors_on_fixture(tmp_path) -> None:
    for name, (path, anchors) in audit.EVIDENCE.items():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('a', encoding='utf-8') as stream:
            stream.write(' '.join(anchors) + '\n')
    result = audit.inspect_sources(tmp_path)
    assert set(result) == set(audit.EVIDENCE)
    assert all(row['anchors_present'] for row in result.values())


def test_missing_anchor_not_forgiven(tmp_path) -> None:
    for path in {p for p, anchors in audit.EVIDENCE.values()}:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('unrelated source\n', encoding='utf-8')
    assert all(not record['anchors_present'] for record in audit.inspect_sources(tmp_path).values())


def test_normalize_source_spacing() -> None:
    assert audit.normalize(' H(\\alpha \\circ  E\\beta)\n') == audit.normalize('H(\\alpha\\circ E\\beta)')


def test_dry_run_never_launches_worker(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(audit, 'ROOT', tmp_path)
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'test-head'})
    monkeypatch.setattr(audit, 'run_worker', lambda timeout: pytest.fail('worker invoked'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    monkeypatch.setattr('sys.argv', ['audit', '--dry-run'])
    assert audit.main() == 0
```

