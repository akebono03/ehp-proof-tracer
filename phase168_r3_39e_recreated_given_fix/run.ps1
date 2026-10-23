$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$Target = Join-Path $Project 'phase165_r52_r16_web_citation_gate.py'
$Backup = Join-Path $PSScriptRoot 'original_web_citation_gate.py'
Copy-Item -LiteralPath $Target -Destination $Backup -Force
try {
    python (Join-Path $PSScriptRoot 'apply.py')
    if ($LASTEXITCODE -ne 0) { throw 'Patch application failed.' }
    python -m pytest -q (Join-Path $PSScriptRoot 'tests/test_phase168_r3_39e_recreated_given.py')
    if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed.' }
    Write-Host 'R3-39E scoped GIVEN screening: passed; full suite NOT run.'
} catch {
    Copy-Item -LiteralPath $Backup -Destination $Target -Force
    Write-Host 'ROLLBACK: original Web citation gate restored.'
    throw
}
