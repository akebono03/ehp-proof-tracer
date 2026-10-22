$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
Write-Host "R2-7(2): read-only registry audit"
Write-Host "Repository: $repo"
python -m pytest ".\phase168_r2_7_2_registry_source_audit\tests\test_audit.py" -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m phase168_r2_7_2_registry_source_audit.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
