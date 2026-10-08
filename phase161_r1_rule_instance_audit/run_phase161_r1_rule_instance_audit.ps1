$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$script = Join-Path $PSScriptRoot 'audit_phase161_r1_rule_instances.py'
Write-Host "Repository root: $root"
python -B $script
if ($LASTEXITCODE -ne 0) { throw "Phase 161 R1 audit failed (exit code $LASTEXITCODE)." }
Write-Host "Audit succeeded. See phase161_r1_rule_instance_audit\audit_output"
