$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Get-Location).Path
$required = @(
    'phase168_r3_3_proof_narrative_model.py',
    'phase168_r3_4_link_bridge.py',
    'phase165_r52_r9_shared_math.py'
)
foreach ($item in $required) {
    if (-not (Test-Path (Join-Path $root $item))) {
        throw "Required file missing from repository: $item"
    }
}
Copy-Item (Join-Path $folder 'phase168_r3_8_citation_origin.py') -Destination (Join-Path $root 'phase168_r3_8_citation_origin.py') -Force
$original = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $root + [IO.Path]::PathSeparator + $folder + [IO.Path]::PathSeparator + $original
    python -m pytest -q (Join-Path $folder 'tests\test_phase168_r3_8_citation_origin.py')
    if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
    python (Join-Path $folder 'probe.py')
    if ($LASTEXITCODE -ne 0) { throw 'Origin probe failed' }
} finally {
    $env:PYTHONPATH = $original
}
Write-Host 'R3-8 origin audit done. Full test suite not run.'
