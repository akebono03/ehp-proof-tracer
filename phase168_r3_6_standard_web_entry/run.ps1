$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Get-Location).Path
foreach ($required in @('web_group_proof.py', 'phase165_r52_r3_web_adapter.py', 'phase168_r3_3_proof_narrative_model.py', 'phase168_r3_4_link_bridge.py', 'phase168_r3_5_model_renderer.py')) {
    if (-not (Test-Path (Join-Path $root $required))) { throw "Required repository file missing: $required" }
}
$backup = Join-Path $folder 'backup'
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item (Join-Path $root 'web_group_proof.py') -Destination (Join-Path $backup 'web_group_proof.py') -Force
Copy-Item (Join-Path $folder 'web_group_proof.py') -Destination (Join-Path $root 'web_group_proof.py') -Force
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$root;$previous"
    python -m pytest -q (Join-Path $folder 'tests/test_phase168_r3_6_standard_web_entry.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-6 targeted tests failed' }
    python (Join-Path $folder 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-6 probe failed' }
}
finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-6 standard entry accepts model projection; default long-form unchanged; full suite not run.'
