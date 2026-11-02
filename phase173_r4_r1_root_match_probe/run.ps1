param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $Here '..')).Path
Push-Location $Root
try {
    Write-Output 'PHASE173_R4_R1_ROOT_MATCH_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_root_match_probe\tests'
    if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R4-R1 root-match focused pytest failed' }
    Write-Output 'PHASE173_R4_R1_ROOT_MATCH_FOCUSED_PYTEST=PASS'
    $AuditArguments = @('-m', 'phase173_r4_r1_root_match_probe.audit', '--root', $Root)
    if ($DryRun) { $AuditArguments += '--dry-run' }
    & python @AuditArguments
    if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R4-R1 root-match audit failed' }
}
finally {
    Pop-Location
}
