$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $repo 'phase161_r5_backward_proof_reconstruction.py'))) {
    throw 'Run from the EHP Proof Tracer repository root.'
}
if (-not (Test-Path (Join-Path $repo 'phase162_pi5_3_backward_selection.py'))) {
    throw 'Phase 162 backward selection module is missing.'
}
$testsPath = Join-Path $repo 'tests'
if (-not (Test-Path (Join-Path $testsPath 'test_phase59_n3_ehp_chain.py'))) {
    throw 'Required Phase 59 tests are missing.'
}
$previousPythonPath = $env:PYTHONPATH
try {
    $paths = @($repo, $testsPath)
    if (-not [string]::IsNullOrEmpty($previousPythonPath)) {
        $paths += $previousPythonPath
    }
    $env:PYTHONPATH = $paths -join ';'
    python -B (Join-Path $PSScriptRoot 'diagnose.py')
    if ($LASTEXITCODE -ne 0) {
        throw "Diagnostic failed: $LASTEXITCODE"
    }
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
Write-Host 'Read-only diagnostic completed; no source files changed.'
