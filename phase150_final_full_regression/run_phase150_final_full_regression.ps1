$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Final Full Regression"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Documentation changes: none"
Write-Host "Purpose: Phase 150 closure baseline"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Output = Join-Path $ScriptRoot "phase150_final_full_regression_output.txt"

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
    Write-Host ""
    Write-Host "A. Environment snapshot..."
    "Repository: $RepoRoot" | Tee-Object -FilePath $Output
    ("Python: " + (python --version 2>&1)) | Tee-Object -FilePath $Output -Append
    ("Pytest: " + (python -m pytest --version 2>&1)) | Tee-Object -FilePath $Output -Append
    ("Git branch: " + (git branch --show-current 2>&1)) | Tee-Object -FilePath $Output -Append
    ("Git HEAD: " + (git rev-parse HEAD 2>&1)) | Tee-Object -FilePath $Output -Append
    "Git status:" | Tee-Object -FilePath $Output -Append
    git status --short 2>&1 | Tee-Object -FilePath $Output -Append

    Write-Host ""
    Write-Host "B. Running the complete test suite exactly once..."
    $Stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

    python -m pytest tests -q --tb=short 2>&1 |
      Tee-Object -FilePath $Output -Append

    $ExitCode = $LASTEXITCODE
    $Stopwatch.Stop()

    Write-Host ""
    Write-Host "C. Final result..."
    $Elapsed = $Stopwatch.Elapsed
    $ElapsedText = "{0:hh\:mm\:ss\.fff}" -f $Elapsed
    "Pytest exit code: $ExitCode" | Tee-Object -FilePath $Output -Append
    "Wall-clock elapsed: $ElapsedText" | Tee-Object -FilePath $Output -Append
    "Production changes by this package: none" | Tee-Object -FilePath $Output -Append
    "Test changes by this package: none" | Tee-Object -FilePath $Output -Append
    "Documentation changes by this package: none" | Tee-Object -FilePath $Output -Append

    Write-Host ""
    Write-Host "=============================================================="
    if ($ExitCode -eq 0) {
        Write-Host "PHASE 150 FINAL FULL REGRESSION: PASS"
    }
    else {
        Write-Host "PHASE 150 FINAL FULL REGRESSION: FAIL"
    }
    Write-Host "Pytest exit code: $ExitCode"
    Write-Host "Wall-clock elapsed: $ElapsedText"
    Write-Host "Output: $Output"
    Write-Host "=============================================================="

    exit $ExitCode
}
finally {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
