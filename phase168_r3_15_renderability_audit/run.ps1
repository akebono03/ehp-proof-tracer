$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($required in @('phase168_r3_3_proof_narrative_model.py','phase168_r3_4_link_bridge.py','phase168_r3_14_reasoned_narrative.py')) {
    if (-not (Test-Path (Join-Path $project $required))) { throw "Missing prerequisite: $required" }
}
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$package;$project;$previous"
    python -m pytest -q (Join-Path $package 'tests/test_phase168_r3_15_renderability_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-15 targeted tests failed' }
    python (Join-Path $package 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-15 audit probe failed' }
} finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-15 AUDIT ONLY; repository unchanged; full suite not run.'
