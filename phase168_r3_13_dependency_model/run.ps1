$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($required in @('phase168_r3_3_proof_narrative_model.py', 'phase168_r3_4_link_bridge.py')) {
    if (-not (Test-Path (Join-Path $project $required))) { throw "Missing prerequisite: $required" }
}
Copy-Item (Join-Path $package 'phase168_r3_13_dependency_model.py') (Join-Path $project 'phase168_r3_13_dependency_model.py') -Force
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$project;$package;$previous"
    python -m pytest -q (Join-Path $package 'tests/test_phase168_r3_13_dependency_model.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-13 targeted tests failed' }
    python (Join-Path $package 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-13 probe failed' }
}
finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-13 dependency projection installed; Search, Renderer, Web unchanged; full suite not run.'
