param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Push-Location $Root
try {
    & python -m phase171_r2j_r4_r9_r17_public_context_path_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R17 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R17_DRY_RUN=PASS'
        exit 0
    }
    Write-Output 'PHASE171_R17_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider 'phase171_r2j_r4_r9_r17_public_context_path_audit/tests/test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R17 focused pytest failed' }
    Write-Output 'PHASE171_R17_FOCUSED_PYTEST=PASS'
    & python -m phase171_r2j_r4_r9_r17_public_context_path_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R17 audit failed' }
    Write-Output 'PHASE171_R17_RESULT=PASS_READ_ONLY_CONTEXT_PATH_AUDIT'
}
finally {
    Pop-Location
}
