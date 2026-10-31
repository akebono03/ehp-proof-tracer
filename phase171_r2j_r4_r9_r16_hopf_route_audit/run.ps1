param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$PackagePath = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $PackagePath
Push-Location $Root
try {
    $argsPy = @('-m', 'phase171_r2j_r4_r9_r16_hopf_route_audit.audit', '--dry-run')
    & python @argsPy
    if ($LASTEXITCODE -ne 0) { throw 'R16 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R16_DRY_RUN=PASS'
        exit 0
    }
    Write-Output 'PHASE171_R16_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider 'phase171_r2j_r4_r9_r16_hopf_route_audit/tests/test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R16 focused pytest failed' }
    Write-Output 'PHASE171_R16_FOCUSED_PYTEST=PASS'
    & python -m phase171_r2j_r4_r9_r16_hopf_route_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R16 audit failed' }
    Write-Output 'PHASE171_R16_RESULT=PASS_READ_ONLY_HOPF_ROUTE_AUDIT'
}
finally {
    Pop-Location
}
