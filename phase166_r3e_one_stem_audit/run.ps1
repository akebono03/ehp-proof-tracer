$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -m phase166_r3e_one_stem_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-E read-only audit failed' }
python -m pytest -q '.\phase166_r3e_one_stem_audit\test_r3e.py'
if ($LASTEXITCODE -ne 0) {
    Write-Host 'R3-E completion condition not met; inspect audit_result.json. No production code changed.'
    exit 1
}
Write-Host 'R3-E focused PASS; no production modifications; full pytest NOT run.'
