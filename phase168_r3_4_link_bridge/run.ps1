$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase168_r3_3_proof_narrative_model.py'))) {
    throw 'R3-3 model missing at repository root. Run phase168_r3_3_narrative_model/run.ps1 first.'
}
Copy-Item (Join-Path $folder 'phase168_r3_4_link_bridge.py') -Destination (Join-Path $root 'phase168_r3_4_link_bridge.py') -Force
Copy-Item (Join-Path $folder 'tests/test_phase168_r3_4_link_bridge.py') -Destination (Join-Path $root 'tests/test_phase168_r3_4_link_bridge.py') -Force
$r33Test = Join-Path $root 'phase168_r3_3_narrative_model\tests\test_phase168_r3_3_proof_narrative_model.py'
$r34Test = Join-Path $folder 'tests\test_phase168_r3_4_link_bridge.py'
if (-not (Test-Path $r33Test)) { throw "R3-3 test not found: $r33Test" }
if (-not (Test-Path $r34Test)) { throw "R3-4 test not found: $r34Test" }
python -m pytest -q $r34Test $r33Test
if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
# Python adds the probe script directory, not the repository root, to sys.path.
# Expose the repository root for this command without changing the user's environment.
$previousPythonPath = $env:PYTHONPATH
try {
    if ($previousPythonPath) {
        $env:PYTHONPATH = $root + [IO.Path]::PathSeparator + $previousPythonPath
    } else {
        $env:PYTHONPATH = $root
    }
    python (Join-Path $folder 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'Diagnostic probe failed' }
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
Write-Host 'R3-4 link adapter installed; Web renderer unchanged; full suite not run.'
