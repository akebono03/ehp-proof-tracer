$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Get-Location).Path
foreach ($required in @('phase165_r52_r3_web_adapter.py', 'phase168_r3_3_proof_narrative_model.py', 'phase168_r3_4_link_bridge.py')) {
    if (-not (Test-Path (Join-Path $root $required))) { throw "Required repository file missing: $required" }
}
$backup = Join-Path $folder 'backup'
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item (Join-Path $root 'phase165_r52_r3_web_adapter.py') -Destination (Join-Path $backup 'phase165_r52_r3_web_adapter.py') -Force
Copy-Item (Join-Path $folder 'phase165_r52_r3_web_adapter.py') -Destination (Join-Path $root 'phase165_r52_r3_web_adapter.py') -Force
Copy-Item (Join-Path $folder 'phase168_r3_5_model_renderer.py') -Destination (Join-Path $root 'phase168_r3_5_model_renderer.py') -Force
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$root;$previous"
    python -m pytest -q (Join-Path $folder 'tests/test_phase168_r3_5_model_web_boundary.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-5 targeted tests failed' }
    python (Join-Path $folder 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-5 probe failed' }
}
finally { $env:PYTHONPATH = $previous }
Write-Host 'R3-5 opt-in model-backed Web boundary installed; default Web route unchanged; full suite not run.'
