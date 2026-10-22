$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($required in @('phase168_r3_3_proof_narrative_model.py', 'phase168_r3_12_body_binding.py', 'phase168_r3_5_model_renderer.py')) {
    if (-not (Test-Path (Join-Path $project $required))) { throw "Missing prerequisite: $required" }
}
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$project;$package;$previous"
    python -m pytest -q (Join-Path $package 'tests/test_phase168_r3_12_body_binding.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-12 corrected targeted tests failed' }
    python (Join-Path $package 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-12 search probe failed' }
}
finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-12 TEST EXPECTATION FIX: PASS; production files unchanged; full suite not run.'
