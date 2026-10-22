$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Get-Location).Path
foreach ($name in @('phase168_r3_3_proof_narrative_model.py', 'phase168_r3_4_link_bridge.py', 'phase165_r52_r3_web_adapter.py')) {
    if (-not (Test-Path (Join-Path $root $name))) { throw "Required module missing: $name" }
}
Copy-Item (Join-Path $folder 'phase168_r3_7_cutover_gate.py') -Destination (Join-Path $root 'phase168_r3_7_cutover_gate.py') -Force
$oldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = "$root;$oldPythonPath"
    python -m pytest -q (Join-Path $folder 'tests\test_phase168_r3_7_cutover_gate.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-7 targeted tests failed' }
    python (Join-Path $folder 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'R3-7 cutover probe failed' }
}
finally { $env:PYTHONPATH = $oldPythonPath }
Write-Host 'R3-7 citation cutover gate installed; long-form Web route unchanged; full suite not run.'
