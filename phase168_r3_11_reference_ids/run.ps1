$ErrorActionPreference = "Stop"
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $project "phase168_r3_3_proof_narrative_model.py"
if (-not (Test-Path $target)) { throw "Missing R3-3 model: $target" }
if (-not (Test-Path (Join-Path $project "phase168_r3_4_link_bridge.py"))) { throw "Missing R3-4 bridge adapter" }
$backup = Join-Path $package "backup"
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item $target (Join-Path $backup "phase168_r3_3_proof_narrative_model.py") -Force
Copy-Item (Join-Path $package "phase168_r3_3_proof_narrative_model.py") $target -Force
$env:PYTHONPATH = "$project;$package;$env:PYTHONPATH"
python -m pytest -q (Join-Path $package "tests/test_phase168_r3_9_citation_dedup.py") (Join-Path $package "tests/test_phase168_r3_10_registered_alias.py") (Join-Path $package "tests/test_phase168_r3_11_reference_ids.py")
if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed" }
python (Join-Path $package "probe.py")
if ($LASTEXITCODE -ne 0) { throw "Real search probe failed" }
Write-Host "R3-11 registered identity metadata: PASS; default Renderer unchanged; full suite not run."
