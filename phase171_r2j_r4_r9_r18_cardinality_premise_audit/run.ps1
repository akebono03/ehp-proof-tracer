param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Push-Location $Root
try {
    & python -m phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R18 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R18_DRY_RUN=PASS'
        exit 0
    }
    Write-Output 'PHASE171_R18_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider 'phase171_r2j_r4_r9_r18_cardinality_premise_audit/tests/test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R18 focused pytest failed' }
    Write-Output 'PHASE171_R18_FOCUSED_PYTEST=PASS'
    & python -m phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R18 audit failed' }
    Write-Output 'PHASE171_R18_RESULT=PASS_READ_ONLY_CARDINALITY_AUDIT'
}
finally {
    Pop-Location
}
