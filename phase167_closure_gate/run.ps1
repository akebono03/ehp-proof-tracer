$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$folder = Join-Path $root 'phase167_closure_gate'
if (-not (Test-Path (Join-Path $root 'web_group_proof.py'))) {
    throw 'Run from the EHP Proof Tracer repository root.'
}
$env:PYTHONPATH = $root
$started = (Get-Date).ToString('yyyy-MM-ddTHH:mm:ssK')
$metadata = [ordered]@{
    started = $started
    branch = ((git branch --show-current) -join "`n")
    commit = ((git rev-parse HEAD) -join "`n")
    dirty_files = @((git status --short))
}
$metadata | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $folder 'execution_metadata.json') -Encoding UTF8
Write-Host '=== Phase 167 1-stem public narrative audit ==='
python (Join-Path $folder 'audit.py') 2>&1 | Tee-Object -FilePath (Join-Path $folder 'stem1_audit.log')
if ($LASTEXITCODE -ne 0) { throw '1-stem audit crashed; see stem1_audit.log' }
Write-Host '=== Phase 167 closing full pytest (one run) ==='
$pytestLog = Join-Path $folder 'pytest_full.log'
python -m pytest -q --tb=short --disable-warnings 2>&1 | Tee-Object -FilePath $pytestLog
$code = $LASTEXITCODE
"PYTEST_EXIT_CODE=$code" | Set-Content (Join-Path $folder 'pytest_exit_code.txt') -Encoding UTF8
Write-Host "PYTEST_EXIT_CODE=$code"
Write-Host "PYTEST_LOG=$pytestLog"
Write-Host "AUDIT_REPORT=$(Join-Path $folder 'stem1_audit.json')"
if ($code -ne 0) { Write-Warning 'Phase 167 closure NOT confirmed: full pytest failed.' }
else { Write-Host 'Full pytest PASS. Review stem1_audit.json findings before recording Phase closure.' }
