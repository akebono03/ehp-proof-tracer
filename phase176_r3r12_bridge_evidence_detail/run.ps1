param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$previous10 = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase176_r3r10_right_zero_transport_isolated\report.json'
$previous11 = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase176_r3r11_isolated_shared_bridge_audit\report.json'
$output = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase176_r3r12_bridge_evidence_detail\report.json'
foreach ($inputPath in @($previous10, $previous11)) {
    if (-not (Test-Path -LiteralPath $inputPath)) { throw "Prior report missing: $inputPath" }
}
$argsList = @((Join-Path $PSScriptRoot 'audit.py'), '--root', $root, '--previous10', $previous10, '--previous11', $previous11, '--output', $output)
if ($DryRun) { $argsList += '--dry-run' }
& python @argsList
if ($LASTEXITCODE -ne 0) { throw 'R3R12 evidence-detail audit failed' }
if (-not $DryRun) {
    & python -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'tests\test_audit.py') (Join-Path $root 'phase175_r4r14r5_public_zero_transport\tests\test_provider.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3R12 focused tests failed' }
}
