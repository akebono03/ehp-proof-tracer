$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$script = Join-Path $root 'phase162_r4_b3_full_text_check\check_phase162_r4_b3_full_text.py'
if (-not (Test-Path (Join-Path $root 'toda_group_proof_narrative_renderer.py'))) {
    throw 'Run this script from the EHP Proof Tracer repository root.'
}
if (-not (Test-Path $script)) {
    throw 'The original Phase 162 R4-B3 inspection script was not found. Extract phase162_r4_b3_full_text_check.zip first.'
}
$previousPythonPath = $env:PYTHONPATH
try {
    if ([string]::IsNullOrEmpty($previousPythonPath)) {
        $env:PYTHONPATH = $root
    } else {
        $env:PYTHONPATH = $root + [IO.Path]::PathSeparator + $previousPythonPath
    }
    python -B $script
    if ($LASTEXITCODE -ne 0) {
        throw 'Full-text inspection failed.'
    }
    Write-Host 'Read-only full-text inspection complete. No production files changed.'
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
