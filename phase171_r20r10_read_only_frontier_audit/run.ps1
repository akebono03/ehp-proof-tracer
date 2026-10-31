param(
    [switch]$DryRun,
    [switch]$SkipReferenceComparison,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    if (-not $DryRun -and -not $SkipTests) {
        & python -B -m pytest -p no:cacheprovider -q '.\phase171_r20r10_read_only_frontier_audit\tests\test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R20R10 focused pytest failed' }
    }
    $ArgsForAudit = @('-B', '-m', 'phase171_r20r10_read_only_frontier_audit.audit')
    if ($DryRun) { $ArgsForAudit += '--dry-run' }
    if ($SkipReferenceComparison) { $ArgsForAudit += '--skip-reference-comparison' }
    & python @ArgsForAudit
    if ($LASTEXITCODE -ne 0) { throw 'R20R10 read-only audit failed' }
}
finally {
    Pop-Location
}
