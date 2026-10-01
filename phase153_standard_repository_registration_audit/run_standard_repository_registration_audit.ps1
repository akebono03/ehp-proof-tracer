$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================================="
Write-Host "Standard Repository Registration Audit"
Write-Host "=============================================================================="
Write-Host ""

if (-not (Test-Path (Join-Path $RepoRoot "toda_calculation.py"))) {
    throw "Run this script from C:\Users\oomae\Dropbox\Python\fitz\ehp_proof"
}

$PreviousPythonPath = $env:PYTHONPATH
$PreviousPythonIoEncoding = $env:PYTHONIOENCODING
$PreviousPythonUtf8 = $env:PYTHONUTF8

if ([string]::IsNullOrWhiteSpace($PreviousPythonPath)) {
    $env:PYTHONPATH = $RepoRoot
}
else {
    $env:PYTHONPATH = $RepoRoot + [IO.Path]::PathSeparator + $PreviousPythonPath
}

$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

try {
    Write-Host "A. Syntax check..."
    python -m py_compile `
      (Join-Path $PackageRoot "audit_standard_repository_registration.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "B. Import/API preflight..."
    python -c "import sys, pathlib; sys.path.insert(0, str(pathlib.Path.cwd() / 'tests')); from toda_calculation import _find_specialized_stable_toda_group_results; from test_phase68_pi_n_plus_4_n_zero import build_phase68_10_data; from test_phase70_pi_n_plus_5_n_zero import build_phase70_9_data; print('Registration audit imports passed.')"

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "C. Auditing Standard Repository registration and selection..."
    python `
      (Join-Path $PackageRoot "audit_standard_repository_registration.py")

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "=============================================================================="
    Write-Host "Standard Repository registration audit complete."
    Write-Host "Production files were NOT changed."
    Write-Host "Tests were NOT changed."
    Write-Host "Full pytest was NOT run."
    Write-Host ""
    Write-Host "Please paste the console report."
    Write-Host "=============================================================================="
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONIOENCODING = $PreviousPythonIoEncoding
    $env:PYTHONUTF8 = $PreviousPythonUtf8
}
