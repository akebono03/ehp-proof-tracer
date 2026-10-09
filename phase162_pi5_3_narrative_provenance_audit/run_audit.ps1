$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$required = @(
    'phase162_pi5_3_backward_selection.py',
    'phase162_pi5_3_renderer_audit\phase162_pi5_3_renderer_audit.py',
    'phase161_r5_backward_proof_reconstruction.py'
)
foreach ($relativePath in $required) {
    if (-not (Test-Path (Join-Path $repo $relativePath))) {
        throw "Missing required file at repository root: $relativePath"
    }
}
$previousPythonPath = $env:PYTHONPATH
try {
    $parts = @($repo, (Join-Path $repo 'tests'), (Join-Path $repo 'phase162_pi5_3_renderer_audit'), $PSScriptRoot)
    if (-not [string]::IsNullOrEmpty($previousPythonPath)) {
        $parts += $previousPythonPath
    }
    $env:PYTHONPATH = $parts -join ';'
    python -B (Join-Path $PSScriptRoot 'audit.py')
    if ($LASTEXITCODE -ne 0) {
        throw "Read-only narrative provenance audit failed: $LASTEXITCODE"
    }
    Write-Host 'Read-only audit completed. No pytest or production modifications.'
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
