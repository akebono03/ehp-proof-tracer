param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$env:PYTHONPATH = $Root
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Output 'PHASE173_R3_PORTABLE_FOCUSED_PYTEST_START'
python -B -m pytest -q -p no:cacheprovider '.\phase173_r3_portable\tests\test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R3 focused pytest failed' }
Write-Output 'PHASE173_R3_PORTABLE_FOCUSED_PYTEST=PASS'
if ($DryRun) {
    python -B -m phase173_r3_portable.audit --dry-run
} else {
    python -B -m phase173_r3_portable.audit
}
if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R3 audit failed' }
git status -sb
