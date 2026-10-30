param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Set-Location $Root
if ($DryRun) {
    python -m phase171_r2j_r4_r9_r19_right_end_diagnostic.audit --dry-run
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Output 'PHASE171_R19_DRY_RUN=PASS'
    exit 0
}
python -m phase171_r2j_r4_r9_r19_right_end_diagnostic.audit --dry-run
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'PHASE171_R19_FOCUSED_PYTEST_START'
python -m pytest -q -p no:cacheprovider .\phase171_r2j_r4_r9_r19_right_end_diagnostic\tests\test_audit.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'PHASE171_R19_FOCUSED_PYTEST=PASS'
python -m phase171_r2j_r4_r9_r19_right_end_diagnostic.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'PHASE171_R19_RESULT=PASS_READ_ONLY_RIGHT_END_AUDIT'
