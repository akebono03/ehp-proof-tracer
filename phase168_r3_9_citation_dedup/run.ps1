$ErrorActionPreference = "Stop"
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $project "phase168_r3_3_proof_narrative_model.py"
$original = Join-Path $package "phase168_r3_3_proof_narrative_model.py"
if (-not (Test-Path $target)) { throw "R3-3 model is missing: $target" }
if (-not (Test-Path (Join-Path $project "phase168_r3_4_link_bridge.py"))) { throw "R3-4 link adapter is missing" }
$backup = Join-Path $package "backup"
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item $target (Join-Path $backup "phase168_r3_3_proof_narrative_model.py") -Force
Copy-Item $original $target -Force
$env:PYTHONPATH = "$project;$package;$env:PYTHONPATH"
python -m pytest -q (Join-Path $package "tests/test_phase168_r3_9_citation_dedup.py")
if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed" }
python (Join-Path $package "probe.py")
if ($LASTEXITCODE -ne 0) { throw "Probe failed" }
Write-Host "R3-9 citation dedup installed; Web default unchanged; full suite not run."
