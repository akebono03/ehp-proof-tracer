param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$previous = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase176_r3r10_right_zero_transport_isolated\report.json'
$output = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase176_r3r11_isolated_shared_bridge_audit\report.json'
if (-not (Test-Path -LiteralPath $previous)) { throw "R3R10 report missing: $previous" }
$python = 'python'
$argsList = @((Join-Path $PSScriptRoot 'audit.py'), '--root', $root, '--previous', $previous, '--output', $output)
if ($DryRun) { $argsList += '--dry-run' }
& $python @argsList
if ($LASTEXITCODE -ne 0) { throw 'R3R11 evidence inventory failed' }
if (-not $DryRun) {
    & $python -m pytest -q (Join-Path $PSScriptRoot 'tests\test_audit.py') (Join-Path $root 'phase175_r4r14r5_public_zero_transport\tests\test_provider.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3R11 focused tests failed' }
}
