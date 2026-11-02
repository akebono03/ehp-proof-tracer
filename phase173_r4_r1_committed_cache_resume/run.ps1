param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
Push-Location -LiteralPath $root
$oldPath = $env:PYTHONPATH
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    $env:PYTHONPATH = $root
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Write-Output 'PHASE173_R4_R1_RESUME_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_committed_cache_resume\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 resume focused pytest failed' }
    Write-Output 'PHASE173_R4_R1_RESUME_FOCUSED_PYTEST=PASS'
    $arguments = @('.\phase173_r4_r1_committed_cache_resume\audit.py', '--root', $root)
    if ($DryRun) { $arguments += '--dry-run' }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 resumed audit failed' }
}
finally {
    $env:PYTHONPATH = $oldPath
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    Pop-Location
}
