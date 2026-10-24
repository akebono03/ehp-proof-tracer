$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

python -m pytest -q ".\phase168_r3_41e_certified_prefix_reference_audit\tests\test_phase168_r3_41e_certified_prefix_reference_audit.py" ".\phase168_r3_41d1_boundary_audit_fix\tests\test_phase168_r3_41d1_boundary_audit_fix.py"
if ($LASTEXITCODE -ne 0) { throw 'R3-41E limited pytest failed' }

python -m phase168_r3_41e_certified_prefix_reference_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-41E cited-prefix audit failed' }
Write-Output 'R3-41E audit-only complete. No implementation files modified; full suite NOT run.'
