$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($required in @('phase168_r3_3_proof_narrative_model.py', 'phase168_r3_4_link_bridge.py', 'phase168_r3_13_dependency_model.py')) {
    if (-not (Test-Path (Join-Path $project $required))) { throw "Missing prerequisite: $required" }
}
$target = Join-Path $project 'phase168_r3_14_reasoned_narrative.py'
if (Test-Path $target) {
    $backup = Join-Path $package 'backup'
    New-Item -ItemType Directory -Path $backup -Force | Out-Null
    Copy-Item $target (Join-Path $backup 'phase168_r3_14_reasoned_narrative.py') -Force
}
Copy-Item (Join-Path $package 'phase168_r3_14_reasoned_narrative.py') $target -Force
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$project;$package;$previous"
    python -m pytest -q (Join-Path $package 'tests/test_phase168_r3_14_reasoned_narrative.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-14 targeted tests failed' }
    python (Join-Path $package 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-14 probe failed' }
}
finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-14 opt-in narrative diagnostic installed; public Web path unchanged; full suite not run.'
