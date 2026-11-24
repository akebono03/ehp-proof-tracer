# R3R46R2 変更コード全文

既存 `run.ps1` を置換し、同じディレクトリに `pytest_runner.py` を追加する。

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
    & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner --check-only
    if ($LASTEXITCODE -ne 0) { throw 'R3R46R2 canonical import check failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R46R1_GATE=PASS_R3R46R1_DRYRUN'
        Write-Host 'PHASE176_R3R46R2_GATE=PASS_R3R46R2_IMPORT_DRYRUN'
    } else {
        $groups = @(
            'phase176_r3r46r1_prior_group_availability/tests/test_prior_availability.py',
            'phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py',
            'phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py',
            'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
            'phase176_r3r45_direct_premise_audit/tests/test_audit.py',
            'tests/test_phase165_r3_recursive_search.py'
        )
        foreach ($group in $groups) {
            Write-Host ('PHASE176_R3R46R2_TEST_GROUP=' + $group)
            & python -B -m phase176_r3r46r1_prior_group_availability.pytest_runner $group
            if ($LASTEXITCODE -ne 0) { throw ('R3R46R2 focused pytest failed: ' + $group) }
        }
        Write-Host 'PHASE176_R3R46R2_GATE=PASS_R3R46R2_ISOLATED_FOCUSED_TESTS'
        & python -B -m phase176_r3r46r1_prior_group_availability.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R46R1 Web audit failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R46R1 diff check failed' }
        Write-Host 'PHASE176_R3R46R1_GATE=PASS_R3R46R1_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R46R2_GATE=PASS_R3R46R2_RESUMED_PUBLIC_AUDIT'
        Write-Host 'PHASE176_R3R46R1_NEW_MATH_RULES=0'
        Write-Host 'PHASE176_R3R46R1_NEW_GIVEN_REGISTRATIONS=0'
        Write-Host 'PHASE176_R3R46R1_FULL_PYTEST=NOT_RUN'
    }
    Write-Host '(END)'
} finally { Pop-Location }
```

## `pytest_runner.py`

```python
"""Run one focused suite in a fresh process with canonical Hopf module identity."""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import inspect
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def canonical_hopf_modules() -> None:
    """Load production modules before tests/conftest.py changes sys.path."""
    for name in ('hopf_rules', 'hopf_facts'):
        expected = (ROOT / (name + '.py')).resolve()
        spec = importlib.util.find_spec(name)
        if spec is None or spec.origin is None or Path(spec.origin).resolve() != expected:
            raise RuntimeError(f'NONCANONICAL_MODULE:{name}:{getattr(spec, "origin", None)}')
        module = importlib.import_module(name)
        if Path(module.__file__).resolve() != expected:
            raise RuntimeError(f'NONCANONICAL_LOADED_MODULE:{name}:{module.__file__}')
        print(f'PHASE176_R3R46R2_IMPORT_{name.upper()}={expected}', flush=True)
    from hopf_rules import HopfInvariantStatement
    from hopf_facts import ETA_2_HOPF_INVARIANT_FACT

    parameters = inspect.signature(HopfInvariantStatement).parameters
    if not {'expression', 'value', 'source', 'note'}.issubset(parameters):
        raise RuntimeError('CANONICAL_HOPF_SIGNATURE_MISMATCH')
    if type(ETA_2_HOPF_INVARIANT_FACT) is not HopfInvariantStatement:
        raise RuntimeError('CANONICAL_HOPF_TYPE_IDENTITY_MISMATCH')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('test_file', nargs='?')
    args = parser.parse_args()
    if Path.cwd().resolve() != ROOT:
        raise RuntimeError('REPOSITORY_ROOT_REQUIRED')
    if args.check_only == bool(args.test_file):
        parser.error('specify exactly one test file or --check-only')
    canonical_hopf_modules()
    if args.check_only:
        return 0
    path = (ROOT / args.test_file).resolve()
    if ROOT not in path.parents or not path.is_file() or path.suffix != '.py':
        raise RuntimeError('INVALID_FOCUSED_TEST_PATH')
    import pytest

    return int(pytest.main(['-q', '-p', 'no:cacheprovider', '--import-mode=importlib', str(path)]))


if __name__ == '__main__':
    raise SystemExit(main())
```

