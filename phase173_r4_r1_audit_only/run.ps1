param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
Push-Location -LiteralPath $root
$oldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $root
    Write-Output 'PHASE173_R4_R1_FOCUSED_PYTEST_START'
    & python -m pytest -q '.\phase173_r4_r1_audit_only\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 focused pytest failed' }
    Write-Output 'PHASE173_R4_R1_FOCUSED_PYTEST=PASS'
    $arguments = @('.\phase173_r4_r1_audit_only\audit.py', '--root', $root)
    if ($DryRun) { $arguments += '--dry-run' }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 audit failed' }
}
finally {
    $env:PYTHONPATH = $oldPythonPath
    Pop-Location
}
