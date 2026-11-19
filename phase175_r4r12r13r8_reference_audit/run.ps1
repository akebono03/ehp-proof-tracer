param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r12r13r8_reference_audit'
if (-not (Test-Path (Join-Path $package 'audit.py'))) { throw 'Execute this script from the repository root.' }
$head = & git rev-parse --abbrev-ref HEAD
if ($LASTEXITCODE -ne 0 -or $head -ne 'develop') { throw 'Expected develop branch; nothing changed.' }
$before = & git status --porcelain
Write-Output 'PHASE175_R13R8_MODE=READ_ONLY_AUDIT'
if ($DryRun) {
    & python -B (Join-Path $package 'audit.py') --root $repo
} else {
    & python -B -m pytest -q -p no:cacheprovider (Join-Path (Join-Path $package 'tests') 'test_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R13R8 audit tests failed' }
    $out = Join-Path $env:TEMP 'EHP_Phase175_R13R8_report.json'
    & python -B (Join-Path $package 'audit.py') --root $repo --output $out
}
if ($LASTEXITCODE -ne 0) { throw 'R13R8 source audit failed' }
$after = & git status --porcelain
if (($before -join "`n") -ne ($after -join "`n")) { throw 'Repository status changed unexpectedly' }
Write-Output 'PHASE175_R13R8_REPOSITORY_UNCHANGED=PASS'
Write-Output 'PHASE175_R13R8_GATE=AUDIT_ONLY_NOT_COMPLETE'
