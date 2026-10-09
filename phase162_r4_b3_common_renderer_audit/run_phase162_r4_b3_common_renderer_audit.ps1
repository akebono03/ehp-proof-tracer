$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = $PSScriptRoot
$Source = Join-Path $Package 'files'
$Targets = @('phase162_r4_b3_renderer_audit.py', 'tests\test_phase162_r4_b3_common_renderer_audit.py')
foreach ($Item in $Targets) {
    $From = Join-Path $Source $Item
    $To = Join-Path $Root $Item
    $Parent = Split-Path $To -Parent
    New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    Copy-Item -LiteralPath $From -Destination $To -Force
    Write-Host "Updated: $Item"
}
python -B -m pytest -q tests/test_phase162_r4_b3_common_renderer_audit.py tests/test_phase162_r4_b2_replay_integration.py
if ($LASTEXITCODE -ne 0) { throw 'R4-B3 focused tests failed' }
python -B phase162_r4_b3_renderer_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R4-B3 renderer audit failed' }
Write-Host 'R4-B3 common renderer audit complete; no production renderer changes; full suite not run.'
