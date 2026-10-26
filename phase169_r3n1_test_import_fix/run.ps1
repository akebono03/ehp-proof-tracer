$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Write-Host 'Phase 169 R3N1: import-only focused-test repair'
$root = (Get-Location).Path
$testPath = Join-Path $root 'phase169_r3n_prior_result_search\tests\test_r3n_prior_result_alias.py'
$pipeline = Join-Path $root 'phase169_r3n_prior_result_search\run.ps1'
if (-not (Test-Path -LiteralPath $testPath -PathType Leaf)) { throw 'R3N1 test file missing' }
if (-not (Test-Path -LiteralPath $pipeline -PathType Leaf)) { throw 'R3N pipeline missing' }
python -B -c "import ast, pathlib; p=pathlib.Path(r'$testPath'); t=ast.parse(p.read_text(encoding='utf-8')); names=[a.name for stmt in t.body if isinstance(stmt,ast.ImportFrom) and stmt.module=='expression' for a in stmt.names]; assert 'eta' in names and 'nu' in names, names; print('R3N1_ETA_IMPORT_PRESENT=True')"
if ($LASTEXITCODE -ne 0) { throw "R3N1 preflight failed: $LASTEXITCODE" }
& powershell -ExecutionPolicy Bypass -File $pipeline
if ($LASTEXITCODE -ne 0) { throw "R3N1 pipeline failed: $LASTEXITCODE" }
Write-Host 'R3N1_COMPLETE: missing test import fixed; R3N limited validation completed.'
