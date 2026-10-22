$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($required in @('phase168_r3_3_proof_narrative_model.py', 'phase168_r3_4_link_bridge.py', 'phase168_r3_5_model_renderer.py')) {
    if (-not (Test-Path (Join-Path $project $required))) { throw "Missing prerequisite: $required" }
}
$backup = Join-Path $package 'backup'
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item (Join-Path $project 'phase168_r3_5_model_renderer.py') (Join-Path $backup 'phase168_r3_5_model_renderer.py') -Force
foreach ($name in @('phase168_r3_12_body_binding.py', 'phase168_r3_5_model_renderer.py')) {
    Copy-Item (Join-Path $package $name) (Join-Path $project $name) -Force
}
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$project;$package;$previous"
    python -m pytest -q (Join-Path $package 'tests/test_phase168_r3_12_body_binding.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-12 targeted tests failed' }
    python (Join-Path $package 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-12 search probe failed' }
}
finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-12 body-to-citation binding installed; default long-form Renderer unchanged; full suite not run.'
